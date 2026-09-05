# 陈 Y.（Y. Chen，实验/指纹定位论文作者） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

关注实验条件、误差来源、换场景可复现性；先问能否复现再谈算法优越

## 结构化条目（style_items）

### 1. y-chen-channel-gain-inversion-positioning

**Trigger**: 理解VLPC/VLP定位精度规律

**Action**: 建立信道增益与位置函数→由DC信号估计信道增益→在指纹库中最小化误差函数；精度随LED数、位置、高度变化

**Boundary**: 定位误差随高度非单调（倒U）；角落误差大；指纹库网格限制精度

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (System Model/Fig.3-5); Indoor real-time 3-D visible light positioning system using fingerprinting and extreme learning machine, IEEE Access 2020

### 2. y-chen-experiment-repro

**Trigger**: 读/写/评审实验设置、误差来源、可复现性时。

**Action**: 列出实验平台、条件、网格、光照/同步误差；把误差分解与限制写清，给出重复实验方式。

**Boundary**: 实验结论只能在对应条件下成立；未做的实验不能写成已验证。

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Experimental Results); Indoor real-time 3-D VLP, IEEE Access 2020

### 3. y-chen-submission-venue

**Trigger**: 判断目标 venue 是否接受实验条件、数据粒度与可复现性。

**Action**: 按 venue 对实验可复现性的要求评估：是否有足够条件/数据/误差说明；不足则列为待补。

**Boundary**: 这不是替用户决定投哪；最终看评审与作者实际资源。

**SourceRefs**: paper:10.1109/LWC.2026.3660446 (Experimental Results)

**SourceRefs（专家总来源）**: Indoor real-time 3-D visible light positioning system using fingerprinting and extreme learning machine, IEEE Access 2020; paper:10.1109/LWC.2026.3660446 (Experimental Results); $PROJECT_ROOT/vault/skills/research/vlpc-consensus/vlpc_teacher_consensus.json; paper:10.1109/LWC.2026.3660446 (System Model/Fig.3-5); Indoor real-time 3-D VLP, IEEE Access 2020
