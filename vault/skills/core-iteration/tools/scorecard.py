#!/usr/bin/env python3
"""Automated proxy scorecard for core-iteration skills.

Scores each SKILL.md on 5 dimensions (0-4 each, total 20) using simple
section/keyword heuristics. It is a *proxy* for the rubric in
value-meta-scheduler; the final human/agent score may still differ, but this
gives a fast, reproducible baseline for round-to-round comparison.

Usage:
    python3 tools/scorecard.py [core-iteration-dir]
"""
import json
import re
import sys
from pathlib import Path

SKILLS = [
    "web-research-consensus",
    "search-source",
    "info-source-adapter",
    "benefit-filter",
    "distillation-consensus",
    "value-iterator",
    "value-validator",
    "value-effect-audit",
    "return-forensics",
    "value-meta-scheduler",
    "skill-verification-consensus",
    "dev-workflow-consensus",
]

# Map vault dir name -> file path inside each skill directory.
SKILL_FILE = {
    "web-research-consensus": "SKILL.md",
    "search-source": "SKILL.md",
    "info-source-adapter": "SKILL.md",
    "benefit-filter": "SKILL.md",
    "distillation-consensus": "SKILL.md",
    "value-iterator": "SKILL.md",
    "value-validator": "SKILL.md",
    "value-effect-audit": "SKILL.md",
    "return-forensics": "SKILL.md",
    "value-meta-scheduler": "SKILL.md",
    "skill-verification-consensus": "SKILL.md",
    "dev-workflow-consensus": "SKILL.md",
}


def find_skill_dir(root: Path, name: str) -> Path | None:
    """Resolve skill dir across workspace and vault layouts."""
    candidates = [
        root / name,
        root.parent / name,
        root.parent / "base" / name,
        root / "core-iteration" / "impl" / name,
    ]
    for candidate in candidates:
        if (candidate / SKILL_FILE[name]).exists():
            return candidate
    return None


def score_trigger(text: str) -> int:
    has_trigger = ("## 触发" in text or "## 何时使用" in text or "## 触发条件" in text)
    frontmatter_ok = text.startswith("---") and "description:" in text[:300]
    when_to_use = "whenToUse" in text[:600] or "何时" in text
    if not has_trigger:
        return 0
    if frontmatter_ok and when_to_use:
        return 4
    if frontmatter_ok:
        return 3
    return 2


def score_action(text: str) -> int:
    checkboxes = len(re.findall(r"\[[ xX]\]", text))
    bullets = len(re.findall(r"^\s*[-*]\s", text, re.M))
    numbered = len(re.findall(r"^\s*\d+\.\s", text, re.M))
    code_blocks = len(re.findall(r"```", text)) // 2
    total = checkboxes * 2 + bullets + numbered + code_blocks * 3
    if total >= 60:
        return 4
    if total >= 30:
        return 3
    if total >= 10:
        return 2
    if total > 0:
        return 1
    return 0


def score_boundary(text: str) -> int:
    has_section = bool(re.search(r"^## .*(边界|反模式|反例|防坑)", text, re.M))
    mentions = len(re.findall(r"边界|反例|反模式|失效|不适用", text))
    if not has_section and mentions == 0:
        return 0
    if has_section and mentions >= 8:
        return 4
    if has_section or mentions >= 4:
        return 3
    return 2


def score_traceability(text: str, directory: Path) -> int:
    urls = len(re.findall(r"https?://", text))
    source_refs = len(re.findall(r"source_refs|来源|SOURCES", text))
    has_sources_file = (directory / "SOURCES.md").exists() or (directory / "CONSENSUS.md").exists()
    if urls == 0 and source_refs == 0:
        return 0
    if urls >= 6 and source_refs >= 6 and has_sources_file:
        return 4
    if urls >= 2 or source_refs >= 4:
        return 3
    return 2


def score_integration(text: str, directory: Path) -> int:
    has_input = ("## 输入" in text or "input = {" in text or "## 输入约定" in text)
    has_output = ("## 输出" in text or "## 输出契约" in text or "输出格式" in text)
    has_dryrun = "干跑验证" in text
    has_examples = (directory / "examples").exists() or (Path(directory.parent) / "examples").exists()
    has_group = "core-iteration" in text or "六合一" in text
    score = 0
    if has_input:
        score += 1
    if has_output:
        score += 1
    if has_dryrun:
        score += 1
    if has_examples:
        score += 1
    if has_group:
        score += 1
    return min(score, 4)


def score_skill(name: str, root: Path) -> dict | None:
    skill_dir = find_skill_dir(root, name)
    if skill_dir is None:
        return None
    text = (skill_dir / SKILL_FILE[name]).read_text(encoding="utf-8")
    sub = {
        "trigger": score_trigger(text),
        "action": score_action(text),
        "boundary": score_boundary(text),
        "traceability": score_traceability(text, skill_dir),
        "integration": score_integration(text, skill_dir),
    }
    sub["total"] = sum(sub.values())
    return sub


def main() -> int:
    root = (Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()).resolve()
    if not root.exists():
        print(f"not found: {root}", file=sys.stderr)
        return 1
    result = {}
    for name in SKILLS:
        scored = score_skill(name, root)
        if scored is not None:
            result[name] = scored
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
