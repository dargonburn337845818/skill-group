# Quick Use：skill-vault-publish

> 一句话：把新蒸馏 skill 入库 dsh-skill-vault 的方法、目录规范、校验步骤与手动推送流程。

## 何时用

- 当任务命中 `SKILL.md` 的“触发条件 / 何时使用”时。

## 最小可复现动作

- 刚完成一次蒸馏，想把结果沉淀成可复用的 skill。
- agent 需要知道“新 skill 该放哪、怎么校验、怎么提交”。
- 1. **确认产物**：源目录必须含 `SKILL.md`，且满足蒸馏共识——触发/动作/边界/来源。
- 2. **选场景**（真实目录，先按 `vault/TAG_TAXONOMY.md` 的决策树判断）：

## 验证方式

- 按 `SKILL.md` 的干跑/检查清单执行；
- 发布/更新前跑 `skill_package_check.py` 与本 skill 对应校验。
