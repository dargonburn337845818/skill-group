---
name: research-module
description: 科研多 agent 导师团队与论文/组会流程骨架——读论文、理脉络、写论文、实验设计、投稿、组会、PPT、模拟导师审查与职业路径，全部按“回合式讨论 + 人名专家”协议执行。
whenToUse: 用户进入科研/论文/组会/导师审查/研究 PPT/职业路径等场景时；需要多 agent 导师团队以具体人名给出意见时。
---
# 科研模块 · 多 agent 导师团队与论文/组会流程

> 这是科研模块的入口。它复用教师模块的“回合式讨论 + 人名专家”协议，把
> 读论文、理脉络、写论文、实验设计、投稿、组会、PPT、导师审查、职业路径串成一套可执行流程。
> 每条指导必须标注具体专家/导师姓名，不能让用户觉得“来自一个匿名大模型”。
> 本模块流程统一挂到 `expert-decision-consensus` 九段决策环；需要持久台账/检索/门禁/文件交付时，优先走 `workbench-module` + `wb` CLI。

## 何时使用

- 用户要读一篇论文、做文献脉络、写论文章节。
- 用户要设计实验、选统计检验、估样本量，或处理选刊/投稿/审稿回复。
- 用户要准备组会、做研究 PPT、模拟导师审查/答辩。
- 用户要选择科研方向、规划读研/求职路径。
- 用户明确提到“科研 / 论文 / 组会 / 导师 / 实验 / 投稿 / 物理 / VLPC”等场景。

## 设计与教师模块共用的讨论协议

科研模块不另造一套协议，直接复用 `vault/skills/teacher/expert-team/SKILL.md` 的标准化专家团协议（其规范来源为 `FORMAL_SPEC.md` 第 4 节）：

```text
1. 选定专家团（科研导师团）
2. 每轮：每位专家独立表态/提问
3. 汇总：冲突点表（claim_a / claim_b / source）
4. 裁决：主持人（或用户）选择 采纳 / 保留分支 / 驳回，并记录
5. 输出：每条结论/问题/建议都带 expert_id 与 expert_name
```

### 硬性纪律

1. **人名专家不是抽象角色**：先说“这是谁、什么领域、依据哪些公开文献”。
2. **不编造原话**：只做“风格/方法论参考”，推理时说明是风格推断，保留 sourceRefs。
3. **不静默降级**：识别到科研领域但没有 ready 人名专家时，默认直接用大模型继续，并把这个“专家缺口”记进项目台账；不要弹 DSH 对话框询问。
4. **每条意见署名**：`【Ting Yang · 系统架构】` 这类标注是必选项。
5. **一次只问一个高信息增益问题**：导师审查时不要一次抛一串问题。

## 科研模块子技能地图

| 子技能 | 文件 | 触发一句话 |
|---|---|---|
| 论文阅读 | `subskills/paper-reading/SKILL.md` | 给我一篇论文，帮我读懂并提问题 |
| 文献脉络 | `subskills/paper-outline/SKILL.md` | 这个方向还有哪些路、领域地图长什么样 |
| 论文写作 | `subskills/paper-writing/SKILL.md` | 帮我写/改摘要、引言、章节 |
| 实验设计 | `subskills/experiment-design/SKILL.md` | 设计实验、选统计检验、估样本量、查可复现性 |
| 科研投稿 | `subskills/submission/SKILL.md` | 选刊/会议、写 cover letter、回审稿、处理拒稿 |
| 组会 | `subskills/group-meeting/SKILL.md` | 准备组会、模拟组会问答 |
| 研究 PPT | `subskills/research-ppt/SKILL.md` | 做组会/答辩/投稿用幻灯片 |
| 导师审查 | `subskills/mentor-review/SKILL.md` | 提交前让导师团队模拟审查 |
| 职业路径 | `subskills/career-path/SKILL.md` | 科研方向选择、读研/求职规划 |

调用方式：用户进入任一子场景时，先读取对应子技能文件，再按其中的触发/动作/边界执行。
子技能当前是主包的一部分，不单独注册为 vault 顶层 skill；若要单独启用，再复制到
`vault/skills/research/<id>/SKILL.md` 并补 manifest。

## 导师团队组成与接口（本轮先留接口）

### 数据来源

- 统一人名专家库：`vault/meta/EXPERT_LIBRARY.json`
- 领域字典：`vault/meta/domain-profiles.json`
- 用户自定义导师（预留接口）：`vault/meta/USER_MENTORS.json` 尚未创建；当前以 `EXPERT_LIBRARY.json` 为准。

