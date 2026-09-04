# 核心迭代元能力 · Round 1 报告

> 日期：2026-09-04 ｜ 目标：core-iteration 六件套 ｜ 状态：CONTINUE（自动续轮已允许）

## 当前轮次与预期收敛

- **当前第 1 轮**。
- **预期收敛**：还需 **1–2 轮**（边际收益 1.00 很高、剩余高优率 0.35；下一轮后预计进入收益评估点）。
- 本轮 `value-validator` 判定：`CONTINUE`，未触发硬 STOP，`forced_review=false`。

## 收益曲线

| 轮次 | 原始语料 | 高优命中 | 丢弃低质 | 有效新增 | 边际收益 | 累计节点 | 停止原因 |
|---|---|---|---|---|---|---|---|
| 1 | 25 | 23 | 2 | 23 | 1.00 | 23 | 未完 |
| 2（预测） | 12–20 | 9–16 | 2–4 | 5–10 | 0.5–0.8 | 28–33 | 待定 |

## 校验器实测指标（Round 1）

| Skill | 文本变化率 | Token Jaccard | 近似语义位移 | 是否命中 STOP |
|---|---|---|---|---|
| web-research-consensus | 0.186 | 0.785 | 0.215 | 否 |
| benefit-filter | 0.187 | 0.776 | 0.224 | 否 |
| distillation-consensus | 0.221 | 0.709 | 0.291 | 否 |
| value-iterator | 0.111 | 0.819 | 0.181 | 否 |
| value-validator | 0.120 | 0.757 | 0.243 | 否 |
| value-meta-scheduler | 0.123 | 0.810 | 0.190 | 否 |

所有 skill 均超过 `text_change > 0.05`、`semantic_displacement > 0.03`，规则 A/C 未触发；缺口 Jaccard 与边际收益规则也均通过。

## 本轮实际改动

- 六件套 `SKILL.md` 全部升级，新增/修复 23 个知识节点（17 个设计/契约节点 + 6 个干跑验证节点）。
- 新增 `core-iteration/README.md`：六阶段接口契约、版本表、状态文件。
- 新增 `examples/smoke_pipeline.md`：六阶段干跑样例。
- 新增每个 skill 的 `CHANGELOG.md`。
- 新增 `round_ledger.json`：可恢复的调度状态。
- 修复关键 bug：`benefit-filter` 密度评分公式锚点写法导致加权上限仅 34、永远过不了 60 阈值。
- workspace 与 vault 双副本同步；`~/.dsh` 只读，外部同步命令见下文。

## 量化 Skill 能力提升（5 维 20 分）

| Skill | Round0 | Round1 | Delta | 提升 |
|---|---|---|---|---|
| web-research-consensus | 17 | 19 | +2 | +10.0% |
| benefit-filter | 15 | 18 | +3 | +15.0% |
| distillation-consensus | 17 | 20 | +3 | +15.0% |
| value-iterator | 14 | 18 | +4 | +20.0% |
| value-validator | 13 | 18 | +5 | +25.0% |
| value-meta-scheduler | 16 | 19 | +3 | +15.0% |
| **平均/总计** | **15.33** | **18.67** | **+20** | **+16.7%** |

## 效果与上一版相比

- 之前：六个 skill 各自独立，缺少统一的输入/输出契约；`benefit-filter` 评分公式不可达 60；无批量调度、无持久化、无能力量化。
- 现在：六阶段字段全部对齐，`verified_high_remaining_ratio` 可跨模块传递；调度器可以一次跑六个 skill 并记录每轮收益；能力提升可直接用 20 分评分卡看到。

## 丢弃/待验证

- 丢弃 2 条低密度候选（合并成一个大 skill、无预算全网搜）。
- 待验证 0 条。

## 外部同步（~/.dsh 只读，需用户确认后在外部终端执行）

```bash
SKILLS_SRC=$PROJECT_ROOT/vault/skills/core-iteration
SKILLS_DST=~/.dsh/.agent-presets/router-standard/skills
# 如需让这些 skill 在 DSH 中实际可用，把每个子目录复制到预设技能目录
for s in web-research-consensus benefit-filter distillation-consensus value-iterator value-validator value-meta-scheduler; do
  mkdir -p "$SKILLS_DST/$s"
  cp "$SKILLS_SRC/$s/SKILL.md" "$SKILLS_DST/$s/SKILL.md"
done
```

> 注意：运行中 agent 会话不要热更；请按 DSH 运维共识先隔离验证。
