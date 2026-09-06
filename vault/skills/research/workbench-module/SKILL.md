---
name: workbench-module
description: 科研/专家决策工作台编排模块——用 wb CLI 建项目台账，按九段决策环执行检索、精读、专家团、写作、实验、验证与文件交付；效果对齐 LightRead 的“搜读写算一体”云端科研工作台。
whenToUse: 用户要开始一个科研任务、读论文、文献调研、写综述、设计实验、准备组会/PPT、做可追溯专家决策，或希望“像 LightRead 一样在一个工作区里把搜读写算串起来”时。
---

# 科研工作台模块（Workbench Module）

> 一句话：**这不是一个聊天工具，而是一个有项目台账、有证据、有门禁、有交付物的可执行工作台。**
> 本模块调用 `expert-decision-consensus` 的九段决策环，并用 `wb` CLI 把所有状态落到文件；科研、教学、开发都走同一套“软件式”流程。

## 触发条件

- 用户说“开始一个科研任务 / 读这篇论文 / 帮我做文献调研 / 写综述 / 设计实验 / 组会 PPT / 做可追溯决策”。
- 用户希望“最终效果像 LightRead / 像科研软件一样”，而不是只给一段聊天。
- 需要跨会话继续：项目台账、证据、未决冲突、下一步都要能重新打开。

## 启动路径

```text
1. wb init <project-id> --title "..."
2. wb brief <project-id> --goal "..." --non-goal "..."
3. wb status <project-id>
4. 按九段环推进
```

## 九段环在本模块的落地

| 阶段 | 动作 | 命令/输出 |
|---|---|---|
| 0 Brief | 定目标、交付物、非目标 | `wb brief` |
| 1 Evidence | 多源检索 + 引用核验 + 证据 claim | `wb search`、`wb verify`、`wb claim` |
| 2 Panel | 加载科研导师团，独立表态 | `teacher_discussion_start(domain_id="research")` |
| 3 Conflict | 冲突点表 | `wb conflict` |
| 4 Adjudicate | 用户/主持人裁决 | `wb decision --resolution ...` |
| 5 Plan | 子任务 + 验收条件 | `wb todo add`、`wb status` |
| 6 Execute | 子代理并行/接力，产物落 `artifacts/` | subagent / `wb status` |
| 7 Verify | 引用可点回、P1=0、测试过、见过红 | `wb gate --stage "7 verify" --pass-gate --evidence ...` |
| 8 Log & Distill | 记忆回写，重复流程蒸馏成 Skill | `wb memory add`、`wb skill` |

## 内置工作流

- `wb search "attention" --source arxiv,openalex,crossref`：多源检索。
- `wb verify "10.xxxx/..."`：DOI/标题引用核验（Crossref/OpenAlex）。
- `wb claim <project> "..." --source <url/doi>`：把结论挂证据。
- `wb conflict <project> --topic ... --claim-a ... --claim-b ...`：保留分歧。
- `wb decision <project> "..." --resolution adopt_a --adjudicator user`：记录裁决。
- `wb gate <project> --stage "7 verify" --item "引用可点回原文" --pass-gate --evidence "..."`：阶段门禁。
- `wb memory <project> add "..."` / `search "..."`：跨会话记忆。
- `wb status --verbose`：查看当前阶段、门禁、冲突、决策。

## 领域适配

| 域 | 本模块怎么用 |
|---|---|
| 科研 | 论文/综述/实验/投稿/组会；证据台账 + 引用可点回 + 导师团 |
| 教学 | 拆题/讨论；独立表态 + 冲突 + 一次一问 |
| 开发 | 规格/实现/测试；`wb` 台账 + `dev-workflow-consensus` 门禁 |
| 写作 | 从证据表到稿件；交付可编辑 Word/MD/PPT |

## 硬性纪律

