# y08lin4（DSH 多 Agent 协作预设 / dsh-multiagent-modes 作者）

> 风格/方法论推断，非本人原话。

## 风格总述

多 Agent 协作要‘分层且可切换’：提供均衡/高效等多档预设；子代理执行具体工作，主代理保持思维链不断；用预设把协作参数固化，避免每轮临时拼多 Agent。

## 结构化条目

**Trigger**: 设计/选用多 Agent 协作预设时

**Action**: 提供分档预设（如 balanced / efficient）：子代理负责干活，主代理保持主线思维；用预设固化角色、模型、工具与协作方式，而不是每轮临时拼装

**Boundary**: 预设是起点不是终点；任务复杂度与协作开销要匹配，简单任务不应强行多 agent

**SourceRefs**: https://github.com/y08lin4/dsh-multiagent-modes; https://github.com/y08lin4

**Trigger**: 在多档协作模式之间决策（质量 vs 速度）时

**Action**: 按任务目标选档：追求质量/复杂推理用均衡档，追求快速执行/机械任务用高效档；并让档位差异可见可配置

**Boundary**: 档位切换不能隐藏质量风险；关键结果仍需主代理或验证步骤确认

**SourceRefs**: https://github.com/y08lin4/dsh-multiagent-modes; https://github.com/y08lin4/163help

**Trigger**: 担心主代理上下文被并行子代理冲散、丢失主线时

**Action**: 让子代理做具体执行并把结论带回，主代理只保留思考主线；必要时后台执行、收口汇总，避免主代理被过程噪音淹没

**Boundary**: 后台/并行必须有收口、超时与深度上限；否则会养长期 child 或丢失子代理结果

**SourceRefs**: https://github.com/y08lin4/dsh-multiagent-modes; https://github.com/y08lin4

## 来源纪律

所有条目均为风格/方法论推断，非本人原话；引用时保留 sourceRefs，具体预设参数与协作效果以仓库文档和真实运行结果为准。
