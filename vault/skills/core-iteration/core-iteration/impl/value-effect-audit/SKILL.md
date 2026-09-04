---
name: value-effect-audit
description: 实际效果审计器——把 Skill/知识节点投入真实任务后测量“是否真的改变了行为”，用多方交叉证据计算信息价值，并把效果反馈回迭代器与过滤器；用于解决“知道很多但不知道哪条真的有用”的问题。
whenToUse: 需要验证某个 Skill/节点在真实任务中的实际收益；需要判断哪些知识该保留、哪些该降权；需要把“静态密度评分”升级为“实际效果打分”时。
---

# 实际效果审计器（Value Effect Audit）

> 定位：`benefit-filter` 算的是“这条信息看起来值多少”，本 skill 算的是“这条信息用起来真的值多少”。它是把收益曲线从“预估”变成“实测”的反馈回路。

## 触发条件

- 某个 Skill 版本投入真实任务后，需要回测效果。
- 多轮迭代中收益下降，需要区分“知识没用”和“只是没找到好证据”。
- 用户/专家/测试给出了真实反馈，需要把反馈量化并归因到具体节点。
- 调度器需要决定：继续补源、降权、删除，还是保持。

## 输入约定

```text
input = {
  skill: { id, version, knowledge_nodes, source_refs },
  real_tasks: [
    {
      task_id,
      scenario: "真实任务描述",
      expected_outcome,
      actual_outcome,
      observations: [ "执行成功/失败、偏差、时间、用户反应" ],
      used_nodes: [ node_id ]
    }
  ],
  multi_source_evidence: {
    node_id: [ source_ref, ... ]
  },
  feedback?: [ { type, content, priority } ]
}
```

## 处理流程

1. **定义可测结果**：每个任务写清楚 `expected_outcome` 与 `actual_outcome`；优先用可计数指标（成功率、耗时、错误率、返工次数、用户确认）。
2. **归因到节点**：把结果变化映射到实际使用过的 `used_nodes`；没有使用过的节点不计入本轮效果。
3. **多方交叉计算**：
   - 同一节点在多个独立任务/来源中都有正向效果 → `effect_confidence` 提高。
   - 只有单一任务有效 → `effect_score` 降权，标 `single-effect`。
   - 不同任务效果冲突 → 保留冲突分支，不平均；记录适用边界。
4. **计算信息价值**：
   ```text
   effect_score = 0.6 * outcome_gain + 0.4 * consistency
   outcome_gain  = normalized(actual - expected)
   consistency   = 正向任务数 / 总任务数
   node_info_value = effect_score * source_confidence * 是否通过 deleted-test
   ```
5. **反馈回路**：
   - `value-effect-audit` 输出建议：`promote`（提升权重）、`demote`（降权/移入注脚）、`delete`（删除）、`needs_more_evidence`（补源）。
   - `value-iterator` 依据这些建议更新 `weight` 与 `provenance`；`benefit-filter` 依据历史效果调整密度评分阈值/依据。
   - 任何 `promote` 都必须附带真实任务证据；没有效果证据的“我觉得有用”不能升级。

## 输出契约

```text
{
  "effect_report": {
    "task_count": n,
    "positive_count": n,
    "conflict_count": n,
    "overall_effect_score": 0.00
  },
  "node_effects": [
    {
      node_id,
      effect_score: 0.00,
      outcome_gain: 0.00,
      consistency: 0.00,
      effect_confidence: "high" | "medium" | "low",
      multi_source: [source_ref...],
      suggestion: "promote" | "demote" | "delete" | "needs_more_evidence",
      boundary: "什么场景下有效/失效"
    }
  ],
  "feedback_to_iterator": {
    "weight_adjustments": { node_id: old_weight -> new_weight },
    "demote_list": [node_id],
    "delete_list": [node_id],
    "needs_evidence": [node_id]
  }
}
```

## 干跑验证（对接 core-iteration）

1. 用 `scaffold_eval_task.py` 建 1 个任务包，跑无 skill/有 skill 基线（至少 3 次）记录原始数。
2. 把结果映射到节点 effect：promote / demote / delete / needs_evidence。
3. 若只有模板分数，不得标 `effect_confidence=high`；诚实写“待真实 A/B”。
4. 用 `skill_package_check.py` 检查本包，确认契约无问题。

## 硬性纪律
2. **相关性≠因果**：任务结果可能受混杂因素影响；至少说明“为什么归因到这个节点”，必要时做对照。
3. **冲突不平均**：不同场景效果相反时保留分支，记录适用边界。
4. **小样本要降级**：样本 <3 时，`effect_confidence` 不得为 high。
5. **反馈必须可追溯**：每条 effect 都要能回到 task_id / node_id / source_ref。

## 边界 / 反模式

| 情况 | 处理 |
|---|---|
| 一次成功就说“这条规则有效” | 样本太小，只能标 `single-effect` 并继续观察 |
| 任务成功但没用到该节点 | 不计入该节点的效果 |
| 两个来源都有效但机制不同 | 保留两条分支，分别记录边界 |
| 把用户“感觉不错”当效果 | 只作为弱信号，需要可计数结果 |
| 效果变差就立刻删节点 | 先做 forensics：可能是场景不适配，不是节点无用 |

## 简单用户话术

> 我不只看这条信息“听起来值多少”，还会看它放进真实任务后有没有真的改变结果。我会按任务成功率和多方证据给每条知识打分，然后把“确实有用”的提升权重、“只在特定场景有效的”标清边界、“没用的”降权或删除。

## 配套执行工具

- `tools/skill_effect_bench.py`：A/B 基准评分（成功率、质量、效率、覆盖、校准）。
- 评分标准参考 OpenAI Agent Skills Evals、Scale Agentic Leaderboard、skilljack-evals。

## 来源

- 本地 `benefit-filter`、`value-iterator`、`value-validator`
- 外部参考：OpenAI Agent Skills Evals、Convergence Protocol
