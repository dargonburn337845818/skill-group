# DSH 双端（WSL + Windows）交叉更新规范

> 本文档由 2026-09-05 实际双端升级踩坑蒸馏而来。
> 实战背景：`@deepseek-ai/dsh 0.1.1-rc.2 → 0.1.2-rc.1`；过程中曾误用本地源码 `0.1.3-alpha.1` 直链作为正式安装，最终回滚到官方 `0.1.2-rc.1` 并在 WSL / Windows 两侧完成核心 + 专家团 + presets + Skill 同步。
> 使用时机：本机同时存在 WSL 与 Windows 两套独立 DSH，需要升级核心、同步插件/专家团、修复启动或“某一端缺功能”时；也用于升级前预防性核对。

---

## 0. 一句话核心

**双端更新不是“更新两个 dsh 二进制”，而是同步一套完整状态：核心版本 + profile bundle + 插件源码/节点依赖 + presets + Skills + 开关状态。只同步二进制一定会漏。**

---

## 1. 不可妥协底线（沿用全局共识）

1. **先提醒用户**：会中断运行中 agent / web 的操作必须停下等确认。
2. **运行中 agent 禁止热更/重启**：磁盘新版 ≠ 内存新版；等没有 running agent 后由外部终端重启。
3. **先隔离兼容 + 冒烟，后落地**：`--dump-config` → 真实 boot → API/插件 smoke → 回滚验证。
4. **永远保留一个健康侧**：失败时不要两侧同时动，至少一侧可救援。
5. **真实回滚**：回滚不能只恢复 pin，必须恢复实际包体/符号链/备份文件。

---

## 2. 实战坑清单

### 2.1 核心安装坑

- **坑 1：把源码目录直链当正式安装**
  - 现象：`dsh` 符号链指向 `~/.dsh-versions/0.1.3-alpha.1/.../apps/cli`，而该目录只有一条指回 `$HOME/work/.dsh-update-smoke/src-0.1.3-alpha.1/` 的链接，不是完整 npm 包。
  - 后果：只要 smoke 目录清理/移动，下次启动就挂；`dsh --version` 可能正常，但“入口存在≠包完整”。
  - 动作：正式 `dsh` 必须指向完整 npm 包：`~/.dsh-versions/<version>/node_modules/@deepseek-ai/dsh/lib/bin.js`（或 `~/.npm-global/lib/node_modules/@deepseek-ai/dsh/lib/bin.js`）。
  - 边界：本地 `build` / `pnpm link` 只可用于开发调试，不可作为正式升级目标。

- **坑 2：side-by-side staged 目录没有验证完整包**
  - `npm install --prefix "$VER_DIR" "$NPM_SPEC"` 后只检查 `NEW_BIN` 存在不够；还要确认 `package.json`、`node_modules` 是真实安装，不是空目录/残留链接。
  - 本次 `~/.dsh-versions/0.1.3-alpha.1/` 就是空壳：只有 `node_modules/@deepseek-ai` 空目录，没有 package.json，切换后必然失败。

- **坑 3：Windows `cmd.exe` 从 WSL 调用时的 UNC 坑**
  - 现象：`cmd.exe /c "cd /d %USERPROFILE% && ..."` 在当前 WSL 工作目录下会输出：
    `'\wsl.localhost\Ubuntu\home\ru\work' 不是当前目录… UNC 路径不受支持。默认值设为 Windows 目录。`
  - 后果：当前目录被重置，命令仍可能执行，但日志混乱、路径不可控。
  - 动作：显式用 `cd /d C:\Users\<用户名>`（或目标绝对 Windows 路径），不要依赖 `%USERPROFILE%` 从 WSL 传入。

- **坑 4：Windows npm 提示 `allow-scripts`**
  - 现象：`npm install -g` 输出 `npm warn allow-scripts ... Run npm approve-scripts ...`。
  - 后果：部分 postinstall / 原生模块脚本可能没执行，后续启动才暴露。
  - 动作：升级后检查 `npm approve-scripts` 状态，或确认包不需要脚本；不要把“安装完成”当“脚本执行完成”。

- **坑 5：升级前没有完整备份 Windows 全局包**
  - 现象：只备份了“旧版本记录”或 `package.json`，没有旧全局包体。
  - 后果：Windows 回滚只能重新联网 `npm install -g old`，离线/网络故障时无法恢复。
  - 动作：Windows 全局执行 `npm install -g` 前，先把 `/mnt/c/Users/<用户名>/AppData/Roaming/npm/node_modules/@deepseek-ai/dsh` 完整复制到 WSL 侧备份目录（作为离线回滚源）。

### 2.2 插件 / 专家团同步坑

