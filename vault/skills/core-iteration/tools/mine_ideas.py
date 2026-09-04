#!/usr/bin/env python3
"""GitHub as an inspiration factory: mine plugin/skill/meta-capability ideas.

One tool, three modes:
  --category all     general inspiration mining (default)
  --category plugin  DSH/agent plugin market candidates
  --category skill   agent skill ecosystem candidates

Emits JSON + Markdown under tools/output/.

Usage:
  python3 tools/mine_ideas.py [--offline] [--proxy-mode host] [--limit 6]
  python3 tools/mine_ideas.py --category plugin --proxy-mode host --limit 6
  python3 tools/mine_ideas.py --category skill --proxy-mode host --limit 6
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
OUTPUT = ROOT / "tools" / "output"

CATEGORIES = {
    "all": {
        "queries": [
            "topic:agent-skills", "topic:llm-plugin", "topic:dsh", "topic:ai-assistant",
            "topic:skill-management", "topic:cli plugin agent",
        ],
        "keywords": {
            "dsh": 3, "deepseek-harness": 3, "skill": 3, "skills": 3, "plugin": 2,
            "agent": 2, "workflow": 1, "cli": 1, "knowledge": 1, "eval": 1,
            "recursive": 2, "self-improve": 2, "toolkit": 2, "harness": 2, "automation": 1,
        },
        "file": "ideas",
        "title": "GitHub 灵感挖掘（Plugin / Meta-capability Ideas）",
    },
    "plugin": {
        "queries": ["topic:dsh-plugin", "topic:deepseek-harness", "topic:dsh", "topic:agent-plugin", "topic:harness"],
        "keywords": {"dsh": 3, "deepseek": 2, "harness": 3, "plugin": 3, "agent": 2, "extension": 1},
        "file": "plugin_market",
        "title": "Plugin Market Candidates",
    },
    "skill": {
        "queries": ["topic:agent-skills", "topic:claude-skills", "topic:skills", "topic:skill-management", "topic:ai-assistant"],
        "keywords": {"skill": 3, "skills": 3, "agent": 2, "cli": 1, "workflow": 1, "plugin": 1},
        "file": "skill_market",
        "title": "Skill Market Candidates",
    },
}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def score_repo(item, keywords):
    src = item.get("source", {})
    meta = item.get("metadata", {})
    text = " ".join([
        src.get("title", ""), src.get("claim", ""), item.get("text", ""),
        " ".join(meta.get("topics", []) or []),
    ]).lower()
    score = 0
    hits = []
    for kw, weight in keywords.items():
        if kw in text:
            score += weight
            hits.append(kw)
    return score, hits


def suggestion(item):
    src = item.get("source", {})
    meta = item.get("metadata", {})
    title = src.get("title", "")
    desc = (src.get("claim") or item.get("text") or "")[:160]
    topics = meta.get("topics", []) or []
    if "dsh" in title.lower() or "deepseek-harness" in (topics + [title]):
        return f"DSH 生态直接参考：{title} — 可借鉴其插件/harness 设计，反哺 dsh 元能力。"
    if any(k in " ".join(topics).lower() for k in ("skill", "skills")):
        return f"Skill 生态参考：{title} — 可借鉴其 skill 组织/发现/评估方式。"
    return f"通用 agent/plugin 参考：{title} — {desc}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--proxy-mode", default="host", choices=["host", "system", "none"])
    parser.add_argument("--category", default="all", choices=list(CATEGORIES))
    parser.add_argument("--limit", type=int, default=6)
    args = parser.parse_args()
    cfg = CATEGORIES[args.category]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    all_items = []
    failures = []
    for q in cfg["queries"]:
        cmd = [sys.executable, str(TOOLS / "info_source_cli.py"), "--proxy-mode", args.proxy_mode]
        if args.offline:
            cmd += ["--offline"]
        cmd += ["github", "--query", q, "--limit", str(args.limit)]
        p = run(cmd)
        if p.returncode != 0:
            failures.append(q + ": " + ((p.stdout or "") + (p.stderr or "")).strip()[:200])
            continue
        all_items.extend(json.loads(p.stdout).get("raw_corpus", []))

    scored = []
    for item in all_items:
        score, hits = score_repo(item, cfg["keywords"])
        scored.append({
            "repo": item["source"]["title"],
            "url": item["source"]["url"],
            "score": score,
            "keywords": hits,
            "suggestion": suggestion(item),
            "topics": (item.get("metadata") or {}).get("topics", []),
            "source_type": item["source"]["type"],
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    dedup = {}
    for s in scored:
        dedup.setdefault(s["repo"], s)
    ideas = list(dedup.values())[:40]

    json_path = OUTPUT / f"{cfg['file']}.json"
    md_path = OUTPUT / f"{cfg['file'].upper()}.md"
    json_path.write_text(json.dumps({"category": args.category, "total_found": len(all_items), "queries": cfg["queries"], "failures": failures, "ideas": ideas}, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# {cfg['title']}", "", f"- category: {args.category}", f"- 查询: {len(cfg['queries'])}", f"- 原始仓库: {len(all_items)}", f"- 候选 ideas: {len(ideas)}", "", "## Top Ideas", ""]
    for i, s in enumerate(ideas[:20], 1):
        lines.append(f"{i}. **{s['repo']}** (score={s['score']})")
        lines.append(f"   - {s['suggestion']}")
        lines.append(f"   - {s['url']}")
        lines.append(f"   - keywords: {', '.join(s['keywords'])}")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"category": args.category, "queries": len(cfg["queries"]), "raw_items": len(all_items), "ideas": len(ideas), "failures": failures}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    main()
