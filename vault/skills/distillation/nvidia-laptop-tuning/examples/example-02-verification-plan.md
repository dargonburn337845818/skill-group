# 示例 02：验证计划模板（一次只改一个变量）

> 适用于任何“尝试性调优”。每次实验 = 同一个任务 + 改前 3 次 + 改后 3 次 + 记录。

## 实验表

| # | 变量 | 预期收益 | 改前基线 | 改后结果 | 保留/回滚 |
|---|---|---|---|---|---|
| 1 | 加第二根 16GB DDR5-5600（双通道） | 内存带宽/数据加载/CPU受限场景提升 | 单通道数据 | 待测 | 待定 |
| 2 | WSL `.wslconfig` memory=10GB | 训练 OOM 减少、吞吐提升 | 7.4GB | 待测 | 待定 |
| 3 | Armoury Crate GPU 模式 → Ultimate | 游戏 dGPU 直连、延迟/1% low 改善 | Hybrid | 待测 | 待定 |
| 4 | 控制面板电源模式 → 性能 | 高负载频率/性能 | Balanced/自动 | 待测 | 待定 |
| 5 | NVIDIA App 一键自动调优 | 小幅频率提升 | 关 | 待测 | 待定（最低优先） |

## 游戏基准模板

```text
游戏/场景：__________________（固定回放或同一关卡）
画质设置：__________________（固定）
分辨率/刷新：2560x1600 @165Hz，G-Sync ________
改前：
  run1 avg=___ fps, 1%low=___ fps, p95_frame=___ ms
  run2 avg=___ fps, 1%low=___ fps, p95_frame=___ ms
  run3 avg=___ fps, 1%low=___ fps, p95_frame=___ ms
改后：
  run1/2/3 同上
结论：avg 提升 ___%，1%low 提升 ___%，p95 改善 ___ms，是否保留？________
```

## AI 基准模板

```python
import torch, time
# 固定模型/数据/batch/seed；跑 3 次取中位数
def bench(model, loader):
    torch.cuda.synchronize(); t0=time.perf_counter()
    for x,y in loader: model(x)
    torch.cuda.synchronize()
    return time.perf_counter()-t0
# 记录：steps/s、显存峰值、温度/功耗（nvidia-smi 并行采样）
```

```text
改前：step/s=___, peak_vram=___GB, gpu_temp=___C, power=___W
改后：step/s=___, peak_vram=___GB, gpu_temp=___C, power=___W
结论：吞吐提升___%，显存/温度是否可接受？________
```

## 保留/回滚规则

1. 同一指标 3 次中位数，不看单次运气。
2. 平均帧提升但 1% low/帧时间长尾变差 → 不保留（或记录取舍）。
3. 出现花屏、崩溃、驱动重启、WSL 无法启动 → 立即回滚，并在表中写“副作用”。
4. 至少保留 3 个正向重复样本才下“有效”结论；只有 1 次提升标 `single-effect`。
