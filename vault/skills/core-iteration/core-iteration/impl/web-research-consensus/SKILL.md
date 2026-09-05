---
name: web-research-consensus
description: 网络信息搜集与核验共识——可靠来源判断、精确检索、高效核验与 Agent 引用纪律；用于网络调研、事实核查、开源信息收集、学术检索等任务前。
whenToUse: - 用户要“查资料 / 做调研 / 核实事实 / 比较来源 / 搜代码 / 查论文 / 验证图片或视频”。
---
# 网络信息搜集共识 · 可调用摘要

> 完整版见本目录 `CONSENSUS.md`；来源表见 `SOURCES.md`。
> 本 skill 的目标：让 agent 在需要查外部事实时，先精确定义问题，再精准检索，最后把每条结论回溯到可核验的一手来源；不确定就明说，不硬凑。

## 触发条件

- 用户要“查资料 / 做调研 / 核实事实 / 比较来源 / 搜代码 / 查论文 / 验证图片或视频”。
- agent 需要回答依赖时效性或外部事实的问题，且这个问题不能只靠模型记忆。
- 需要判断某条信息是否可靠、是否被断章取义、是否来自一手证据。
- 需要做系统性的开源信息收集（OSINT 式检索、事实核查、文献检索）。

## 一句话结论

```text
可靠结论 = 一手来源 + 独立交叉验证 + 原始语境 + 明确的确定性标记
```

## 核心动作：四步走

1. **拆问题**：把宽泛主题拆成 1–3 个可检索的子问题，并写下“我要找什么类型的证据”。
2. **精准检索**：关键词 → 同义词/缩写/上位下位词 → 布尔与操作符 → 迭代换词/换库/换引擎。
3. **来源过滤**：用手性原则（SIFT / CRAAP / 横向阅读）判断每个候选，优先一手与原始出处。
4. **核验与交付**：回到原文/原始语境，找 2–3 个独立来源交叉验证，标注事实/推断/未知，给出可回溯引用。

## 输出契约（给下游 benefit-filter / value-meta-scheduler）

本 skill 不只是“给答案”，还必须产出结构化 `raw_corpus` 与 `knowledge_gaps`，才能被收益过滤器接管：

```text
raw_corpus_entry = {
  chunk_id,                 # 稳定唯一 id，如 "<skill>_<kebab-topic>_<n>"
  text,                     # 原文片段，保留可引用上下文
  semantic_vector?,         # 可选，用于去重
  source: { url, title, author, publisher, date, type },
  claim?,                   # 已提取的核心主张
  evidence_class?,          # static/runtime/data/rendering/tooling，供下游验证选用唯一证明
  gap_id?                   # 对应知识缺口
}

knowledge_gap = {
  gap_id,                   # 如 "benefit-filter_scoring_fix"
  claim,                    # “尚待确认/需要证据”的命题
  source_refs: [ ... ],     # 支持/相关来源
  evidence_type: "verified-high" | "verified-single" | "single-doubt" | "unknown",
  uncertainty: "low" | "medium" | "high",
  related_skill: "benefit-filter" | "distillation-consensus" | "value-iterator" | "value-validator" | "value-meta-scheduler"
}

search_meta = {
  queries_run,              # 实际查询数
  sources_checked,          # 打开并核验过的来源数
  exhausted_flags: [ "gap_id" ],
  budget_notes
}
```

- `gap_id` 生成规则：`<目标skill名>_<kebab实体或主题>_<序号>`；同一主张换来源仍用同一 `gap_id`，不因来源数变化而新建。
- 缺 `source_refs` 的条目只能标 `unknown`/`single-doubt`，不得标 verified。

## 扩展信息源：GitHub / 开源库（深度 + 广度）

用于回答“这个库/框架/工具/生态怎么选、怎么用、是否可信”等开放源码信息问题。

### 广度：打开哪些入口

- **仓库搜索**：`github.com/search` / GitHub REST Search API；按 `topic:`、`language:`、`stars:`、`created:`、`in:name/readme` 组合。
- **代码搜索**：code search 找具体 API 用法、实现片段、配置样例；按 `path:`、`repo:`、`language:` 限定。
- **Issue / PR / Release / Changelog**：看已知问题、路线图、迁移与发布说明，比 README 更接近“真实状态”。
- **安全公告**：GitHub Security Advisories、OSV、各生态安全库。
- **包仓库与生态**：npm / PyPI / Maven / crates.io / RubyGems / Go module proxy；看版本、下载量、依赖关系、维护状态。
- **精选列表**：awesome-*、Curated lists、CNCF Landscape、官方 ecosystem directory；作为“地图”，不作为证据。

