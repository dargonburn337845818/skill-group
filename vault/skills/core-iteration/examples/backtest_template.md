# 真实使用回测模板（Backtest Template）

> 目标：验证六个 skill 不只是“读起来对”，而是在真实任务里能执行、能产出可审计结果。
> 用法：每个 skill 至少选 2 个真实任务跑一遍，填写下表；未通过项进入下一轮补强。

## 任务记录

| 字段 | 填写 |
|---|---|
| 日期 | 2026-09-04 |
| 被测 skill | 例如 benefit-filter |
| 真实任务 | 一句话：把哪些语料过滤成 verified 类 |
| 输入样本数 | N |
| 输出是否匹配接口契约 | 是/否 |
| 通过/失效 | 通过 / 失效：<具体现象> |

## 六阶段回测矩阵

| 阶段 | 通过标准 | 结果 |
|---|---|---|
| web-research-consensus | 能产出 raw_corpus/knowledge_gaps，字段齐全 | ☐ |
| benefit-filter | 能产出 yield_stats/verified_high，阈值 60 可达成 | ☐ |
| distillation-consensus | 能产出三件套 Node，且自检分 ≥5/7 | ☐ |
| value-iterator | 能产出 changelog 并正确计数 | ☐ |
| value-validator | 能复算四条规则并给出 stop_reason | ☐ |
| value-meta-scheduler | 能输出收益曲线/评分卡/收敛预测 | ☐ |

## 回测结论

- 通过的 skill：填空
- 未通过的 skill：填空 + 原因
- 下一轮优先级：排序

## 反例注入

对每个 skill 至少构造 1 个失效场景（例如“只用单一通稿的来源”“新版只改措辞”），确认 skill 能正确拒绝或降级。

> 人类接管：如果回测出现“技能教条与实际不符”，停下来记录 `override: human`。
