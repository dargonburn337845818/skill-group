# ninipa（DSH 专家子代理预设 / oh-my-dsh-slim 作者）

> 风格/方法论推断，非本人原话。

## 风格总述

复杂 agent 任务先拆成明确角色，再按角色分配合适的模型、effort、工具过滤与作用域 MCP；让子代理干活、主代理保持思维链，并优先后台委派。

## 结构化条目

**Trigger**: 把复杂任务委派给子代理，或设计多角色 agent 团队时

**Action**: 先定义 orchestrator 与少数专业角色（如 oracle/designer/fixer/explorer/librarian），每个角色有明确职责、模型/effort、工具过滤与作用域 MCP；不要一个万能子代理干所有事

**Boundary**: 角色过多会带来编排开销与上下文碎片；小任务用普通子代理或直接做更快

**SourceRefs**: https://github.com/ninipa/oh-my-dsh-slim; https://github.com/ninipa

**Trigger**: 决定子代理用哪种模型/effort，或担心成本与质量失衡时

**Action**: 按角色与任务复杂度分流：机械/只读用便宜模型 + 收敛工具集；疑难/关键决策用高 effort；把工具过滤与 MCP 作用域做成角色级配置

**Boundary**: 成本优化不能牺牲正确性；关键路径上仍要有验证与人工门禁

**SourceRefs**: https://github.com/ninipa/oh-my-dsh-slim; https://github.com/awesome-dsh-plugin/awesome-dsh-plugin

**Trigger**: 担心主 agent 被并行/后台子代理带偏思路时

**Action**: 让子代理后台执行并负责具体工作，主代理保留主线思维；用明确的收口/汇总机制把结果带回来

**Boundary**: 后台委派必须有收口与超时/深度上限；否则会养出长期 resident child 或失联子代理

**SourceRefs**: https://github.com/ninipa/oh-my-dsh-slim; https://github.com/Dominic789654/awesome-deepseek-harness

**Trigger**: 把已有 agent 预设迁移/移植到 DSH 时

**Action**: 以已知成熟预设为起点（如 oh-my-opencode-slim），做职责裁剪与 DSH 能力适配：保留角色骨架，替换模型/工具/MCP 到目标运行时可支持的范围

**Boundary**: 移植不等于复制；必须适配目标运行时的工具、权限与并发模型，并进行真实验证

**SourceRefs**: https://github.com/ninipa/oh-my-dsh-slim; https://github.com/alvinunreal/oh-my-opencode-slim

## 来源纪律

所有条目均为风格/方法论推断，非本人原话；引用时保留 sourceRefs，具体预设参数以仓库文档和真实运行结果为准。
