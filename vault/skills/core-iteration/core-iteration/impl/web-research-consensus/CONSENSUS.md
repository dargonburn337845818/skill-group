# 网络信息搜集与核验共识（完整版）

> 适用对象：需要在网络/数据库/开源情报中查找、判断、核验信息的 agent 与用户。
> 产出物：一套可执行的信息搜集纪律——不是“多用搜索”的口号，而是“先定问题、再精准检索、再独立核验、最后诚实标注”的流程。
> 本文遵守 `distillation-consensus`：每条规则都有触发、动作、边界与来源；没有来源的只作 `common-lore` 并降权。

## 0. 一句话共识

```text
可靠信息 = 一手来源 + 独立交叉验证 + 原始语境 + 明确的确定性标记
```

## 1. 定目标：先知道自己在找什么

触发：任何网络调研/事实核查/代码与文档检索/学术检索之前。

动作：

1. 把宽泛主题转成 1–3 个具体子问题。例：“XX 是否安全？” → “官方对 XX 的标准是什么？” “最近一次事故报告说了什么？” “第三方评估有哪些？”
2. 写清证据类型：要一手政策文件？同行评审论文？原始数据？目击者/图片？还是只需要一个入门概览？
3. 决定检索范围：语言、时间窗、地域、数据库、是否接受二手转述。

边界：

- 子问题太窄会漏掉关键材料，太宽会被噪音淹没。
- “入门概览”和“可引用的可靠结论”是不同的检索任务；不要混用一种深度。

