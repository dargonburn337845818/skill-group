---
name: skill-management
description: 管理、定位、启用 DSH agent skills 的方法，并指导 agent 开发“一键启用所需 skill”的 DSH 功能/插件。用于用户问“怎么管理/开启 skill”“做 skill 开关面板”“把本地 SKILL.md 变成可调用 skill”时。
whenToUse: 用户问怎么管理/开启 skill、做 skill 开关面板、把本地 SKILL.md 变成可调用 skill。
---
# Skill 管理方法（DSH）

> 目标：让 agent 能快速回答“现在有哪些 skill、该用哪个、要怎么启用”，并能动手开发一个 DSH 功能/插件，使用户可以方便地开启所需 skill。
> 完整扩展与来源：见本目录 `SOURCES.md`。

## 触发条件

- 用户说“管理 skill”“开启/启用 skill”“哪个 skill 适合这个任务”。
- 用户要“把本地的 SKILL.md 变成 agent 可调用的 skill”。
- 用户要“做一个 DSH 功能/插件，让我一键启用所需 skill”。
- 当前 `available_skills` 里找不到某个 skill，但工作区里有对应文件。

## 第一步：定位（先判断，再动手）

1. 读当前会话的 skill 目录：`available_skills` 里只有“已发现且模型可调用”的摘要。
2. 读工作区 skill 文件：`$WORKSPACE/*/SKILL.md`、`$WORKSPACE/*/.agents/skills/*/SKILL.md`。
3. 按“任务意图”映射：
   - 重构/拆模块 → `work-consensus`
   - DSH 升级/子代理/热更 → `dsh-optimization-consensus`
   - 材料做成可执行 Skill → `distillation-consensus`
   - 从多个 skill 里选调度方向 → `info-layer-skill-routing`
   - 压测方案 → `grill-me`
   - PPT → `ai-ppt`
   - 算法教学 → `teacher-consensus`
   - DSH 皮肤 → `dsh-skin-install`
4. 找不到 → 检查文件是否满足 skill 格式（见下）。

## 第二步：理解 DSH 的 skill 机制

### 关键事实

- Skill 注册表是 `ctx.skills`（`@deepseek-ai/dsh-skill`）。
- 文件系统提供方 `@deepseek-ai/dsh-skill-filesystem` 发现 skill：
  - 只扫一层：`<根>/<name>/SKILL.md` 或 `<根>/<name>.md`。
  - 支持的项目/用户根：`<项目>/.dsh/skills`、`<项目>/.agents/skills`、`customSkillDirs`、`<dshHome>/skills`、`<agentsHome>/skills`。
- Frontmatter 必填：`name`（kebab-case）、`description`。
- 可选：`whenToUse`、`disable-model-invocation`、`user-invocable`。
- 当前 preset 的 `customSkillDirs` 指向：
  - `~/.dsh/.agent-presets/router-standard/skills/`
  - `$DSH_CHECKOUT/.agents/skills/`
- `ctx.skills.list()` / `snapshot()` 返回当前目录；`ctx.skills.get(name)` 加载正文；`ctx.skills.register(skill)` 可以运行时注册一个内存 skill。

### 模型可调用 / 用户可调用

- `modelInvocable: true`：出现在 `<available_skills>`，模型可用 `skill` 工具加载。
- `userInvocable: true`：用户在输入框用 `/skill名` 可显式加载。
- `disable-model-invocation: true`：只允许用户显式调用，模型目录不出现。
- `user-invocable: false`：用户菜单不出现。

## 第三步：启用一个 skill（三种方式，按场景选）

### 方式 A：放进已监视的 skill 根（持久，推荐给“本地 skill 入库”）

```text
目标目录 = <项目>/.dsh/skills/<name>/SKILL.md
或 customSkillDirs 下的 <name>/SKILL.md
```

