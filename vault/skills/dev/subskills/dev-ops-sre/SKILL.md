---
name: dev-ops-sre
description: 部署/CI/CD/可观测性子技能——发布流水线、容器镜像、日志/指标/追踪、告警与回滚的可执行检查清单；先让流水线可重复、可审计、可回滚，再谈自动化；代码格式化、JSON 整理等非部署/运维任务不要加载。
whenToUse: 用户搭建或评审部署流程、CI/CD、容器镜像、监控告警、on-call 与回滚方案时；需要判断“线上为什么没告警/怎么安全发布/怎么回滚”时。
---

# dev-ops-sre · 部署 / CI/CD / 可观测性（已蒸馏）

> 定位：给 dev 模块提供“运维可靠性工程判断”的最小可执行集。安全细节交给 dev-security，性能分析交给 dev-performance，测试策略交给 dev-testing。
> 核心原则：**先让流水线可重复、可审计、可回滚，再谈自动化；可观测性先定信号与 SLO，再堆告警。**

## 触发条件

- 用户要搭建/改造部署流水线、CI/CD、容器镜像、配置管理或发布流程。
- 需要评审上线方案、回滚方案、监控告警、on-call 与事故处理。
- 用户问“为什么线上挂了没告警”“怎么安全发布”“CI 慢/不可信”“镜像怎么瘦身”。

## 核心动作

### 1. 部署流水线与发布

- **Build / Release / Run 分离**：一次构建生成不可变制品（镜像、jar、bundle），发布与运行只引用它，不现场重新构建。
- **制品可追溯**：记录来源 commit、版本号、镜像 digest、构建时间；坏版本能快速定位并回滚到上一稳定制品。
- **配置注入而非重建**：代码里不放环境差异；通过环境变量/配置中心/密钥管理注入（12-Factor Config）。
- **环境一致性**：dev/staging/prod 用同一构建产物，只换配置；避免“我本地能跑、线上不行”的 build/run 漂移。
- **渐进发布**：滚动更新、蓝绿、金丝雀；先小流量，经过健康检查/冒烟再扩大，失败时能快速全量回滚。
- **发布前检查**：数据库迁移是否向前兼容（expand/contract）、依赖/协议兼容、回滚计划与上一制品是否仍在。

> 边界：回滚不等于修复根因；数据库结构不兼容时，回滚旧代码可能比继续前进更危险，需在改动前设计双向兼容。

### 2. CI/CD

- **流水线即代码**：放在仓库中、可评审、可追溯；同一 commit 在相同输入下应产生可预期结果。
- **CI 做门禁，CD 做发布**：PR 跑 lint/单测/构建/扫描；只有通过的门禁才有资格触发部署，生产环境部署默认需要人为确认或受保护分支。
- **密钥与权限**：不把密钥写进仓库/镜像/日志；使用 CI 密钥库或密钥管理服务，给 job 最小权限并限制有效期。
- **缓存与产物**：依赖按 lockfile 缓存（不缓存无锁定依赖）；构建产物（镜像、二进制、测试报告）按 key 跨 job 复用并设置过期。
- **可重复构建**：锁工具链版本（`.nvmrc`、`package-lock.json`、Go modules、maven wrapper 等），不依赖 `latest` 或漂移的 base image。
- **快速反馈**：失败即失败，日志可定位；flaky 测试走重试/隔离/quarantine，不靠“重跑归零”掩盖问题。

> 边界：CI 绿 ≠ 可发布；测试通过 ≠ 满足 SLO；把 CI 当 CD 会带来“没跑完整验证就上生产”的风险。

### 3. 容器与镜像

- **多阶段构建**：构建依赖与运行时依赖分离，最终镜像只包含运行所需；用 `.dockerignore` 防止把无关文件送进构建上下文。
- **精简且安全**：优先官方/最小基础镜像、非 root 用户、单进程职责；不把 SSH、调试器、源码仓、CI 凭据打进生产镜像。
- **可复现与可扫描**：固定镜像 tag/digest；CI 中做漏洞扫描与 SBOM 生成；供应链敏感时做镜像签名/校验。
- **动态配置**：镜像不含环境差异；配置由运行时/编排层注入，避免“同一镜像改配置要重新构建”。
- **健康检查**：容器/编排配置中区分 liveness（挂了重启）、readiness（能否接流量）、startup（慢启动期不误杀）。

> 边界：不是所有应用都适合容器化；把每个函数/小脚本都拆成微服务会放大运维成本；镜像瘦身不能以丢失可观测/排障工具为代价。

### 4. 可观测性（日志 / 指标 / 追踪）

