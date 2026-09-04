# 训练模式固化状态（Resume Guide）

> 本文件作用是：**随时停止，新会话可无缝继续**。
> 真正持久化的东西：所有 skill、工具、报告、评分器都在本目录与 `.git` 文件中；本文件只是“怎么续”的入口。

## 当前训练状态

- **训练轮次**：Round 30（已固化，override: user）
- **下一轮**：无（按成本边界收敛；剩余高价值项需真实模型评测/插件隔离改造）
- **状态**：已收敛并落盘
- **收敛状态**：CONVERGED（stop_reason=`diminishing_returns`）
- **收敛原因**：基础能力已工具化且补齐低分 Skill 的门禁/干跑/示例；剩余高价值动作（更多 Skill 真实 A/B、插件热改）成本高
- **直观能力分**：87 / 100（A 级，final_evolution_report）
- **当前指标**：
  - scorecard: 204/240（12 个 skill）
  - package_check: PASS，平均 95.4/100
  - 可执行工具：13 个
  - effective_new: 1（Round 30，边际已明显下降）
- **Skill 增强指数**：真实 A/B 已落盘——dev-security 正例/反例任务包（`evals/`），DeepSeek 3 次/格，Skill Lift **23.2%**，门禁 PASS；复现入口 `evals/benchflow.config.yaml`

## Round 22→30 进化冲刺内容

- 新增 `skill-verification-consensus`（检验底座）与 `dev-workflow-consensus`（开发底座）。
- 更新 `distillation-consensus` v0.7.0、`search-source` v0.3.0、`web-research-consensus` v0.3.0、`info-source-adapter` v0.7.0、`value-meta-scheduler` v0.5.0、`value-effect-audit` v0.2.0、`return-forensics` v0.2.0。
- 新增/进化工具：
  - `scorecard.py`：纳入基础 skill 与新增底座
  - `skill_package_check.py`：Skill 包结构/契约/证据自动检查
  - `distill_skill_package.py`：Nodes → 完整可发布 Skill 包
  - `scaffold_eval_task.py`：Skill 评测任务包脚手架（Skill TDD）
  - `scaffold_dev_spec.py`：开发规格单 + 路径手册脚手架
  - `final_evolution_report.py`：直观迭代终评
  - `info_source_cli.py`：新增 `github-file` 适配器
- 详见 `reports/REPORT_ROUND30.md`。

## 已固化的训练模式

### 执行模式：提升 → 验证 循环

```bash
cd $WORKSPACE/skills/core-iteration

# 1) 真实采集 + 六阶段 + 校验
python3 tools/run_improve_validate.py --proxy-mode host

# 2) 生成标准报告（轮次/收益/收敛/直观分；支持 --round 与 --old-nodes）
python3 tools/meta_report.py --input tools/output/info_dump.json --round 22 --old-nodes tools/output/nodes_round20_list.json

# 3) 生成 Skill 草案/完整包
python3 tools/skill_draft_builder.py --input tools/output/info_dump.json
python3 tools/distill_skill_package.py --nodes tools/output/nodes_round22_list.json --id my-skill --description "..."
python3 tools/scaffold_eval_task.py --task-id my-task --skill-name my-skill --prompt "..."
python3 tools/scaffold_dev_spec.py --project /path/to/project --entry src/index.ts --test "npm test"

# 4) 一键全量校验 + 终评
python3 tools/smoke_test.py
python3 tools/final_evolution_report.py .

# 5) 量化 Skill 对模型增强（A/B 模板）
python3 tools/skill_effect_bench.py --input benchmarks/skill_benchmark_template.json
```

### 可选：灵感/市场侦察（按需，不膨胀）

```bash
python3 tools/mine_ideas.py --proxy-mode host --category all
python3 tools/mine_ideas.py --proxy-mode host --category plugin
python3 tools/mine_ideas.py --proxy-mode host --category skill
```

## 新会话如何续训

1. 读取本文件。
2. 读取 `README.md` 的模块地图。
3. 读取 `reports/REPORT_ROUND{22,30}.md` 了解最近两轮。
4. 读取 `round_ledger.json` 了解持久化状态（Round 30 CONVERGED）。
5. 若要继续高价值迭代：
   - 真实 Skill A/B 已实现：`scaffold_eval_task.py` → `skilljack_runner.py`（DeepSeek agent 循环）→ `benchflow_runner.py`（矩阵+门禁）→ `skill_effect_bench.py`；后续可补外部 key 接官方 skilljack-evals CLI；
   - 或做插件侧集成（dsh-skill-router dev 路由）——必须按 `dsh-optimization-consensus` 隔离冒烟；
   - 若只是复核当前结果，不需要重跑。

## 停止/恢复

- 停止：直接结束会话即可；文件已落盘。
- 恢复：新会话按上面步骤继续，不需要重做。
