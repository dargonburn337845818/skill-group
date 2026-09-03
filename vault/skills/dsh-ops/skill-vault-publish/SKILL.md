---
name: skill-vault-publish
description: 把新蒸馏的 skill 入库到 dsh-skill-vault 的方法；告诉 agent 仓库位置、目录规范、校验步骤，以及只能手动 git 推送。
---

# 入库 dsh-skill-vault

> 本 skill 是“向技能仓库发布新蒸馏产物”的操作手册。
> 仓库根：`$HOME/work/dsh-skill-vault`（远程：`https://github.com/dargonburn337845818/skill-group.git`）
> 插件：`@dsh-external/dsh-skill-vault`

## 何时使用

- 刚完成一次蒸馏，想把结果沉淀成可复用的 skill。
- agent 需要知道“新 skill 该放哪、怎么校验、怎么提交”。

## 入库流程

1. **确认产物**：源目录必须含 `SKILL.md`，且满足蒸馏共识——触发/动作/边界/来源。
2. **选场景**：
   - `teaching` 教学引导 / 拆题
   - `distillation` 内容蒸馏 / 知识化
   - `research` 科研 / 组会 / 论文
   - `dsh-ops` DSH 运维 / 工具
3. **生成 manifest**：在 skill 目录下写 `manifest.json`（可参考 `vault/manifest.schema.json`）。
4. **插件入库**（可选，自动拷贝+生成 manifest）：
   - 调用 `skill_vault_add`，传 `sourcePath`、`scenario`、`id` 等。
   - 工具只准备文件，**不会 git commit/push**。
5. **人工审核**：检查 `SKILL.md` 是否过长、来源是否可追溯、有无示例。
6. **手动推送**（必须人工，因为要输入 HTTPS 凭据）：
   ```bash
   cd $HOME/work/dsh-skill-vault
   bash scripts/push.sh
   ```
   脚本会提示确认并执行 `git add -A && git commit && git push`。

## 边界

- 不把个人开关状态提交进仓库（`enabled.json` 在 `~/.dsh/skill-vault/`）。
- 不自动推送；不要在 agent 会话里让模型持有密码或直接执行 `git push`。
- 外部开源项目（如 ai-ppt 等别人的 skill）不迁入本仓库，除非是你自己的蒸馏产物。
