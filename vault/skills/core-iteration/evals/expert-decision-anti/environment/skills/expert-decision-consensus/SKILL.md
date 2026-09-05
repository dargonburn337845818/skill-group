---
name: expert-decision-consensus
description: 规范化专家决策共识——把“专家意见”升级为可检查、可追溯、可验收的决策流程；统一科研/教学/开发/写作/蒸馏的专家团回合、证据台账、阶段门禁、子代理执行与技能蒸馏。用于任何需要多人专家评审、方案决策、流程门禁或可追溯验收的场景。
whenToUse: 用户需要多位专家/导师/审稿人评审方案、做科研/教学/开发决策、给流程加验收门禁、把重复工作流沉淀为 Skill，或希望“AI 不只给意见，还能给出可检查的决策链”时。
---

# 专家决策共识（Expert Decision Consensus）

> 一句话：**AI 缺的不是更多知识，而是把“专家决策”变成可检查、可追溯、可验收的规范流程。**
> 本 skill 是通用层：在 `teacher-module` 的回合式专家团之上，补上证据纪律、阶段门禁、执行编排、记忆回写与技能蒸馏；科研、教学、开发、写作、蒸馏都复用同一套决策环，不另起炉灶。

## 触发条件

- 用户要“多位专家/导师/审稿人给出意见并决策”；
- 用户要“规范化流程”用于科研、教学、开发、写作、蒸馏；
- 用户要“AI 缺开发规范 / 决策总在拍脑袋 / 做完无法验收”；
- 用户要把一个反复出现的流程固化成可复用 Skill 或规则。

## 九段决策环（EDGE Loop）

> 每段都有“完成才进入下一段”的 gate；未过 gate 不往下凑。

```text
0 Brief       定目标：为谁、什么处境、交付什么可观测结果、不做什么
1 Evidence    证据收集：检索/数据/代码/材料 → 来源台账
2 Panel       专家独立表态：每轮独立、署名、带 sourceRefs
3 Conflict    冲突点表：claim_a / claim_b / 来源 / 对齐专家
4 Adjudicate  裁决：adopt_a / adopt_b / merge / reject / defer
5 Plan        行动计划：子任务 / 接口 / 验收条件 / 负责人
6 Execute     执行编排：主线程 + 子代理并行/接力/续跑
7 Verify      证据化验证：P1=0 / 测试过 / 引用可核验 / 见过红
8 Log & Distill 回写决策日志与台账；重复流程蒸馏成 Skill/规则
```

### 0 Brief（对齐）

- 写北极星：为谁、什么处境、交付什么可观测结果。
- 写非目标：明确“这次不做”的清单。
- Gate：一句话目标 + 交付物 + 非目标都写下来；缺一样先问，不猜。

### 1 Evidence（证据）

- 先检索/收集，再表态；不拿记忆直接补外部事实。
- 每条关键主张挂 `source_refs`；只标 `fact / inference / unknown`。
- 无来源 = `single-doubt`；同源转载不算独立；“不确定”不是“否”。
- Gate：所有关键事实有来源或已标 unknown；当前检索无果要写“未发现”，不写“不存在”。

### 2 Panel（专家团）

- 用 `expert_team_start` / `teacher_discussion_start` 加载 ready 人名专家。
- 每位专家独立表态，只给“按公开风格的倾向”，不互相看答案。
- 输出必须带 `expert_id` + `expert_name` + `sourceRefs`，注明“风格推断，非本人原话”。
- Gate：每个专家都有名字、领域、来源；无 ready 专家时显式走 `expert_gap`，不静默降级。

### 3 Conflict（冲突）

- 相同问题不同立场必须写成冲突条目，不强行合并。
- 专家 A 主张 X、专家 B 主张 Y → 保留两个分支，不要揉成 50% 共识。
- Gate：至少存在一份冲突点表；若本轮无冲突，显式写“本轮无冲突”。

### 4 Adjudicate（裁决）

- 主持人或用户选择：采纳 A / 采纳 B / 合并 / 驳回 / 延后。
- AI 可以给建议，但最终裁决人必须记录（主持人或用户）。
- 信息不足不能硬裁 → `defer` 保留开放分支。
- Gate：每条冲突都有 `adjudicator` + `decision`；未决冲突标 `defer` 并保留。

### 5 Plan（计划）

- 把决策落成可执行计划：子任务、公开接口、验收条件、负责人（主线程/子代理）。
- 每个子任务必须能测量“完成”；没有验收条件的任务不进入执行。
- Gate：计划包含阶段、接口/契约、验收标准；计划本身经过一次对抗式检查（BLOCKER/GAP/NOTE）。

### 6 Execute（执行）

- 主线程负责规划、集成、验证；重复/机械型工作交给子代理。
- 子代理纪律：明确能碰的文件/不能碰的文件/要跑的命令；重叠文件串行；子代理不进 git 状态。
- 接力：前一个交得出，后一个才接；断了能自己续上，不靠用户点“继续”。
- Gate：每个子代理产出过 gate 才交给下一手；不合格重做，不跳步凑结果。

### 7 Verify（验证）

