# 专家决策共识 · 完整版

> 本文是 `SKILL.md` 的展开版，供实现、审计、回测与跨会话复用时参考。
> 核心立场：**AI 在专家决策中的短板不是“不够聪明”，而是“过程不可检查、结论不可追溯、交付不可验收”。**
> 本共识把 LightRead 一类科研工作台的“工作流化 + 证据化 + 门禁化 + 记忆化”原则抽象成通用专家决策环，并复用到科研、教学、开发、写作、蒸馏。

## 1. 为什么需要“规范化专家决策”

传统专家团讨论（包括很多 AI 工作流）的价值在“多视角观点”，但容易停在：

- 只有意见，没有证据台账；
- 有分歧，却被静默平均；
- 有结论，但不知道下一步谁做、做到什么算完成；
- 有“我觉得可以”，但没有可证伪的验证；
- 换一个会话，上一轮决策就丢失了。

LightRead 的公开设计给出了相反的方向：

1. **引用必须能点回原文**：没有可追溯链接的引用不显示；
2. **每一步做完才交给下一手**：阶段验收，不合格重做；
3. **多子代理并行/接力/续跑**：主线程拆解，叶子结果一层层交回；
4. **科研记忆与项目规则**：跨对话保持偏好、状态与约束；
5. **交出来是文件**：不是一段聊天，而是可继续编辑的 Word/PPT/PDF/代码/图。

开源项目 Research Workbench 又把这些原则落成了更具体的 13 阶段状态机：
文献/找 Gap → 方案审查 → 新颖性 → 数学验证 → 故事动机 → 实验矩阵/实现/自检 →
实验运行/调参 → 数据图 → 写作 → 机制图 → 排版/引用核验 → 三轮审查 → 去 AI 味，
并配有研究台账、知识图谱、阶段门禁、真实实验复现、写作保真协议。

本共识把它们抽象成“九段决策环”，作为所有领域的通用决策协议。

## 2. 九段决策环（EDGE Loop）

### 0 Brief——定目标

- 必须回答：为谁？什么处境？交付什么可观测结果？不做什么？
- 产出：`brief.md` 或一段结构化目标。
- Gate：若目标含糊，先问一个最高信息增益问题，不要边做边猜。

### 1 Evidence——证据收集

- 外部事实先检索（`search-source` / `web-research-consensus`），再用模型推理。
- 内部材料先读原文/源码/数据，再下结论。
- 每条关键主张记录：claim、source_refs、evidence_class、确定性。
- Gate：无来源的主张不得进入 Panel；检索无果必须写“当前公开检索未发现”。

### 2 Panel——专家独立表态

- 使用标准化专家团协议：定域 → 加载 ready 专家 → 独立表态 → 冲突 → 裁决 → 署名。
- 专家必须来自 `EXPERT_LIBRARY.json`，有真实公开人物、领域、sourceRefs。
- 无 ready 专家：返回 `expert_gap`，默认直接用大模型继续，并把缺口记进项目台账；不弹 DSH 对话框询问。

### 3 Conflict——冲突点表

- 字段：`conflict_id`、`topic`、`claim_a`、`claim_b`、`aligned_expert_ids`、`sources`、`resolution`。
- 不平均分歧：两个立场都保留，哪怕看起来可以折中。
- Gate：无冲突也要显式声明“本轮无冲突”，不伪造。

### 4 Adjudicate——裁决

- 裁决人：用户 / 主持人 / 明确授权的角色。
- 取值：`adopt_a` / `adopt_b` / `merge` / `reject` / `defer`。
- Gate：每个冲突必须有裁决记录；`defer` 不是失败，是明确保留开放分支。

### 5 Plan——行动计划

- 把裁决变成可执行计划：阶段、子任务、接口/契约、验收条件、执行形态。
- 开发类任务套用 `dev-workflow-consensus` 的 Frame/Spec/Gate；科研类套用 research-module 的子技能。
- Gate：计划通过对抗式检查（BLOCKER/GAP/NOTE）后才进入执行。

### 6 Execute——执行编排

- 主线程负责规划和集成；子代理负责可并行、可机械化的子任务。
- 子代理纪律：
  - 有界并发；
  - 模型分层（机械/编辑/判断）；
  - 明确“拥有的文件、不能碰的文件、必须跑的命令、不变量”；
  - 重叠文件串行；
  - 不碰 git 状态；
  - 任务中断必须可续跑。
- Gate：每个子代理产出通过其阶段 gate 才交给下一手；“列了步骤”不等于“做完了”。

### 7 Verify——证据化验证

- 使用 `skill-verification-consensus`：
  - 静态：源码/配置/commit 原文；
  - 运行时：真实命令输出 + 退出码；
  - 数据：可复算的测量与脚本；
  - 渲染：实际 PDF/PPT/截图 + 生成命令；
  - 工具链：版本/API/包元数据。
- 每个机械可判断点必须“见过红”：故意破坏 → 失败 → 恢复 → 通过。
- 专家/审稿类验证使用三轮审查：
  1. Originality / Methodology / Evidence / Coherence / Writing 五维找 P1/P2；
  2. re-review 生成 traceability matrix，逐条核对是否真实处理；
  3. P1=0 且 P2 低于阈值才放行。
- Gate：无未决 P1/BLOCKER；有 conflicts 未裁决不得宣称通过。

### 8 Log & Distill——回写与蒸馏

- 写决策日志与项目台账：结论挂证据、实验留状态、冲突保留未决分支。
- 跨会话记忆：项目状态、用户偏好、错误纠正，回写到可读文件。
- 重复工作流蒸馏：用 `distillation-consensus` 生成 SKILL.md / 规则 / 提示词模板；
  新技能必须满足“触发 + 动作 + 反例 + 来源 + 简单话术”。
