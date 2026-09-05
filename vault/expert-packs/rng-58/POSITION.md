# rng_58（AtCoder 核心成员/命题人） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

AtCoder 命题哲学与算法设计视角，强调可解释性、构造与竞赛节奏

## 结构化条目（style_items）

### 1. rng-58-read-model-reformulate

**Trigger**: 读题或卡壳时，限制不自然、术语可疑、目标函数易误读，或看到题面就想套算法。

**Action**: 先系统自问“为什么有这个限制/去掉会怎样/有什么不寻常”，把题面重述成纯数学模型或标准问题；确认非标准术语定义与目标函数类型；再决定选用什么工具。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/113785; https://codeforces.com/blog/entry/142536; https://codeforces.com/blog/entry/64543; https://codeforces.com/blog/entry/62730

### 2. rng-58-library-as-oracle

**Trigger**: 题目核心在思考/构造，但其中需要调用一个已知但实现复杂的算法或数据结构（如卷积、匹配、带 lazy 的线段树）时

**Action**: 把该算法封装成可信的库/oracle，只写调用代码；不花时间重复实现或调常数，把精力留给模板之外的真正思维部分

**Boundary**: 没有可靠库/模板，或题目需要大量定制、调常数/精度时，黑盒化反而增加调试成本；对‘粘贴模板后还要继续实现’的纯库题也不适用

**SourceRefs**: https://codeforces.com/blog/entry/82400

### 3. rng-58-practice-design-delayed-feedback

**Trigger**: 制定长期训练计划、选择练习难度、决定是否看题解、评价长期水平。

**Action**: 选“略高于当前但可能做出”的题；不读题解、隔月再回来；把“学会新题”和“比赛变快”分成两条训练轨道；讨论多个错误想法；用相对排名而非绝对 rating 衡量长期水平。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/98806; https://codeforces.com/blog/entry/82401

### 4. rng-58-thinking-vs-implementation-split

**Trigger**: 评估一道题是否值得做、难度多大，或出题人挑选题目时，容易把‘实现复杂’和‘思考困难’混在一起

**Action**: 把题目成本拆成思维量和实现量两维（实现量可以排除库部分）；优先投入思维量高、实现量小的题，而降低‘主要靠粘贴复杂模板后继续实现’的题的目标

**Boundary**: 赛前往往无法准确预估思维量与实现量；禁止用库/模板或必须自写底层实现时，实现量必须重新计入，二维分解会失真

**SourceRefs**: https://codeforces.com/blog/entry/82400

### 5. rng-58-reusable-blackbox-abstraction

**Trigger**: 某类内容/实现/问题反复出现且每次完整展开成本高、信息量低，而重复的本质不是当前思考核心

**Action**: 先识别能否把其压缩成可复用对象：题面剥离成纯数学模型，复杂算法封装成库/oracle，常见问题沉淀为资源链接；之后直接使用该抽象，把精力留给真正需要思考/建模/实现的部分

**Boundary**: 高度具体或个性化问题不能泛化；抽象可能过时或隐藏关键线索（如故事本身是转化提示）；需要大量定制/调常数时黑盒化反而增加调试成本

**SourceRefs**: https://codeforces.com/blog/entry/62730; https://codeforces.com/blog/entry/71349; https://codeforces.com/blog/entry/82400

### 6. rng-58-contest-strategy-parallel

**Trigger**: 多题赛/锁头赛/团队赛，需要决定做题顺序、时间分配，或单题卡住想切换。

**Action**: 先通读全部题，用点值/公告/榜上时间校准难度；按赛制收益与对手状态排序；卡题时切换题目，回来换新角度；相似题记忆召回作为候选并先验证。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/72557; https://codeforces.com/blog/entry/65099; https://codeforces.com/blog/entry/53457

### 7. rng-58-problem-nature-first-no-anchor

**Trigger**: 面对题目或选择训练题时，容易因标签、库名、常见算法名过早锁定解法/难度；或者把'思维难'与'实现难'混为一谈，导致训练目标错位。

**Action**: 先把问题按自身结构做'类型/成本'预分类：是 ad-hoc/思维题还是教育型/套路题？主要成本在思考还是实现？同时警惕从规模、标签、算法库名反向锁定解法；把算法、库、标签当作候选工具而非解题前提。先开放地列出候选方向，再做类型识别，最后选实现工具。

**Boundary**: 在时间紧、专题赛或裸模板题中，标签、库名、算法预判可能是有效信号；完全不用会浪费效率。对需要快速熟悉模板或明确算法覆盖的训练，也应保留专题模式。

**SourceRefs**: https://codeforces.com/blog/entry/113785; https://codeforces.com/blog/entry/82400; https://codeforces.com/blog/entry/82401

### 8. rng-58-no-library-anchor

**Trigger**: 在已知附带算法库/专题的比赛中，读题后容易先想‘这题要用哪个库’，把解法框死在库名上

**Action**: 把库当作可选工具，但仍从题面本身的问题结构出发；不先假设‘这题要求某库，所以解法应该…’，保持解法开放

**Boundary**: 当题目确实是某算法的裸模板、或库名是解法唯一强线索时，完全不做库联想会浪费时间；专题赛中库名也常是有效信号，不能一律无视

**SourceRefs**: https://codeforces.com/blog/entry/82400

**SourceRefs（专家总来源）**: https://codeforces.com/profile/rng_58; https://codeforces.com/blog/entry/82401; https://codeforces.com/blog/entry/65099; https://codeforces.com/blog/entry/61066; $WORKSPACE/skills/teacher-consensus-skill/output/teacher_consensus_final.json; https://codeforces.com/blog/entry/113785; https://codeforces.com/blog/entry/142536; https://codeforces.com/blog/entry/64543; https://codeforces.com/blog/entry/62730; https://codeforces.com/blog/entry/82400; https://codeforces.com/blog/entry/98806; https://codeforces.com/blog/entry/71349; https://codeforces.com/blog/entry/72557; https://codeforces.com/blog/entry/53457