- **坑 6：只同步核心，不同步专家团/插件/preset**
  - 现象：Windows 核心升到新版本，但没有 `dsh-skill-vault`、`dsh-skill-router`、`dsh-graded-mode`，`~/.dsh/skill-vault`、`skill-router` 不存在，preset 缺 Skill 目录和运行时文件。
  - 后果：一端“有专家团”，另一端“只有空壳”，功能不对齐。
  - 动作：把以下作为一套状态同步：
    - `profiles/web/package.json`（bundle 列表）
    - 插件源码目录（`C:\Users\<用户名>\work\dsh-skill-vault`、`dsh-skill-router`）
    - `dsh-graded-mode` tgz / 安装产物
    - `.agent-presets/*` 运行时与 Skill 目录
    - `~/.dsh/skill-vault/enabled.json`、`~/.dsh/skill-router/reset.done`
    - `profiles/node_modules` / `profiles/web/node_modules` 依赖链接

- **坑 7：把 WSL 的 `node_modules` 符号链接直接复制到 Windows**
  - 现象：WSL 用相对/绝对 `ln -s` 建的解析链，复制到 NTFS 后变成悬空或指向 `\\wsl.localhost\...`。
  - 后果：Windows Node 无法解析 `cordis`、`schemastery`、`@deepseek-ai/dsh-tools` 等。
  - 动作：Windows 侧必须重建依赖，用 `pnpm install` / `npm install`，或为插件源码创建真正的 Windows junction：
    ```
    mklink /J "C:\Users\<用户名>\work\plugin\node_modules\cordis" "C:\...\node_modules\cordis"
    ```
    并验证目标解析到 Windows 路径，而不是 `\\wsl.localhost\...`。

- **坑 8：漏装 `@deepseek-ai/dsh-client-ui-slots`**
  - 现象：`dsh-skill-vault` / `dsh-skill-router` 的 peer/metadata 引用 `@deepseek-ai/dsh-client-ui-slots`，但 DSH 官方 npm 包并不自动携带它；只在源码 monorepo 里存在。
  - 后果：客户端 UI slots 注入缺失（BLOCKER）；`--dump-config` 未必报错。
  - 动作：`npm view @deepseek-ai/dsh-client-ui-slots version` 确认可从 npm 安装；随后安装到：
    - 插件源码 `node_modules`
    - `profiles/web/node_modules`
    - `profiles/node_modules`（共享层）
  - 验证：在插件目录执行 `require.resolve('@deepseek-ai/dsh-client-ui-slots')` 成功，不能只看 `dump-config`。

- **坑 9：Windows 共享层链接目标仍指向 WSL**
  - 现象：`fsutil reparsepoint query ...` 显示 target 为 `\\wsl.localhost\Ubuntu\...`，说明 junction/symlink 指向 WSL 路径而非 Windows 路径。
  - 动作：删除后用 `mklink /J` 指向 Windows 本机路径；用 `fsutil reparsepoint query` 确认目标以 `C:\` 开头。

### 2.3 预设 / Shell 坑

- **坑 10：Windows 默认还在用 PowerShell**
  - 现象：`router-standard` / `router-spec` / `spark-lite` / `liangshen` 中有 `tool-pwsh`。
  - 动作：如需 Git Bash，为预设增加 `gitbash-executor.mjs`（或 `custom-bash`）并禁用 `tool-pwsh`；WSL 侧保留原生 bash-sandbox。
  - 边界：Git Bash / MSYS 在 Windows 上通常不声明 sandbox mode，文件沙箱约束会变弱，这是已知取舍。

### 2.4 验证 / 收尾坑

- **坑 11：`--dump-config` 通过 ≠ 真实启动通过**
  - 本次对 Windows 只有 `dump-config` 时，真实 boot 曾失败（exit 1 / exit 255）；必须做真实 boot + HTTP readiness + API smoke。
  - 动作：独立端口启动 `dsh web --no-open --port 3090`，等 HTTP 返回（新版返回 401 token 也说明服务已起来），再调 `/skill-router/api/status` 等端点。

- **坑 12：隔离 `DSH_HOME` 放在 `/tmp` 导致相对链接失效**
  - 现象：profile `node_modules` 是相对 `~/.dsh` 定位到 `~/work` 的链接；复制到 `/tmp/dsh-isolated` 后全部失效。
  - 动作：隔离复制必须放在 `$HOME/` 下（与原路径同根），或先解析绝对路径再复制。

- **坑 13：磁盘已切换，运行中进程仍是旧版**
  - 现象：`dsh --version` 输出的可能是磁盘新版本，但当前 agent 进程（PID 1164）是切换前启动的，内存仍为旧版。
  - 动作：把“磁盘版本”和“运行中进程版本”分开记录；确认无 running agent 后再重启 `dsh web`，不能默认自动重启。

- **坑 14：`profiles/node_modules` 残留 broken symlink**
  - 现象：WSL 约 29 个、Windows 约 6 个悬空链接，多数指向已删除的 `$HOME/deepseek-harness` 或旧 client 包。
  - 动作：不要一律当成 BLOCKER；先确认运行时是否引用。暂时无害可保留，稳定后另开清理。

- **坑 15：机器本地配置不要强行同步**
  - 现象：WSL `cordis.patch.yml` 有 `qwen-local`，Windows 是 `local-llama` / `radeon`。
  - 动作：本地模型/provider/端口/凭据按机器保留，不纳入“双端同步”范围；强行复制会覆盖另一端的本机配置。

---

## 3. 推荐操作顺序（双端交叉更新）

```text
0. 记录两端：版本、npm prefix、DSH_HOME、profile bundle、preset 列表、插件源码路径。
1. 预先准备：
   - 备份两端 profile / .agent-presets / plugins / patch / config / settings
   - 备份两端全局 DSH 完整包体（离线回滚）
   - 确认无 running agent，停止目标端 web
