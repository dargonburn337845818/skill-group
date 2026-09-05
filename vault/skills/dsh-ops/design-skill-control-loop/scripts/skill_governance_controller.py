#!/usr/bin/env python3
"""skill_governance_controller — 技能库治理控制器（CLI 版）。

把传感器（effect-log + skill_doctor）读进来，按可检查阈值输出每个 skill 的
治理建议（keep / enable / disable_or_demote / reduce_trigger / fix / no_data /
merge_candidate），并读取 agent-memory/open-changes.json 做流量控制。

命令：
  suggest               生成治理建议（默认）
  init                  初始化 agent-memory/skill-governance.md 与 open-changes.json
  flow list|add|close   管理开放变更（流量控制）

用法示例：
  python3 skill_governance_controller.py suggest --repo $HOME/work/dsh-skill-vault
  python3 skill_governance_controller.py flow add --skill design-skill-control-loop
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def default_dsh_home() -> Path:
    return Path(os.environ.get("DSH_HOME") or Path.home() / ".dsh")


def default_effect_path() -> Path:
    return default_dsh_home() / "skill-vault" / "effect-log.json"


def default_enabled_path() -> Path:
    return default_dsh_home() / "skill-vault" / "enabled.json"


def load_json(path: Path, fallback: Any = None) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def load_effects(path: Path) -> list[dict[str, Any]]:
    data = load_json(path, fallback=[])
    if isinstance(data, dict):
        data = data.get("entries", [])
    return data if isinstance(data, list) else []


def load_enabled(path: Path) -> dict[str, Any]:
    data = load_json(path, fallback={}) or {}
    return data if isinstance(data, dict) else {}


def enabled_ids(enabled: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    skills = enabled.get("skills") or {}
    scenarios = enabled.get("scenarios") or {}
    for k, v in skills.items():
        if v:
            out.add(k)
    return out | {k for k, v in scenarios.items() if v}


def load_open_changes(repo: Path) -> list[str]:
    path = repo / "agent-memory" / "open-changes.json"
    data = load_json(path, fallback=[])
    if isinstance(data, dict):
        data = data.get("open") or data.get("changes") or []
    return [str(x.get("skill") if isinstance(x, dict) else x) for x in data] if isinstance(data, list) else []


def write_open_changes(repo: Path, changes: list[dict[str, Any]]) -> None:
    path = repo / "agent-memory" / "open-changes.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"version": 1, "open": changes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def effect_metrics(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by: dict[str, dict[str, Any]] = {}
    latest: dict[str, str] = {}
    for e in entries:
        s = str(e.get("skill", "?"))
        row = by.setdefault(s, {"total": 0, "triggered": 0, "used": 0, "pos": 0, "neu": 0, "neg": 0})
        row["total"] += 1
        row["triggered"] += int(bool(e.get("triggered")))
        row["used"] += int(bool(e.get("used")))
        oc = e.get("outcome", "neu")
        if oc == "pos":
            row["pos"] += 1
        elif oc == "neg":
            row["neg"] += 1
        else:
            row["neu"] += 1
        at = e.get("at", "")
        if not latest.get(s) or at > latest[s]:
            latest[s] = at
    for s, row in by.items():
        row["effectRate"] = row["pos"] / row["total"] if row["total"] else 0
        row["misuseRate"] = max(0.0, (row["triggered"] - row["used"]) / row["triggered"]) if row["triggered"] else 0
        row["lastAt"] = latest.get(s)
    return by


def doctor_results(repo: Path) -> list[dict[str, Any]]:
    """Run the local doctor.py over the vault and return public rows only."""
    doctor_script = Path(__file__).parent / "skill_doctor.py"
    vault = repo / "vault" / "skills"
    if not vault.exists() or not doctor_script.exists():
        return []
    import subprocess
    out = subprocess.run(
        [sys.executable, str(doctor_script), str(vault), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if out.returncode not in (0, 1):
        return []
    try:
        payload = json.loads(out.stdout)
    except Exception:
        return []
    # Keep only non-internal public rows, normalized to TS DoctorIssue row
    # (skill_doctor.py returns `id`; the controller uses `skill`).
    return [
        {**r, "skill": r.get("id", r.get("skill", ""))}
        for r in payload.get("results", [])
        if not r.get("internal") and r.get("skill") or r.get("id")
    ]


def decide(skill: str, meta: dict[str, Any], enabled: bool, doctor: dict[str, Any] | None,
           open_changes: set[str]) -> list[dict[str, str]]:
    if skill in open_changes:
        return [{"action": "flow_control", "reason": "already has an open governance change; close it first"}]
    total = meta.get("total", 0)
    effect_rate = meta.get("effectRate", 0)
    misuse_rate = meta.get("misuseRate", 0)
    evidence = total >= 3
    actions: list[dict[str, str]] = []
    issues = doctor.get("issues", []) if doctor else []
    if issues:
        actions.append({"action": "fix", "reason": "doctor issues: " + "; ".join(issues)})
    if not evidence and not enabled:
        actions.append({"action": "merge_candidate", "reason": "no effect data; possibly redundant"})
    if not evidence:
        actions.append({"action": "no_data", "reason": "no effect entries yet" if total == 0 else "effect sample < 3"})
    elif enabled:
        if effect_rate < 0.4:
            actions.append({"action": "disable_or_demote", "reason": f"effect_rate={effect_rate:.1%} < 40%"})
        if misuse_rate > 0.3:
            actions.append({"action": "reduce_trigger", "reason": f"misuse_rate={misuse_rate:.1%} > 30%"})
        if effect_rate >= 0.4 and misuse_rate <= 0.3:
            actions.append({"action": "keep", "reason": f"effect_rate={effect_rate:.1%}, misuse_rate={misuse_rate:.1%}"})
    else:
        if effect_rate >= 0.5 and misuse_rate <= 0.3:
            actions.append({"action": "enable", "reason": f"effect_rate={effect_rate:.1%} >= 50%, misuse_rate={misuse_rate:.1%}"})
        else:
            actions.append({"action": "no_data", "reason": "disabled and insufficient positive evidence"})
    seen: set[str] = set()
    out = []
    for a in actions:
        if a["action"] in seen:
            continue
        seen.add(a["action"])
        out.append(a)
    return out


def cmd_suggest(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    entries = load_effects(default_effect_path())
    enabled = load_enabled(default_enabled_path())
    open_changes = set(load_open_changes(repo))
    metrics = effect_metrics(entries)

    # Catalog: from vault directory names + enabled state (simplified; uses
    # manifest if present).
    catalog: list[dict[str, Any]] = []
    vault = repo / "vault" / "skills"
    if vault.exists():
        for scenario in sorted(p for p in vault.iterdir() if p.is_dir()):
            for skill_dir in sorted(p for p in scenario.iterdir() if (p / "SKILL.md").exists()):
                catalog.append({"id": skill_dir.name, "scenario": scenario.name})

    # Expand scenario-level switches to actual skill ids, then mark enabled.
    sk = enabled.get("skills") or {}
    sc = enabled.get("scenarios") or {}
    enabled_set = {k for k, v in sk.items() if v}
    for sc_id, v in sc.items():
        if v:
            enabled_set.update(c["id"] for c in catalog if c["scenario"] == sc_id)
    for c in catalog:
        c["enabled"] = c["id"] in enabled_set

    doctors = {d["skill"]: d for d in doctor_results(repo)}
    rows = []
    for c in catalog:
        skill = c["id"]
        meta = metrics.get(skill, {})
        dr = doctors.get(skill)
        rows.append({
            "skill": skill,
            "scenario": c["scenario"],
            "enabled": c["enabled"],
            "total": meta.get("total", 0),
            "effectRate": meta.get("effectRate", 0),
            "misuseRate": meta.get("misuseRate", 0),
            "lastAt": meta.get("lastAt"),
            "doctorOk": dr.get("ok", True) if dr else True,
            "doctorIssues": dr.get("issues", []) if dr else [],
            "openChange": skill in open_changes,
            "actions": decide(skill, meta, c["enabled"], dr, open_changes),
        })

    actionable = [r for r in rows if any(a["action"] not in ("keep", "no_data", "merge_candidate") for a in r["actions"])]
    report = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "enabledCount": len(enabled_set),
        "catalogCount": len(catalog),
        "totalEntries": len(entries),
        "effectLogPath": str(default_effect_path()),
        "openChanges": sorted(open_changes),
        "actions": actionable,
        "rows": rows,
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"技能库治理报告：{report['enabledCount']}/{report['catalogCount']} 已启用")
    print(f"效果日志：{report['totalEntries']} 条（{report['effectLogPath']}）")
    print(f"开放变更：{', '.join(sorted(open_changes)) if open_changes else '无'}")
    print(f"建议动作：{len(actionable)} 项")
    for r in actionable:
        acts = "; ".join(f"{a['action']}: {a['reason']}" for a in r["actions"])
        print(f"  - {r['skill']}（{'启用' if r['enabled'] else '停用'}）total={r['total']} effect={r['effectRate']:.1%} misuse={r['misuseRate']:.1%} | {acts}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    mem_dir = repo / "agent-memory"
    mem_dir.mkdir(parents=True, exist_ok=True)
    mem = mem_dir / "skill-governance.md"
    if not mem.exists():
        template = Path(__file__).parent.parent / "references" / "skill-governance-memory-template.md"
        if template.exists():
            mem.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            mem.write_text("# Skill Governance Memory\n\n## 金标准\n\n## 已知误触发 / 假阳性\n\n## 用户偏好与覆盖\n\n## 待验证 / 低置信\n\n## 流量控制\n\n## 最近一次治理\n", encoding="utf-8")
        print(f"created {mem}")
    else:
        print(f"exists {mem}")

    changes = mem_dir / "open-changes.json"
    if not changes.exists():
        write_open_changes(repo, [])
        print(f"created {changes}")
    else:
        print(f"exists {changes}")
    return 0


def cmd_flow(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    current = load_open_changes(repo)
    if args.flow == "list":
        print("\n".join(current) if current else "no open changes")
        return 0
    if args.flow == "add":
        if not args.skill:
            print("error: --skill required", file=sys.stderr)
            return 1
        if args.skill in current:
            print(f"already open: {args.skill}")
        else:
            current.append(args.skill)
            write_open_changes(repo, [{"skill": s, "openedAt": datetime.now(timezone.utc).isoformat(timespec="seconds")} for s in current])
            print(f"added {args.skill}")
        return 0
    if args.flow == "close":
        if args.skill not in current:
            print(f"not open: {args.skill}")
            return 1
        current = [s for s in current if s != args.skill]
        write_open_changes(repo, [{"skill": s, "openedAt": ""} for s in current])
        print(f"closed {args.skill}")
        return 0
    print("unknown flow command", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="skill governance controller")
    ap.add_argument("--repo", default=str(Path("$HOME/work/dsh-skill-vault")), help="skill vault repo root")
    ap.add_argument("--json", action="store_true", help="json output for suggest")
    sub = ap.add_subparsers(dest="cmd")

    ap_suggest = sub.add_parser("suggest")
    ap_suggest.set_defaults(cmd=cmd_suggest)

    ap_init = sub.add_parser("init")
    ap_init.set_defaults(cmd=cmd_init)

    ap_flow = sub.add_parser("flow")
    ap_flow.add_argument("flow", choices=["list", "add", "close"])
    ap_flow.add_argument("--skill", default=None)
    ap_flow.set_defaults(cmd=cmd_flow)

    args = ap.parse_args()
    if not hasattr(args, "cmd"):
        args.cmd = cmd_suggest
    return args.cmd(args)


if __name__ == "__main__":
    sys.exit(main())
