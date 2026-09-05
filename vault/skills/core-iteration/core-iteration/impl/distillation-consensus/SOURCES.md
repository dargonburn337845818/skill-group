# 蒸馏共识 · 网络来源清单

> 本清单记录本次“网络蒸馏技巧”研究曾参考的公开资料。
> 说明：这些链接用于交叉验证与继续深挖；本共识不是对任一来源的逐句搬运，而是抽取共性后重新组织。

## 内容 → Agent Skill 蒸馏

| 来源 | 主题 | 对本共识的贡献 |
|---|---|---|
| [cangjie-skill（kangarooking）](https://github.com/kangarooking/cangjie-skill) | 把书、长视频、播客等高价值内容蒸馏成可执行的 Agent Skills | “可执行 Skill”而非复述；内容片段切分 |
| [cangjie-skill SKILL.md](https://github.com/kangarooking/cangjie-skill/blob/main/SKILL.md) | 具体 skill 指令 | 触发/动作/边界/用户话术的结构化样例 |
| [仓颉 · 认知植入式思维蒸馏引擎（Yeadon8888）](https://github.com/Yeadon8888/cangjie-skill) | 让 AI“想得像他”，不只是“说得像他” | 强调思维方式/决策过程蒸馏，而非复述观点 |
| [WorkBuddyGuide 第22章：打造 Skill，将书和视频蒸馏为可执行 Skill](https://github.com/AlephAITech/WorkBuddyGuide/blob/main/docs/bluebook/%E7%AC%AC%E4%B8%89%E7%AF%87%20%E8%BF%9B%E9%98%B6%E7%AF%87%EF%BC%9A%E6%8A%8A%E6%A1%88%E4%BE%8B%E5%8F%98%E6%88%90%E8%87%AA%E5%B7%B1%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%B3%BB%E7%BB%9F/%E7%AC%AC%2022%20%E7%AB%A0%20%E6%89%93%E9%80%A0skill%EF%BC%9A%E5%B0%86%E4%B9%A6%E5%92%8C%E8%A7%86%E9%A2%91%E8%92%B8%E9%A6%8F%E4%B8%BA%E5%8F%AF%E6%89%A7%E8%A1%8C%20Skill/index.md) | 从书/视频构造可执行 Skill 的章节 | 目标先定、多轮加工、成品可执行 |
| [WorkBuddy 把书和视频蒸馏为 Skill（文章镜像）](http://www.jxxy.net/ai/paths/workbuddy-basics/workbuddy-34-build-skill/) | 入门到精通：打造 Skill | 用户侧简单语言表达方向/方式 |
| [knowledge-distillation-survey（windags-skills）](https://github.com/curiositech/windags-skills/tree/main/skills/knowledge-distillation-survey) | 知识类型与智能分解的调研 | 按知识类型选择蒸馏形态 |
| [ASPS：三层 Skill 构建框架](https://github.com/Beunec/asps) | 把技能拆成可部署工件 | 成品不能只是“一段话”，要有可部署的形态 |

## 知识蒸馏研究（跨领域启发）

| 来源 | 主题 | 对本共识的贡献 |
|---|---|---|
| [A Survey on Knowledge Distillation of Large Language Models](https://arxiv.org/html/2402.13116) | LLM 知识蒸馏综述 | “教师/学生”分层、响应/特征蒸馏等类比 |
| [A Comprehensive Survey on Knowledge Distillation](https://github.com/IPL-sharif/KD_Survey) | 通用知识蒸馏综述 | 蒸馏目标不是复制，而是迁移可复用的判断 |
| [A Comprehensive Survey on Data Distillation](https://xplorestaging.ieee.org/document/11250975) | 数据蒸馏综述 | 先选高价值样本/片段，再压缩 |

## Agent Skill 工程化与验证（Round 22 新增）

| 来源 | 主题 | 对本共识的贡献 |
|---|---|---|
| [WordPress agent-skills authoring-guide](https://github.com/WordPress/agent-skills/blob/trunk/docs/authoring-guide.md) | 确定性 Skill 创作门禁 | SKILL.md 简短、eval 场景、确定性脚本、Verification/Failure modes |
| [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | 官方 Skill 规范 | 元数据、渐进披露、一层引用、多模型测试 |
| [skilljack-evals](https://github.com/olaservo/skilljack-evals) | Skill 评测 | 任务先行、无 skill 基线、Skill Lift、anti-trigger、oracle gate |
| [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) | 专业级 Skill 编写/验证 | 元数据、可执行内容、验证实践、控制上下文 | consensus |
| [Anthropic Engineering: Agent Skills 落地](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | 官方工程实践 | 渐进披露、真实世界赋能、Skill 生态 | consensus |
| [claude-workflow-kit](https://github.com/ncoevoet/claude-workflow-kit) | Evidence-first 工作流 | 验证标准、claim 证明、prove-it-can-fail、对抗审查 |
| 本地 `skill-verification-consensus` | 检验底座 | 发布前校验报告与门槛 |

## 本地实践（交叉验证）

- `$WORKSPACE/skills/teacher-consensus-skill/SKILL.md`：算法竞赛教师共识 + 信息论 + 提问协议。
- `$WORKSPACE/skills/teacher-consensus-skill/METHOD.md`：七步蒸馏法（语料 → primitive → 矩阵 → 回测）。
- `$WORKSPACE/skills/dsh-optimization-consensus/CONSENSUS.md`：官方文档/源码 → 可执行运维共识。

## Round 37 新增来源

> 本轮补充用于「2026 深度补强」：来源编号 R37-1 … R37-10 与 SKILL.md 新节中的标记一一对应。

| 编号 | 来源 | 主题 | 对本共识的贡献 |
|---|---|---|---|
| R37-1 | [Anthropic Agent Skills: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md) | 官方创作规范 | 可观察触发、动作可检查、引用一层深、多模型测试 |
| R37-2 | [OpenAI ChatGPT Learn: Build skills](https://learn.chatgpt.com/docs/build-skills) | 平台侧技能创作 | 单元化、任务导向、避免模糊指令 |
| R37-3 | [Microsoft GitHub Copilot for Azure skill-authoring SKILL.md](https://github.com/microsoft/github-copilot-for-azure/blob/915f8099093ad7dbfe8f388da6fbaf47b8216ab8/.github/skills/skill-authoring/SKILL.md) | 企业级 Skill 创作与 anti-trigger | 触发/反触发必须显式、验证门禁 |
| R37-4 | [skillkit meta skill-authoring SKILL.md](https://github.com/rohitg00/skillkit/blob/5691b10c7e637cc7044da5df7891aa05ce732e1e/packages/core/src/methodology/packs/meta/skill-authoring/SKILL.md) | 元技能/自迭代创作 | 覆盖矩阵、迭代式补料 |
| R37-5 | [samzhu/skills-hub: Skill Design Patterns](https://github.com/samzhu/skills-hub/blob/5b5f8d6d2ef87592d9ac0d02705237153fd7ca59/.claude/skills/skill-author/references/design-patterns.md) | Skill 设计模式 | 边界/反例/失败路径设计 |
| R37-6 | [Jamie-BitFlight claude_skills: authoring-checklist.md](https://github.com/Jamie-BitFlight/claude_skills/blob/main/plugins/plugin-creator/skills/skill-creator/references/authoring-checklist.md) | Skill 创作检查清单 | 原子性检查、干跑检查 |
| R37-7 | [SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering?](https://ar5iv.labs.arxiv.org/html/2603.15401) | 技能实际增益与上下文干扰 | “skill 可能降性能”，反例/近失测试必要 |
| R37-8 | [SkillConsist: Detecting Inconsistencies in Agent Skills via Bidirectional Graph Alignment](https://arxiv.org/abs/2608.07639) | 技能内部/交叉不一致检测 | 来源/claim 冲突审查、一致性校验 |
| R37-9 | [AgentsMeetRL: data-curation.md](https://github.com/thinkwee/AgentsMeetRL/blob/main/skills/agents-meet-rl/problems/research-workflow/data-curation.md) | 语料筛选与数据质量 | 覆盖矩阵、低价值重复语料过滤 |
| R37-10 | [NaturalThoughts: Selecting and Distilling Reasoning Traces for General Reasoning Tasks](https://arxiv.org/abs/2507.01921) | 推理迹筛选与蒸馏 | 高价值片段筛选、最小推理单元 |
