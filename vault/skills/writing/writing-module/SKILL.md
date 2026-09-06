---
name: writing-module
description: 文稿模块——提示词、文案、文档/报告、学术写作、演讲/口播等文本生产的统一文本服务；供 dev/teacher/research/distill 按公开接口调用，不替代各领域专家判断。
whenToUse: 需要生产或改写提示词、提问稿、文案、PPT 文案、README、组会报告、成果汇报等文本，并由其他模块按文本接口调用时。
---
# 文稿模块（writing-module）

> 定位：**文本服务，不是领域之王。**
> 其他模块把“要表达的素材、对象、场景”交进来，文稿模块负责把话说清楚、说得像、说得体；不负责判断内容对不对、该不该这么做。

## 这个模块是什么

文稿模块是五个正式模块中的文本生产层。它聚合五类子技能：

| 子技能 | 生产什么 | 主要服务对象 |
|---|---|---|
| `prompt-writing` | 提示词、提问稿、多专家讨论 prompt | teacher / research / distill |
| `copywriting` | 文案、PPT 文案、发布说明、去 AI 味改写 | dev / 对外发布 |
| `document-report` | 文档、报告、组会汇报稿、成果汇报 | research / dev |
| `academic-writing` | 学术论文、学位论文章节、LaTeX/BibTeX 排版与引用 | research / teacher / distill |
| `speech-writing` | 演讲、口播、视频脚本、PPT 讲稿与时长控制 | dev / teacher / research / distill |

所有子技能共享同一个**文本接口**：调用方传入 `topic/domain/audience/type`，模块返回可复用的文本骨架或成品；调用方保留领域判断、事实核验与最终决定权。

## 何时使用

- 用户说“帮我写一段提示词 / 提问稿 / 组会汇报 / PPT 文案 / README / 报告 / 学术论文 / 演讲稿 / 视频脚本”。
- dev 模块需要把技术结论包装成用户可读的说明或去 AI 味的发布文本。
- teacher 模块需要把专家观点转成可执行的讨论 prompt 或追问。
- research 模块需要把论文/实验结论转成组会汇报、成果报告或投稿文本。
- distill 模块需要把蒸馏结论包装成 skill 的说明、模板或示例话术。

## 文本接口（与四模块的调用契约）

### 输入（TextRequest）

调用方只需尽量提供以下字段；未提供的字段由模块用占位符或提问补齐，**不静默编造**。

```json
{
  "topic": "本次文本的主题/核心内容",
  "domain": "算法竞赛 | 开发 | 科研 | 通用（影响用词与例证）",
  "audience": "学生 | 开发同行 | 评审 | 客户 | 组会听众 | 大众",
  "type": "prompt | copy | document | report | academic | speech",
  "purpose": "一句话：这份文本要达成什么效果",
  "tone": "可选：严谨 | 轻松 | 鼓励 | 克制 | 激昂",
  "length": "可选：100字 | 一页 | 三页 | 不限",
  "constraints": ["可选：不要出现算法名", "去 AI 味", "引用必须带出处"],
  "references": ["可选：素材/论文/数据/竞品链接"],
  "expert_opinions": ["可选：教师/科研专家已经给定的结论或分歧点"]
}
```

### 输出（TextResult）

```json
{
  "text": "可复用的文本主体（成品或带占位符的骨架）",
  "placeholders": ["需要调用方补填的事实/数据/人名"],
  "questions": ["如果输入不足，这里列出必须由用户/专家回答的问题"],
  "choices": ["可选：多个风格分支，由调用方选择"],
  "notes": "写法说明、边界提醒、引用核验提示"
}
```

### 调用规则

1. **先取素材，后动笔**：调用方负责提供事实、结论、专家意见；文稿模块不自行做领域研究，不编造数据、引用或承诺。
2. **缺什么问什么**：输入不足以支撑“有具体内容的文本”时，输出 `placeholders` / `questions`，而不是替用户随便填。
3. **保留专家署名与分歧**：teacher/research 的多专家讨论文本必须保留 `expert_id` / `expert_name` 与冲突分支；文稿模块只做表达层，不改写结论归属。
4. **可覆写**：模板是起点不是枷锁；调用方说偏离模板时，按新要求重写。
5. **服务不独吞**：最终技术/学术判断由 dev/teacher/research/distill 或其用户负责；文稿模块只对“文本表达质量”负责。

