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

- `$CORE_ITERATION_ROOT/tools/skill_effect_bench.py`：A/B 基准评分（成功率、质量、效率、覆盖、校准）。
- 评分标准参考 OpenAI Agent Skills Evals、Scale Agentic Leaderboard、skilljack-evals。

## 2026 深度补强（Round 40）

> 补强目标：把“真实任务 A/B、多方交叉价值、效果指标与反馈回路”落成可直接执行的检查清单。以下规则在原有“可测结果 / 归因 / 多方交叉 / 效果公式 / 硬性纪律”之上新增，不替代旧规则。

### 1. 真实 A/B 五查：确认你在比较“同一只猫”

- **同任务集**：无 skill 与有 skill 必须跑同一批 `task_id`；任务集先冻结为 `taskset_hash`，skill 内容不得出现在评分答案里（防泄漏）。
- **同环境**：仅切换 skill，其余（模型、温度、工具、系统提示、缓存、时间窗、评测标准）保持一致；任何一项变化都要记录为 `environment_diff`，并降级该轮证据。
- **盲评**：评分者不知道哪条是 skill 版；先导出无标签结果，再统一评分；人评与 LLM-judge 分开记录 `rater_id`。
- **基线先固定**：先跑无 skill 基线并落盘，再改 skill；禁止“边改边比”或把历史成绩/别的任务当基线。
- **顺序/疲劳**：任务顺序随机或轮换；多次运行间设最小间隔，避免缓存、记忆和评分漂移。

反例：拿上周模型版本的历史成绩当基线；只展示成功案例；同一评测者看着标签打分；一次改动同时改系统提示、skill 和评分标准，却把整体提升归到 skill。

### 2. 多方交叉：用“价值轴 × 独立评分方 × 复现”代替“转载数量”

- 每个候选节点先填三维矩阵：①价值轴（成功率、质量、效率、覆盖、校准、失败/副作用/恢复成本）；②独立评分方（真人专家、目标用户、自动化规则、LLM-judge——至少两类，且彼此不共享同一偏见源）；③复现（不同任务族、不同模型、不同时间点或不同实现路径）。
- 同一节点只有“多个来源 URL”不算多方；必须能说出这多方在价值轴和评分方上确实独立。跨来源去重按 DOI/URL/作者/机制判定，转贴与同机构通稿只算 1 方。
- 评分分歧处理：记录 `inter_rater_agreement`（一致率/kappa 或分歧样本），分歧大 → `effect_confidence` 降级；不要只输出平均分。LLM-judge 与人类一致要作为“被验证过的证据”，不是默认事实。
- 反例：三篇博客/同一新闻转载算三份证据；两个 LLM-judge 都高分但都偏好长答案/格式漂亮；只看平均分不看每个价值轴的负面项。

### 3. 效果指标：OEC + 护栏 + 意外记录，先定义后跑

- 每个 A/B 先写：**主指标 OEC**（总体评估准则，如“任务成功率”或“任务质量分”）、**2–3 个护栏**（成本、延迟、拒绝率、安全/越权、可恢复性）、**1 个意外观察字段**。
- 报告必须包含：`n_control / n_treatment`、双均值、`lift`、置信区间/显著性（或贝叶斯后验）、实际最小可接受提升；样本过小或区间跨 0 时只能 `needs_more_evidence`。
- 防挑指标：所有指标在跑之前写入模板；跑完后不得只报最漂亮指标；主指标提升但任一护栏显著变差 → 建议 `demote` 或 `needs_more_evidence`，并记录 tradeoff。
- 反例：3 个任务报“提升 30%”；只报成功率不报成本翻倍；从 10 个指标里挑最好的一个写进报告；把统计显著当实际显著（提升 0.1% 不值得 promote）。

### 4. 节点级 ablation：promote 前必须证明“去掉它会回退”

- 对每个候选 promote 节点跑三条：①无 skill 基线；②含该节点；③去掉该节点（其余节点不变）。若③与①无显著差异，则该节点标 `correlated`（伴随现象），不得 `promote`。
- 一次改多个节点时，先按节点分组 ablation；整体提升不得直接摊派给单个节点。
- 效果变化先做 forensics：检查模型版本、任务集、时间、缓存、评分者、环境是否漂移；受控后的变化才进 `effect_score`。变差不直接删除，先查场景适配。
- 反例：同时加 5 条规则后整体变好，就报其中 3 条 promote；任务变好但模型也升级了；删掉节点后不回测就说“它没用了”。

### 5. 反馈回路：版本化、定时复测、防指标博弈

- 每个 `effect_report` 落盘必须携带 `skill_version`、`prompt_hash`、`model_id`、`taskset_hash`、`date`、`baseline_id`；任何 promote/demote 都要能回溯。
- 每个 promote 建“复测卡片”：触发条件（taskset 更新、模型换代、来源变化、用户反馈异常）、复测内容（原 A/B + 至少 1 个负面/边界任务）、预置动作（先查漂移 → 再 ablation → 再降权，不直接删除）。
- **Goodhart/Campbell 检查**：promote 后若指标在涨但真实行为/用户确认/副作用没有同步改善，说明指标可能被博弈或不是价值本身；此时先质疑指标定义，而不是继续优化该指标。
- 反例：一次成功永久 promote；改版后不重跑 negative cases；只监控提升不监控回归；等到用户投诉才发现效果已衰减。

## 来源

- 本地 `benefit-filter`、`value-iterator`、`value-validator`
- 外部参考：OpenAI Agent Skills Evals、Convergence Protocol
