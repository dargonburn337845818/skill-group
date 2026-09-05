# G-Helper 轻量智能调度优化器

> 一个纯 PowerShell 的 Windows 后台守护：根据 **GPU 负载、CPU 负载、温度、是否在跑游戏/AI 程序**，自动在 G-Helper 的性能档（Silent / Balanced / Turbo / Custom）之间切换。
>
> 目标不是“更高频超频”，而是**按需调度**：日常安静，重负载才起飞。**不做超频**，只切换你在 G-Helper 里预先配置好的 BIOS 档位。

## 为什么需要它

- G-Helper 的 Turbo 是“固定高性能预设”，不是“智能档”，所以日常开着会一直起飞；
- 手动切档太依赖记忆；
- 本守护把“什么情况该切什么档”变成一条可观察、可验证的规则。

## 内存调度（已纳入）

- 监控 Windows 内存占用；
- 内存 >= 80%：自动调用 Mem Reduct `/clean:0x67`；
- 即将进入重负载且内存 >= 60%：先清理再切高性能档；
- 默认冷却 10 分钟，防频繁清理；
- 调度器需以管理员运行才能真正调用 Mem Reduct（注册自启已尝试 RunLevel=Highest）。

## 原理

```
每 5 秒：
  nvidia-smi 读 GPU 利用率/温度/功耗
  WMI 读 CPU 负载
  检查是否有游戏/AI 重负载进程
        ↓
  状态机（带持续时间和冷却，防抖动）
        ↓
  需要切档时 → 模拟 G-Helper 全局热键
              Ctrl+Shift+Alt+F16(Silent) / F17(Balanced) / F18(Turbo) / F19/F20(Custom)
```

- 热键层是因为 G-Helper **目前没有官方 CLI**（[issue #1](https://github.com/seerge/g-helper/issues/1)），但提供全局热键。
- 如果未来 G-Helper 支持 CLI，只需替换 `Send-GHelperHotkey` 这一个函数。

## 文件

| 文件 | 作用 |
|---|---|
| `GHelperSmartScheduler.ps1` | 核心守护脚本 |
| `GHelperSmartScheduler.config.json` | 阈值、进程名单、热键、模式映射 |
| `install.ps1` | 复制到 `%LOCALAPPDATA%` 并注册登录自启 |
| `uninstall.ps1` | 删除计划任务（可选清理数据） |

## 安装（在 Windows 侧执行）

1. 把整个 `optimizer/` 文件夹放到一个 Windows 可访问位置（例如 `C:\Users\<你>\Desktop\ghelper-scheduler`）。
2. 确保 **G-Helper 正在运行并开机自启**。
3. 在 PowerShell（普通用户权限即可）运行：
   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\install.ps1
   ```
4. 先试 **DryRun**，确认规则合理：
   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
     "$env:LOCALAPPDATA\GHelperSmartScheduler\GHelperSmartScheduler.ps1" -DryRun
   ```
   （按 `Ctrl+C` 停止；日志在 `%LOCALAPPDATA%\GHelperSmartScheduler\scheduler.log`）
5. 无异常后启动正式任务：
   ```powershell
   schtasks /Run /TN GHelperSmartScheduler
   ```

## 配置说明

打开 `GHelperSmartScheduler.config.json`：

| 字段 | 说明 |
|---|---|
| `heavyMode` / `balancedMode` / `idleMode` | 各状态切到哪个 G-Helper 档 |
| `thermalMode` | GPU 温度超过 `turboTemp` 时强制切到的档（防止持续高温） |
| `heavyGpuUtil` / `moderateGpuUtil` / `highCpuLoad` | 重负载判定阈值 |
| `idleGpuUtil` / `idleCpuLoad` / `idleTemp` | 空闲判定阈值 |
| `heavySustainSeconds` / `idleSustainSeconds` | 持续多少秒才切换（防抖动） |
| `minSwitchIntervalSeconds` | 两次切换最小间隔 |
| `heavyProcesses` | 进程名列表：命中即视为重负载（如 `python`、`blender`、游戏 exe） |
| `hotkeys` | G-Helper 各档热键；请与你 G-Helper 里设置的一致 |

## 推荐搭配（重要）

这个守护只负责“切档”，**每档内部的风扇/功耗/温度策略必须在 G-Helper 里配好**：

| 档位 | 推荐内部配置 |
|---|---|
| Silent | 默认静音即可（日常轻度） |
| Balanced | 自定义风扇：60°C 前安静，85°C 才接近全速；功耗默认/适中 |
| Turbo / Custom1 | 高功耗 + Dynamic Boost + 激进风扇；只在重负载时命中 |

## 验证方法

- 先 DryRun 看日志：`desired=` 是否和你预期一致；
- 再正式运行：观察切档是否在**真正重负载时**发生，轻负载是否保持安静；
- 用 G-Helper OSD（`Ctrl+Shift+Alt+O`）看温度/功耗，确认“风扇起飞 = 真的在跑重负载”。

## 边界与风险

- **依赖 G-Helper 运行**：G-Helper 未启动时不会切换（脚本会记录）；
- **模拟热键是间接控制**：如果 G-Helper 热键冲突或被其他程序占用，可能失效；
- **不做超频**：不碰 GPU 时钟/电压；只切 BIOS 预设档；
- **不是诊断工具**：它按规则调度，不能替代“先测量再调优”；
- 若 G-Helper 更新改变了热键/行为，需要同步更新 `hotkeys`。