### 深度：读什么才算“读懂”

- 源码 / commit diff / PR diff / issue 线程本身是**一手**；README 只是“门面”。
- 重要结论至少核对：**仓库 + 最近 release/commit + 实际 API/行为**，必要时跑小样本验证。
- 关注仓库维护状态：最近 commit、issue 响应、release 频率、维护者是否变更。

### 可信度：开源信息不能只看热度

- **stars / forks / README 宣传不是证据**；它们是“流行度信号”。
- **fork、镜像、同作者/同组织仓库不算独立来源**；交叉验证要找不同维护者/不同生态/不同数据库的独立证据。
- 对开源结论，至少一个**一手代码/commit/release** 来源，外加至少一个**独立旁证**（官方包元数据、安全库、下游用户、第三方评测）。
- 只有单个开源仓库支持时，标 `verified-single` 并给出 `repo_url + commit/release/tag`；不能仅写“GitHub 上有人做”。

### 边界

- “awesome list 收了它”不等于“它更可信”；只说明进入某个社区视野。
- 高 star 仓库也可能过时、广告化或存在安全问题；以实际代码与维护状态为准。
- 镜像/转帖需要回溯到上游仓库，避免把搬运者当作者。

## 快速检查表

### A. 来源可靠性

- [ ] 优先一手证据：官方文件、原始数据、论文全文、原始声明；新闻只当线索。
- [ ] 用 SIFT：Stop → Investigate the source → Find better coverage → Trace to original context。
- [ ] 用 CRAAP 过滤：Currency（时间）/ Relevance（相关性）/ Authority（作者与机构资质）/ Accuracy（可查证、有引文）/ Purpose（为何存在）。
- [ ] 横向阅读：不要只读页面自我介绍，新开标签搜“站点名 + 主张”看别人怎么评价它。
- [ ] 至少 2–3 个彼此独立且不是同一通稿/同一数据库转载的来源；检查它们是否都引用同一信源。

### B. 精确检索

- [ ] 先列同义词、近义词、缩写、上位/下位词；学术库查 MeSH / Subject Headings / Thesaurus。
- [ ] 布尔：AND 连接核心概念，OR 汇集同义词，NOT 排除噪音；复杂查询用括号分组。
- [ ] 精确短语加引号；用 `site:` 限定域名、`filetype:` 限定文件类型、`intitle:`/`inurl:` 定位标题或 URL 关键词；用日期范围/`before:`/`after:` 限时效。
- [ ] 迭代：检索 → 读前几页 → 记下有效词 → 拓宽/收窄 → 换数据库、换引擎、换语言 → 重复。
- [ ] 不只看第一页；搜索引擎/引擎的索引与算法有偏差，换一个往往能发现关键材料。

### C. 高效核验

- [ ] 打开原页/原文/原始数据表，不凭搜索摘要或精选摘要下结论。
- [ ] 回溯到原始语境：读完整段落、访谈记录、原始音视频，检查是否断章取义。
- [ ] 交叉核对 2–3 个独立来源，并确认它们不是同源转载。
- [ ] 链接失效时用 Wayback Machine / archive.today 查存档；图片视频做反向搜索、元数据/原发时间/地理定位检查。
- [ ] 给结论标确定性：事实 / 推断 / 未知；无法验证时写“当前公开检索未发现支持证据”。

### D. Agent 引用纪律

- [ ] Search-first：先检索收集证据，再组织答案；不要用“记忆”直接补全外部事实。
- [ ] Grounded citation：每条陈述绑定真实 URL 与可引用原文/片段；URL 必须“存在”且“支持该结论”。
- [ ] 绝不编造论文/网址/引文；生成引用后核验链接可访问、标题真实、内容匹配。
- [ ] 优雅降级：检索失败先换引擎/换词/加 `site:`/查存档；仍无结果就明确说“未发现”，不硬凑。
- [ ] 不过度声称：区分“已证实”“多源支持”“推测”，说明检索范围与限制。
- [ ] 用户说“我感觉不对劲”时，停下来重新核验来源与推理，不硬套模板。

## 搜索预算与停止准则

让调度器能预估轮次成本，避免在收敛后继续空转：

