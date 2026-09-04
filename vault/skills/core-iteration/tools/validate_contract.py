#!/usr/bin/env python3
"""Validate that the six core-iteration skills expose the interface fields
their downstream consumers require.

Usage:
    python3 tools/validate_contract.py [core-iteration-dir]

Exit code 0 = all PASS, 1 = at least one FAIL.
"""
import sys
from pathlib import Path

REQUIREMENTS = {
    "web-research-consensus": {
        "SKILL.md": ["knowledge_gap", "raw_corpus", "search_meta", "搜索预算"],
        "SOURCES.md": [],
        "examples": ["dry_run.md", "smoke_pipeline.md"],
    },
    "benefit-filter": {
        "SKILL.md": ["verified_high_remaining_ratio", "yield_stats", "conflict_branches", "密度评分"],
        "SOURCES.md": [],
    },
    "distillation-consensus": {
        "SKILL.md": ["Node = {", "empty_draft", "蒸馏质量自检分", "触发条件"],
        "SOURCES.md": [],
    },
    "value-iterator": {
        "SKILL.md": ["CHANGELOG.md", "反馈优先级", "增量计数细则", "semver"],
        "SOURCES.md": [],
    },
    "value-validator": {
        "SKILL.md": ["STOP 原因映射", "计算降级", "阈值校准", "stop_reason"],
        "SOURCES.md": [],
    },
    "value-meta-scheduler": {
        "SKILL.md": ["target_skills", "能力评分卡", "收敛预测", "round_ledger", "per_skill_yield", "扩展元能力"],
        "SOURCES.md": [],
    },
    "info-source-adapter": {
        "SKILL.md": ["source_scope_report", "raw_corpus", "适配器", "degradation"],
        "SOURCES.md": [],
    },
    "value-effect-audit": {
        "SKILL.md": ["effect_report", "node_effects", "feedback_to_iterator", "promote"],
        "SOURCES.md": [],
    },
    "return-forensics": {
        "SKILL.md": ["root_cause", "trace_chain", "diagnosis", "yield_diagnosis"],
        "SOURCES.md": [],
    },
    "inspiration-miner": {
        "SKILL.md": ["GitHub", "ideas.json", "suggestion", "tools/mine_ideas.py"],
        "SOURCES.md": [],
    },
}



TOOL_FILES = [
    "validate_contract.py",
    "scorecard.py",
    "behavior_test.py",
    "smoke_test.py",
    "skill_package_check.py",
    "distill_skill_package.py",
    "scaffold_eval_task.py",
    "skilljack_runner.py",
    "benchflow_runner.py",
    "scaffold_dev_spec.py",
    "final_evolution_report.py",
    "info_source_cli.py",
    "run_improve_validate.py",
    "mine_ideas.py",
]

def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    failures = []
    for skill, reqs in REQUIREMENTS.items():
        skill_dir = root / skill
        for file_name, needles in reqs.items():
            if file_name == "examples":
                # Shared examples live at core-iteration/examples
                ex_dir = root / "examples"
                for n in needles:
                    if not (ex_dir / n).exists():
                        failures.append(f"{skill}: examples/{n} missing")
                continue
            path = skill_dir / file_name
            if not path.exists():
                failures.append(f"{skill}: {file_name} missing")
                continue
            text = path.read_text(encoding="utf-8")
            for needle in needles:
                if needle not in text:
                    failures.append(f"{skill}: {file_name} missing '{needle}'")
    for tool in TOOL_FILES:
        if not (root / "tools" / tool).exists():
            failures.append(f"tools/{tool} missing")

    if failures:
        print("FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