### 科研导师团默认成员（示例）

| expert_id | 姓名 | 领域 | 状态 | 来源 |
|---|---|---|---|---|
| `ting-yang` | Ting Yang | 可见光定位通信系统架构 | ready | NOMA-VLPC 论文等 |
| `ping-wang` | Ping Wang | 定位算法/信号处理 | ready | NOMA-VLPC 论文等 |
| `s-ma` | S. Ma | VLPC 波形设计 | ready | IEEE TCOM 2023 等 |
| `y-chen` | Y. Chen | 实验/指纹定位 | ready | IEEE Access 2020 等 |
| `o-k-h-shanker` | O. K. H. Shanker | NOMA-VLC | ready | IEEE Commun. Lett. 2024 等 |
| `a-k-sah` | A. K. Sah | NOMA-VLCP | ready | Photonics 2024 等 |
| `richard-feynman` | Richard Feynman | 物理直觉与教学 | ready | 公开讲座/教材（EXPERT_LIBRARY 已蒸馏） |

具体字段以 `EXPERT_LIBRARY.json` 为准；`richard-feynman` 已蒸馏为 ready。

### 预留工具接口（本轮不实现）

```text
mentor_add(name, domain, sourceRefs, ...)   # 添加科研导师
mentor_select(...)                          # 选择本次审查/讨论的导师
mentor_list(...)                            # 列出可用导师
mentor_remove(id)                           # 移除/停用导师
```

在工具未实现的阶段，用户可以说“这次用 Ting Yang 和 Ping Wang 做导师团队”，
或“添加导师 X，来源是……”，agent 按 EXPERT_LIBRARY 契约读取并记录；USER_MENTORS 预留接口在创建前不可用。

## 标准流程：模拟导师团队审查

任何审查/讨论都按以下四段走，见 `examples/committee_review.md` 的完整示例：

```text
1. 学生汇报
   学生（或用户）给出论文/工作/进展的口头摘要。
2. 各导师提问
   每轮一位导师，只问一个当前最重要的可回答问题，标注导师名。
3. 问题点 / 创新点汇总
   - 问题表：问题 / 提问导师 / 论文或实验证据 / 严重程度
   - 创新表：贡献 / 支撑证据 / 哪位导师认为值得深挖
4. 建议下一步
   按 1–3 条短期行动给出，每条标注导师姓名与原因。
```

## 侧边栏展示契约（讨论流 + 导师姓名）

科研模式的过程监视器应显示“科研讨论流”，每条事件至少包含：

```json
{
  "id": "evt_001",
  "session_id": "...",
  "ts": "2026-09-05T10:00:00Z",
  "mode": "research",
  "kind": "expert_speak | decision | stage",
  "actor": { "type": "expert", "id": "ting-yang", "name": "Ting Yang" },
  "action": "提问：为什么 DC 定位需要双相编码？",
  "reason": "检查学生对定位链路的理解",
  "detail": { "claim": "...", "source": "..." },
  "status": "done"
}
```

侧边栏顶部显示当前模式（科研）与当前导师团队姓名列表；中间按时间线渲染
“哪位导师说了什么”；底部显示冲突/裁决状态。本契约只做只读展示。

## 边界

- 本模块是流程骨架，不是论文事实库；具体公式/实验数据必须回原文核对。
- 专家看法是“风格/方法论参考”，不是本人原话，也不是对论文的官方评审意见。
- 不生成或篡改实验数据；没有数据支撑的“创新点”必须标为推测。
- 若识别到科研领域但无 ready 导师团，按专家缺口分支处理：默认直接用大模型继续，并把缺口记进项目台账；不弹 DSH 对话框询问。
- 用户说“我感觉不对劲”时，停止套模板，重新核对来源与推理链。

## 启动动作

1. 先判断用户要进入哪个子流程（读论文 / 理脉络 / 写作 / 实验设计 / 投稿 / 组会 / PPT / 审查 / 职业路径）；不确定时在普通回复里列出候选，让用户文字选择，不弹窗。
2. 用 `vault/meta/domain-profiles.json` 做领域识别；若为科研/物理类，加载对应导师团。
3. 读取对应 `subskills/<id>/SKILL.md`。
4. 按子技能执行，并始终在输出中标注导师姓名与 sourceRefs。

