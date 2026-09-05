#!/usr/bin/env python3
"""
DSH subagent/parallelism bound patcher (idempotent, comment-preserving).

Reads the consensus in CONSENSUS.md before running.  It intentionally does
NOT touch a running DSH instance.  Run it from an external terminal, then
restart DSH after confirming `dsh --dump-config` and a real smoke boot in an
isolated DSH_HOME first.

Edits (bounded defaults for a ~8 GB / 20-core machine):
  - profile web cordis.patch.yml:
      agent-loop.maxParallelToolCalls = 8
      jobs.maxConcurrentJobsPerOwner = 8
  - each agent preset (router-standard, router-spec, liangshen):
      tool-subagent.maxDepth = 2
      tool-subagent-fork.maxDepth = 2
      workflow-worker-thread.maxConcurrentAgents = 4
      workflow-worker-thread.maxTotalAgents = 128
      workflow-worker-thread.maxItemsPerCall = 1024

Every modified file is backed up next to it as <file>.bak-<timestamp>.
Use rollback_limits.py to restore the most recent backup set.
"""
from __future__ import annotations

import datetime
import os
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)


class DSHLoader(yaml.SafeLoader):
    """SafeLoader that tolerates Cordis's `!!js` extension tag.

    The tag is evaluated by DSH, not by Python; for structural validation we
    only need the document to remain parseable.
    """


def _js_constructor(loader, tag_suffix, node):  # noqa: ARG001
    return None


DSHLoader.add_multi_constructor("tag:yaml.org,2002:js", _js_constructor)


def validate_yaml(text: str) -> None:
    yaml.load(text, Loader=DSHLoader)

# --------------------------------------------------------------------------
# Desired policy.  Tune these before applying if the machine/budget differs.
# --------------------------------------------------------------------------
PROFILE_CHANGES = {
    "agent-loop": {"maxParallelToolCalls": 8},
    "jobs": {"maxConcurrentJobsPerOwner": 8},
}
# Keys required by a NEW profile row that are not limits we want to force.
PROFILE_NEW_ROW_EXTRA = {
    "agent-loop": {"agents": []},
}
PRESET_CHANGES = {
    "tool-subagent": {"maxDepth": 2},
    "tool-subagent-fork": {"maxDepth": 2},
    "workflow-worker-thread": {
        "maxConcurrentAgents": 4,
        "maxTotalAgents": 128,
        "maxItemsPerCall": 1024,
    },
}
PRESET_NAMES = ["router-standard", "router-spec", "liangshen"]


def home_root() -> Path:
    return Path(os.environ.get("DSH_HOME", str(Path.home() / ".dsh")))


def targets() -> list[Path]:
    root = home_root()
    files = [root / "profiles" / "web" / "cordis.patch.yml"]
    for name in PRESET_NAMES:
        files.append(root / ".agent-presets" / name / "agent.cordis.yml")
    return files


