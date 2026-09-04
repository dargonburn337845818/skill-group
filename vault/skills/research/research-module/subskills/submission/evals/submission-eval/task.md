---
{
  "id": "submission-eval",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [],
  "expected_skill": "research-submission",
  "expect_skill_invocation": "true",
  "timeout_ms": 300000,
  "checks": [
    "contains:选刊",
    "contains:Cover Letter",
    "contains:Response to Reviewers",
    "contains:拒稿",
    "contains:SUBMIT_OK"
  ]
}
---

为一篇论文写投稿准备清单，输出 markdown，必须覆盖选刊/会议匹配、cover letter、response to reviewers、拒稿处理。最后输出 SUBMIT_OK。