## 2026 深度补强（Round 36）

> 主题：**横切科研全流程的多 agent 协作与门禁**——把“读论文 / 理脉络 / 实验 / 写作 / 投稿 / 组会 / PPT / 审查”从并列子技能串成一条可审计的流水线。
> 本轮补的是“骨架层”的执行规则，不重复子技能里的阅读、统计、写作、投稿细节；每条含触发 / 动作 / 反例 / 来源，来源清单见 `SOURCES.md` `## Round 36 新增来源`。

### R36-1 项目级“研究台账”：所有子流程回流同一个事实源

- 触发：用户开始一个新研究 / 论文 / 组会周期，或已有工作但结论散落在多个文件与对话里。
- 动作：
  1. 建立 `research_canvas.md`（或 JSON），固定字段：可证伪研究问题、假设与反证条件、证据表（claim / source_refs / 证据等级 / 状态）、实验记录（设计 / 样本 / 指标 / 状态）、投稿与汇报目标、下一步、冲突与待裁决。
  2. 任何子技能输出前先回写这份台账；只给出结论但不落台账的，视为临时讨论，不得直接进入下一步。
  3. 每次回写带日期与负责人；明确区分 `已证 / 待证 / 推测`，不把“没想过”写成“不存在”。
- 反例：读完 10 篇论文、做了 3 轮仿真，结论只在聊天记录里；下次又让用户从头复述。
- 示例：读论文后在证据表加一行“X 方法在静态 NLOS 下 RMSE 1.2 m（原始实验，L1）；动态目标未验证（待证）”，后续写作、组会、审查都引用同一条。
- 来源：Ten simple rules for implementing electronic lab notebooks (ELNs)；本地 `experiment-design` 可复现清单作回写校验。

### R36-2 多 agent 编排：最小四角色，执笔人不得同时当验收人

- 触发：要跑“多 agent 协作”的科研流程（并行读文献、生成方案、模拟审查、写稿）。
- 动作：
  1. 每个阶段定义四角色：`证据官 Reader`（只提取 claim + source + 边界）、`红队 Skeptic`（专找替代解释、反例、可复现漏洞）、`执笔 Writer`（组织成文本/PPT/回复）、`守门人 Gatekeeper`（对照研究台账验收是否达到该阶段退出标准）。
  2. 已有导师团可兼角色，但同一任务中 **执笔人与验收人必须分离**；至少保留一个独立 skeptical / gatekeeper 通道。
  3. 每个 agent 只拿到“本子任务 + 交接物”，不要把整个会话历史同时塞给所有 agent，避免上下文污染和互相复读。
- 反例：同一个 agent 既写“创新点”又下结论“这个创新点成立”；多 agent 退化成多人轮流说“我也觉得不错”。
- 来源：MetaGPT（角色分工 + SOP + 结构化产物）；The AI Scientist（idea → experiment → paper → reviewer 流水线）；Towards agentic science（人类监督与分步授权）。

### R36-3 跨 agent / 跨步骤交接：只认“证据卡”，不认“口头感觉”

- 触发：Reader 交给 Writer、实验交写作、导师审查后交下一步、子技能之间互转。
- 动作：交接物必须是一张结构化证据卡：
  ```text
  claim: ...
  source_refs: [...]
  evidence_class: 原始实验 / 理论推导 / 综述转述 / 我的推断
  boundary: 在什么条件下成立
  next_action: 下一步具体动作
  pending: [待证清单]
  ```
  下游收到后先做三件事：核对 source 是否支持 claim、检查 claim 是否越出证据、把待证显式列出；三件事没做完不得产出新文本。
- 反例：Reader 说“这方法不错”，Writer 写成“该方法显著优于 SOTA”，中间丢了“哪篇文献、什么条件、什么指标”。
- 来源：本地 `paper-reading` R33-4/R33-8（声明-证据-边界与证据分级）；The AI Scientist（端到端流水线中的结构化产物）；MetaGPT（结构化接口降低级联错误）。

### R36-4 冲突升级阶梯：同轮分歧 → 冲突表 → 可区分实验 → 用户裁决

- 触发：两位导师 / 两个 agent 对同一问题给出相反结论。
- 动作：
  1. 第一层：完整保留 `claim_a（谁 + 依据）/ claim_b（谁 + 依据）/ 分歧点`，不合并、不“平均成一句话”。
  2. 第二层：判断能否用一个低成本实验 / 一组现有数据把两方分开；能，就写成下一行动项（谁做、多久、什么指标）。
  3. 第三层：无法靠实验分开时，把选择权交给用户或明确负责人，给出“采纳 A / 保留 B / 先做小验证”三选一，并记录决策人。
