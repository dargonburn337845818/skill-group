# Quick Use：inspiration-miner

> 一句话：从 GitHub 真实开源仓库中挖掘插件/skill/元能力灵感，评分排序并反哺递归升级。

## 何时用

- 当任务命中 `SKILL.md` 的“触发条件 / 何时使用”时。

## 最小可复现动作

- 用户/调度器需要“插件思路 / 新功能方向 / 元能力升级灵感”。
- 已有元能力进入瓶颈，需要外部对照。
- 需要找到与 DSH / agent skills / plugin / harness 相关的开源项目作为参照。
- 1. **真实检索**：运行 `tools/mine_ideas.py --proxy-mode host --limit 6`。

## 验证方式

- 按 `SKILL.md` 的干跑/检查清单执行；
- 发布/更新前跑 `skill_package_check.py` 与本 skill 对应校验。
