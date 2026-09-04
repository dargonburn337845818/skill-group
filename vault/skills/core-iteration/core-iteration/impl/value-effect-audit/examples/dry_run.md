# Value-Effect-Audit 干跑样例

## 场景：单次成功不升级

- 输入：1 个任务、1 次成功。
- 预期：`effect_confidence=low`，节点标 `single-effect` 并继续观察。

## 场景：A/B 结果

- 输入：3 个任务，无 skill 成功率 0.33，有 skill 0.67。
- 预期：输出 `resolution_rate`、`skill_lift`，并给出 `needs_evidence` / `promote` 建议。
- 检查：结果能回到 task_id / node_id / source_ref。
