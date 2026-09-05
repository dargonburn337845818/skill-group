# distill-eval-task · 来源与证据

> 本子技能是蒸馏模块内部子技能（`activation=internal`）。操作手册内容直接来自 core-iteration 的可执行工具与 distill-module 配套文档。
> 采集验证：2026-09-04 实际运行 `--help` 确认 CLI 参数；`real-ab-bench.md` 为模块内一手文档。

## 来源清单

| 来源 | 类型 | 支撑内容 |
|---|---|---|
| `$WORKSPACE/skills/core-iteration/tools/scaffold_eval_task.py` | 可执行工具源码/CLI | 任务包字段、`--task-id/--skill-name/--prompt/--checks/--assertions/--anti-trigger/--out` |
| `$WORKSPACE/skills/core-iteration/tools/skilljack_runner.py` | 可执行工具源码/CLI | 单任务 A/B、`--mode both/no-skill/with-skill`、`--runs`、`--judge`、输出 JSON 字段 |
| `$WORKSPACE/skills/core-iteration/tools/benchflow_runner.py` | 可执行工具源码/CLI | 矩阵 runner、`--config`、`--min-lift-percent`、`--max-discovery-false-positive`、门禁退出码 |
| `$WORKSPACE/skills/core-iteration/tools/skill_effect_bench.py` | 可执行工具源码/CLI | Skill Lift 汇总与 `ENHANCEMENT_REPORT` |
| `$PROJECT_ROOT/vault/skills/distill/distill-module/real-ab-bench.md` | 模块内一手文档 | 任务包结构、oracle gate、基线能失败、至少 3 次、anti-trigger 必测、回填位置 |
| `$PROJECT_ROOT/vault/skills/base/search-source/` | 本地底座 | 来源与检索纪律 |
| `$PROJECT_ROOT/vault/skills/core-iteration/skill-verification-consensus/` | 本地底座 | 可证伪/证据分类/发布门槛 |
| `$PROJECT_ROOT/vault/skills/core-iteration/dev-workflow-consensus/` | 本地底座 | 任务先行与门禁思维 |

## 目录与 id 说明

- 目录名 `subskills/eval-task/` 是任务 Owned Path 固定值；技能 id/name 按任务与 I03 集成登记为 `distill-eval-task`，因此 package checker 的“id/name mismatch dir name”只是任务约定，不是拼贴割裂。

## 可信度说明

- CLI 参数来自 `--help` 实测输出，属于 `verified-high`（工具自身一手）。
- 任务包 schema 与 A/B 纪律来自 `real-ab-bench.md` 与 `skill-verification-consensus` 交叉一致。
- 未使用外部博客/教程；若 runner 版本更新导致参数变化，以 `python3 <tool> --help` 为准并回填本台账。

## Round 40 新增来源

| 来源 | 类型 | 支撑内容 |
|---|---|---|
| [Anthropic Engineering — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 官方工程博客（2026-01） | 能力评测 vs 回归评测、正负任务平衡、outcome 优先于 path、partial credit、参考解、0% pass 常为坏任务信号、transcript 复核、环境隔离 |
| [Anthropic Research — A statistical approach to model evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals) | 官方研究论文/博客（2024-11） | SEM / 95% CI、配对差值分析、power analysis、聚类标准误 |
| [Anthropic Engineering — Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise) | 官方工程博客/实验（2026-02） | 资源与基础设施配置可造成数个百分点评分波动、infra error 单列、A/B 环境一致性 |
| [SWE-bench — evaluation docs](https://github.com/SWE-bench/SWE-bench/blob/main/docs/guides/evaluation.md) | 基准官方文档 | FAIL_TO_PASS / PASS_TO_PASS 二元判分、test patch 判分方法 |
| [GroundEval: A Deterministic Replacement for LLM-as-Judge in Stateful Agent Evaluation](https://huggingface.co/papers/2606.22737) | 论文/预印本 | 用确定性状态检查替代 LLM-as-judge 做有状态 agent 评测 |
| [OpenAI Developers — Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | 官方开发者博客 | Agent Skills 的系统化评测：任务分类、应触发/不应触发、评测自动化 |

### Round 40 可信度说明

- Anthropic 三篇为官方一手来源；SWE-bench 与 GroundEval 为基准/论文来源；OpenAI 博客仅作方法论交叉印证（页面正文未在本轮抓取，引用时注明“官方博客标题/结论级”）。
- 本轮补强只写“可执行检查与反例”，不覆盖已有步骤中的 CLI 用法；若工具/环境版本变化，仍以 `python3 <tool> --help` 为准。
