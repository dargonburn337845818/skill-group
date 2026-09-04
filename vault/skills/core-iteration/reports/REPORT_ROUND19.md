# Round 19：Skill 对模型增强的量化评分

> 参考：OpenAI Agent Skills Evals、Scale Agentic Leaderboard、skilljack-evals

## 标准

A/B 基准：同一任务集上，模型 **无 skill** vs **有 skill** 对比：

| 指标 | 说明 | 权重 |
|---|---|---|
| 任务成功率 | 0-1 | 0.30 |
| 输出质量 | 0-100 | 0.25 |
| 效率 | steps/time，越低越好 | 0.15 |
| 能力覆盖 | 0-1 | 0.15 |
| 置信校准 | 0-1 | 0.15 |

## 增强指数

```text
增强指数 = Σ(各指标相对增益 × 权重)
```

评级：

- ≥30%：显著增强
- 15-30%：明显增强
- 5-15%：轻微增强
- <5%：近乎无增强

## 当前示例（模板数据，非真实模型评测）

```text
基准模型分：45.8
使用 Skill 后：62.0
增强指数：25.5%
评级：明显增强
```

## 工具

- `tools/skill_effect_bench.py`
- `benchmarks/skill_benchmark_template.json`
- 输出：`tools/output/ENHANCEMENT_REPORT.json/.md`

## 说明

这是可执行框架 + 示例模板；真实增强指数需要填写真实 A/B 任务结果后再计算。
