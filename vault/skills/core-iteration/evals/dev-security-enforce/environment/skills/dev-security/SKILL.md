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

## 来源

- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [GitHub Docs: Removing sensitive data / Security hardening for GitHub Actions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [OSV.dev](https://osv.dev/)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`
