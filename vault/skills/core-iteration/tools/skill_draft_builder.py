#!/usr/bin/env python3
"""Build a publishable Skill draft from live/offline distilled Nodes.

Usage:
  python3 tools/skill_draft_builder.py [--input tools/output/info_dump.json]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "tools" / "output"
DISTILL = ROOT / "tools" / "distill_live.py"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(OUTPUT / "info_dump.json"))
    args = parser.parse_args()
    out = subprocess.run([sys.executable, str(DISTILL), "--input", args.input], capture_output=True, text=True)
    data = json.loads(out.stdout)
    nodes = data["nodes"]
    lines = [
        "---",
        "name: live-github-intel",
        "description: 从真实 GitHub 仓库/issue/release/commit/PR 提炼的开源情报与维护性判断规则。",
        "whenToUse: 需要评估/理解 GitHub 开源项目、已知问题、版本变更或提交历史时。",
        "---",
        "",
        "# Live GitHub Intel Skill Draft",
        "",
        "> 本草案由 `skill_draft_builder.py` 从真实 live 语料自动生成，所有 Node 均为 `verified-single`，需要多源交叉验证后才能发布为正式核心知识。",
        "",
        "## 触发条件",
        "",
        "- 需要评估开源仓库的 license/活跃度/生态/topics。",
        "- 需要理解 issue/PR 讨论或 release 变更。",
        "- 需要定位具体 commit/代码变化。",
        "",
        "## 核心动作",
        "",
        "1. 先回到 repo/issue/release/commit 原始 URL。",
        "2. 用 metadata 判断健康度；stars/forks 只当流行度信号。",
        "3. 单源信息标记 verified-single，多源一致才升级 verified-high。",
        "",
        "## 知识节点（Node 列表）",
        "",
    ]
    for n in nodes:
        lines.append(f"### {n['id']}")
        lines.append(f"- claim: {n['claim']}")
        lines.append(f"- trigger: {n['trigger']}")
        lines.append(f"- action: {n['action']}")
        lines.append(f"- boundary: {n['boundary']}")
        lines.append(f"- source_refs: {', '.join(n['source_refs'])}")
        lines.append("")
    lines += ["## 来源与可追溯", "", "- `tools/output/info_dump.json`", "- 每个 Node 的 `trace_chain` 保留原始链路。", ""]
    md = "\n".join(lines)
    (OUTPUT / "SKILL_DRAFT.md").write_text(md, encoding="utf-8")
    (OUTPUT / "skill_draft.json").write_text(json.dumps({"skill_draft": data["skill_draft"], "nodes": nodes}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"nodes": len(nodes), "draft": str(OUTPUT / "SKILL_DRAFT.md")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
