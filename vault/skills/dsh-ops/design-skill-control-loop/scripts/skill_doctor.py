#!/usr/bin/env python3
"""skill_doctor — DSH 技能库健康检查（可执行传感器）。

检查一个或多个 skill 目录：
  1. SKILL.md 文件名/frontmatter/目录名一致性
  2. manifest.json 与目录/场景/id 一致性
  3. SKILL.md 是否具备 trigger/action/boundary 纪律
  4. 引用文件是否存在、未引用文件是否残留
  5. CHANGELOG 是否存在
  6. 可选：与 ~/.dsh/skill-vault/enabled.json 交叉核对“启用但缺失/未注册”

用法：
  python3 skill_doctor.py [skill_or_root ...] [--enabled-file PATH] [--json]
默认扫描 ~/work/skills 与 ~/work/dsh-skill-vault/vault/skills。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

HOME = Path.home()
DEFAULT_ROOTS = [
    Path("$HOME/work/skills"),
    Path("$HOME/work/dsh-skill-vault/vault/skills"),
]
DEFAULT_ENABLED_FILE = HOME / ".dsh" / "skill-vault" / "enabled.json"

STATE_WORDS = {"已蒸馏", "已填充", "挂载", "done", "pending", "status"}


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    body = text[3:end]
    data: dict = {}
    for line in body.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip("\"'")
    return data


INTERNAL_PARENT_HINTS = {"subskills", "impl", "tools", "examples", "evals", "benchmarks"}


def is_internal_dir(path: Path) -> bool:
    return any(part in INTERNAL_PARENT_HINTS for part in path.parts)


def check_skill_dir(path: Path, enabled_file: Path | None = None) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    internal = is_internal_dir(path)
    info: dict = {"id": path.name, "path": str(path), "ok": True, "issues": issues, "warnings": warnings, "internal": internal}

    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        issues.append("missing SKILL.md")
        info["ok"] = False
        return info

    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    fm = frontmatter(text)
    name = fm.get("name", "")
    if not internal and name != path.name:
        issues.append(f"frontmatter name '{name}' != dir '{path.name}'")

    if not fm.get("description"):
        warnings.append("frontmatter description missing")

    manifest = path / "manifest.json"
    if not manifest.exists():
        if internal:
            warnings.append("internal package: no independent manifest.json (expected for subskills/impl)")
        else:
            issues.append("missing manifest.json")
    else:
        try:
            m = json.loads(manifest.read_text(encoding="utf-8"))
            if not internal and m.get("id") != path.name:
                issues.append(f"manifest.id '{m.get('id')}' != dir '{path.name}'")
            parent = path.parent.name
            if parent != "skills" and m.get("scenario") != parent and not internal:
                warnings.append(f"manifest.scenario '{m.get('scenario')}' != parent dir '{parent}'")
            tags = m.get("tags") or []
            if len(tags) > 8:
                warnings.append(f"tags > 8 ({len(tags)})")
            bad = [t for t in tags if t in STATE_WORDS or not t.strip()]
            if bad:
                issues.append(f"tags contain state/invalid words: {bad}")
            src = m.get("sourceRefs")
            if not isinstance(src, list) or not src:
                warnings.append("manifest.sourceRefs missing/empty")
        except Exception as e:
            issues.append(f"manifest.json invalid: {e}")

    # trigger/action/boundary discipline
    lower = text.lower()
    has_trigger = any(k in lower for k in ("触发", "when to use", "trigger"))
    has_action = any(k in lower for k in ("动作", "workflow", "action", "步骤"))
    has_boundary = any(k in lower for k in ("边界", "反例", "boundary", "not when", "失效"))
    if not (has_trigger and has_action and has_boundary):
        issues.append(f"SKILL body discipline incomplete: trigger={has_trigger} action={has_action} boundary={has_boundary}")

    # local references actually referenced vs present
    refs_dir = path / "references"
    scripts_dir = path / "scripts"
    if refs_dir.exists():
        ref_names = [p.name for p in refs_dir.iterdir() if p.is_file()]
        link_refs: set[str] = set()
        local_code_refs: set[str] = set()
        # markdown links: strict (must exist if local)
        for m in re.finditer(r"\]\(([^)]+)\)", text):
            ref = m.group(1).strip().split("#")[0].split("?")[0].lstrip("./")
            if ref and not ref.startswith(("http://", "https://")):
                link_refs.add(ref)
        # code spans: only verify skill-local paths (references/..., scripts/...)
        for m in re.finditer(r"`([^`]+)`", text):
            ref = m.group(1).strip().split("#")[0].split("?")[0].lstrip("./")
            if ref.startswith("references/"):
                local_code_refs.add(ref)
            elif ref.startswith("scripts/"):
                local_code_refs.add(ref)
        referenced = link_refs | local_code_refs
        for ref in referenced:
            if ref in ref_names:
                continue
            candidate = path / ref
            if candidate.exists() or (refs_dir / ref).exists() or (scripts_dir / ref).exists():
                continue
            # external/target paths like agent-memory/... are not skill-local references
            if ref.startswith(("agent-memory/", ".github/", "~", "examples/")):
                continue
            issues.append(f"SKILL.md references missing file: {ref}")
        # warn unreferenced reference files
        for ref in ref_names:
            if ref not in referenced and ref not in text:
                warnings.append(f"references/{ref} not referenced by SKILL.md")

    if not (path / "CHANGELOG.md").exists():
        warnings.append("no CHANGELOG.md")

    # enabled cross-check
    if enabled_file and enabled_file.exists():
        try:
            state = json.loads(enabled_file.read_text(encoding="utf-8"))
            skills = state.get("skills", {})
            scenarios = state.get("scenarios", {})
            enabled = skills.get(path.name, False)
            if not enabled and scenarios.get(path.parent.name):
                enabled = True
            info["enabled"] = bool(enabled)
        except Exception:
            warnings.append("enabled file unreadable")

    info["ok"] = not issues
    return info


def find_skill_dirs(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    seen: set[str] = set()
    for p in paths:
        if not p.exists():
            continue
        candidates: list[Path] = []
        if (p / "SKILL.md").exists():
            candidates.append(p)
        else:
            candidates.extend(q.parent for q in p.rglob("SKILL.md") if q.parent != p)
        for c in candidates:
            key = str(c.resolve())
            if key in seen:
                continue
            seen.add(key)
            out.append(c)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--enabled-file", type=Path, default=DEFAULT_ENABLED_FILE)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    roots = args.paths or DEFAULT_ROOTS
    dirs = find_skill_dirs(roots)
    results = [check_skill_dir(d, args.enabled_file) for d in sorted(set(dirs))]
    if args.json:
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
        return 0 if all(r["ok"] for r in results) else 1

    bad = [r for r in results if not r["ok"]]
    for r in results:
        mark = "OK" if r["ok"] else "FAIL"
        print(f"[{mark}] {r['id']} ({r['path']})")
        for issue in r["issues"]:
            print(f"    - {issue}")
        for w in r["warnings"]:
            print(f"    ~ {w}")
    print(f"\n{len(results)} skill(s), {len(bad)} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
