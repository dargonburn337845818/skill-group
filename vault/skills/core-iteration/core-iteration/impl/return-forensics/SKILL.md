---
name: return-forensics
description: 收益下降根因分析器——当边际收益下降、强制评估或意外 STOP 时，从语料、过滤、蒸馏、接口、效果、范围六个维度定位真正原因，并给出可执行的下一步；同时把每个知识节点的“来源→验证→蒸馏→应用→效果”串成可追溯思维链。
whenToUse: 调度器收益曲线下滑、连续两轮收益 <3、出现 forced_review，或用户觉得“迭代没进展但不知道卡在哪”时。
---

# 收益下降根因分析（Return Forensics）

> 定位：`value-validator` 只说“该停了”，本 skill 回答“为什么停、卡在哪、下一步该做什么”。它是收益曲线的“病理科”。

## 触发条件

- 边际收益连续两轮下降或 <3。
- `forced_review=true`。
- 决策器 STOP 但用户/调度员怀疑不是真收敛。
- 有效新增少，但 `verified_high` 不少（说明不是没料，而是没转化好）。

## 输入约定

```text
input = {
  yield_curve: [ round_stats ... ],
  gap_list_prev,
  gap_list_curr,
  verified_high_remaining_ratio,
  discarded_ratio,
  effective_new_nodes_per_round,
  node_effects?: [ value-effect-audit 输出 ],
  source_scope_report?: [ info-source-adapter 输出 ],
  stop_reason?
}
```

## 诊断矩阵

| 症状 | 可能根因 | 证据 | 下一步 |
|---|---|---|---|
| 新缺口很少，Jaccard 高 | `corpus_exhaustion` | gap_list 连续两轮高度重合 | 换信息范围/换生态/换问题角度 |
| 丢弃率高，pending 多 | `filter_over_tight` | discarded/raw >80% 且单源存疑多 | 复核阈值、人工提升、降低 single-doubt 门槛 |
| 高优不少但有效新增少 | `distillation_loss` | verified_high_count 高、effective_new_nodes 低 | 检查 Node 三件套/可执行性，重蒸馏 |
| 来源类型单一 | `source_saturation` | source_scope_report 只有 github/博客 | 增加 package/academic/independent ecosystem |
| 输出契约字段丢失 | `interface_mismatch` | validate_contract FAIL 或字段改名 | 修契约/修调用顺序 |
| 旧节点与新任务不匹配 | `scope_drift` | 本轮新增节点与目标主题相关度下降 | 重定义目标，冻结旧分支 |
| 只有文字变化 | `no_real_delta` | validator 规则 A/C 命中 | 停止并回退，不做粉饰迭代 |
| 效果变差 | `negative_effect` | value-effect-audit 出现 demote/delete | 优先降权/删除，再谈增量 |

## 处理流程

1. 先看**总量**：是“没有新料”还是“有料没变成有效节点”。
2. 再看**分布**：是哪一类来源/哪一个 skill 环节损失最多。
3. 然后看**效果**：是否有真实任务证明新增节点真的有用；没有效果的“新增”只是论文式增加。
4. 最后给结论：**root_cause + evidence + one_action**；不要把多个原因揉成一句话。

## 思维链输出（Trace Chain）

每个知识节点都应能回答“这条知识怎么来的、凭什么信、用在哪、效果如何”：

```text
trace_chain = [
  {
    node_id,
    source_refs: [ ... ],
    origin: "raw_corpus chunk -> verified -> primitive -> node",
    transform_notes: "为什么这样合并/拆分",
    application_ref: "真实任务/回测 id",
    effect_ref: "value-effect-audit node_effects 条目",
    boundary: "失效场景"
  }
]
```

产出 `trace_graph.json` 时按 `node_id` 聚合，不做单向隐藏；冲突、降权、删除也要保留在链上，方便审计“为什么最后没采用”。

## 输出契约

```text
{
  "diagnosis": {
    "root_cause": "distillation_loss" | "source_saturation" | ...,
    "confidence": "high" | "medium" | "low",
    "evidence": [ "具体指标/字段" ],
    "one_action": "一句话下一步"
  },
  "yield_diagnosis": { "stage_loss": { "gather": x, "filter": y, "distill": z, "apply": w } },
  "trace_chains": [ ... ],
  "recommendation": "继续/停止/换范围/重蒸馏/修接口/调阈值"
}
```

## 干跑验证（对接 core-iteration）

1. 用一次真实 `effective_new=0` 的轮次跑根因分析，确认输出 `root_cause` 与 `one_action`。
2. 回放 `trace_chains`，确认降权/删除节点仍留在链上。
3. 将诊断结果交给 `value-meta-scheduler` 收口；用 `skill_package_check.py` 检查本包。
4. 干跑样例见 `examples/dry_run.md`。

## 硬性纪律
2. **用证据区分“没料”和“没转化”**：只看 effective_new_nodes 会误判。
3. **保留所有分支**：降权/删除的节点也要留在 trace_chain 里，不能用删除了事。
4. **效果优先**：当真实效果与静态评分冲突时，以 `value-effect-audit` 为准。
5. **一次只改一个环节**：修复根因后重跑一轮，观察收益是否恢复，再决定是否继续。

## 简单用户话术

> 收益下降时我不会只说“该停了”，我会先查是“没找到新东西”“找到了但没用好”“用起来没用”还是“方向变了”。然后给你一个明确的原因和一个下一步动作，并把每条知识从来源到效果的完整链条留下来。

## 来源

- 本地 `value-meta-scheduler`、`value-validator`、`value-effect-audit`、`info-source-adapter`
- 外部参考：Convergence Detection、Convergence Protocol
