# HANDOFF — 系统综合调度器 / 调优面板

> 供新会话接管。当前项目版本 **0.6.0**。实际运行在 `D:\<工具目录>`（Windows 侧），知识/源码/文档镜像在 `skills/nvidia-laptop-tuning`。

## 一、目标（北极星）

为一个 Windows + ASUS TUF FX608LM 用户（RTX 5060 Laptop 8G / 16GB 单通道 / WSL2）做一套**轻量、系统综合、可验证**的调度与优化工具：
- 自动按负载调度 G-Helper 性能档（Silent/Balanced/Turbo/Custom）
- 自动内存调度（Mem Reduct）
- 一键本地优化 / 回滚（电源、WSL、游戏注册表）
- 托盘后台 EXE 数据看板

## 当前状态（0.4.0）

- **UI 已重设计**：面板视觉/暗色模式/图标与控件已完成，EXE 已编译；
- **A/B 脚本待真实负载执行**：协议与测量脚本已就绪，尚未跑本机 3DMark/AI 数据；**UI 已由用户实机确认可打开**；
- 当前无后台进程运行。

## 二、专家共识（2026-09-05）

- 控制面收窄：G-Helper 性能档为**唯一控制源**，Windows 电源只作关联；
- 内存清理是第二控制动作；磁盘/网络**只观测不控制**；
- 所有自动动作需：持续确认 + 冷却 + 可回退 + 前后快照；
- 轻量化：单进程、无网络、无框架依赖，调度器自身低占用。

## 三、当前产物（0.6.0）

```text
D:\<工具目录>\
├── NvidiaTuningPanel.exe           ← 当前托盘版（0.5.0，Sketch 手绘风）
├── NvidiaTuningPanel_v3.exe        ← 同一版本副本

├── NVIDIA调优面板.bat / 启动调度.bat / 停止调度.bat / 查看状态.bat
├── 一键优化预检.bat / 一键优化应用.bat / 回滚优化.bat
├── 注册自启.bat / 取消自启.bat
├── 优化说明.txt / README.txt
├── HANDOFF.md                      ← 本文件
├── docs\
│   └── ab-protocol.md              # A/B 验证协议（真实对照）
├── optimizer\
│   ├── GHelperSmartScheduler.ps1     # 核心调度器（已含内存调度）
│   ├── GHelperSmartScheduler.config.json
│   ├── ab-measure.ps1                # A/B 测量脚本（只观测/CSV/JSON/DryRun）
│   ├── status-report.ps1
│   └── ...
├── local-optimizer\
│   ├── LocalOptimizer.ps1
│   └── LocalOptimizer.restore.ps1
└── src\
    ├── NvidiaTuningPanel.cs          # 托盘 EXE 源码（0.4.0 UI）
    ├── UI_DESIGN.md                  # 视觉契约（浅/暗色板、图标、层级）
    ├── app.manifest
    └── build-exe.bat
```

## 四、已实现功能（0.6.0）

1. **UI 产品化**：StyleKit 铅笔手绘风 + 启动默认显示主窗口（关闭入托盘）；浅/暗主题切换 + 注册表持久化；Segoe MDL2 按钮图标、自绘 MetricIcon；hover/pressed/focus；Windows 原生工具风，去除模板化彩色卡片。
2. **调度器**：GPU/CPU/内存/磁盘观测；G-Helper mode 自动切换；内存自动清理；防抖/冷却/回退日志。
3. **本地优化**：电源计划、WSL config、GameDVR/GameMode；备份+一键回滚；默认 dry-run。
4. **托盘 EXE**：托盘后台、双击打开、右键菜单、数据看板、实时趋势图、异步刷新、DPI 清晰。
5. **G-Helper 一键保守预设**：备份+写入风扇曲线+回滚；`disable_osd` 已关闭弹窗。
6. **A/B 基建**：`docs/ab-protocol.md` + `optimizer/ab-measure.ps1`（DryRun 实测通过；真实负载待执行）。

## 五、未完成 / 下一步候选

- [ ] **完整真实 A/B（≥3 对随机化）**：试点已跑（见 `audit/real-ab-pilot.md`），发现并修复调度器切档故障；需按协议做 3 对随机+冷却后再下结论。
- [x] **用户实机视觉确认**：用户已确认可打开并看到面板（2026-09-05）。
- [ ] 可选：历史曲线、阈值告警（不扩控制面，仅观测展示）。
- [ ] 可选：调度器更细的 disk/network 观测面板（仅观测，不控制）。

## 六、验证记录（0.5.0）

- PowerShell 脚本语法：OK
- 调度器 DryRun：OK（日志含 GPU/CPU/mem）
- 本地优化 备份→应用→回滚：OK（此前 0.3.x 记录）
- 托盘 EXE：编译 OK（csc exit 0），0.4.0 未实机截图（待用户）
- A/B 测量脚本：`-DryRun` exit 0；3 秒采样自测生成 CSV/JSON（含 11 字段；非真实负载，真实负载待用户）
- 图标与控件红队裁决：PASS（5 轮对抗后通过）
- Skill 包校验：见 manifest（0.4.0）

## 七、新会话建议入口

1. 先读本文件；
2. 用户说“UI 确认/截图”：重点看 `src/NvidiaTuningPanel.cs` + `src/UI_DESIGN.md`，运行 `D:\<工具目录>\NvidiaTuningPanel.exe` 实机确认；
3. 用户说“跑真实 A/B”：按 `docs/ab-protocol.md` + `optimizer/ab-measure.ps1` 执行；不要扩控制面；
4. 不要盲目加磁盘/网络自动控制；专家已裁决只观测。
