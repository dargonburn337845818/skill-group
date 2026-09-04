---
{
  "id": "eval-task-eval",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [],
  "expected_skill": "distill-eval-task",
  "expect_skill_invocation": "true",
  "timeout_ms": 300000,
  "checks": [
    "contains:prompt",
    "contains:checks",
    "contains:anti-trigger",
    "contains:对照",
    "contains:EVAL_OK"
  ]
}
---

为一个技能设计评测任务包，直接在回复中输出一份精简的 markdown 方案，必须包含：真实任务 prompt 示例、确定性 checks 示例、anti-trigger 任务、无/有 skill 对照设计。请在最终回复里呈现这些要点，不要只写文件。最后输出 EVAL_OK。