## 专家团调用（标准化流程）

文稿模块可请专家团提供“多视角文本判断”：风格、受众、说服力、结构取舍。

- 默认写作专家：`william-zinsser`（On Writing Well 风格/方法论）。
- 论文/学术写作可叠加：`paul-halmos`（数学写作）、`donald-knuth`（数学写作与排版）、`steven-pinker`（学术写作/去知识诅咒）。
- 需要产品/体验视角时叠加 `product-ux`：`don-norman`、`jakob-nielsen`、`julie-zhuo`。
- 需要科研/技术受众时叠加 `research` 或对应 dev 领域专家。
- 调用方式与 teacher 模块一致：`expert_team_start(text="文案评审", expert_ids=["william-zinsser"])` → 回合式表态 → 冲突裁决 → 带署名的文本建议。
- 文稿模块只负责把专家署名意见组织成文本，不改变结论归属。

## 如何被其他模块调用

### dev → writing

```
dev 传入：topic=“xx 功能发布说明”、domain=开发、audience=开发同行/产品、
         type=copy, constraints=["去 AI 味","不夸大"]
writing 返回：发布说明草稿 + 可选的“人味改写”版本 + 需补填的截图/数据占位
```

- 用于：README、更新日志、PR 描述、PPT 文案、公告、去 AI 味审查。
- 边界：不替 dev 判断技术正确性；技术细节不确定时留 `[待确认]` 占位。

### teacher → writing

```
teacher 传入：topic=“算法题 A 的引导方向”、domain=算法竞赛、audience=学生、
         type=prompt, expert_opinions=[“tourist: 先暴力后优化”, “jiangly: 找不变量”]
writing 返回：可连续追问的提问稿；每位专家观点标正确认来源；分歧保留为分支
```

- 用于：拆题提问流、多专家讨论 prompt、课程讲解稿、反馈话术。
- 边界：不修改教师的判断方向；只把观点组织成自然、有梯度的语言。

### research → writing

```
research 传入：topic=“本周论文进展”、domain=科研、audience=组会听众,
         type=report, references=[论文/实验数据]
writing 返回：一页式组会汇报稿 + 模拟问答草稿 + PPT 分页文案
```

- 用于：组会报告、成果汇报、论文写作中的章节初稿、学术论文写作、PPT 讲稿、演讲/口播稿。
- 边界：不替代论文原文与数据；涉及公式、数字、结论归属时全部留引用/占位，交由科研模块核验。

### distill → writing

- 用于：把蒸馏结论写成 skill 的说明、示例、模板、用户话术。
- 边界：不改变蒸馏产物的证据与来源；只负责“说得清楚”。

## 文本质量底线

1. **具体 > 抽象**：优先给可执行句子、可复现动作、可核验事实。
2. **有标点、有节奏、有开口**：提示词要能被直接使用；文案要有语气；报告要有结论先行。
3. **不制造伪引用**：没有来源的“专家说”“研究表明”一律不写，改为 `[来源后续]`。
4. **不伪深刻**：不为了显得高级堆术语；面向谁就用谁的语言。
5. **去 AI 味**：在 dev 场景尤其注意，避免“首先/其次/总而言之”“赋能”“闭环”等空泛高频词，改用具体动作和短句。

## 子技能入口

- [提示词写作 subskill](./subskills/prompt-writing/SKILL.md)
- [文案写作 subskill](./subskills/copywriting/SKILL.md)
- [文档/报告 subskill](./subskills/document-report/SKILL.md)
- [学术写作 subskill](./subskills/academic-writing/SKILL.md)
- [演讲/口播 subskill](./subskills/speech-writing/SKILL.md)

## 示例模板

- [提示词模板](./examples/prompt_template.md)
- [文案模板](./examples/copy_template.md)
- [报告模板](./examples/report_template.md)

## 边界与反模式

| 场景 | 不要做 |
|---|---|
| 调用方只给 topic，要求“写一篇专业报告” | 不要直接编内容；输出骨架 + 明确 `placeholders` / `questions` |
| teacher 给专家观点 | 不要抹平分歧、不要替换专家署名 |
| research 给论文 | 不要绕过原文编造实验结果；数字/引用留 `[待核对]` |
| dev 要“去 AI 味” | 不要只做同义词替换，要重写句法和语气 |
| 任何模块要求“权威/专业” | 不要用“业内公认”等无来源断言；用具体证据或留空 |

