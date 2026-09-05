---
name: dsh-optimization-consensus
description: DSH 运维与优化共识——子代理数量有界、升级插件先隔离兼容+冒烟、运行中 agent 禁止热更、破坏性操作先提醒用户并准备回滚。用于任何 DSH/插件升级、子代理调度、热更新或重启决策前。
whenToUse: 任何 DSH/插件升级、WSL+Windows 双端同步、子代理调度、热更新或重启决策前。
---
# DSH 运维与优化共识

## 触发条件

- 任何 DSH/插件升级、子代理数量/并发调度、热更新、重启、回滚决策前。
- 需要判断“是否可以安全地安装/更新/卸载插件”时。
- 需要处理 WSL + Windows 双端同步或隔离冒烟时。

先读完整版：`~/.dsh/dsh-optimization-consensus.md`。本技能只在上下文中放摘要；执行前必须打开完整文档核对可操作细节。

## 三条不可妥协底线

1. **先提醒用户**：可能中断运行中 agent/监听/会话的破坏性操作，先说明影响、风险、回滚方案，等用户确认。不默认替用户执行破坏性更新。
2. **运行中 agent 禁止热更**：update/install/uninstall 都会让磁盘新版本与内存旧版本混跑，导致在途请求崩溃或留下半成品；等 `agents.status === 'running'` 为空，或让用户在外部终端执行。
3. **先隔离兼容 + 冒烟，再落地**：在隔离 `DSH_HOME` 完成 dump-config、真实启动、插件 smoke、卸载复原；通过后才碰正式 profile。

## 子代理数量优化

- `maxParallelToolCalls` 只是“一步内未结算工具调用”的硬上限，不限制 background/continuable 子代理离开后的并发；不要只调大它来对付大任务。
- 实例：50 并行工具 + 139 子代理 → Node heap OOM。正确做法是**有界调度器**：并发 4–10、排队、深度 1–3。
- 设置显式并发上限：`maxConcurrentChildren` / `maxConcurrent`（建议 4–8）；超出的排队，不要同时全拉起。
- 限制 `maxDepth`（官方默认 3，0=禁止委派）；嵌套子代理需 allowlist，防指数 fan-out。
- 按任务分流：机械/只读用便宜模型 + `toolFilter` 只读；疑难/关键决策用高 effort。不要为并发而并发。
- 后台/continuable 用 `run_in_background: true`，然后用 `job_output` / `subagent_wait` / `list_agents` 收口；wait 设超时。
- 长任务用 `workflow` / 编排工具的 `parallel` / `pipeline`，避免一次 spawn 上百个裸子代理。
- 外部桥接代理控制空转超时、并发上限、权限天花板、secret 脱敏和 durable recovery。

## DSH/插件升级安全

升级前：

1. 记录当前精确版本、profile `package.json` / `pnpm-lock.yaml`、插件来源。
2. 读 release notes / `engines.dsh` / peerDependencies / `dsh.compat.*`。
3. GitHub Release 已发但 NPM 未发时等 NPM 制品；锁定精确版本 + integrity + commit。
4. 备份 profile / `DSH_HOME`、`package.json`、`cordis.patch.yml`、lockfile。
5. 确认无 running agent；无 agents 服务时 fail-open 但必须写 warning。

隔离冒烟：

- 临时 `DSH_HOME` 中 `dsh plugin add` → `--dump-config`（无重复 loader id / 坏 patch / 缺 bundle）→ 真实 `dsh web` / headless 启动 → 插件专属 smoke → remove → 再 dump 确认无残留。

回滚必须**恢复实际文件**：

- 只恢复 `package.json` pin 不够；必须 `pnpm install --no-frozen-lockfile` 把旧版真正装回 `node_modules`。
- `github:` 直装要保存 `beforeCommit`；失败时如实告知，别假装成功。
- “入口存在但 import 即抛”的坏版需要完整 trial boot / 真实启动验证，离线 checksum 覆盖不到。

升级后：