- **三支柱 + 关联**：日志、指标、追踪都带上统一关联字段（`trace_id`、`service`、`env`、`version`），能从一个用户请求串起全链路。
- **日志**：结构化 JSON，含时间、级别、服务、trace、关键字段；有保留策略；不打印密钥/个人敏感信息；按需采集，避免“全量 info”淹没故障信号。
- **指标**：服务用 RED（Rate/Errors/Duration），资源用 USE（Utilization/Saturation/Errors）；计数器/直方图要带标签，但标签基数受控。
- **追踪**：跨越服务边界记录调用链；在关键路径/采样率上做平衡，不因追踪拖垮性能；先保证 trace 能跨服务传播。
- **SLI / SLO**：先定义用户可感知指标（可用性、延迟、错误率）与目标，再据此设告警；无 SLO 的告警容易变成噪声。
- **健康检查**：liveness 只反映进程是否可恢复，readiness 反映能否接流量；两种检查不要混用，避免滚动更新被误杀。

> 边界：可观测性不等于“多几个 dashboard”；没有 SLO、没有 alert 责任人的监控没人看；采集一切数据而不控制基数/保留期，成本会失控。

### 5. 告警与 On-call

- **告警症状而非原因**：基于错误率、延迟、饱和度、SLO 消耗率；不要对每个 500 或每个 CPU 尖刺都 page。
- **可行动**：每条 page 必须能回答“影响多大、谁负责、怎么处理”，附 runbook 链接与严重级别；重复告警做分组/去重。
- **分级**：区分“立即叫醒”和“攒工单”；阈值要有 duration，避免瞬时抖动疯狂通知。
- **验证告警**：告警本身要能被触发（合成监控、演练、chaos 原则），不能只是“配了没人看”。
- **On-call 可持续**：轮值、交接、升级路径明确；每次 page 后有跟进，避免“告警疲劳—漏看真告警”。

> 边界：告警数量越多不代表越可靠；告警疲劳是真事故的温床；自动修复只用于被验证安全、可逆的动作。

### 6. 回滚与事故处理

- **发布前准备回滚**：保留上一稳定制品；明确触发条件（错误率/延迟阈值）、执行人、审批与通知。
- **回滚方式**：重新部署上一制品；或用 feature flag 关闭新逻辑；数据库迁移需 expand/contract 或预留向前兼容路径。
- **前进 vs 回滚**：回滚成本大于前进成本时（如 schema 不兼容、数据已写），选择“向前修复”而不是硬回滚。
- **事故复盘**：blameless 复盘，记录时间线、证据、影响、行动项与负责人；不重写历史、不把复盘变成追责。

> 边界：未测试过的回滚路径等于没有回滚；回滚后仍需关新代码入口、补监控与根因修复。

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “CI 全绿就能直接上生产” | 生产门禁 + 人工确认 + 灰度 + 回滚计划 |
| “把密钥写在 Dockerfile 里” | 密钥走密钥管理/CI secret，镜像里零密钥 |
| “镜像越大越好，工具全带上” | 多阶段构建，只带运行所需；可观测工具按需侧载 |
| “先上线再配监控” | 发布前先定义 SLI/SLO、关键告警与 runbook |
| “每个 500 都 page” | 按错误率/SLO burn 告警，加上持续时长与去重 |
| “回滚就是重新发旧版本” | 先确认 DB/协议兼容；必要时 expand/contract 或 rollforward |
| “日志全量存一年” | 结构化 + 分级采集 + 保留策略；敏感信息脱敏 |

## 与相邻子技能边界

- **dev-security**：密钥管理、依赖/容器漏洞扫描、供应链签名细节交给 dev-security；本技能只把它作为 CI 门禁与发布约束。
- **dev-performance**：指标可用于性能定位，但 profiling/慢查询/优化优先级交给 dev-performance；本技能只负责“采集哪些信号”。
- **dev-testing**：测试分层与 flaky 处理细节交给 dev-testing；本技能只定义“哪些测试要进发布门禁”。
- **dev-backend**：服务分层与可观测性基础有重叠；本技能从“发布与运行”视角补充，不重复 API/数据模型规范。

## 来源

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)
- [Docker: Best practices for writing Dockerfiles](https://docs.docker.com/build/building/best-practices/)
- [Docker: Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Kubernetes: Deployments (rolling update / rollback)](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes: Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [OpenTelemetry: Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/)
- [Prometheus: Alerting Overview](https://prometheus.io/docs/alerting/latest/overview/)
- [Prometheus: Alerting Best Practices](https://prometheus.io/docs/practices/alerting/)
- [12-Factor App: Build, release, run](https://12factor.net/build-release-run)
- [12-Factor App: Dev/prod parity](https://12factor.net/dev-prod-parity)
- [12-Factor App: Logs](https://12factor.net/logs)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`、`vault/skills/core-iteration/dev-workflow-consensus/`