## 2026 深度补强（Round 36）

> 本轮补强点是文稿模块/文本服务本体的五件事：**接口设计、受众分层、风格指南、去 AI 味、可复现文本交付**。
> 每条都带“触发 / 动作 / 反例 / 边界 / 来源”；与已有子技能 Round 32/34 内容不重复。

### R36-1 内容模式先于文体：把 `type` 落到 Diátaxis 四模式

- **触发**：调用方只给 `type=document` 或 `type=copy`，但没说清这份文本是“教人学会”“完成任务”“查参数”还是“理解原理”；或同一份文档四种模式混杂。
- **动作**：
  - 把文本目标先归入四种模式：**tutorial（学习者获得技能）**、**how-to（解决具体任务）**、**reference（快速查信息）**、**explanation（理解背景/取舍）**。
  - 若调用方没给模式，按 `purpose` 推断，并把推断写进 `notes`；拿不准时返回 `mode_question` 而不是硬写。
  - 不同模式切换措辞与结构：tutorial 用“你 + 现在进行”，多给练习与反馈；how-to 用祈使句步骤 + 前提 + 预期结果；reference 用统一字段模板 + 可扫描排版，不写叙事；explanation 用类比、因果、权衡，少给操作步骤。
- **反例**：把“教新用户首次配置”写成 API 字段全表；或把“这个功能为什么这样设计”写成“第一步、第二步”的操作清单。两者都让读者找不到自己需要的模式。
- **示例**：`purpose=“教用户 10 分钟内完成第一次部署”` → 选 `how-to`/`tutorial`，正文先给“跑通的最小命令”，把全部参数表移到 appendices。
- **边界**：同一产品文档可多模式并存，但应**分文件或分显式大节**（如 `## Tutorial`、`## Reference`、`## Why this works`），不要在同一段里来回切。
- 来源：[Diátaxis · Start here](https://diataxis.fr/start-here/)、[GitHub Docs · Style guide and content model](https://docs.github.com/en/contributing/style-guide-and-content-model/style-guide)

### R36-2 受众分层：从标签进到“用户需求声明”

- **触发**：输入只有 `audience=“开发者/学生/评委”`；写完发现读者其实不知道“这篇对他有什么用”；或同一篇稿子服务多个角色却只按一个角色写。
- **动作**：
  - 动笔前把 `audience + purpose` 合成一句 **user need**：`As a [角色], I need [可观测结果], because [处境/动机].` 例如 `As a 新用户, I need 在 10 分钟内完成第一次部署, because 我只有 10 分钟且没有文档背景。`
  - 把这句话放进 TextResult 的 `need_statement`；之后每个段落若不能服务它，就删掉或移到附录。
  - 用“任务/决策”而不是“职位名”分受众：决策者要“决定是否合入”，执行者要“照步骤完成”，复现者要“拿到原始参数”。
  - 至少区分主读者与次要读者：主读者决定正文密度，次要读者需要的信息放附录/折叠区。
- **反例**：`audience=开发者, purpose=介绍功能` → 写成面面俱到的功能清单；主读者（想判断“要不要用”）与次要读者（想查参数）都被淹没。
- **示例**：主读者=评审（30 秒抓结论），次读者=复现者（附录给命令 + 参数），正文不放实验细节。
- **边界**：若调用方/领域专家明确不认同该 user need，以 expert 判断覆盖；文稿模块只负责把需求声明写清楚，不替用户定义“他到底需要什么”。
- 来源：[GOV.UK · Identify user needs](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/identify-user-needs/)、[Google Technical Writing · Audience](https://developers.google.com/tech-writing/one/audience)

### R36-3 风格指南是最小可交付契约：voice/tone + 术语表 + 正反例

- **触发**：同一模块/仓库多份文本由不同人或 AI 产出，语气不一致；同一个概念出现 `用户/客户/使用者/消费者` 多种叫法；或“去 AI 味”只靠感觉、没有可复核标准。
- **动作**：
  - 每个文本服务维护一份**最小风格指南**，至少 5 块：`1) voice/tone 一句话；2) 人称与语气词；3) 术语表 term / accepted / rejected / example；4) 句式偏好；5) 正反例`。
  - 术语表**一次只选一个词**；首次出现给定义，之后全篇统一；不为了显得专业换同义词。
  - 句式偏好：短句优先、主动语态、直呼读者 `you`（避免 `the user` 抽象）；标题用句子式或问题式；用 sentence case（协议名/品牌名除外）。
  - 包含性写作：避免男性泛称（`manpower`）、默认正常化的贬义隐喻（`sanity check`）、基于人群的泛化标签；需要时用“人”或具体角色。
  - 风格指南本身要可 diff：放 `STYLE.md` 进仓库，并在每次交付的 `notes` 注明“按哪一条执行/偏离了哪一条”。
- **反例**：同一篇 README 里 `点击 / 单击 / 按下 / 点按` 混用；或者没有 STYLE.md，于是每轮都凭感觉重新发明语气。
- **示例**：`deploy`（accepted）；`发布/上线`（rejected，除非语境是 App Store）；`Run npm run deploy.`（正例），`进行部署操作`（反例）。
- **边界**：风格指南不改变领域术语；若领域已约定（如 `API`、`接口`），以领域为准；不要用风格指南把“必须核验的事实”改成“感觉”。
- 来源：[Google developer documentation style guide · Voice and tone](https://developers.google.com/style/tone)、[Microsoft Writing Style Guide · Welcome](https://learn.microsoft.com/style-guide/welcome/)、[Microsoft · Bias-free communication](https://learn.microsoft.com/style-guide/bias-free-communication)

### R36-4 去 AI 味：从“删几个词”升级为“句法级 tells 检查”

- **触发**：用户说“太 AI 了”，但按旧检查表删掉“首先/其次/赋能”后仍很机器；或出现 `It's not X, it's Y`、`Great question!`、`Let's dive into`、`delve/tapestry/testament/leverage`、整齐三段平行、破折号密集。
- **动作**：执行五层检查：
  1. **词汇层**：`delve, tapestry, testament, leverage, unlock, elevate, seamlessly, empower, robust, pivotal, nuanced` 等高频 AI 词——能换就换，不能换就保留（词本身不是罪）。
  2. **句式层**：固定开场/转折模板——`It's not X, it's Y`、`Whether you're X or Y`、`In today's fast-paced world`、`It is worth noting`、`Let's dive into`、`Great question!`。
  3. **结构层**：每段三句完美平行、答案永远“首先/其次/最后”、段落等长、每个观点都“先概括后展开”——像模板拼装。
  4. **标点层**：破折号/分号密度异常、连续项目符号、感叹号堆叠。
  5. **人味层**：缺具体数字、时间、失败、取舍；没有第一人称观点；没有“我们在这里卡住/换过方案”的真实施工痕迹。
- **改写策略**：把模板句改成“具体观察 + 具体动作”；把 `not X, but Y` 直接说 Y 或给对比数据；把 `Great question!` 删掉直接答；刻意让长短句交错、允许一个不完美句；补一条原文不可替代的事实/代码/失败。
- **反例**：`Whether you're a beginner or an expert, this tool empowers you to seamlessly elevate your workflow.` → `这个工具对新手：一条命令跑通；对老手：可覆盖默认配置。实测在新电脑上 3 分钟完成安装。`
- **边界**：不能为“像人”牺牲准确性，更不能编个人经历；口播/TTS 可保留少量排比作节奏，但不要三段全同构；中英文 AI tells 不完全相同，先收集你所在语料的真实 tells。
- 来源：[NYT · Why Does A.I. Write Like … That?](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html)、[vale-ai-tells（社区规则地板，不是检测器）](https://github.com/krishnasunkam/vale-ai-tells)、[anti-ai-writing-style（社区改写指南）](https://github.com/shaswatco/anti-ai-writing-style)

### R36-5 Plain language 不是降智：专家同样受益

- **触发**：把“读者是专家”当理由写满术语；或担心“写简单”显得不专业；或专家读者也要反复查术语。
- **动作**：
  - 用短句、主动语态、具体名词**不降低信息密度**——简单不等于少内容，更不等于少技术。
  - 首次出现专业术语给一句话定义或链接；之后统一用缩写/简称；不要让“懂行”成为读者门槛。
  - 把“显著提升/高度优化/业界领先”换成可核验数字或具体机制；通用评价词对专家同样无效。
  - 自检：把文档给比目标读者低一级的人看，他能否说出“我该做什么/该查什么”？不能，说明抽象词太多。
- **反例**：为了显得专业，把“能设置”写成“具备可配置化能力”；把“错误率更低”写成“表现更优”却不说低多少。
- **示例**：`显著改进` → `错误率从 8.1% 降到 2.3%（n=1000，95% CI ±0.4）`。
- **边界**：`API`、`梯度下降` 这类术语不必全部翻译；但每个术语要“先定义后使用”，不要用术语堆砌代替解释。
- 来源：[NN/g · Plain Language For Everyone, Even Experts](https://www.nngroup.com/videos/plain-language-for-experts/)、[Google · Voice and tone](https://developers.google.com/style/tone)

### R36-6 可复现文本交付：源文件 + 生成命令 + 校验三元组

- **触发**：文本只在对话里生成、没有落盘；同一文本出现 `v1`、`final`、`final2` 多个版本；交付后无法回答“基于哪份来源、跑过什么检查”。
- **动作**：
  - 文本交付按**三元组**给：`source`（可编辑源文件路径）、`render_command`（从源到成品的命令，如 `pandoc`、`mkdocs build`、`pnpm docs:build`）、`checks`（`markdownlint`、`vale`、链接检查、字数/时长脚本）。
  - 版本化：文本随仓库/代码使用语义化版本，变更记入 `CHANGELOG.md`（`Added/Changed/Fixed/Removed`），文档变更与对应代码变更同 PR；不用 `final_v2_new.docx`。
  - 审阅门禁：文档评审与代码评审同门——作者给 Better/Best 替代建议，评审给可执行替代；合入前跑校验脚本；过期文档标记 deprecated 或删除。
  - 如果调用方只要一段文案而非仓库文档，也至少返回 `version + date + owner + source_refs`，保证可找回同一版。
- **示例**：`repro = { source: "docs/quickstart.md", command: "pnpm docs:check && pnpm docs:build", checks: ["markdownlint", "links", "vale-ai-tells"] }`
- **反例**：把最终文本直接粘在聊天里，没有版本与来源；下次说“再改一点”无法 diff、无法回归。
- **边界**：短文/口播稿可轻量到“文件 + 日期 + 来源”即可，不必上完整 CI；但“能找回上一版”是底线。
- 来源：[Write the Docs · Docs as Code](https://www.writethedocs.org/guide/docs-as-code/)、[GitHub Docs · Best practices for writing docs](https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs)

### R36-7 一文档一模式；确实要混合就显式分区

- **触发**：一份稿子同时“教入门、列 API、讲设计哲学”；或 README 既想当教程又想当 reference；或读者三种任务都在同一节里找。
- **动作**：
  - 先确定主模式（tutorial / how-to / reference / explanation），其余内容拆到独立文件或独立大节。
  - 推荐拆分：`tutorial.md`（带步骤学）、`reference/`（字段/参数/API 速查）、`explanation.md`（为什么这样设计）。
  - TextResult 中只保留主模式正文；次模式内容放 `choices`/`notes` 或单独交付物，不静默混排。
  - 读者提问驱动选择：`怎么用 X` → how-to；`X 是什么/有哪些参数` → reference；`为什么用 X 而不是 Y` → explanation；`教我一步步做` → tutorial。
- **反例**：把 API 字段表、安装步骤、设计权衡写在同一节，三种读者都需要全文扫描。
- **示例**：同一功能：`tutorial.md` 教人搭起来；`reference.md` 列全部 flag；`explanation.md` 讲取舍。
- **边界**：短文档可用显式分区；分区后每个区仍应保持模式纯度。学术论文/组会报告是另一种文本类型，不强行套用这四模式。
- 来源：[Diátaxis · Start here](https://diataxis.fr/start-here/)

### Round 36 执行检查清单

- [ ] 已把 `type/purpose` 映射到 tutorial / how-to / reference / explanation 中的**一个主模式**
- [ ] 已有 `need_statement`：每个段落都能回答“主读者今天要做什么决定”
- [ ] 已按最小风格指南统一：voice/tone、人称、术语表、正反例；术语全文唯一
- [ ] 已过“五层 AI tells”：词汇 / 句式 / 结构 / 标点 / 人味；不是只删词
- [ ] 已交付 `repro` 三元组：源文件 + 生成命令 + 校验；版本、日期、owner 可追溯
