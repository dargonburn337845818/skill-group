---
name: dev-backend
description: 后端开发子技能——公开 API 契约、数据模型/迁移、错误语义、鉴权边界、服务分层与可观测性的可执行检查清单；来源以官方文档与标准为主。
whenToUse: 用户设计/实现后端 API、服务、数据模型、鉴权、错误处理或部署边界时；需要快速判断后端规范与取舍时。
---

# dev-backend · 后端开发（已蒸馏）

> 定位：给 dev 模块提供“后端工程判断”的最小可执行集。安全细节交给 dev-security，并发/性能分别交给 dev-concurrency / dev-performance。
> 核心原则：**公开接口先定型，错误语义明确，数据边界可迁移，服务分层按依赖方向不绕圈。**

## 触发条件

- 用户要设计/实现 REST/GraphQL/RPC API、后台任务、数据库模型、迁移、鉴权或服务分层。
- 需要审查后端实现：接口是否稳定、错误是否可处理、数据一致性是否被破坏。
- 用户问“这个后端方案有没有坑 / 该怎么拆”。

## 核心动作

### 1. 公开接口契约

- **输入输出先定契约**：字段、类型、必填、枚举、错误码，用 OpenAPI/JSON Schema/gRPC proto 等机器可读格式落盘。
- **版本与兼容**：破坏性变更走新版本或显式迁移；不要静默改字段语义。
- **分页/过滤/排序**：列表接口明确默认值和最大页大小；避免一次全量返回。
- **幂等性**：对会重复执行的写操作（支付、任务创建）设计幂等键或唯一约束。

> 边界：内部一次性脚本可不做完整契约；但会被多个调用方复用的接口必须做。

### 2. 数据模型与迁移

- **约束建在数据库层**：主键、唯一、外键、非空、检查约束，不能只靠应用代码。
- **迁移可逆/可回滚**：至少为破坏性迁移准备向下迁移或备份方案。
- **事务边界**：多表保持一致时用事务；事务内不做远程调用，避免长事务。
- **软删除/审计**需要时显式设计，不能把“字段还在”当成安全删除。

> 边界：NoSQL 文档模型不强行套关系约束，但仍要定义一致性边界（最终一致/强一致）。

### 3. 错误处理语义

- **错误要可区分**：客户端错误（4xx）、服务端错误（5xx）、业务失败要分类型，不全部返回 500。
- **错误信息可诊断但不泄露**：日志返回内部 trace id，对外只给用户可理解信息，不返回堆栈/内部 SQL。
- **失败可重试**：暂时性错误标注 Retry-After 或可重试标志；幂等键防止重复副作用。
- **统一错误结构**：`{ code, message, details? }` 之类，避免每个接口自造格式。

> 边界：内部微服务间错误格式可更丰富；对外 API 要保守，防止信息泄露。

### 4. 鉴权与权限边界

- **默认拒绝**：新接口默认需要鉴权；公开接口显式白名单。
- **权限在服务端判定**：不能只靠前端隐藏按钮；每次资源访问都要在服务端校验 ownership/role。
- **敏感操作写审计日志**：谁、何时、对什么、结果如何。
- **密钥/凭据不进代码与日志**：从环境变量/密钥管理服务读取。

> 边界：详细认证/授权方案交 dev-security；这里只定义“后端工程必须有的边界”。

### 5. 服务分层与依赖方向

- **依赖单向流动**：接口层 → 应用层 → 领域/数据层；避免循环依赖。
- **领域逻辑不依赖 Web/ORM 细节**：核心规则放在可测试的领域层，不放在 controller 里。
- **可替换边界**：数据库、消息队列、外部 API 都走窄接口，便于测试与替换。
- **不为了分层而分层**：小服务一个文件能讲清就行；出现第二种实现/第二种用法时才抽接口。

> 边界：简单 CRUD 不必套六层架构；分层是为了隐藏复杂度，不是为了增加中转层。

### 6. 可观测性

- 每个请求有 correlation/trace id，能串起日志、指标、调用链。
- 关键路径有耗时指标、错误率、队列积压；告警阈值要有依据。
- 健康检查区分 liveness/readiness；不要把外部依赖宕机当进程不健康。

