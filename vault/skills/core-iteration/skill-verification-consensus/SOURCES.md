# 检验与验证共识 · 来源清单

> 分级：`consensus` = 多来源重复；`style` = 单一专家独特做法；`warning` = 反例/边界；`common-lore` = 无直接引用但圈内普遍认同（已降权）。

| 来源 | 主题 | 贡献 | 分级 |
|---|---|---|---|
| [WordPress agent-skills authoring-guide](https://github.com/WordPress/agent-skills/blob/trunk/docs/authoring-guide.md) | 确定性 Skill 创作门禁 | SKILL.md 简短、确定性脚本、eval 场景、frontmatter 校验 | consensus |
| [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | 官方 Skill 创作规范 | 元数据第三人称、渐进披露、引用一层深、测试多模型 | consensus |
| [Anthropic docs 镜像 shipyard](https://github.com/lgbarn/shipyard/blob/main/skills/shipyard-writing-skills/anthropic-best-practices.md) | Anthopic 实践摘要 | 自由度分级、质量检查表、反模式 | consensus |
| [uinaf/agents skill-audit best-practices](https://github.com/uinaf/agents/blob/3cd37beb662b9038c5e1031fea4968e908741b5c/skills/skill-audit/references/best-practices.md) | Skill 审计清单 | 元数据/身体形态/渐进披露/审计问题 | consensus |
| [skilljack-evals](https://github.com/olaservo/skilljack-evals) | Skill 评测 CLI | 任务先行 TDD、无 skill 基线、Skill Lift、anti-trigger、oracle gate、judge 不门禁 | consensus |
| [claude-workflow-kit](https://github.com/ncoevoet/claude-workflow-kit) | Evidence-first 开发/验证 | claim-class 证明表、prove 可证伪、对抗规格审查、commit/spec gates、in-flight 阻断 | consensus |
| [Promptfoo Red Team Coding Agents](https://www.promptfoo.dev/docs/red-team/coding-agents/) | 编码 agent 红队 | 对交付物做对抗证据收集；按风险选证据 | consensus/style |
| 本地 `distillation-consensus` | 蒸馏三件套/来源纪律 | trigger/action/boundary + source_refs | common-lore（本地实践） |
| 本地 `value-validator` | 收敛判定 | 四条硬规则、数值可复算 | common-lore（本地实践） |
| 本地 `dsh-optimization-consensus` | 运维安全 | 不热更、隔离冒烟、回滚恢复实际文件 | common-lore（本地实践） |
