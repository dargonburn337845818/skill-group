# 核心迭代元能力 · Round 3 收敛报告

> 日期：2026-09-04 ｜ 目标：core-iteration 六件套 ｜ 状态：**STOP / yield_exhausted**（已收敛）

## 当前轮次与收敛

- 当前：**第 3 轮**
- 校验器判定：**STOP**
- 停止原因：`yield_exhausted`（规则 D：本轮新增 ≤2，且剩余高优率 <0.10）
- 剩余高优率：0.05
- 预期收敛：**本轮已收敛**，不再自动续轮；如需继续需用户显式 override。

## 收益曲线

| 轮次 | 原始语料 | 高优命中 | 丢弃低质 | 有效新增 | 边际收益 | 累计节点 |
|---|---|---|---|---|---|---|
| 1 | 25 | 23 | 2 | 23 | 1.00 | 23 |
| 2 | 14 | 14 | 0 | 14 | 1.00 | 37 |
| 3 | 2 | 2 | 0 | 2 | 1.00 | 39 |

## 本轮新增

- `examples/backtest_template.md`：真实使用回测模板。
- `tools/smoke_test.py`：一键运行契约校验 + 能力评分汇总。
- 契约校验：**PASS**

## 三轮累计能力提升（自动评分卡）

| Skill | Round0 | Current | Delta |
|---|---|---|---|
| web-research-consensus | 15 | 18 | +3 |
| benefit-filter | 14 | 16 | +2 |
| distillation-consensus | 10 | 16 | +6 |
| value-iterator | 14 | 17 | +3 |
| value-validator | 13 | 16 | +3 |
| value-meta-scheduler | 16 | 19 | +3 |
| **总计/平均** | **82 / 13.67** | **102 / 17.00** | **+20 / +24.4%** |

## 三轮效果对比

- **Round0**：六个 skill 各自独立；benefit-filter 密度公式不可达 60；无输出契约、无来源声明、无自动校验、无能力量化。
- **Round1**：六阶段接口对齐、修复公式、增加调度器批量/评分卡/收敛预测；capability 大幅提升。
- **Round2**：工具化——自动评分卡、契约校验 PASS、SOURCES 补齐、distillation 触发条件补齐。
- **Round3**：回测模板 + 一键冒烟；剩余高价值缺口耗尽，触发收敛。

## 产物清单

- `core-iteration/README.md`
- `core-iteration/REPORT_ROUND{1,2,3}.md`
- `core-iteration/round_ledger.json`
- `core-iteration/CHANGELOG.md`
- `core-iteration/examples/{smoke_pipeline,artifact_examples,backtest_template,dry_run}.md`
- `core-iteration/tools/{scorecard,validate_contract,smoke_test}.py`
- 每个 skill：`SKILL.md`、`CHANGELOG.md`、`SOURCES.md`（内部四个）、`manifest.json`

## 人工接管出口

- 如果用户认为还有未覆盖的重要缺口，可设置 `user_override: "continue"`，下一轮从 Round 4 继续，但需重新过四条硬规则。
- 回测模板是下一轮最可能的入口：按真实任务填表，发现失效点后再次进入信息搜集/过滤。
