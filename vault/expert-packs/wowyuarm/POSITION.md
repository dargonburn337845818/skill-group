# wowyuarm（DSH Agent 团队协作 / dsh-agent-team 作者）

> 风格/方法论推断，非本人原话。

## 风格总述

多 Agent 协作要给人类一个持久、显式的组织骨架：Workspaces、Channels、Tasks 与受管 Agent 成员，而不是散落的临时会话；先写清领域模型与架构文档，再实现协作语义；让人来组织任务、让 Agent 协作执行。

## 结构化条目

**Trigger**: 组织多个 Agent 协作，或在 DSH 上做‘团队协作’而非单会话时

**Action**: 引入持久化的 Workspaces / Channels / Tasks 与受管 Agent 成员：给任务一个稳定归属与可恢复上下文，让协作不依赖单条聊天记录

**Boundary**: 持久化结构需要生命周期与清理策略；临时小任务不应被塞进重型 workspace 结构

**SourceRefs**: https://github.com/wowyuarm/dsh-agent-team; https://github.com/wowyuarm/dsh-agent-team/blob/HEAD/docs/domain-model.md

**Trigger**: 设计 Agent 团队协作语义、职责与状态机时

**Action**: 先输出领域模型与架构文档，把 Workspaces/Channels/Tasks/成员关系定义清楚，再实现；避免只靠 prompt 约定

**Boundary**: 显式建模也不等于过度工程；文档必须跟实现一致，否则成为负担

**SourceRefs**: https://github.com/wowyuarm/dsh-agent-team/blob/HEAD/docs/domain-model.md; https://github.com/wowyuarm/dsh-agent-team/blob/HEAD/docs/architecture.md

**Trigger**: 让人与 Agent 团队协作、安排任务流时

**Action**: 把人放在组织者位置：由人拆分任务、建立 channel/task，Agent 在其中协作执行并汇报；提供可观察的成员与任务状态

**Boundary**: 人机分工要保留人的否决与澄清权；不要让 Agent 静默推进高风险/不可逆操作

**SourceRefs**: https://github.com/wowyuarm/dsh-agent-team; https://www.npmjs.com/package/@wowyuarm/dsh-agent-team

## 来源纪律

所有条目均为风格/方法论推断，非本人原话；引用时保留 sourceRefs，具体协作语义与生命周期以仓库文档和真实运行为准。
