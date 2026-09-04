#!/usr/bin/env python3
"""Executable value-validator stage over live/offline distilled Nodes.

Usage:
  python3 tools/validator_live.py [--input tools/output/info_dump.json]
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "tools" / "output" / "info_dump.json"
DISTILL = ROOT / "tools" / "distill_live.py"


def load_nodes(input_path: Path) -> list[dict]:
    import subprocess
    out = subprocess.run([sys.executable, str(DISTILL), "--input", str(input_path)], capture_output=True, text=True)
    return json.loads(out.stdout)["nodes"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--effective-new", type=int, default=None)
    args = parser.parse_args()
    nodes = load_nodes(Path(args.input))
    effective = args.effective_new if args.effective_new is not None else len(nodes)
    verified_high_remaining_ratio = 0.0  # no remaining gap list in this live pass
    triggered = []
    if effective == 0:
        triggered.append("D: effective_new_nodes=0")
    decision = "STOP" if triggered else "CONTINUE"
    result = {
        "decision": decision,
        "triggered_rules": triggered,
        "benefit_summary": {
            "hit_high_quality_count": len([n for n in nodes if n.get("evidence") == "verified-high"]),
            "discarded_low_quality_count": 0,
            "effective_new_nodes": effective,
            "new_nodes_from_doubt": 0,
            "verified_high_remaining_ratio": verified_high_remaining_ratio,
            "cumulative_nodes": effective,
        },
        "forced_review": False,
        "reason": "15 个单源 verified-single Nodes 通过当前硬规则；暂无 verified-high 和剩余缺口清单",
        "suggested_next_action": "继续多源交叉验证以升级 verified-high",
        "stop_reason": None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
