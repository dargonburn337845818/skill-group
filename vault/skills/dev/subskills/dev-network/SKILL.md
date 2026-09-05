---
name: dev-network
description: 网络排障与网络访问子技能——面向 AI/开发者在开发机、CI、容器与 agent 场景中的网络故障：DNS、代理/VPN、TLS/证书、连通性/防火墙、HTTP、包管理器、Git、Docker、镜像源与 GFW 场景。按“症状分类→诊断→根因→可逆修复→重跑验证”执行；无关的网络概念科普或纯后端业务不要加载。
whenToUse: 出现 ECONNREFUSED / ECONNRESET / ETIMEDOUT / ENOTFOUND / ERR_NAME_NOT_RESOLVED / SSL certificate / proxy connection failed / npm ERR! network / pip timeout / git unable to access / docker pull failed / 连不上 / 无法访问 / 代理 / 超时 / 网络问题 等网络故障时；或需要给开发工具、包管理器、Git/Docker 配置网络访问时。
boundary: 只解决网络可达与访问路径问题；不替代 dev-security 的密钥/证书供应链安全、不替代 dev-ops-sre 的可观测性/发布流程、不替代 dev-performance 的协议栈性能调优。
---

# dev-network · 网络排障与网络访问（已蒸馏）

> 目标：让 agent 遇到网络报错时，不再“瞎试镜像/关证书/换代理”，而是先收集证据、定位层、给出可逆修复、并验证原命令恢复。
> 核心信条：**先分类，后动手；诊断优先于猜测；修复必须可逆；改完必须重跑原命令。**

## 触发条件（命中任一项即进入本技能）

- 错误码：`ECONNREFUSED`、`ECONNRESET`、`ETIMEDOUT`、`ENOTFOUND`、`EAI_AGAIN`、`EAI_NONAME`、`ERR_NAME_NOT_RESOLVED`、`ERR_CONNECTION_TIMED_OUT`、`ERR_SSL_PROTOCOL_ERROR`、`UNABLE_TO_VERIFY_LEAF_SIGNATURE`、`CERT_HAS_EXPIRED`、`HPE_INVALID_CONSTANT`、`ERR_OSSL_EVP_UNSUPPORTED`。
- 场景话术：`连不上`、`无法访问`、`网络问题`、`代理`、`超时`、`DNS`、`证书`、`防火墙`、`端口`、`镜像`、`梯子`、`VPN`、`网络排障`。
- 工具报错：`npm ERR! network`、`pip install` 超时、`fatal: unable to access 'https://github.com/...'`、`docker pull` 失败、`curl` 超时/证书错误、浏览器 `ERR_*` 系列。

## 六步工作流

```text
1 Collect  收集症状：错误原文、目标 host/URL、触发命令、范围、时间、环境（OS/代理/VPN）
2 Classify 按错误码匹配类别：连通性 / DNS / 代理 / TLS / HTTP / 防火墙 / 包管理器
3 Diagnose 按类别跑最小诊断命令，拿到证据
4 Analyze  解读诊断输出，定位根因（层、配置、服务、路径）
5 Resolve  应用可逆修复；改配置前先记录原值/备份
6 Verify   重跑原始失败命令，确认恢复；未恢复则回到第 2 步或升级方案
```

## 症状分类表（快速判断）

