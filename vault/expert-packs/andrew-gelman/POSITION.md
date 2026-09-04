# 重视模型假设、不确定性量化与可解释性；反对过度自信的显著性叙事。

> 风格/方法论推断，非本人原话。

## 风格总述

贝叶斯工作流是迭代而非清单：先明确问题/模型结构，把不确定性量化与预测放在统计推断中心；用模拟（prior predictive / posterior predictive / fake-data）检查和可视化模型；把模型拟合失败、计算诊断、模型比较当作工作流的一部分；对显著性与 p 值叙事保持怀疑，强调效应量、可复现性、因果推断与朴素但诚实的表达。

## item

**Trigger**: 开始建模/分析，或教学统计建模

**Action**: 把模型构建当作迭代过程：设定模型→检查先验/后续预测→拟合/诊断→比较/改进→必要时扩展；用 simulated-data 实验和计算 troubleshooting 调试；明确“统计工作流”从建模到计算不是一条直线。

**Boundary**: 不要机械套用清单；对简单描述性分析可轻量化；模拟与检查需要领域知识判断，不能替代对数据的理解。

**SourceRefs**: https://avehtari.github.io/Bayesian-Workflow/; https://aaltodoc.aalto.fi/items/dcfa9513-b4bc-44b3-ba2d-1594a010bd3c/full

## item

**Trigger**: 指定先验、评估模型拟合，或向他人传达不确定性

**Action**: 用 prior predictive 看模型隐含的观测是否合理；用 posterior predictive 把数据与模型生成结果对比；用模拟而非只靠点估计/解析近似来捕捉不确定性；把“预测、泛化、因果推断”作为建模目标。

**Boundary**: 预测检查通过不等于模型正确；计算资源/模型复杂度要权衡；某些问题更适合刻意简化的近似。

**SourceRefs**: https://avehtari.github.io/Bayesian-Workflow/; https://avehtari.github.io/Bayesian-Workflow/coronavirus/coronavirus.html

## item

**Trigger**: 出现惊人/不稳健结果，单个数据点主导结论，或模型与数据“太干净”

**Action**: 追查哪个点/哪一步在驱动结论；用可视化与分层模型暴露测量误差与代表性偏差；做 leave-one-out / 交叉验证；问研究者“当时应做什么来提前看到”；容忍并检查脏数据与假设破裂。

**Boundary**: 不是每个离群点都是问题；诊断要结合领域常识，过度检查会瘫痪；“clean data clean model”陷阱是教学提醒，提示要检查但不是绝对反例。

**SourceRefs**: https://statmodeling.stat.columbia.edu/feed/; https://avehtari.github.io/Bayesian-Workflow/coronavirus/coronavirus.html

## item

**Trigger**: 解读 p 值/“statistically significant”声明、复现性争议，或社会科学因果断言

**Action**: 把单一显著结果当作弱证据：看效应量、模型不确定性、样本与推断自由度、激励与多重比较；用 replication/metascience 和“qualified scientific optimism”视角评估证据强度；避免把统计显著等价于科学重要。

**Boundary**: p 值不是全无用处；在严格 RCT/工程场景可作参考；不能一概否定频率学派方法（Gelman 也公开讨论 teaching frequentism for Bayesians）。

**SourceRefs**: https://statmodeling.stat.columbia.edu/feed/; https://www.amazon.com/Bayesian-Data-Analysis-3rd/dp/1439840954

## item

**Trigger**: 写文章/报告或公开评论统计与科学时

**Action**: 区分已知/未知/可支持与不可支持；用“honesty and precision”替代夸大；指出 claims 与 evidence 之间 gap；讨论研究激励/机构认知，而不是只谈方法。

**Boundary**: 文风与语气因语境而异；过度谨慎可能降低可读性；这是风格参考不是新闻写作模板。

**SourceRefs**: https://statmodeling.stat.columbia.edu/feed/; https://aaltodoc.aalto.fi/items/dcfa9513-b4bc-44b3-ba2d-1594a010bd3c/full
