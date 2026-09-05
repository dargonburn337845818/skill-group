# 校验器 · 来源声明

> 本 skill 的规则来自“认知收益架构 / 价值驱动递归提升模块”的用户规格，并结合收敛检测与相似度计算的外部实践。

| 来源 | 贡献 |
|---|---|
| 用户规格：认知收益架构 / 价值驱动递归提升模块 | 四条硬规则与强制收益评估的原始设计 |
| `benefit-filter` | `verified_high_remaining_ratio` 与 `yield_stats` |
| `value-iterator` | `effective_new_nodes` / 新旧 Skill 版本 |
| [Convergence Protocol: AI Agent Stopping Rules](https://inferensys.com/glossary/recursive-error-correction/iterative-refinement-protocols/convergence-protocol) | 停止类协议的启发式（网络参考） |
| [Convergence Detection](https://github.com/agentpatterns-ai/website/blob/main/loop-engineering/convergence-detection.md) | 连续无增量即收敛（网络参考） |
| [SemHash-LLM 语义哈希去重](https://arxiv.org/html/2607.01601) | 文档相似度/去重的工程实践（网络参考） |

## Round 40 新增来源

> 采集说明：本会话未暴露独立 `web_search` 工具，改用等效真实检索（`wb`/Crossref 学术元数据接口直接查询与核验）收集；以下均为真实可复核的公开来源，编号对应 SKILL.md「2026 深度补强（Round 40）」中的 S1～S7。

| 来源 | 贡献 |
|---|---|
| [S1] Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback"（NeurIPS 36, 2023）— https://doi.org/10.52202/075280-2019 | 自反馈迭代精炼的基准实践：精炼后改善会快速饱和，支撑“迭代不是越多越好”的成本/增量判断 |
| [S2] "Toward a Theory of Semantic Fixed Points: Evidence from Iterative Language Model Self-Refinement"（SSRN 预印本, 2026）— https://doi.org/10.2139/ssrn.7095579 | 语义轨迹呈指数收敛到稳定状态，支撑固定点检测与增量衰减拟合 |
| [S3] "Cognitive Drift in Generative AI: Self-Normalized Displacement as a Measurement Principle for Semantic Coherence in LLMs"（SSRN 预印本, 2026）— https://doi.org/10.2139/ssrn.7127098 | 仅用 embedding 几何计算 Volatility Factor 与 Stagnation Signal，支撑轨迹级停滞/震荡检测 |
| [S4] "Algorithmic Groupthink: Causal Analysis and Mitigation of Semantic Convergence in Multi-agent LLM Systems"（Research Square 预印本, 2026）— https://doi.org/10.21203/rs.3.rs-10172697/v1 | 共享草稿使输出语义多样性下降、隔离提升多样性，支撑同源回声检测与隔离探针 |
| [S5] "Iterative Audit Convergence in LLM-Managed Multi-Agent Systems: A Case Study in Prompt-Engineering Quality Assurance"（Software, 2026）— https://doi.org/10.3390/software5020026 | 九轮缺陷数呈非单调波动（15,8,12,2,8,1,4,1,0），支撑“单轮低产不立即定死、需连续轮次确认”的守卫 |
| [S6] "Multi-Objective Optimal Threshold Selection for Similarity Functions in Siamese Networks for Semantic Textual Similarity Tasks"（预印本, 2024）— https://doi.org/10.20944/preprints202407.0020.v1 | 阈值选择是多目标/稳定性问题，支撑近边界脆弱带与阈值校准不要只看单点 |
| [S7] "Chronological text similarity with pretrained embedding and edit distance"（书章, 2022）— https://doi.org/10.1016/b978-0-12-824054-0.00014-9 | 同时使用预训练 embedding 与编辑距离做文本相似度，支撑 A/C 交叉核验与降级策略 |