- 反例：把“A 觉得可行，B 觉得风险高”揉成“需要权衡”；或主持人自己偷偷选边后继续推进。
- 来源：本地 `expert-decision-consensus`（冲突保留与裁决）；PLOS 多作者协作文章（显式沟通、争议处理）。

### R36-5 阶段门禁：没有退出标准，就不准进入下一阶段

- 触发：从“读文献”跳到“写全文”、从“实验”跳到“投稿”，或用户说“先写着，边写边补”。
- 动作：每个阶段进入前先写三行：`exit criteria`（至少达到什么）、`blockers`（什么算未完成）、`gatekeeper`（谁签字放行）。给四个默认门禁：
  - 阅读 → 脉络：≥N 篇核心论文已有“声明-证据-边界”卡，且能一句话回答“为什么现在做、和谁比、什么结果算成功”。
  - 脉络 → 实验：研究问题可证伪，候选方向有最小实验与失败判据。
  - 实验 → 写作：预注册 / 假设、SESOI、指标、干净环境复跑脚本站齐；不是“结果好看”。
  - 写作 → 投稿：图表自包含、Results/Discussion 不越界、AI / 伦理 / 作者披露齐全、审稿人冷读已过。
- 反例：研究问题还没定就先写 Introduction；实验还没跑完就投会议；大家说“应该差不多”但没人定义“差不多”。
- 来源：Towards agentic science（分阶段授权与人类监督）；Ten Simple Rules for Getting Grants（评审人视角的成功判据）；本地 `paper-writing` / `experiment-design` 门禁。

### R36-6 合作 / 共著先签“科研条约”：角色、数据、署名、退出机制

- 触发：多人合作、跨实验室、师生共同署名，或 AI 参与写作时。
- 动作：
  1. 开始前一页 `collaboration prenup`：目标；每人预期角色与贡献（可参考 CRediT）；数据 / 代码 / 材料归属与访问；作者顺序与变更规则；沟通与会议节奏；退出或中断时成果归属；争议解决人。
  2. 随实际贡献更新，不在完成后“补签”；关键字段写死：谁负责哪个实验、谁保有 raw data、谁可访问代码。
  3. 若使用 AI / LLM：按目标期刊与机构政策披露；工具不得列为作者；人类作者对全部内容负责。
- 反例：合作半年后争一作；说好共享数据但没写进协议；把 ChatGPT 列为共同作者。
- 来源：Ten simple rules for collaboratively writing a multi-authored paper；Nature Portfolio AI editorial policy；ICMJE Recommendations（2026 更新）。

### R36-7 投稿 / 汇报前做“审稿人冷读”：只看标题摘要图，先挑三个问题

- 触发：准备投稿、pre-submission、或重要导师审查前。
- 动作：
  1. 假装自己是没读过正文的领域 reviewer：只看标题、摘要、图表、结论，写下 3 个第一眼问题。
  2. 用 peer review checklist 快速过：贡献是否明确、方法是否可复现、结果是否支撑结论、图表是否误导、文献是否覆盖、伦理 / 利益冲突是否披露。
  3. 把问题标 major / minor，并注明“在哪个位置改”（章节 / 图 / 表 / 补充材料），而不是只写“感觉不够好”。
- 反例：只让熟人看，被夸“挺好的”就投；或只查错别字和格式，没检查“结论是否被证据支持”。
- 来源：Ten simple rules for writing a peer review；PLOS Peer Review Checklist。

### R36-8 需要资源的项目先做“15 分钟 grant 预检”

- 触发：需要经费、设备、学生 / 算力，或用户问“要不要先写 proposal”。
- 动作：在投入大量实验前，写一页并请 gatekeeper 审：
  - 解决什么、给谁解决；
  - 为什么现在、为什么只有我们能做；
  - 预期 1–3 个可衡量产出；
  - 预算 / 时间线 / 风险；
  - 成功与失败判据（拿到资源后怎么验收）。
- 反例：先花半年做实验再补预算，评审人第一段就看不到“到底解决什么问题”；或不写失败判据，项目无法验收。
- 来源：Ten Simple Rules for Getting Grants；本地 `career-path`（资源与预算的现实约束）。
