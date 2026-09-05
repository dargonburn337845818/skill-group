# Design Skill Control Loop — 完整共识

> 本文是 `SKILL.md` 的完整依据与实现细节；SKILL.md 负责可调用摘要，本文负责“为什么、怎么落地、反例怎么处理”。

## 1. 问题

当前 DSH 技能体系已有「路由 + 开关」，但缺三个闭环能力：

1. **没有运行期传感器**：不知道 skill 是否真的被采用、是否改变行为、是否误触发。
2. **控制器不读效果**：路由/推荐只依据首条消息的文本分类，不依据效果数据。
3. **技能库更新是一次性堆叠**：缺少“一个 skill 一个可审查变更 + 反馈文件 + 流量控制”的纪律。

本共识把控制论模型平移到技能库治理，解决上述三个缺口。

## 2. 控制论映射

- **系统**：DSH 技能库（`enabled.json` + vault 目录 + 运行时 `ctx.skills` 注册状态）。
- **设定点**：理想状态是“技能总集合很小、每个技能触发精准、上下文成本可控、行为增益可测”。
  - 示例阈值：全局 enabled ≤ 底座 + 当前场景；效果率 ≥ 60%；误触发率 ≤ 20%；连续 2 轮无行为增量 → 收敛。
- **传感器**：
  - 静态：`skill_vault_list`、`enabled.json`、`skill_package_check`、`validate-vault`、`validate-tags`。
  - 运行期（待建）：`skill_effect_log`——每次使用后记录 `skill_id / task / triggered? / used? / outcome(+/-/0) / forced_user? / date`。
  - 健康检查（待建）：`skill_doctor`——三件套完整性、manifest 与目录一致、重复/语义重叠、断链、enabled 但未注册、过期来源。
- **误差**：`setpoint - measured`。例如设定点“效果率≥60%”，某 skill 实际 35% → 误差 +25%，控制器输出“降权/停用/待复核”。
- **控制器**：从确定性规则起步：
  - 如果误触发率高于阈值 → 优先修 `description` / `whenToUse` 或停用；
  - 如果效果率低于阈值 → 进入“待复核”，不自动删除；
  - 如果与另一 skill 语义重叠 → 标记 conflict，交给用户裁决；
  - 如果连续两轮无行为增量 → 调用 `value-validator` 的 STOP 逻辑，收敛或归档。
- **执行器**：一次只改一个 skill：
  - 修改 `SKILL.md`、`manifest.json`、`CHANGELOG.md`；
  - 更新后跑校验脚本与 3 个样例干跑；
  - 形成可审查 diff/PR，不做“全库重构”式大 PR。
- **干扰**：新 skill 入库、新专家/场景、模型生态变化、用户手动打开、插件升级。
- **阻尼器**：
  - 所有新 skill 默认 `activation: catalog`；
  - 质量门不过不得 enable；
  - 治理循环期间不得继续新增无证据常驻 skill。
- **流量控制**：每个 skill 治理主题最多一个开放变更；用标签/分支标识（如 `skill-gov-<skill-id>`）。
- **人类在环**：持久反馈文件 `agent-memory/skill-governance.md`；评论/反馈触发下一轮修改；用户可随时 `override`。

## 3. 落地步骤

### 3.1 先做低风险项
1. 全局 enabled 收敛为“底座三件套 + 当前场景”。
2. 增加 `skill_effect_log` 记录工具。
3. 增加 `skill_doctor` 健康检查。
4. 新 skill 默认 catalog，不自动 enable。

### 3.2 再接控制器
- 把 `core-iteration` 现有的 `value-meta-scheduler` / `benefit-filter` / `value-validator` 作为“技能库治理循环”的内核；
- 新增一个轻量的“技能库效果传感器”数据文件；
- 控制器输出：`enable / disable / demote / merge / archive / update-description` 六类动作建议；
- 所有动作建议只给“建议”，最终由人确认或由周度工作流小步执行。

### 3.3 形成周期
- 建议节奏：周度传感器读数 + 月度小步执行；
- 每次只处理 1–3 个 high-priority skill；
- 每次执行后更新 `CHANGELOG.md` 与效果日志。

## 4. 反例处理

| 反例 | 正确处理 |
|---|---|
| “我觉得这个 skill 很全面” | 不成立；必须有行为差异/效果数据 |
| 一次改 10 个 skill | 拒绝；拆成 10 个可审查变更 |
| 只看来源数量 | 不足；要看误触发/效果/上下文 |
| 新 skill 直接 enable | 违反阻尼器；默认 catalog |
| 热更运行中 agent | 违反 DSH 运维共识；隔离冒烟后落地 |
| 用“没搜到”证明不存在 | 只写“当前公开检索未发现” |

## 5. 验收标准

- 有明确设定点（可选但推荐）与至少一个可测量指标；
- 传感器能用（至少能列出 enabled 数量与静态质检结果）；
- 控制器能输出“下一步动作”而不是“继续观察”；
- 执行器遵循“一次一个 skill + 校验 + 干跑 + 变更日志”；
- 文中所有来源可复核，不把推测写成事实。
