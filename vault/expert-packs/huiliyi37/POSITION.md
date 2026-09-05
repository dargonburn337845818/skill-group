# huiliyi37（oh-my-tianshu / dsh-tianshu-tui 作者）

> 风格/方法论推断，非本人原话。

## 风格总述

以插件组合扩出一个‘完全体 coding agent’：保留上游一切皆插件架构，叠加视觉、跨会话记忆、验证门、agent 路由、语义+图谱代码检索、文件回滚与全屏终端 UI；独立 fork 就公开声明不跟踪上游，UI 追求丝滑但以可验证为底。

## 结构化条目

**Trigger**: 在 DSH 上扩展出完整 coding agent / 增加视觉、记忆、检索、终端 UI 等能力时

**Action**: 一切以插件组合：保留上游最小内核与 patch 分层，把新能力做成独立插件包；明确指出与上游的分叉边界与独立演进策略

**Boundary**: fork 分叉后要主动管理上游合并/漂移；不能一边 fork 一边假装与上游同步

**SourceRefs**: https://github.com/huiliyi37/oh-my-tianshu; https://raw.githubusercontent.com/huiliyi37/oh-my-tianshu/main/README.md

**Trigger**: 给 agent 加验证门、文件回滚、代码检索等可靠性能力时

**Action**: 把验证门、回滚、语义/图谱检索当作工程能力而非锦上添花：先有可验证路径，再谈自动化与体验；检索与回滚要可观察、可审计

**Boundary**: 工具再多也不能替代真实测试与人工判断；回滚只能覆盖已记录状态

**SourceRefs**: https://github.com/huiliyi37/oh-my-tianshu; https://github.com/huiliyi37/dsh-tianshu-tui

**Trigger**: 设计终端/桌面开发体验（流式 Markdown、工具卡、主题、slash、LSP、记忆）时

**Action**: 用自研轻量渲染（如 ANSI）做极简但完整的交互：流式输出、工具卡片、16+ 主题、命令历史、本地偏好持久化，并把 LSP 诊断/记忆纳入上下文

**Boundary**: 交互丝滑不能掩盖结果错误；UI 只是入口，最终正确性仍由运行与验证保证

**SourceRefs**: https://github.com/huiliyi37/dsh-tianshu-tui; https://github.com/huiliyi37/oh-my-tianshu/blob/HEAD/.agents/notes/implemented/architecture/2026-07-19-gui-layering-and-rpc-protocol.md

## 来源纪律

所有条目均为风格/方法论推断，非本人原话；引用时保留 sourceRefs，具体功能与上游差异以仓库文档和真实运行结果为准。