- 写入/软链 `SKILL.md`。
- 文件系统提供方会通过 watcher 自动刷新；`ctx.skills.list()` 即可看到。
- 边界：不要写成嵌套 `**/SKILL.md`；名称必须是 kebab-case；frontmatter 必须合法。
- 涉及 `~/.dsh` 时先按运维共识提醒用户，不要在运行中 agent 里硬改。

### 方式 B：运行时 `ctx.skills.register()`（内存，立即生效）

```ts
ctx.skills.register({
  name: 'my-skill',
  description: '一句话说明',
  content: 'skill 正文',
  // 可选
  invocation: { modelInvocable: true, userInvocable: true },
  resourceBase: { kind: 'directory', path: '/abs/path/to/skill' },
});
```

- 适合做成 DSH 插件：插件启动时读取“已启用清单”，把每个本地 skill 注册进运行时层。
- 边界：运行时注册不持久；插件重启后必须重新注册。跨重启的“已启用状态”要由插件自己写配置文件。

### 方式 C：插件的“技能保险库”模式（深模块方案）

```text
skill-management-plugin/
├── config: 已启用 skill 清单
├── vault/: 本地 skill 源文件（SKILL.md 仓库）
└── 启动时: 对每个 enabled 条目调用 ctx.skills.register()
```

- 用户通过 tool/UI/命令开启或关闭。
- 开启 = 写配置 + `ctx.skills.register()` + `invalidate`/`skills/change`。
- 关闭 = 改配置 + 由插件维护 disposer，释放运行时注册。
- 优点：不依赖用户手工复制文件到 `~/.dsh`，不破坏项目根；可持久、可回滚。

## 第四步：开发“一键启用所需 skill”的 DSH 功能

### 先定形态

| 形态 | 适合 | 说明 |
|---|---|---|
| `toolkit` | 让 agent 调用 `skill_enable`/`skill_disable`/`skill_list` | 最快可用，命令行/Agent 侧管理 |
| `ui-panel` | 让用户可视化勾选 skill | 需要 client 构建，适合“方便开启” |
| `hybrid` | tool + UI 都提供 | 推荐，agent 和人都能管理 |

### 推荐接口

```text
skill_list                 # 列出当前目录 + vault 候选 + 启用状态
skill_enable <name|path>   # 启用一个本地 skill
skill_disable <name>       # 关闭一个运行时 skill
```

### 实现要点

1. 插件 `inject` 至少包含 `skills`；做工具时再加 `tools`。
2. 启动时读取持久化配置（如 `<pluginDir>/enabled.json` 或 DSH 配置项）。
3. 用 `ctx.skills.register()` 注册启用项；保存 disposer。
4. 变更后调用注册表失效机制：`ctx.skills.register()` 本身会发 `skills/change`，消费方自动刷新。
5. 校验：启用后调 `ctx.skills.list()` / `ctx.skills.get(name)` 确认模型可调用。
6. 安全：恢复 disposer、保留配置快照；涉及插件更新按 `dsh-optimization-consensus` 走隔离冒烟。

### 边界

- 运行时 skill 的 rank 是 250：项目文件系统 skill 会覆盖它，自定义/用户根会被它覆盖。同名冲突要明确“谁赢”。
- 不要试图“禁用”文件系统已存在的 skill 只靠运行时注册；同名会被项目层覆盖。要禁用应改文件/软链或 frontmatter 调用策略。
- DSH 当前发现深度只支持一层；不要做递归 skill 树。
- `~/.dsh` 在本会话沙箱中只读；任何写 `~/.dsh` 的操作必须先提醒用户，最好交给外部终端执行。

## 第五步：按共识交付

- 面向用户话术：方向（现在该用哪个 skill）、方式（怎么启用/开发）、边界（什么时候这条路不通）。
- 改动 DSH/插件前先读 `dsh-optimization-consensus`：备份、隔离冒烟、确认无 running agent、回滚实际文件。
- 完成后给来源/路径表，让用户能复核。

## 反例/边界速查

