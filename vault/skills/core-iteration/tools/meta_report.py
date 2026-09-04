#!/usr/bin/env python3
"""Consolidate all live pipeline stages into one meta report.

Reads/exports from tools/output/info_dump.json and runs the executable stages:
benefit_filter_live, distill_live, iterator_live, validator_live, forensics_live.

Outputs:
  tools/output/META_REPORT.json
  tools/output/META_REPORT.md

Usage:
  python3 tools/meta_report.py [--input tools/output/info_dump.json] [--proxy-mode host] [--offline]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
OUTPUT = ROOT / "tools" / "output"
CURRENT_ROUND = 18


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def parse(cmd, default):
    p = run(cmd)
    try:
        return json.loads(p.stdout)
    except Exception:
        return default


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(OUTPUT / "info_dump.json"))
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--proxy-mode", default="host")
    args = parser.parse_args()

    bf = parse([sys.executable, str(TOOLS / "benefit_filter_live.py"), "--input", args.input], {})
    dl = parse([sys.executable, str(TOOLS / "distill_live.py"), "--input", args.input], {})
    it = parse([sys.executable, str(TOOLS / "iterator_live.py"), "--input", args.input], {})
    vl = parse([sys.executable, str(TOOLS / "validator_live.py"), "--input", args.input], {})
    fr = parse([sys.executable, str(TOOLS / "forensics_live.py"), "--input", args.input], {})
    sc = parse([sys.executable, str(TOOLS / "scorecard.py"), str(ROOT)], {})

    ys = bf.get("yield_stats", {})
    ds = dl.get("distillation_stats", {})
    it_effective = it.get("effective_new_count", 0)
    vl_decision = vl.get("decision", "UNKNOWN")
    converged = vl_decision == "STOP"
    skill_totals = list(sc.values()) if isinstance(sc, dict) else []
    scorecard_percent = round(sum(s.get("total", 0) for s in skill_totals) / max(1, len(skill_totals) * 20) * 100, 1) if skill_totals else 0
    ys0 = bf.get("yield_stats", {})
    high = ys0.get("verified_high_count", 0)
    single = ys0.get("verified_single_count", 0)
    cross_ratio = high / max(1, high + single)
    cross_component = 50 + 50 * min(1.0, cross_ratio / 0.30)
    human_score = round(0.6 * scorecard_percent + 0.4 * cross_component, 0)
    report = {
        "human_score": human_score,
        "scorecard_percent": scorecard_percent,
        "cross_component": round(cross_component, 1),
        "round": CURRENT_ROUND,
        "yield_curve": [{
            "round": CURRENT_ROUND,
            "raw_count": ys.get("raw_count", 0),
            "verified_high": ys.get("verified_high_count", 0),
            "verified_single": ys.get("verified_single_count", 0),
            "nodes": ds.get("total_nodes", 0),
            "effective_new": it_effective,
            "decision": vl_decision,
        }],
        "convergence": {
            "status": "CONVERGED" if converged else "CONTINUING",
            "converged": converged,
            "stop_reason": vl.get("stop_reason"),
            "expected": "已收敛" if converged else "需继续多源交叉验证/扩大主题覆盖",
        },
        "benefit_filter": ys,
        "distillation": ds,
        "iterator": {"accepted": it.get("accepted"), "effective_new_count": it_effective},
        "validator": {"decision": vl_decision, "benefit_summary": vl.get("benefit_summary", {})},
        "forensics": fr.get("diagnosis", {}),
        "recommendation": fr.get("recommendation"),
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "META_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 元能力实时报告", "",
        f"- 直观能力分: {report['human_score']} / 100",
        f"- 轮次: Round {report['round']}",
        f"- 原始语料: {report['yield_curve'][0]['raw_count']}",
        f"- verified_high: {report['benefit_filter'].get('verified_high_count', 0)}",
        f"- verified_single: {report['benefit_filter'].get('verified_single_count', 0)}",
        f"- distilled nodes: {report['distillation'].get('total_nodes', 0)}",
        f"- iterator effective_new: {report['iterator'].get('effective_new_count', 0)}",
        f"- validator decision: {report['validator'].get('decision')}",
        f"- 收敛状态: {report['convergence']['status']}",
        f"- root_cause: {report['forensics'].get('root_cause')}",
        "",
        "## 建议",
        "",
        report["recommendation"] or "",
    ]
    (OUTPUT / "META_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
