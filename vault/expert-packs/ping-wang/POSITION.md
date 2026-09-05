# 王平（Ping Wang，定位/信号处理论文作者） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

抓噪声来源与抗噪链路：编码稳定、多次平均、多数投票、两阶段定位

## 结构化条目（style_items）

### 1. ping-wang-dc-ac-signal-split

**Trigger**: 面对一个同时做定位和通信的可见光系统

**Action**: 先确认接收端如何分离DC与AC；DC用于信道增益/位置指纹估计，AC用于数据通信

**Boundary**: 若AC分量同时承担定位与通信，通常计算复杂或精度受限；本文采用DC定位/AC通信路线

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (System Model); S. Ma et al. Waveform Design and Optimization for Integrated VLPC, IEEE TCOM 2023

### 2. ping-wang-dc-ac-power-tradeoff

**Trigger**: 总电功率固定，DC用于定位，AC用于通信

**Action**: 由Pmax(Idc^2)=min{Idc^2/K, Ptotal-Idc^2}，最优点Idc^2=K/(K+1)Ptotal；超过后需在定位与通信间权衡

**Boundary**: 解析最优基于理想线性LED；实际LED非线性、背景光、同步误差会使拐点偏移

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Optimal DC Power Setting)

### 3. ping-wang-noma-sic-ipSIC

**Trigger**: AC分量给多个用户做NOMA通信

**Action**: 按信道增益排序，强用户先解码并做SIC；比较pSIC与ipSIC；考虑GRPA/FPA/NGDPA功率分配

**Boundary**: ipSIC残留干扰降低总速率与EE；SIC顺序/功率系数/信道估计误差耦合

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Communication Scheme); Multi-user grouping for NOMA enabled VLC system, IEEE Commun. Lett. 2024; SIC-free based indoor two-user NOMA-VLCP system, Photonics 2024

### 4. ping-wang-dc-drift-biphase

**Trigger**: 用直流分量做定位/信道估计，但消息比特随机导致直流分量漂移

**Action**: 使用双相编码（0→-1 1，1→1 -1）使信息序列不影响DC；再对多个连续DC样本平均以抑制噪声

**Boundary**: 只解决消息随机性；接收机噪声、LED非线性、背景光、同步误差仍会引入偏差

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Positioning Scheme); Digital Communications (Sklar & Harris, 3rd ed.), ref [8] of paper

### 5. ping-wang-noise-majority-two-stage

**Trigger**: 单次指纹定位结果受噪声和数据库粒度影响

**Action**: 多次采样平均→多轮定位结果取众数→先粗定位缩小范围→局部精定位

**Boundary**: 增加时延/计算量；指纹库网格间距决定精度下限；环境变化会使离线库失效

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Positioning Scheme); fingerprinting refs [10][11][12]

### 6. ping-wang-fingerprint-vs-metaheuristic-complexity

**Trigger**: 对比定位算法精度与运行时间

**Action**: 定位复杂度约O(M(Nc+Nf))，无迭代；通信模块解析解O(1)；在4cm精度目标下比WOA/HBA/GA/SSA/BA快

**Boundary**: 元启发式更灵活、可不依赖指纹库；本文依赖离线库且误差受网格间隔限制

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Computational Complexity, Table II)

### 7. ping-wang-positioning-chain

**Trigger**: 读/写/评审定位链路、抗噪、指纹库、精度规律相关章节。

**Action**: 先梳理定位链路：DC 估计信道增益→反演位置；关注噪声、多数投票/两阶段、误差来源，并在方法节解释每一步为什么这样设计。

**Boundary**: 定位精度与实验条件强相关；不能用单点结果推广到所有环境。

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Positioning Scheme); Indoor real-time 3-D VLP, IEEE Access 2020

### 8. ping-wang-rebuttal

**Trigger**: 审稿人对定位算法/信号处理提出方法质疑时。

**Action**: 回复时定位到具体公式/流程/参数，给出公平对比与误差来源，不绕概念。

**Boundary**: 若质疑需要补充实验，应说明条件与重复方式，不能只给解释。

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Positioning Scheme)

**SourceRefs（专家总来源）**: paper:10.1109/LWC.2026.3660446 (Positioning Scheme); $PROJECT_ROOT/vault/skills/research/vlpc-consensus/vlpc_teacher_consensus.json; paper:10.1109/LWC.2026.3660446 (System Model); S. Ma et al. Waveform Design and Optimization for Integrated VLPC, IEEE TCOM 2023; paper:10.1109/LWC.2026.3660446 (Optimal DC Power Setting); paper:10.1109/LWC.2026.3660446 (Communication Scheme); Multi-user grouping for NOMA enabled VLC system, IEEE Commun. Lett. 2024; SIC-free based indoor two-user NOMA-VLCP system, Photonics 2024; Digital Communications (Sklar & Harris, 3rd ed.), ref [8] of paper; fingerprinting refs [10][11][12]; paper:10.1109/LWC.2026.3660446 (Computational Complexity, Table II); Indoor real-time 3-D VLP, IEEE Access 2020
