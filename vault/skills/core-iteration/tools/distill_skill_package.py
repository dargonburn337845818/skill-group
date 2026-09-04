#!/usr/bin/env python3
"""Executable distillation->package generator (蒸馏执行层的打包增强).

Reads a machine-readable nodes JSON (list of verified Nodes with claim,
trigger, action, boundary, source_refs) and writes a complete, publishable
skill package directory:

  SKILL.md / CONSENSUS.md / SOURCES.md / README.md / CHANGELOG.md /
  manifest.json / examples/dry_run.md

Then it runs `skill_package_check.py` on the generated package.

Usage:
  python3 tools/distill_skill_package.py \
    --nodes tools/output/nodes_round22_list.json \
    --id my-skill --title "我的技能" \
    --description "做什么 + 何时触发" \
    --scenario core-iteration --routing base \
    --out /tmp/my-skill
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parent


def slugify(text: str, max_len: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:max_len] or "skill"


def normalize_nodes(raw: list[dict]) -> list[dict]:
    nodes = []
    for i, n in enumerate(raw or []):
        nodes.append({
            "id": n.get("id") or f"node_{i+1}",
            "claim": n.get("claim") or n.get("text") or "",
            "trigger": n.get("trigger") or "当需要应用这条规则时",
            "action": n.get("action") or "回到原始来源并执行可验证步骤",
            "boundary": n.get("boundary") or "单源/未验证；需独立证据",
            "source_refs": n.get("source_refs") or [""],
            "evidence": n.get("evidence", "verified-single"),
            "weight": n.get("weight", 0.5),
            "trace_chain": n.get("trace_chain", []),
        })
    return nodes


def frontmatter(name: str, description: str, when_to_use: str = "") -> str:
    lines = ["---", f"name: {name}", f"description: {description}"]
    if when_to_use:
        lines.append(f"whenToUse: {when_to_use}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def generate_skill_md(nodes: list[dict], title: str) -> str:
    parts = [f"# {title}", "", "> 由 `distill_skill_package.py` 从已验证 Nodes 生成。", "", "## 触发条件", ""]
    seen_triggers = []
    for n in nodes:
        if n["trigger"] not in seen_triggers:
            seen_triggers.append(n["trigger"])
    for t in seen_triggers:
        parts.append(f"- {t}")
    parts += ["", "## 核心动作", ""]
    seen_actions = []
    for n in nodes:
        if n["action"] not in seen_actions:
            seen_actions.append(n["action"])
    for a in seen_actions:
        parts.append(f"- {a}")
    parts += ["", "## 边界", ""]
    seen_boundaries = []
    for n in nodes:
        if n["boundary"] not in seen_boundaries:
            seen_boundaries.append(n["boundary"])
    for b in seen_boundaries:
        parts.append(f"- {b}")
    parts += ["", "## 知识节点", ""]
    for n in nodes:
        parts += [
            f"### {n['id']}",
            f"- claim: {n['claim']}",
            f"- trigger: {n['trigger']}",
            f"- action: {n['action']}",
            f"- boundary: {n['boundary']}",
            f"- evidence: {n['evidence']} (weight {n['weight']})",
            f"- source_refs: {', '.join(n['source_refs'])}",
            "",
        ]
    return "\n".join(parts).rstrip() + "\n"


def generate_consensus(nodes: list[dict], title: str, description: str) -> str:
    parts = [f"# {title}（完整版）", "", f"> {description}", "", "## 一句话共识", "",
             f"```text\n{description}\n```", "", "## 规则明细", ""]
    for n in nodes:
        parts += [
            f"### {n['id']}",
            f"- **触发**：{n['trigger']}",
            f"- **动作**：{n['action']}",
            f"- **边界**：{n['boundary']}",
            f"- **来源**：{', '.join(n['source_refs'])}",
            f"- **证据**：{n['evidence']}（权重 {n['weight']}）",
            "",
        ]
    return "\n".join(parts).rstrip() + "\n"


def generate_sources(nodes: list[dict], source_refs: list[str]) -> str:
    parts = ["# 来源清单", "", "| 来源 | 说明 |", "|---|---|"]
    for s in source_refs:
        parts.append(f"| {s} | 支撑节点来源 |")
    return "\n".join(parts) + "\n"


def generate_manifest(id_: str, description: str, scenario: str, routing: str, source_refs: list[str], version: str) -> dict:
    return {
        "id": id_,
        "name": id_,
        "title": id_.replace("-", " ").title(),
        "description": description,
        "whenToUse": "由节点触发条件汇总；使用前请人工完善。",
        "scenario": scenario,
        "scenarios": [scenario, "base"] if routing == "base" else [scenario],
        "routing": routing,
        "qualityCriteria": {
            "high": ["每条规则有 source_refs", "trigger/action/boundary 三件套齐全"],
            "reject": ["无来源断言", "摘要代替蒸馏"],
            "minIndependentSources": 2,
        },
        "tags": ["蒸馏", "自动生成"],
        "experts": [],
        "sourceRefs": source_refs,
        "activation": "catalog",
        "version": version,
        "license": "MIT",
    }


def write_package(out_dir: Path, nodes: list[dict], id_: str, description: str, scenario: str, routing: str, title: str, version: str) -> dict:
    source_refs = []
    for n in nodes:
        for s in n["source_refs"]:
            if s and s not in source_refs:
                source_refs.append(s)
    out_dir.mkdir(parents=True, exist_ok=True)
    if (out_dir / "SKILL.md").exists():
        # Do not silently overwrite; write into a fresh subdir if collision.
        out_dir = out_dir / "generated"
        out_dir.mkdir(parents=True, exist_ok=True)
    when_to_use = "；".join({n["trigger"] for n in nodes})
    (out_dir / "SKILL.md").write_text(frontmatter(id_, description, when_to_use) + generate_skill_md(nodes, title), encoding="utf-8")
    (out_dir / "CONSENSUS.md").write_text(generate_consensus(nodes, title, description), encoding="utf-8")
    (out_dir / "SOURCES.md").write_text(generate_sources(nodes, source_refs), encoding="utf-8")
    (out_dir / "README.md").write_text(f"# {title}\n\n{description}\n\n> 自动生成，发布前请人工完善来源与示例。\n", encoding="utf-8")
    (out_dir / "CHANGELOG.md").write_text(f"# CHANGELOG\n\n## {version} · 初版\n\n- 由 distill_skill_package.py 自动生成。\n", encoding="utf-8")
    manifest = generate_manifest(id_, description, scenario, routing, source_refs, version)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    examples = out_dir / "examples"
    examples.mkdir(exist_ok=True)
    (examples / "dry_run.md").write_text(
        "# 干跑样例\n\n> 发布前需补 3 个真实 prompt-style 场景与确定性 checks。\n\n| 场景 | 输入 | 预期 | 实际 |\n|---|---|---|---|\n| 1 | ... | ... | ... |\n",
        encoding="utf-8",
    )
    return {"out_dir": str(out_dir), "nodes": len(nodes), "sources": len(source_refs)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nodes", required=True, help="json file with node list")
    parser.add_argument("--id", required=True)
    parser.add_argument("--title", default=None)
    parser.add_argument("--description", required=True)
    parser.add_argument("--scenario", default="core-iteration")
    parser.add_argument("--routing", default="base", choices=["base", "core", "domain"])
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--out", default="/tmp/generated-skill")
    parser.add_argument("--check", action="store_true", default=True)
    args = parser.parse_args()

    raw = json.loads(Path(args.nodes).read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        raw = raw.get("nodes") or raw.get("knowledge_nodes") or list(raw.values())[0] if raw else []
    nodes = normalize_nodes(raw)
    title = args.title or args.id.replace("-", " ").title()
    info = write_package(Path(args.out), nodes, args.id, args.description, args.scenario, args.routing, title, args.version)
    result = {"ok": True, "generated": info}
    if args.check:
        check = subprocess.run(
            [sys.executable, str(TOOLS_DIR / "skill_package_check.py"), info["out_dir"]],
            capture_output=True,
            text=True,
        )
        try:
            check_data = json.loads(check.stdout)
        except Exception:
            check_data = {"ok": False, "error": check.stdout[:500]}
        result["package_check"] = check_data
        result["ok"] = result["ok"] and bool(check_data.get("ok"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
