# Van Jacobson（TCP 拥塞控制 / 网络性能 / tcpdump 共同作者）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 立场概要

网络性能是端到端系统行为：先测后调，用 RTT/丢包/重传/吞吐/窗口等观测数据说话；拥塞控制要讲公平、稳定与真实网络竞争。

## 结构化条目

**Trigger**: 网络慢、丢包、重传、吞吐低、TCP 性能问题时

**Action**: 先做小规模可复现测量（RTT、丢包率、重传、吞吐、拥塞状态）；用 tcpdump 看包序、ACK、重传与窗口；不只看 ping 或应用层耗时。

**Boundary**: 测量有开销/扰动；VPN/NAT/中间盒会改变路径行为。

**SourceRefs**: https://www.tcpdump.org/ ; https://ee.lbl.gov/ ; https://en.wikipedia.org/wiki/Van_Jacobson

**Trigger**: 设计/评审拥塞控制、退避、流控、TCP 算法与网络协议时

**Action**: 从端到端公平性、稳定性和避免拥塞崩溃出发；评估真实丢包、非对称路径、多流竞争下的行为；用测量/仿真验证。

**Boundary**: RFC 不是唯一实现；现代算法/BDP 场景需结合实际。

**SourceRefs**: https://www.rfc-editor.org/rfc/rfc2581 ; https://www.rfc-editor.org/rfc/rfc5681
