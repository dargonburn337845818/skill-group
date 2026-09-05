# Core Iteration Shared Tools

本目录是 `core-iteration` 元能力的共享工具底座，供下列 skill 包按统一入口调用：

- `skill-verification-consensus`
- `dev-workflow-consensus`
- `core-iteration/impl/*`（info-source-adapter、distillation-consensus、value-*、web-research 等）

## 约定

- `$CORE_ITERATION_ROOT` 指向本仓库的 `vault/skills/core-iteration/`（若从源码工作区运行，也可指向 `$HOME/work/skills/core-iteration/`）。
- 示例命令统一写成：
  ```bash
  python3 "$CORE_ITERATION_ROOT/tools/skill_package_check.py" <skill-dir>
  python3 "$CORE_ITERATION_ROOT/tools/scaffold_eval_task.py" --task-id my-task --skill-name my-skill --prompt "..." --checks "contains:..."
  python3 "$CORE_ITERATION_ROOT/tools/info_source_cli.py" --offline github --query demo
  ```
- 各 impl skill 不再在包内复制脚本，避免多份实现漂移。

## 工具索引

| 脚本 | 用途 |
|---|---|
| `validate_contract.py` | 校验六阶段接口契约 |
| `behavior_test.py` | 合成行为冒烟 |
| `scorecard.py` | 5 维能力评分卡 |
| `skill_package_check.py` | Skill 包结构/三件套/来源检查 |
| `distill_skill_package.py` | Nodes → 完整 Skill 包 |
| `scaffold_eval_task.py` | 评测任务包脚手架 |
| `scaffold_dev_spec.py` | 开发规格单 + 路径手册 |
| `info_source_cli.py` | GitHub/OSV/包生态等真实检索 |
| `run_improve_validate.py` | 提升→验证一键循环 |
| `skilljack_runner.py` | 本地 DeepSeek A/B runner |
| `benchflow_runner.py` | 多任务矩阵 + 门禁 |
| `smoke_test.py` | 一键冒烟 |
| `final_evolution_report.py` | 终评报告 |