| 情况 | 正确做法 |
|---|---|
| 只做了一个摘要，没有 trigger/action/boundary | 不是可执行 skill，补全或删除 |
| 想“禁用”一个已由文件系统提供的 skill | 运行时 register 同名的遮蔽不一定稳定，改文件/frontmatter 更可靠 |
| 用户想在当前会话快速用某个本地 skill | 先读对应 `SKILL.md` 即可，不必急着装插件 |
| 要在运行中的 agent 里热装插件 | 禁止；等无 running agent 或外部终端执行 |
| skill 不在 available_skills 里 | 检查是否在自定义根、frontmatter 是否合法、是否被 `disable-model-invocation` 隐藏 |

## 简单用户话术

> 我给你的是三样东西：方向（哪个 skill 该用）、方式（怎么开启/怎么把它做成 DSH 功能）、边界（什么情况下这个方法不适用）。

## 2026 深度补强（Round 37）

> 本轮基于 Agent Skills 生态（Anthropic 官方、Vercel 社区技能生态、技能管理器/桌面 App、企业注册表与安全层）蒸馏，补齐目录规范、渐进披露、两步启用、分发模式、面板清单与安全底线。来源编号见 `SOURCES.md` 的 `## Round 37 新增来源`；每条规则都带可执行检查清单与反例。

### R37-1 目录发现：浅层遮蔽深层，目录名必须等于 skill name

**规则**

- 一个 skill = 一个目录，入口是 `<dir>/SKILL.md`；目录名必须等于 frontmatter `name`（kebab-case），避免“目录叫 x、frontmatter 叫 y”导致归属混乱。
- 发现器按“浅层优先”：`skills/<name>/SKILL.md` 遮蔽 `skills/<category>/<name>/SKILL.md`；同仓库内更浅的 `SKILL.md` 会压过更深层的同名条目。
- 分类目录（`skills/frontend/`、`skills/.curated/`）不是 skill；不要把它们注册为可调用条目。
- DSH 当前只支持一层发现；生态里的 2–3 层分类写法（`skills/<category>/<name>/SKILL.md`）只有在消费者明确支持时才可使用，否则把分类做进面板标签/索引，而不是目录层级。

**检查清单**

- `find <skill根> -name SKILL.md`，确认每个 skill 目录只出现一个入口。
- frontmatter `name` 与所在目录名一致；不一致立即修。
- 若要用多级分类，先查当前 DSH 版本/`dsh-skill-filesystem` 是否支持；不支持就保持一层，并在 UI 里用 tag/category 过滤。
- 发行前用 `npx skills add <repo> --list`（或等价 list 命令）验证实际发现清单与预期一致。

**反例**

- 同时存在 `skills/frontend/react/SKILL.md` 与 `skills/react/SKILL.md`：浅层遮蔽深层，用户以为自己装了 `react`，实际发现的是另一个路径。
- 在 DSH 里直接写 `skills/a/b/SKILL.md`：当前只扫一层，永远发现不了，面板还显示“已启用”是假阳性。

### R37-2 渐进披露：SKILL.md 是入口，长材料放 references/scripts

**规则**

- `SKILL.md` 保持短而可执行：打开就能判断“该不该触发、下一步做什么、何时停”；详细检查表放 `references/`，脚本放 `scripts/`。
- 所有资源路径以 skill 根为基准相对引用；运行时注册时必须传 `resourceBase`，否则相对路径解析失败。
- 支持“按需加载”：入口只引用文件名，正文里写明“需要时再读 `references/xxx.md`”。

**检查清单**

- `SKILL.md` 开头几行能独立回答：做什么 / 何时用 / 最小步骤。
- `references/` 与 `scripts/` 使用相对路径；不存在绝对路径或跨 skill 目录的隐式依赖。
- 按单 skill 安装（不装整仓）后仍能工作；若失败，检查共享 `references/` 是否被遗漏。
- `ctx.skills.get(name)` 后能读取 `resourceBase` 下的资源文件。

**反例**

