# 英伟达笔记本调优（nvidia-laptop-tuning）

> 面向 GeForce 笔记本 + Windows 11 + WSL2 CUDA 的可执行调优与验证手册。
> 入口是 `SKILL.md`；深入规则读 `CONSENSUS.md` / `SOURCES.md`；验证模板读 `examples/`。

## 如何使用

1. 加载 `SKILL.md`。
2. 先跑“记录现状”基线，再按规则一次只改一个变量。
3. 需要依据时读 `CONSENSUS.md`，需要来源时读 `SOURCES.md`。
4. 需要现成验证模板时读 `examples/example-01-baseline.md`、`examples/example-02-verification-plan.md`。
5. 本机面板 UI 契约见 `src/UI_DESIGN.md`；调度器有无的真实对照协议见 `docs/ab-protocol.md`。

## 目录

- `SKILL.md` — agent 可执行摘要（入口）
- `CONSENSUS.md` — 完整规则、证据分级、边界
- `SOURCES.md` — 可审计来源清单
- `manifest.json` — vault 元数据（0.5.0）
- `examples/` — 基线记录与验证模板
- `optimizer/` — G-Helper 轻量智能调度守护（PowerShell，可选）与 A/B 测量脚本
- `local-optimizer/` — 本地电脑设置一键优化/回滚脚本（安全版，默认 dry-run）
- `docs/` — A/B 验证协议与报告模板
- `src/` — Windows 托盘面板源码与 UI 设计契约
- `audit/` — 专家讨论与过程材料

## 面板与 UI（0.5.0）

- Windows 托盘面板源码：`src/NvidiaTuningPanel.cs`（WinForms，单 EXE）。
- 视觉契约：`src/UI_DESIGN.md`（StyleKit 铅笔手绘风：纸张色、楷体、虚线边框、趋势图规则）。
- 已实现：StyleKit 手绘风、浅/暗主题切换、MDL2 图标、自绘指标图标、实时趋势图、异步刷新、托盘后台。

## A/B 验证（0.5.0）

- 协议：`docs/ab-protocol.md`（负载选择、变量隔离、随机化、样本量、指标、判定规则）。
- 测量脚本：`optimizer/ab-measure.ps1`（`-Arm baseline/tuned`、`-Duration`、`-Interval`、`-OutputDir`、`-DryRun`；只观测，输出 CSV/JSON）。
- 真实试点已跑：见 `audit/real-ab-pilot.md` 与 `audit/real-ab-data/`；同时发现并修复调度器“持续判定按次数而非秒”导致的不切档故障。
- 当前状态：试点完成；**完整 ≥3 对随机化 A/B 仍待按协议执行后下结论**。

## G-Helper 一键保守预设（0.6.0）

- 入口：`应用GHelper预设.bat`（一键备份+写入+重启）。
- 脚本：`optimizer/ghelper-apply-presets.ps1`（不带 `-Apply` 只预览）。
- 默认只改风扇曲线；功耗限制不动，避免单位/超频风险；可回滚（备份文件）。

## 边界

- 不承诺“一定提升多少”；所有收益必须通过本机 A/B 验证。
- 驱动/BIOS/超频改动前先备份、确认保修与厂商支持。
- 本包不自动执行任何系统改动，只提供方法；面板也只提供按钮触发，不默认改系统。