- 用 `skill-verification-consensus` 的证据分类证明：static / runtime / data / rendering / tooling。
- 每个机械可判断的点必须“见过红”才算验证：故意破坏 → 变红 → 恢复 → 变绿。
- 专家/审稿类验证：P1（致命问题）= 0 才放行；第二轮逐条核对是否真实处理。
- Gate：无未决 P1 / BLOCKER；证据可回溯；有 conflicts 未裁决不得宣称通过。

### 8 Log & Distill（回写与蒸馏）

- 写决策日志：`decision_log_entry` 含 id / 阶段 / 角色 / 决策 / 证据 / 裁决人 / 未决分支。
- 写课题/项目台账：假设、实验、结论、引用、矛盾、待验证项，跨会话可续。
- 重复出现的工作流，用 `distillation-consensus` 蒸成新 Skill 或规则；用户纠正累计后更新画像/规则。
- Gate：台账已更新；本次决策可被下次会话读取；可复用流程已入 skill 目录或候选清单。

## 领域适配（同一套环，不同落地）

| 场景 | 专家/来源 | 领域流程 | 本环重点 |
|---|---|---|---|
| 科研 | `research-module` 导师团 | 读论文 → 理脉络 → 实验 → 写作 → 投稿/组会 | 证据台账、引用可点回原文、新颖性审计、三轮审查 |
| 教学 | `teacher-module` / `teacher-consensus` | 拆题 → 引导 → 讨论 → 复盘 | 独立表态、冲突表、信息论式追问、一次一问 |
| 开发 | `dev-workflow-consensus` | Frame → Spec → Gate → Build → Verify → Ship | 规格门禁、接口测试、对抗审查、redteam |
| 写作/PPT | `writing-module` / `ai-ppt` | 受众 → 结构 → 稿件 → 成品 | 交付文件、风格保真、可编辑产物 |
| 蒸馏 | `distillation-consensus` | 定目标 → 选语料 → 提原语 → 校验 | 来源可追溯、保留分歧、样例干跑、人工复核 |

## 硬性纪律

1. **人类最终裁决**：用户说“我感觉不对劲”时，停止套模板，重新核验；AI 不拥有最终决定权。
2. **没有证据不成立**：无来源的“专家说”降权；编造引用/数据是红线。
3. **冲突不平均**：专家 A 主张 X、专家 B 主张 Y，保留两个分支，不揉成中间值。
4. **不静默降级**：没有 ready 专家时走 `expert_gap` 分支，不直接用大模型冒充专家。
5. **一次一个高信息增益问题**：和用户交互时，不问一串，只问最能把候选空间砍半的问题。
6. **交付是文件/产物**：论文、教案、代码、PPT、图、报告都落到工作区；只回聊天不算交活。
7. **保真红线**：润色/去 AI 味/改稿不得改变数字、引用、术语、claim 强度；改前先保全审计。
8. **有界子代理**：数量有界、模型分层、同文件串行、不碰 git 状态。

## 输出契约（机器可读）

```text
decision_log_entry = {
  id,                # 稳定唯一
  round,             # 决策环阶段
  actor,             # expert / main / subagent / human
  claim?, decision?, # 结论或决策
  evidence_refs: [], # 必须可回溯
  adjudicator?,      # 最终裁决人
  resolution?,       # adopt_a / adopt_b / merge / reject / defer
  unresolved: []     # 保留未决冲突
}

gate_check = {
  stage, item, pass: bool,
  evidence: "证明方式",          # static/runtime/data/rendering/tooling
  checks_observed_red: []        # 见过失败的检查
}

ledger = {
  project: "...",
  claims: [...], decisions: [...], conflicts: [...],
  next_actions: [...], updated_at: "..."
}
```

## 边界

- 本 skill 是流程层，不替代领域知识；具体公式、实验、代码结果必须回原文/实跑核对。
- 简单一次性问答不必走完整九段；本流程用于“会长期存在 / 要多人决策 / 要可验收”的任务。
- 涉及 DSH/插件热更、重启、子代理调度：先读 `dsh-optimization-consensus`。
- 专家观点是“风格/方法论参考”，不是本人原话，也不是官方评审意见。

## 简单用户话术

> 我给你的是三样东西：**方向**（先把目标和交付物定清楚）、**方式**（专家独立表态 → 冲突 → 裁决 → 计划 → 执行 → 验收 → 回写）、**边界**（没有证据的结论不成立，分歧不硬合，你随时可以说“我感觉不对劲”）。
>
> 如果哪条和你的直觉冲突，请直接说“我感觉不对劲”，我会停下来重新核验，而不是硬套模板。

## 来源

- LightRead AI 官方站与博客（引用可点回原文、并行智能体、科研记忆、阶段验收）
- `vault/skills/teacher/expert-team/SKILL.md`（标准化专家团协议）
- `vault/skills/research/research-module/SKILL.md`（科研多 agent 流程）
- `vault/skills/core-iteration/dev-workflow-consensus/SKILL.md`（开发强流程与门禁）
- `vault/skills/core-iteration/skill-verification-consensus/SKILL.md`（证据化验证）
- 完整来源表见 `SOURCES.md`
