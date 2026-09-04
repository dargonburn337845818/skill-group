#!/usr/bin/env python3
"""BenchFlow-style matrix runner for Skill A/B evaluation.

This is the orchestration layer on top of `skilljack_runner.py`:
  - one matrix = {tasks} x {no-skill, with-skill} x {runs}
  - each cell invokes the real DeepSeek agent loop
  - aggregates rows into `skill_effect_bench.py` input
  - runs the bench scorer and applies thresholds / CI gate

Usage:
  python3 tools/benchflow_runner.py --config benchflow.yaml
  python3 tools/benchflow_runner.py \
      --task-dir evals/dev-security-enforce --task-dir evals/dev-security-anti \
      --skill-dir vault/skills/dev/dev-security --runs 3 --output bench.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parent.parent


def load_config(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise SystemExit("PyYAML is required for --config")
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        data = yaml.safe_load(text) or {}
    else:
        data = json.loads(text)
    return data


def run_task(task: dict[str, Any], cfg: dict[str, Any], out_path: Path) -> dict[str, Any]:
    """Run one task via skilljack_runner subprocess and return its bench row list."""
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "skilljack_runner.py"),
    ]
    if task.get("yaml"):
        cmd += ["--tasks-yaml", str(task["yaml"])]
    else:
        cmd += ["--task-dir", str(task["dir"])]
    if cfg.get("skill_dir"):
        cmd += ["--skill-dir", str(cfg["skill_dir"])]
    cmd += [
        "--mode", "both",
        "--runs", str(cfg.get("runs", 3)),
        "--model", str(cfg.get("model", "deepseek-chat")),
        "--output", str(out_path),
    ]
    if cfg.get("judge"):
        cmd.append("--judge")
    if cfg.get("verbose"):
        cmd.append("--verbose")
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(Path.cwd()))
    if proc.returncode != 0:
        raise RuntimeError(f"skilljack_runner failed for {task}: {proc.stderr or proc.stdout}")
    data = json.loads(out_path.read_text(encoding="utf-8"))
    return data.get("tasks", [])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="benchflow YAML/JSON config")
    parser.add_argument("--task-dir", action="append", help="scaffold task dir (repeatable)")
    parser.add_argument("--tasks-yaml", action="append", help="skilljack tasks.yaml (repeatable)")
    parser.add_argument("--skill-dir", help="skills directory used by all tasks")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--model", default="deepseek-chat")
    parser.add_argument("--judge", action="store_true")
    parser.add_argument("--output", default="bench_ab.json")
    parser.add_argument("--min-lift-percent", type=float, default=0.0)
    parser.add_argument("--max-discovery-false-positive", type=float, default=0.5,
                        help="max allowed skill activation rate on anti-trigger rows")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.config:
        cfg = load_config(Path(args.config))
        tasks: list[dict[str, Any]] = cfg.get("tasks", [])
        if not tasks:
            raise SystemExit("config tasks must not be empty")
        # normalize config task entries
        normalized = []
        for t in tasks:
            if isinstance(t, str):
                normalized.append({"dir": t} if not t.endswith(".yaml") else {"yaml": t})
            else:
                normalized.append(t)
        tasks = normalized
        output = Path(cfg.get("output", args.output))
        runs = int(cfg.get("runs", args.runs))
        model = str(cfg.get("model", args.model))
        judge = bool(cfg.get("judge", args.judge))
        skill_dir = cfg.get("skill_dir")
        min_lift = float(cfg.get("thresholds", {}).get("min_lift_percent", args.min_lift_percent))
        max_fp = float(cfg.get("thresholds", {}).get("max_discovery_false_positive", args.max_discovery_false_positive))
    else:
        tasks = []
        for td in (args.task_dir or []):
            tasks.append({"dir": td})
        for ty in (args.tasks_yaml or []):
            tasks.append({"yaml": ty})
        if not tasks:
            raise SystemExit("provide --config or --task-dir/--tasks-yaml")
        output = Path(args.output)
        runs = args.runs
        model = args.model
        judge = args.judge
        skill_dir = args.skill_dir
        min_lift = args.min_lift_percent
        max_fp = args.max_discovery_false_positive

    output.parent.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict[str, Any]] = []
    per_task_reports: list[dict[str, Any]] = []
    for idx, task in enumerate(tasks):
        tmp = output.parent / f".cell-{idx}.json"
        rows = run_task(task, {
            "skill_dir": skill_dir,
            "runs": runs,
            "model": model,
            "judge": judge,
            "verbose": args.verbose,
        }, tmp)
        all_rows.extend(rows)
        per_task_reports.append({
            "task": task,
            "rows": rows,
        })
        if args.verbose:
            for r in rows:
                print(f"  task={r.get('id')} without={r.get('success_without')} with={r.get('success_with')} coverage_with={r.get('coverage_with')}", flush=True)
        tmp.unlink(missing_ok=True)

    combined = {
        "name": "skill-ab",
        "model": model,
        "judged": judge,
        "runs": runs,
        "tasks": all_rows,
        "cells": per_task_reports,
    }
    combined_path = output.with_suffix(".combined.json")
    combined_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")

    # Feed into skill_effect_bench.py.
    bench_input = output.with_suffix(".ab.json")
    bench_input.write_text(json.dumps({"tasks": all_rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    bench_proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "skill_effect_bench.py"), "--input", str(bench_input)],
        capture_output=True,
        text=True,
        cwd=str(Path.cwd()),
    )
    bench_data: dict[str, Any] = {}
    if bench_proc.returncode == 0:
        try:
            bench_data = json.loads(bench_proc.stdout)
        except Exception as e:
            bench_data = {"error": f"bench parse failed: {e}", "stdout": bench_proc.stdout[:500]}
    else:
        bench_data = {"error": bench_proc.stderr or bench_proc.stdout}

    # Gates.
    gates: dict[str, Any] = {"passed": True, "reasons": []}
    lift = float(bench_data.get("enhancement_index", 0))
    if lift < min_lift:
        gates["passed"] = False
        gates["reasons"].append(f"enhancement_index {lift:.1f}% < threshold {min_lift:.1f}%")
    fp_rows = [r for r in all_rows if not r.get("expected_skill") and r.get("coverage_with", 0) > max_fp]
    if fp_rows:
        gates["passed"] = False
        gates["reasons"].append(f"anti-trigger rows still loaded skill: {[r['id'] for r in fp_rows]}")

    result = {
        "matrix": combined,
        "bench": bench_data,
        "gates": gates,
    }
    (output.parent / (output.stem + ".result.json")).write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Gates: {'PASS' if gates['passed'] else 'FAIL'}")
    return 0 if gates["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