> 边界：内部工具可只打日志；对外服务建议至少有关键指标与 trace。

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “接口返回 500，反正前端处理” | 区分 4xx/5xx，并给出稳定错误码 |
| “数据库迁移直接在线上改” | 先备份、先向下迁移、再灰度；破坏性变更走版本 |
| “controller 里写全部业务逻辑” | 领域逻辑下沉到可测试层，controller 只做编排 |
| “把 ORM 的 query 直接暴露给前端” | 通过服务层窄接口暴露，不把数据访问细节当 API |
| “所有写操作都认为会成功” | 写操作考虑幂等、失败补偿、事务回滚 |

## 2026 深度补强（Round 32）

> 本轮不替代 1–6 节；补强重点是“可执行检查 + 反例”，并新增独立来源台账（见 `SOURCES.md` 的 Round 32 新增来源）。

### R1. 错误响应用标准 Problem Details，不每次自造 JSON

- **触发**：对外 REST API 返回错误 JSON；团队已有 `{code, message}` 但字段名不统一；客户端需要按错误类型做分支处理。
- **动作**：对外错误使用 `application/problem+json`，至少带 `type`（稳定 URI，最好可解析到文档）、`title`、`status`、`detail`、`instance`；`status` 必须与实际 HTTP 状态一致。扩展字段（如 `errors[]` 的 `pointer`）属于 problem type 定义，客户端对未知扩展必须忽略。
- **反例**：一个接口返回 `{"error":"Oops","msg":"..."}`，另一个接口返回 `{"code":"INVALID","message":"..."}`，客户端为每个接口写解析器；或把堆栈/SQL 放进 `detail`。
- **要点**：`type` 是机器可读主标识，`detail` 只用于帮助客户端修正，不承载内部调试信息；`instance` 可放该次错误的具体标识/请求 trace。
- **来源**：RFC 9457。

### R2. 列表分页：用 cursor/token + 稳定排序；offset 只用于静态低并发场景

- **触发**：列表按时间/ID 排序且持续写入；接口已有 `page`/`offset`/`limit`；客户端翻页出现重复/丢行。
- **动作**：集合接口从第一版就带分页（AIP-158：给未分页接口补充分页是破坏性变更）；请求用 `page_size`（可选、服务端封顶）+ `page_token`，响应用 `next_page_token`（无后续页则省略）；token 必须 opaque/URL-safe、只表达位置、不能当权限凭据；排序键必须唯一（如 `id` 或 `created_at+id`）并在光标中带上过滤条件。
- **反例**：`?page=1&size=100` 在持续写入的 feed 上翻页会重复/跳过；把 `offset=50` 做 base64 当“token”暴露实现；只按非唯一 `created_at` 排序导致边界重复。
- **来源**：Google AIP-158。

### R3. 幂等键要有完整语义：请求指纹、同键不同参冲突、过期与归属

- **触发**：支付、下单、任务创建等可重试写操作；客户端超时后重试；只在前端用 UUID 防重复。
- **动作**：服务端持久化 `(idempotency_key, endpoint, request_hash, response_snapshot, 过期时间)`；相同 key + 相同请求指纹返回原响应（200/201），相同 key + 不同请求指纹返回 `409 Conflict`；key 必须绑定身份/租户，防止跨账户重放；数据库层用唯一约束兜底；过期后同一 key 可作为新请求。
- **反例**：对同 key 不同 payload 静默返回第一次结果；幂等表无唯一索引，并发重试仍插入两条；key 由客户端可预测且未绑定用户。
- **来源**：Stripe Idempotent Requests。

### R4. 破坏性变更走 expand–contract（parallel change）：先扩、再迁、后缩

