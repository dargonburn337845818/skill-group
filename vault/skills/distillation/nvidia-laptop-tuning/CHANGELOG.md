# Changelog

## 0.6.0 (2026-09-05)

- G-Helper 一键保守风扇预设：读取并备份 `%APPDATA%\GHelper\config.json`，写入 Silent/Balanced 与 Turbo 两套保守风扇曲线，默认不改功耗限制，可一键回滚。
- OSD 弹窗消除：为 G-Helper 配置写入 `disable_osd=true` 并重启，切档不再弹透明小窗。
- 新增入口：`应用GHelper预设.bat`（一键应用）+ `optimizer/ghelper-apply-presets.ps1`（可预览/回滚）。

## 0.5.0 (2026-09-05)

- UI 重做：StyleKit 铅笔手绘风（Sketch Style）——纸张米色 #F5F0E8、铅笔灰 #2C2C2C、不规则虚线边框、楷体手写感、低饱和强调色、交叉线阴影。
- 参数图形化：新增实时趋势图（GPU/CPU/内存/温度/功耗），指标卡与调度状态更直观。
- 流畅性：自动刷新改后台线程，避免每 5 秒阻塞 UI；按钮保留短促铅笔 hover/pressed 反馈。
- 调度器与 A/B：保持控制面不变；status-report 增加 CPU 负载；A/B 真实测试待执行。
- 新 EXE：NvidiaTuningPanel.exe（0.5.0，仅单入口）。
- 调度器修复：持续判定从“轮询次数”改为按秒累计；修复合入前实际需要 150s 才切档的问题；修复后 160s 真实切换到 Turbo。
- 真实 A/B 试点：B=104.8 it/s vs A=93.4 it/s（含热漂移，未下结论）；原始数据见 `audit/real-ab-data/` 与 `audit/real-ab-pilot.md`。


## 0.4.0 (2026-09-05)

- 启动行为：默认显示主窗口（不再静默隐藏）；关闭窗口仍最小化到托盘。
- 修复：`FlatAppearance.BorderColor` 不能设为 `Transparent` 导致的启动崩溃；现仅保留 `NvidiaTuningPanel.exe` 一个入口。
- UI 产品化：按 ui-aesthetics-design 重构面板视觉（Windows 原生工具风，去掉模板化彩色卡片/深色侧栏+白卡，统一间距与 2-3 档层级）。
- 暗色模式：浅/暗主题切换 + 注册表持久化（HKCU\Software\NvidiaTuningPanel\DarkTheme），默认跟随系统；双主题对比度达标。
- 图标与控件：8 个操作按钮 + 主题按钮使用 Segoe MDL2 图标；6 个指标卡自绘 MetricIcon；托盘 32x32 Power 图标；全按钮 hover/pressed/focus 状态。
- A/B 验证基建：新增 `docs/ab-protocol.md`（负载/变量隔离/样本量/指标/判定规则）与 `optimizer/ab-measure.ps1`（只观测、CSV/JSON 落盘、DryRun）。
- 新 EXE：`NvidiaTuningPanel.exe` / `NvidiaTuningPanel_v3.exe`（0.4.0，包含本轮 UI）。
- 边界：真实 A/B 负载执行待用户本机运行；UI 实机视觉确认待用户。

## 0.3.0 (2026-09-05)

- 核心迭代：按专家共识收窄到“G-Helper 性能档 + 内存清理”为主控制面，CPU/GPU/内存/磁盘统一观测。
- UI 产品化：自定义 PillBar 进度条、去 emoji/去 AI 味、更克制的配色与间距。
- 新 EXE：NvidiaTuningPanel_v3.exe（托盘后台版）。

## 0.2.5 (2026-09-05)

- EXE 增加系统托盘后台模式：启动即隐藏到托盘，双击/右键菜单可用。
- 托盘菜单：打开面板 / 启动调度 / 停止调度 / 刷新状态 / 退出。
- 关闭窗口默认最小化到托盘，只能从托盘菜单退出。

## 0.2.4 (2026-09-05)

- 指标卡片内部改为 TableLayoutPanel，修复数值/进度条重叠；指标区加高。
- 操作按钮自动换行，避免挤出屏幕；侧栏标题/头部重排，减少裁切。
- 新 EXE 以 NvidiaTuningPanel_v2.exe 提供（旧 EXE 被占用时无法覆盖）。

