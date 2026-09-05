# 迭代器 · 来源声明

> 本 skill 的规则来自“认知收益架构 / 价值驱动递归提升模块”的用户规格，并参考版本管理与 Skill 评估的外部实践。

| 来源 | 贡献 |
|---|---|
| 用户规格：认知收益架构 / 价值驱动递归提升模块 | 知识节点、有效新增、变更日志的原始设计 |
| `distillation-consensus` | Node 的 claim/action/boundary 三件套 |
| `benefit-filter` | `verified_high` / `verified-single` 输入 |
| [Prompt Versioning in Production](https://www.respan.ai/articles/prompt-versioning) | 版本号、changelog、回滚（网络参考） |
| [How to Version & Rollback LLM Agent Prompts](https://www.arthur.ai/column/version-rollback-prompts-llm-agents) | semver + 可回滚（网络参考） |

## Round 40 新增来源

| 来源 | 贡献 |
|---|---|
| [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) | 变更日志人类可读、类型分组、Unreleased/Deprecated/Removed、yanked 回退记录（S1） |
| [Semantic Versioning 2.0.0](https://semver.org/) | 公共 API 声明、major/minor/patch 边界、breaking 与弃用路径（S2） |
| [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) | 条目类型 feat/fix/BREAKING CHANGE 与语义化版本映射（S3） |
| [GraphSentinel: Incremental CTI Knowledge Graph Updates with Structure-Aware Entity Alignment and Conflict Detection](https://doi.org/10.21203/rs.3.rs-9836957/v1) | 结构感知实体对齐、文本相似度不足以判等价、增量 duplicate/conflict 分类、多跳矛盾检测（S4） |
| [Sample Ratio Mismatch and Other Trust-Related Guardrail Metrics](https://doi.org/10.1017/9781108653985.027) | A/B 实验可信度与守卫指标：样本比偏移、实验质量检查（S5） |
| [Metrics for Experimentation and the Overall Evaluation Criterion](https://doi.org/10.1017/9781108653985.010) | 目标指标与守卫指标分离、总体评估准则（S6） |
| [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) | 反馈→生成→评估→接受/回退的迭代循环（S7） |
| [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | 记忆化失败、自我反思与下一轮行动修正（S8） |
