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

## 2026 深度补强（Round 37）

> 补强目标：把“检索式构造、跨库适配、来源可信度、证据分级、搜索质量评估”落成可直接执行的清单。以下规则在原有“独立来源 / 台账 / 搜索预算”之上新增，不替代旧规则。

### 1. 检索式：先写“概念×关键词”矩阵，再组装布尔式

- 每个子问题先拆 2–5 个概念；每个概念写同义词、缩写、大小写、中英文变体（例：“包管理” = npm / PyPI / cargo / registry / 依赖版本、依赖锁定）。
- 组装顺序：概念间用 `AND`/空格，概念内用 `OR` 或括号；精确短语加引号；收紧结果用 `site:`、`filetype:`、`inurl:`、`repo:`、`path:`、`language:`。
- 每个 query 都要版本化记录；先窄后宽反向验证：窄式无结果时先换同义词，再删限定词，不要直接放弃。
- 反例：把整段自然语言粘进搜索框；只用一个关键词；把同义词用 `AND` 连起来反而得到 0 结果。

### 2. 跨库适配：每个入口用各自的语法，不做“一处搜索走天下”

- 网页用 `site:`；GitHub 用 `repo:`/`path:`/`language:`；Crossref 用 `query.bibliographic`/`filter`；OpenAlex 用 `search`/`filter`/`concepts`；学术库用 MeSH/主题词；包生态用精确名称 + 版本/OSV ID。
- 换库前先读该入口的查询文档；不要把网页站点语法硬套到学术/代码 API。
- 同一子问题至少在“网页 / 学术 / 代码 / 包生态”中选两类不同生态，并各自记录 query 原文。
- 反例：在 Crossref 用 `site:`；只在 Google 第一页找学术证据；把数据库 0 结果直接写成“不存在”。

### 3. 来源可信度：五维快检 + 横向阅读

- 对每个候选源用 5 个问题快检：作者/机构可识别？渠道/载体正规？日期/版本明确？目的是告知还是说服？是否引用一手或可复现材料？
- 任一维度完全未知 → 该来源降为“线索”，不能作为独立证据。
- 不要相信页面自述；横向阅读：另开标签查作者、机构、原始出处，而不是用域名或粉丝量代替可信度。
- 反例：看到 `.edu`/`.gov`/大媒体即默认可信；拿第一条结果当定论；把二手摘要当原文。

### 4. 证据强度五级 + 降级项

- L0 无来源/纯线索 → `single-doubt`；L1 单一转载/聚合 → `verified-single`；L2 单一一手或官方文档；L3 两个以上独立一手/授权一致；L4 可复现（命令、代码、数据、原件可验证）。
- 降级检查（GRADE 式）：风险偏倚（自述/软文）、不一致（自相矛盾）、间接性（结论 ≠ 证据对象）、不精确（版本/数字含糊）、发表偏倚（只报支持面）。
- 出现任一降级项不得升到 L3；冲突证据保留“冲突分支”，不自动合并为“多源一致”。

### 5. 搜索质量验收：覆盖检查 + 反证检索

- 每个关键 claim 至少要有三类证据：一手证据、独立旁证、反例/限制。缺哪类，就补一次定向检索（`limitations`、`criticism`、`counterexample`、`does not`、`风险/争议`）。
- 自评精度/召回：结果若全来自同一域名或同一通稿，只算 1 个“来源族”；连续两轮无新独立来源 → `search_exhausted`；只得到支持面 → 标 `coverage_bias`。
- 用 IR 评估视角自查：不是看排名，而是看是否覆盖相关结果集；明确记录命中与漏检，不把“搜到”当“结论成立”。

### 6. 反例清单（必须主动避开）

- 把聚合页、榜单、star 数、被引数当证据。
- 只记录支持证据，删掉反对/限制证据。
- 把 AI 生成的引用当来源——必须回链到可核验 URL，并确认内容确实支持主张。
- 用“没有搜到”写“不存在”。
- 不记录 query/入口/日期，导致结果不可复现。
- 同一新闻多站转载当“多个独立来源”。
- 用旧版本结论回答当前事实，却不核对时效。

### 7. 源族归一化：检测“伪独立”

- 跨库去重按 `DOI / URL / canonical title / repo commit / version` 判定身份，不按“文字相似”判定同一。
- 两个 URL 若同通稿、同数据源、同一母库派生、同作者/机构 → 归为同一“源族”。
- 源族内只计 1 个来源；要升到 L3，必须再找一个真正独立、且不共享该源族的来源。
- 反例：把同一新闻的 10 个转载链接列成 10 条证据。

### 本轮来源

- [PRISMA-S: 系统综述检索报告扩展](https://doi.org/10.1186/s13643-020-01542-z)
- [Cochrane Handbook Chapter 4: Searching for and selecting studies](https://training.cochrane.org/handbook/current/chapter-04)
- [PRESS 2015 电子检索策略同行评审指南](https://www.cda-amc.ca/press-peer-review-electronic-search-strategies-2015-guideline-explanation-and-elaboration)
- [TREC Overview（NIST）](https://trec.nist.gov/overview.html)
- [NIST Special Publication 500-249（检索运行评估）](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-249.pdf)
- [Google 搜索质量评估者指南（E-E-A-T）](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t)
- [Google 搜索运算符文档](https://developers.google.com/search/docs/monitor-debug/search-operators)
- [Georgetown: Evaluating Web Sources with SIFT](https://guides.library.georgetown.edu/c.php?g=1497500&p=11189585)
- [Queen's University: Evaluating Sources](https://guides.library.queensu.ca/politicalstudies/112/evaluation)
- [Cochrane: GRADE 证据分级方法](https://www.cochrane.org/learn/courses-and-resources/cochrane-methodology/grade)
- [OpenAlex: Searching（查询构造）](https://developers.openalex.org/guides/searching)
- [GitHub: 代码搜索语法](https://docs.github.com/zh/search-github/github-code-search/understanding-github-code-search-syntax)
