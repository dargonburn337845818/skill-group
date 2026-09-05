# Michael W. Lucas（网络工程 / 系统管理 / DNS 与 SSH 作者）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 立场概要

网络排障是系统工程：先确认问题范围与最近变更，再查 DNS/代理/防火墙/路由；每次只改一个变量并验证；把可重复操作写成文档/脚本，强调幂等、可回滚与“命令在当前环境真的能跑”。

## 结构化条目

**Trigger**: 服务器/开发机网络不通、DNS 解析异常、配置发布后出问题时

**Action**: 从“最近改了什么”和“问题范围”开始；检查 resolv.conf/hosts、代理、防火墙与路由；用 dig/host/nslookup 与配置查询确认；一次只改一个变量，改完立即验证。

**Boundary**: 生产变更先备份/记录原值，回滚路径明确；不要同时改多个变量。

**SourceRefs**: https://mwl.io/ ; https://www.oreilly.com/library/view/dns-and-bind-5th/0596100574/

**Trigger**: 编写网络运维文档、SSH/DNS/网络管理脚本或 SOP 时

**Action**: 把操作做成可重复、幂等、带验证与回滚的命令/脚本；写清配置位置、默认路径、错误场景与验证命令；先确认命令在当前环境可执行。

**Boundary**: 不同 OS/工具版本命令不同；不要把厂商特例当普适。

**SourceRefs**: https://www.tiltedwindmillpress.com/ ; https://www.oreilly.com/library/view/network-flow-analysis/1593272036/
