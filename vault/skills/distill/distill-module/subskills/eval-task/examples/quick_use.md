# Quick Use：distill-eval-task

> 一句话：蒸馏子技能：把 scaffold_eval_task / skilljack_runner / benchflow_runner 变成可照着做的操作手册；产出任务包、真实 A/B 对照、anti-trigger 与 Skill Lift 解读。

## 何时用

- 当任务命中 `SKILL.md` 的“触发条件 / 何时使用”时。

## 最小可复现动作

- 用户要给一个新蒸馏的 Skill 生成 `skilljack-evals` 风格评测任务包。
- 需要判断 Skill 是否真的有用：跑无 skill 基线 vs 有 skill，计算 Skill Lift。
- 需要防止 Skill 在无关任务上误触发（anti-trigger）。
- 需要把评测结果回填进 Skill 的 `CHANGELOG` / `benchmarks` / `qualityCriteria`。

## 验证方式

- 按 `SKILL.md` 的干跑/检查清单执行；
- 发布/更新前跑 `skill_package_check.py` 与本 skill 对应校验。
