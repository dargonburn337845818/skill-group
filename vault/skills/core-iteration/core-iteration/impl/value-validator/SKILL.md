---
name: value-validator
description: 动态校验决策器——用语义位移、缺口重合度、编辑距离、边际收益四条硬规则判断是否继续迭代，输出 STOP/CONTINUE 与收益摘要。用于价值驱动递归提升模块的每轮收敛判定。
whenToUse: - 每轮迭代器输出新 Skill 后。
---
# 校验决策器（Value Validator）

> 定位：校验器是“止损器”。它不判断新 Skill 好不好，只判断“继续迭代是否还有可量化的认知增量”。任何一条硬规则触发即 STOP，防止低价值空转。

## 触发条件

- 每轮迭代器输出新 Skill 后。
- 调度器需要决定“进入下一轮还是收敛”。
- 用户需要一份本轮收益摘要与停止原因。

## 输入约定

```text
input = {
  round,
  old_skill: { text, knowledge_nodes, embeddings? },
  new_skill: { text, knowledge_nodes, embeddings? },
  gap_list_prev: [ "缺口A", "缺口B", ... ],   # 上一轮知识缺口清单
  gap_list_curr: [ "缺口A", "缺口C", ... ],   # 本轮知识缺口清单
  round_stats: {
    high_quality_hits,        # 命中【已验证-高优】语料数
    discarded_low_quality,    # 丢弃低质语料数
    effective_new_nodes,      # 本轮新增有效节点数
    new_nodes_from_doubt,     # 本轮来自单源-存疑的新增脚注数
    verified_high_remaining,  # 剩余缺口清单中【已验证-高优】来源占比
    corpus_processed,
    cumulative_nodes
  },
  previous_round_effective_new_nodes?   # 用于连续两轮收益监控
}
```

## 四条硬规则（满足任一条 → STOP）

### 规则 A：语义位移判据

```text
semantic_displacement = mean(embedding_distance(old_skill_chunks, new_skill_chunks))
if semantic_displacement < 0.03:
    → STOP
```

- 用同一 embedding 模型对旧、新 Skill 的正文分段向量化；取逐段最近邻距离的平均。
- 若旧版本身为空，跳过本规则。
- 位移过小说明“改了个寂寞”，没有产生实质认知变化。

### 规则 B：缺口重合度判据

```text
jaccard = |gap_list_prev ∩ gap_list_curr| / |gap_list_prev ∪ gap_list_curr|
if jaccard > 0.90:
    → STOP
```

- 连续两轮“知识缺口清单”高度重合，说明搜索没有打开新缺口，继续迭代只会原地打转。
- 集合元素需先做归一化：同义词、近似表达合并为一个缺口 id。

### 规则 C：编辑步长判据

```text
edit_distance_ratio = Levenshtein(new_skill.text, old_skill.text) / max(len(old_skill.text), len(new_skill.text))
if edit_distance_ratio < 0.05:
    → STOP
```

- 编辑距离占全文比例过低，说明新版相比旧版几乎没有结构变化。
- 该规则与规则 A 可同时触发；任一触发即 STOP。

### 规则 D：边际收益判据（新增）

```text
if effective_new_nodes <= 2 and verified_high_remaining_ratio < 0.10:
    → STOP
```

- `verified_high_remaining_ratio` = 剩余未处理的高优语料 / 剩余缺口总数；
- 当本轮只新增 ≤2 个节点，且剩余缺口里高优来源已不足 10%，说明“矿脉接近枯竭”，继续迭代预期收益很低。

## 计算降级（无 embedding / 空旧版）

硬规则需要数值，但环境不一定有 embedding 模型：

1. **无 embedding**：用“分词 token 集合 Jaccard”代替语义位移：`semantic_displacement ≈ 1 - token_jaccard(old, new)`；仍用同一阈值 0.03 判断。
2. **旧版为空**：跳过规则 A 和规则 C（没有旧文本可比较），规则 B/D 照常执行。
3. **新版为空**：视为无效迭代，直接 STOP，不进入后续规则。
4. **文本极短（<200 字符）**：编辑距离比可能失真，先合并“句子级”再算，并在 `triggered_rules` 注明 `fallback-used`。

