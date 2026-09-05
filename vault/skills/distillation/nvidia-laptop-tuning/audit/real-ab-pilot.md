# 真实 A/B 试点（0.5.0）

> 日期：2026-09-05
> 负载：WSL PyTorch CUDA（RTX 5060 Laptop，固定 Linear 网络，seed=42，batch=256）
> 方法：B=调度器关 + G-Helper Balanced；A=调度器开（默认配置）+ 允许自动切档。
> 采样：`optimizer/ab-measure.ps1`（CSV/JSON 原始数据见 `audit/real-ab-data/`）。

## 数据摘要

| 臂 | 训练吞吐 (it/s) | GPU 平均利用率 | GPU 平均温度 | GPU 平均功耗 |
|---|---|---|---|---|
| B（无调度器，Balanced） | 104.8 | 95.3% | 84.3°C | 64.5W |
| A（有调度器，首次试点 100s 未切档） | 93.5 | 92.4% | 86.0°C | 52.5W |
| A（修复后 160s，后期切 Turbo） | 93.4 | 96.7% | 86.3°C | 53.5W |
| A 切 Turbo 后（约 47s） | — | 99.2% | 86.4°C | 59.0W |

## 结论（诚实声明）

- 本次是**试点**，不是完整 3 对随机化 A/B；顺序上 B 先跑、A 后跑，存在热漂移，**不能据此判定“调度器无收益”或“有收益”**。
- 发现并修复了调度器实际不切档故障：`heavySustainSeconds` 被按“轮询次数”累计，实际需 150s 才切换；且首次切档受 `minSwitchIntervalSeconds=120s` 保护。修复后 A 臂在 160s 内真实切到 Turbo（日志见 `ab-data`，状态文件显示 Turbo）。
- 试点中 A 平均吞吐低于 B，但 A 后期温度/功耗更高、Turbo 仅约 47s；需要按 `docs/ab-protocol.md` 做 ≥3 对随机 + 冷却后再下结论。
- 真实数据原始 CSV/JSON 已留存，供后续完整 A/B 使用。
