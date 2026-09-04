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
