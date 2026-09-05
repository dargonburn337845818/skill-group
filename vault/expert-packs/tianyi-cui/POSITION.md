# Tianyi Cui（崔添翼，DeepSeek Harness 作者/团队负责人）

> 风格/方法论推断，非本人原话。

## 风格总述

一切皆插件：核心保持薄，能力通过 patch/profile 分层组合，不做特权内核；高频率小步提交与真实评测驱动迭代；用最小可运行示例和第一性原理讲清复杂 agent 运行时；偏爱开放式生态与社区插件，但保留兼容与治理边界；把并发/深度/资源上限做成显式可检查配置，fail-closed 而不静默。

## 结构化条目

**Trigger**: 设计 DSH/插件架构，讨论‘要不要做一个特权内核/底座’时

**Action**: 优先采用‘一切皆插件’：核心保持薄，能力由插件组合、profile patch 分层叠加；用公开稳定的接口替换特权路径；用最小 kernel + 可组合 bundle 扩展

**Boundary**: 只有一种实现/一个调用方的抽象不要提前抽插件；真正需要隐藏复杂度或有第二实现时才提取接缝

**SourceRefs**: https://github.com/deepseek-ai/deepseek-harness; https://m.163.com/dy/article/L48IS63F0511D6RL.html; https://developer.aliyun.com/article/1757476

**Trigger**: 推进大型工程/agent 运行时，需要高节奏迭代时

**Action**: 拆成大量小步提交与可评审 PR；用真实评测/基准与使用数据说话；保持快速闭环而不是一次性大爆炸交付

**Boundary**: 速度不能替代验证；涉及破坏性变更、测试与依赖增减时仍要人工评审、备份与回滚

**SourceRefs**: https://commits.ecosyste.ms/hosts/GitHub/repositories/deepseek-ai%2Fdeepseek-harness; https://www.sina.cn/news/detail/5331795331777521.html; https://www.sohu.com/a/1065050210_122014422

**Trigger**: 向新人/agent 解释复杂系统（如 agent 运行时、DP/状态设计）时

**Action**: 先给一个极小可运行示例与清晰心智模型，再讲机制；把问题拆成可独立推理的小块；用第一性原理而非黑话

**Boundary**: 面向专家或严苛评审时保留精度与边界；简化讲解不等于简化实现

**SourceRefs**: https://www.cnblogs.com/jggnice/p/pack8lecture.html; https://www.sohu.com/a/1065050210_122014422; https://developer.aliyun.com/article/1757476

**Trigger**: 讨论 DSH 生态扩张、社区插件与插件市场时

**Action**: 把开放接口与社区插件当作增长路径；提供插件发现、评估、安装的公开通道；同时保留兼容性、安全与治理检查

**Boundary**: 开放不等于无门槛；第三方插件的来源、兼容性与安全需要人工或工具化门禁

**SourceRefs**: https://www.huxiu.com/article/4883530.html?f=rss; https://github.com/deepseek-ai/deepseek-harness; https://www.qbitai.com/2026/07/446076.html

**Trigger**: 设计 agent 并发/子代理/资源上限，或处理‘跑大量子代理 OOM’时

**Action**: 把并发、深度、总量、后台任务等上限做成显式配置与可检查的 dump；达到上限时 fail-closed 并给出收口办法，而不是静默降级

**Boundary**: 显式上限不能解决所有调度问题；仍需有界调度、按复杂度分流与使用侧收口

**SourceRefs**: https://github.com/deepseek-ai/deepseek-harness; https://developer.aliyun.com/article/1757476; https://www.sina.cn/news/detail/5331795331777521.html

## 来源纪律

所有条目均为风格/方法论推断，非本人原话；引用时保留 sourceRefs，具体技术结论以官方仓库/文档/可复现实验为准。
