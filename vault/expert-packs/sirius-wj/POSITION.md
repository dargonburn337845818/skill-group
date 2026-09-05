# SiriusWJ（DSH 更新器与文档同步 / dsh-updater-npm 作者）

> 风格/方法论推断，非本人原话。

## 风格总述

更新与同步要‘可看见’：一键更新但带进度、增量同步、前后检查；把官方文档做成 agent 可搜索/可读的工具，避免黑盒升级与离线盲操作。

## 结构化条目

**Trigger**: 需要升级 DSH 或 npm 包，担心‘升完坏了’时

**Action**: 提供一键更新但带实时进度、增量步骤与前后状态可见；升级前检查当前版本/来源，升级后保留可回滚信息，而不是静默替换

**Boundary**: 进度与友好 UI 不等于安全；跨 major/有生命周期脚本时仍需隔离冒烟与人工评审

**SourceRefs**: https://github.com/SiriusWJ/dsh-updater-npm; https://github.com/SiriusWJ

**Trigger**: 在 agent 会话中查 DSH 官方文档/搜索用法时

**Action**: 把官方文档做成增量同步 + 可搜索/可读工具（dsh_docs_search/read），让 agent 先查文档再动手，减少凭记忆硬编码

**Boundary**: 本地同步的文档可能滞后；关键 API/命令以当前安装版本的官方文档为准

**SourceRefs**: https://github.com/SiriusWJ/dsh-updater-npm; https://github.com/awesome-dsh-plugin/awesome-dsh-plugin

**Trigger**: 设计长时间运维操作（升级/同步/大批量处理）的体验时

**Action**: 显式显示进度、阶段与可重试点，让用户/agent 知道走到哪、失败在哪；把重试与恢复纳入设计

**Boundary**: 进度可见不能替代结果校验；最终要以真实启动/测试/冒烟收口

**SourceRefs**: https://github.com/SiriusWJ/dsh-updater-npm; https://github.com/Dominic789654/awesome-deepseek-harness

## 来源纪律

所有条目均为风格/方法论推断，非本人原话；引用时保留 sourceRefs，具体升级行为以官方文档和真实环境为准。
