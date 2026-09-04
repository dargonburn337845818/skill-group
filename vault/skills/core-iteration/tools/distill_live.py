#!/usr/bin/env python3
"""Executable distillation stage: turn verified raw_corpus into Nodes.

This is the executable counterpart of `distillation-consensus`. It reads the
live/offline `info_dump.json`, converts each verified item into a machine-readable
Node (claim/trigger/action/boundary/source/trace_chain), and reports a
distillation_stats summary. It intentionally does not invent expert quotes; it
marks everything as verified-single until independent sources confirm them.

Usage:
  python3 tools/distill_live.py [--input tools/output/info_dump.json]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "tools" / "output" / "info_dump.json"

PROFILES = {
    "github": {
        "trigger": "当需要评估/选择开源仓库时",
        "action": "检查 license、recent push、语言、topics、是否 archived，把 stars/forks 当流行度信号而非证据",
        "boundary": "单仓库单源信息；README 可能过时；需要独立旁证才能升级 verified-high",
    },
    "github_issue": {
        "trigger": "当需要理解已知问题/讨论/决策时",
        "action": "读 issue 正文、labels、评论数与关联 PR，避免只看标题",
        "boundary": "issue 可能已过期、观点化或未被合并；单源需要交叉验证",
    },
    "github_release": {
        "trigger": "当需要确认版本、变更、迁移或安全修复时",
        "action": "读 release body、tag、publish date 与 assets，对照 CHANGELOG",
        "boundary": "release notes 可能省略破坏性变更；以实际代码/commit 为准",
    },
    "github_commit": {
        "trigger": "当需要定位具体代码改动时",
        "action": "读 commit message，回到 diff/sha 验证；commit 是最接近一手代码的证据",
        "boundary": "commit message 可能简洁或误导；单个 commit 不代表完整上下文",
    },
    "github_pr": {
        "trigger": "当需要评估一个提议中的改动时",
        "action": "读 PR 标题/正文/diff/评论与 merged 状态",
        "boundary": "PR 可能未合并或后来被否决；不能当作已落地事实",
    },
}


def make_node(item: dict, idx: int) -> dict:
    src = item.get("source", {})
    stype = src.get("type", "unknown")
    profile = PROFILES.get(stype, {
        "trigger": "当发现相关外部信息时",
        "action": "回到原始来源阅读完整上下文",
        "boundary": "单源信息；需独立验证",
    })
    title = src.get("title") or item.get("chunk_id", "")
    text = item.get("text") or item.get("claim") or title
    node_id = f"live_{stype}_{idx+1}"
    meta = item.get("metadata") or {}
    quality = item.get("quality_score")
    if quality is None:
        # simple fallback
        quality = 70 if stype != "unknown" else 50
    return {
        "id": node_id,
        "claim": f"{title}: {text[:180]}",
        "trigger": profile["trigger"],
        "action": profile["action"],
        "boundary": profile["boundary"],
        "source_refs": [src.get("url")],
        "evidence": "verified-single",
        "weight": 0.5,
        "provenance": "new",
        "quality_score": quality,
        "trace_chain": [f"{item.get('chunk_id')} -> verified-single -> {node_id}"],
        "metadata": meta,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    items = data.get("raw_corpus", data if isinstance(data, list) else [])
    nodes = [make_node(item, i) for i, item in enumerate(items)]

    # Pull verified-high aggregates from the real benefit-filter output.
    bf = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "benefit_filter_live.py"), "--input", args.input],
        capture_output=True, text=True,
    )
    try:
        bfdata = json.loads(bf.stdout)
        for entry in bfdata.get("verified_high", []):
            if entry.get("verdict") == "verified-high" and entry.get("chunk_id", "").startswith("cross_"):
                node_id = "cross_" + entry["chunk_id"].replace("cross_", "")
                nodes.append({
                    "id": node_id,
                    "claim": entry["claim"],
                    "trigger": "当需要判断某个开源生态/主题是否存在多个独立活跃项目时",
                    "action": "检查多个独立仓库的 license、活跃度、topics；把聚合主题作为 verified-high 知识节点",
                    "boundary": "共享 topic 只是聚合信号，不代表这些项目在具体技术上达成一致",
                    "source_refs": entry.get("independent_sources", []),
                    "evidence": "verified-high",
                    "weight": 1.0,
                    "provenance": "new",
                    "quality_score": entry.get("density_score", 90),
                    "trace_chain": [f"{', '.join(entry.get('independent_sources', []))} -> cross-verify -> {node_id}"],
                    "metadata": {"cross_verified": True, "source_count": entry.get("source_count", 0)},
                })
    except Exception:
        pass

    stats = {
        "total_nodes": len(nodes),
        "verified_single": sum(1 for n in nodes if n["evidence"] == "verified-single"),
        "verified_high": sum(1 for n in nodes if n["evidence"] == "verified-high"),
        "with_trigger": sum(1 for n in nodes if n["trigger"]),
        "with_action": sum(1 for n in nodes if n["action"]),
        "with_boundary": sum(1 for n in nodes if n["boundary"]),
        "avg_quality": round(sum(n["quality_score"] for n in nodes) / max(1, len(nodes)), 1),
    }
    result = {
        "skill_draft": {"id": "live-github-intel-draft", "version": "0.1.0", "knowledge_nodes": nodes},
        "nodes": nodes,
        "trace_chains": [n["trace_chain"] for n in nodes],
        "distillation_stats": stats,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