- 把 10k 行 checklist 全塞进 `SKILL.md`：每次加载都在烧 token，入口被淹。
- 只拷贝 `skills/<name>/`、不拷贝仓库级 `references/`：skill 能注册，但正文里“详见 references”全部断链。

### R37-3 两步启用：先入中央库，再部署到具体 agent

**规则**

- 把“安装到库/目录”与“启用/部署到 agent”拆成两步，不要让“启用”动作直接往 agent 目录写文件。
- 库是唯一事实源，保留来源、版本、预设成员关系和跨 agent 部署状态；agent 目录只是库的链接/副本/运行时注册。
- DSH 插件对应：`skill_install` 只入库、不出现在模型目录；`skill_enable <name> --for <profile/agent>` 才注册/建链；`skill_disable` 只移除该 agent 的启用，不删库。

**检查清单**

- 有“已安装未启用”状态，且能一眼看出每个 skill 在哪些 agent/profile 上启用。
- 每次启用/停用都持久化到配置，可回滚。
- enable 操作输出明确：目标 agent、来源、是否成功、是否冲突。
- 不要让 agent 直接写 `~/.claude/skills` 等目录；驱动管理器/CLI/插件 API 完成。

**反例**

- agent 直接往各 agent 目录写 `SKILL.md`：后续无法回答“这个 skill 从哪来、什么版本、哪些工具装了”，update/remove 全部抓瞎。

### R37-4 分发模式二选一：托管插件 vs 可编辑副本，禁止混装

**规则**

- 每个 skill 源只选一种分发模式：
  - 托管/插件（managed）：只读、订阅、自动更新，适合“跟着上游走”；
  - 可编辑副本/软链（editable copy/symlink）：自己拥有、显式 update，适合“改成自己的”。
- 优先 symlink 作为单源；不支持软链的环境用 copy，并在 UI 标明。
- 面板要展示 source + mode + update available；同一来源同时走两种安装会出现重复 skill 和互相打架的更新。

**检查清单**

- 安装时允许选择 symlink/copy，默认推荐 symlink。
- 提供 `skill_doctor` / `fix`（或等价命令）检查断链、重复、版本漂移。
- 卸载/更新按原分发模式执行，避免“symlink 装的却被 copy 删除”。
- 若检测到同一 name 来自两个来源，面板标 conflict，不要静默覆盖。

**反例**

- 先 `npx skills add repo` 拷贝一份，又 `/plugin install 同一套`：每个 skill 出现两份，更新时一份自动、一份手改，行为不可预期。

### R37-5 description 是触发入口，不是营销文案

**规则**

- `description` 必须同时回答“做什么”和“何时用”，因为它承担自动激活与搜索匹配；正文再写 `When to Use` / 触发场景。
- 避免宽泛关键词堆砌（`best practices`、`AI`、`GPT`），否则模型在很多无关任务上误触发或根本不触发。
- 复杂任务映射交给 meta/router skill（如 `using-agent-skills`、`using-superpowers`），而不是把触发逻辑塞进单个 description。

**检查清单**

- description 控制在 1–2 句，含明确对象 + 场景 + 可观测结果。
- 启用后用 3 个真实用户句子做干跑：该触发时触发、不该触发时不触发。
- 若技能不触发，先查 description；若太泛，加具体名词/动词/场景边界。
- 有 list/search 时，`description` 能被关键词检索命中。

**反例**

- description 只写 `Best practices for engineering`：模型不知道怎么用，用户搜“code review”也搜不到它。
- description 写满所有潜在关键词：任何“做个设计”都会被误触发，实际执行时上下文质量下降。

### R37-6 面板/插件命令集：不止开关，还要来源、范围、更新、诊断

**规则**

- 一个合格的 skill 管理面板/插件至少提供：`list/search`、`install`（入库）、`enable/disable --for <agent>`、`update`、`remove`、`doctor/fix`、`--dry-run`、`--json`。
- 每个条目显示：name/description、enabled 状态、scope（项目/全局）、source（项目/全局/库/插件/市场）、distribution mode、版本与可更新、同名冲突。
- 支持非交互/CI：`--yes`、`--all`、指定 `--agent`、`--skill`；默认不自动全部启用。

