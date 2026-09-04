# dev-ops-sre · 来源与证据

> 本技能为内部子技能（`activation=internal`）。以下来源均为官方一手文档/标准；每条用于支撑正文中对应小节。
> 采集验证：2026-09-04 通过 HTTP 请求确认大部分 URL 可访问（GitHub Actions、GitLab CI、Docker、Kubernetes、OpenTelemetry、Prometheus、12-Factor 均返回 200）；sre.google 在本环境不可直连，未列入正文来源。

## 来源清单

| URL | 标题/权威性 | 支撑正文 |
|---|---|---|
| https://docs.github.com/en/actions | GitHub Actions 官方文档 | CI/CD 门禁、secrets、缓存的通用参考 |
| https://docs.gitlab.com/ee/ci/ | GitLab CI/CD 官方文档 | 跨平台 CI 门禁、环境保护语义 |
| https://docs.docker.com/build/building/best-practices/ | Docker 官方 best practices | 多阶段、.dockerignore、最小化层、缓存顺序 |
| https://docs.docker.com/build/building/multi-stage/ | Docker 官方 multi-stage 文档 | 构建/运行分离、镜像瘦身 |
| https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ | Kubernetes 官方 Deployment 文档 | 滚动更新、回滚、副本与发布策略 |
| https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ | Kubernetes 官方探针文档 | liveness/readiness/startup 区分 |
| https://opentelemetry.io/docs/concepts/observability-primer/ | OpenTelemetry 官方 observability primer | 日志/指标/追踪三支柱与关联 |
| https://prometheus.io/docs/alerting/latest/overview/ | Prometheus 官方告警综述 | 告警规则、分组/抑制、severity |
| https://prometheus.io/docs/practices/alerting/ | Prometheus 官方告警实践 | 告警症状而非原因、避免告警疲劳 |
| https://12factor.net/build-release-run | 12-Factor App（Factor 9） | Build/Release/Run 分离、不可变制品 |
| https://12factor.net/dev-prod-parity | 12-Factor App（Factor 10） | 环境一致性 |
| https://12factor.net/logs | 12-Factor App（Factor 11） | 日志作为事件流、结构化输出 |

## 可信度

- 全部为官方一手文档/标准，符合 `verified-high`（官方一手即使单篇也算）。
- 未使用单一博客/教程作为普适规则；公司内部实践需按自身 SLO 调整。
- 本地隐藏底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`、`vault/skills/core-iteration/dev-workflow-consensus/`。