1. 每个子问题先跑 1 轮宽检索 + 1 轮精检索；仍缺关键证据时，最多再扩大 1–2 轮（换词、换库、换语言、查存档）。
2. 连续两轮没有出现新独立来源、也没有新增 `knowledge_gap`，就把该子问题标为 `search_exhausted`，不再硬搜。
3. 未解决的缺口如实进入 `pending_verification`，不为了“看起来完整”而把弱证据标成 verified。
4. 输出 `search_meta`，调度器据此判断“这轮信息搜集是否真的打开了新缺口”。

边界：

- 预算不是硬性禁止继续查，而是默认的优雅降级；用户显式要求深挖时可以放宽并在 `budget_notes` 记录。
- `search_exhausted` 只表示“当前检索范围未发现”，不等于“该缺口不存在”。

## 边界 / 反模式速查

| 情况 | 正确做法 |
|---|---|
| 找到 10 个来源但都是同一篇通稿/同一数据库 | 不算独立交叉验证；继续找真正不同的信源 |
| 官方/机构页面看起来很权威 | 仍可能有公关色彩、过时或选择性表述；需独立证据 |
| 搜索引擎摘要说得很确定 | 摘要可能截断或错误；打开原页核对 |
| 来源已删除 | 用存档查历史，但存档≠事实，仍需其他证据 |
| 反向图搜只有相同图片 | 只能说明“同一张图已收录”，不能证明原创/真假 |
| 公开检索没有结果 | 不等于“这件事不存在”；只能说“当前未发现支持证据” |
| “我记得某篇论文/某个 URL” | 不是引用；必须实际检索并核验存在性与内容匹配 |

## 简单用户话术

> 我给你的是三样东西：方向（先回到一手/原始出处，别被二手转述带偏）、方式（用 SIFT/CRAAP 过滤来源，用布尔和操作符精确检索，用独立交叉验证+存档确认）、边界（什么时候不能下结论：单一来源、同源转载、摘要不可信、检索无果≠不存在）。
>
> 如果哪条和你的直觉冲突，请说“我感觉不对劲”，我会停下来重新核验，而不是硬套模板。

## 干跑验证

- 六阶段完整干跑样例见 `core-iteration/examples/smoke_pipeline.md`（workspace/vault 同步）。
- 使用本 skill 后至少跑 3 个真实查询，确认 `raw_corpus`/`knowledge_gaps` 字段齐全再交给收益过滤器。

## 2026 深度补强（Round 40）

> 补强目标：把“检索可复现、证据分级、源族独立、反证检索、引用四要素”从原则落成可执行检查。以下规则在原有四步走、检查表、搜索预算之上新增，不替代旧规则。

### 1. 先定证据门槛，再分配搜索预算

- 每个子问题开搜前写一句“达标线”：只要概览（overview），还是要 `verified-high`（≥2 独立一手 + 反证检索过），还是只接受“单源待证”？门槛不同，搜索轮数与深度不同。
- 达标线本身决定停止：达到门槛即停，不因“怕漏”继续空转；未到门槛继续，不因“已有结果”提前收工。
- 把门槛写进 `search_meta.budget_notes`，供下游判断“这轮检索是否足以支撑结论”。

反例：用户只要概览，却执行 6 轮深搜；或结论需要 verified-high，却只搜 1 轮就交付。

### 2. 检索日志：每轮 query 留痕，结论才可复现

- 每个关键 claim 至少记：`query 原文 / 引擎或数据库 / 日期 / 过滤条件 / 命中的独立域名 / 决策（采纳、降级、放弃）/ 下一步`。
- 引用时带上“检索日期 + 版本/归档时间”；网页会变、论文会更正、包会发新版，裸 URL 无法证明“我当时看到什么”。
- 失败也要留痕：0 结果、全是广告、只看到 AI 摘要，都写进 `search_meta.failures`；未留痕的“搜不到”不构成排除证据。

反例：交付 3 条引用但不含检索日期与 query；或说“我已经查过没有”却拿不出查询记录。

### 3. 证据定级：先定级，再过五维降级

- 证据阶梯：L0 无来源 → `single-doubt`；L1 单一转载/聚合 → `verified-single`；L2 单一一手/官方文档；L3 ≥2 独立一手且无反证；L4 可复现（命令/数据/原件/重复实验）。
- 升到 L3/L4 前过五问：是否偏倚（利益/公关/自述）？是否不一致（来源间互相矛盾）？是否间接（证据对象≠结论对象）？是否不精确（版本/日期/数字含糊）？是否只看到支持面（发表偏倚）？
- 任一回答“是/无法判断”即降一级，并写进 `uncertainty`；不能靠“来源数量多”绕过降级。

