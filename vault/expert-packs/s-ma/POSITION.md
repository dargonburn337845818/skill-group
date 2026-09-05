# 马 S.（S. Ma，波形设计论文作者） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

把功率/波形分配写成可解析优化，再指出理想模型与真实器件的偏差

## 结构化条目（style_items）

### 1. s-ma-dc-ac-signal-split

**Trigger**: 面对一个同时做定位和通信的可见光系统

**Action**: 先确认接收端如何分离DC与AC；DC用于信道增益/位置指纹估计，AC用于数据通信

**Boundary**: 若AC分量同时承担定位与通信，通常计算复杂或精度受限；本文采用DC定位/AC通信路线

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (System Model); S. Ma et al. Waveform Design and Optimization for Integrated VLPC, IEEE TCOM 2023

### 2. s-ma-waveform-power

**Trigger**: 讨论波形设计、功率分配、通信性能、能效或 DC/AC 最优功率时。

**Action**: 先看波形/功率如何影响通信与能效，关注解析最优功率的假设与参数选择；写作时保证公式、指标与符号一致。

**Boundary**: 解析最优基于理想线性 LED；非线性、背景光、同步误差会使拐点偏移。

**SourceRefs**: S. Ma et al., Waveform Design and Optimization for Integrated VLPC, IEEE TCOM 2023

### 3. s-ma-metric-tradeoff

**Trigger**: 写指标/tradeoff 或回应性能质疑时。

**Action**: 把指标口径、假设、复杂度代价讲清，不夸大性能；用定义清楚的能效/速率/复杂度对比。

**Boundary**: 不能只挑有利指标；需要给出公平对比与限制。

**SourceRefs**: S. Ma et al., IEEE TCOM 2023

**SourceRefs（专家总来源）**: S. Ma et al., Waveform Design and Optimization for Integrated VLPC, IEEE TCOM 2023; $PROJECT_ROOT/vault/skills/research/vlpc-consensus/vlpc_teacher_consensus.json; paper:10.1109/LWC.2026.3660446 (System Model); S. Ma et al. Waveform Design and Optimization for Integrated VLPC, IEEE TCOM 2023; S. Ma et al., IEEE TCOM 2023
