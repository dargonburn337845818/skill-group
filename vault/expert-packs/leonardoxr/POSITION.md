# leonardoxr（DSH 子代理路由 / 原生客户端 / 更新器作者）

> 风格/方法论推断，非本人原话。

## 风格总述

子代理按任务复杂度路由到不同运行时档位，而不是一刀切；给外部/原生客户端提供受控的只读接口与可信 HTTPS 入口；更新检测要显式提示、可一键通道更新但保持可回退。

## 结构化条目

**Trigger**: 决定子代理用哪个运行时/档位，或避免‘所有任务都套同一子代理’时

**Action**: 按任务复杂度路由：让模型为每个任务选运行时 tier；提供按调用挂载任意 preset、每次调用可覆盖模型/提供方，并带模型可用性预检

**Boundary**: 路由不能变成静默降级；预检失败要显式报错或换用确认过的方案，不能假装成功

**SourceRefs**: https://github.com/leonardoxr/dsh-routed-subagent; https://github.com/leonardoxr

**Trigger**: 为 DSH 做桌面/iOS/原生客户端或外部工具接入时

**Action**: 优先信任的 HTTPS Web 入口 + 保存服务器 + 第一方 DSH 支持；暴露只读 workspace/session JSON API，供客户端读取而不做危险写操作

**Boundary**: 只读接口也要鉴权与最小暴露；不要为了‘方便’开放可写入、可执行的高权限通道

**SourceRefs**: https://github.com/leonardoxr/dsh-native; https://github.com/leonardoxr/dsh-companion

**Trigger**: 处理 DSH 版本更新、订阅更新渠道时

**Action**: 提供更新检测：发现新版本显式提示，支持一键按渠道更新；更新前保留当前版本与通道信息，更新后验证可用

**Boundary**: 一键更新不等于零风险；跨 major/运行中 agent 仍应隔离冒烟、备份并等无 running agent

**SourceRefs**: https://github.com/leonardoxr/dsh-harness-updater; https://github.com/leonardoxr/dsh-routed-subagent

## 来源纪律

所有条目均为风格/方法论推断，非本人原话；引用时保留 sourceRefs，具体路由/更新行为以仓库文档和真实环境为准。