1. **引用必须能点回原文**：`wb verify` 核验不通过不得进入正文。
2. **没有证据不成立**：claim 必须带 source；无来源标 `single-doubt`。
3. **人类最终裁决**：冲突由用户/主持人裁决，`defer` 保留开放分支。
4. **交付是文件**：报告、笔记、PPT、代码落在 `artifacts/`，不是只回聊天。
5. **阶段不过 gate 不往下**：`wb gate` 未 PASS 不得宣称完成。
6. **跨会话可续**：所有状态在 `research-workbench/projects/<id>/`，下次直接 `wb status`。
7. **不弹 DSH 对话框**：科研工作台流程中不要调用 `ask_user_question`，也不要制造审批/确认弹窗。需要用户选择时先给默认方案，并用普通文字列出选项，让用户直接回复即可。

## 交互纪律

- 用户在科研工作台里不知道下一步时，先判断当前项目阶段，按“九段环”的下一步提示推进。
- 能自助完成的决定（建项目、定目标、默认来源、默认处理方式）直接照默认走，不要反问。
- 只有真正影响方向的用户偏好才用文字询问；绝不为了“确认”而弹出 DSH 对话框。
- 专家团缺失时默认使用已有领域模型继续，并把“专家缺口”记进项目台账，不阻塞流程。

## 边界

- 本模块不替代论文原文/实验实跑；公式、数据必须回原文核对。
- 没有 ready 专家时走 `expert_gap`，默认直接用大模型继续，并把缺口记进项目台账；不弹窗。
- 简单一次性问答不必开项目；本模块用于“会长跑/要交付/要审计”的任务。
- 涉及 DSH/插件热更、重启、子代理调度：先读 `dsh-optimization-consensus`。

## 简单用户话术

> 我会先给你建一个项目工作区，把目标和非目标写下来；然后搜证据、请专家团表态、记录冲突和裁决，再排计划、派子代理执行、做验证，最后把所有结论和文件落在工作区里。你随时可以说“我感觉不对劲”，我会停下来重新核验。

## 2026 深度补强（Round 35）

> 本轮把“证据、专家、门禁、交付”从口号补成可执行检查点；每条都带动作、反例与来源。

### R1 引用核验分三层：存在 → 未撤稿 → 可点回
- **动作**：`wb verify` 通过只算第 1 层（DOI 元数据存在）。进入正文前再查：① Crossref/OpenAlex 元数据与标题/作者一致；② Retraction Watch/Crossref 的撤稿状态；③ 原文可打开或 DOI 可解析到全文页。
- **示例**：`wb verify "10.1016/j.jclinepi.2021.03.001"` 后，再用 Crossref 的 `is-retracted` / OpenAlex 的 `retracted` 字段排除撤稿，最后把可解析 URL 放进 claim 的 `--source`。
- **反例**：只因为 Crossref 返回了一条 DOI 记录就把论文写进综述；它可能是已被撤稿或撤回的版本。
- **来源**：Crossref Retraction Watch API；OpenAlex。

### R2 高争议/高风险主张用“2 个独立来源”起步，单源必须标风险
- **动作**：对“方法有效、指标显著、某领域存在缺口”这类会影响判断的 claim，至少找 2–3 个相互独立的来源（不同作者/期刊/数据库）；只有 1 个来源时在 claim 上加 `single-doubt` 或 `needs-corroboration`。
- **示例**：断言“长程任务评测是缺口”时，除 OpenAlex 命中外，再用 Semantic Scholar 或逆向引文找一篇独立综述佐证；两条都进 `wb claim`。
- **反例**：同一组作者在不同会议论文里重复同一结论，只算 1 个独立证据，却当成“多方支持”。
- **来源**：opendraft 的 claim-level two-of-three；ISPOR 结构化专家启发（对单专家判断的校准提醒）。

### R3 检索要留“查询日志 + 筛选决定”，不是只贴结果
- **动作**：每次 `wb search` 记录：查询串、日期、数据库、返回数、纳入/排除数；对排除的每条写一句原因（不相关/无全文/已撤稿/重复）。最终给一个 PRISMA 式流水账。
- **示例**：组会综述项目里 `wb search` 得到 47 条，纳入 12 条，排除 35 条各带原因；用 `wb memory` 存下这条日志，方便一周后复现。
- **反例**：只给用户“我搜到了这些论文”而没有检索式与筛选标准，后续无法判断为什么漏掉某篇。
- **来源**：PRISMA 2020。

