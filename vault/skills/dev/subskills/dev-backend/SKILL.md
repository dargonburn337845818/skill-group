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

## 来源

- [MDN: HTTP 状态码](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [PostgreSQL Docs: Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [12-Factor App: Config / Backing services](https://12factor.net/config)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/dev-workflow-consensus/`
