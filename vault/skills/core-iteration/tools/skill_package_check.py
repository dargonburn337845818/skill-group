#!/usr/bin/env python3
"""Executable skill-package checker (检验底座的可执行层).

Checks a distilled skill directory or a whole skills tree for:
  - frontmatter (name / description)
  - required files (SKILL.md / manifest.json / SOURCES.md or CONSENSUS.md)
  - manifest contract (id/description/scenario/sourceRefs/version/routing)
  - SKILL body has trigger/action/boundary/source discipline
  - examples present, no obvious README-only stub
  - warnings: TODO / 待补 / no version / missing examples

Usage:
  python3 tools/skill_package_check.py <skill-or-root-dir> [more dirs...]
"""
import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_FILES = ["SKILL.md", "manifest.json"]
SOURCE_EVIDENCE_FILES = ["SOURCES.md", "CONSENSUS.md", "README.md"]
BOUNDARY_PATTERNS = [r"^## .*边界", r"^## .*反模式", r"^## .*反例", r"边界", r"不适用", r"失效"]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"<read error: {e}>"


def check_skill(dir_path: Path) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    name = dir_path.name
    skill = (dir_path / "SKILL.md")
    manifest = (dir_path / "manifest.json")

    # Required files
    missing = [f for f in ["SKILL.md", "manifest.json"] if not (dir_path / f).exists()]
    if missing:
        issues.append(f"missing required files: {', '.join(missing)}")
        return {"id": name, "ok": False, "issues": issues, "warnings": warnings, "score": 0}

    text = skill.read_text(encoding="utf-8")
    # Frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not fm_match:
        issues.append("SKILL.md missing YAML frontmatter")
    else:
        fm = fm_match.group(1)
        if "name:" not in fm:
            issues.append("frontmatter missing name")
        if "description:" not in fm:
            issues.append("frontmatter missing description")
        else:
            desc = re.search(r"description:\s*(.+)", fm)
            if desc and len(desc.group(1).strip()) < 20:
                warnings.append("description too short (<20 chars)")
        if "whenToUse" in fm or "whenToUse:" in fm:
            pass
        else:
            warnings.append("frontmatter lacks whenToUse (discoverability hint)")

    # Body quality
    body = text[fm_match.end():] if fm_match else text
    triggers = len(re.findall(r"## 触发|## 何时|触发条件", body))
    actions = len(re.findall(r"^## .*(动作|流程|步骤|动作（)|步骤", body, re.M)) + len(re.findall(r"^\s*(?:[0-9]+\.|[-*])\s", body, re.M))
    boundary_hits = any(re.search(p, body, re.I | re.M) for p in BOUNDARY_PATTERNS)
    source_hits = len(re.findall(r"source_refs|来源|https?://", body))
    if triggers == 0:
        issues.append("body missing trigger section")
    if actions == 0:
        issues.append("body missing actionable steps")
    if not boundary_hits:
        issues.append("body missing boundary/failure-mode section")
    if source_hits == 0:
        issues.append("body missing source_refs/source links")

    # Manifest
    try:
        m = json.loads(manifest.read_text(encoding="utf-8"))
        if m.get("id") != name and m.get("name") != name:
            warnings.append(f"manifest id/name mismatch dir name ({m.get('id')!r} vs {name!r})")
        if not m.get("description"):
            issues.append("manifest missing description")
        if not m.get("scenario"):
            warnings.append("manifest missing scenario")
        if not m.get("sourceRefs"):
            warnings.append("manifest missing sourceRefs")
        if not m.get("version"):
            warnings.append("manifest missing version")
        if m.get("routing") not in ("base", "core", "domain", None):
            warnings.append(f"manifest routing not standard: {m.get('routing')!r}")
    except Exception as e:
        issues.append(f"manifest invalid JSON: {e}")

    # Sources/evidence/version files
    if not any((dir_path / f).exists() for f in SOURCE_EVIDENCE_FILES):
        warnings.append("no SOURCES.md/CONSENSUS.md/README.md evidence file")
    if not (dir_path / "CHANGELOG.md").exists():
        warnings.append("no CHANGELOG.md (version audit)")
    examples = dir_path / "examples"
    if examples.exists():
        if not any(p.is_file() for p in examples.rglob("*")):
            warnings.append("examples dir empty")
    else:
        warnings.append("no examples/ dir (dry-run evidence optional but recommended)")

    # Common warning markers
    for marker in ["TODO", "FIXME", "待补"]:
        if marker in text:
            warnings.append(f"contains marker {marker!r}")

    score = max(0, 100 - len(issues) * 25 - len(warnings) * 5)
    return {
        "id": name,
        "ok": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "score": score,
        "path": str(dir_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="skill dir(s) or root containing skills")
    parser.add_argument("--recursive", action="store_true", help="scan subdirs for SKILL.md when path is a root")
    args = parser.parse_args()

    targets = []
    for p in args.paths:
        path = Path(p)
        if not path.exists():
            print(json.dumps({"ok": False, "error": f"not found: {path}"}, ensure_ascii=False))
            return 2
        if (path / "SKILL.md").exists():
            targets.append(path)
        elif args.recursive:
            targets.extend(d.parent for d in path.rglob("SKILL.md"))
        else:
            targets.extend(d.parent for d in path.glob("*/SKILL.md"))

    results = [check_skill(t) for t in sorted(set(targets), key=str)]
    overall = all(r["ok"] for r in results)
    print(json.dumps({"ok": overall, "results": results}, ensure_ascii=False, indent=2))
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
