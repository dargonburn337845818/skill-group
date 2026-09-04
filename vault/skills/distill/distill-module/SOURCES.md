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