- Gate：本次决策可复现、可续跑；可复用流程已入候选或正式 skill。

## 3. 领域适配

| 场景 | 专家/来源 | 领域流程 | 本环重点 |
|---|---|---|---|
| 科研 | `research-module` 导师团 | 读论文 → 理脉络 → 实验 → 写作 → 投稿/组会 | 证据台账、引用可点回原文、新颖性审计、三轮审查 |
| 教学 | `teacher-module` / `teacher-consensus` | 拆题 → 引导 → 讨论 → 复盘 | 独立表态、冲突表、信息论式追问、一次一问 |
| 开发 | `dev-workflow-consensus` | Frame → Spec → Gate → Build → Verify → Ship | 规格门禁、接口测试、对抗审查、redteam |
| 写作/PPT | `writing-module` / `ai-ppt` | 受众 → 结构 → 稿件 → 成品 | 交付文件、风格保真、可编辑产物 |
| 蒸馏 | `distillation-consensus` | 定目标 → 选语料 → 提原语 → 校验 | 来源可追溯、保留分歧、样例干跑、人工复核 |

## 4. 硬性纪律与红线

1. 人类最终裁决：用户“我感觉不对劲”时无条件暂停自动流程。
2. 没有证据不成立：编造引用/数据/专家原话是红线。
3. 冲突不平均：分歧保留分支，不揉成 50% 共识。
4. 不静默降级：无 ready 专家必须走 expert_gap 分支。
5. 一次一个高信息增益问题：不一次抛一串问题。
6. 交付是文件/产物：不是聊天记录。
7. 保真红线：润色/去 AI 味不改数字、引用、术语、claim 强度。
8. 有界子代理：数量、模型、文件冲突、git 状态都要约束。

## 5. 机器可读契约

```text
# 单条决策日志
decision_log_entry = {
  id: "dec_001",
  round: "adjudicate",
  actor: { type: "expert|main|subagent|human", id, name },
  decision: "...",
  evidence_refs: ["url/dOI/path#line"],
  adjudicator: "user|host",
  resolution: "adopt_a|adopt_b|merge|reject|defer",
  unresolved: ["conflict_003"]
}

# 门禁检查
gate_check = {
  stage: "verify",
  item: "引用可点回原文",
  pass: true,
  evidence: "DOI/OpenAlex 解析通过；5 条引用全部可回溯",
  checks_observed_red: ["invalid_citation_should_fail"]
}

# 项目台账
ledger = {
  project: "example-project",
  claims: [{ id, text, evidence_refs, status }],
  decisions: [...],
  conflicts: [...],
  next_actions: [...],
  updated_at: "..."
}
```

## 6. 干跑验证（3 个样例）

### 样例 A：科研论文评审

- Brief：为某 VLPC 方向论文找“最可能被审稿人质疑的 3 点”。
- Evidence：读原文 + OpenAlex/Crossref 核验引用。
- Panel：Ting Yang / Ping Wang / S. Ma 独立指出问题。
- Conflict：对“是否缺少 baseline”出现分歧。
- Adjudicate：用户选择保留“补 baseline”和“先说明 why 不做”两条分支。
- Plan：修改计划含引用核验、新增对照实验表。
- Execute：子代理并行抽表格、查 baseline、整理引用。
- Verify：P1=0；每条新增引用可点回原文。
- Log：回写论文评审台账。

### 样例 B：教学拆题

- Brief：学生卡在“为什么 DP 要倒推”。
- Evidence：先看学生代码与题目约束，不直接给答案。
- Panel：两位竞赛导师独立给出“先暴力/先重述”两种风格。
- Conflict：两种引导顺序冲突。
- Adjudicate：用户选择“先让学生重述关键不变量”。
- Plan：设计 3 个追问，按熵减顺序。
- Execute：逐问推进，只在高信息增益处继续。
- Verify：学生能在不提示下写出状态转移。
- Log：把有效追问序列沉淀为教学 skill 候选。

### 样例 C：开发模块重构

- Brief：为某模块增加缓存，不改公开接口。
- Evidence：读现状代码 + 测试。
- Panel：架构/性能/安全专家独立表态。
- Conflict：缓存放在 API 层 vs 数据层。
- Adjudicate：用户选择 API 层，但保留数据层作为后续分支。
- Plan：接口不变，先写失败测试。
- Execute：子代理实现，重叠文件串行。
- Verify：测试先红后绿；破坏缓存键看是否红；redteam 通过。
- Log：回写模块地图与决策日志。

## 7. 反模式

| 反模式 | 处理 |
|---|---|
| 只给意见不挂证据 | 降权或退回 Evidence 阶段 |
| 有分歧却“综合一下” | 保留冲突表，交用户裁决 |
| 无 ready 专家直接大模型扮演 | 走 expert_gap，不静默降级 |
| 说“已完成”但没跑验证 | 只算“已运行，未验证” |
| 把“列步骤”当“做完” | 用阶段 gate 拦截 |
| 润色改掉数字/引用/claim 强度 | 保全审计拦截 |
| 一次抛 5 个问题 | 只问最高信息增益问题 |
| 只输出聊天不给文件 | 定义交付物契约，落盘 |

## 8. 与现有技能的分工

- `teacher-module` / `expert-team`：提供“人名专家 + 回合式讨论”；
- `research-module`：科研场景适配；
- `dev-workflow-consensus`：开发场景适配；
- `skill-verification-consensus`：验证与红队；
- `distillation-consensus`：把重复流程蒸馏为 Skill；
- 本 skill：把上述能力统一成一条“可检查、可追溯、可验收”的决策协议。
