---
{
  "id": "math-consensus-eval",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [],
  "expected_skill": "teacher-math-consensus",
  "expect_skill_invocation": "true",
  "timeout_ms": 300000,
  "checks": [
    "contains:引导",
    "contains:反例",
    "contains:边界",
    "contains:MATH_OK"
  ]
}
---

设计一道数学证明题的引导性提问流（不直接给答案），输出 markdown，必须覆盖定义、反例、边界、收敛。最后输出 MATH_OK。
