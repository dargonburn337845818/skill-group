# 检验与验证共识 · 来源清单

> 分级：`consensus` = 多来源重复；`style` = 单一专家独特做法；`warning` = 反例/边界；`common-lore` = 无直接引用但圈内普遍认同（已降权）。

| 来源 | 主题 | 贡献 | 分级 |
|---|---|---|---|
| [WordPress agent-skills authoring-guide](https://github.com/WordPress/agent-skills/blob/trunk/docs/authoring-guide.md) | 确定性 Skill 创作门禁 | SKILL.md 简短、确定性脚本、eval 场景、frontmatter 校验 | consensus |
| [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | 官方 Skill 创作规范 | 元数据第三人称、渐进披露、引用一层深、测试多模型 | consensus |
| [Anthropic docs 镜像 shipyard](https://github.com/lgbarn/shipyard/blob/main/skills/shipyard-writing-skills/anthropic-best-practices.md) | Anthopic 实践摘要 | 自由度分级、质量检查表、反模式 | consensus |
| [uinaf/agents skill-audit best-practices](https://github.com/uinaf/agents/blob/3cd37beb662b9038c5e1031fea4968e908741b5c/skills/skill-audit/references/best-practices.md) | Skill 审计清单 | 元数据/身体形态/渐进披露/审计问题 | consensus |
| [skilljack-evals](https://github.com/olaservo/skilljack-evals) | Skill 评测 CLI | 任务先行 TDD、无 skill 基线、Skill Lift、anti-trigger、oracle gate、judge 不门禁 | consensus |
| [claude-workflow-kit](https://github.com/ncoevoet/claude-workflow-kit) | Evidence-first 开发/验证 | claim-class 证明表、prove 可证伪、对抗规格审查、commit/spec gates、in-flight 阻断 | consensus |
| [Promptfoo Red Team Coding Agents](https://www.promptfoo.dev/docs/red-team/coding-agents/) | 编码 agent 红队 | 对交付物做对抗证据收集；按风险选证据 | consensus/style |
| [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) | 专业级 Skill 编写/LLM 验证/上下文窗口 | 元数据、可执行内容、验证实践、lean context | consensus |
| [Anthropic Engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | 官方工程实践 | Agent Skills 的真实世界落地、渐进披露与工具生态 | consensus |
| 本地 `distillation-consensus` | 蒸馏三件套/来源纪律 | trigger/action/boundary + source_refs | common-lore（本地实践） |
| 本地 `value-validator` | 收敛判定 | 四条硬规则、数值可复算 | common-lore（本地实践） |
| 本地 `dsh-optimization-consensus` | 运维安全 | 不热更、隔离冒烟、回滚恢复实际文件 | common-lore（本地实践） |

## Round 37 新增来源

| 来源 | 主题 | 贡献 | 分级 |
|---|---|---|---|
| [OpenAI Evals（README/docs/custom-eval）](https://github.com/openai/evals) | 通用 LLM 评测框架 | eval 即测试：数据集 + grader；私有/自定义 eval 防污染；确定性 grader 与模型打分并存 | consensus |
| [Promptfoo Deterministic Metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/deterministic/) | 确定性断言矩阵 | contains/regex/json/sql/f-score/python/webhook 等逻辑断言；应优先于模型打分 | consensus |
| [Promptfoo Evaluate Coding Agents](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/) | Agent 评测差异 | 多步非确定性累积、需要轨迹/沙箱/多步断言，不能只验最终输出 | consensus |
| [Promptfoo Sandboxed Code Evals](https://www.promptfoo.dev/docs/guides/sandboxed-code-evals/) | 生成代码隔离评测 | 在隔离容器执行生成代码，防安全风险并记录环境 | style |
| [Promptfoo LLM Red Teaming](https://www.promptfoo.dev/docs/guides/llm-redteaming/) | LLM 自动化红队 | 20+ 漏洞类型（注入/越权/PII/越狱/窃取），按类目生成对抗证据 | consensus |
| [Inspect AI Scorers](https://inspect.aisi.org.uk/scorers.html) | 标准/自定义 scorer | includes/match/pattern/exact/f1 等确定性 scorer；复杂才用 model grading；离线评分 | consensus |
| [DeepEval Metrics Introduction](https://deepeval.com/docs/metrics-introduction) | 评测指标设计 | metric 即“尺子”；reference vs referenceless；component vs trajectory；LLM-judge 限定任务 | consensus |
| [EvalPlus](https://github.com/evalplus/evalplus) | 严格代码评测 | 对 HumanEval 类弱测试集做测试增强，暴露隐藏错误与过拟合 | consensus |
| [SWE-bench](https://github.com/SWE-bench/SWE-bench) | 真实 GitHub issue 评测 | 真实 issue + 测试补丁；Docker 固定环境执行；FAIL_TO_PASS/PASS_TO_PASS 双门禁 | consensus |
| [Stryker Mutator](https://stryker-mutator.io/) | 变异测试 | 变异→跑测试→统计存活变异；验证测试套件自身质量 | consensus |
| [Martin Fowler: Test Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html) | TDD 方法论 | Red-Green-Refactor、先列测试清单、test-first 推动接口设计 | consensus |

