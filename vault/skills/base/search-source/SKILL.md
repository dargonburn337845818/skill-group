---
name: search-source
description: 搜索与来源深模块——把网络/GitHub/包生态/学术等多源检索、归一化与来源可信度判断合成一个常驻底座，供任何工作流先检索、留来源、再进入蒸馏或开发。
whenToUse: 任何需要查资料、搜 GitHub、看源码/commit/release、查论文/包生态、核验信息来源、生成 raw_corpus 的任务；作为所有工作的第一步。
---

# 搜索与来源（Search & Source）

> 定位：这是技能库的常驻底座。它不替代具体领域知识，而是保证“信息从哪来、凭什么可信、怎么交给下游”。

## 触发条件

- 用户要求“查资料 / 搜 GitHub / 看源码 / 查论文 / 查包 / 核验来源”。
- 蒸馏、开发、验证类任务开始前需要先建立原始语料与来源清单。
- 上游需要 `raw_corpus` / `source_scope_report` 时。

## 动作（最小可执行链）

1. **拆问题**：把问题切成可检索的子问题，明确要的是“事实、机制、最佳实践、还是生态地图”。
2. **选独立入口**：优先上游一手（源码/commit/release/安全公告/论文原文），再用不同生态/不同维护者做旁证。
3. **归一化**：每个结果输出 `raw_corpus_entry`（chunk_id/text/source/claim?/gap_id?）。
4. **报告范围**：输出 `source_scope_report`（查了哪些源、用了哪些 query、失败与降级、覆盖限制）。
5. **底线下判断**：stars/forks/awesome 收录只当线索，不是证据；单源结论必须挂“单源待证”。
6. **证据归类**：给每条 raw_corpus 标 `evidence_class`（static/runtime/data/rendering/tooling），后续验证才知道“唯一可接受证明”是什么。

## 来源台账与独立判定

- **台账字段**：每条结果至少带 `url + title + publisher + date + evidence_rank + claim?`；重要结论再补 `repo/package version、commit/tag、查询命令`。
- **独立来源**：两个来源必须不是同作者/同机构/同一通稿转载/同一母库派生；至少一个能回溯到一手证据。
- **降级规则**：单源 → `verified-single` 并降权；无来源 → `single-doubt`；同源转载 → 不算独立。
- **引用纪律**：生成引用后核验“链接存在 + 内容支持主张”；检索无果写“当前公开检索未发现”，不写“不存在”。

## 搜索预算

- 每个子问题先 1 轮宽搜 + 1 轮精搜；仍缺关键证据最多再扩 1–2 轮（换词/换库/换语言/查存档）。
- 连续两轮无新独立来源、无新 `knowledge_gap` → 标该子问题 `search_exhausted`。
- `search_exhausted` 只表示当前范围未发现，不等于缺口不存在。

## 输出契约（对接 core-iteration）

```text
raw_corpus_entry = {
  chunk_id, text,
  source: { type, url, title, author, publisher, date, evidence_rank },
  claim?, evidence_class?, gap_id?
}

source_scope_report = {
  sources_queried, total_candidates, failures, degradation, coverage_notes
}
```

- `evidence_class`：static/runtime/data/rendering/tooling，交给 `skill-verification-consensus` 选择唯一证明。
- 本底座只产出语料与范围报告，不替代 `benefit-filter` 的收益判断。

## 干跑验证

- 使用前至少跑 3 个真实查询：确认每条结果有 URL、有 claim、有 evidence_class。
- 例行验证命令：`python3 tools/info_source_cli.py --proxy-mode host github-file --repo <repo> --path <path>`（真实文档拉取）。
- 干跑样例见 `examples/dry_run.md`。

## 边界

## 内部实现

- 详细检索策略见同库 `distillation-consensus/impl` 与 `web-research-consensus` 内部文档。
- 真实抓取入口：`info-source-adapter`（GitHub/OSV/npm/PyPI/crates/学术等适配器）。
