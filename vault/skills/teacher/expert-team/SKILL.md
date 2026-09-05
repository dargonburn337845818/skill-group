---
name: expert-team
description: 任意模块通用的人名专家团标准化流程——领域识别、加载 ready 专家、回合式表态、冲突裁决、署名结论；dev/writing/teacher/research/distill 均可复用。
whenToUse: 开发、文稿、教师、科研、蒸馏等模块需要多位真实公开人物风格参考来评审方案、拆解问题、生成署名意见、保留分歧时。
---

# 专家团标准化流程（Expert Team Protocol）

> 目标：让“专家团”不再是 teacher 模块私有能力，而是 dev / writing / teacher / research / distill 共用的标准流程。
> 数据源：`vault/meta/EXPERT_LIBRARY.json`（人名专家库）+ `vault/meta/domain-profiles.json`（领域字典）。
> 若要把专家团讨论升级为“可检查、可追溯、可验收”的完整决策，统一再加载 `expert-decision-consensus`；需要长期台账/文件交付时走 `workbench-module` + `wb`。
## 触发条件

- 任何模块（dev/writing/teacher/research/distill）需要“多位真实公开人物风格参考”时。
- 需要对方案/产物做多视角评审、拆解、纠偏、分歧裁决时。
- 需要把“某专家怎么看”写成带署名的结论并保留来源时。

> 运行时：任意模块统一使用 `expert_team_start / expert_team_round / expert_team_status / expert_team_select / expert_team_finish` 工具；同时兼容 `teacher_discussion_*` 别名与 `/skill-vault/api/expert-team/*`、`/skill-vault/api/teacher/*` HTTP 接口。

## 一、标准化协议（六步）

任何模块调用专家团，都按同一套流程，不另起炉灶：

```text
1. 定域：识别本次任务属于哪个领域（algorithm / frontend / backend / security /
   performance / math / physics / writing / research / ai-llm-agent / devops /
   data-science / product-ux / dsh-ops）。
2. 加载：从 domain-profiles 取 expert_ids → EXPERT_LIBRARY 过滤 status=ready 且
   persona_type=public-figure-style-reference 且 sourceRefs 非空。
3. 独立表态：每轮每位专家只给“按公开风格的倾向”，不互相看答案。
4. 冲突点表：相同问题不同立场写成 claim_a / claim_b / 来源 / 对齐专家，不强行合并。
5. 裁决：主持人或用户 adopt_a / adopt_b / merge / reject / defer，保留未裁决分支。
6. 署名结论：每条结论带 expert_id + expert_name + sourceRefs，并注明“风格推断，非本人原话”。
```

无 ready 专家时：明确返回 `expert_gap`，询问“蒸馏专家团 / 放弃专家团直接用大模型”，**不得静默降级**。

## 二、各模块默认专家团

| 模块 | 默认领域/专家团 | 调用示例 |
|---|---|---|
| dev | 按任务域选：frontend / backend / security / performance / devops / ai-llm-agent / data-science / product-ux / dsh-ops | `teacher_discussion_start(text="后端架构评审", expert_ids=["martin-fowler"])` |
| writing | writing（William Zinsser）+ 必要时 product-ux / research | `teacher_discussion_start(text="写作/文案", expert_ids=["william-zinsser"])` |
| teacher | algorithm / math / physics 等教学领域 | `teacher_discussion_start(text="算法竞赛教学")` |
| research | research（Ting Yang / Ping Wang / S. Ma / Y. Chen / O. K. H. Shanker / A. K. Sah / Richard Feynman） | `teacher_discussion_start(text="VLPC 论文评审", domain_id="research")` |
| learning | learning（Dan Koe / Richard Feynman / Andrej Karpathy） | `teacher_discussion_start(text="AI 十倍速学习评审", domain_id="learning")` |
| distill | 按被蒸馏材料所属领域选专家团；元流程本身可请 dsh-ops / ai-llm-agent 专家审查 | `teacher_discussion_start(text="蒸馏算法竞赛语料", domain_id="algorithm")` |

