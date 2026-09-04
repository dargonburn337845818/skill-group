# 六阶段产物样例（Artifact Examples）

> 供六个 skill 干跑时对照。每个样例只演示“字段与结构”，数值为示意。

## 1. web-research-consensus 输出

```text
raw_corpus = [{
  chunk_id: "web-research-consensus_scoring_1",
  text: "Density score should use 0-100 raw dimensions ...",
  source: { url: "https://...", title: "...", author: "...", date: "2026-09-04", type: "internal-spec" },
  claim: "密度评分必须使用 0-100 原始分再加权",
  gap_id: "benefit-filter_scoring_fix"
}]
knowledge_gap = {
  gap_id: "benefit-filter_scoring_fix",
  claim: "密度评分公式可能导致阈值 60 永远不可达",
  source_refs: ["internal consistency analysis"],
  evidence_type: "verified-single",
  uncertainty: "low",
  related_skill: "benefit-filter"
}
search_meta = { queries_run: 2, sources_checked: 6, exhausted_flags: [], budget_notes: "ok" }
```

## 2. benefit-filter 输出

```text
verified_high = [{
  chunk_id: "web-research-consensus_scoring_1",
  claim: "密度评分必须使用 0-100 原始分再加权",
  density_score: 86,
  verdict: "verified-single",
  independent_sources: ["internal consistency analysis"],
  source_count: 1,
  weight: 0.5,
  gap_id: "benefit-filter_scoring_fix"
}]
yield_stats = {
  raw_count: 25, density_pass: 23, verified_high_count: 9,
  verified_single_count: 14, pending_count: 0, discarded_count: 2,
  avg_density_score: 77, remaining_verified_high: 6,
  remaining_gap_count: 17, verified_high_remaining_ratio: 0.35
}
```

## 3. distillation-consensus 输出（Node）

```text
Node = {
  id: "distillation_density_scoring_fix",
  claim: "给语料打密度分时，先打 0-100 原始分，再 0.4/0.3/0.3 加权；不要把锚点当满分",
  source_refs: ["benefit-filter SKILL.md"],
  evidence: "verified-single",
  weight: 0.5,
  boundary: "若环境已使用显式 0-100 计分且阈值可达，则本条为冗余",
  provenance: "new"
}
```

## 4. value-iterator 变更日志

```text
## 变更日志 v0.0.1 → v0.1.0
### Added (有效新增)
| node_id | claim 摘要 | 证据 | 来源 | 权重 | 对应缺口 |
|---|---|---|---|---|---|
| distillation_density_scoring_fix | 密度分 0-100 再加权 | verified-single | benefit-filter | 0.5 | benefit-filter_scoring_fix |
### Footnotes (待定注脚)
| node_id | 内容 | 来源 | 为何不升级为核心 |
|---|---|---|---|
| none | - | - | - |
```

## 5. value-validator 输出

```text
{
  "decision": "CONTINUE",
  "triggered_rules": [],
  "benefit_summary": {
    "hit_high_quality_count": 23,
    "discarded_low_quality_count": 2,
    "effective_new_nodes": 23,
    "new_nodes_from_doubt": 0,
    "verified_high_remaining_ratio": 0.35,
    "cumulative_nodes": 23
  },
  "forced_review": false,
  "reason": "文本变化、语义位移、缺口更新和边际收益全部通过",
  "suggested_next_action": "继续下一轮"
}
```
