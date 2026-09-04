# DSH 优化共识（子代理数量 / 并发边界 / 安全运维）

> 本文档是从 DeepSeek Harness（`deepseek-ai/deepseek-harness`）官方源码、subsystem 文档与 Agent Notes 中蒸馏出的可执行共识。
> 本目录配套 `apply_limits.py` / `rollback_limits.py`，用于在外部终端安全落地子代理/并发上限。
> 现有 `~/.dsh/dsh-optimization-consensus.md` 是机器级短版；本文是其带来源、带数值论证的完整版。

## 0. 优先级与纪律

1. 用户直接指令 > 项目指令 > 本共识 > 默认习惯。
2. **破坏性操作先提醒用户**：升级、改 bundle、重启、改 `cordis.patch.yml`、热更插件，都必须先说明影响/回滚并等确认。
3. **运行中的 agent 禁止热更**：磁盘新版 + 内存旧版会新旧混跑。
4. **先隔离兼容 + 冒烟，后落地**：隔离 `DSH_HOME` 中 `--dump-config` → 真实启动 → 插件 smoke → 回滚验证。

---

## 1. 爬取到的官方机制

### 1.1 有多个不同的“上限”，不要只调一个

DSH 不是单一“子代理数量”开关，而是分层限流：

| 层 | 插件 / 配置键 | 官方默认 | 作用 |
|---|---|---|---|
| 同一步的工具调用池 | `agent-loop` → `maxParallelToolCalls` | `10` | 一个 assistant step 内同时未结算的并行安全调用上限（`1` = 串行） |
| 后台 Task / 子代理任务 | `jobs` → `maxConcurrentJobsPerOwner` | `10` | 每个精确 owner 的 running+stopping 后台任务上限；`stopping` 也占名额 |
| workflow 并发子代理 | `workflow-worker-thread` → `maxConcurrentAgents` | `0` → 自动 `min(16, cores-2)` | 脚本内 `agent()` 并发上限 |
| workflow 总子代理数 | `workflow-worker-thread` → `maxTotalAgents` | `1000` | 一次运行的运行跳闸（runaway-loop backstop） |
| workflow 单批条目 | `workflow-worker-thread` → `maxItemsPerCall` | `4096` | 一次 `parallel()` / `pipeline()` 接受的条目数 |
| workflow 脚本同步超时 | `workflow-worker-thread` → `syncTimeoutMs` | `5000` | worker 初始同步切片 VM 超时 |
| workflow 强制结算宽限 | `workflow-worker-thread` → `disposeGraceMs` | `5000` | 取消后脚本不结算时的强制终止窗口 |
| 委派深度 | `tool-subagent` → `maxDepth` | `3`（`0` 禁止委派） | 递归树绝对深度上限；持久化且单调 |
| 后台任务等待/收集 | `tool-jobs` / `job_output` | — | 用于收口，不增加硬上限 |
| Ralph 轮次 | `tool-ralph` → `maxRounds` | 包默认 `256`，base 组合实际 `64` | 每个 fresh-agent 轮次一个全新子代理 |
| PTC 子调用池 | `tools` → `maxParallelSubCalls` | `10` | `run_code` 内 SDK 子调用重叠上限 |

### 1.2 关键语义（决定“为什么这么限”）

- **`maxParallelToolCalls` 只管“未结算的工具调用”**。后台/可继续子代理在启动调用返回后就已经离开该池；它们留下的 live Activation、进程、持久化会话不受这个池限制。因此，只调大 `maxParallelToolCalls` 无法限制后台/continuable 子代理的长期并发。
- **`maxDepth` 是持久化且单调的**。`SessionHeader.delegationDepth` 是权威值，运行时只能加深、不能降低；恢复后的子代理不会重新变成顶层。所以“重启后再派一次”不能绕过深度预算。
- **可继续（continuable）子代理不是 `SubagentRun`，也不是 Task**。它有持久化 Session、至多一个进程内 Activation、自己的 FIFO inbox；`send_message` 跟进，结算通知独立送到父会话。限制它的主要手段是使用侧约定（不要无限养 resident child），而不在单个工具池上限内。
- **`list_agents` / `listDescendants` 没有分页或数量上限**。官方明确列为 deferred：返回稳定排序的完整集合。长期 parent + 大量持久化 child 会让列表成本线性增长，应在使用侧限制 child 数量，而不是依赖列表分页。
- **workflow 的 `maxTotalAgents` 可被调用方降低、不能提高**；`workflow` 工具本身不暴露该参数，Ralph 固定脚本通过 `maxTotalAgents` 传入轮次上限。超限是 fatal workflow error，不是静默 `null`。
- **后台任务准入按 exact owner 分桶**：`running`/`stopping` 占名额，终态不占；无 owner 任务共享独立服务桶。`job_kill` 后不能立即释放容量，要等 producer `done` 结算。
- **子代理并发安全由 `isConcurrencySafe: () => true` 声明**：同一 assistant 消息里的多个 subagent 调用会在 `maxParallelToolCalls` 滚动池内重叠，结果仍按模型顺序提交。因此并发不是“能不能真并行”的问题，而是“会不会超出预算”的问题。