## 0.2.3 (2026-09-05)

- 数据看板产品化：2x3 指标卡片 + 强调色条 + 图标化操作按钮 + Tooltip。
- 窗口自动贴合屏幕，避免高 DPI 下右列被切出屏幕。

## 0.2.1 (2026-09-05)

- EXE UI 重做：深色侧栏 + 圆角卡片 + 扁平按钮 + 日志区，按 ui-aesthetics-design 检查。
- 启用 DPI 感知（SetProcessDPIAware + app.manifest PerMonitorV2），改善高 DPI 下字体模糊。

## 0.2.0 (2026-09-05)

- 内存纳入智能调度：Mem Reduct 自动清理（>=80% 或重负载前 >=60%），10 分钟冷却。
- 调度器/状态报告增加内存占用与上次清理时间显示。
- 注册自启任务尝试 RunLevel=Highest，让后台也能调用 Mem Reduct。

## 0.1.9 (2026-09-05)

- D:\<工具目录> 增加图形面板 NvidiaTuningPanel.exe（WinForms，中文按钮+日志反馈）。
- 集成 Mem Reduct 按钮（/clean:0x67，管理员自动提示）。
- 新增优化说明.txt，说明具体优化项；EXE 内含“查看优化说明”按钮。

## 0.1.8 (2026-09-05)

- D:\<工具目录> 增加中文一键面板：NVIDIA调优面板.bat + 启动/停止/状态/优化/回滚/自启中文入口。
- 新增 status-report.ps1，查看状态时反馈当前档位/GPU/温度/进程数。
- 实测：中文菜单、启动→状态→停止全链路通过。

## 0.1.7 (2026-09-05)

- 部署到 D:\<工具目录>：新增 start/stop/status/install/optimize/restore 一键入口。
- optimizer 增加 register-scheduler-task.ps1，自启任务直接指向 D:\<工具目录> 路径。
- 实测：start->status->stop 全链路通过；本地优化 backup/apply/restore 通过。

## 0.1.6 (2026-09-05)

- 新增 local-optimizer/：本地电脑设置一键优化脚本（安全版，默认 dry-run，写前备份，可回滚）。
- 实测：-Test 预检通过；GameDVR/GameMode 备份→应用→恢复→校验通过；未触碰电源计划与 .wslconfig。

## 0.1.5 (2026-09-05)

- 新增 optimizer/：G-Helper 轻量智能调度守护（PowerShell，基于热键自动切档，不超频，支持 DryRun）。

## 0.1.4 (2026-09-05)

- 修正 G-Helper 策略：不再建议日常常驻 Turbo；改为 Balanced/Custom 安静曲线 + 重负载临时 Turbo。

## 0.1.3 (2026-09-05)

- 新增 R12：NVIDIA Profile Inspector 深度参数（Power/LowLatency/帧率上限/Shader Cache）。
- 新增 R13：8GB VRAM 的 PyTorch/AI 调优（TF32、BF16、显存分配器、DataLoader）。

## 0.1.2 (2026-09-05)

- 新增 R11：G-Helper 参数调优（性能/风扇/功耗，不超频）。
- 更新 SKILL.md 规则速查；更新 SOURCES.md G-Helper 来源。

## 0.1.1 (2026-09-05)

- 新增 R0：NVIDIA 616.56 已知闪屏 Bug 与 GeForce Hotfix 616.86 修复路径。
- 更新 SKILL.md 触发条件与第一步检查；更新 SOURCES.md 来源表。
- 补充结论：不要用非官方“鸡血/魔改”驱动；官方热修复 + 参数调优更稳。

## 0.1.0 (2026-09-05)

- 首版：英伟达笔记本调优 Skill。
- 内容：SKILL.md 可执行摘要、CONSENSUS.md 完整规则与边界、SOURCES.md 来源表、manifest.json、2 个验证模板、1 份专家讨论记录。
- 来源：NVIDIA 官方驱动/控制面板/Max-Q/App/CUDA on WSL、Microsoft WSL 配置文档、ASUS FX608LM 官方规格、第三方旁证、本机实测。
- 专家：John Carmack / Brendan Gregg performance 讨论 R1（风格/方法论参考，非本人原话）。
- 质量：蒸馏自检 7/7；具体 Skill Lift 需后续真实任务 A/B，未虚报。
