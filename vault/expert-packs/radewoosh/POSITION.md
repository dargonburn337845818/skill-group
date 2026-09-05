# Radewoosh（波兰顶尖选手/自创算法） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

自创算法、离线分块与均摊结构；用长博客深度推导复杂度与正确性

## 结构化条目（style_items）

### 1. radewoosh-monotone-bitonic-binary-ternary-search

**Trigger**: 问题中有一个可排序/可计数的搜索空间（候选集、答案 t、阈值 k、中位数规模 j），且可行性或目标值随参数单调，或函数本身凸/凹因此单峰；需要找最优/最左可行解而不是枚举全部。

**Action**: 把搜索空间压到二分/三分：先写出 check(x) 或目标 f(x)。若判定随 x 单调，则二分最小/最大可行 x；若 f 单峰则三分（或二分边际量）找极值。交互类可把候选排全序后查中间位；具体 check 按问题构造，如贪心排序取前 k、树形 DP 维护最长合格前缀、拓扑定向验证无环、比例不等式等。

**Boundary**: 若 check 不单调、函数多峰/平台/离散噪声、候选无法快速计数排序，或单次检查代价极高，二分/三分剪枝会失效或收益有限。三分对浮点精度、非严格单峰也需要谨慎。

**SourceRefs**: https://codeforces.com/blog/entry/93568; https://codeforces.com/blog/entry/61710; https://codeforces.com/blog/entry/43467; https://codeforces.com/blog/entry/64543

### 2. radewoosh-interval-constraints-intersection

**Trigger**: 多个约束都要求一个一维分割点落入某个区间 [a_i, b_i]，需要求所有约束同时满足的分割点范围/数量

**Action**: 把每个约束转成“分割点在 a_i 右侧、b_i 左侧”；取所有 a_i 的最大值 A、所有 b_i 的最小值 B，有效区间为 [A, B]，答案为 max(0, B - A)

**Boundary**: 如果约束不是单一区间而是一组区间/不等式组，或者需要处理多个维度，只取最大/最小会漏掉联合约束

**SourceRefs**: https://codeforces.com/blog/entry/44754

### 3. radewoosh-relax-exact-to-at-least

**Trigger**: 要求选出若干个“恰好大小为 k”的连通块/子结构，而结构本身允许从叶子/端点逐步删除顶点来缩小尺寸

**Action**: 先把“恰好 k”松弛成“至少 k”；对任何超过 k 的组件，通过切除叶子把它降到恰好 k，从而只需考虑下界约束

**Boundary**: 若结构不是树/没有可随意删除的叶子，或题目要求“恰好”且不能额外裁剪（如外部有依赖/权值限制），松弛后不等价

**SourceRefs**: https://codeforces.com/blog/entry/61331

### 4. radewoosh-offline-timeline-dc-scc

**Trigger**: 所有边/更新按时间顺序给出（离线已知），要在每次加入后知道 SCC/连通分量信息；在线增量算法难写或想做成 O(m log m)。

**Action**: 对时间区间 [a,b] 分治：取中点 s，先用截止 s 已加入的边在当前缩点图上算 SCC；把算出的 SCC 压缩成单点，右递归只传跨 SCC 的边，左递归传剩下边；每个边每层出现一次，总复杂度 O(m log m)。

**Boundary**: 若边需要在线实时回答、无法先知道完整列表，或分量之后会分裂（而不仅是合并），则不能简单压缩；需要在线动态连通性/可撤销并查集。

**SourceRefs**: https://codeforces.com/blog/entry/91608

### 5. radewoosh-convex-bitonic-search

**Trigger**: 问题被化成一个一维函数，且已知该函数凸/凹从而单峰（bitonic），需要在其中找最大值、最小值或正负分界点。

**Action**: 利用凸性推出单峰性，用三分法（或对离散单峰做三分）在 O(log n) 次函数求值内定位峰值；若是判符号存在性，可据峰值正负判断是否存在合法区域，避免完整枚举/实现厚重的原算法。

**Boundary**: 函数不是严格单峰（多峰/平台/离散噪声）时三分会收敛到局部；对浮点/精度敏感的凸问题，三分同样可能受误差影响。

**SourceRefs**: https://codeforces.com/blog/entry/61710

### 6. radewoosh-monotonic-binary-ternary

**Trigger**: 答案/可行性随参数单调，或目标函数凸/凹单峰；候选空间可排序计数、可二分阈值。

**Action**: 先写 check(x) 或目标 f(x)；单调则二分最小/最大可行 x，单峰则三分；对“最大单个代价”类目标显式转成阈值可行性判定；值域大时先压缩/乘积界。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/93568; https://codeforces.com/blog/entry/61710; https://codeforces.com/blog/entry/64543; https://codeforces.com/blog/entry/61331

### 7. radewoosh-incremental-dominant-color

**Trigger**: 需要枚举所有区间并统计每个区间的主导元素/众数；固定左端点后，右端点右移时只新增一个元素

**Action**: 固定左端点后，随 j 增加只更新 cnt[新颜色]；用当前 best 和 (cnt > cnt[best] 或 cnt == cnt[best] 且颜色编号更小) 的规则 O(1) 判断新主导色，每步给 answer[best] 加一

**Boundary**: 如果主导定义需要 top-k 或区间删除/两端伸缩，单变量 best 不充分；若每次新增元素会改变多个计数排序，需要更重的数据结构

**SourceRefs**: https://codeforces.com/blog/entry/44754

### 8. radewoosh-few-values-product-bound

**Trigger**: 要算 f(k) 对每个 k，且 f(k) 随 k 单调不增，同时 k·f(k) ≤ n 把答案值域压到 O(sqrt n) 个不同值

**Action**: 先用黑盒算一个 f，再通过二分找它保持不变的最远 k；已知区间两端值相等时整个区间不用再询问，递归/循环填充所有 k，总调用次数 O(sqrt n)

**Boundary**: 若 f 不单调、乘积界不成立，或黑盒 O(n) 不可接受/常数过大，不同值数量可能退化为 O(n)，该优化失效

**SourceRefs**: https://codeforces.com/blog/entry/61331

**SourceRefs（专家总来源）**: https://codeforces.com/profile/Radewoosh; https://codeforces.com/blog/entry/91608; https://codeforces.com/blog/entry/61331; https://codeforces.com/blog/entry/44754; $WORKSPACE/skills/teacher-consensus-skill/output/teacher_consensus_final.json; https://codeforces.com/blog/entry/93568; https://codeforces.com/blog/entry/61710; https://codeforces.com/blog/entry/43467; https://codeforces.com/blog/entry/64543