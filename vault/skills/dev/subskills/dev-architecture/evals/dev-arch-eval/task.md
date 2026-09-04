---
{
  "id": "dev-arch-eval",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [],
  "expected_skill": "dev-architecture",
  "expect_skill_invocation": "true",
  "timeout_ms": 300000,
  "checks": [
    "contains:服务拆分",
    "contains:消息",
    "contains:一致性",
    "contains:容量",
    "contains:ARCH_OK"
  ]
}
---

为一个需要拆微服务的系统做架构决策，输出 markdown，必须覆盖服务拆分、消息队列、一致性模型、容量估算。最后输出 ARCH_OK。