- 真实重启 + 跑原有测试/冒烟；用诊断页检查 load order、重复条目、多版本核心、peer 不匹配。
- 涉及测试、依赖增减、跨 major、安装生命周期脚本时，即使开启自动交付也回到人工 PR。
- 双端升级（WSL + Windows）：用另一端当操作手；先更新一侧并真实冒烟稳定后，再同步另一侧；绝对路径调用、分别备份、失败先回滚被更新侧。
- 双端升级不是“更新两个二进制”，而是同步完整状态（核心 + profile bundle + 插件源码/依赖 + presets + Skills + 开关状态）。只同步 dsh 会漏。
- 本次实战新增坑（详见本目录 `DUAL_END_UPDATE.md`）：
  - 不要用源码目录直链当正式安装；确认 `dsh` 指向完整 npm 包。
  - 插件/专家团必须连依赖一起同步；Windows 上重建 `node_modules`（junction/pnpm），不能直接复制 WSL symlink。
  - 插件 UI 依赖 `@deepseek-ai/dsh-client-ui-slots` 不会随 DSH 核心自动装，需额外安装并 `require.resolve` 验证。
  - Windows 从 WSL 调 `cmd.exe` 要显式 `cd /d C:\Users\<用户名>`，避免 UNC 路径坑；npm 的 `allow-scripts` 告警要检查。
  - `--dump-config` 通过 ≠ 真实启动通过；隔离 DSH_HOME 要放在原根目录下（相对链接会因 `/tmp` 失效）。
  - 磁盘版本 ≠ 运行中进程版本；确认无 running agent 后再重启。

## 提醒用户模板

升级前：

> 我要升级 DSH/插件：当前 `x` → 目标 `y`。会先备份，并在隔离 profile 里做兼容检查 + 真实启动 + 插件 smoke；不会动正在运行的 agent/监听。确认继续吗？

需重启：

> 这一步需要重启 `dsh web`，会中断当前监听/进行中的会话。我已准备好快照和回滚命令。确认执行？

无法保证安全：

> 隔离冒烟未通过 / 存在不可逆风险，我不自动执行。请你在外部终端运行我写好的 `apply` 脚本，并把输出贴回来；失败时运行 `rollback` 脚本。

## 边界与反例

- 本共识是安全底线，不是具体领域知识；纯教学/论文/GitHub 发布不需要提前展开。
- 不把“隔离冒烟通过”当成“可以热更运行中 agent”的许可。
- 回滚必须恢复实际文件，不能只改 package.json pin。
- 无法保证安全时，不自动执行；请用户在外部终端运行脚本并回贴输出。

## 2026 深度补强（Round 37）

### 1. 并发调度：白名单 + 配额 + 预检 + 超时四件套