反例：10 篇转载同一公关稿 → 仍是 L1；只有官方白皮书无第三方 → 最多 L2/`verified-single`；只搜到支持证据就标 `verified-high`。

### 4. 源族计数：数“独立来源族”，不数网页数

- 用 `family_id` 归一：同 DOI/同 URL/同 canonical title/同 commit/同版本 = 同一族；同作者/同机构/同通讯社/同母库/同一原始数据集 = 同一族。
- 一族的多个网页只计 1 个来源；跨族才可能算“多源支持”。若两个族最终都引用同一上游原始报告，标记 `same_upstream` 并降权。
- 交付时给出“族计数”而非“链接计数”：例如 `families=2, links=11，其中 9 条同源转载`。

反例：同一新闻 10 个站点转贴 → 1 族；同一作者博客+采访稿+机构页 → 1 族；两个独立机构引用同一数据集只能证明“都读了同一数据”，不能证明数据本身被独立验证。

### 5. 反证检索：正面证据之外，必须定向找一次反面

- 关键 claim 的支持证据齐了后，补 1 轮反证检索（`limitations` / `criticism` / `counterexample` / `does not` / `risk` / `争议` / `更正` / `retraction`）。
- 没找到反证 ≠ 反证不存在；但定向找过并记录，才能把 `verified-high` 从“单边支持”升级为“抗反驳支持”。
- 找到反证时不要合并：保留冲突分支，注明“支持面与反证并存”，`uncertainty` 升高，不得把反证删成“噪音”。

反例：只搜“X 有效”，从不搜“X 副作用/争议”；把反对意见当水军删除；用“有 3 篇支持”掩盖“另有 2 篇不支持”。

### 6. 引用四要素：作者/时间/可核验标识/检索时间，缺一不可

- 每条引用至少四要素：谁说的（作者/机构）、何时发布/版本、哪里能核对（DOI/PMID/arXiv/commit/version/具体页+段落）、我何时检索到（retrieved date）。
- 优先稳定标识与原始出处：DOI/版本号/commit/tag 优于会失效的搜索 URL；原件优于聚合页/镜像/转帖。
- 引用有更正/撤回历史的来源时，必须附带“是否有更正/撤回”状态；引用存档须同时给原始 URL 与存档 URL。

反例：只给 home page；引用 PDF 不给版本/日期；引用论文不带 DOI 且未查是否被撤回；把 AI 生成的“看起来像引文”的字符串当来源。

### 本轮来源（详细表见 SOURCES.md）

- [Cochrane Handbook Chapter 4: Searching for and selecting studies](https://training.cochrane.org/handbook/current/chapter-04)
- [Cochrane: GRADE approach](https://www.cochrane.org/learn/courses-and-resources/cochrane-methodology/grade)
- [PRISMA-S](https://doi.org/10.1186/s13643-020-01542-z)
- [PRESS 2015](https://doi.org/10.1016/j.jclinepi.2016.01.021)
- [NIST TREC Overview](https://trec.nist.gov/overview.html)
- [OpenAlex: Searching](https://developers.openalex.org/guides/searching)
- [Lateral reading: College students learn to critically evaluate internet sources in an online course](https://doi.org/10.37016/mr-2020-56)
- [How Unique Are Hallucinated Citations Offered by Generative Artificial Intelligence Models?](https://doi.org/10.3390/publications14030038)

## 主要来源

- [Google Search Help: Refine web searches](https://support.google.com/websearch/answer/2466433?hl=en)
- [Bing: Advanced search options](https://support.microsoft.com/en-us/bing/advanced-search-options)
- [UNCC: SIFT](https://guides.library.charlotte.edu/c.php?g=1499262&p=11347573)
- [CSU Chico: CRAAP Test](https://libguides.csuchico.edu/c.php?g=414299&p=2822727)
- [Stanford Civic Online Reasoning](https://cor.inquirygroup.org/blog/module-for-high-school/)
- [Drexel: Database Searching](https://libguides.library.drexel.edu/c.php?g=1484012&p=11065571)
- [Poynter: How to uncover out-of-context quotes](https://www.poynter.org/fact-checking/2023/how-to-uncover-out-of-context-quotes/)
- [Hermes Agent: Grounded Citations](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-grounded-citations)
- （完整来源表见 `SOURCES.md`）