| 错误模式 | 类别 | 首选诊断 |
|---|---|---|
| `ECONNREFUSED`、`Connection refused`、`ERR_CONNECTION_REFUSED` | 连通性/端口 | `curl -v telnet://<host>:<port> --connect-timeout 5` |
| `ECONNRESET`、`connection reset`、`socket hang up` | 防火墙/中间设备 | 同层诊断 + `ss/netstat` 看重置路径 |
| `ETIMEDOUT`、`ERR_CONNECTION_TIMED_OUT` | 超时/路由 | `ping` / `traceroute` / `mtr` |
| `ENOTFOUND`、`ERR_NAME_NOT_RESOLVED`、`getaddrinfo`、`EAI_NONAME` | DNS | `nslookup <host>`、`dig @8.8.8.8 <host>`、检查 `/etc/hosts` |
| `ERR_PROXY_CONNECTION_FAILED`、`ECONNREFUSED 127.0.0.1:7890` | 代理 | `echo $HTTP_PROXY/...`、`curl -x` 测试代理端口 |
| `UNABLE_TO_VERIFY_LEAF_SIGNATURE`、`CERT_HAS_EXPIRED`、`self signed` | TLS/证书 | `openssl s_client -connect <host>:443 -showcerts </dev/null` |
| `HTTP 403 / 407 / 502 / 503 / 504` | HTTP/代理 | `curl -I -L -v <url>` 看状态与响应头 |
| `npm ERR! network`、`pip install` 超时、`git fatal: unable to access`、`docker pull fails` | 包管理器/工具链 | 对应工具 config + `--verbose` / `GIT_CURL_VERBOSE=1` |
| `EACCES`、`EPERM`、`端口被防火墙丢包` | 权限/防火墙 | 平台防火墙规则（`ufw`/`netsh advfirewall`） |

## 诊断动作清单（按平台选命令）

### 连通性 / 端口

```bash
# 基础连通
ping -c 4 <host>                 # Linux/macOS
ping -n 4 <host>                 # Windows
curl -v telnet://<host>:<port> --connect-timeout 5   # 跨平台端口探测
nc -zv <host> <port>             # Linux/macOS
powershell.exe -Command "Test-NetConnection -ComputerName <host> -Port <port>"  # Windows
```

### DNS

```bash
nslookup <host>
nslookup <host> 8.8.8.8          # 指定 DNS，绕过本机污染/缓存
dig @1.1.1.1 <host>              # Linux/macOS
cat /etc/hosts                   # Linux/macOS；Windows: C:\Windows\System32\drivers\etc\hosts
ipconfig /flushdns               # Windows
sudo systemd-resolve --flush-caches   # Linux systemd
```

> 要点：`ENOTFOUND` 先分清“本机 hosts 写错/缓存”还是“DNS 服务器返回 NXDOMAIN”。用指定公共 DNS 复测即可隔离。

### 代理 / VPN（多进程应用尤其重要）

```bash
echo $HTTP_PROXY $HTTPS_PROXY $ALL_PROXY $NO_PROXY          # 当前 shell
git config --global --get http.proxy
npm config get proxy
pip config get global.proxy
curl -x http://127.0.0.1:7890 -v https://<target> --connect-timeout 5   # 显式走代理
curl -sS --noproxy "*" --connect-timeout 5 https://<target>             # 显式绕代理
netstat -ano | grep <proxy_port> | grep LISTENING           # 代理端口是否在听
```

代理层级覆盖矩阵（关键）：

| 层 | 机制 | 覆盖 | 漏掉 |
|---|---|---|---|
| 系统代理（Windows WinINET/IE） | 注册表 | Chromium、.NET、Edge | Go/Rust、Python（除非 env vars）、Node（除非 env vars） |
| 环境变量 `HTTP_PROXY/HTTPS_PROXY/ALL_PROXY` | env | curl、wget、Go net/http、Python urllib/requests、Node | 不读 env 的进程、gRPC（多数） |
| 应用内代理（如 Electron `--proxy-server`） | 应用 flag | 该应用 renderer | 其子进程/后端 |
| TUN 模式（虚拟网卡） | OS 层路由 | 全协议、全进程 | 需要权限；未开启时最易漏 |

> 常见根因：系统代理只让浏览器/UI 通，而 CLI/后端/子进程没有继承 env；`登录成功但 API 失败` 常是这种“代理层级不匹配”。

### TLS / 证书

