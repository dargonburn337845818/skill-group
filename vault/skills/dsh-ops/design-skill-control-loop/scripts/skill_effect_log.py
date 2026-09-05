#!/usr/bin/env python3
"""skill_effect_log — 技能效果传感器（轻量记录/统计）。

用于把“技能是否真的被采用/是否带来行为改变/是否误触发”从只读状态变成可审计数据。

数据文件默认：~/.dsh/skill-vault/effect-log.json（可用 DSH_HOME 或 --file 覆盖；不进 git）。

用法：
  # 记录一次使用
  python3 skill_effect_log.py record --skill design-skill-control-loop --task "优化技能库" \
      --triggered true --used true --outcome pos --note "用户采纳了收敛方案"

  # 报表
  python3 skill_effect_log.py report
  python3 skill_effect_log.py stats
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def default_path() -> Path:
    dsh_home = os.environ.get("DSH_HOME")
    if dsh_home:
        return Path(dsh_home) / "skill-vault" / "effect-log.json"
    return Path.home() / ".dsh" / "skill-vault" / "effect-log.json"


def load(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "entries" in data:
            return data["entries"]
        if isinstance(data, list):
            return data
    except Exception:
        return []
    return []


def save(path: Path, entries: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "entries": entries}
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def parse_bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    return str(v).strip().lower() in {"1", "true", "yes", "y", "on"}


def cmd_record(args: argparse.Namespace, path: Path) -> int:
    entries = load(path)
    entry = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "skill": args.skill,
        "task": args.task or "",
        "triggered": parse_bool(args.triggered),
        "used": parse_bool(args.used),
        "outcome": args.outcome,
        "note": args.note or "",
    }
    entries.append(entry)
    save(path, entries)
    print(f"recorded {args.skill} -> {entry['outcome']} ({path})")
    return 0


def cmd_report(args: argparse.Namespace, path: Path) -> int:
    entries = load(path)
    if args.skill:
        entries = [e for e in entries if e["skill"] == args.skill]
    if args.since:
        entries = [e for e in entries if e.get("at", "") >= args.since]
    for e in entries:
        print(f"{e.get('at','')} | {e.get('skill')} | task={e.get('task')} | triggered={e.get('triggered')} used={e.get('used')} outcome={e.get('outcome')} | {e.get('note','')}")
    print(f"\n{len(entries)} entries")
    return 0


def cmd_stats(args: argparse.Namespace, path: Path) -> int:
    entries = load(path)
    if args.skill:
        entries = [e for e in entries if e["skill"] == args.skill]
    by: dict[str, dict[str, int]] = {}
    for e in entries:
        s = e.get("skill", "?")
        row = by.setdefault(s, {"total": 0, "triggered": 0, "used": 0, "pos": 0, "neu": 0, "neg": 0})
        row["total"] += 1
        row["triggered"] += int(bool(e.get("triggered")))
        row["used"] += int(bool(e.get("used")))
        oc = e.get("outcome", "")
        if oc in ("pos", "positive", "+"):
            row["pos"] += 1
        elif oc in ("neg", "negative", "-"):
            row["neg"] += 1
        else:
            row["neu"] += 1
    print(f"{'skill':<32} {'total':>5} {'trig':>5} {'used':>5} {'pos':>5} {'neu':>5} {'neg':>5}")
    for s, row in sorted(by.items()):
        print(f"{s:<32} {row['total']:>5} {row['triggered']:>5} {row['used']:>5} {row['pos']:>5} {row['neu']:>5} {row['neg']:>5}")
    if by:
        total = sum(r["total"] for r in by.values())
        used = sum(r["used"] for r in by.values())
        pos = sum(r["pos"] for r in by.values())
        print(f"\noverall: {total} entries, used={used}, positive={pos}")
        if total:
            print(f"effect_rate={pos / total:.2%}")
    else:
        print("no entries")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="skill effect log")
    ap.add_argument("--file", type=Path, default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("record")
    r.add_argument("--skill", required=True)
    r.add_argument("--task", default="")
    r.add_argument("--triggered", default="false")
    r.add_argument("--used", default="false")
    r.add_argument("--outcome", choices=["pos", "neu", "neg"], default="neu")
    r.add_argument("--note", default="")

    rep = sub.add_parser("report")
    rep.add_argument("--skill", default=None)
    rep.add_argument("--since", default=None)

    st = sub.add_parser("stats")
    st.add_argument("--skill", default=None)

    args = ap.parse_args()
    path = args.file or default_path()
    if args.cmd == "record":
        return cmd_record(args, path)
    if args.cmd == "report":
        return cmd_report(args, path)
    if args.cmd == "stats":
        return cmd_stats(args, path)
    return 1


if __name__ == "__main__":
    sys.exit(main())
