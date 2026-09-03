---
name: skill-management
description: 管理、定位、启用 DSH agent skills 的方法，并指导 agent 开发“一键启用所需 skill”的 DSH 功能/插件。用于用户问“怎么管理/开启 skill”“做 skill 开关面板”“把本地 SKILL.md 变成可调用 skill”时。
---

# Skill 管理方法（DSH）

> 目标：让 agent 能快速回答“现在有哪些 skill、该用哪个、要怎么启用”，并能动手开发一个 DSH 功能/插件，使用户可以方便地开启所需 skill。
> 完整扩展：本目录 `CONSENSUS.md`；API/来源：`SOURCES.md`。

## 触发条件

- 用户说“管理 skill”“开启/启用 skill”“哪个 skill 适合这个任务”。
- 用户要“把本地的 SKILL.md 变成 agent 可调用的 skill”。
- 用户要“做一个 DSH 功能/插件，让我一键启用所需 skill”。
- 当前 `available_skills` 里找不到某个 skill，但工作区里有对应文件。

## 第一步：定位（先判断，再动手）

1. 读当前会话的 skill 目录：`available_skills` 里只有“已发现且模型可调用”的摘要。
2. 读工作区 skill 文件：`$HOME/work/*/SKILL.md`、`$HOME/work/*/.agents/skills/*/SKILL.md`。
3. 按“任务意图”映射：
   - 重构/拆模块 → `work-consensus`
   - DSH 升级/子代理/热更 → `dsh-optimization-consensus`
   - 材料做成可执行 Skill → `distillation-consensus`
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
  - `$HOME/deepseek-harness/.agents/skills/`
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

## 来源

- `@deepseek-ai/dsh-skill`：`~/.npm-global/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-skill/README.zh.md`
- `@deepseek-ai/dsh-skill-filesystem`：同目录下 `dsh-skill-filesystem/README.zh.md`
- `@deepseek-ai/dsh-tool-skill`：同目录下 `dsh-tool-skill/README.zh.md`
- `@deepseek-ai/dsh-client-ui-skill`：同目录下 `dsh-client-ui-skill/README.zh.md`
- 运维共识：`~/.dsh/dsh-optimization-consensus.md`
- 蒸馏共识：`~/.dsh/.agent-presets/router-standard/skills/distillation-consensus/CONSENSUS.md`