2. 选择一端作为被更新端（建议先 WSL，稳定后再同步 Windows）
   - 用 side-by-side 安装到 ~/.dsh-versions/<version>
   - 验证 staged 包完整（package.json + lib/bin.js + node_modules 非空）
   - 备份、切换符号链、--dump-config、真实 boot smoke
   - 跑一轮受控任务/API smoke
   - 失败：立即回滚该端，不要继续同步另一侧
3. 同步插件/专家团到另一端：
   - 复制源码/preset/skill/开关状态
   - 在 Windows profile / 插件源码中重建依赖（pnpm install / junctions）
   - 安装缺失的 @deepseek-ai/dsh-client-ui-slots
   - 验证 require.resolve 与 dump-config
4. 重复此端真实 boot + API smoke
5. 最后才同步操作手端（若操作手端也要升级）
6. 两端稳定后，重启运行中的 DSH web，确认新版本真正生效
7. 记录回滚备份路径与遗留事项
```

---

## 4. 验证清单

- [ ] 两端 `dsh --version` 与目标一致
- [ ] 两端 `dsh --profile web --dump-config` 退出 0 且无 duplicate loader entry / missing bundle
- [ ] `readlink -f` 确认 WSL `dsh` 指向完整 npm 包（不是源码直链）
- [ ] Windows `dsh` shim 存在且版本正确
- [ ] 插件目录 `require.resolve('@deepseek-ai/dsh-client-ui-slots')`（以及其他 peer）成功
- [ ] Windows `profiles/node_modules` 的 junction target 以 `C:\` 开头（`fsutil reparsepoint query`）
- [ ] 真实启动：独立端口 HTTP 可响应（401 亦表示服务已起来）
- [ ] API smoke：`/skill-router/api/status`、`/skill-vault/api/teacher/status` 等返回 200
- [ ] 预设：目标平台不带 pwsh / 使用期望 shell
- [ ] 备份：旧全局包体完整存在，可离线回滚
- [ ] 运行中进程版本 = 磁盘版本（或已确认待重启）

---

## 5. 回滚要点

1. 只回滚被更新端；不要同时动另一侧。
2. Linux 侧：恢复符号链到旧全局包或旧 `~/.dsh-versions` 包；确认 `readlink -f` 为完整包。
3. Windows 侧：优先从备份目录复制旧全局包（离线），其次才 `npm install -g old`。
4. 恢复 profile / presets / plugins / patch 后必须重新 `--dump-config` + 真实 boot。
5. 若某端只更新了插件/预设，按同一套“实际文件恢复”原则回滚，不能只改 package.json pin。

---

## 6. 反例 / 边界

- “能启动”不代表“功能完整”：本次 `0.1.2-rc.1` 启动成功，但专家团 UI 依赖缺 `dsh-client-ui-slots`，需要额外安装。
- “版本号对”不代表“文件完整”：源码直链 `0.1.3-alpha.1` 的 `dsh --version` 可显示，但目录不是完整包。
- “dump-config 通过”不代表“真实 boot 通过”：Windows 曾多次 dump 通过但真实启动失败。
- “npm install 成功”不代表“allow-scripts 已执行”：必须检查 `approve-scripts` 或启动验证。
- “一侧稳定”不能作为立即同步另一侧的理由：要等被更新端真实任务/API smoke 稳定后再同步。
- “同步配置”不能覆盖机器本地配置：模型/provider/凭据/端口保留差异。

---

## 7. 来源

- 实战会话记录：`~/.dsh/sessions/--home-ru-work--/session-c4c799b4-abf5-4e17-b0fd-1c6834ceb1ea/session.v2.jsonl.zstd`（WSL/Windows 检修与同步全过程）
- 更新计划与脚本：`$HOME/work/.dsh-update-smoke/UPGRADE_NOTES.md`、`safe-update-dsh.sh`、`rollback-safe-update.sh`
- 备份目录：`$HOME/.dsh-wsl-win-sync-backup-20260905-123528/`、`$HOME/.dsh-upgrade-backup-20260905-*`
- 官方 npm 包信息：`@deepseek-ai/dsh@0.1.2-rc.1`、`@deepseek-ai/dsh-client-ui-slots@0.0.1-rc.1`
