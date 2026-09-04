---
{
  "id": "academic-eval",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [],
  "expected_skill": "academic-writing",
  "expect_skill_invocation": "true",
  "timeout_ms": 300000,
  "checks": [
    "contains:摘要",
    "contains:LaTeX",
    "contains:BibTeX",
    "contains:引用",
    "contains:ACAD_OK"
  ]
}
---

写一段学术摘要并给出 LaTeX/BibTeX 排版与引用检查清单，输出 markdown，必须覆盖结构、引用规范。最后输出 ACAD_OK。