### 1.3 官方对数量的立场（从 Agent Notes 摘录）

- **并行 subagent 委派**：同级委派并发安全；容量控制留在调度器，`maxParallelToolCalls` 限制单步未结算调用数量；后台/可继续启动即释放池位，不受该上限约束。
- **有界后台任务准入**：模型可以跨工具调用/后续轮次反复启动后台任务，`maxParallelToolCalls` 管不到它们；因此 `LocalJobRegistry` 增加 `maxConcurrentJobsPerOwner`，默认 `10`，满了就 fail-closed 拒绝并指导 `job_kill`。
- **人设/工具过滤/深度**：`maxDepth` 是绝对树上限；顶层深度 0，子代理 +1；默认 `3` 是“较小有限值”，允许 root 加三代后代。工具在上限处仍可见，以便运行时拒绝而不是配置期隐藏。
- **动态 workflows**：脚本扇出多个子代理，由 `maxConcurrentAgents`、`maxTotalAgents`、`maxItemsPerCall` 限制；fatal errors 不消融为 `null`。
- 已知问题：社区/实测中 `maxParallelToolCalls=50` + 139 个子代理会导致 Node heap OOM。这不是“官方默认不够大”，而是缺少有界调度与总量兜底。

---

## 2. 本机推荐值（20 核 / ~7.4 GB RAM）

> 原则：内存/上下文比 CPU 更稀缺；并发上限用于防 OOM 与失控，不是驱动速度。若机器/预算不同，按比例调整。

| 配置 | 当前默认 | 推荐 | 理由 |
|---|---|---|---|
| `agent-loop.maxParallelToolCalls` | 10 | **8** | 单步同时跑 8 个未结算工具/前台子代理已足够；保守防内存峰值 |
| `jobs.maxConcurrentJobsPerOwner` | 10 | **8** | 后台 Task 每 owner 最多 8 个 running/stopping |
| `workflow-worker-thread.maxConcurrentAgents` | 自动 ≈16 | **4** | 7.4GB 下 16 个并发子代理上下文/进程会明显吃内存；4 是稳健起点 |
| `workflow-worker-thread.maxTotalAgents` | 1000 | **128** | 防一次性跑上千个子代理；128 对大多数 audit/migration 足够 |
| `workflow-worker-thread.maxItemsPerCall` | 4096 | **1024** | 单批扇出 1024 已是大任务；再大应拆阶段 |
| `tool-subagent.maxDepth` / `tool-subagent-fork.maxDepth` | 3 | **2** | 允许 root + 2 层子代理，阻止指数级深层 fan-out |
| `tool-ralph.maxRounds` | 64（base 已设） | 保持 64 | 已有界；不要因为“想多跑几轮”改大 |
| `list_agents` 数量 | 无界 | 使用侧限制 | 官方没有分页；长期大量 child 会让列表成本线性增长 |
| `allowParallelInProgress` | `true`（preset 已设） | 保持 `true` | 子代理/后台并行时有多个 in_progress 是正当的 |

若你主要跑轻量任务（编译、单文件修复），可以再收紧：`maxConcurrentAgents=2`、`maxTotalAgents=64`、`maxDepth=1`。
若你确实需要大批量一次性审计且内存充足（≥16GB），可以放宽到 `maxConcurrentAgents=6~8`、`maxTotalAgents=256`，但不要超过 `maxParallelToolCalls=12`。

---

## 3. 应用方式（安全步骤）

当前会话工作区是只读的（`~/.dsh` 在沙箱中只读），所以不自动改 DSH 配置。请按下面步骤在**外部终端**落地：

1. **备份**：脚本会为每个目标文件生成 `.bak-<timestamp>`；也可先手动 `cp -a ~/.dsh ~/.dsh.backup-$(date +%Y%m%d)`。
2. **先隔离冒烟**（推荐）：
   ```bash
   export DSH_HOME=/tmp/dsh-isolated
   mkdir -p "$DSH_HOME"
   # 复制 profile 与 preset（或按模板重建）
   cp -a ~/.dsh/profiles "$DSH_HOME/"
   cp -a ~/.dsh/.agent-presets "$DSH_HOME/"
   cp $WORKSPACE/skills/dsh-optimization-consensus/apply_limits.py "$DSH_HOME/"
   python3 "$DSH_HOME/apply_limits.py"
   dsh --profile web --dump-config       # 必须成功且无 duplicate loader entry id
   # 真实启动一次 headless 或 web smoke，观察无启动错误
   ```
