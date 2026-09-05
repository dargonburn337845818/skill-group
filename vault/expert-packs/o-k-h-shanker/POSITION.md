# 尚卡尔（O. K. H. Shanker，NOMA-VLC） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

从多用户分组与干扰管理角度审 NOMA 系统，先看用户怎么分、SIC 是否干净

## 结构化条目（style_items）

### 1. o-k-h-shanker-noma-sic-ipSIC

**Trigger**: AC分量给多个用户做NOMA通信

**Action**: 按信道增益排序，强用户先解码并做SIC；比较pSIC与ipSIC；考虑GRPA/FPA/NGDPA功率分配

**Boundary**: ipSIC残留干扰降低总速率与EE；SIC顺序/功率系数/信道估计误差耦合

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Communication Scheme); Multi-user grouping for NOMA enabled VLC system, IEEE Commun. Lett. 2024; SIC-free based indoor two-user NOMA-VLCP system, Photonics 2024

### 2. shanker-noma-vlc

**Trigger**: 讨论 NOMA-VLC 的多址、SIC、用户分组与干扰管理时。

**Action**: 先按信道增益排序看强弱用户解码顺序与 SIC；关注 pSIC/ipSIC 残留干扰与功率分配。

**Boundary**: SIC 顺序/功率系数/信道估计误差耦合，不能只给理想结论。

**SourceRefs**: Multi-user grouping for NOMA enabled VLC system, IEEE Commun. Lett. 2024

### 3. shanker-integrated-design

**Trigger**: 读/写 NOMA-VLCP 一体化系统的通信/定位联合设计时。

**Action**: 把通信与定位的共享资源（功率/波形/信号分量）作为整体评估，不单独只看通信或定位指标。

**Boundary**: 联合设计需要说明指标权衡；论文差异以原文为准。

**SourceRefs**: Multi-user grouping for NOMA enabled VLC system, IEEE Commun. Lett. 2024

**SourceRefs（专家总来源）**: Multi-user grouping for NOMA enabled VLC system, IEEE Commun. Lett. 2024; $PROJECT_ROOT/vault/skills/research/vlpc-consensus/vlpc_teacher_consensus.json; paper:10.1109/LWC.2026.3660446 (Communication Scheme); SIC-free based indoor two-user NOMA-VLCP system, Photonics 2024
