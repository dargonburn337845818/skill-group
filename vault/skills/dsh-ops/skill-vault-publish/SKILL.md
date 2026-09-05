---
name: skill-vault-publish
description: 把新蒸馏的 skill 入库到 dsh-skill-vault 的方法；告诉 agent 仓库位置、目录规范、校验步骤，以及默认交互/可自动化的 git 推送流程。
whenToUse: 刚蒸馏完新技能；需要把产物放进技能仓库并提交开源。
---
# 入库 dsh-skill-vault

> 本 skill 是“向技能仓库发布新蒸馏产物”的操作手册。
> 仓库根：`$PROJECT_ROOT`（远程：`https://github.com/dargonburn337845818/skill-group.git`）
> 插件：`@dsh-external/dsh-skill-vault`

## 何时使用

- 刚完成一次蒸馏，想把结果沉淀成可复用的 skill。
- agent 需要知道“新 skill 该放哪、怎么校验、怎么提交”。

## 入库流程

1. **确认产物**：源目录必须含 `SKILL.md`，且满足蒸馏共识——触发/动作/边界/来源。
2. **选场景**（真实目录，先按 `vault/TAG_TAXONOMY.md` 的决策树判断）：
   - `base` 常驻底座 / 搜索与共识
   - `core-iteration` 核心迭代元能力 / 价值递归提升
   - `dev` 开发模块
   - `distill` 蒸馏编排层
   - `teacher` 教师模块壳（回合式讨论）
   - `teaching` 教学引导 / 拆题（领域内容）
   - `research` 科研 / 组会 / 论文
   - `writing` 文稿 / 提示词 / 文案 / 报告
   - `distillation` 内容蒸馏 / 知识化
   - `dsh-ops` DSH 运维 / 工具
   - `github` GitHub 开源仓库 / Actions
3. **生成 manifest**：在 skill 目录下写 `manifest.json`（可参考 `vault/manifest.schema.json`）；`tags` 从 `TAG_TAXONOMY.md` 受控词表中选，≤8 个，禁止状态词。
4. **插件入库**（可选，自动拷贝+生成 manifest）：
   - 调用 `skill_vault_add`，传 `sourcePath`、`scenario`、`id` 等。
   - 工具只准备文件，不主动执行 git commit/push；提交/推送统一走 `scripts/push.sh`。
5. **审核**：检查 `SKILL.md` 是否过长、来源是否可追溯、有无示例、`tags` 是否符合分类法。
6. **推送**（默认交互确认，也支持全自动）：
   ```bash
   cd $PROJECT_ROOT
   bash scripts/push.sh
   # 全自动（凭据已由 credential helper / CI secret 配置时）
   bash scripts/push.sh --yes --message "vault: update distilled skills"
   # 或
   PUSH_CONFIRM=yes PUSH_MESSAGE="vault: update distilled skills" bash scripts/push.sh
   ```
   脚本会提示确认并执行 `git add -A && git commit && git push`；自动模式仍会拒绝内部开发产物。

## 边界

- 不把个人开关状态提交进仓库（`enabled.json` 在 `~/.dsh/skill-vault/`）。
- 默认不自动推送；自动化必须显式开启（`--yes`/`PUSH_CONFIRM=yes`）且凭据可用。不要在 agent 提示词里粘贴密码；凭据只走 credential helper / CI secret 等安全通道。
- 外部开源项目（如 ai-ppt 等别人的 skill）不迁入本仓库，除非是你自己的蒸馏产物。

## 2026 深度补强（Round 38）

> 本节是外部生态的“硬约束”补强，用于发布前自查；本地脚本只保证最小契约，以下规则补足跨端兼容、版本、安全与回滚。来源索引见 `SOURCES.md`「Round 38 新增来源」。

### 1. 目录与命名一致性（发布前必查）

- skill 目录名必须等于 `SKILL.md` 的 `name`，且 `manifest.id` 使用同一串小写 `kebab-case`。
- `name` 只能是 1–64 字符、小写字母/数字/连字符；不能以连字符开头/结尾，也不能出现连续连字符（`pdf--processing` 非法，`PDF-Processing` 非法）。
- 文件名必须是 `SKILL.md`，不要写成 `skill.md` 或 `Skill.md`；大小写敏感的客户端会读不到。
- 只允许一层场景 + 一层 skill；模块内部能力放 `module/subskills/` 并以 `activation: internal` 归档，不独立注册。
- 反例：frontmatter 写 `name: pdf-processing` 但目录叫 `PDF-Processing`，客户端按目录生成命令名时失配，技能“装上了但调不响”。

### 2. manifest 与 SKILL.md 双份元数据一致性

