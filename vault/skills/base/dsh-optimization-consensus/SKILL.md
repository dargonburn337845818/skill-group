---
name: dsh-optimization-consensus
description: DSH 运维与优化共识——子代理数量有界、升级插件先隔离兼容+冒烟、运行中 agent 禁止热更、破坏性操作先提醒用户并准备回滚。用于任何 DSH/插件升级、子代理调度、热更新或重启决策前。
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

## 来源

DeepSeek Harness 官方文档/源码（https://github.com/dargonburn337845818/dsh-harness）、dsh-market（PR #199 / #19 / #98 / #186）、LCYLYM/dsh-plugin-compat-guardian、Luck9Star/dsh-plugin-subagents、leonardoxr/dsh-routed-subagent、y08lin4/dsh-multiagent-modes、weijiafu14/pi2dsh 与 tintinweb/pi-subagents。
