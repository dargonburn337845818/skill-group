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

## 2026 深度补强（Round 40）

> 目标：把六类根因从“看表猜”升级为“可证伪探针 + 可复现 trace_chain”。以下规则在原有诊断矩阵之上新增，不替代旧规则。

### 1. 根因判别探针：先做单变量扰动，再下结论

- `corpus_exhaustion`：换一个新生态入口（package / academic / independent ecosystem），沿用同一条蒸馏路径；若 `effective_new` 仍不升，才确认语料枯竭；若升高，则是来源饱和或范围问题，不是语料枯竭。
- `filter_over_tight`：随机抽取 10% 的 `single-doubt` 样本，放宽一个阈值（如 0.8 → 0.6）跑一轮；若 `verified_high` 和最终有效节点同步上升，说明过滤过紧；若只增加垃圾，说明过滤是合适的。
- `distillation_loss`：手工重蒸馏 10 个高优 raw 节点；若有效转化率显著低于基线，说明损失在蒸馏，不在语料。
- `interface_mismatch`：不猜，直接回放 `validate_contract`、旧 schema、调用顺序；FAIL 即接口问题，与数据量无关。
- `negative_effect`：对新增节点做反事实删除（ablation）；若目标任务表现恢复或不变，该节点没有正效果。
- `scope_drift`：用冻结的基准任务集对比新旧节点覆盖率；若旧目标覆盖率下降且任务集在扩大，才判范围漂移。

反例：不做扰动就同时加语料、调阈值、重蒸馏、改接口——收益恢复也无法归因到某个根因。

### 2. 过滤与蒸馏的分流检查：别把“没转化”全算到语料头上

- 过滤侧看“被丢弃的到底是不是低质”：用目标对齐的过滤（target-aligned filtering）而非通用质量分；统计被丢弃项中“单源待证/无旁证”的占比。若丢弃主因是来源单一，不是质量差，则不要只压过滤阈值。
- 蒸馏侧看“是否在自我回收”：若新节点与已有节点语义相似度持续升高、表述越来越同质，更可能是蒸馏模板在吃自己的产出，而不是外部语料枯竭。
- 反例：只加新语料、不换蒸馏视角、不去重、不补负例——等于给循环继续喂同一个模板，火不会变旺。

### 3. trace_chain 可复现审计（PROV 对齐）

- 每个节点至少包含：`source_refs`（URL + 版本/日期 + chunk_id）、`transform_params`（prompt/版本/设置）、`application_ref`（真实任务 id）、`effect_ref`（effect-audit id）、`boundary`（失效场景）、`status`（kept / deprioritized / invalidated）。
- 复现检查：从一个 raw chunk + 同一参数能否重建该节点？不能 → 标 `non-reproducible` 并降权。
- 删除/降权用 `wasInvalidatedBy` 事件保留，不做物理删除；冲突保留双分支，不自动合并。
- 审计清单：node_id → 至少一条 raw source；transform_params 可版本化；application_ref 有真实任务；effect_ref 有效果记录；boundary 非空；status 非空。

反例：只存“来源链接”，不存 chunk、版本、蒸馏参数和失败分支——两轮以后无法回答“这条从哪来、为何没采用”。

### 4. 效果证据三层阶梯 + 反事实验证

- L1 静态评分（模型/人觉得有用）→ L2 单任务通过率 → L3 真实目标任务增量（删节点后任务失败或得分下降）。
- 只有 L3 计入 `effective_new`；L1/L2 只能作为候选，不能直接算收益。
- 新增节点时跑一次快速反事实：移除该节点 → 目标任务通过率变化。若变化约等于 0，标记 `paper_increase`，不计入收益。
- 反例：把“模型说这个节点更完整/更专业”当作效果；在真实任务回测中它可能只是装饰性增长。

### 5. 诊断自身的可复现与退出条件

- 每次诊断输出：`diagnosis_evidence`（指标快照）、`probe_ran`（跑了哪个扰动）、`conclusion_boundary`（该根因在什么条件下不适用）、`repro_steps`。
- 证据不足时输出 `insufficient_evidence`，不硬给单一 root_cause；给出两个候选 + 下一轮探针。
- 每轮落盘一份 forensics record：yield_curve、discarded 日志、contract 日志、trace_graph 哈希；后续轮次可对比、可审计、可申诉。
- 反例：只给一句“语料枯竭”，没有指标快照、没有探针、没有失效边界——后续无法验证，也无法区分“真结论”和“随口归因”。

### 6. 误诊反例清单（主动避开）

- 同源转载重复计数当“新语料”——先用源族归一化去重。
- 上一轮有效新增少就立刻 STOP，而不是先跑探针区分“没料 / 没转化 / 没用”。
- 一次改多个环节（过滤 + 蒸馏 + 接口），再宣称找到了根因。
- 把 self-refine 的“输出更被偏好”直接当迭代有效——已有证据表明 self-correction 可能无改善甚至变差。
- 只记录成功节点，删掉被降权/删除节点，破坏 trace_chain 审计链。
- 同一轮同时换目标、换评价集，却与旧轮收益曲线直接比较——范围漂移与评价漂移双重混淆。

## 来源

- 本地 `value-meta-scheduler`、`value-validator`、`value-effect-audit`、`info-source-adapter`
- 外部参考：Convergence Detection、Convergence Protocol
