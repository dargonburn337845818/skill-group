# 专家讨论记录：R1

- 会话：teacher_1788596188748_asonqq
- 领域：性能优化（performance）
- 专家团：John Carmack（实时渲染/系统性能风格参考）、Brendan Gregg（系统性能方法论参考）
- 主题：审查 ASUS FX608LM（RTX 5060 Laptop 8G / 16GB 单通道 / WSL2 + Windows 混合用途）的 NVIDIA 驱动与设备调优方案
- 性质：风格/方法论推断，**不是本人原话**；来源见 EXPERT_LIBRARY.json 对应条目。

## R1 结论（署名）

1. **John Carmack**：先固定基线，一次只改一个变量，用帧时间/延迟而不是平均 FPS 判断；硬件瓶颈（单通道内存）比 GPU 超频更值得优先处理。
2. **Brendan Gregg**：用 USE/TSA 思路把资源利用率、饱和度和错误先量化：GPU 利用率、显存占用/换出、CPU/内存/存储饱和度；验证方案必须可复现并记录环境，不能靠“感觉”。

## 裁决

- 冲突 c1（是否先尝试 NVIDIA App 自动调优/超频）：merge —— 自动调优只能作为“测量后确认 GPU 是瓶颈并有余量”的后续选项，不能作为开局默认动作。
