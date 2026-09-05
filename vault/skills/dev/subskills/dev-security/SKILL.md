---
name: dev-security
description: 信息安全子技能——威胁建模、输入校验/输出编码、认证授权、依赖与供应链、密钥/配置/日志的降险检查清单；以 OWASP/CWE/官方公告为主要来源。
whenToUse: 用户做认证授权、输入处理、密钥管理、依赖审计、安全审查或安全评审时；需要把安全经验变成可检查动作时。
---

# dev-security · 信息安全（已蒸馏）

> 定位：提供“降险”而非“绝对安全”的可执行检查。安全是系统属性，不是一个库开关。
> 重点：先列攻击面，再逐项做输入/输出/认证/依赖/密钥检查。

## 触发条件

- 用户要设计/审核登录、权限、API 输入、文件上传、支付/订单、密钥存储、依赖升级。
- 用户要“安全评审这段代码/部署配置”。
- 需要把 OWASP/CWE 的抽象条目转成能直接落地的动作。

## 核心动作

### 1. 威胁建模（先于写码）

- 列出资产（数据、钱、凭据）、攻击者（外部/内部/供应链）、信任边界。
- 对每个入口问：谁能访问？越权会怎样？失败模式是什么？
- 输出最小威胁清单：认证绕过 / 注入 / 越权 / 敏感信息泄露 / 依赖投毒。

> 边界：不追求完整 STRIDE 论文；单页应用可按“入口→信任边界→缓解”快速过。

### 2. 输入校验与输出编码

- **服务端校验一切输入**：类型、长度、格式、枚举、业务规则；前端校验只是体验。
- 输出到 HTML 用上下文编码/转义，不拼接未处理字符串；富文本用白名单 sanitizer。
- SQL 用参数化查询/ORM 绑定；不要字符串拼接 SQL。
- 文件上传：限制类型/大小/文件名，存储到非执行目录，随机化文件名。
- 重定向、命令执行、模板渲染都要视为敏感输出点。

> 边界：正则校验不等于安全白名单；复杂语义的校验（URL、邮箱）还要做规范化后再匹配。

### 3. 认证 / 授权 / 会话

- 密码用自适应哈希（bcrypt/argon2/scrypt），不存明文、不用 MD5/SHA1 单轮。
- 会话 cookie 设 `HttpOnly`、`Secure`、`SameSite`；登录态要能失效。
- **每次资源操作都在服务端校验权限**（用户/角色/资源拥有者），不能只靠前端隐藏。
- MFA、限流、锁定策略按风险分级；不要对所有接口一刀切强密码政策。

> 边界：OAuth/OIDC 细节复杂，接入时按官方文档与 RFC，不凭印象实现。

### 4. 依赖与供应链

- 锁定版本并定期扫漏洞：`npm audit` / `pip-audit` / `cargo audit` / `osv-scanner`，至少一个持续集成。
- 升级前看 advisory 的受影响版本与修复 commit；不要只改 package.json 不跑测试。
- 第三方 action/docker 镜像尽量 pin 到不可变引用（commit SHA / digest），并限制来源。
- 锁定文件（lockfile）必须提交；不要用 `*` 或松散版本范围。

> 边界：内部私有依赖无公告时，降权为“单源待证”，不号称已审计。

### 5. 密钥、配置与日志

- 密钥/凭据只从环境变量或密钥管理服务读，不硬编码、不进 git、不进日志。
- `.gitignore` 提前忽略 `.env`、证书、构建产物；已提交的 secret 先 revoke/rotate 再清历史。
- 日志不打印 token、密码、身份证号、完整支付信息；脱敏优先。
- 生产配置最小权限：数据库账号只给所需权限，管理后台不在公网暴露。

> 边界：公网暴露管理端、宽泛 CORS、缺 CORS 白名单等都属于高风险项，需显式决策。

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “用了 HTTPS 就安全” | HTTPS 只保护传输；输入校验/权限/密钥管理仍需做 |
| “前端拦截就够防 XSS” | 输出编码/安全解析必须在服务端与渲染层都做 |
| “用了某某框架就自动安全” | 框架默认值不等于业务安全；仍要审计配置与用法 |
| “CVE 升级没影响就不管” | 先看修复内容与影响面，再升级+回归，不能因为“低危”忽略 |
| “日志里记 body 方便排查” | 脱敏后记录；敏感字段一律屏蔽 |

