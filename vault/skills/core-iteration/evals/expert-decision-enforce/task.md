---
{
  "id": "expert-decision-enforce",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [],
  "expected_skill": "expert-decision-consensus",
  "expect_skill_invocation": "true",
  "timeout_ms": 300000,
  "checks": [
    "contains:0 Brief",
    "contains:1 Evidence",
    "contains:3 Conflict",
    "contains:4 Adjudicate",
    "contains:7 Verify",
    "contains:decision_log_entry",
    "files:report.md"
  ]
}
---

请对「是否把某个已下载的 PDF 文献工具接入团队资源库」做一次规范化专家决策，并把结果写入 report.md。报告必须包含以下标题原样保留：0 Brief、1 Evidence、3 Conflict、4 Adjudicate、7 Verify；并至少给出一条机器可读的 decision_log_entry。
