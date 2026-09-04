#!/usr/bin/env python3
"""Quantify how much a skill enhances the model, using an A/B benchmark.

Reference frameworks:
- OpenAI: Testing Agent Skills Systematically with Evals
- Scale: Agentic Leaderboards
- skilljack-evals: discoverability / instruction adherence / output quality

Metrics per task:
  success_without / success_with     (0-1)
  quality_without / quality_with     (0-100)
  efficiency_without / efficiency_with (lower is better: steps/time)
  coverage_without / coverage_with   (0-1)
  calibration_without / calibration_with (0-1)

Output:
  tools/output/ENHANCEMENT_REPORT.json + .md

Usage:
  python3 tools/skill_effect_bench.py --input benchmarks/skill_benchmark_template.json
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "tools" / "output"

PAIRS = [
    ("success", "任务成功率", 0.30),
    ("quality", "输出质量", 0.25),
    ("efficiency", "效率(越少越好)", 0.15),
    ("coverage", "能力覆盖", 0.15),
    ("calibration", "置信校准", 0.15),
]


def avg(vals):
    return sum(vals) / max(1, len(vals))


def skill_grade(ratio):
    if ratio >= 30: return "显著增强"
    if ratio >= 15: return "明显增强"
    if ratio >= 5: return "轻微增强"
    return "近乎无增强"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    tasks = data.get("tasks", data if isinstance(data, list) else [])

    rows = []
    for metric, label, weight in PAIRS:
        without = [float(t.get(f"{metric}_without")) for t in tasks if f"{metric}_without" in t]
        with_ = [float(t.get(f"{metric}_with")) for t in tasks if f"{metric}_with" in t]
        if not without or not with_:
            continue
        w_avg, s_avg = avg(without), avg(with_)
        # efficiency is 'lower better'; invert so gain is positive when lower
        if metric == "efficiency":
            base_gain = (w_avg - s_avg) / max(1.0, w_avg)
            norm_w, norm_s = None, None
        else:
            base_gain = (s_avg - w_avg) / max(1.0, w_avg)
            norm_w = w_avg * 100 if metric in ("success", "coverage", "calibration") else w_avg
            norm_s = s_avg * 100 if metric in ("success", "coverage", "calibration") else s_avg
        rows.append({
            "metric": metric,
            "label": label,
            "weight": weight,
            "without": round(w_avg, 3),
            "with": round(s_avg, 3),
            "without_norm": round(norm_w, 1) if norm_w is not None else None,
            "with_norm": round(norm_s, 1) if norm_s is not None else None,
            "gain": round(base_gain, 3),
            "gain_percent": round(base_gain * 100, 1),
        })

    norm_rows = [r for r in rows if r["without_norm"] is not None]
    norm_weight = sum(r["weight"] for r in norm_rows)
    base_score = sum(r["without_norm"] * r["weight"] for r in norm_rows) / max(1.0, norm_weight)
    skill_score = sum(r["with_norm"] * r["weight"] for r in norm_rows) / max(1.0, norm_weight)
    total_gain = sum(r["gain"] * r["weight"] for r in rows) / sum(r["weight"] for r in rows)
    enhancement_index = total_gain * 100
    grade = skill_grade(enhancement_index)

    result = {
        "tasks": len(tasks),
        "metrics": rows,
        "base_model_score": round(base_score, 1),
        "skill_model_score": round(skill_score, 1),
        "enhancement_index": round(enhancement_index, 1),
        "enhancement_grade": grade,
        "interpretation": f"使用 skill 后综合能力提升 {enhancement_index:.1f}%：{grade}。",
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "ENHANCEMENT_REPORT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Skill 对模型增强评分报告", "",
        f"- 任务数: {result['tasks']}",
        f"- 基准模型分: {result['base_model_score']}",
        f"- 使用 Skill 后: {result['skill_model_score']}",
        f"- 增强指数: {result['enhancement_index']}%",
        f"- 评级: {result['enhancement_grade']}",
        "", "| 指标 | 权重 | 无 Skill | 有 Skill | 增益 |", "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['label']} | {r['weight']} | {r['without']} | {r['with']} | {r['gain_percent']}% |")
    lines += ["", "## 判断标准", "", "- ≥30%: 显著增强", "- 15-30%: 明显增强", "- 5-15%: 轻微增强", "- <5%: 近乎无增强", ""]
    (OUTPUT / "ENHANCEMENT_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
