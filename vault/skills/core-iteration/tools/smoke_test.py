#!/usr/bin/env python3
"""One-command smoke test for core-iteration.

Runs validate_contract + scorecard + skill_package_check and prints a compact
summary. Exits 0 when all gates pass.
"""
import json
import subprocess
import sys
from pathlib import Path

import scorecard as sc

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    validate = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate_contract.py"), str(ROOT)],
        capture_output=True,
        text=True,
    )
    scorecard = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "scorecard.py"), str(ROOT)],
        capture_output=True,
        text=True,
    )
    behavior = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "behavior_test.py")],
        capture_output=True,
        text=True,
    )
    scores = json.loads(scorecard.stdout) if scorecard.returncode == 0 else {}
    total = sum(v["total"] for v in scores.values())

    checked_dirs = []
    for name in scores:
        d = sc.find_skill_dir(ROOT, name)
        if d:
            checked_dirs.append(str(d))
    pkg = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "skill_package_check.py")] + checked_dirs,
        capture_output=True,
        text=True,
    )
    pkg_data = {}
    if pkg.returncode == 0:
        try:
            pkg_data = json.loads(pkg.stdout)
        except Exception:
            pkg_data = {"ok": False, "error": pkg.stdout[:300]}
    package_ok = bool(pkg_data.get("ok"))

    summary = {
        "contract": validate.stdout.strip(),
        "behavior": behavior.stdout.strip(),
        "package_check": {"ok": package_ok, "results": pkg_data.get("results", [])},
        "scorecard_total": total,
        "scorecard_avg": round(total / len(scores), 2) if scores else None,
        "per_skill": scores,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if validate.returncode == 0 and behavior.returncode == 0 and package_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
