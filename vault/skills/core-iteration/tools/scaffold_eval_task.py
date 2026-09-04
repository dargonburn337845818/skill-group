#!/usr/bin/env python3
"""Scaffold a Skill eval task package (检验底座的可执行层).

Creates a skilljack-evals-style task directory:

  <task-id>/
    task.md                 # frontmatter + prompt body (prompt never names skill)
    environment/
      skills/<skill-name>/  # mount point; put SKILL.md here
      workspace/            # optional seed files
    verifier/verify.mjs     # deterministic verifier scaffold
    oracle/solve.mjs        # optional reference solution (oracle gate)

Use this before writing/updating a Skill: task first, then SKILL.md.

Usage:
  python3 tools/scaffold_eval_task.py --task-id my-example --skill-name demo-skill --prompt "complete this task" --checks contains:SOME_MARKER files:out.txt
  python3 tools/scaffold_eval_task.py --task-id anti-trigger --skill-name demo-skill --prompt "unrelated request" --anti-trigger
"""
import argparse
import json
import re
from pathlib import Path


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_frontmatter(task_id: str, skill_name: str, anti: bool, checks: list[str], assertions: list[str]) -> dict:
    fm = {
        "id": task_id,
        "difficulty": "medium",
        "category": "skill-eval",
        "tags": [],
        "expected_skill": "none" if anti else skill_name,
        "expect_skill_invocation": "false" if anti else "true",
        "timeout_ms": 300000,
    }
    if checks:
        fm["checks"] = checks
    if assertions:
        fm["assertions"] = assertions
    return fm


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--skill-name", required=True, help="skill under test")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--checks", default="", help="comma/space separated lite checks, e.g. contains:SUCCESS files:out/report.txt")
    parser.add_argument("--assertions", default="", help="comma separated LLM-judge assertions (diagnostic only)")
    parser.add_argument("--anti-trigger", action="store_true", help="generate an anti-trigger task (should NOT invoke skill)")
    parser.add_argument("--out", default="evals")
    args = parser.parse_args()

    check_items = [c.strip() for c in re.split(r"[,;]", args.checks) if c.strip() and ":" in c]
    assertions = [a.strip() for a in re.split(r"[,;]", args.assertions) if a.strip()]
    fm = build_frontmatter(args.task_id, args.skill_name, args.anti_trigger, check_items, assertions)
    task_dir = Path(args.out) / args.task_id

    task_md = "---\n" + json.dumps(fm, ensure_ascii=False, indent=2) + "\n---\n\n" + args.prompt.rstrip() + "\n"
    write_file(task_dir / "task.md", task_md)
    write_file(task_dir / "environment" / "skills" / args.skill_name / ".gitkeep", "")
    write_file(task_dir / "environment" / "workspace" / ".gitkeep", "")
    write_file(
        task_dir / "verifier" / "verify.mjs",
        "// Deterministic verifier: use process.env.SKILLJACK_OUTPUT_FILE / SKILLJACK_TRAJECTORY_FILE\n"
        "// Write reward 0..1 to process.env.SKILLJACK_REWARD_FILE or exit 0/1.\n"
        "import fs from 'node:fs';\n"
        "const out = fs.readFileSync(process.env.SKILLJACK_OUTPUT_FILE || 'output.txt', 'utf8');\n"
        "process.stdout.write(out.includes('SUCCESS_MARKER') ? 'PASS\\n' : 'FAIL\\n');\n"
        "process.exit(out.includes('SUCCESS_MARKER') ? 0 : 1);\n",
    )
    write_file(
        task_dir / "oracle" / "solve.mjs",
        "// Reference solution used by the oracle gate; verifier must yield reward 1.0.\n"
        "import fs from 'node:fs'; fs.writeFileSync('output.txt', 'SUCCESS_MARKER');\n",
    )

    result = {
        "ok": True,
        "task_id": args.task_id,
        "anti_trigger": args.anti_trigger,
        "path": str(task_dir),
        "prompt": args.prompt,
        "checks": check_items,
        "assertions": assertions,
        "next": [
            f"put SKILL.md under {task_dir / 'environment' / 'skills' / args.skill_name}",
            "run no-skill baseline and with-skill trials (>=3 each), record Skill Lift",
            "validate task with oracle gate before treating it as credible",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