## 阈值校准

阈值不是不可调的“真理”，但不能随意放宽：

- 每 3 轮回看一次：若 `forced_review` 连续触发但没有硬 STOP，说明阈值可能过严；若连续被规则 A/C 误 STOP，说明阈值可能过松。
- 调整必须先记录：`old_threshold, new_threshold, rationale, affected_rounds`。
- 单轮内禁止为“想继续”而临时调阈值；要调就作为下一轮的配置变更，并交给用户/调度器确认。

## 强制收益评估（非自动 STOP，但必须上报）

除四条硬规则外，还必须执行顶层“边际收益监控”：

```text
if 连续两轮 effective_new_nodes < 3:
    → 输出 forced_review = true
    → 不自动 STOP，但必须把收益曲线交给调度器/用户，由人决定提前终止还是继续
```

- 该信号不是第五条自动 STOP 规则；它是“人类接管提示”。
- 若同时触发任一硬规则，则 STOP 优先。

## 输出格式

```text
{
  "decision": "STOP" | "CONTINUE",
  "triggered_rules": ["A: semantic_displacement=0.021", "D: ..."],
  "benefit_summary": {
    "hit_high_quality_count": n,
    "discarded_low_quality_count": n,
    "effective_new_nodes": n,
    "new_nodes_from_doubt": n,
    "verified_high_remaining_ratio": 0.xx,
    "cumulative_nodes": n
  },
  "forced_review": true | false,
  "reason": "一句话说明为什么 STOP/CONTINUE",
  "suggested_next_action": "外部补源" | "人工复核" | "继续下一轮" | "收敛"
}
```

## STOP 原因映射（给调度器）

| 触发 | 输出 `stop_reason` |
|---|---|
| 规则 A：语义位移 < 0.03 | `semantic_static` |
| 规则 B：缺口 Jaccard > 0.90 | `gap_static` |
| 规则 C：编辑距离比 < 0.05 | `text_static` |
| 规则 D：新增 ≤2 且剩余高优率 <0.10 | `yield_exhausted` |
| 强制收益评估 | `forced_review`（不自动 STOP） |

调度器使用这些稳定 ID 组装 `convergence_report.stop_reason`，不要用自由文本。

## 2026 深度补强（Round 40）

> 本轮方向：把校验器从“单轮新旧对比”升级为“轨迹记忆 + 回声检测 + 脆弱带复查 + 指标交叉诊断 + 成本归一化”。以下信号不替代原四条硬规则；它们负责把单轮噪声变成可追溯的收敛证据，并为 `forced_review` 提供更细的触发理由。新增来源见 `SOURCES.md`「Round 40 新增来源」。

### R40-1 轨迹级信号：固定点与震荡（trajectory_state）

- **触发**：回合数 ≥3，且本次判定前已有连续 3 轮的旧/新版本位移记录。
- **动作**：维护 `semantic_trajectory = [d_01, d_12, d_23, ...]`（相邻两轮语义位移），并计算相邻位移向量的方向余弦：
  - `fixed_point`：最近 3 轮位移都低于原规则 A 阈值，且方向基本稳定（相邻方向余弦 >0.9）→ 标记 `trajectory_fixed_point`；若原硬规则同时触发，`stop_reason` 追加 `trajectory_static`；若单独出现，输出 `forced_review=true` 交用户判断。
  - `oscillating`：位移幅度不大但方向每轮大幅旋转（相邻方向余弦 <0.3，连续 2 轮）→ 标记 `trajectory_oscillating`，`forced_review=true`；这是围绕旧版本打转，不是“仍在进步”。
  - `progressing`：仅此状态不触发任何门禁。
- **边界**：旧版为空或不足 3 轮时跳过；轨迹必须使用同一 embedding 模型，降级时用 token Jaccard 序列并写 `fallback-used`。
- 来源：S2、S3。

### R40-2 来源新鲜度 / 同源回声（source_echo / isolation probe）

