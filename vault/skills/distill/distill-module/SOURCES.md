# 蒸馏模块 · 来源清单

> 本模块是编排层，不产生新算法；以下来源用于说明“模块缺口 → core-iteration → 回填”的依据。

## 正式版蓝图与模块定义

| 来源 | 贡献 |
|---|---|
| `FORMAL_SPEC.md` | 五模块定义、distill 职责、专家缺口处理、assignment 格式 |
| `内部任务分派（未随公开仓库发布） distill/assignment.md` | 本模块交付物与验收 |
| `vault/meta/modules.json` | 各模块 skills/gaps 注册表，回填目标 |
| `vault/meta/domain-profiles.json` | 领域识别 + pending_distill 专家缺口入口 |
| `vault/meta/EXPERT_LIBRARY.json` | 人名专家库；专家蒸馏回填目标 |

## 核心迭代与蒸馏共识

| 来源 | 贡献 |
|---|---|
| `$WORKSPACE/skills/core-iteration/README.md` | 六阶段契约、工具路径、版本表 |
| `$WORKSPACE/skills/core-iteration/value-meta-scheduler/SKILL.md` | 调度器输入/轮次/收敛契约 |
| `$WORKSPACE/skills/core-iteration/skill-verification-consensus/SKILL.md` | 发布前校验门槛 |
| `$WORKSPACE/skills/distillation-consensus-skill/SKILL.md` | 蒸馏九步、Node 三件套、质量自检 |

## 评测与 runner

| 来源 | 贡献 |
|---|---|
| `core-iteration/tools/scaffold_eval_task.py` | skilljack-evals 风格任务包脚手架 |
| `core-iteration/tools/skilljack_runner.py` | 真实 DeepSeek agent 循环 + loadSkill / verifier / judge |
| `core-iteration/tools/benchflow_runner.py` | BenchFlow 式矩阵 runner + 门禁 |
| `core-iteration/tools/skill_effect_bench.py` | Skill Lift / 增强指数汇总 |
| [skilljack-evals](https://github.com/olaservo/skilljack-evals) | 任务先行、Skill Lift、oracle gate |
| BenchFlow（本地实现 `benchflow_runner.py`） | 批量矩阵/门禁；已用 dev-security 正例/反例跑出真实结果 |

## Round 38 新增来源

> 本轮为“来源独立性 / 重叠闸门 / 专家证据分级 / 评测卫生 / 回填事务 / 审计轨迹”补充的外部高质量来源。

| 来源 | 贡献 |
|---|---|
| [OpenAI · Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | Skill 评测系统化：任务先行、可发现性/遵守度/质量三维度；支撑 R38-2 的 Skill 边界与 R38-4 评测卫生 |
| [OpenAI · Evaluation Best Practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | 评测基线、校准、防泄漏与样本要求；支撑 R38-4 |
| [Anthropic · Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Agent 评测设计、假阳性与评测陷阱；支撑 R38-4 |
| [OWASP · Universal Skill Format v1.0](https://owasp.org/www-project-agentic-skills-top-10/universal-skill-format.html) | Skill 包/清单的字段与验证格式范本；支撑 R38-5 回填事务化 |
| [LangChain · How We Build Agent Environments & Tasks](https://www.langchain.com/blog/building-agent-environments-and-tasks) | 任务环境、verifier 与可失败基线设计；支撑 R38-4 |
| [Datadog · Evaluating Production-Grade AI Agents Best Practices Guide](https://www.datadoghq.com/resources/evaluating-ai-agents-guide/) | 生产级 Agent 评测指标与门禁；支撑 R38-4 / R38-6 |
| [Trace2Skill · Distill Trajectory-Local Lessons into Transferable Agent Skills](https://ar5iv.labs.arxiv.org/html/2603.25158) | 从轨迹蒸馏可迁移技能；支撑模块缺口→Skill 的蒸馏语料与验证 |
| [SKILL-KD · Skill-level Distillation Framework](https://huggingface.co/buckets/huggingchat/papers-content/tree/2607/2607.28048.md) | 教师 Agent → 学生 Agent 的程序性知识蒸馏；支撑技能蒸馏的层级化 |
| [Oregon State · The CRAAP Test](https://open.oregonstate.education/goodargument/chapter/craap-test/) | 来源可信度四维检查（时效/相关性/权威/准确/目的）；支撑 R38-1 / R38-3 |
| [Where did this come from? · Citation in scientific publications](https://ouci.dntb.gov.ua/en/works/4KQLJBq9/) | 什么时候/如何引用来源；支撑 R38-1 / R38-3 的引用纪律 |
| [What Do ML Researchers Mean by “Reproducible”?](https://ar5iv.labs.arxiv.org/html/2412.03854) | 可复现实验的元数据与记录要求；支撑 R38-6 审计轨迹 |
| [MMLU-CF · Contamination-free Multi-task Benchmark](https://ar5iv.labs.arxiv.org/html/2412.15194) | 评测污染（contamination）与干净基准设计；支撑 R38-4 / R38-6 |