3. **正式 profile 应用**：
   ```bash
   python3 $WORKSPACE/skills/dsh-optimization-consensus/apply_limits.py
   dsh --profile web --dump-config
   ```
4. **重启 DSH**（外部终端，不要在 running agent 会话里做）：等没有 running agent 后重启 `dsh web`。
5. **观察**：跑一个包含 workflow / 多个 subagent 的任务，确认 `maxConcurrentAgents`、`maxTotalAgents`、`maxDepth` 生效且没有 OOM。
6. **回滚**：
   ```bash
   python3 $WORKSPACE/skills/dsh-optimization-consensus/rollback_limits.py
   ```
   然后重启 DSH 并再次 `--dump-config`。

### 3.1 脚本实际改动

`apply_limits.py` 使用行级、注释保留的修改：

- `~/.dsh/profiles/web/cordis.patch.yml` 新增/更新：
  ```yaml
  - id: agent-loop
    config:
      maxParallelToolCalls: 8
      agents: []
  - id: jobs
    config:
      maxConcurrentJobsPerOwner: 8
  ```
- `~/.dsh/.agent-presets/{router-standard,router-spec,liangshen}/agent.cordis.yml` 的 `delegation` 组中：
  - `tool-subagent` / `tool-subagent-fork` 增加 `maxDepth: 2`
  - `workflow-worker-thread` 增加：
    ```yaml
    maxConcurrentAgents: 4
    maxTotalAgents: 128
    maxItemsPerCall: 1024
    ```

注意：`tool-subagent` 等行位于 agent preset 的 scoped `delegation` group，普通 profile `cordis.patch.yml` 不一定覆盖得到；因此脚本同时改所有当前存在的 preset（`router-standard`、`router-spec`、`liangshen`）。如果你的实际使用 preset 不在这个列表，请手工把同样键加入对应 `agent.cordis.yml`。

---

## 4. 使用侧纪律（不依赖配置也要遵守）

1. **不为并发而并发**：独立且量大的任务用 `workflow` / `parallel` / `pipeline`；一两项委派用普通 `subagent`。
2. **后台/continuable 要收口**：启动后明确知道何时 `job_output` / `send_message` / `interrupt_agent` 收口；不长期养 resident child。
3. **限制深度和权限**：子代理的权限在创建时固定；`maxDepth` 是防指数 fan-out 的机械底线。
4. **按复杂度分流**：机械/只读用便宜模型 + `toolFilter` 只读；关键决策用高 effort；不要用“多开几个子代理”替代更好的 prompt。
5. **监控成本**：DSH 目前没有 token/货币编排预算；目标可用 `maxGoalRounds`，Ralph 用 `maxRounds`，workflow 用 `maxTotalAgents`。给长任务设机械上限。
6. **`list_agents` 不是 delete/limit API**：无分页、不删除；child 多时需要手动/通过 `send_message` 或清理策略收敛。

---

## 5. 来源

官方（本机安装 `@deepseek-ai/dsh@0.1.1-rc.2` 与 cloned master 源码）：

- DeepSeek Harness 仓库：https://github.com/deepseek-ai/deepseek-harness
- `docs/subsystems/workflow.zh.md`、`docs/subsystems/subagent.zh.md`、`docs/config-catalog.zh.md`
- `.agents/notes/implemented/feature/2026-08-09-parallel-subagent-delegations.zh.md`
- `.agents/notes/implemented/feature/2026-07-10-parallel-tool-call-execution.zh.md`
- `.agents/notes/implemented/feature/2026-07-12-subagent-persona-tool-filter-and-depth.zh.md`
- `.agents/notes/implemented/feature/2026-07-05-dynamic-workflows.zh.md`
- `.agents/notes/implemented/bug-fix/2026-08-11-bounded-background-job-admission.zh.md`
- `.agents/notes/implemented/feature/2026-07-22-durable-subagent-catalog-and-list-agents.zh.md`
- 包 README：`dsh-workflow-worker-thread`、`dsh-tool-subagent`、`dsh-tool-ralph`、`dsh-agent-loop`、`dsh-jobs-local`

社区（机器级共识已引用，供交叉验证）：

- https://github.com/deepseek-ai/deepseek-harness/discussions/754 — 大量子代理导致 JS heap OOM
- https://github.com/Luck9Star/dsh-plugin-subagents
- https://github.com/y08lin4/dsh-multiagent-modes
- https://github.com/leonardoxr/dsh-routed-subagent
- https://github.com/weijiafu14/pi2dsh
- https://github.com/tintinweb/pi-subagents