- 本地 `manifest.json` 必填 `id`/`description`/`scenario`；`id` 匹配目录名，`scenario` 匹配物理目录，`tags` ≤8 且无状态词。
- 若有 `manifest.version`，按 SemVer 维护；`manifest.sourceRefs` 每条必须落地：本地路径存在、公开 URL 可访问，不留幽灵引用。
- DSH 扩展字段（`whenToUse`、`routing`、`qualityCriteria`、`boundary`、`notWhenToUse`、`activation`、`hidden`）不是通用 Agent Skills 规范字段；面向 Claude.ai / Agent Skills API 上传时会被未知字段检查拦截，DSH 内部可保留，跨端发布前应确认目标客户端接受或移除。
- 反例：`manifest.version: "0.1.0"` 但 git tag 是 `v0.2.0`，Release 产物版本外观不一致，用户拿到的包无法与 Release 对应。

### 3. SKILL.md 结构与体量检查

- 前导 `---` 必须是文件第一行；frontmatter 外另有内容时，部分客户端把整份文件当正文。
- `description` 要同时说清“做什么 + 何时用”，不要只写“帮助处理 X”；规范允许 1–1024 字符，Claude.ai 上传限 200 字符，超长会被截断。
- 正文建议 <500 行 / <5000 tokens；更细材料拆到 `references/`，引用路径用相对路径且保持在 1 层深。
- 被引用的 `references/`、`scripts/`、`assets/` 文件必须真实存在；反之，未被正文引用的 `references/` 文件永远不会加载，应删除或显式引用。
- 反例：正文写 `see [reference.md](reference.md)`，但实际文件在 `references/REFERENCE.md`；或引用 `scripts/extract.py` 而文件缺失——技能看起来触发了，执行时却失败。

### 4. 版本语义与发布顺序

- 用 SemVer 决定 `manifest.version`：不兼容变更（改 `id`/`scenario`/可注册语义）→ major；新增触发场景或能力且向后兼容 → minor；只改文案/来源/小修复 → patch。
- 每轮内容修改同步更新 `manifest.version` 与 `CHANGELOG.md`，禁止“内容变了版本不变”。
- 发布顺序：本地 `node scripts/validate-vault.mjs` && `node scripts/validate-tags.mjs` && `npm test` 全绿 → `git diff` 审查 → `bash scripts/push.sh`（默认交互；自动化需 `--yes`/`PUSH_CONFIRM=yes`，脚本只接受公开目录）。
- 插件级 Release 打 `v*` 注释 tag（`git tag -a v0.1.0 -m ...`）后 push；tag 一旦推送不要 force-push 改写，修复走新 patch release（fix-forward）。
- 反例：先 `git push origin main` 再补 tag，Actions 没触发或 tag 指向旧 commit；或删除已发布 tag 重建，破坏依赖该 tag 的安装者与缓存。

### 5. 安全扫描与最小授权

- 发布前扫描 `SKILL.md`、`scripts/`、`examples/`：不得含真实 API key、密码、token、私钥；用 `git diff --cached` 复核新增内容。
- 若 skill 带脚本/`allowed-tools`，坚持最小授权：能写 `Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/x.py *)` 就不要写 `Bash(*)`。
- 对检入仓库的第三方 skill，先审 `allowed-tools`、`!` 动态命令与网络访问；工作区信任不 gate `allowed-tools`，宽泛授权等于把越权风险交给每一个打开仓库的人。
- 反例：在 `scripts/` 里硬编码内部 token；或给一个“只做读摘要”的 skill 配上 `allowed-tools: Bash(*)`。

### 6. 回滚与事故处置

- 发布前记录当前 HEAD commit hash 与上一个稳定版本号，作为回滚锚点；不要依赖“删掉重发”这种不可追溯的修复。
- 若新发布导致问题，优先新建修复提交（fix-forward），而不是删除/改写已发布 Release；GitHub Release 可用 draft/prerelease 先行，正式发布只保留可追溯 commit。
- 回滚前先确认：目标版本是否跨越了不可逆数据/状态变更（类似 post-deploy migration 的边界），以及是否有部署/发布正在进行；确认安全后再动作。
- 需要撤销历史时必须用 `git revert <bad-commit>` 生成新提交，不要 `git reset --hard` + force push——protected branch 默认禁 force push 与删除，且改写历史会破坏所有 clone。
- 回滚只是缓解，不是结束：落地后继续 fix-forward，并补一条“为什么没在下发前发现”的记录。

### 7. 发布前自行核对清单

- [ ] `SKILL.md` 文件名大小写正确，`---` 是第一行，`name` 与目录名完全一致。
- [ ] `description` 写明触发场景且长度合规。
- [ ] 正文 <500 行，引用文件存在且路径正确，未被引用的 reference 已清理。
- [ ] `manifest.json` 必填项齐全，`version` 已按 SemVer 递增，`CHANGELOG.md` 已更新。
- [ ] `tags` ≤8、无状态词，`sourceRefs` 可落地。
- [ ] 无密钥/令牌；`allowed-tools` 最小化。
- [ ] `validate-vault`、`validate-tags`、`npm test` 全绿。
- [ ] 只走 `scripts/push.sh`（默认交互；自动化显式 `--yes`/`PUSH_CONFIRM=yes`），不把内部产物/个人开关状态带进公开仓库。
- [ ] 插件级发布有 `v*` tag 与已记录的 HEAD 回滚锚点。