- **具名 agent 白名单**：不只设 `maxDepth`，还要有 `allowed_agent_types` / 允许的专家团/人设；按模型/effort 分档给配额，并禁止调用方覆盖模型/effort（参考 [Codex issue #33437](https://github.com/openai/codex/issues/33437) 的 project-scoped policy profile）。
- **扇出前预检**：workflow / `parallel` 启动前先检查所有 worker/agent 引用存在、剩余配额、任务清单合法；缺一个就 fail-fast，不要跑一半才发现（参考 [Codex issue #23479](https://github.com/openai/codex/issues/23479)：主 agent 需要 capacity/status preflight，否则 spawn 失败会退化为“不回子代理”）。
- **三件硬限制**：每个 workflow / 编排至少设 ①最大 agent 数 ②最大阶段/轮次数 ③最大时长；只设 `maxTotalAgents` 而漏掉轮次/时长，仍可能长跑失控（参考 [Loom multi-agent 架构](https://github.com/teradata-labs/loom/blob/main/docs/architecture/multi-agent.md)：默认 20 agents / 10 stages / 5 rounds，且明确 `workflow timeout（待实现）`）。
- **反例**：`maxParallelToolCalls=50` + 不加白名单/配额，等于把 rate limit 和成本爆发的责任交给模型。Loom 的架构评审明确拒绝 “No limit / maximum parallelism, no blocking”，选择 `Limit=5` 以同时防死锁、压过 rate limit 并留 50% 余量。

### 2. 子代理/技能 description 是上下文成本，不是免费元数据

- `description` 会进入路由/上下文，必须一行说清“何时用 + 做什么”；长说明放正文/独立文档。
- 聚合描述超阈值会启动警告（[Claude Code 文档](https://code.claude.com/docs/en/sub-agents)：自定义 subagent descriptions 合计 > 15,000 tokens 时启动警告）；DSH 同类路由也应周期性审计目录中的 description 总长度。
- 反例：把整页指令塞进 description，导致每次路由都付一次上下文税。

### 3. 插件热更要按“同权代码”对待，不是按“可加载”对待

- 第三方防御审计明确：DSH 插件在宿主进程内以宿主权限运行；**安装/更新/篡改/持久化/热更路径没有签名/完整性/来源/确认门**；`!!js` 配置可以在加载时 RCE；安装后篡改零校验；`dsh plugin remove` 不清理 `!!js` 后门；用户 patch 热更约 15s 生效且不需要重启（来源：[deepseek-harness discussion #454](https://github.com/deepseek-ai/deepseek-harness/discussions/454) / [Fz0x00 audit repo](https://github.com/Fz0x00/deepseek-harness-plugin-security-audit)）。
- 动作：新插件先审源码 + 查 npm integrity/provenance + OpenSSF Scorecard / [dsh-plugin-certification](https://github.com/PerryLink/dsh-plugin-certification) 这类机器可查证据；不要只靠 `--dump-config` 或“能启动”就放行。
- 运行中 agent 禁止热更不只是“新旧版本混跑”问题，也是**权限边界**：不可信插件可能借 patch 热更路径静默生效，因此在正式环境保留最小 patch 面并记录 `cordis.patch.yml` 变更。

### 4. 隔离冒烟必须包含“污染测试 + 卸载复原 + 回滚冒烟”

- 在隔离 `DSH_HOME` 中，除 dump-config/启动外，至少再跑：①插件关键路径一次真实调用（如创建/读取/删除或对应 API smoke）②`plugin remove` 后 `--dump-config` 确认无 entry，且 `!!js`/后门型残留不会跨 restart 存在 ③用旧备份完整恢复后再次 boot + dump。
- 反例：只验证 exit code / dump 通过；可能漏掉“安装即投毒但启动正常”“卸载后后门仍在”的情况。

### 5. 回滚要恢复“锁文件快照 + node_modules 重建”，并区分 frozen 与 unfrozen

- 恢复旧 `package.json` 后，优先把旧 `pnpm-lock.yaml` / `package-lock.json` 快照一并恢复，然后 `pnpm install --frozen-lockfile` / `npm ci`：这才是“精确恢复旧版”的路径。
- 只有在没有 lockfile 快照、必须重新解析时才用 `--no-frozen-lockfile`；此时必须再做 `npm ls` / `require.resolve` / integrity 校验，确认真的是旧版，不能把“能安装”当“回滚成功”。
- [pnpm install 文档](https://pnpm.io/cli/install)明确指出 integrity 不匹配是硬失败（`ERR_PNPM_TARBALL_INTEGRITY`），不要用 `--update-checksums` 掩盖；这是供应链边界的守卫。
- [npm ci 文档](https://docs.npmjs.com/cli/v12/commands/npm-ci)：`npm ci` 会删除现有 `node_modules` 并按 lockfile 精确重建，是干净回滚的官方路径。

### 6. 双端同步用 manifest，不用“复制目录/mtime”

- 生成同步状态 manifest：两端 `dsh --version`、全局包/源码 commit、`package.json`+lockfile sha256、插件源码 commit、presets/Skills/开关状态、`require.resolve` 结果。
- 同步时按 manifest 逐项核验；任何一项不符就停在“未同步”，不要用 `cp -r` 补。
- 文件/工作树放在各自原生文件系统：WSL 侧用 `/home/...`，Windows 侧用 `C:\...`；不要在 `/mnt/c` 或 `\\wsl$` 之间维护 `node_modules`/git worktree（[Microsoft Learn: Working across file systems](https://learn.microsoft.com/en-us/windows/wsl/filesystems) 明确建议跨文件系统会损失性能且易混淆大小写/权限）。

### 7. 子代理/后台“已完成但占用槽位”要显式处置

- 已完成但仍有消息/队列的 child 可能继续占用 resident 槽位，使新 spawn 失败（[Codex issue #32353](https://github.com/openai/codex/issues/32353) 实证：completed agent 的 pending mailbox 会 pin 住线程槽，`.length` 值不能代表可用容量）。
- 动作：启动时记录 child 数，收口时确认 queue/消息被消费或显式关闭；项目级配额不能只按“running 数”判断，要按“包含 pending/queued 的保留槽位”判断。
- 反例：只看 `running` 数量以为有容量，实际 `spawn` 已 `agent thread limit reached`。

### 8. 提醒模板与审计留痕

- 升级/热更前多问一句：“这个插件/更新有没有签名、来源、许可证、已知漏洞？是否必须现在动？”；把答案写进操作记录。
- 每次隔离冒烟输出固定四行证据：dump-config 退出码、真实 boot 退出码、关键路径 smoke 结果、remove 后残留检查结果。缺一行就不能进正式 profile。

## 来源

DeepSeek Harness 官方文档/源码（https://github.com/dargonburn337845818/dsh-harness）、dsh-market（PR #199 / #19 / #98 / #186）、LCYLYM/dsh-plugin-compat-guardian、Luck9Star/dsh-plugin-subagents、leonardoxr/dsh-routed-subagent、y08lin4/dsh-multiagent-modes、weijiafu14/pi2dsh 与 tintinweb/pi-subagents。
