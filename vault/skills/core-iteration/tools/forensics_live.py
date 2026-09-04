#!/usr/bin/env python3
"""Executable return-forensics stage on live/offline corpus.

Diagnoses why the current live yield is only verified-single and proposes the
next action.

Usage:
  python3 tools/forensics_live.py [--input tools/output/info_dump.json]
"""
import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "tools" / "output" / "info_dump.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    items = data.get("raw_corpus", [])
    types = Counter((x.get("source") or {}).get("type") for x in items)
    # Run the real benefit-filter to know actual verified-high/single counts.
    bf = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "benefit_filter_live.py"), "--input", args.input],
        capture_output=True, text=True,
    )
    try:
        bfdata = json.loads(bf.stdout)
        ys = bfdata["yield_stats"]
        verified_high = ys.get("verified_high_count", 0)
        verified_single = ys.get("verified_single_count", 0)
    except Exception:
        verified_high = 0
        verified_single = len(items)
        ys = {}
    if verified_high > 0:
        root_cause = "cross_verification_progress"
        confidence = "medium"
        action = "把已形成的 verified-high 聚合主题扩展成独立知识节点；继续增加不同主题的多源证据"
        recommendation = "已有交叉验证产生 verified-high；下一步是扩大主题覆盖，而不是只增加单源数量"
    else:
        root_cause = "single-source_only"
        confidence = "high"
        action = "对同一主题做多源交叉验证：找多个独立 repo/issue/commit/PR 合并为 verified-high"
        recommendation = "继续开源情报采集，但本轮重点改为多源交叉，而非增加单源数量"
    evidence = [
        f"verified_high={verified_high}",
        f"verified_single={verified_single}",
        f"source_types={dict(types)}",
        f"verified_high_remaining_ratio={ys.get('verified_high_remaining_ratio', 0)}",
    ]
    diagnosis = {
        "root_cause": root_cause,
        "confidence": confidence,
        "evidence": evidence,
        "one_action": action,
    }
    result = {
        "diagnosis": diagnosis,
        "yield_diagnosis": {
            "total_items": len(items),
            "type_distribution": dict(types),
            "verified_high": verified_high,
            "verified_single": verified_single,
        },
        "trace_chains": [x.get("source", {}).get("url") for x in items[:3]],
        "recommendation": recommendation,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