```bash
openssl s_client -connect <host>:443 -showcerts </dev/null | openssl x509 -noout -subject -issuer -dates
curl -vvv https://<host> 2>&1 | grep -E "SSL|TLS|certificate|issuer|subject|error"
```

- 证书过期 → 服务端/时钟问题；先查本机时钟，再联系服务端。
- 自签名/内部 CA → 把 CA 导入系统信任库，或工具级 `cafile`；不要默认全局关闭校验。
- `ERR_OSSL_EVP_UNSUPPORTED` → OpenSSL 3.x 与旧签名算法不兼容；升级运行时或用兼容参数，不是网络问题。

### HTTP / 性能 / 路由

```bash
curl -vvv -o /dev/null -w "HTTP/%{http_version} %{http_code}\nDNS:%{time_namelookup}s Connect:%{time_connect}s TLS:%{time_appconnect}s Total:%{time_total}s\n" https://<host>/<path>
traceroute -n <host>   # Linux/macOS
tracert -d <host>      # Windows
mtr -rwzbc 50 <host>   # 若安装
```

## 根因 → 可逆修复矩阵

| 根因 | 修复（先记录原值，可撤销） | 验证 |
|---|---|---|
| 本机 DNS 失败 | 临时改 `/etc/resolv.conf` 或系统 DNS 为 `8.8.8.8`/`1.1.1.1`；`ipconfig /flushdns` | `dig @8.8.8.8 <host>` + 重跑原命令 |
| 代理未运行 | 启动代理并确认端口 LISTENING | `curl -x http://127.0.0.1:<port> -I https://<target>` |
| 代理层级不匹配 | 设 user 级 `HTTP_PROXY/HTTPS_PROXY/ALL_PROXY/NO_PROXY` 后**完全重启应用**；仍不行→开 TUN 模式（需管理员） | 在原本失败的进程里重试；日志中确认同一进程树走代理 |
| npm 超时 | `npm config set registry https://registry.npmmirror.com`（或先确认原 registry） | `npm ping` + 重装/重试 |
| pip 超时 | `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple` | `pip config list` + 重试 |
| Git 拉取失败 | `git config --global http.proxy http://127.0.0.1:7890` 或取消错误代理；必要时 `http.sslVerify false`（仅开发临时） | `GIT_CURL_VERBOSE=1 git ls-remote <repo>` |
| Docker pull 失败 | 编辑 `/etc/docker/daemon.json` 配 `registry-mirrors`（Windows/macOS 在 Docker Desktop 设置） | `docker info` 看 mirror，`docker pull hello-world` |
| SSL 证书链缺失 | 更新系统 CA / 导入中间证书，或设置工具级 CA 文件 | `openssl verify` 通过 + 原命令恢复 |
| HTTP 407 | 为工具配置代理认证（env 或工具 config） | 重试并通过状态码 200 |
| 网关/路由故障 | 换网络/线路/节点；向 ISP 或平台报告 | traceroute 恢复 |

## 中国 / GFW 场景补充

- 关键词：`网络问题`、`连不上`、`无法访问`、`代理`、`超时`、`梯子`、`GFW`、`镜像`、`TUN`。
- 常用镜像：
  - npm：`https://registry.npmmirror.com`
  - pip：`https://pypi.tuna.tsinghua.edu.cn/simple`
  - Docker：腾讯云/中科大等公共 mirror（写入 daemon.json）
  - Maven：阿里云 `https://maven.aliyun.com/repository/public`
