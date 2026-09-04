# 校验报告模板（verification report template）

```json
{
  "target": "distillation-consensus",
  "claims": [
    {
      "claim": "每条规则带 source_refs",
      "class": "static",
      "proof": "SKILL.md 规则段落均含 source_refs 字段；grep 命中 N 条",
      "verdict": "verified"
    },
    {
      "claim": "SKILL.md 能在 3 个真实样例上执行",
      "class": "runtime",
      "proof": "examples/dry_run.md 三个样例均跑通；输出与预期一致",
      "verdict": "verified"
    },
    {
      "claim": "复杂 task 能提升模型成功率 10%",
      "class": "data",
      "proof": "缺少 paired baseline 与 trials，无法复算",
      "verdict": "unverified",
      "gap": "需补 skilljack-evals 风格任务包：无 skill vs 有 skill"
    }
  ],
  "checks_observed_red": ["validate_contract", "behavior_test"],
  "evals": {
    "tasks": 0,
    "baseline": null,
    "with_skill": null,
    "lift": null,
    "anti_trigger": "pending"
  },
  "adversarial_review": {
    "blockers": [],
    "gaps": ["真实 A/B 缺失"],
    "notes": ["描述已含触发词，元数据可发现性尚可"]
  },
  "overall": "needs_work",
  "next_actions": ["补 3 个 eval 场景", "补 anti-trigger", "跑 baseline+with_skill 三次，填 lift"]
}
```
