---
{
  "id": "dev-ai-pilot",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [],
  "expected_skill": "dev-ai-engineering",
  "expect_skill_invocation": "true",
  "timeout_ms": 300000,
  "checks": [
    "contains:上下文预算",
    "contains:RAG",
    "contains:评测",
    "contains:降级",
    "contains:CHECKLIST_OK"
  ]
}
---

你是一位软件工程师，正在为一个内部工具设计大模型集成方案。请给出一个可执行的最小方案，输出 markdown，必须覆盖：上下文预算、RAG 检索、工具调用契约、评测与降级。最后输出一行 CHECKLIST_OK。