### R4 专家团先独立表态，再公开；分歧不平均，保留区间
- **动作**：专家团每轮先各自写下判断与依据（不看彼此），再进入公开讨论；分歧点写入 `wb conflict`，保留“支持/反对/条件支持”三方，不把不同意见揉成“多数同意”。
- **示例**：导师 A 主张“必须包含长程任务”，导师 B 主张“先聚焦经典单任务”：记 `conf-001`，由用户裁决 `merge`，双方理由都留在台账。
- **反例**：模型直接输出“专家组普遍认为……”；这既没有独立表态，也把分歧平均掉了。
- **来源**：ISPOR 结构化专家启发；ESSKA/Delphi 共识协议。

### R5 门禁标准必须可测量，并显式记录 Go/Kill/Recycle
- **动作**：每条 gate item 写成“布尔条件 + 证据句”，例如 `引用可点回`、`P1=0`、`反例检索已执行`；`wb gate` 不 PASS 时写 `recycle` 条件（补什么、谁补、何时复检），而不是停在那里发呆。
- **示例**：`wb gate --stage "7 verify" --item "3 条关键引用均未撤稿且可点回" --pass-gate --evidence "Crossref retraction=否; DOI 全部可解析"`。
- **反例**：门禁写“感觉差不多了”“已请专家看过”，无法复检，也无法判断缺口。
- **来源**：Cooper stage-gate；MARTE/复现实验的验收语义。

### R6 交付物按“研究对象”打包：元数据 + 可重跑 + 稳定标识
- **动作**：`artifacts/` 中每个交付物带 `README.md`（目标、输入、输出、运行方法）、版本、作者、日期、license；代码+数据+笔记+PPT 放在同一 crate 或目录下，关键结果赋予 DOI/hash，不叫 `final_v2`。
- **示例**：交付 `agent-eval-report/` 内含 `report.md`、`data/`、`run.sh`、`README.md`、`LICENSE`；若提交外部，用 Zenodo 生成 DOI。
- **反例**：只发一个 `组会PPT_final_v3.pptx`，没有数据、没有运行说明、没有版本；三个月后无法重跑。
- **来源**：RO-Crate；Zenodo；AiiDAlab。

### R7 结论后必须做“反驳检索”，未找到反例 ≠ 证明为真
- **动作**：每个关键 claim 定稿前，跑一次刻意找反例的检索（反向引文、批评性综述、负结果、撤稿记录）；把“未找到反例（检索范围：arXiv+OpenAlex，日期）”记录为 `limited-support`，而不是“已证实”。
- **示例**：写完“方法 A 优于 B”后，检索 `"A" limitations`、`"A" fails`、`"A" replication`，把反驳证据与支持证据并列。
- **反例**：只收集支持证据就宣称结论；用户一问反例就答不上来。
- **来源**：PRISMA/系统综述的偏倚控制；OpenAlex 引用网络反向搜索；MARTE 复现实验。

### R8 文献笔记原子化：一源一卡，claim 回链
- **动作**：每篇论文建一张独立卡片（`papers/<doi>.md`），卡片含元数据、问题、方法、关键结论、与项目 claim 的链接；不要把所有笔记堆进一个长文件。
- **示例**：`papers/10.1145_3711896.3736570.md` 里写「结论 X → 项目 claim eval-gap-01」；用 `wb claim` 的 source 字段回链。
- **反例**：把 20 篇论文的摘要复制进一个 `notes.md`，后续想引用某一句时找不到出处、无法点回。
- **来源**：Zotero 文档；Obsidian 文献工作流实践。

## 来源

- `expert-decision-consensus`（九段决策环）
- `research-module` / `teacher-module` / `dev-workflow-consensus`（领域适配）
- `workbench_cli.py`（`tools/workbench_cli.py`）
- LightRead 官网与博客（搜读写算、证据回溯、阶段验收）
