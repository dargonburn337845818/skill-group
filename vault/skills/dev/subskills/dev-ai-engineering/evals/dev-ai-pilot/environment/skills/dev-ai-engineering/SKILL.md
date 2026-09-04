---
name: dev-ai-engineering
description: LLM/Agent 工程子技能——LLM API 契约、上下文预算与持久化、RAG 检索、工具调用契约、Agent 循环、评测与降级/成本边界的可执行检查清单；来源以官方工程文档与一手文档为主。
whenToUse: 用户设计/实现/审查 LLM API 集成、Agent、RAG、工具调用、评测或成本控制的方案时；需要把 LLM 工程经验变成可检查动作时。
---

# dev-ai-engineering · LLM/Agent 工程（已蒸馏）

> 定位：给 dev 模块提供“LLM/Agent 工程判断”的最小可执行集。模型能力细节交给具体 provider 文档；这里只冻结可复用的工程边界。
> 核心原则：**把上下文当有限预算，把工具当可验证契约，把 Agent 当有状态循环，把评测当作回归门禁。**

## 触发条件

- 用户要接 LLM API、写 prompt/系统提示、做 RAG、设计工具/MCP、跑 Agent 循环。
- 需要审查一个 AI 方案：上下文会不会爆、检索会不会瞎、工具能不能被模型正确使用、失败时怎么降级。
- 用户问“这个 Agent 怎么不收敛 / 成本怎么控 / 怎么证明改进了”。

## 核心动作

### 1. LLM API 契约

- **模型与版本显式固定**：在配置/环境记录 provider、model、版本或日期；不要只写“gpt-4”之类会漂移的短名。
- **请求契约机器可读**：系统提示、工具 schema、输出 JSON Schema 都落盘为可校验文件；用 provider 的结构化输出/JSON mode 时仍要在代码侧做 schema 校验。
- **错误要分型**：区分 `rate_limit`、`context_length`、`invalid_request`、`upstream_error`、`bad_response`；分别对应退避、截断/压缩、修复请求、重试、转人工。
- **超时/重试/幂等**：非幂等副作用先做幂等键；重试只对可安全重试的请求；流式响应要处理中断与半包。
- **token 与成本可观测**：记录每次请求的 `input_tokens` / `output_tokens` / 工具调用次数，能按任务/租户聚合。
- **缓存前缀稳定**：prompt caching 受益于稳定前缀；把易变内容（时间、用户数据）放在可变后缀，不要污染缓存键。

> 边界：不同 provider 的参数、重试语义、缓存策略不同；不要把一个厂商的魔数写成普适常量。

**可证伪检查**：构建一个“请求契约校验”测试——故意传非法工具参数/坏 JSON，系统必须拒绝或明确报错，而不是悄悄容忍。

### 2. 上下文管理与持久化

- **上下文是有限预算**：为每个任务设 token 预算；写代码时不要把“可能有用”的全文都塞进去。
- **持续精简**：每轮/每阶段后压缩对话：保留目标、约束、已完成事项、下一步；丢弃已无用的工具输出与重复摘要。
- **长任务必须留持久化手牌**：跨多个 context window 的任务，把状态写进文件/数据库/git：进度文件、变更清单、`init` 脚本、可恢复的 checkpoint；不能让新 session 靠猜。
- **先做初始器，再做增量器**：第一个 session 负责搭好环境与初始状态；后续 session 每次只做增量进步，并在结束时留下干净状态（可合并、无半成品）。
- **引用优于复述**：检索/工具结果尽量给 `source + chunk/id`，让模型引用原文而不是把长文再复述一遍。

> 边界：短单次任务不必做完整持久化；但“跨会话/跨窗口”的任务必须做，否则等于用记忆而不是工程解决上下文问题。

**可证伪检查**：在长任务的第二个 session 中，不读持久化状态就无法知道“做到哪一步”时，应判为失败；必须能从进度文件+git 恢复。

### 3. RAG 检索

- **检索是管线不是一句向量搜索**：查询改写/分解 → 混合检索（关键词+向量）→ 重排 → 过滤/去重 → 组包，每一步都留日志。
- **chunk 要自包含**：带来源、时间、章节/ID、必要上下文；宁可小而准，不要大而糊。
- **阈值与“不知道”**：设置最低相关性阈值；低于阈值时明确输出“证据不足/未找到”，禁止用模型补编答案。
- **引用可回溯**：答案中的每个事实尽量挂来源 chunk id；评测时检查“无支撑断言”数量。
- **防止检索污染**：对用户可控输入/外部文档做来源标记与权限过滤；不要把私人数据或高权限文档无差别喂给低权限场景。

> 边界：小语料/单文档问答不必重排；但“检索影响回答正确性”的应用必须有阈值、去重与引用。