- 多进程应用“部分联网”优先查代理层级：UI 走系统代理、后端走 env、gRPC 常漏 → 最终方案是 TUN 模式。
- 边界：镜像源和代理只是“可达性”手段；不能永久替代安全校验与来源核验。关闭 TLS 校验、`strict-ssl false`、`http.sslVerify false` 仅限开发临时排障，必须恢复并记录。

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| 一看到网络错误就 `NODE_TLS_REJECT_UNAUTHORIZED=0` | 先跑 TLS 诊断，分清证书链/时钟/中间人；临时关闭后必须恢复并追因 |
| 同时改代理、DNS、镜像三个变量 | 一次只改一个变量，验证后再改下一个 |
| 只看到 `ping 通` 就判定网络正常 | DNS/TCP/TLS/HTTP 任一层都可能坏；按原命令复测 |
| 把 `EACCES/EPERM` 当网络问题 | 先查权限与防火墙规则 |
| 把 403/429 当网络故障 | 403 多为鉴权/IP 白名单，429 为限流；先看 HTTP 语义 |
| 把“GitHub 打不开”等同于“整个网络坏了” | 分 target 测试；可能是 DNS/代理/特定域名策略 |
| 修改全局 `.gitconfig`/`npmrc` 后不记录原值 | 修复前保存原值，修复后可撤销；CI 中不要把个人代理写进提交 |

## 与相邻子技能边界

- **dev-security**：CA 信任、密钥泄漏、供应链签名、恶意证书/中间人交给 dev-security；本技能只做“证书错误如何诊断与临时恢复”。
- **dev-ops-sre**：CLI/CD、容器镜像安全、发布/回滚、监控告警交给 dev-ops-sre；本技能只解决“开发/CI 中网络可达与工具链配置”。
- **dev-performance**：协议栈性能优化、拥塞控制、延迟/带宽深度调优交给 dev-performance；本技能只做“定位到网络层并给出可逆恢复”。
- **search-source / web-research-consensus**：本技能不负责“查资料”，只负责“网络不通时怎么让查资料/拉包/推代码恢复”。

## 干跑验收（最小）

1. 拿 3 个真实网络错误样本（如 `ENOTFOUND`、`ECONNREFUSED`、`UNABLE_TO_VERIFY_LEAF_SIGNATURE`），按六步流程输出诊断命令与结论。
2. 每个“修复”都必须带撤销方式与验证命令；没有验证步骤的修复不得写入。
3. 跑一次“故意破坏→恢复”：例如临时设错代理，确认诊断命令能发现；改回后重跑原命令确认恢复。

## 2026 深度补强（Round 40）

> 补强目标：把“第二层坑”补成可执行清单——DNS 到底谁在解析、代理环境变量的大小写与 NO_PROXY 匹配、TLS 验证链与进程级 CA、HTTP 时间线与状态码语义、包管理器/Git/Docker 的免改全局修复、GFW/SNI 的命令级绕行。以下为新增规则，不替代旧文，只加深证据与可逆操作。

### 1. DNS：先确认“谁在解析”，再动 resolv.conf

**最小检查链**

```bash
ls -l /etc/resolv.conf                 # systemd-resolved 常是 symlink
readlink -f /etc/resolv.conf           # 是否指到 /run/systemd/resolve/stub-resolv.conf
getent hosts <host>                    # glibc/NSS 视角
dig @127.0.0.53 <host> +short          # 或 @实际 nameserver
resolvectl status                      # 每链路 DNS / DoT / DoH 生效状态
resolvectl query <host>                # systemd-resolved 实际答案
```

- `resolv.conf` 是 symlink 到 stub（127.0.0.53）时，直接改 symlink 目标会被 systemd-resolved 覆盖，且不是可逆修复；临时验证用 `resolvectl dns <iface> 1.1.1.1`，持久改动走网络管理配置。
- `getent hosts` 失败但 `dig @1.1.1.1` 成功 → 根因在本机 NSS/`/etc/hosts`/缓存，不是上游 DNS；不要再改全局 DNS。
- `.local`（mDNS）、容器别名、K8s `*.svc` 不走普通解析链；对应工具是 `avahi`/Docker 内嵌 DNS/kube-dns。

**反例**：`ENOTFOUND` 就写死 `/etc/resolv.conf` 为 8.8.8.8；若 stub 未启动或名称属 mDNS，写死一台公共 DNS 也无效，且破坏原配置难回收。

