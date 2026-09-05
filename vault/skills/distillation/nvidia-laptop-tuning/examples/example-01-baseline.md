# 示例 01：改前基线记录（本机实测版）

> 目的：任何调优前先留下可复现的“改前”数据。本示例直接使用 2026-09-05 在本机 WSL2 采集的数据。

## 硬件/软件快照

| 项 | 值 |
|---|---|
| 主机 | ASUS TX Gaming FX608LM_FX608LM |
| CPU | Intel Core Ultra 7 255HX（20C/20T） |
| GPU | NVIDIA GeForce RTX 5060 Laptop GPU 8GB GDDR7 |
| 显示器 | 16" 2560x1600，165Hz，G-Sync，MUX + Advanced Optimus |
| 内存 | SK Hynix 16GB DDR5-5600，单根（BANK 1 / ChannelB-DIMM1） |
| 存储 | Samsung MZVL81T0HELB-00BTW 1TB NVMe SSD |
| BIOS | FX608LM.305（2025-04-28） |
| Windows 驱动 | 32.0.16.1656 = NVIDIA 616.56（2026-08-20） |
| NVIDIA App | 11.0.9.251 |
| CUDA | Windows 侧 CUDA 13.3；WSL 侧 torch 2.13.0+cu130 |
| WSL 内存 | total 7.4 GiB，swap 2.0 GiB |

## GPU 空闲基线（WSL 内 nvidia-smi）

```text
NVIDIA GeForce RTX 5060 Laptop GPU, KMD 616.56, CUDA UMD 13.4
Temp 65C, Perf P2, Power 15W/95W, Mem 2481MiB/8151MiB, GPU-Util 4%
Clocks: SM 1800-1867 MHz, Mem 11001 MHz, Max SM 3090 MHz
```

> 注意：`nvidia-smi` 显示 Power Limit 95W 是当前配置；ASUS 规格称该 GPU 最高 115W（100W+15W Dynamic Boost）。实际的“满血上限”由 Armoury Crate/BIOS 决定。

## AI 基准（PyTorch fp32 matmul 4096^2）

```text
torch 2.13.0+cu130, cuda available=True
device: NVIDIA GeForce RTX 5060 Laptop GPU
matmul4096 avg 0.0149 s -> 约 9.2 TFLOPS（5 次取平均，热身 3 次）
```

## 改前结论

- 当前处于 Hybrid/中等功耗状态（P2，15-19W），GPU 基本空闲。
- 最大已知瓶颈候选：**单通道内存**，其次 WSL 默认 8GB 内存上限；两者都可能影响 AI 数据加载和 CPU 受限场景。
- 因此第一步不是超频，而是记录游戏/训练基线，再考虑“加第二根内存”和 WSL 内存配置。