## 三、输出纪律

- 必须保留 `expert_id` / `expert_name`。
- 必须写明 `persona_type = public-figure-style-reference`。
- 不得写“某某专家说……”；应写“按某专家风格，倾向……”。
- 分歧未裁决时不得静默合并。
- 专家观点只作为风格/方法论参考，不是对方案的官方评审。

## 四、边界

- 本协议不替代各模块自身业务判断；专家团只提供多视角与可追溯署名。
- 不创建“抽象角色”专家；只允许 EXPERT_LIBRARY 中真实公开人物。
- 如果领域已 ready 但用户点名了 `pending_distill` 专家，仍需提示并选择“先蒸馏 / 换人”。
- 涉及 DSH/插件热更、重启、子代理调度时先读 `dsh-optimization-consensus`，不在此协议内处理。

## 2026 深度补强（Round 36）

> 本轮把专家团协议从“流程骨架”补成“可运行、可审计、可复现”的操作层：盲写独立表态、冲突台账 schema、证据分级、署名可回放、少数意见保留、预注册裁决规则、红队/失败预演、二次独立复跑。全部来源见 `SOURCES.md` →「Round 36 新增来源」；用法与前文一致：逐项执行，命中就给“动作 → 反例 → 可执行检查”。

### R36-1 独立表态必须“盲写 + 锁存”，不允许先看别人再写
- **动作**：每轮开始前，先让每位专家在不看他人观点的情况下写“倾向 + 依据 + 不确定点”，并打上轮次/时间/专家 id；全部提交后才进入公开讨论。任何“同意上一位”的补写必须标记为 `post-exposure`，不计入独立的原始表态。
- **反例**：A 先发言，B 说“我同意 A，并补充……”；或主持人先总结“大多数人倾向 X”，再让专家表态——这已经污染了独立性。
- **可执行检查**：同一轮原始 `speaks` 中，后写者不能引用先写者的内容；如引用，必须单独写成“受暴露后的补充意见”。
- **来源**：RAND Delphi 指南；PMC NGT 研究（静默独立生成后再讨论/排序）。

### R36-2 冲突点表最小 schema：未裁决就是 `deferred`，不能省略
- **动作**：每条冲突至少含：`conflict_id`、`topic`、`claim_a / claim_b`（各带来源）、`aligned_expert_ids`、`status`（`adopt_a / adopt_b / merge / reject / defer`）。若当轮未裁决，显式写 `deferred` + `defer_reason` + `next_trigger`（如“等补充证据后复裁”）。
- **反例**：台账里只有“存在分歧”，没有两个 claim 的原文和来源；或合并时没有写明采纳了哪部分、放弃了哪部分。
- **可执行检查**：每个 conflict 必须有一个终态或明确的 deferred 触发器；不得有空 `status`。
- **来源**：ADR（context/decision/status 可追踪）；IETF Reviewed-By（可签名复核的评审链）。

### R36-3 证据台账按“来源级别 + 单源风险”标记
- **动作**：每条支持结论的证据写：`evidence_class`（`primary`=一手/原文/官方，`secondary`=综述/评论，`style`=风格推断）、`source_ref`（URL 或本地路径）、`access_date`、`owner`。只有 1 个来源时标 `single-source`，并优先找第 2 个独立来源；找不到则在结论里降级为“待证/有条件支持”。
- **反例**：把同一篇转载或同一作者的两篇文章算作“两个来源”；或只写“有资料表明”，没有日期、没有 URL。
- **可执行检查**：结论中每个可验证断言都能点回 `source_ref`；`style` 类必须同时注明“风格推断，非本人原话”。
- **来源**：ISPOR 结构化专家启发（单专家需校准/多独立）；NCBI EtD 框架（证据到决策的显式台账）。

