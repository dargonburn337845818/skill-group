# return-forensics · 来源声明

| 来源 | 贡献 |
|---|---|
| 本地 `value-meta-scheduler` / `value-validator` / `value-effect-audit` | 收益曲线、停止规则、效果数据 |
| [Convergence Detection](https://github.com/agentpatterns-ai/website/blob/main/loop-engineering/convergence-detection.md) | 连续无增量即收敛的启发式 |
| [Convergence Protocol](https://inferensys.com/glossary/recursive-error-correction/iterative-refinement-protocols/convergence-protocol) | 迭代改进停止/根因确认 |

说明：诊断矩阵为内部归纳，需结合真实 yield_curve 与 trace_chain 回测校准。

## Round 40 新增来源

| 来源 | 贡献 |
|---|---|
| [Self-Refine: Iterative Refinement with Self-Feedback (NeurIPS 2023)](https://openreview.net/forum?id=S37hOerQLB) | 单模型自反馈迭代可提升输出，但并非天然收敛；支撑“迭代有效”需效果回测的探针对照。 |
| [Large Language Models Cannot Self-Correct Reasoning Yet (ICLR 2024)](https://openreview.net/forum?id=IkmD3fKBPQ) | self-correction 可能无改善甚至变差；用于 negative_effect 判别与“自我修正即有效”误诊反例。 |
| [The Curse of Recursion: Training on Generated Data Makes Models Forget (2023)](https://openreview.net/forum?id=M69HNTRwc5) | 自生成数据再训练会导致遗忘与同质化；用于蒸馏侧“自我回收”检查。 |
| [Data Filtering Networks (ICLR 2024)](https://openreview.net/forum?id=KAk6ngZ09F) | 目标对齐过滤优于通用质量分；用于 filter_over_tight 探针与过滤侧检查。 |
| [Self-Consuming Generative Models Go MAD (ICLR 2024)](https://openreview.net/forum?id=ShjMHfmPs0) | 自消费生成循环导致分布退化；说明新语料若被同一管道回用仍会衰减。 |
| [Deduplicating Training Data Makes Language Models Better (ACL 2022)](https://doi.org/10.18653/v1/2022.acl-long.577) | 重复数据抑制收益；用于 corpus 去重与源族归一化。 |
| [The Diminishing Returns of Masked Language Models to Science (Findings ACL 2023)](https://doi.org/10.18653/v1/2023.findings-acl.82) | 持续投喂同类语料收益递减；用于 corpus_exhaustion / source_saturation 证据。 |
| [W3C PROV Overview / PROV-DM](https://www.w3.org/TR/prov-overview/) | 溯源本体与实体-活动-派生模型；支撑 trace_chain 可复现审计与 `wasInvalidatedBy` 保留语义。 |
