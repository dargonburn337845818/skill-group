---
{
  "id": "dev-ops-eval",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [],
  "expected_skill": "dev-ops-sre",
  "expect_skill_invocation": "true",
  "timeout_ms": 300000,
  "checks": [
    "contains:CI/CD",
    "contains:容器",
    "contains:可观测",
    "contains:回滚",
    "contains:OPS_OK"
  ]
}
---

为一个内部 Node.js 服务设计安全可回滚的发布流程，输出 markdown，必须覆盖 CI/CD、容器镜像、日志/指标/追踪、告警、回滚。最后输出 OPS_OK。
