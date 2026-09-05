# Sources（skill-management）

> 来源台账。内部路径/本地文件按工作区约定解析；公开链接可在浏览器复核。

## 清单
- $WORKSPACE/skills/skill-management/SKILL.md
- @deepseek-ai/dsh-skill README

## 分级说明
- 本 skill 的核心规则在 `SKILL.md` 中带 `source_refs` 或来源章节；未标注来源的观点应视为待证。
- 单源结论不作为核心规则；冲突分支保留而非合并。

## Round 37 新增来源

> 检索方式：GitHub 仓库/主题搜索 + GitHub Contents API 官方文件交叉收集（本会话未暴露独立 web_search 工具，故用等价真实网络检索）；检索日期 2026-09-05。以下为 `## 2026 深度补强（Round 37）` 中 R37-1…R37-8 的来源编号。

- **R37-S1 — anthropics/skills README**（Anthropic 官方实现/示例/插件市场）：https://github.com/anthropics/skills/blob/main/README.md ，取用：Agent Skills 定义、SKILL.md 最小 frontmatter、Claude Code/Claude.ai/API 启用方式、官方模板与 spec 指针。
- **R37-S2 — vercel-labs/skills README**（开源 Agent Skills CLI）：https://github.com/vercel-labs/skills/blob/main/README.md ，取用：`add/list/find/remove/update` 命令、project/global 作用域、symlink/copy、私有仓库认证、内部 skill `metadata.internal`、发现深度 1–3 层与浅层遮蔽、plugin manifest 发现、下载限额。
- **R37-S3 — vercel-labs/agent-skills README**（技能集合与发现索引）：https://github.com/vercel-labs/agent-skills/blob/main/README.md ，取用：`SKILL.md + scripts/ + references/` 结构、安装后自动可用、“Use when”触发描述写法、discovery index 发布。
- **R37-S4 — addyosmani/agent-skills README**（生产级工程技能包）：https://github.com/addyosmani/agent-skills/blob/main/README.md ，取用：skill 统一 anatomy（Overview/When to Use/Process/Rationalizations/Red Flags/Verification）、Progressive Disclosure、单skill安装与共享 references 的 portability gap、跨 CLI/IDE 安装方式。
- **R37-S5 — obra/superpowers README**（可组合技能方法论）：https://github.com/obra/superpowers/blob/main/README.md ，取用：技能自动触发、meta skill（using-superpowers）、多 harness 分别安装、更新、telemetry/关闭、行为测试。
- **R37-S6 — mattpocock/skills README**（真实工程师技能集）：https://github.com/mattpocock/skills/blob/main/README.md ，取用：托管插件（只读订阅）vs 可编辑副本（自己拥有）两种分发哲学、禁止混装、每仓库 setup skill。
- **R37-S7 — xingkongliang/skills-manager README**（跨 50+ 工具的桌面管理器）：https://github.com/xingkongliang/skills-manager/blob/main/README.md ，取用：中央库 + 两步“install 入库、deploy 到 agent”、agent 驱动管理器而非直写 agent 目录、来源/预设/更新/跨 agent 状态、Git 备份同步、CLI 与 app 共用 SQLite。
- **R37-S8 — jiweiyeah/Skills-Manager README**（symlink 同步桌面管理器）：https://github.com/jiweiyeah/Skills-Manager/blob/main/README.md ，取用：write-once/symlink-to-many、`skm enable/disable/doctor/fix`、Windows 无管理员策略、companion skill 发布到市场、CLI 与桌面共用状态。
- **R37-S9 — iflytek/skillhub README**（企业级自托管 skill 注册表）：https://github.com/iflytek/skillhub/blob/main/README.md ，取用：registry/governance 定位（不是收藏集）、发布/版本/RBAC/审计、CLI install 到指定 agent、与 open collection 的职责分层。
- **R37-S10 — GoPlusSecurity/agentguard README**（Agent 安全层）：https://github.com/GoPlusSecurity/agentguard/blob/main/README.md ，取用：安装前扫描本地 skill/插件与 HTTPS 仓库、屏蔽恶意 skill、按 skill 追踪动作来源、DSH 原生扫描工具、可信更新对比。
- **R37-S11 — tech-leads-club/agent-skills README**（受管安全技能注册表与 CLI）：https://github.com/tech-leads-club/agent-skills/blob/main/README.md ，取用：静态分析/CI、lockfile/content hash、symlink guard、audit trail、install/update/remove/cache、按项目/全局/agent 选择。
- **R37-S12 — lasoons/AgentSkillsManager README**（IDE 技能管理扩展）：https://github.com/lasoons/AgentSkillsManager/blob/main/README.md ，取用：面板形态（browse/install 仓库、搜索云目录、按 workspace 安装到 active skills 目录）、多 IDE 配置。