## 2026 深度补强（Round 32）

> 本轮把抽象安全原则压实成可直接检查的 API / 令牌 / 输入 / 供应链动作；每条给触发、动作、反例，来源见文末“Round 32 新增来源”。

### R1. API 对象级授权（BOLA/IDOR）：查对象，不只看身份

- **触发**：接口用客户端传入的 `id` / `uuid` / `account_id` 查库、读文件、调第三方；或后台管理端点按 ID 操作资源。
- **动作**：每个“用用户提供的 ID 访问数据源”的函数，都必须在服务端校验 `(当前身份, 对象)` 关系（owner / tenant / project / 团队）；登录成功或有某角色 ≠ 拥有该对象。
- **动作**：未授权与不存在返回一致的 `404`/无细节错误，不暴露“对象存在但没权限”；不要只靠 UUID 不可猜（security through obscurity 不是授权）。
- **反例**：`GET /api/orders/{orderId}` 只做 `authenticate()` 后 `repo.find(orderId)` → 改 ID 读到他人订单、账单或凭据。
- **边界**：对象级授权要写进数据访问层/业务服务，不能只在 controller 层做一次可跳过的装饰器。
- **来源**：OWASP API Security Top 10 2023 API1；OWASP API Security 2019 BOLA；OWASP Authorization Cheat Sheet。

### R2. API 批量赋值（Mass Assignment / BOPLA）：显式白名单 DTO，禁止自动绑定

- **触发**：`PUT/PATCH/POST` 接收 JSON/Form，直接 `save(request.body)`、`model.update(request.params)` 或框架自动绑定实体。
- **动作**：用显式 DTO / 字段白名单只接收本次允许修改的字段；敏感字段（`isAdmin`、`credit_balance`、`status`、`owner`、`price`、`role`）永远不来自客户端；未预期字段建议整单拒绝，至少不能静默写入。
- **反例**：`PUT /api/users/me {"user_name":"a","isAdmin":true}` 被 ORM 自动映射成实体字段 → 提权或篡改余额。
- **边界**：不能只靠“前端不展示字段”保护；API 天然暴露实现细节，属性名可被枚举。
- **来源**：OWASP API Security 2023 API3；OWASP API Security 2019 Mass Assignment；CWE-915。

### R3. 输入校验先规范化，再用 allowlist 和解析器

- **触发**：用户输入进入路由/URL/文件名/Unicode 文本；用正则做格式判断；或直接基于输入做路径/跳转/命令。
- **动作**：校验前先规范化——URL 先 percent-decode 并处理 `%2e%2e`、路径分隔符变体；Unicode 文本按 NFC/NFKC 规范化；文本长度设上限，再用字符集/枚举/业务范围 allowlist。
- **动作**：复杂格式（URL、邮箱、IP、域名）用成熟的解析库而不是纯正则；正则设置长度上限、避免灾难性回溯（ReDoS）。
- **反例**：只 denylist `../`，但 `%2e%2e%2f`、Unicode 全角斜杠或编码变体绕过；`^[a-z]+$` 对超长输入让 CPU 爆炸。
- **来源**：OWASP Input Validation Cheat Sheet；OWASP SSRF Prevention Cheat Sheet（URL/主机名校验细节）。

### R4. JWT 校验完整且最小化：签名、claims、撤销都要处理

- **触发**：后端解析/信任 JWT；前端存储 token；使用 refresh token；把 JWT 当“session”。
- **动作**：服务端校验签名前先固定允许的算法集（如只 `RS256/ES256`），拒绝 `alg:none` 与 RS/HS 混淆；公钥只从受信 JWKS/配置取，不信任 token header 里的 `kid`/`jku`/`x5u`。
- **动作**：校验 `exp`、`nbf`、`iat`、`iss`、`aud` 全部匹配资源方；access token 短时；refresh token 服务端存储、轮换、绑定客户端；JWT 不放敏感数据（Base64 可读）；无状态会话要有 denylist/撤销机制。
- **反例**：只 `base64decode` 后看 `exp`，或者直接 `jwt.verify(token, secret)` 且算法从 header 取 → 伪造/算法混淆/跨资源冒充。
- **来源**：OWASP JSON Web Token Cheat Sheet；RFC 9700（audience/权限限制与 token 绑定）。

