# 核心迭代元能力 · Round 2 报告

> 日期：2026-09-04 ｜ 目标：core-iteration 六件套 ｜ 状态：CONTINUE，预期 0–1 轮后进入收敛评估

## 当前轮次与预期收敛

- 当前：**第 2 轮**
- 校验器判定：**CONTINUE**，未触发 STOP，`forced_review=false`
- 预期收敛：**0–1 轮**（本轮后预计进入收益评估/人工决定点）
- 剩余高优率：0.20，仍 >0.10

## 收益曲线

| 轮次 | 原始语料 | 高优命中 | 丢弃低质 | 有效新增 | 边际收益 | 累计节点 |
|---|---|---|---|---|---|---|
| 1 | 25 | 23 | 2 | 23 | 1.00 | 23 |
| 2 | 14 | 14 | 0 | 14 | 1.00 | 37 |
| 3（预测） | 6–10 | 4–7 | 1–2 | 2–5 | 0.5–0.8 | 39–42 |

## 本轮新增（14 个节点/工件）

- `tools/scorecard.py`：自动计算 5 维能力评分。
- `tools/validate_contract.py`：自动校验六阶段接口字段，当前 **PASS**。
- `examples/artifact_examples.md`：六阶段产物字段样例。
- `examples/dry_run.md`：共享网络检索干跑样例。
- `distillation-consensus`：补齐 `## 触发条件`。
- 4 个内部 skill 新增 `SOURCES.md` + “来源与可追溯”小节：benefit-filter、value-iterator、value-validator、value-meta-scheduler。
- `core-iteration/README.md`：补充自动化校验命令与工具入口。
- value-iterator 补入 semver 字样，使契约校验可机器检查。

## 自动评分卡（tools/scorecard.py，0–20 分）

| Skill | Round0 | Round2 | Delta |
|---|---|---|---|
| web-research-consensus | 15 | 18 | +3 |
| benefit-filter | 14 | 16 | +2 |
| distillation-consensus | 10 | 16 | +6 |
| value-iterator | 14 | 17 | +3 |
| value-validator | 13 | 16 | +3 |
| value-meta-scheduler | 16 | 19 | +3 |
| **总计/平均** | **82 / 13.67** | **102 / 17.00** | **+20 / +24.4%** |

## 效果与之前相比

- Round1 之前：六个 skill 缺少统一契约、自动校验、来源声明和可复算评分。
- Round1 之后：接口字段对齐，但仍有结构性缺口：distillation 没“触发条件”、多个内部 skill 没 SOURCES、没有自动校验入口。
- Round2 之后：契约校验一键 PASS；能力评分可自动生成；所有内部 skill 都可追溯到来源；distillation 定位完整。工具链从“文档驱动”进入“可校验、可评分”阶段。

## 丢弃

- 1 条：给每个 skill 单独做示例文件（共享 artifact_examples 已覆盖，重复收益低）。

## 下一步

Round3 建议：真实使用回测模板 + 将 scorecard 输出接到 README 自动表；如果新增节点 <3 且剩余高优率 <0.10，则触发 forced_review。
