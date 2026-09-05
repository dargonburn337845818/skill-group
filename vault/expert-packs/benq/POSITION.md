# 本杰明·齐（Benq，美国顶尖算法选手） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

先做几何/结构性质推导，再写精细实现；对复杂数据结构和计算几何有系统化实现偏好

## 结构化条目（style_items）

### 1. benq-read-model-reformulate

**Trigger**: 读题或卡壳时，限制不自然、术语可疑、目标函数易误读，或看到题面就想套算法。

**Action**: 先系统自问“为什么有这个限制/去掉会怎样/有什么不寻常”，把题面重述成纯数学模型或标准问题；确认非标准术语定义与目标函数类型；再决定选用什么工具。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/113785; https://codeforces.com/blog/entry/142536; https://codeforces.com/blog/entry/64543; https://codeforces.com/blog/entry/62730

### 2. benq-state-compression-encoding

**Trigger**: 对象离散但有界（点/值域小、参数区间连续、小分量可枚举），直接 map/显式枚举常数或空间太高。

**Action**: 用 bitset/数组下标/区间/模不变式/子集状压表示集合、二元组、连续块或小连通分量；用位运算和数组替代 map、用模约束压缩双重枚举。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/81916; https://codeforces.com/blog/entry/93568; https://codeforces.com/blog/entry/51883

### 3. benq-reverse-linearize-transform

**Trigger**: 正向插入/搜索/比较复杂，而倒序扫描、环状排列、排列相对顺序可换成线性的数组/字符串操作。

**Action**: 正向难做就反向扫描或建反向图；把环状排列复制接尾；用第二个排列建位置数组把相对顺序转为线性扫描计数。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/43467; https://codeforces.com/blog/entry/43868; https://codeforces.com/blog/entry/70620

### 4. benq-discrete-state-compact-linear-encoding

**Trigger**: 需要频繁对集合/二元组做合并、统计或查找；对象本身离散且有界（点/值域小、pair 分量可枚举），而朴素用 map 或显式枚举的常数/空间偏高

**Action**: 把离散对象编码成紧凑线性表示：集合/可达集用 bitset 表示以便按位并，二元组用 a*n+b 编码成数组下标；用数组/位运算代替 map 与显式枚举

**Boundary**: 值域太大或太稀疏导致 bitset/数组不可行；编码不是一一映射会产生碰撞；需要动态删除或任意类型键时线性化失效

**SourceRefs**: https://codeforces.com/blog/entry/68131; https://codeforces.com/blog/entry/81916

### 5. benq-reverse-direction-processing

**Trigger**: 正向搜索/扫描/维护时困难（前驱多、分支大、有序插入昂贵），而反向处理时约束更直接或维护操作更简单

**Action**: 把搜索或扫描方向反过来：正向难搜就建反向图/逆向 DP，从终点向前驱推；正向难插入有序表就反向扫描，让插入变成删除，再根据被删元素的近邻维护答案

**Boundary**: 反向操作不等价（有向依赖、流/匹配不可逆），或反向后仍遇到同样爆炸/同样昂贵的操作；若删除也不是 O(1)/简单近邻则不能简化

**SourceRefs**: https://codeforces.com/blog/entry/68131; https://codeforces.com/blog/entry/43467

### 6. benq-bitset-graph-reachability

**Trigger**: 图可达性/传递闭包需要重复做集合与集合的合并，V 中等（约 10^3~10^4）而朴素 O(V^3) 或 O(EV) 的常数偏大时

**Action**: 把每个点的邻接/可达集合编码成 bitset，使集合并、按位或等操作按字并行，用 O(EV/word) 降到常数可过

**Boundary**: V 很大时 bitset 只是压常数，不能改变 O(EV) 本身的量级；边动态变化、需要支持删除或维护最短路时，bitset 也不适用

**SourceRefs**: https://codeforces.com/blog/entry/68131

### 7. benq-reusable-blackbox-abstraction

**Trigger**: 某类内容/实现/问题反复出现且每次完整展开成本高、信息量低，而重复的本质不是当前思考核心

**Action**: 先识别能否把其压缩成可复用对象：题面剥离成纯数学模型，复杂算法封装成库/oracle，常见问题沉淀为资源链接；之后直接使用该抽象，把精力留给真正需要思考/建模/实现的部分

**Boundary**: 高度具体或个性化问题不能泛化；抽象可能过时或隐藏关键线索（如故事本身是转化提示）；需要大量定制/调常数时黑盒化反而增加调试成本

**SourceRefs**: https://codeforces.com/blog/entry/62730; https://codeforces.com/blog/entry/71349; https://codeforces.com/blog/entry/82400

### 8. benq-geometry-constraint-extremes

**Trigger**: 多个独立约束同时满足、半平面/凸包极值、计算几何退化输入、高维点两两配对。

**Action**: 独立约束转成同参数上下界并取极值收缩；半平面交用上下包络判定；几何微扰消退化；递归按坐标分桶配对。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/44754; https://codeforces.com/blog/entry/61710; https://codeforces.com/blog/entry/73366; https://codeforces.com/blog/entry/70620

**SourceRefs（专家总来源）**: https://codeforces.com/profile/benq; https://codeforces.com/blog/entry/73366; https://codeforces.com/blog/entry/55506; $WORKSPACE/skills/teacher-consensus-skill/output/teacher_consensus_final.json; https://codeforces.com/blog/entry/113785; https://codeforces.com/blog/entry/142536; https://codeforces.com/blog/entry/64543; https://codeforces.com/blog/entry/62730; https://codeforces.com/blog/entry/81916; https://codeforces.com/blog/entry/93568; https://codeforces.com/blog/entry/51883; https://codeforces.com/blog/entry/43467; https://codeforces.com/blog/entry/43868; https://codeforces.com/blog/entry/70620; https://codeforces.com/blog/entry/68131; https://codeforces.com/blog/entry/71349; https://codeforces.com/blog/entry/82400; https://codeforces.com/blog/entry/44754; https://codeforces.com/blog/entry/61710