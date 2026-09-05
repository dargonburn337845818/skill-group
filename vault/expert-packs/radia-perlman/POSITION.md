# Radia Perlman（网络协议设计 / 桥接与生成树 / 网络安全）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 立场概要

协议设计从失败模式与拓扑变化出发：先列出链路断、节点宕、环路、恶意/误配置等假设，再看算法是否依赖单点/固定拓扑；网络协议安全默认不信任参与者，显式建模信任边界。

## 结构化条目

**Trigger**: 设计/评审局域网、桥接、生成树、路由或交换网络协议时

**Action**: 先列出失败模式：链路断、节点宕、拓扑成环、广播风暴、误配置；检查协议是否依赖单一中心或固定拓扑；验证环路防制（如 STP）、收敛、通告与恢复机制。

**Boundary**: 规范正确不等于实现正确；厂商实现可能有默认差异。

**SourceRefs**: https://en.wikipedia.org/wiki/Radia_Perlman ; https://books.google.com/books?id=AIRitf5C-QQC

**Trigger**: 网络协议安全、路由劫持、DNS/ARP 欺骗、中间人、恶意/误配置场景时

**Action**: 把协议参与者当潜在对手：默认不信任，显式设计认证、防欺骗、防劫持与信任模型；检查数据面与控制面的安全边界。

**Boundary**: 协议安全需结合部署、密钥管理与运维；单靠算法无法解决全部威胁。

**SourceRefs**: https://en.wikipedia.org/wiki/Radia_Perlman ; https://books.google.com/books?id=AIRitf5C-QQC
