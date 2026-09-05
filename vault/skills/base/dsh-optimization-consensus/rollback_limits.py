#!/usr/bin/env python3
"""Roll back the most recent apply_limits.py backup for each DSH config file.

Run this from an external terminal if the bounded subagent configuration
causes startup/tooling problems.  Restores only the newest `*.bak-*` found
next to each target; it does not touch the running process.
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def home_root() -> Path:
    return Path(os.environ.get("DSH_HOME", str(Path.home() / ".dsh")))


def targets() -> list[Path]:
    root = home_root()
    files = [root / "profiles" / "web" / "cordis.patch.yml"]
    for name in ("router-standard", "router-spec", "liangshen"):
        files.append(root / ".agent-presets" / name / "agent.cordis.yml")
    return files


def newest_backup(path: Path) -> Path | None:
    candidates = sorted(path.parent.glob(f"{path.name}.bak-*"), key=lambda p: p.stat().st_mtime)
    return candidates[-1] if candidates else None


def main() -> int:
    restored = 0
    for path in targets():
        if not path.exists():
            continue
        backup = newest_backup(path)
        if backup is None:
            print(f"NO BACKUP: {path} (nothing restored)")
            continue
        shutil.copy2(backup, path)
        print(f"RESTORED: {path} <- {backup}")
        restored += 1
    if restored == 0:
        print("No backups found; nothing was restored.")
    print("\nNow verify with `dsh --profile web --dump-config` and restart DSH externally.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
