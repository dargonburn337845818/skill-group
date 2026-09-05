---
name: design-skill-control-loop
description: 把 DSH 技能库当成动态系统，用控制论四件套（设定点/传感器/控制器/执行器）设计一个可观测、可收敛、可审查的治理循环；用于用户要优化 skill 调度、技能库质量、减少上下文膨胀时。
whenToUse: 用户问“怎么优化我的技能调度/技能库”“技能太多/太杂”“该不该启用某个 skill”“如何判断 skill 还有没有用”“给技能库加反馈/效果度量”时。
---

# Design Skill Control Loop

> 核心心智：不要只继续“加更多/写更好”的 skill，要把技能库当成一个被持续扰动的动态系统，用 **设定点 → 传感器 → 控制器 → 执行器 → 反馈** 的循环来治理。

## 触发条件

- 用户说“优化技能调度 / 技能库 / 技能质量 / 上下文膨胀”。
- 用户问“哪些 skill 该常驻、哪些该按需、哪些该停用”。
- 用户要给技能库增加效果度量、反馈文件、或“自动判断 skill 是否还有用”。
- 需要在“内容蒸馏”之外，给技能库本身设计一个治理/审计工作流。

## 核心模型（控制论四件套 + 扩展）

| 组件 | 在 DSH 技能库中对应什么 |
|---|---|
| 设定点 | 每个 skill 的目标：该触发时触发、该生效时生效、不占无谓上下文；用可测量指标表达（误触发率、效果率、enabled 数量、上下文成本） |
| 传感器 | 测量“当前技能库状态”：`skill_vault_list` / `enabled.json` / `skill_package_check` / `validate-vault` / 运行期 `skill_effect_log` / `skill_doctor` / `skill_governance` |
| 控制器 | 根据测量值决定“下一个动作”：启用/停用/降权/合并/归档/更新某个 skill；从确定性阈值到数据驱动策略，先简单后调优 |
| 执行器 | 对 skill 本体做一个小而可审查的变更：改 `SKILL.md` / `manifest.json` / `CHANGELOG.md`，更新后跑校验与干跑 |
| 干扰 | 新 skill 入库、新专家/领域、用户手动开关、插件升级、模型/生态变化 |
| 阻尼器 | 新 skill 默认关闭；质量门不过不得直达 enabled；技能库不得在治理循环期间继续膨胀 |
| 人类在环 | 用 `agent-memory/skill-governance.md` 类文件承载持久反馈；用户评论/反馈驱动下一轮修改 |
| 流量控制 | 每个技能治理主题最多一个开放变更，避免一次改十几个 skill 造成不可审查的大 PR |

## 动作（最小可执行链）

### Phase A — 审计当前状态
1. 读 `~/.dsh/skill-vault/enabled.json` 与 `skill_vault_list`，列出：全局常驻、按需启用、已归档。
2. 数一下当前全局 enabled 数量；若超过“底座 + 当前场景”的合理范围，标记为上下文膨胀候选。
3. 跑静态质检：`validate-vault` / `validate-tags` / `skill_package_check`，记录红灯。
4. 找现有反馈材料：`SKILL_EFFECT_REPORT.md`、`skills/*/CHANGELOG.md`、历史迭代报告；没有运行期效果数据要如实标注。

### Phase B — 采访并定设定点
一次只问一个最高信息增益问题，优先确认：
- 这次治理的目标：减上下文？提效果？清重复？还是建立长期反馈回路？
- 愿意接受的指标与阈值（如：效果率 < 40% 或误触发率 > 30% 就停用/降权）。
- 哪些 skill 是“永远不该给 AI 自动调用”的（如涉及密钥、外部发布、破坏性操作）。

### Phase C — 设计三件套
1. **传感器**：确定用什么记录“使用效果”。推荐最小方案：`skill_effect_log`（`skill_id / task / triggered? / used? / outcome / date`），落盘到 `~/.dsh/skill-vault/effect-log.json`，不进 git。
2. **控制器**：先写确定性规则，不急着上复杂模型：
   - 使用 `skill_governance`（插件工具/API 或 `scripts/skill_governance_controller.py`）读取 effect-log + doctor，输出每个 skill 的建议；
   - 新 skill 默认 `activation: catalog`（只进目录，不自动启用）；
   - 有真实效果记录且通过质量门，才允许 `enable`；
   - 连续 N 轮无行为增量 → 归档/收敛（可复用 `value-validator` 的 STOP 逻辑）。
