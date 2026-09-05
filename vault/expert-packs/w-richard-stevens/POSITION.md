# W. Richard Stevens（TCP/IP Illustrated / UNIX Network Programming 作者）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 立场概要

网络现象要落到协议栈与报文：先分层，再把症状对应到具体字段/状态，用规范与抓包验证；网络编程要尊重 API 契约、错误码与超时语义，用小例子复现。

## 结构化条目

**Trigger**: 需要理解 TCP/IP/套接字行为、协议交互或网络故障根因时

**Action**: 按分层链路→IP→TCP→应用逐层分析；把症状对应到 SYN/ACK、RST、FIN、TIME_WAIT、窗口/重传等状态；查规范/权威教材，用 tcpdump/Wireshark 验证字段。

**Boundary**: 不要为应用层问题无限下钻；实际 OS/内核实现存在差异。

**SourceRefs**: https://www.oreilly.com/library/view/tcp-ip-illustrated-volume/0201633469/ ; https://en.wikipedia.org/wiki/W._Richard_Stevens

**Trigger**: 设计/调试网络程序（socket、HTTP、DNS、TCP options、超时重试）时

**Action**: 把返回值、错误码、超时语义当接口契约；用小而完整示例复现；以当前平台 man 文档为准，不把偶然行为当规律。

**Boundary**: 教科书示例与 IPv6/代理/容器/云环境有差异。

**SourceRefs**: https://en.wikipedia.org/wiki/Unix_Network_Programming ; http://www.kohala.com/start/
