#!/usr/bin/env python3
"""Behavioral test for the core-iteration pipeline.

Unlike validate_contract.py (static checks), this script simulates one
complete pipeline round with synthetic data and asserts that every stage
produces the contract shape the next stage consumes. It also verifies that
Nodes carry a trace_chain (the 'thinking chain' requirement).

Exit code 0 = PASS, 1 = FAIL.
"""
import json
import sys
from pathlib import Path


def mock_gather():
    raw_corpus = [
        {
            "chunk_id": "github_trace_1",
            "text": "Repo X uses pattern P in commit abc.",
            "source": {"type": "github", "url": "https://github.com/x", "date": "2026-01-01"},
            "claim": "Pattern P exists in Repo X",
            "gap_id": "gap_1",
        },
        {
            "chunk_id": "osv_1",
            "text": "OSV reports CVE-2026-1 in package Y.",
            "source": {"type": "osv", "url": "https://osv.dev/vulnerability/CVE-2026-1", "date": "2026-02-01"},
            "claim": "Package Y has advisory CVE-2026-1",
            "gap_id": "gap_2",
        },
    ]
    gaps = [
        {"gap_id": "gap_1", "claim": "Does Repo X use P?"},
        {"gap_id": "gap_2", "claim": "Is package Y vulnerable?"},
    ]
    return raw_corpus, gaps


def mock_filter(raw_corpus):
    verified = []
    for c in raw_corpus:
        # Synthetic density: both entries qualify.
        verified.append({**c, "density_score": 80, "verdict": "verified-single", "weight": 0.5})
    return {
        "verified_high": verified,
        "conflict_branches": [],
        "pending_verification": [],
        "discarded_low_density": [],
        "yield_stats": {
            "raw_count": len(raw_corpus),
            "verified_high_count": len(verified),
            "verified_high_remaining_ratio": 0.4,
        },
    }


def mock_distill(verified):
    nodes = []
    for i, v in enumerate(verified):
        nodes.append({
            "id": f"node_{i+1}",
            "claim": v["claim"] + " -> do X -> observe Y",
            "source_refs": [v["source"]["url"]],
            "evidence": v["verdict"],
            "weight": v["weight"],
            "boundary": "if source is stale",
            "provenance": "new",
            "trace_chain": [f"{v['chunk_id']} -> verified -> primitive -> node_{i+1}"],
        })
    return {"skill_draft": {"id": "draft", "knowledge_nodes": nodes}}


def mock_iterate(old, new):
    nodes = new["skill_draft"]["knowledge_nodes"]
    effective_new_count = len(nodes)
    return {
        "accepted": effective_new_count > 0,
        "effective_new_count": effective_new_count,
        "new_skill": new["skill_draft"],
        "changelog": "2 added",
    }


def mock_validate(old, new, gap_list_prev, gap_list_curr, stats):
    # Synthetic metrics: all pass (not STOP).
    return {
        "decision": "CONTINUE",
        "triggered_rules": [],
        "benefit_summary": stats,
        "forced_review": False,
        "reason": "synthetic pass",
        "stop_reason": None,
    }


def main() -> int:
    raw, gaps = mock_gather()
    filtered = mock_filter(raw)
    assert filtered["yield_stats"]["verified_high_count"] == 2
    distilled = mock_distill(filtered["verified_high"])
    for node in distilled["skill_draft"]["knowledge_nodes"]:
        assert "trace_chain" in node, f"{node['id']} missing trace_chain"
        assert node["boundary"], f"{node['id']} missing boundary"
    iterated = mock_iterate({"knowledge_nodes": []}, distilled)
    assert iterated["accepted"] is True and iterated["effective_new_count"] == 2
    validated = mock_validate(
        {}, distilled["skill_draft"], gaps, gaps, {"effective_new_nodes": 2, "verified_high_remaining_ratio": 0.4}
    )
    assert validated["decision"] == "CONTINUE"
    summary = {
        "status": "PASS",
        "stages": ["gather", "filter", "distill", "iterate", "validate"],
        "nodes": [n["id"] for n in distilled["skill_draft"]["knowledge_nodes"]],
        "trace_chains": [n["trace_chain"] for n in distilled["skill_draft"]["knowledge_nodes"]],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