来源：[Wake Forest: Systematic Reviews Step 3](https://guides.zsr.wfu.edu/c.php?g=1470676&p=10952495)

## 2. 可靠来源判断

### 2.1 来源层级

动作：

- 优先一手证据：官方文件、原始数据、论文全文、原始声明、原始音视频。
- 新闻、博客、百科只有“线索价值”；引用时回溯到它们引用的原始出处。
- 二手转述若无法回溯，必须明确标注“二手转述”，不能当作原始证据。

边界：

- 官方材料也可能有公关、营销或选择性表述；不能只因为它“官方”就免核验。
- 一手也不等于绝对正确；仍需要独立来源/方法论确认。

来源：[Wesleyan College: Types of Sources](https://wesleyancollege.libguides.com/c.php?g=1525965&p=11431022)

### 2.2 横向阅读（Lateral Reading）

动作：

- 不要只停在当前页面的自我介绍、关于页、宣传语。
- 新开标签页搜索“站点名 + 主题/主张”，看其他独立权威来源如何评价它。
- 关注作者/机构是否真实存在、是否被主流机构引用、是否有利益冲突。

边界：

- 横向阅读本身依赖搜索质量，可能被 SEO 与算法带偏。
- 它常与 SIFT/CRAAP 配合使用，不能替代后续内容核验。

来源：[UNCC: SIFT](https://guides.library.charlotte.edu/c.php?g=1499262&p=11347573)、[Stanford Civic Online Reasoning](https://cor.inquirygroup.org/blog/module-for-high-school/)

### 2.3 SIFT 四步

动作：

1. **Stop**：先停一下，不急于转发/采信。
2. **Investigate the source**：查这个站点/作者/机构的背景。
3. **Find better coverage**：找更权威的媒体、机构、论文或官方页面覆盖同一事实。
4. **Trace to original context**：回到原始声明/原始报道/原始数据，而不是只看转述。

边界：

- SIFT 是降低风险的方法，不是“完全可信”认证。
- 对精心制作的深度伪造或高度仿冒站点，仍会失效。

来源：[UNCC: SIFT](https://guides.library.charlotte.edu/c.php?g=1499262&p=11347573)

### 2.4 CRAAP 五问

动作：

1. **Currency**：信息多久了？是否需时效更新？
2. **Relevance**：与当前问题相关吗？受众/深度匹配吗？
3. **Authority**：作者、机构、资质是什么？
4. **Accuracy**：是否有参考文献、数据、可查证性？语言是否客观？
5. **Purpose**：页面为什么存在？传播知识、卖货、还是观点宣传？

边界：

- CRAAP 是启发式过滤，不能识别所有伪造/操纵。
- 不要只看“域名以 .edu/.gov 结尾”就认定可靠；域名只是线索之一。

来源：[CSU Chico: CRAAP Test](https://libguides.csuchico.edu/c.php?g=414299&p=2822727)

### 2.5 独立交叉验证

动作：

- 至少找 2–3 个彼此独立、不是同一稿源/同一数据库的来源。
- 检查它们是否引用同一个原始信源；若所有来源都引用同一源头，那只是“一篇被转载 N 次”。
- 优选不同媒体/机构/数据库、不同立场、不同方法论。

边界：

- 多个独立来源也可能共享同一错误原始数据；
- 交叉验证降低风险，但不构成数学证明。

来源：[Stanford Civic Online Reasoning](https://cor.inquirygroup.org/blog/module-for-high-school/)

### 2.6 开源代码库与 GitHub 信息源

触发：需要调研开源项目、库/框架选型、代码实现、生态现状、或“GitHub 上有没有现成方案”时。

动作：

1. 先按“广度”铺开：仓库搜索（topic/language/stars/created）、代码搜索、Issues/PRs、Releases、Security Advisories、包生态（npm/PyPI/Maven/crates/Go proxy）、awesome/Curated lists、Landscape。
2. 再按“深度”收敛：读源码/commit diff/PR 线程/issue 线程/CHANGELOG/release notes；不把 README 或 star 数当成结论。
3. 最后按“可信度”定性：区分“上游一手”与“转述/镜像”；区分“独立维护者”与“fork/同组织”；给结论标注 repo URL + commit/tag/release 或 package version。

可信度规则：

- GitHub stars、forks、README 宣传、awesome 收录都是**流行度信号**，不是事实证据。
- 同一作者/组织、fork、镜像、同一仓库多次转帖，不算独立来源。
- 对一个开源结论，至少一个一手代码/commit/release，外加至少一个独立旁证（官方包元数据、安全库、不同生态下游、第三方评测）。
- 若只有单个开源仓库支持，标 `verified-single`，给出可回溯的 `repo_url + commit/tag`，并提示“单源待证”。

边界：

- 高 star ≠ 正确/安全/维护活跃；需要看最近 commit、issue 响应、release 频率、维护者变更。
- 搜索结果可能包含被污染/伪造的仓库、刷 star、恶意依赖；要检查仓库来源、作者身份、依赖来源。
- GitHub 官方索引与搜索引擎索引不同步时，以仓库当前状态 + release/commit 为准。

来源：[GitHub Docs: Searching code](https://docs.github.com/en/search-github/github-code-search/using-github-code-search)、[GitHub REST Search API](https://docs.github.com/en/rest/search/search)、[GitHub Docs: About searching on GitHub](https://docs.github.com/en/search-github/getting-started-with-searching-on-github/about-searching-on-github)、[GitHub Security Advisories](https://github.com/advisories)、[OSV](https://osv.dev/)、本地 `github-repo-consensus`。

## 3. 精确检索

### 3.1 关键词与概念扩展

动作：

1. 把问题拆成核心概念，每个概念列同义词、近义词、缩写、旧称、上位/下位词。
2. 学术检索查受控词表：PubMed MeSH、数据库 Subject Headings / Thesaurus；不要只靠自由词。
3. 先用日常词“探路”，再切换到领域术语；反之亦然。

边界：

- 普通关键词与数据库主题词表不完全对等；不同库词表不同。
- 同一个词在不同语言/地区可能有不同含义。

来源：[PubMed Help](https://pubmed.ncbi.nlm.nih.gov/help/)、[Drexel: Database Searching](https://libguides.library.drexel.edu/c.php?g=1484012&p=11065571)

### 3.2 布尔与操作符

动作：

- `AND` 连接核心概念，要求同时出现。
- `OR` 汇集同义词/变体，扩大召回。
- `NOT` 排除已知噪音。
- 复杂表达式用括号分组，如 `(A OR B) AND C`。
- 固定短语加引号，如 `"exact phrase"`。
- 常用引擎操作符：
  - `site:example.com` 限定站点/域名
  - `filetype:pdf` 限定文件类型
  - `intitle:` / `inurl:` 限定标题或 URL
  - `before:` / `after:` 或引擎自带时间过滤限定日期
  - `-keyword` 排除词（部分引擎）
- 不同引擎支持不完全一致；不要只依赖单引擎单操作符。

边界：

- `AND` 太多可能 0 结果；`NOT` 可能误删相关信息。
- 操作符可能被搜索引擎悄悄废弃或改变语义；查官方帮助页确认。

来源：[Google Search Help: Refine web searches](https://support.google.com/websearch/answer/2466433?hl=en)、[Bing: Advanced search options](https://support.microsoft.com/en-us/bing/advanced-search-options)、[Drexel: Database Searching](https://libguides.library.drexel.edu/c.php?g=1484012&p=11065571)

### 3.3 迭代式检索

动作：

1. 第一轮：宽泛词 + 少量操作符，读前 5–10 个结果。
2. 记录有效关键词、同义词、作者/机构名、术语。
3. 第二轮：用有效词收紧/放宽，加 `site:`/引号/日期/文件类型。
4. 换数据库、换引擎、换语言；再重复直到覆盖面足够。
5. 对重要结论，至少要看到“从不同入口都能到达”的印证。

边界：

- 只看第一页会被 SEO、算法排名、地域偏见影响。
- 检索是迭代过程，不要期望第一个查询就完成一切。

来源：[Drexel: Database Searching](https://libguides.library.drexel.edu/c.php?g=1484012&p=11065571)、[Wake Forest: Systematic Reviews Step 3](https://guides.zsr.wfu.edu/c.php?g=1470676&p=10952495)

## 4. 高效核验

### 4.1 回到原始出处

动作：

- 打开完整正文/原始数据表/原始声明；不要凭搜索摘要、精选摘要、二级标题下结论。
- 链接失效/被删时用 Wayback Machine、archive.today 查存档。
- 引用时给出能看到原文的具体 URL；无法访问时说明“存档可见”。

边界：

- 存档可能缺失或被人为提交，存档页不等于“原始事实一定如此”。
- 摘要/精选摘要可能过时、截断甚至错误。

来源：[UNCC: SIFT](https://guides.library.charlotte.edu/c.php?g=1499262&p=11347573)、[Full Fact: Google snippet eating glass](https://fullfact.org/health/google-snippet-eating-glass/)、[Wayback Machine](https://web.archive.org/)

### 4.2 核查引用语境

动作：

- 读完整段落、访谈记录、原始音视频，检查是否断章取义。
- 检查被引用的句子是否被删去前提、转折、后续修正。
- 有录音/录像/原始全文时，优先于文字转述。

边界：

- “保留完整句子”仍可能截掉时间线或关键让步，依然会歪曲原意。
- 转述永远可能有损耗；下结论前尽可能找回一手表述。

来源：[Poynter: How to uncover out-of-context quotes](https://www.poynter.org/fact-checking/2023/how-to-uncover-out-of-context-quotes/)

### 4.3 图片/视频/地理核验

动作：

- 图片：反向图片搜索，查原发时间、出处、是否被裁剪/重拍。
- 视频：检查元数据、帧、原发时间；用 InVID 等工具拆帧/比对。
- 地理定位：地图、街景、道路/光线/阴影/地标交叉比对。
- 账号/人物：搜用户名、邮箱、同名，看是否能形成一致身份链。

边界：

- 反向图搜只能找到“已收录的同图”，不能证明原创或真实。
- 生成式图片、重拍、裁剪都可能误导；需要更多上下文与原始出处。

来源：[Bellingcat Toolkit: InVID](https://bellingcat.gitbook.io/toolkit/more/all-tools/invid)

### 4.4 标注不确定性

动作：

- 明确区分：事实（有原始证据）、推断（从证据推出）、未知（未找到证据）。
- 给每个关键结论标置信度/支持程度：已证实 / 多源支持 / 单一来源 / 推测。
- 无法验证时写“当前公开检索未发现支持证据”，不要写“这是假的/不存在”。

边界：

- 检索无结果 ≠ 证据不存在，只说明当前可访问范围内未发现。
- “不确定”是弱证据，不应当成“否”。

来源：[Hermes Agent: Grounded Citations](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-grounded-citations)

## 5. Agent 使用纪律

1. **Search-first**：回答外部事实前先搜索；检索是证据收集，不是用记忆补全。
2. **Grounded citations**：每条陈述绑定真实 URL 和可引用片段；引用必须同时满足“链接存在”和“内容支持结论”。
3. **防幻觉来源**：不编造论文、网址、引文；生成引用后核验链接可访问、标题真实、内容匹配。
4. **优雅降级**：检索失败先换引擎/换词/加 `site:`/查存档；仍无结果就明确说“当前公开检索未发现”。
5. **不过度声称**：区分“已证实”“多源支持”“推测”，并说明检索范围与限制。
6. **人类接管**：用户说“我感觉不对劲”时，停下来重新核验来源与推理，不硬套模板。

边界：

- 搜索结果本身可能被 SEO、推荐算法或 prompt injection 污染；仍要做来源筛选。
- 有 URL 不等于有支持；模型可能把相关文章错误引成“证明”。

来源：[Firecrawl Research Engine](https://github.com/hecailiaoPFS/firecrawl-research-engine)、[Hermes Agent: Grounded Citations](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-grounded-citations)、[Poynter](https://www.poynter.org/fact-checking/2023/how-to-uncover-out-of-context-quotes/)

## 6. 反模式速查

| 反模式 | 处理 |
|---|---|
| 把“来源多”当“独立” | 检查是否同一通稿/同一数据库/同一信源；去重后才是独立 |
| 只引用搜索引擎摘要 | 打开原页核对；摘要可能截断或错误 |
| 把官方页面当免检 | 官方也可能公关/过时；找独立证据与原始数据 |
| 引用“我记得的论文” | 不算引用；必须实际检索并确认存在 + 内容匹配 |
| 检索无果就说“不存在” | 改为“当前公开检索未发现支持证据” |
| 单来源下强结论 | 至少 2–3 个独立来源；争议话题更保守 |
| 只看第一页 | 换库/换引擎/换语言/换时间窗；迭代检索 |
| 不标注事实/推断/未知 | 每个关键结论都标确定性层级 |
| 用户说“不对劲”仍硬套 | 停下，重新核验；不把人类接管当算法选项 |

## 7. 简单用户话术

开始前：

> 我会先拆问题，再定点检索，最后把结论回溯到一手来源；不会把搜索摘要直接当答案。

交付时：

> 我给你的是三样东西：方向（先找一手/原始出处）、方式（SIFT+CRAAP 过滤，布尔/操作符精搜，独立交叉验证+存档核验）、边界（什么时候不能下结论）。

分歧时：

> 如果哪条和你的直觉冲突，请说“我感觉不对劲”。我会停下来检查是不是检索或核验错了，而不是硬套模板。

## 8. 校验 / 回测

交付或使用前干跑 3–5 个真实查询：

1. 能否把用户问题拆成 1–3 个子问题？
2. 每个关键结论是否有可访问的一手/原始来源？
3. 是否至少 2–3 个真正独立的来源（非同一通稿）？
4. 是否回到原文核验了语境/摘要/引用？
5. 是否明确标注了“事实/推断/未知”与支持程度？
6. 是否有反例/边界说明什么情况下不适用？

有数值评估时（如搜索命中率、误引率），抽 20–50 个样本记录：是否找到一手来源、是否多源独立、是否错误引用、是否过度声称。只用让指标变好的规则；有争议的进入 shadow 模式。

## 9. 来源表

| 主题 | 来源 | 贡献 |
|---|---|---|
| 精确检索 | [Google Search Help: Refine web searches](https://support.google.com/websearch/answer/2466433?hl=en) | 官方操作符/空格/引号说明 |
| 精确检索 | [Bing: Advanced search options](https://support.microsoft.com/en-us/bing/advanced-search-options) | 不同引擎操作符差异 |
| 检索迭代 | [Drexel: Database Searching](https://libguides.library.drexel.edu/c.php?g=1484012&p=11065571) | 布尔、同义词、迭代式数据库搜索 |
| 检索框架 | [Wake Forest: Systematic Reviews Step 3](https://guides.zsr.wfu.edu/c.php?g=1470676&p=10952495) | 系统综述检索步骤/问题拆分 |
| 学术受控词 | [PubMed Help](https://pubmed.ncbi.nlm.nih.gov/help/) | MeSH/主题词与自由词区别 |
| 来源判断 | [Wesleyan College: Types of Sources](https://wesleyancollege.libguides.com/c.php?g=1525965&p=11431022) | 一手/二手/三手来源层级 |
| 来源判断 | [UNCC: SIFT](https://guides.library.charlotte.edu/c.php?g=1499262&p=11347573) | SIFT 四步、横向阅读、回溯原始语境 |
| 来源判断 | [CSU Chico: CRAAP Test](https://libguides.csuchico.edu/c.php?g=414299&p=2822727) | Currency/Relevance/Authority/Accuracy/Purpose |
| 交叉验证 | [Stanford Civic Online Reasoning](https://cor.inquirygroup.org/blog/module-for-high-school/) | 横向阅读、独立来源，避免单信源依赖 |
| 事实核验 | [Poynter: How to uncover out-of-context quotes](https://www.poynter.org/fact-checking/2023/how-to-uncover-out-of-context-quotes/) | 断章取义/上下文核验 |
| 摘要风险 | [Full Fact: Google snippet eating glass](https://fullfact.org/health/google-snippet-eating-glass/) | 精选摘要可错的实例 |
| 图像/视频 | [Bellingcat Toolkit: InVID](https://bellingcat.gitbook.io/toolkit/more/all-tools/invid) | 视频拆帧/核验工具 |
| 存档 | [Wayback Machine](https://web.archive.org/) | 链接失效时查历史快照 |
| Agent 引用 | [Hermes Agent: Grounded Citations](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-grounded-citations) | 引用必须存在且支持结论 |
| Agent 检索 | [Firecrawl Research Engine](https://github.com/hecailiaoPFS/firecrawl-research-engine) | search-first、优雅降级、防幻觉 |
