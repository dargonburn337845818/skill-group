# Julia Evans（网络调试 / 开发者教育 / wizard zines 作者）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 立场概要

网络排障是“做小实验”而不是“猜”：先读错误原文，确定在哪一层，再用最小工具收集证据，一次只改一个变量，最后确认原操作恢复。她用图解/漫画把 DNS、TCP、HTTP 讲成可理解的状态流。

## 结构化条目

**Trigger**: 遇到网络报错、DNS/TCP/HTTP 不通，需要定位是哪个环节失败时

**Action**: 先读原始错误，确认失败层；用 dig/nslookup、nc/curl telnet、openssl s_client、curl -v 等做受控实验；一次只改一个变量；把结论缩小到层。

**Boundary**: 需要工具与权限；生产环境谨慎；无法复现不硬下结论。

**SourceRefs**: https://jvns.ca/ ; https://jvns.ca/blog/2019/03/15/new-zine--bite-size-networking-/ ; https://wizardzines.com/

**Trigger**: 向他人解释网络概念/方案/诊断过程时

**Action**: 用图示/zine 从底层到上层建立心智模型；先讲“数据包/状态如何流动”，再给工具和命令。

**Boundary**: 教学风格不替代协议规范；深度以 RFC/教材为准。

**SourceRefs**: https://jvns.ca/blog/2019/03/15/new-zine--bite-size-networking-/ ; https://jvns.ca/blog/2022/04/26/new-zine--how-dns-works-/

**Trigger**: 排查“能上外网但某应用/某域名不通”的部分失败时

**Action**: 逐层测试：IP 可达？DNS 正确？端口开放？TLS 通过？HTTP 正常？把“网络问题”缩小到具体层。

**Boundary**: 代理/中间盒会让直连与经代理结果不同；分别测试。

**SourceRefs**: https://jvns.ca/ ; https://wizardzines.com/