### R5. OAuth/OIDC：公共客户端用 PKCE + 精确 redirect_uri，不用 implicit

- **触发**：SPA、移动端/原生 App 接入授权码流程；第三方登录；把 client secret 放进前端包。
- **动作**：新系统不要用 implicit grant（`response_type=token`）；用 authorization code + PKCE（`S256`）；原生 App 用外部浏览器/系统 user-agent，不用 embedded webview。
- **动作**：`redirect_uri` 必须精确匹配注册值，拒绝通配/前缀模式；公共客户端不携带 client secret；access token 做 audience 限制；refresh token 轮换并对公共客户端做 sender-constraint。
- **反例**：SPA 内嵌 `client_secret`，`https://*.example.com/cb` 通配重定向，access token 出现在 URL fragment → 泄露/截获。
- **来源**：RFC 8252；RFC 9700。

### R6. SSRF：服务端拉取外部资源前做出口校验

- **触发**：webhook、URL 预览、图片拉取、代理转发、文档导入等让用户控制服务端发起 HTTP 请求。
- **动作**：先按业务 allowlist 校验 scheme/host，禁止 `file://`、`gopher://`、`dict://` 等非 HTTP(S) 协议；对允许域名解析全部 A/AAAA 后再次校验不是 loopback/私网/link-local/云 metadata。
- **动作**：默认禁用自动重定向（或每次重定向重新校验）；同一出口策略在网关/egress proxy 层再守一道，避免只靠应用层。
- **反例**：只挡 `localhost` 和 `127.0.0.1`，但 `169.254.169.254`、`10.x`、IPv6 变体、DNS rebinding 仍可达内部。
- **来源**：OWASP SSRF Prevention Cheat Sheet；OWASP API Security Top 10 2023 API7。

### R7. API 资源消耗与敏感业务流：配额、分页、成本都要限

- **触发**：列表分页、批量导入/导出、上传大文件、发短信/邮件、OCR/支付/下单等消耗 CPU/内存/存储/钱的端点。
- **动作**：每个端点明确最大 payload、最大分页 size、最大记录数、内存/CPU 预算；按 client/token/IP/tenant 设速率与配额；超限返回 `429` + `Retry-After`，并记录审计。
- **动作**：对“敏感业务流”（抢票、刷评论、批量下单）加频控、验证码、风控或并发上限，防止自动化滥用；限流在网关/API 层做，不只在业务代码。
- **反例**：`/api/users?page=1&size=999999` 一次返回全库；登录接口有限流但创建订单/导出没有 → DoS 或成本失控。
- **来源**：OWASP API Security Top 10 2023 API4/API6；OWASP API Security 2019 Lack of Resources & Rate Limiting。

### R8. 供应链完整性与密钥生命周期：SBOM/来源验证 + 动态短时凭据

- **触发**：引入第三方依赖/镜像/action；CI/CD 使用云或包仓库凭据；生产服务使用静态数据库密码/API key。
- **动作**：除漏洞扫描外，生成并消费 SBOM，验证第三方组件来源、构建 provenance 与签名（SLSA 思路），限制仓库源/镜像源，警惕 typosquatting。
- **动作**：CI/CD 优先 OIDC 换取短时、最小范围的云/包仓库凭据；`GITHUB_TOKEN` 默认最小权限；第三方 action pin 到完整 commit SHA；慎用 `pull_request_target`/`workflow_run` checkout 不可信 PR。
- **动作**：密钥优先动态短时凭据（Vault 动态 secret / KMS 签发 / OIDC）；静态密钥按环境/服务隔离、自动轮换、最小权限访问并审计；加密密钥与数据分离（DEK/KEK、KMS/HSM）；别把长期密钥放环境变量（`/proc/self/environ`、dump 可读）。
- **反例**：全项目共用一个数据库密码且提交进 `.env`；CI 里存长期 `AWS_ACCESS_KEY_ID` 或用 JSON/YAML blob 当 secret（日志脱敏会失效）；没有 SBOM、没有 provenance、不验证依赖来源。
- **来源**：NIST SP 800-218；SLSA Specification v1.2；GitHub Actions Security Hardening；OWASP Secrets Management Cheat Sheet；OWASP Cryptographic Storage Cheat Sheet。


## 来源

- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [GitHub Docs: Removing sensitive data / Security hardening for GitHub Actions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [OSV.dev](https://osv.dev/)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`