def backup(path: Path) -> Path:
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_name(f"{path.name}.bak-{stamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def find_block(lines: list[str], entry_id: str) -> tuple[int, int] | None:
    """Return (start_line_index, end_line_index) of one YAML list item.

    The item starts at `- id: <entry_id>` and ends just before the next
    sibling list item with the same or smaller indentation.
    """
    pattern = re.compile(r"^(\s*)- id:\s*[\"']?" + re.escape(entry_id) + r"[\"']?\s*$")
    for i, line in enumerate(lines):
        m = pattern.match(line)
        if not m:
            continue
        indent = len(m.group(1))
        start = i
        for j in range(i + 1, len(lines)):
            cur = lines[j]
            if not cur.strip():
                continue
            # A new sibling at the same/smaller indentation ends this block.
            if re.match(r"^\s*- ", cur) and (len(cur) - len(cur.lstrip())) <= indent:
                return start, j
        return start, len(lines)
    return None


def block_indent(lines: list[str], start: int, end: int) -> int:
    m = re.match(r"^(\s*)- ", lines[start])
    return len(m.group(1)) if m else 0


def has_config(lines: list[str], start: int, end: int) -> bool:
    for line in lines[start:end]:
        if re.match(r"^\s*config:\s*$", line):
            return True
    return False


def ensure_config_block(lines: list[str], start: int, end: int, base_indent: int) -> int:
    """Make sure the YAML item has a `config:` mapping; return its end index."""
    for i in range(start, end):
        if re.match(r"^\s*config:\s*$", lines[i]):
            return i
    # Insert `config:` after the `- id` line (or after name line if present).
    insert_at = start + 1
    for i in range(start + 1, end):
        if re.match(r"^\s*name:\s*", lines[i]):
            insert_at = i + 1
            break
    lines.insert(insert_at, f"{' ' * (base_indent + 2)}config:")
    return insert_at


def config_value_lines(lines: list[str], config_idx: int, base_indent: int) -> tuple[int, int]:
    """Return (start, end) of the value lines inside a `config:` mapping."""
    indent = len(lines[config_idx]) - len(lines[config_idx].lstrip())
    start = config_idx + 1
    end = start
    for i in range(start, len(lines)):
        line = lines[i]
        if not line.strip():
            continue
        cur_indent = len(line) - len(line.lstrip())
        if cur_indent <= indent:
            break
        end = i + 1
    return start, end


def set_simple_keys_into_config(
    lines: list[str],
    start: int,
    end: int,
    base_indent: int,
    changes: dict,
) -> list[str] | None:
    """Return new list of lines after applying simple keys to one item's config."""
    config_idx = ensure_config_block(lines, start, end, base_indent)
    value_start, value_end = config_value_lines(lines, config_idx, base_indent)
    config_indent = len(lines[config_idx]) - len(lines[config_idx].lstrip())
    key_indent = config_indent + 2

    existing: dict[str, tuple[int, int]] = {}
    for i in range(value_start, value_end):
        line = lines[i]
        m = re.match(rf"^({' ' * key_indent})([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            existing[m.group(2)] = (i, m.group(3))

    insert_at = value_end
    # Insert before the first blank line that would otherwise end the block,
    # or before a comment?  Keeping it simple: append at the end of the config
    # value region (before any blank separator).
    while insert_at > value_start and not lines[insert_at - 1].strip():
        insert_at -= 1

    out = lines[:]
    has_newline = any(line.endswith("\n") for line in lines[config_idx:value_end])
    # Replace existing keys first.
    for key, value in changes.items():
        rendered = format_yaml_scalar(value)
        suffix = "\n" if has_newline else ""
        if key in existing:
            idx, _ = existing[key]
            if out[idx].endswith("\n"):
                suffix = "\n"
            out[idx] = f"{' ' * key_indent}{key}: {rendered}{suffix}"
        else:
            out.insert(insert_at, f"{' ' * key_indent}{key}: {rendered}{suffix}")
            insert_at += 1
    return out


def format_yaml_scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return "[]" if not value else yaml.safe_dump(value, default_flow_style=True).strip()
    return str(value)


def patch_profile(path: Path) -> list[str] | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    changed = False
    for entry_id, changes in PROFILE_CHANGES.items():
        block = find_block(lines, entry_id)
        if block is None:
            # Append a new top-level entry.  Preserve a trailing newline.
            if lines and not lines[-1].endswith("\n"):
                lines[-1] += "\n"
            lines.append(f"- id: {entry_id}\n")
            lines.append(f"  config:\n")
            for extra_key, extra_value in PROFILE_NEW_ROW_EXTRA.get(entry_id, {}).items():
                lines.append(f"    {extra_key}: {format_yaml_scalar(extra_value)}\n")
            for key, value in changes.items():
                lines.append(f"    {key}: {format_yaml_scalar(value)}\n")
            changed = True
            continue
        start, end = block[0], block[1]
        base_indent = block_indent(lines, start, end)
        before = lines[:]
        updated = set_simple_keys_into_config(lines, start, end, base_indent, changes)
        if updated != before:
            lines = updated
            changed = True
    return lines if changed else None


def patch_preset(path: Path) -> list[str] | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    changed = False
    for entry_id, changes in PRESET_CHANGES.items():
        block = find_block(lines, entry_id)
        if block is None:
            print(f"  WARN: {path.name}: no `{entry_id}` row found; skipped")
            continue
        start, end = block[0], block[1]
        base_indent = block_indent(lines, start, end)
        before = lines[:]
        updated = set_simple_keys_into_config(lines, start, end, base_indent, changes)
        if updated != before:
            lines = updated
            changed = True
    return lines if changed else None


def main() -> int:
    files = targets()
    for path in files:
        if not path.exists():
            print(f"SKIP (missing): {path}")
            continue
        profile = "cordis.patch.yml" in path.name and "profiles" in path.parts
        try:
            updated = patch_profile(path) if profile else patch_preset(path)
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: {path}: {exc}", file=sys.stderr)
            return 1
        if updated is None:
            print(f"NO CHANGE: {path}")
            continue
        # Validate before writing.
        try:
            validate_yaml("".join(updated))
        except Exception as exc:  # noqa: BLE001
            print(f"ABORT: {path} would not parse as YAML: {exc}", file=sys.stderr)
            return 1
        backup_path = backup(path)
        path.write_text("".join(updated), encoding="utf-8")
        print(f"PATCHED: {path}\n  backup: {backup_path}")
    print("\nDone. Next steps:")
    print("  1. Run `dsh --profile web --dump-config` in an isolated/home copy to verify.")
    print("  2. Restart DSH from an external terminal (never while agents are running).")
    print("  3. If something breaks, run `python3 rollback_limits.py`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
