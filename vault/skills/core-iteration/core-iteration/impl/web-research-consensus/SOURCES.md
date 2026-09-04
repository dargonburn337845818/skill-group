# 网络信息搜集共识 · 来源清单

> 本清单记录本次“网络信息搜集技巧”蒸馏研究参考的公开资料。
> 说明：这些链接用于交叉验证与继续深挖；本共识不是对任一来源的逐句搬运，而是抽取共性后重新组织。
> 分级：`consensus` = 多来源重复；`style` = 单一专家独特做法；`warning` = 反例/边界；`common-lore` = 无直接引用但圈内普遍认同（已降权）。

## 精确检索

| 来源 | 主题 | 贡献 | 分级 |
|---|---|---|---|
| [Google Search Help: Refine web searches](https://support.google.com/websearch/answer/2466433?hl=en) | 官方搜索优化 | 引号、`site:`、`filetype:`、排除词、日期等确定性操作 | consensus |
| [Bing: Advanced search options](https://support.microsoft.com/en-us/bing/advanced-search-options) | Bing 高级搜索 | 不同引擎操作符差异，不能只依赖单引擎 | consensus |
| [Drexel: Database Searching](https://libguides.library.drexel.edu/c.php?g=1484012&p=11065571) | 数据库检索 | Boolean、同义词、迭代式搜索 | consensus |
| [Wake Forest: Systematic Reviews Step 3](https://guides.zsr.wfu.edu/c.php?g=1470676&p=10952495) | 系统综述步骤 | 问题拆分、检索流程 | consensus |
| [PubMed Help](https://pubmed.ncbi.nlm.nih.gov/help/) | 医学数据库 | MeSH/主题词与自由词的区别 | consensus |

## 可靠来源判断

| 来源 | 主题 | 贡献 | 分级 |
|---|---|---|---|
| [Wesleyan College: Types of Sources](https://wesleyancollege.libguides.com/c.php?g=1525965&p=11431022) | 来源类型 | 一手/二手/三手来源层级 | consensus |
| [UNCC: SIFT](https://guides.library.charlotte.edu/c.php?g=1499262&p=11347573) | SIFT / 横向阅读 | Stop/Investigate/Find better coverage/Trace to original | consensus |
| [CSU Chico: CRAAP Test](https://libguides.csuchico.edu/c.php?g=414299&p=2822727) | CRAAP | Currency/Relevance/Authority/Accuracy/Purpose | consensus |
| [Stanford Civic Online Reasoning](https://cor.inquirygroup.org/blog/module-for-high-school/) | 公民在线推理 | 横向阅读、独立来源、避免单信源依赖 | consensus |

## 高效核验

| 来源 | 主题 | 贡献 | 分级 |
|---|---|---|---|
| [Poynter: How to uncover out-of-context quotes](https://www.poynter.org/fact-checking/2023/how-to-uncover-out-of-context-quotes/) | 断章取义 | 读完整上下文、保留时间线/前提/让步 | consensus |
| [Full Fact: Google snippet eating glass](https://fullfact.org/health/google-snippet-eating-glass/) | 搜索摘要错误实例 | 不要信任摘要/精选摘要 | warning |
| [Bellingcat Toolkit: InVID](https://bellingcat.gitbook.io/toolkit/more/all-tools/invid) | 视频核验 | 拆帧、元数据、原发时间 | style/consensus |
| [Wayback Machine](https://web.archive.org/) | 网页存档 | 链接失效时回溯 | consensus |

## Agent 检索与引用

| 来源 | 主题 | 贡献 | 分级 |
|---|---|---|---|
| [Hermes Agent: Grounded Citations](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-grounded-citations) | 落地引用 | 引用必须“存在”且“支持结论”，不能事后附会 | consensus |
| [Firecrawl Research Engine](https://github.com/hecailiaoPFS/firecrawl-research-engine) | Agent 深度检索 | search-first、优雅降级、防幻觉、引用核验 | style（社区实践，多 agent 项目交叉出现） |
| [Agentic Search / Citation Verification 类实践](https://docs.agentos.sh/features/citation-verification) | 引用验证 | 模型引文需可访问、可回溯、内容匹配 | common-lore |

## 开源代码与 GitHub

| 来源 | 主题 | 贡献 | 分级 |
|---|---|---|---|
| [GitHub Docs: Using GitHub code search](https://docs.github.com/en/search-github/github-code-search/using-github-code-search) | 代码搜索 | 按代码/路径/语言定位实现片段 | consensus |
| [GitHub Docs: Searching code (legacy)](https://docs.github.com/en/search-github/searching-on-github/searching-code) | 代码搜索 | 旧版/不同版本搜索说明 | consensus |
| [GitHub REST API: Search](https://docs.github.com/en/rest/search/search) | API 检索 | 仓库/代码/issue 结构化搜索 | consensus |
| [GitHub Docs: About searching on GitHub](https://docs.github.com/en/search-github/getting-started-with-searching-on-github/about-searching-on-github) | 搜索范围 | 仓库/代码/issue/PR 的可用入口 | consensus |
| [GitHub Security Advisories](https://github.com/advisories) | 安全公告 | 开源漏洞的一手公告源 | consensus |
| [OSV](https://osv.dev/) | 漏洞数据库 | 跨生态漏洞数据与 API | consensus |
| 本地 `github-repo-consensus` | 仓库可执行共识 | README/安全/Actions/结构检查，交叉指导 | style |

## 本地实践（交叉验证）

- `distillation-consensus`：本 skill 的父共识，要求每条规则带触发/动作/边界/来源。
- `github-repo-consensus`：同类“从外部资料蒸馏成可执行检查表”的本地实例。
- `teacher-consensus-skill`：信息论/提问协议在教研场景的具体应用。
