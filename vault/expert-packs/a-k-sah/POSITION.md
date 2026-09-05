# 萨赫（A. K. Sah，NOMA-VLCP） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

关注免 SIC 或简化 SIC 的室内两用户方案，比较复杂度和性能折中

## 结构化条目（style_items）

### 1. a-k-sah-noma-sic-ipSIC

**Trigger**: AC分量给多个用户做NOMA通信

**Action**: 按信道增益排序，强用户先解码并做SIC；比较pSIC与ipSIC；考虑GRPA/FPA/NGDPA功率分配

**Boundary**: ipSIC残留干扰降低总速率与EE；SIC顺序/功率系数/信道估计误差耦合

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Communication Scheme); Multi-user grouping for NOMA enabled VLC system, IEEE Commun. Lett. 2024; SIC-free based indoor two-user NOMA-VLCP system, Photonics 2024

### 2. sah-noma-vlcp-system

**Trigger**: 讨论 NOMA-VLCP 系统级设计、能效/功率分配或定位通信一体化时。

**Action**: 先看总功率如何在定位与通信之间分配，识别不同 NOMA/资源方案对系统性能的影响。

**Boundary**: 不能脱离具体系统约束推广；结果需回原文/实验。

**SourceRefs**: SIC-free based indoor two-user NOMA-VLCP system, Photonics 2024

### 3. sah-fair-comparison

**Trigger**: 比较不同 NOMA/SIC/功率方案时。

**Action**: 保持公平条件：相同总功率/信道/用户数，逐项对比指标与复杂度。

**Boundary**: 只比单项指标容易误导；要给出适用边界。

**SourceRefs**: SIC-free based indoor two-user NOMA-VLCP system, Photonics 2024

**SourceRefs（专家总来源）**: SIC-free based indoor two-user NOMA-VLCP system, Photonics 2024; $PROJECT_ROOT/vault/skills/research/vlpc-consensus/vlpc_teacher_consensus.json; paper:10.1109/LWC.2026.3660446 (Communication Scheme); Multi-user grouping for NOMA enabled VLC system, IEEE Commun. Lett. 2024
