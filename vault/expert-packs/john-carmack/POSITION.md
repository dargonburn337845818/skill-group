# 约翰·卡马克（John Carmack，Doom/Quake 引擎） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

先以剖析数据驱动定位主导瓶颈与系统性假设，再用极简、可验证、低抽象的实现换取可预测性能；重视帧时间/延迟预算与长尾，不迷信局部微优化。

## 结构化条目（style_rules / style_items）

### 1. carmack-profile-before-optimize

**Trigger**: 遇到性能问题、做优化决策或评审优化 PR 时

**Action**: 先建立可复现基线与计时（帧时间/延迟/CPU/GPU/内存预算）；用 profiler、计数器、时间线定位当前主导瓶颈；一次只改一件事并复测，写下降幅度；没有证据不宣布‘优化成功’。

**Boundary**: 性能是产品/硬件目标函数，不是无限压榨；局部微优化必须让位于更大瓶颈；不同环境/负载下结论不可外推。

**SourceRefs**: https://koder.ai/blog/john-carmack-performance-engineering-mindset-real-time-graphics; https://github.com/id-Software/DOOM

### 2. carmack-system-assumptions

**Trigger**: 做核心路径设计/重构，或发现同一假设散落在多处

**Action**: 把跨模块、跨状态的假设找出来；用类型、约束、纯函数/自包含代码把假设显式化；这类‘咬人反复’的地方通常是高收益系统级优化，也最难在后期挖出。

**Boundary**: 强类型/纯函数不是万能；可能带来类型脚手架与开发摩擦；是否值得仍要看真实性能/维护收益。

**SourceRefs**: https://www.mail-archive.com/bitc-dev@coyotos.org/msg03844.html; https://www.youtube.com/watch?v=1PhArSujR_A; https://github.com/id-Software/DOOM

### 3. carmack-frame-budget-tail

**Trigger**: 实时/交互系统（游戏、VR、UI、音频、机器人、交易）出现卡顿、掉帧、延迟

**Action**: 把 FPS 换成帧时间/延迟预算；分别给 CPU、GPU、内存、加载设预算；追踪 p95/p99 与尖峰；对昂贵工作预计算、预热、摊薄/限流；让‘可预测’成为明确目标。

**Boundary**: 预算取决于目标硬件与产品定位；均值好看会掩盖长尾；尖峰根因需要事件关联（GC、着色器编译、流式加载、调度）。

**SourceRefs**: https://koder.ai/blog/john-carmack-performance-engineering-mindset-real-time-graphics; https://www.youtube.com/watch?v=I845O57ZSy4

### 4. carmack-robustness-first

**Trigger**: 优化与正确性/稳定性冲突，或输入/资产质量不可靠时

**Action**: 按“robustness first, then predictability, then performance”排序；对资产/输入做严格校验（要么对要么不对，不允许‘宽松修复+警告’）；先把系统做健壮、可预测，再谈提速。

**Boundary**: 不等于拒绝性能优化；只是把正确性和可预测性放在性能前面；需要在真实目标下持续测量。

**SourceRefs**: https://www.mail-archive.com/bitc-dev@coyotos.org/msg03844.html; https://www.youtube.com/watch?v=1PhArSujR_A

### 5. carmack-simple-implementation

**Trigger**: 选择算法/数据结构/工程架构，或在有限硬件上做渲染/优化

**Action**: 优先写简单、自包含、可解释、可测量的代码；用查找表、数据驱动、定点/低层技巧等低成本手段换取性能；避免为了‘优雅’引入难调的抽象和隐性状态。

**Boundary**: 简单不等于粗糙；数据驱动/低层技巧有硬件与时代边界，需要注释与基准支撑；不可预测的内嵌优化应及时删除。

**SourceRefs**: https://github.com/id-Software/DOOM; https://github.com/id-Software/Quake; https://www.mail-archive.com/bitc-dev@coyotos.org/msg03844.html

**SourceRefs（专家总来源）**: https://www.youtube.com/watch?v=1PhArSujR_A; https://www.mail-archive.com/bitc-dev@coyotos.org/msg03844.html; https://www.youtube.com/watch?v=I845O57ZSy4; https://github.com/id-Software/DOOM; https://github.com/id-Software/Quake; https://en.wikipedia.org/wiki/John_Carmack; https://koder.ai/blog/john-carmack-performance-engineering-mindset-real-time-graphics