### R36-4 署名结论要“可回放”：问题、轮次、输入、裁决、输出缺一不可
- **动作**：每条结论结构化为：`concl_id`、`round`、`question`、`experts`、`considered_claims`（含冲突 id）、`adjudication`、`source_refs`、`style_disclaimer`。不能只留一段“专家认为……”的聊天摘要。
- **反例**：用户一周后问“这个结论是怎么来的”，只能看到一句“Martin Fowler 风格建议采用事件驱动”，看不到原始问题、轮次、冲突和裁决。
- **可执行检查**：每条结论都应有稳定 ID，能回溯到对应 round 的 `speaks / conflicts / adjudications`。
- **来源**：IETF Reviewed-By（签名评审历史）；Elsevier Registered Reports（先写问题与判据再给结果）。

### R36-5 裁决后保留少数意见：合并必须写出“采纳了什么/放弃了什么”
- **动作**：裁决后把未被采纳的立场写成 `minority` / `dissent` 条目：保留原 claim、来源、拥护专家；`merge` 必须列出两侧各采哪些点、放弃哪些点；`reject` 必须写成被拒的具体 claim 与理由。
- **反例**：把两人的观点平均成“既 A 又 B”，却未保留 A/B 各自的条件；或说“专家组已达成共识”，实际上一方的核心条件被丢弃。
- **可执行检查**：最终结论旁须有少数意见区；没有少数意见时显式写“无记录到未采纳意见”，而不是不写。
- **来源**：PMC Consensus methods（共识≠简单多数，过程与方法须先定）；Delphi/NGT 的分歧保留传统。

### R36-6 开轮前先定“共识/裁决判据”，事后不得临时解释
- **动作**：每轮 start 时写下：本问题什么是 `pass`（例如 ≥2 个独立来源 + 至少 2 位独立专家倾向一致）、什么算 `defer`、由谁最终裁决（主持人/用户）；把这条判据作为 `gate_rules` 保存在台账。若轮后未达到判据，显式 `defer`，不能把“多数倾向”改名为“共识”。
- **反例**：事前没有判据；看到有人说“觉得还行”，事后就把“至少两位专家提到”当作共识。
- **可执行检查**：每条 gate 都能回答“预先判据是什么？达成了吗？证据在哪？”。
- **来源**：Elsevier Registered Reports（预注册方法与判据）；ISPOR 结构化专家启发（先定共识规则）。

### R36-7 每轮至少做一次“失败预演/反驳检索”，并把结果入台账
- **动作**：结论定稿前，指定 1 位专家或独立红队做 pre-mortem/反面视角：列出“如果按当前倾向执行，最可能失败/被反驳的原因”，并为每条写证据或“未找到反例（检索范围+日期）”。预演结果以独立 claim/conflict 入账，不得删除。
- **反例**：专家团全程只论证方案优点；用户问“哪里会翻车”，没有人给过失败模式。
- **可执行检查**：每个关键结论都要有一条对应“失败/反例检查”记录；如果没有，说明未执行。
- **来源**：AHRQ Pre-mortem 工具；NIST 红队实践（对抗性独立挑战）；IEEE 1028（评审需覆盖缺陷与风险）。

### R36-8 高利害评审做“二次独立复跑”，差异作为证据
- **动作**：对高利害结论（影响发布/架构/教学主干），在同一台账输入下另开一次独立会话/另一模型/经用户复跑，生成 `replication-<id>`；比较两次 `speaks / conflicts / adjudications` 的差异，差异点作为新的冲突或 `caution` 记录。
- **反例**：只有一次会话，却声称“可复现”；或第二次复跑只挑相同结论复述，未记录分歧。
- **可执行检查**：能否给出一份“两次运行差异表”（一致点、分歧点、新增风险）。
- **来源**：Elsevier Registered Reports（预注册方法与判据）；结构化专家判断交叉验证（Strathprints 古典模型校准）；IETF Reviewed-By（可追踪签名链）。

## 来源

- `vault/meta/EXPERT_LIBRARY.json`
- `vault/meta/domain-profiles.json`
- `vault/skills/teacher/teacher-module/discussion-protocol.md`
- `vault/skills/teacher/teacher-module/expert-selection.md`
- `vault/skills/research/research-module/SKILL.md`（科研复用示例）
