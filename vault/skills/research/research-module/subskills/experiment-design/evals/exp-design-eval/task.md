---
{
  "id": "exp-design-eval",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [],
  "expected_skill": "experiment-design",
  "expect_skill_invocation": "true",
  "timeout_ms": 300000,
  "checks": [
    "contains:假设",
    "contains:统计检验",
    "contains:样本量",
    "contains:可复现",
    "contains:EXP_OK"
  ]
}
---

为对比两套推荐算法设计实验方案，输出 markdown，必须覆盖变量与假设、统计检验、效应量/样本量、可复现步骤。最后输出 EXP_OK。
