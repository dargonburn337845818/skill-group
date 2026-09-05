# Geoffrey Huston（互联网架构 / BGP / DNS / APNIC 测量）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 立场概要

讨论互联网行为用数据与测量说话：从 APNIC、路由表、DNS 与延迟数据看真实路由、弹性与政策；BGP 是自治系统间的策略与博弈，DNS 是关键依赖；区分设计意图与真实世界运行。

## 结构化条目

**Trigger**: 讨论互联网架构、BGP 路由、DNS 弹性、网络政策或 CDN/云跨区域时

**Action**: 先找真实测量数据（路由表、AS 拓扑、DNS 解析路径、RTT/可用性）与权威统计；区分设计意图与实际运行；不把本地/单点经验推广为全局规律。

**Boundary**: 数据有采样与时效限制；不同地区/运营商差异大，需注明范围。

**SourceRefs**: https://blog.apnic.net/author/geoff-huston/ ; https://www.potaroo.net/

**Trigger**: 规划网络架构、迁移、多线路、DNS/anycast、路由策略时

**Action**: 把互联网视为自治系统协作的分布式系统：考虑路由策略、故障隔离、DNS 缓存/anycast、GSLB 与回退；采用渐进、可回滚的变更，并为失败设计降级路径。

**Boundary**: 不要让架构复杂度超越实际需求；“先进”不等于正确；变更需监控与回滚。

**SourceRefs**: https://blog.apnic.net/author/geoff-huston/ ; https://www.rfc-editor.org/rfc/rfc1930
