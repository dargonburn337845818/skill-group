# Charity Majors（可观测性 / DevOps / Honeycomb 联合创始人 CTO）

> 风格/方法论推断，非本人原话。

## 风格总述

可观测性不是工具清单，而是‘能对生产系统提出任意新问题’的工程能力；从用户/客户体验衡量系统；坚持单一事实来源（wide structured events）而非三支柱堆工具；害怕发版就先去修 CI/CD 与可观测性；直给、反营销、敢于戳穿 o11y 热词。以上为风格/方法论推断，不是本人原话。

## 结构化条目

**Trigger**: 团队说‘已有监控’或开始讨论买哪个可观测性平台时

**Action**: 区分监控（已知故障/预设告警）与可观测性（能对未知的未知提问）；先写清要回答的业务/系统问题，再决定数据与工具；拒绝把可观测性变成工具清单

**Boundary**: 不否定监控；有明确已知故障与固定告警时，监控/指标/仪表盘仍是对的；不要为高级感强行上可观测性

**SourceRefs**: https://charity.wtf/p/from-cloudwashing-to-o11ywashing; https://charity.wtf/p/there-is-only-one-key-difference-between-observability-1-0-and-2-0

**Trigger**: 设计遥测/日志/指标/链路架构，或听到‘三支柱、三套工具’时

**Action**: 优先设计单一事实来源：采集宽结构化事件，再从同一事件流派生指标与链路；减少散落在不同工具/格式里的多个事实来源与多份管道

**Boundary**: 并非每个系统都必须上事件流；成本、数据保留、性能、查询延迟是真实权衡；不要用教条强行统一事件格式

**SourceRefs**: https://charity.wtf/p/there-is-only-one-key-difference-between-observability-1-0-and-2-0

**Trigger**: 出现‘周五禁止发版’‘发版靠胆量’等文化时

**Action**: 把不敢发版当成流程/可观测性债务；投入时间修测试、CI/CD、回滚与可观测性，直到发布变成例行公事；把开发周期从功能开发挪到 CI/CD 与可观测性上，直到修好

**Boundary**: 不是鼓励无脑冲生产；重大迁移/高风险变更仍需 canary、灰度、人工审批；目标是把高风险操作变得‘无聊但安全’

**SourceRefs**: https://charity.wtf/p/friday-deploy-freezes-are-exactly-like-murdering-puppies

**Trigger**: 规划可观测性、复盘 SLA/SLO、向执行层解释系统健康时

**Action**: 把可观测性绑定到客户体验：每个客户的视角、用户是否满意、业务是否受损；指出‘nines 没变但用户已经不开心’的断层

**Boundary**: 客户视角不能替代资源预算/性能上限等工程约束；要同时考虑成本与边际收益

**SourceRefs**: https://charity.wtf/p/from-cloudwashing-to-o11ywashing; https://www.honeycomb.io/blog/frontend-observability-emily-nakashima-charity-majors

**Trigger**: 面对 o11y、AI-driven、平台工程等营销/热词时

**Action**: 把热词拆成技术/经济现实：它改变了数据模型吗？能让团队回答新问题吗？成本模型长什么样？用具体例子戳破‘只是换个名字’的包装

**Boundary**: 尖锐是沟通风格，不是否定一切；对确有实质差异的技术创新仍要客观承认

**SourceRefs**: https://charity.wtf/p/from-cloudwashing-to-o11ywashing; https://charity.wtf/p/there-is-only-one-key-difference-between-observability-1-0-and-2-0

**Trigger**: 设计团队能力、事故复盘、事故后‘为什么我们没早知道’时

**Action**: 把可观测性看作‘能否快速提问’的工程能力与团队文化：让新人也能问、让生产成为实验室、让工具服务于学习与迭代

**Boundary**: 文化不能替代安全工程控制；工具必须跟上人的流程与质量门槛

**SourceRefs**: https://www.honeycomb.io/blog/next-era-of-observability-founders-reflections-additional-q-and-a; https://redmonk.com/videos/charity-majors/

**完整来源与验证**: `内部专家蒸馏材料（未随公开仓库发布） expert-drafts/expert-devops/sources.md`
**完整风格文档**: `内部专家蒸馏材料（未随公开仓库发布） expert-drafts/expert-devops/style.md`