- **触发**：本轮有 `high_quality_hits`，且 `verified_high_remaining_ratio` 尚未枯竭。
- **动作**：对每条高优命中记录 `source_family_id`（同作者/同站点/同数据库/同论文族合并为一个 family）：
  - 若 `source_family_overlap > 0.85`（本轮来自上一轮已出现 family 的高优占比），且本轮没有打开新缺口 → 标记 `source_echo`，`forced_review=true`，并在 `benefit_summary` 单列 `echo_hits`，不得把这些命中描述为“新知识”。
  - 若需要区分“真收敛”与“共享导致的趋同”，做一次隔离探针：让迭代器在不看旧 Skill 的情况下产出一个候选版本，再与旧 Skill 算语义位移。隔离版同样落入停滞半径 → 收敛证据更强；隔离版打开新缺口 → 说明前几轮是同源/同稿造成的假收敛，应切换来源并恢复 CONTINUE。
- **边界**：缺 `source_family_id` 时跳过并写 `source_echo_skipped`；同一上游的多个 URL 只算一个 family，与 `info-source-adapter` 的独立性检查一致。
- 来源：S4。

### R40-3 非单调低产与近边界复查（nonmonotonic_dip / near_boundary）

- **触发**：每次输出 CONTINUE 前，或单轮收益突降时。
- **动作**：
  - 若本轮 `effective_new_nodes <= 1` 但上一轮 ≥3，且剩余高优比例仍 ≥0.10 → 标记 `nonmonotonic_dip`，`forced_review=true`，不自动 STOP；下一轮恢复则回 CONTINUE，连续两轮低产再升级为收敛/停止讨论。
  - 若所有指标都“刚好过线”（例如语义位移 0.031、编辑距离比 0.055、有效新增 3 个）→ 标记 `near_boundary=true`；连续两轮 `near_boundary` → `forced_review=true`，防止“凑合过线”的假 CONTINUE。
- **边界**：任一项原硬规则已触发时，STOP 优先，不因“非单调”而豁免；`near_boundary` 只是脆弱信号，不能推翻硬 STOP。
- 来源：S5、S6。

### R40-4 编辑-语义交叉核验（metric_conflict）

- **触发**：规则 A 与规则 C 都计算完成后。
- **动作**：
  - A 判“语义在动”而 C 判“文本没变” → `metric_conflict = edit_semantic_reverse`；这是小改动高杠杆信号，CONTINUE 但必须 `suggested_next_action = "人工复核单点改动"`，并在输出中注明改动位置；不要只看其中一条。
  - A 判“语义没动”而 C 判“文本大改” → `metric_conflict = cosmetic_rewrite`；本轮收益记 `cosmetic` 或 `0`，不得计入有效新增。
  - 同一冲突类型连续 2 轮 → `forced_review=true`，并检查 embedding 模型/切分方式是否失义（例如文本过短、分段粒度不合理）。
- **边界**：冲突本身不是 STOP 条件；它必须出现在输出 `diagnostics` 中（新增可选字段：`diagnostics: { trajectory_state, source_echo, nonmonotonic_dip, near_boundary, metric_conflict, yield_trend }`）。
- 来源：S7。

### R40-5 成本归一化与增量衰减（yield_density / yield_plateau）

- **触发**：已有 ≥2 轮且 `corpus_processed` 有值。
- **动作**：
  - 算 `yield_density = effective_new_nodes / max(1, corpus_processed)`，并记 `marginal_yield = new_nodes_t - new_nodes_{t-1}`。
  - 若 `yield_density` 连续两轮下降且 `marginal_yield <= 0` → `forced_review=true`，在收益摘要给 `yield_trend`；不要把“累计节点还在涨”当成收益还在涨。
  - 有 ≥4 轮时拟合指数衰减 `yield_t ≈ c + a·e^{-λt}`；若估计未来两轮新增 <0.5 节点（或已到平台期），输出 `yield_plateau=true` 并 `forced_review=true`；只有同时命中原规则 D 才自动 STOP。
- **边界**：语料规模不稳定时不要直接比绝对密度，要与同源同规模轮次对比；缺 `corpus_processed` 时跳过并写 `yield_density_skipped`。
- 来源：S1、S2、S5。

### Round 40 检查清单