3. **执行器**：每次只改 1 个 skill，产出可审查 diff：
   - 改 `SKILL.md` 时保持三件套（触发/动作/边界）与来源；
   - 更新 `manifest.json` 版本与 `CHANGELOG.md`；
   - 改完跑 3 个样例干跑 + 校验脚本，不通过不得宣告完成。

### Phase D — 本地验证再进入周期
- 每个组件先能在本地单独跑（`skill_vault_list`、`skill_doctor`、`skill_effect_log`、`skill_governance_controller.py suggest`）；
- 再考虑配置成周/月级治理 workflow，而不是一次“全库重构”。

### Phase E — 人类在环与流量控制
- 在技能库仓库建立 `agent-memory/skill-governance.md`，记录：已知误触发、用户偏好、金标准、待验证项。
- 每次治理变更用标签标识（如 `skill-gov-<skill-id>`），检查是否已有开放变更；有则先关闭旧的，避免堆积。

## 附带工具（本 skill 包的 scripts/）

- `scripts/skill_doctor.py`：健康检查传感器。检查 SKILL.md/manifest 一致性、三件套、引用文件、CHANGELOG；可选与 `~/.dsh/skill-vault/enabled.json` 交叉核对。
- `scripts/skill_effect_log.py`：运行期效果记录。`record` 记录一次使用，`report` 输出明细，`stats` 输出按 skill 的效果率/误触发率。
- `scripts/skill_governance_controller.py`：治理控制器。`suggest` 输出建议，`init` 初始化 `agent-memory`，`flow` 管理开放变更（流量控制）。
- `references/skill-governance-memory-template.md`：人类反馈文件模板，用于 `agent-memory/skill-governance.md`。
- 用法示例：
  ```bash
  python3 scripts/skill_doctor.py <skill-dir>
  python3 scripts/skill_effect_log.py record --skill <id> --task "..." --triggered true --used true --outcome pos
  python3 scripts/skill_effect_log.py stats
  python3 scripts/skill_governance_controller.py --repo $HOME/work/dsh-skill-vault suggest
  python3 scripts/skill_governance_controller.py --repo $HOME/work/dsh-skill-vault flow add --skill <id>
  ```

## 边界 / 反例

- **不是内容蒸馏**：本 skill 治理“技能库怎么迭代”，不替代 `distillation-consensus`（那是把材料变成可执行知识）。
- **不要一次性全库重构**：一次改一个 skill，小步可审查。
- **不要只看来源数量**：效果必须落在“行为是否改变/误触发是否下降”上。
- **不要热更运行中的 agent**：改 `dsh-skill-vault` / `dsh-skill-router` 插件前先读 `dsh-optimization-consensus`，隔离冒烟后再落地。
- **不要无证据启用**：没有效果记录的 skill 默认关闭，可以用但别常驻。
- **不要只做“清单”**：传感器没有真实数据时，先诚实输出“当前无运行期数据”，不要假装有。

## 用户话术

> 我会先把你的技能库当成一个控制系统看：设定点（希望技能达到什么效果）、传感器（怎么知道它有没有用）、控制器（下一步该启用/停用/改谁）、执行器（一次只改一个技能并验证）。先给你方向、方式和边界；如果你说“感觉不对劲”，我会停下来重新检查。

## 来源

- HumanLayer `design-control-loop` / `build-iterated-agentic-loop`：https://github.com/humanlayer/skills
- HumanLayer `12-factor-agents`（Own context window / Small focused agents / Own control flow）：https://github.com/humanlayer/12-factor-agents
- 本机审计报告：`$HOME/work/control-loop-skill-audit-2026-09-06.md`
- B 站视频 BV1Sw3H66Eav（中配 Kyle Mistele 演讲）：https://www.bilibili.com/video/BV1Sw3H66Eav/
