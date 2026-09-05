# Contributing to dsh-skill-vault

感谢你愿意给这个开源技能库贡献内容。

## 提 issue / PR

- 先搜索已有 issue，避免重复。
- 描述尽量包含：复现步骤、期望行为、实际行为、环境（DSH 版本、Node 版本）。
- 改技能内容时，请保持 `SKILL.md` 的“触发 / 动作 / 边界 / 来源”四件套。
- 不要把个人开关状态（`~/.dsh/skill-vault/enabled.json`）提交进仓库。

## 新增一个 skill

1. 在 `vault/skills/<scenario>/<skill-id>/` 下创建 `SKILL.md` 与 `manifest.json`。
2. 运行 `node scripts/validate-vault.mjs` 与 `node scripts/validate-tags.mjs`，确保通过。
3. 运行 `npm run typecheck` 与 `npm test`，确保插件没有回归。
4. 执行 `bash scripts/push.sh` 提交（脚本会拒绝把内部产物推上去；默认交互确认，自动化时可用 `--yes --message "..."`）。

## 代码风格

- TypeScript strict 模式；公共接口尽量小而深。
- 提交生成产物 `lib/` 时，确保 `src/` 与 `lib/` 同步。
- 不要提交 `node_modules/`、`*.tgz`、`__pycache__/`。
