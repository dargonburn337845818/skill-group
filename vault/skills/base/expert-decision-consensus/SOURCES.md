# 来源表（Sources）

## LightRead AI（商业科研工作台，作为“工作流化 + 可追溯 + 多 Agent”样本）

- 官网首页：https://lightingread.cn/
  - “云端科研执行 Agent”“一个工作区搜读写算”“关掉网页也继续”
- 产品介绍：https://lightingread.cn/intro
  - 多源学术搜索、智能 PDF 阅读、证据追溯、论文图谱 & 智能记忆、云端 AI Agent
- 博客《如何用 AI 高效阅读学术论文：5 个实用技巧》：https://lightingread.cn/blog/ai-reading-tips
  - 先问再读、结构化摘要、边读边标证据、跨论文统一维度、从证据表生成综述提纲
- 博客《从混乱到有序：构建个人学术文献管理体系》：https://lightingread.cn/blog/literature-management
  - 结构化存储、多维标签、证据笔记（结论回链 PDF 原句/图表/页码）
- 博客《研究生 AI 使用声明怎么写》：https://lightingread.cn/blog/ai-usage-declaration-how-to-write
  - 透明披露、过程留痕、验证过程（引用核对/事实核对/原意比对/记录留存）
- CLI 包：https://www.npmjs.com/package/lightread-cli
  - 论文搜索、资源库、PDF Markdown Bundle、笔记、图谱、记忆、内置 Skill Catalog
- 公开前端资源（zh-CN 文案，用于确认“并行智能体/子代理/阶段验收/记忆/创建技能”等术语）：
  - `zh-CN-6C50C0it.js`：`multiAgentModeHover`、`agentSwarmTip`、`swarmExplain`、
    `workflows`（接力/验收/续上）、`taskBuilder.promptRules`、“用对话创建技能”等。

## 开源 Research Workbench（非 LightRead 官方，更具体的可抄实现）

- 仓库：https://github.com/M-24rjgc/research-workbench
  - README：13 阶段流程、三层架构、研究台账、阶段门禁、三轮互盲审查、写作保真、新颖性审计
  - 文档：`docs/stages.md`、`docs/hooks-gates.md`、`docs/memory-graph.md`
  - 技能：30 个技能随仓库打包（7 自研 + 23 精选第三方）

## 本地 DSH 技能体系

- `vault/skills/teacher/expert-team/SKILL.md` —— 标准化专家团协议（定域/加载/独立表态/冲突/裁决/署名）
- `vault/skills/teacher/teacher-module/SKILL.md` —— 教师模块：人名专家团与回合式讨论
- `vault/skills/research/research-module/SKILL.md` —— 科研多 agent 导师团队与论文/组会流程
- `vault/skills/core-iteration/dev-workflow-consensus/SKILL.md` —— 开发工作流：Frame→Spec→Gate→Build→Verify→Ship
- `vault/skills/core-iteration/skill-verification-consensus/SKILL.md` —— 证据分类、可证伪检查、任务先行评测、红队
- `~/.dsh/.agent-presets/router-standard/skills/distillation-consensus/CONSENSUS.md` —— 内容蒸馏为可执行 Skill 的九步流水线
- `~/.dsh/AGENTS.md` —— 深模块优先、Deletion Test、接口即测试面、模块地图、AI 即新人

## 来源纪律

- 本 skill 不把任何单一来源当作“权威结论”；每条通用规则都至少能从“产品实践 + 开源实现 + 本地协议”三处交叉验证。
- LightRead 相关文案是公开产品/网页材料；开源 Research Workbench 是可直接审计的代码/文档。
- 专家观点风格推断非本人原话；引用时必须保留出处与“风格推断”声明。

## Round 38 新增来源

- McMillan SS, King M, Tully MP. How to use the nominal group and Delphi techniques. https://pubmed.ncbi.nlm.nih.gov/26846316/
  - 支持“匿名独立首轮 → 结构化反馈 → 再次评分”的两轮共识协议；“一致同意”与“真实收敛”之间的区别。
- CDC ACIP GRADE Handbook, Chapter 7: GRADE Criteria Determining Certainty of Evidence. https://www.cdc.gov/acip-grade-handbook/hcp/chapter-7-grade-criteria-determining-certainty-of-evidence/index.html
  - 支持证据确定性分档（high/moderate/low/very low）与“决策强度不得超过证据上限”的纪律。
- Emergence of Biased Consensus in Multi-Agent LLM Debates. ICML 2026. https://icml.cc/virtual/2026/poster/66269
  - 支持“看似一致可能是有偏共识”，反共识审计与少数派报告的必要性。
- An Empirical Study of Group Conformity in Multi-Agent Systems. ACL Findings 2025. https://aclanthology.org/2025.findings-acl.265/
  - 支持匿名化表态、避免从众/锚定，多数意见不等于正确意见。
- SELENE: Selective and Evidence-Weighted LLM Debating for Efficient and Reliable Reasoning. EACL 2026 Industry. https://aclanthology.org/2026.eacl-industry.7/
  - 支持证据加权的辩论/表决策略：不是每轮都全员全量再吵，而是按证据与分歧选择性重议。
- Spring AI Agentic Patterns (Part 4): Subagent Orchestration. https://spring.io/blog/2026/01/27/spring-ai-agentic-patterns-4-task-subagents
  - 支持子代理任务契约、独立验收与接力门禁的工程化做法。
- Sub-Agents & Orchestration. https://learn.agentpatterns.ai/harness-engineering/sub-agents-and-orchestration/
  - 支持子代理边界、工具范围、可恢复性与“结果由他人核验”的编排守则。
- OWASP GenAI: Vendor Evaluation Criteria for AI Red Teaming Providers & Tooling v1.0. https://genai.owasp.org/resource/owasp-vendor-evaluation-criteria-for-ai-red-teaming-providers-tooling-v1-0/
  - 支持按失败模式展开红队检查单（幻觉、数据泄露、提示注入、工具越权等），而非泛泛复核。
- GDS Way: Documenting architecture decisions. https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html
  - 支持 ADR 式决策记录：status、context、alternatives、consequences、superseded。
- Red Hat: Why you should be using architecture decision records. https://www.redhat.com/en/blog/architecture-decision-records
  - 支持“被否决/被替代决策保留原文”的审计留痕，以及决策日志可搜索性。
- GO FAIR Foundation: FAIR Principles. https://www.gofair.foundation/fair-principles
  - 支持证据/数据指针可发现、可访问、可互操作、可复用；数据版本与 provenance 不能丢。
- kangarooking/system-prompt-skills: 从 165 个顶级 AI 产品系统提示词中蒸馏出的 15 个可执行 Agent skill. https://github.com/kangarooking/system-prompt-skills
  - 支持技能蒸馏不仅要成功案例，还要从真实提示词/失败教训中提取“何时不用”与反例。

