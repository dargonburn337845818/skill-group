# ecnerwala（美国顶尖选手） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

反向扫描/线性化/数据结构推导；喜欢用精确实现和均摊结构把论文式做法落地

## 结构化条目（style_items）

### 1. ecnerwala-median-fixed-bitonic-search

**Trigger**: 从排序数组中选子集最大化某个含中位数的统计量；固定一个中间元素后，子集大小 j 每增加 1 只会加入两侧各一个元素，且新增元素随 j 单调变差

**Action**: 先证明最优子集大小限制（如奇数），固定中位数位置，贪心选两侧最大的 j 个；观察新增边际量随着 j 单调变化，从而把枚举 j 变成在边际量上的二分/三分

**Boundary**: 如果边际增量不单调、目标有多峰，或偶数大小/多个中位数的情形使固定中位数不成立，则二分/贪心会漏解

**SourceRefs**: https://codeforces.com/blog/entry/23522

### 2. ecnerwala-greedy-future-cheaper-station

**Trigger**: 线性路径上带油箱容量、各站油价不同的最小购油成本；只要知道前方是否有更便宜的油站，当前站买多少就有贪心决策

**Action**: 在每一站只买到能到达下一个更便宜/相同油站的油量；若当前油箱范围内没有更便宜的站，就加满。等价地，维护最近 n 距离内最便宜的油并让每一单位油由最低价供给

**Boundary**: 如果价格可以波动且允许回头/绕路，或油耗/距离不是简单线性，则‘只买到下一更便宜站’不再最优；实现上若无法快速求下个更便宜站也需额外数据结构

**SourceRefs**: https://codeforces.com/blog/entry/43467

### 3. ecnerwala-gas-station-cheaper-next-greedy

**Trigger**: 线性路径上带油箱容量、各站油价不同的最小购油成本；只需要知道前方是否有更便宜的油站即可决定当前站买多少。

**Action**: 在每一站只买到能到达下一个更便宜/相同油站的油量；若油箱范围内没有更便宜站，就加满。等价地维护最近 n 距离内最低价，让每一单位油由最低价供给。

**Boundary**: 若价格可波动且允许回头/绕路，或油耗/距离不是简单线性，'只买到下一更便宜站'不再最优；实现上需快速求下个更便宜站。

**SourceRefs**: https://codeforces.com/blog/entry/43467

### 4. ecnerwala-binary-search-tree-dp-prefix

**Trigger**: 在树上/DFS 序上要求一个可行前缀满足阈值，且答案随阈值单调；判定一个问题可以交给树形 DP

**Action**: 二分阈值 v；对每个子树分别算出‘整棵子树都合格’或‘从子树开头能延伸的最长合格前缀’；从根合并时，全合格子树大小相加，再取一个最大的部分合格子树前缀，检查能否达到 k

**Boundary**: 如果 check(v) 不单调、DFS 遍历顺序可任意变化导致前缀不是简单子树拼接，或一个子树需要两个以上部分前缀，则贪心树 DP 不够

**SourceRefs**: https://codeforces.com/blog/entry/43467

### 5. ecnerwala-monotone-bitonic-binary-ternary-search

**Trigger**: 问题中有一个可排序/可计数的搜索空间（候选集、答案 t、阈值 k、中位数规模 j），且可行性或目标值随参数单调，或函数本身凸/凹因此单峰；需要找最优/最左可行解而不是枚举全部。

**Action**: 把搜索空间压到二分/三分：先写出 check(x) 或目标 f(x)。若判定随 x 单调，则二分最小/最大可行 x；若 f 单峰则三分（或二分边际量）找极值。交互类可把候选排全序后查中间位；具体 check 按问题构造，如贪心排序取前 k、树形 DP 维护最长合格前缀、拓扑定向验证无环、比例不等式等。

**Boundary**: 若 check 不单调、函数多峰/平台/离散噪声、候选无法快速计数排序，或单次检查代价极高，二分/三分剪枝会失效或收益有限。三分对浮点精度、非严格单峰也需要谨慎。

**SourceRefs**: https://codeforces.com/blog/entry/93568; https://codeforces.com/blog/entry/61710; https://codeforces.com/blog/entry/43467; https://codeforces.com/blog/entry/64543

### 6. ecnerwala-group-as-interval-open-dp

**Trigger**: 把元素分组，代价只由每组最大/最小值决定（如组内极差）；排序后每组可看作一个区间，总代价等于所有单位间隙被覆盖的次数之和

**Action**: 把元素排序，把每组看成一个 [min,max] 区间，用“当前有多少个区间已经打开但未关闭”作为 DP 状态；处理每个元素时先按开放区间数累加跨过空隙的代价，再决定单组/开启/加入/关闭

**Boundary**: 如果分组代价依赖组内更多结构（如次大值、内部顺序）或区间覆盖公式不成立，开放区间 DP 状态不够

**SourceRefs**: https://codeforces.com/blog/entry/23522

### 7. ecnerwala-xor-add-bitwise-count

**Trigger**: 给出 a+b=s 与 a^b=x（或类似双约束），需要求 (a,b) 的数量/存在性；位运算与普通加法之间存在精确关系

**Action**: 用 a+b = (a^b) + 2*(a&b) 先解出 a&b；再按每个二进制位独立分析：x 位为 0 时 a、b 只能同为 AND 位，x 位为 1 时 a、b 必相反且 AND 位必须为 0，最后乘起来并排除边界

**Boundary**: 当 (s-x)/2 不是整数、或某些位要求 AND 与 xor 冲突时无解；若存在多个相互耦合的加法/异或约束，逐位独立性会被破坏

**SourceRefs**: https://codeforces.com/blog/entry/43467

### 8. ecnerwala-monotonic-binary-ternary

**Trigger**: 答案/可行性随参数单调，或目标函数凸/凹单峰；候选空间可排序计数、可二分阈值。

**Action**: 先写 check(x) 或目标 f(x)；单调则二分最小/最大可行 x，单峰则三分；对“最大单个代价”类目标显式转成阈值可行性判定；值域大时先压缩/乘积界。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/93568; https://codeforces.com/blog/entry/61710; https://codeforces.com/blog/entry/64543; https://codeforces.com/blog/entry/61331

**SourceRefs（专家总来源）**: https://codeforces.com/profile/ecnerwala; https://codeforces.com/blog/entry/43467; https://codeforces.com/blog/entry/90011; $WORKSPACE/skills/teacher-consensus-skill/output/teacher_consensus_final.json; https://codeforces.com/blog/entry/23522; https://codeforces.com/blog/entry/93568; https://codeforces.com/blog/entry/61710; https://codeforces.com/blog/entry/64543; https://codeforces.com/blog/entry/61331