- **触发**：重命名/删除数据库列、改 API 字段名或消息格式、切下游消费者；计划直接改线上 schema 或 payload。
- **动作**：展开阶段先加新列/新字段并保持旧接口可用；迁移阶段双写/回填并逐个迁移消费者；收缩阶段在确认无读取后再删除旧列/字段。同一端点应先增加字段而不是先删字段，若合同阶段不执行会永久背上双写双读复杂度。
- **反例**：`ALTER TABLE users RENAME COLUMN name TO full_name` 先部署，旧代码直接崩；API 把 `name` 字段删除只留 `fullName`，老客户端解析失败。
- **来源**：Martin Fowler: Parallel Change（expand and contract）。

### R5. 迁移文件不可变、可校验、由工具执行，不做“生产手补”

- **触发**：多环境部署；生产库出现“手工改过”的 schema；有人想修改已发布的迁移文件。
- **动作**：所有 schema/data 变更写成 versioned migration 进版本库，按版本顺序执行，迁移工具维护 schema history；已应用的迁移文件发布后禁止编辑（checksum 改变会校验失败），修复用新的 forward migration/undo；CI 中做 drift 检查与 dry-run；大表 DDL 评估在线/分批/锁表风险。
- **反例**：改已发布的 `V2__create_users.sql` 补约束；生产库 `ALTER TABLE` 后不回写迁移；百万行表直接 `ADD COLUMN NOT NULL DEFAULT` 造成长时间锁写。
- **来源**：Flyway Migrations；Martin Fowler: Parallel Change（联用）。

### R6. 读接口支持 HTTP 缓存与条件请求：ETag / If-None-Match / If-Match

- **触发**：读多写少的详情/列表；多个客户端编辑同一资源；PUT 覆盖导致丢更新。
- **动作**：可缓存表示返回 `ETag`，客户端用 `If-None-Match` 得到 `304 Not Modified`；`Cache-Control` 明确 `public/private/no-store`（用户私密数据禁止共享缓存）；写操作要求客户端带 `If-Match`，版本不符返回 `412 Precondition Failed`，避免 last-write-wins。
- **反例**：GET 永远 200 + 全量数据，客户端每次重复下载；PUT 不带版本直接覆盖他人修改；把含个人信息的响应设成 `Cache-Control: public`。
- **来源**：RFC 9110（ETag/If-Match/If-None-Match/304/412）；RFC 6585（428 Precondition Required）。

### R7. 鉴权边界 HTTP 语义精确：401 vs 403，凭据只走 Authorization

- **触发**：受保护端点；登录失效/无权；API 示例把 token 放 URL。
- **动作**：未认证或凭据缺失/无效返回 `401 Unauthorized` 并带 `WWW-Authenticate` challenge；已认证但无权访问返回 `403 Forbidden`；Bearer token 只放 `Authorization` 头，不放 query 或 body（会被日志/CDN/历史记录暴露）；401/403 的 body 不泄露内部身份细节。
- **反例**：token 缺失返回 403；`?token=...` 被网关日志与浏览器历史记录保存；401 响应没有 `WWW-Authenticate`，标准客户端无法触发认证流程。
- **来源**：RFC 9110；OWASP Web Service Security Cheat Sheet。

### R8. 可观测性用标准 trace context + 语义约定，绝不放敏感信息

- **触发**：多服务/异步/队列链路排障；日志里只有随机 request id，跨服务串不起来；指标 path 基数爆炸。
- **动作**：入口接收并向下游传播 W3C `traceparent`/`tracestate`（或 OpenTelemetry context）；HTTP span 按语义约定设置 `http.request.method`、`http.route`、脱敏后的 `url.path`、`http.response.status_code`、低基数 `error.type`；4xx 服务端 span 一般保持 unset，5xx/客户端失败置 Error；日志行携带 trace_id/span_id；指标按 route 聚合，不把完整 URL/ID 当 label。
- **反例**：日志只打 `request_id` 且不复用到出站调用；把 `/users/123` 的完整 ID 当 span name/指标 label 造成高基数；把 token/请求体/个人信息塞进日志或 `tracestate`。
- **来源**：W3C Trace Context；OpenTelemetry HTTP Semantic Conventions。

## 来源

- [MDN: HTTP 状态码](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [PostgreSQL Docs: Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [12-Factor App: Config / Backing services](https://12factor.net/config)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/dev-workflow-consensus/`
