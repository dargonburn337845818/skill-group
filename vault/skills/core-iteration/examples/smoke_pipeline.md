# 六阶段干跑样例：迭代 core-iteration 六件套（Round 1）

> 本样例以本轮真实迭代为蓝本，演示六个阶段如何衔接。所有数值可复算。

## 输入

```text
input = {
  target_skills: ["web-research-consensus", "benefit-filter", "distillation-consensus",
                  "value-iterator", "value-validator", "value-meta-scheduler"],
  core: true,
  max_depth: 5,
  state_path: "round_ledger.json"
}
```

## 第 1 阶段：信息搜集

- 拆问题：六件套缺什么？哪些接口没对齐？如何量化能力提升？
- 产出 `raw_corpus`（25 条候选主张：19 个内审缺口 + 6 个干跑验证要求）、`knowledge_gaps`（19 个）。
- 外部参考：OpenAI Agent Skills Evals、Convergence Protocol、Prompt Versioning 等。
- `search_meta.queries_run = 2`。

## 第 2 阶段：收益过滤

- 修正后的密度公式：`density = 0.4*novelty + 0.3*steps + 0.3*evidence`（全部 0–100）。
- 23 条候选全部 ≥60；2 条低密度候选被丢弃（“合并成一个大 SKILL”“无预算全网搜”）。
- `yield_stats`：

```text
raw_count=25, density_pass=23, verified_high_count=9,
verified_single_count=14, pending_count=0, discarded_count=2,
avg_density_score=77, verified_high_remaining_ratio=0.35
```

## 第 3 阶段：蒸馏

- 23 条候选被蒸馏成 23 条 Node，每条含 trigger/action/boundary/source_refs。
- 蒸馏自检分：7/7，达到可交付标准。

## 第 4 阶段：迭代器

```text
effective_new_count = 23
node_delta = { added: 21, updated: 0, merged: 0, conflict: 2, footnotes: 0 }
accepted = true
```

- 变更日志写入各 skill `CHANGELOG.md`；版本 `0.0.1 → 0.1.0`。

## 第 5 阶段：校验器

```text
semantic_displacement ≈ 0.12  (> 0.03, pass)
gap_jaccard = 0.10            (< 0.90, pass)
edit_distance_ratio ≈ 0.18    (> 0.05, pass)
effective_new_nodes = 23 > 2, verified_high_remaining_ratio = 0.35 >= 0.10 (pass)
decision = CONTINUE, triggered_rules = [], forced_review = false
```

## 第 6 阶段：调度收尾

```text
yield_curve = [
  { round: 1, raw_count: 25, high_hit: 23, discarded: 2, new_nodes: 23,
    marginal_yield: 1.00, cumulative: 23 }
]
capability_scorecard = { round0: 12/20 avg, current: 15/20 avg, total_gain: 3 }
expected_convergence_rounds = "1-2"
```

## 结论

- 本轮接受：六件套 SKILL.md + 新增 group README + 干跑样例 + round_ledger。
- 下一轮建议：针对“如何让评分卡可自动计算”“如何把 Node 变成可执行测试”继续补源。