**检查清单**

- 用户能回答：这是什么、谁装的、装在哪些 agent、能不能更新、怎么回滚。
- 命令行与 UI 读同一份状态文件，不出现“UI 关掉但 CLI 还启用”。
- `install` 后不自动 enable；`enable` 后立刻可通过 list 验证。
- 每次变更可留审计日志（who/what/when/from）。

**反例**

- 面板只有“绿/灰开关”：用户不知道它是项目级还是全局级、是软链还是副本、有没有新版，出了故障只能删目录重来。

### R37-7 安全门：启用前扫描、来源可追溯、操作可审计

**规则**

- Skill 是“可执行指令包”，不是纯文本；从公开源启用前先过信任门：静态扫描、内容 hash/lockfile、symlink 防护、审计日志、pin commit/tag。
- 面板的“启用”按钮不应静默写文件；记录来源 + commit + hash，允许回滚。
- 更新前做 diff/compare，确认没有新增权限或危险逻辑；扫描失败/截断时不允许标“安全”。

**检查清单**

- 安装前可扫描本地 skill/插件或 HTTPS 仓库；有 SHOW SOURCE / 信任层级。
- 记录每个已启用 skill 的来源 URL/commit/hash；可复现安装。
- 知道哪个 skill 触发了哪个动作；出问题时能定位。
- 对签名/发布不完整或扫描结果 `incomplete` 的包，默认拒绝或降级为“仅查看”。

**反例**

- `npx skills add unknown-repo` 直接执行：仓库里的 `SKILL.md` 可引导 agent 跑任意命令，无来源、无审计、无回滚。
- “看到有 star 就觉得安全”：stars 是热度不是安全证据。

### R37-8 分发用 manifest/index 声明 skills，不靠全仓递归

**规则**

- 仓库/插件把“哪些 skill 属于哪个插件/市场”写进 manifest（如 `.claude-plugin/marketplace.json`、`plugin.json` 的 skills 数组）或 discovery index；agent/面板按声明选择，而不是全仓扫描所有 `SKILL.md`。
- DSH 插件自带的 skill 应作为插件资源在启动时 `ctx.skills.register()`，并随 manifest 声明；不要指望 watcher 去插件目录递归发现（DSH 只探一层）。
- 大集合应允许“按 skill 选择/按子集安装”，避免 200 个技能全部进模型目录造成触发噪音与上下文膨胀。

**检查清单**

- `--list` / `find` 能列出可声明 skill，且与 manifest 一致。
- 插件安装后 `ctx.skills.list()` 能看到声明的条目；卸载时全部释放。
- 安装单 skill 不携带整仓无关材料；携带的资源随包走。
- 发布/更新时校验 manifest 中路径存在、重复、失效。

**反例**

- 把社区大集合直接丢进同一个 `skills/` 并让 agent 全量发现：每个任务都在与几百个 description 竞争，误触发和 token 消耗同时上升。
- 插件里声明了 10 个 skill，却只注册了 5 个：面板和运行时状态不一致。

## 来源

- `@deepseek-ai/dsh-skill`：`~/.npm-global/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-skill/README.zh.md`
- `@deepseek-ai/dsh-skill-filesystem`：同目录下 `dsh-skill-filesystem/README.zh.md`
- `@deepseek-ai/dsh-tool-skill`：同目录下 `dsh-tool-skill/README.zh.md`
- `@deepseek-ai/dsh-client-ui-skill`：同目录下 `dsh-client-ui-skill/README.zh.md`
- 运维共识：`~/.dsh/dsh-optimization-consensus.md`
- 蒸馏共识：`~/.dsh/.agent-presets/router-standard/skills/distillation-consensus/CONSENSUS.md`
