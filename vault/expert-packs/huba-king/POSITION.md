# HubaKing（DSH 社区插件生态指南 / dsh-community-plugins 作者）

> 风格/方法论推断，非本人原话。

## 风格总述

把‘发现、评估、安装社区插件’流程化并教给 agent：先找可信来源，再评估来源与兼容性，最后按可验证步骤安装；生态知识应固化成可复用 skill，避免凭感觉装插件。

## 结构化条目

**Trigger**: agent 需要发现/评估/安装 DSH 社区插件时

**Action**: 先查 GitHub dsh-plugin topic、dshmarket 与 npm 等公开入口；对照项目说明、更新时间、维护状态与兼容信息做评估；再按可追溯步骤安装，来源不明确时停下说明风险

**Boundary**: 自动化评估不能替代人工安全审查；高危/未验证插件不应因为‘流程顺’就装

**SourceRefs**: https://github.com/HubaKing/dsh-community-plugins; https://raw.githubusercontent.com/HubaKing/dsh-community-plugins/main/README.md

**Trigger**: 想把 DSH 生态经验沉淀成 agent 可调用的知识时

**Action**: 做成一个注册到 DSH 的全局 skill：包含发现、评估、安装的检查清单与反例，让 agent 遇到‘找插件/装插件’任务时自动按清单走

**Boundary**: skill 要随生态更新；不能把单一时点的仓库列表当成长期权威

**SourceRefs**: https://github.com/HubaKing/dsh-community-plugins; https://github.com/wgd753/awesome-dsh-plugin

**Trigger**: 面对插件生态信息分散、来源质量参差时

**Action**: 依赖公开 registry/awesome 列表做横向收集，但把每个插件的来源、描述、状态保留可审计；鼓励社区共同维护生态目录

**Boundary**: 收录不等于背书；目录/列表只负责可见性，责任判断仍在安装者

**SourceRefs**: https://github.com/wgd753/awesome-dsh-plugin; https://github.com/dshworks/awesome-dsh-plugins

## 来源纪律

所有条目均为风格/方法论推断，非本人原话；引用时保留 sourceRefs，具体安全与兼容结论以官方文档和实际验证为准。
