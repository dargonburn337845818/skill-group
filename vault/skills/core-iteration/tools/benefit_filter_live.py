#!/usr/bin/env python3
"""Execute a live/offline benefit-filter pass over info_source_cli output.

This is the executable counterpart of the `benefit-filter` skill. It reads
`tools/output/info_dump.json` (or another raw_corpus dump), applies a simple
quality/density gate, and produces the exact output contract used by
distillation-consensus: verified_high / pending_verification /
discarded_low_density / yield_stats.

For the current live corpus every item is single-source (one GitHub repo,
issue, release, commit or PR), so they are marked verified-single with weight
0.5 unless multiple independent sources are supplied later.

Usage:
  python3 tools/benefit_filter_live.py [--input tools/output/info_dump.json]
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "tools" / "output" / "info_dump.json"


def quality_of(item: dict) -> tuple[int, list[str]]:
    t = item.get("source", {}).get("type", "")
    meta = item.get("metadata") or {}
    notes = []
    score = 0
    if t == "github":
        if not meta.get("archived"): score += 20; notes.append("not archived")
        if meta.get("license"): score += 20; notes.append("license")
        pushed = meta.get("pushed_at") or ""
        if pushed and "2024" not in pushed and "2023" not in pushed:
            score += 20; notes.append("recently pushed")
        if meta.get("language"): score += 10; notes.append("language")
        if len(meta.get("topics", [])) >= 3: score += 10; notes.append("topics")
        if meta.get("stars"): notes.append("stars are popularity only")
    elif t in ("github_issue", "github_pr"):
        score = 50
        if meta.get("state") == "open": score += 20; notes.append("open")
        if (meta.get("comments") or 0) >= 3: score += 20; notes.append("discussion")
        if meta.get("labels"): score += 10; notes.append("labels")
    elif t == "github_release":
        score = 70
        if not meta.get("draft"): score += 20; notes.append("not draft")
        if meta.get("tag_name"): score += 10; notes.append("tag")
    elif t == "github_commit":
        score = 70
        if meta.get("message"): score += 20; notes.append("message")
        if meta.get("sha"): score += 10; notes.append("sha")
    else:
        score = 50; notes.append("no metadata heuristic")
    return min(score, 100), notes


def cross_verify(items: list[dict]) -> list[dict]:
    """Turn multiple independent GitHub repos sharing a topic into verified-high."""
    from collections import defaultdict
    topic_map = defaultdict(list)
    for item in items:
        meta = item.get("metadata") or {}
        if item.get("source", {}).get("type") != "github":
            continue
        for topic in meta.get("topics", []) or []:
            if topic:
                topic_map[topic.lower()].append(item)
    language_map = defaultdict(list)
    for item in items:
        if item.get("source", {}).get("type") != "github":
            continue
        lang = (item.get("metadata") or {}).get("language")
        if lang:
            language_map[lang.lower()].append(item)
    aggregates = []
    for topic, group in topic_map.items():
        urls = sorted({item.get("source", {}).get("url") for item in group if item.get("source", {}).get("url")})
        if len(urls) >= 2:
            aggregates.append({
                "chunk_id": f"cross_{topic}",
                "claim": f"多个独立开源项目围绕主题【{topic}】活跃（{len(urls)} 个独立仓库）",
                "density_score": 90,
                "verdict": "verified-high",
                "independent_sources": urls,
                "source_count": len(urls),
                "weight": 1.0,
                "gap_id": None,
                "quality_notes": ["multiple independent repos share topic"],
            })
    for lang, group in language_map.items():
        urls = sorted({item.get("source", {}).get("url") for item in group if item.get("source", {}).get("url")})
        if len(urls) >= 3:
            aggregates.append({
                "chunk_id": f"cross_lang_{lang}",
                "claim": f"多个独立项目使用语言【{lang}】，形成活跃技术生态（{len(urls)} 个独立仓库）",
                "density_score": 85,
                "verdict": "verified-high",
                "independent_sources": urls,
                "source_count": len(urls),
                "weight": 1.0,
                "gap_id": None,
                "quality_notes": ["multiple independent repos share language"],
            })
    return aggregates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    items = data.get("raw_corpus", data if isinstance(data, list) else [])

    verified = []
    discarded = []
    pending = []
    for item in items:
        score, notes = quality_of(item)
        src = item.get("source", {})
        entry = {
            "chunk_id": item.get("chunk_id"),
            "claim": item.get("claim", ""),
            "density_score": score,
            "verdict": "verified-single" if score >= 60 else "single-doubt",
            "independent_sources": [src.get("url")],
            "source_count": 1,
            "weight": 0.5 if score >= 60 else 0.0,
            "gap_id": item.get("gap_id"),
            "quality_notes": notes,
        }
        if score >= 60:
            verified.append(entry)
        else:
            pending.append({**entry, "reason": "quality below 60", "suggested_action": "外部补源/人工复核"})

    verified += cross_verify(items)
    verified_high_count = sum(1 for x in verified if x["verdict"] == "verified-high")
    verified_single_count = sum(1 for x in verified if x["verdict"] == "verified-single")
    yield_stats = {
        "raw_count": len(items),
        "density_pass": len(verified),
        "verified_high_count": verified_high_count,
        "verified_single_count": verified_single_count,
        "pending_count": len(pending),
        "discarded_count": len(discarded),
        "avg_density_score": round(sum(x["density_score"] for x in verified) / max(1, len(verified)), 1),
        "remaining_verified_high": verified_high_count,
        "remaining_gap_count": 0,
        "verified_high_remaining_ratio": verified_high_count / max(1, verified_high_count + verified_single_count),
    }
    result = {
        "verified_high": verified,
        "conflict_branches": [],
        "pending_verification": pending,
        "discarded_low_density": discarded,
        "yield_stats": yield_stats,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
