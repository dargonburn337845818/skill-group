# Sources（dev-architecture）

> 来源台账。内部路径/本地文件按工作区约定解析；公开链接可在浏览器复核。

## 清单
- https://martinfowler.com/bliki/MonolithFirst.html
- https://martinfowler.com/bliki/BoundedContext.html
- https://martinfowler.com/articles/microservices.html
- https://martinfowler.com/articles/consumerDrivenContracts.html
- https://martinfowler.com/articles/patterns-of-distributed-systems/
- https://www.rabbitmq.com/docs/confirms
- https://kafka.apache.org/documentation/#semantics
- https://aws.amazon.com/builders-library/exactly-once-processing/
- https://microservices.io/patterns/data/saga.html
- https://microservices.io/patterns/data/transactional-outbox.html
- https://sre.google/workbook/
- https://en.wikipedia.org/wiki/Consistency_model
- book: Designing Data-Intensive Applications, Martin Kleppmann, O'Reilly 2017
- book: Building Microservices, Sam Newman, O'Reilly
- book: Domain-Driven Design, Eric Evans, Addison-Wesley 2003
- book: The Art of Capacity Planning, John Allspaw
- $PROJECT_ROOT/vault/skills/base/search-source/
- $PROJECT_ROOT/vault/skills/core-iteration/skill-verification-consensus/
- $PROJECT_ROOT/vault/skills/core-iteration/dev-workflow-consensus/

## 分级说明
- 本 skill 的核心规则在 `SKILL.md` 中带 `source_refs` 或来源章节；未标注来源的观点应视为待证。
- 单源结论不作为核心规则；冲突分支保留而非合并。

## Round 35 新增来源
- [Kamil Grzybek: Modular Monolith: A Primer](https://www.kamilgrzybek.com/blog/posts/modular-monolith-primer) — 模块化单体：业务模块、契约/封装、独立性与垂直切片（SKILL Round35 规则 1）
- [Kamil Grzybek: Modular Monolith: Architecture Enforcement](https://www.kamilgrzybek.com/blog/posts/modular-monolith-architecture-enforcement) — 用编译器/架构测试/ADR 守住模块边界（SKILL Round35 规则 1）
- [AWS Prescriptive Guidance: Strangler fig pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html) — 增量迁移单体、代理层、anti-corruption layer（SKILL Round35 规则 2）
- [Microsoft Learn: Challenges and solutions for distributed data management](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/architect-microservice-container-applications/distributed-data-management) — 每服务独立库、CAP/2PC/Saga、CQRS/只读投影（SKILL Round35 规则 3）
- [Microsoft Learn: Cloud Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/) — Circuit Breaker/Bulkhead/Retry/Queue-Based Load Leveling 等模式目录（SKILL Round35 规则 5）
- [AWS SQS Developer Guide: Using dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html) — maxReceiveCount、redrive policy、DLQ 告警与 FIFO 注意（SKILL Round35 规则 4）
- [AWS Well-Architected: Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html) — 成本意识、支出/用量感知、成本有效资源（SKILL Round35 规则 6）
- [Raft Consensus Algorithm](https://raft.github.io/) — 共识=复制日志/状态机；多数派前进、少数派不可用（SKILL Round35 规则 7）
- [Principles of Chaos Engineering](https://principlesofchaos.org/) — 稳态假设、真实故障注入、小爆炸半径、持续自动化实验（SKILL Round35 规则 5）
- [microservices.io: Idempotent Consumer](https://microservices.io/patterns/communication-style/idempotent-consumer.html) — 至少一次投递下用已处理消息表/幂等键去重（SKILL Round35 规则 4）
