#!/usr/bin/env python3
"""Final evolution report generator.

Combines the extended scorecard, skill-package checks, round ledger yield
curve, and executable-tool inventory into one intuitive evaluation:

  tools/output/EVOLUTION_REPORT.json
  tools/output/EVOLUTION_REPORT.md

Usage:
  python3 tools/final_evolution_report.py [core-iteration-root]
"""
import json
import subprocess
import sys
from pathlib import Path

import scorecard as sc

ROOT = Path(__file__).resolve().parent.parent
DIMENSIONS = {
    "search": ["web-research-consensus", "search-source"],
    "distill": ["distillation-consensus", "value-iterator"],
    "verify": ["value-validator", "skill-verification-consensus", "value-effect-audit"],
    "dev": ["dev-workflow-consensus", "return-forensics", "info-source-adapter"],
    "meta": ["value-meta-scheduler", "benefit-filter"],
}
TOOL_FILES = [
    "validate_contract.py", "scorecard.py", "behavior_test.py", "smoke_test.py",
    "skill_package_check.py", "distill_skill_package.py", "scaffold_eval_task.py",
    "scaffold_dev_spec.py", "info_source_cli.py", "run_improve_validate.py",
    "mine_ideas.py", "meta_report.py", "skill_draft_builder.py", "skilljack_runner.py", "benchflow_runner.py",
]


def score_dimension(scores: dict, names: list[str]) -> float:
    vals = [scores[n]["total"] for n in names if n in scores]
    if not vals:
        return 0.0
    return round(sum(vals) / len(vals) / 20 * 100, 1)


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT.resolve()
    sc_run = subprocess.run([sys.executable, str(root / "tools" / "scorecard.py"), str(root)], capture_output=True, text=True)
    scores = json.loads(sc_run.stdout) if sc_run.returncode == 0 else {}

    # Package-check every scored skill that can be resolved.
    dirs = []
    for name in scores:
        d = sc.find_skill_dir(root, name)
        if d:
            dirs.append(str(d))
    pk_run = subprocess.run([sys.executable, str(root / "tools" / "skill_package_check.py")] + dirs, capture_output=True, text=True)
    pkg_data = {}
    if pk_run.returncode == 0:
        try:
            pkg_data = json.loads(pk_run.stdout)
        except Exception:
            pkg_data = {"ok": False}
    pkg_ok = bool(pkg_data.get("ok"))
    pkg_avg = round(sum(r.get("score", 0) for r in pkg_data.get("results", [])) / max(1, len(pkg_data.get("results", []))), 1)

    dims = {k: score_dimension(scores, v) for k, v in DIMENSIONS.items()}

    ledger_path = root / "round_ledger.json"
    ledger = {}
    if ledger_path.exists():
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    yield_curve = ledger.get("yield_curve", [])
    last_effective = yield_curve[-1].get("effective_new", 0) if yield_curve else 0
    prev_effective = yield_curve[-2].get("effective_new", 0) if len(yield_curve) >= 2 else 0
    marginal = last_effective <= 2 and prev_effective <= 2
    tool_count = sum(1 for t in TOOL_FILES if (root / "tools" / t).exists())

    overall = round(
        0.30 * dims["search"] +
        0.20 * dims["distill"] +
        0.25 * dims["verify"] +
        0.15 * dims["dev"] +
        0.10 * dims["meta"],
        1,
    )
    if pkg_ok:
        overall = round(overall * 0.9 + 100 * 0.1, 1)
    else:
        overall = round(overall * 0.9, 1)

    grade = "A" if overall >= 85 else "B" if overall >= 72 else "C" if overall >= 60 else "D"
    if ledger.get("decision") == "STOP":
        convergence = "已按成本/收益边界收敛（decision=STOP）"
    elif last_effective == 0:
        convergence = "已收敛（有效新增为 0）"
    elif marginal:
        convergence = "已进入收敛区"
    else:
        convergence = "仍可继续进化"

    report = {
        "round": ledger.get("round"),
        "decision": ledger.get("decision"),
        "overall_score": overall,
        "grade": grade,
        "dimensions": dims,
        "scorecard_total": sum(v["total"] for v in scores.values()),
        "scorecard_skills": len(scores),
        "package_check": {"ok": pkg_ok, "avg_score": pkg_avg, "checked": len(dirs)},
        "tool_count": tool_count,
        "tools": [t for t in TOOL_FILES if (root / "tools" / t).exists()],
        "convergence": convergence,
        "yield_tail": yield_curve[-3:],
        "evaluation": {
            "search": "检索/来源链路已工具化并有 evidence_class 贯通" if dims["search"] >= 75 else "搜索仍有提升空间",
            "distill": "蒸馏端已有打包与质检自动化" if dims["distill"] >= 75 else "蒸馏自动化仍可加深",
            "verify": "检验端已有可执行门禁与评测脚手架" if dims["verify"] >= 75 else "验证证据链仍待补齐",
            "dev": "开发端已有规格/路径手册脚手架与深模块强流程" if dims["dev"] >= 75 else "开发流程仍以文档为主",
            "meta": "元能力调度/评分卡可复用" if dims["meta"] >= 75 else "调度自动化仍可增强",
        },
        "next_high_value": [
            "补真实 Skill A/B（skilljack-evals 风格）替换模板增强指数",
            "把 scaffold_eval_task.py 产物接入真实 runner",
            "将 dev/spec 门禁接入 dsh-skill-router 插件（隔离冒烟后）",
        ],
    }

    OUTPUT = root / "tools" / "output"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "EVOLUTION_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 迭代进化终评（Evolution Report）", "",
        f"- **综合评分**: {report['overall_score']} / 100 （{report['grade']} 级）",
        f"- 轮次: Round {report['round']} / {report['decision']}",
        f"- 收敛判断: {report['convergence']}",
        f"- Scorecard: {report['scorecard_total']}/{report['scorecard_skills']*20}（{report['scorecard_skills']} 个 skill）",
        f"- Skill 包检查: {'PASS' if report['package_check']['ok'] else 'FAIL'}，平均 {report['package_check']['avg_score']}/100",
        f"- 可执行工具: {report['tool_count']} 个",
        "",
        "## 维度评分", "",
        "| 维度 | 分数 | 一句话评价 |",
        "|---|---|---|",
    ]
    for k, label in [("search", "搜索"), ("distill", "蒸馏"), ("verify", "检验"), ("dev", "开发"), ("meta", "元能力/调度")]:
        lines.append(f"| {label} | {dims[k]} | {report['evaluation'][k]} |")
    lines += ["", "## 收益尾部", "", "| 轮次 | effective_new | 决策 |", "|---|---|---|"]
    for y in report["yield_tail"]:
        lines.append(f"| {y.get('round')} | {y.get('effective_new')} | {y.get('decision')} |")
    lines += ["", "## 下一步高价值", ""]
    lines += [f"- {x}" for x in report["next_high_value"]]
    (OUTPUT / "EVOLUTION_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
