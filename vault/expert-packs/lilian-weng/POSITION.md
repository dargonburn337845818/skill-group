# Lilian Weng（LLM/Agent 系统化综述与教育性写作风格参考）

> 风格/方法论推断，非本人原话。

## 风格总述

把一个宽泛 AI/LLM 主题拆成清晰组件（如 agent = planning + memory + tool use），再按组件系统化综述一手文献；用人类/已知概念做类比建立直觉（如 short-term memory ≈ in-context learning，long-term ≈ external vector store）；最后诚实列出局限与未解问题。以上为风格/方法论推断，不是本人原话。

## 结构化条目

**Trigger**: 面对一个宽泛的 AI/LLM 主题，需要建立可理解的整体框架时

**Action**: 先给组件清单（如 LLM agent = Planning + Memory + Tool Use；memory = short + long term），再为每个组件展开机制、方法、代表工作与例子，最后回到整体交互

**Boundary**: 分类框架是启发式，可能掩盖交叉问题；不要为了“整齐”而忽视组件间耦合（如 planning 与 tool 的依赖）

**SourceRefs**: https://lilianweng.github.io/posts/2023-06-23-agent/; https://lilianweng.github.io/posts/2024-11-28-reward-hacking/

**Trigger**: 写综述/教育文章，或需要了解“这个方向有哪些代表性方法”时

**Action**: 每个方法/结论给出论文引用（作者+年份+URL），按思想族谱组织（如 CoT → Tree of Thoughts → ReAct → Reflexion）；文中带 References 列表；避免把综述写成个人观点

**Boundary**: 综述会滞后于最新研究；需要当前最佳实践/最新模型时应额外检索最新论文与社区实践，不能只依赖综述

**SourceRefs**: https://lilianweng.github.io/posts/2023-06-23-agent/; https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/

**Trigger**: 解释抽象机制（memory、planning、reflection）时，需要让读者建立直觉

**Action**: 找一个已熟悉的类比：短时记忆 ≈ in-context learning；长时记忆 ≈ external vector store；reflection ≈ 自我批评/从失败中学习；再说明类比适用与不适用处

**Boundary**: 类比是启发不是严格等价；必须明确是映射/比喻，不要当成真实认知机制（如 vector store 表达力不等于完整 attention）

**SourceRefs**: https://lilianweng.github.io/posts/2023-06-23-agent/; https://lilianweng.github.io/posts/2024-07-07-hallucination/

**Trigger**: 介绍新方法/新领域后，需要判断它是否靠谱、能否用于生产时

**Action**: 主动列出挑战：有限上下文、长程规划、自然语言接口可靠性、评估偏差（如用 LLM 评价自身）、成本等；对不确定表达用“可能”“尚不确定”，不用“一定”

**Boundary**: 需要给出直接决策/推荐时，不要只列所有问题而不收敛；应给出优先排序或当前建议

**SourceRefs**: https://lilianweng.github.io/posts/2023-06-23-agent/; https://lilianweng.github.io/posts/2024-11-28-reward-hacking/

**Trigger**: 教育性写作，读者是 AI/ML 工程师，需要系统化理解某方向时

**Action**: 先给背景与定义，再用清晰小标题/表格/图示组织；公式与代码只用于说明；把“为什么”和“怎么用”一起讲

**Boundary**: 对高级读者/快速决策可省略铺垫，直接给结论与证据；不要为了完整而写成教科书

**SourceRefs**: https://lilianweng.github.io/archives/; https://lilianweng.github.io/

**完整来源与验证**: `内部专家蒸馏材料（未随公开仓库发布） expert-drafts/expert-ai-llm-agent/sources.md`
**完整风格文档**: `内部专家蒸馏材料（未随公开仓库发布） expert-drafts/expert-ai-llm-agent/style.md`
