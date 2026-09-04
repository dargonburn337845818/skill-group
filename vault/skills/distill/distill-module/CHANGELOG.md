# Changelog · distill-module

## 0.1.0 · 2026-09-04

- 首次落盘蒸馏模块编排层。
- 新增：
  - `SKILL.md`：GapRequest → 六步编排 → BackfillResult；
  - `feed-other-modules.md`：模块缺口 → 新 skill/专家 → 回填 modules.json；
  - `meta-iteration.md`：复用 core-iteration，不另起炉灶；
  - `real-ab-bench.md`：scaffold_eval_task → skilljack-evals/BenchFlow → Skill Lift 接入方案；
  - `examples/distill_task.md`：模块 skill 与专家蒸馏两个样例；
  - `SOURCES.md`：来源清单。
- 回填 `vault/meta/modules.json` 的 distill.skills/gaps/gapProgress/module。
- 更新本地 `assignments/distill/assignment.json` 状态为 done（内部开发记录）。

## 0.2.0 · 2026-09-04

- 实现真实 A/B runner：
  - 新增 `core-iteration/tools/skilljack_runner.py`（DeepSeek agent 循环、loadSkill、verifier、可选 LLM judge）；
  - 新增 `core-iteration/tools/benchflow_runner.py`（多任务矩阵、Skill Lift、门禁）；
  - `scaffold_eval_task.py` 的 verifier/oracle 模板改为 ESM，兼容 Node 22+；
  - 更新 `real-ab-bench.md` 与 core-iteration 文档，从“待接入”改为“本地真实 runner 已实现”。

## 0.3.0 · 2026-09-04

- 第一份真实 Skill A/B 证据落盘：
  - `core-iteration/evals/dev-security-enforce` 正例 + `dev-security-anti` 反例任务包；
  - DeepSeek `deepseek-chat` 每格 3 次跑通，Skill Lift **23.2%（明显增强）**，门禁 PASS；
  - 设置页 `skill-effect-bench` 状态从“待接入”改为“已接入”；
  - 修复 `skilljack_runner.py` 对相对 `verifier/workspace` 路径的解析（子进程 cwd 切换后仍能执行 verifier）。