1. 已有三条以上轮次时，是否算过 `semantic_trajectory` 并输出 `trajectory_state`？
2. 本轮高优来源是否按 `source_family_id` 去重？是否算过 `source_family_overlap`？
3. 单轮低产前一轮是否高产？是否标记了 `nonmonotonic_dip`？
4. 所有“刚好过线”的指标是否都标了 `near_boundary`？
5. A/C 是否做过交叉核验？`metric_conflict` 是否落盘？
6. `yield_density` 与 `marginal_yield` 是否出现？累计节点有没有被误当作收益？
7. 原四条硬规则是否仍是最终 STOP 裁决者？新增信号有没有把它们软绕过？

### Round 40 反例速查

| 反例 | 判定 |
|---|---|
| 只看新旧两版位移，不知道上一轮也在原地 | 漏掉 `trajectory_fixed_point`；必须看轨迹 |
| 新增节点来自同一批作者/站点，却包装成“多源新增” | 判 `source_echo`，不计新知识 |
| 一轮低产就 STOP，下一轮本可恢复 | 违反非单调守卫；至少看连续两轮/`forced_review` |
| 语义判动、编辑判没动，直接忽略 | 必须报 `metric_conflict`，可能漏掉高风险单点改动 |
| 累计节点从 5 涨到 50 就说“还在增长” | 边际收益曲线才是收益；累计不是 |
| 阈值刚好过线就当 CONTINUE 稳了 | 标 `near_boundary`，连续两轮脆弱过线要上报 |
| 用新增信号替代原四条硬规则 | 不允许；新增信号只做诊断/强制评估，不撤销硬 STOP |

## 来源与可追溯

- 完整来源声明见本目录 `SOURCES.md`。
- 设计来源：用户规格《认知收益架构 / 价值驱动递归提升模块》；输入来自 `benefit-filter` 的 `yield_stats` 与 `value-iterator` 的新旧版本。
- 外部参考：[Convergence Protocol](https://inferensys.com/glossary/recursive-error-correction/iterative-refinement-protocols/convergence-protocol)、[Convergence Detection](https://github.com/agentpatterns-ai/website/blob/main/loop-engineering/convergence-detection.md)、[SemHash-LLM](https://arxiv.org/html/2607.01601)。

## 干跑验证

- 六阶段完整干跑样例见 `core-iteration/examples/smoke_pipeline.md`。
- 至少用一轮真实迭代数据跑四条规则，并输出 `triggered_rules` 与 `stop_reason`；只有结论没有数值不算完成。

## 硬性纪律

1. **任一硬规则触发即 STOP**，不允许“虽然触发了但我觉得还能继续”的软绕过。
2. **所有数值必须可复算**：输出要写明 metrics 值、阈值、公式；不允许只给结论。
3. **强制收益评估不能吞掉**：`forced_review=true` 必须出现在输出里，调度器必须展示给用户。
4. **STOP 不代表 Skill 失败**：只代表“本轮迭代的边际收益已经低于阈值”，应输出当前版本作为最终版本。
5. **人工覆盖**：用户明确要求继续时，可以覆盖 STOP，但必须在输出中记录 `override: user`，且下一轮仍要重新校验。

## 反模式速查

| 反模式 | 处理 |
|---|---|
| 只看新增节点数不看剩余高优缺口 | 会漏掉“矿脉枯竭”；必须用规则 D 双条件 |
| 编辑距离小但语义变化大 | 仍可能合理，但规则 A 会捕捉“语义没变化”；两者互补 |
| 缺口清单两次只是措辞不同 | 先归一化再算 Jaccard，否则会误判 |
| STOP 之后不提供收益摘要 | 违反输出契约；必须给命中/丢弃/新增节点数 |
| 强制评估被忽略 | 必须上报 forced_review，交给用户决定 |

## 简单用户话术

> 我每次迭代后都会算四个指标：语义是否真的变了、搜索缺口是否还在原地、文本有没有实质改动、以及这轮新增的有效知识够不够多。只要有一个指标说明“继续做下去收益已经很差”，我就 STOP，并给你一份本轮收益摘要：命中多少高优语料、丢掉多少低质语料、新增了多少有效节点。
