---
name: writing-module
description: 文稿模块——提示词、文案、文档/报告、学术写作、演讲/口播等文本生产的统一文本服务；供 dev/teacher/research/distill 按公开接口调用，不替代各领域专家判断。
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
3. **不制造伪引用**：没有来源的“专家说”“研究表明”一律不写，改为 `[来源待补]`。
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
