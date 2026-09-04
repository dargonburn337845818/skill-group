#!/usr/bin/env python3
"""Executable value-iterator stage over live/offline distilled Nodes.

Usage:
  python3 tools/iterator_live.py [--input tools/output/info_dump.json]
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "tools" / "output" / "info_dump.json"
DISTILL = ROOT / "tools" / "distill_live.py"


def load_nodes(input_path: Path) -> list[dict]:
    out = subprocess_run([sys.executable, str(DISTILL), "--input", str(input_path)])
    data = json.loads(out.stdout)
    return data["nodes"]


def subprocess_run(cmd):
    import subprocess
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--old-nodes", default=None)
    args = parser.parse_args()
    nodes = load_nodes(Path(args.input))
    old = []
    if args.old_nodes:
        old = json.loads(Path(args.old_nodes).read_text(encoding="utf-8"))
    old_ids = {n.get("id") for n in old}
    added = [n for n in nodes if n.get("id") not in old_ids]
    effective_new_count = len(added)
    changelog_lines = [
        "## 变更日志 live-draft",
        "",
        "### Added (有效新增)",
        "| node_id | claim 摘要 | 证据 | 来源 | 权重 | 对应缺口 |",
        "|---|---|---|---|---|---|",
    ]
    for n in added:
        changelog_lines.append(
            f"| {n['id']} | {n['claim'][:60]} | {n['evidence']} | {n['source_refs'][0] if n['source_refs'] else '-'} | {n['weight']} | - |"
        )
    changelog = "\n".join(changelog_lines)
    result = {
        "accepted": effective_new_count > 0,
        "signal": "ok",
        "effective_new_count": effective_new_count,
        "footnote_added_count": 0,
        "node_delta": {
            "added": [n["id"] for n in added],
            "updated": [],
            "merged": [],
            "removed": [],
            "footnotes": [],
        },
        "changelog": changelog,
        "risk_notes": ([
            f"含 {sum(1 for n in nodes if n.get('evidence') == 'verified-high')} 个 verified-high（多源交叉验证），仍建议继续扩大独立来源"
        ] if any(n.get("evidence") == "verified-high" for n in nodes) else [
            "全部为 verified-single，无 verified-high；需要后续多源交叉验证"
        ]),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