**可证伪检查**：构造 10 题“答案必须来自给定语料”的评测；若某题答案正确但对应来源 chunk 不在检索结果中，记为失败。

### 4. 工具调用契约

- **工具是给 Agent 的接口**：名称要命名空间化且边界清晰，描述要写清“做什么、什么时候用、返回什么”；不要只写函数签名。
- **schema 严格**：参数类型、必填、枚举、长度都定义；服务端验证输入，非法参数返回结构化错误，不要静默转换。
- **返回结果可消费**：返回结构化 JSON + 状态 + 少量必要字段；不要返回整页日志/HTML/超大原始数据。
- **错误要可行动**：失败时给“为什么失败 + 下一步建议 + 状态码/错误码”，让 Agent 能决定重试、换工具还是上报。
- **工具不要贪多**：按任务加载必要工具；同一领域用命名空间分组；上百个工具会稀释注意力与选择质量。
- **副作用要可控**：写操作尽量幂等；破坏性/不可逆操作先确认、留审计、设权限边界。

> 边界：内部脚本工具可以粗糙；但要被 Agent 复用的工具必须按“人机都可读”的契约写。

**可证伪检查**：用“错误参数 + 正常参数”两组用例跑工具；错误参数必须被 schema 拒绝，正常用例返回的可消费 JSON 能被下游稳定解析。

### 5. Agent 循环

- **显式状态机**：定义 `gather → decide → act → verify → update` 循环；每步有输入/输出，不要只给一句“让它自己看着办”。
- **有界运行**：设置 `max_steps`、`max_tokens_per_step`、`max_cost`、`max_wall_time`；到达上限必须停止并汇报，不能静默继续。
- **增量交付**：长任务按 feature/阶段推进，每个 session 只做一小步，结束时留干净状态；避免“一次想做完”。
- **失败处理**：同一工具连续失败 N 次后换策略或升级用户；循环中出现格式/工具错误先修错误本身，不要盲目重试。
- **并行要有界**：并行工具调用设上限并考虑副作用顺序；有关联/相互覆盖的操作串行。
- **人在环**：不可逆、高成本、权限提升、对外发送等动作前暂停并请用户确认/授权。

> 边界：简单“单轮调用 + 解析”不是完整 Agent 循环，不需要状态机；但多步/长时间任务必须有。

**可证伪检查**：跑一个“工具永远失败”的测试用例，Agent 必须在重试上限后停止并输出明确错误，而不是无限循环或假装成功。

### 6. 评测 / 降级 / 成本

- **任务先行**：评测集来自真实任务，每条有输入、期望输出/检查点；至少 10 条，覆盖关键分支与失败模式。
- **回归门禁**：改 prompt/模型/工具/检索后先跑同一评测；记录准确率、工具错误率、平均步骤、延迟与 token 成本，不当场只看手感。
- **降级路径**：定义“主模型失败/超预算/工具不可用”时的 fallback：降模型、降功能、走规则/缓存、转人工；降级也要有指标。
- **成本有预算**：每任务设置 token/金额上限；缓存、批量、小模型分流；高价值任务用强模型，低价值任务用弱模型。
- **记录决策**：评测结果、降级触发、成本数据写入报告；不要把“看起来更好”当证据。

> 边界：没有真实任务样本的“模板评测”不能声称“有提升”；至少要有可重复执行的检查集与基线对照。

**可证伪检查**：给出“新版相对旧版在 N 条评测上不回归”的断言；如果某条由人工目测通过但无法用检查脚本复现，必须降级为“未验证”。

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “把整份维基喂进 prompt，反正模型上下文大” | 先定义预算，检索后压缩/筛选，保留引用 |
| “工具返回全部原始日志，模型自己会找” | 返回结构化、带错误码的最小可消费结果 |
| “Agent 卡住就多给它几轮提示” | 检查状态机/工具契约/上下文是否干净，设 max_steps |
| “换了个新模型，感觉更聪明了” | 跑同一评测集，对比准确率/成本/错误率 |
| “RAG 没搜到就让模型猜” | 低于阈值时明确“证据不足”，禁止编造 |
| “低风险任务也用最强模型” | 按风险/收益分流，设成本预算与降级路径 |
| “prompt caching 只要写了 system 就有效” | 检查前缀稳定性与缓存命中日志，再决定是否启用 |

## 来源

- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic: Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [OpenAI: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)
- [LangChain: Retrieval docs](https://docs.langchain.com/oss/python/langchain/retrieval)
- [AWS Prescriptive Guidance: Writing best practices for RAG applications](https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/writing-best-practices-rag/writing-best-practices-rag.pdf)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`、`vault/skills/core-iteration/dev-workflow-consensus/`