### 2. 代理：大小写、NO_PROXY 匹配、进程内验证

- curl/libcurl：`http_proxy` **只认小写**（`HTTP_PROXY` 不生效）；`HTTPS_PROXY`/`ALL_PROXY`/`NO_PROXY` 可大小写，小写优先。排障时把大小写两种都列出。
- `NO_PROXY` 匹配：`example.com` 会匹配 `www.example.com` 及带端口形式；支持 IP 和 CIDR（curl ≥ 7.86），`*` 匹配全部；命令行 `--noproxy` 可覆盖环境变量禁代理列表。
- 验证“是否真的走代理”：先 `curl -v --noproxy "*" https://<target>` 做直连基线，再 `curl -x http://127.0.0.1:<port> -v https://<target>`，看 `* Connected to`/`CONNECT` 行。
- “UI 能开网页、CLI 失败”先查进程继承：`env | grep -i proxy`，对顽固进程用 `strace -e connect` 或应用日志确认。

**反例**：只 `echo $HTTP_PROXY` 就认为代理已生效；实际该进程读的是小写 `http_proxy`，或没有继承环境。

### 3. TLS：用 SNI + 验证链 + 进程级 CA，不用“关校验”

```bash
openssl s_client -connect <host>:443 -servername <host> -showcerts -verify_return_error </dev/null
openssl s_client -connect <host>:443 -servername <host> -showcerts </dev/null | openssl x509 -noout -subject -issuer -dates
openssl verify -CAfile <root.pem> -untrusted <intermediate.pem> <leaf.pem>
```

- `s_client` 默认“接受任何证书”只为调试；要看真实信任结论必须加 `-verify_return_error`，并配 `-CAfile`/`-CApath`。
- 缺中间证书时，用进程级 CA 注入，不改全局信任库：`curl --cacert <ca.pem>`、`NODE_EXTRA_CA_CERTS=<ca.pem>`、`GIT_SSL_CAINFO=<ca.pem>`、`REQUESTS_CA_BUNDLE=<ca.pem>`、`SSL_CERT_FILE=<ca.pem>`。
- 证书“过期”先 `date -u` 查本机时钟；`notBefore/notAfter` 与时钟偏差是常见假象，不要先关校验。

**反例**：`NODE_TLS_REJECT_UNAUTHORIZED=0` / `--insecure` 当修复；先定位具体校验失败（issuer/日期/hostname），再进程级白名单，并记录恢复。

### 4. HTTP：时间线分解 + 状态码语义 + 受控重试

```bash
curl -sS -o /dev/null -w 'DNS=%{time_namelookup}s TCP=%{time_connect}s TLS=%{time_appconnect}s TTFB=%{time_starttransfer}s TOTAL=%{time_total}s HTTP=%{http_code}\n' https://<host>/
curl -sS -D - -o /dev/null https://<host>/    # 看 Proxy-Authenticate / Retry-After / Via / Server
```

- `time_namelookup` 大 → DNS；`time_connect` 大 → TCP/路由/防火墙；`time_appconnect` 大 → TLS 握手；`time_starttransfer` 大而前三者正常 → 服务端/代理响应慢。
- 407 = 代理认证缺失（看 `Proxy-Authenticate`）；403 = 服务端授权/IP 白名单；429 = 限流（看 `Retry-After`）；502/504 = 网关/上游问题，不等于你本机网络坏。
- `curl --retry` 默认只重试超时与 408/429/500/502/503/504/522/524，并遵守 `Retry-After`；`--retry-all-errors` 可能产生重复数据，不默认放进 curlrc/脚本。

**反例**：502 就换代理/镜像；先 `--noproxy "*"` 直连或看 `Via`/`Server`，确认是上游还是代理再动手。

### 5. 免改全局：命令级与进程级优先

| 工具 | 单次/局部修复 | 回滚方式 |
|---|---|---|
| curl | `--resolve host:443:IP`、`--cacert <ca>`、`--proxy`、`--noproxy "*"`、`--doh-url` | 命令结束即还原，无文件残留 |
| npm | `npm install --registry <url> --fetch-retries 5 --fetch-timeout 60000`；项目级 `.npmrc` | `npm config delete registry`/删项目 `.npmrc` |
| pip | `pip install --index-url <mirror> --timeout 60 --retries 5`；`pip config debug` 看来源 | `pip config unset global.index-url` |
| git | `git -c http.proxy=... clone ...`；`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=http.proxy GIT_CONFIG_VALUE_0=http://... git clone ...`；`git config --local` | `git config --local --unset http.proxy` |
| Docker | `docker run --dns 1.1.1.1`、`--network host`；build 时临时代理参数 | 删容器/网络即还原，不动宿主 DNS/代理 |

- `GIT_CONFIG_COUNT` 把配置注入当前 git 进程，不写任何配置文件；适合 CI 和一次性 clone，显式 `git -c` 优先于它。
- 不要在 CI 里把个人代理/镜像写进 `~/.gitconfig`、`~/.npmrc`；用环境注入或命令级参数替换。
- 容器内 `127.0.0.1` 是容器自己，不是宿主；Docker 的自动 DNS 只保证同一用户自定义网络内名字可解析，跨宿主/外部域名仍走宿主 DNS 配置。

**反例**：为了一次拉包改全局 npm registry / daemon.json；应先试验命令级参数，确认根因后再说是否持久化。

### 6. GFW/SNI：命令级临时地址/DoH，不动全局

```bash
# 先拿正确解析，再单命令验证（不写 /etc/hosts、不改系统 DNS）
curl --doh-url https://cloudflare-dns.com/dns-query \
     --resolve cloudflare-dns.com:443:<ip> -I https://<target>
curl --resolve <target>:443:<ip> -I https://<target>
```

- `curl --resolve` 是命令行级“/etc/hosts”，只影响该命令；适合验证是“解析污染/解析错”还是“路由/SNI”问题。
- 用 DoH 拿到 IP 后先 `--resolve` 单命令确认；确认后可选择是否配置代理/镜像，且必须记录原 DNS/hosts 并可还原。
- Git 可用 `GIT_CONFIG_COUNT` 或 `url.<base>.insteadOf` 在单次命令中重定向，不写全局配置。

**反例**：把 `github.com` 写死进 `/etc/hosts` 当长期修复；hosts 不参与证书校验，IP 池变化会导致证书/可用性漂移，只做临时证据，不做“修复”。

## 来源

- [CacinieP/network-troubleshoot-skill（开发者网络排障技能仓库，MIT）](https://github.com/CacinieP/network-troubleshoot-skill)
- [curl 文档：--verbose / --connect-timeout / --proxy](https://curl.se/docs/manpage.html)
- [curl 退出码](https://curl.se/docs/manpage.html)
- [BIND 文档：dig / nslookup](https://bind9.readthedocs.io/en/latest/reference.html)
- [npm 配置：registry / proxy / strict-ssl](https://docs.npmjs.com/cli/v10/using-npm/config)
- [pip 配置：index-url / trusted-host](https://pip.pypa.io/en/stable/topics/configuration/)
- [Git 配置：http.proxy / http.sslVerify](https://git-scm.com/docs/git-config)
- [Docker Engine 配置：registry-mirrors / proxies](https://docs.docker.com/engine/daemon/proxy/)
- [OpenSSL 文档：s_client](https://www.openssl.org/docs/manmaster/man1/openssl-s_client.html)
- [Node.js 错误码（ECONNREFUSED/ENOTFOUND/ETIMEDOUT 等）](https://nodejs.org/api/errors.html)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`、`vault/skills/core-iteration/dev-workflow-consensus/`
- 完整来源表见同目录 `SOURCES.md`
