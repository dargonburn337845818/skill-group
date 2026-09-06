---
name: teacher-module
description: 教师模块的人名专家团 + 回合式讨论协议：按领域加载具体人名专家，每轮独立表态→冲突点表→主持人/用户裁决→带 expert_id/expert_name 的结论。用于答疑、纠偏、多专家讨论、方案分歧裁决。
whenToUse: 用户进入教师模式，需要“具体人名专家团”而不是抽象角色；或需要对一个问题做多专家独立表态、冲突裁决、结论留痕。
---

# 教师模块 · 人名专家团与回合式讨论

> 专家不是抽象角色，而是“领域 + 具体人名”。本模块负责：识别领域 → 加载已备好人名专家团 → 按回合式协议讨论 → 裁决 → 输出带专家署名的结论。
> 数据源：`vault/meta/EXPERT_LIBRARY.json`（人名专家库）与 `vault/meta/domain-profiles.json`（领域字典）。
> 标准化协议：`vault/skills/teacher/expert-team/SKILL.md`——本模块是 teacher 场景实现，dev/writing/research/distill 复用同一协议，不另造流程。
> 需要把讨论升级为“可检查、可追溯、可验收决策”时，加载 `expert-decision-consensus`；需要项目台账/文件交付时走 `workbench-module` + `wb`。

## 这是什么

- **人名专家团**：每个专家是真实公开人物，只作为“风格/方法论参考”，不伪造原话。
- **回合式讨论协议**：每轮每位专家独立表态 → 汇总冲突点表 → 主持人/用户裁决 → 每条结论标注 `expert_id` + `expert_name`。
- **专家缺口**：识别到领域但没有 ready 人名专家时，默认直接用大模型继续，并把缺口记进项目台账；不弹 DSH 对话框询问。若用户后续明确要求，再蒸馏专家团。

## 何时使用

- 学生/用户拿一道题或一个方案，需要“被多位大师视角拆解”而不是单一答案。
- 存在分歧：需要保留不同立场，交给用户或主持人裁决。
- 需要可追溯的教学结论：以后能看出“是哪位专家的风格在指导”。

## 一、启动：领域识别与专家团加载

1. 使用运行时工具 **`teacher_discussion_start`**：传 `text`（自然语言）或 `domain_id`，可直接创建讨论会话并加载 ready 专家团。
2. 也可以先调用 `skill_domain_recognize`（或 `python3 scripts/domain_recognize.py --text ... --json`）查看识别结果。
3. 读取输出：
   - `decision = "expert_team"`：`experts[]` 是已 ready 的人名专家，直接使用。
   - `decision = "expert_gap"`：会话 `discussion.status = "expert_gap"`，默认按 `use_llm_directly` 继续；不弹窗，把缺口记进项目台账。若用户明确要求，再蒸馏专家团。
   - `decision = "ask_domain"`：默认按 `use_llm_directly` 继续；如需用户指定领域，用普通文字列出候选，不弹窗。
4. 如果用户指定人数/风格，可用 **`teacher_expert_select`** 选择子集（选择规则见 `expert-selection.md`）。

## 二、回合式讨论协议（单轮）

每轮按以下顺序执行，完整 JSON 契约见 `discussion-protocol.md`。

```text
1. 定主题（本轮要回答的问题）
2. 专家独立表态（彼此不知道他人的回答）
3. 汇总冲突点表（claim_a / claim_b / 来源 / 对齐专家）
4. 主持人或用户裁决（采纳 A / 采纳 B / 合并分支 / 驳回 / 延后）
5. 输出本轮结论（每条带 expert_id + expert_name + sourceRefs）
6. 若未收敛且用户要求，进入下一轮
```

### 独立表态的输入

每个专家的“立场”必须来自其 `style` / `sourceRefs` 的风格推断，不是本人原话。模拟时统一注明：

> 以下为基于公开资料的风格推断，非本人原话。

### 冲突点表

相同问题、不同专家给出不同立场时，必须写成冲突条目，不得强压成一致结论：

```json
{
  "conflict_id": "c1",
  "topic": "是否先写暴力",
  "claim_a": { "expert_id": "tourist", "expert_name": "Tourist", "stance": "先暴力再优化" },
  "claim_b": { "expert_id": "um-nik", "expert_name": "Um_nik", "stance": "先读题重述再动手" },
  "aligned_expert_ids": ["tourist", "jiangly"],
  "sources": ["..."],
  "resolution": null
}
```

### 裁决取值

- `adopt_a` / `adopt_b`：采纳某一分支。
- `merge`：两者不矛盾，合并为复合结论。
- `reject`：证据不足，驳回该分支。
- `defer`：信息不足，保留为开放分支，进入下一轮。

## 三、输出纪律（每条结论）

- 必须含 `expert_id` 与 `expert_name`。
- 必须含 `persona_type = public-figure-style-reference`。
- 必须保留该专家的 `sourceRefs`。
- 不得写“某某专家说……”的伪造原话；应写“按某专家风格，倾向……”。
- 分歧未被裁决时不得静默合并；在冲突表中保留。

## 三点五、运行时工具与 API（已实现）

Agent 可直接调用：

- `teacher_discussion_start(text|domain_id, expert_ids?)` — 创建会话、加载 ready 专家、处理专家缺口。
- `teacher_discussion_round(session_id, topic, speaks, conflicts, adjudications, conclusions)` — 追加一轮完整讨论。
- `teacher_discussion_status(session_id?)` — 读取当前领域、专家团与每轮讨论记录。
- `teacher_expert_select(session_id, expert_ids)` — 从该领域 ready 专家中选择子集。
- `teacher_discussion_finish(session_id)` — 结束会话。

HTTP API（供侧边栏/外部 UI 只读或写事件）：

- `GET /skill-vault/api/teacher/status?session_id=...`
- `POST /skill-vault/api/teacher/start`
- `POST /skill-vault/api/teacher/round`
- `POST /skill-vault/api/teacher/select`
- `POST /skill-vault/api/teacher/finish`

## 四、侧边栏过程监视器数据接口

统一过程监视器（`conversation.view`）需要拿到三类信息：当前领域、专家团名单、每轮讨论记录。最小 payload：

```json
{
  "mode": "teacher",
  "domain": { "id": "algorithm", "name": "算法竞赛", "confidence": "high" },
  "experts": [
    { "id": "tourist", "name": "Tourist", "displayName": "Tourist（顶尖算法选手）", "status": "ready" },
    { "id": "jiangly", "name": "jiangly", "displayName": "jiangly（顶尖算法选手）", "status": "ready" }
  ],
  "discussion": {
    "status": "active",
    "current_round": 2,
    "rounds": [ /* 每轮 speak / conflicts / adjudications / conclusions */ ]
  }
}
```

- 领域与专家团可从 `GET /skill-vault/api/domain/status` 读取。
- 讨论记录按 `discussion-protocol.md` 中的 `DiscussionSession` 契约输出。
- 无 ready 专家时 `discussion.status = "expert_gap"`，侧边栏显示“专家缺口”。

## 五、专家添加/选择接口（先留接口，不强制 UI）

- **选择专家**：默认使用领域 `expert_ids` 中全部 ready 专家；用户可点名“只要 tourist 和 jiangly”或“换掉某某”，会话内按名字/ID 过滤。
- **添加专家**：由用户/蒸馏会话向 `EXPERT_LIBRARY.json` 追加条目；字段与 ready 门槛见 `expert-selection.md`。已实现 `teacher_expert_select` 用于选择；`expert_add` 仍走数据文件 + `domain-profiles.json` 手工/蒸馏回填入口。

## 边界

- 本 skill 不保证专家“真实说过”某句话；它只按公开风格推断搭模型。
- 没有 `sourceRefs` 的专家不得设为 `status: ready`。
- 不替用户做最终裁决；主持人可以给建议，但结论必须记录裁决人。
- 若讨论无明显分歧，也应显式说明“本轮无冲突”，不要伪造冲突。

## 2026 深度补强（Round 36）

> 本节补齐教师模块的五类高频实操缺口：专家组合的视角多样性、多轮独立表态防锚定、主持人提问/追问节奏、教学反馈的可行动结构、跨模块调用路由。每条规则按“触发 → 动作 → 边界 → 来源”写；来源编号见 `SOURCES.md` 的 Round 36。

### R36-1 专家团视角多样性检查

**触发**：`teacher_expert_select` 或用户点名专家子集时。

**动作**：

1. 把候选专家的 `role`/`style` 归入三类：实现/基线型、模型/读题型、教学/拆解型。
2. 至少覆盖 2 类；只有 1 类时明确告诉用户“这是单一视角专家团”，并询问是否补一位不同方法论专家。
3. 同一类 ≥ 3 人时，建议只保留来源与风格差异最大者，避免重复视角稀释讨论。
4. 用户只选 1 位专家时，输出 `single_expert_view=true`，结论标注为“单一专家参考”，不当作多专家裁决。

**边界**：领域只有一位权威或用户明确只要单人时不硬凑；不要为“多样性”引入来源可信度不足的人物。

**来源**：R36-7、R36-8、R36-9。

### R36-2 多轮独立表态防锚定

**触发**：开始第 2 轮及以后；或发现某专家直接引用其他专家立场。

**动作**：

1. 每轮重新生成表态：隐藏上一轮结论与其他专家的 `stance`，只按该专家自己的 `style` + `sourceRefs` 独立生成。
2. 表态中禁止出现“因为 X 专家也这么说”作为理由；出现即判为空锚定，删除重写。
3. 输出附 `round_anchor_free=true`，供侧边栏与过程监视器核查。

**反例**：R2 某专家写“tourist 都先暴力了，那我也先暴力”——这是锚定，不是独立表态。

**边界**：用户显式要求专家互相反驳（`mode=debate`）时，允许引用他人立场，但必须标注为反驳模式，不再按匿名独立表态计。

**来源**：R36-7、R36-10。

### R36-3 提问节奏与追问链

**触发**：教师/主持人向学员提问，或讨论中需要把学员引到下一步。

**动作**：

1. 三阶提问：先低风险确认题（“你的状态定义是什么？”）→ 再推理题（“这个转移为什么成立？”）→ 最后元认知题（“你第一次卡在哪一步？”）；不要上来就问大而空的“你怎么想”。
2. 每次提问后默认等待 3–5 秒；沉默不等于不会，不要替学员回答或立刻追问。
3. 追问一次只问一个信息点：`依据是什么？` → `有没有反例？` → `条件变了会怎样？`；禁止“所以你是……？然后呢？还有呢？”式三连问。
4. 连续 2 次追问仍无产出时，转为给一个最小例子/提示，而不是继续加问。

**边界**：学员明确说“只要答案”或时间极紧（如考后快复盘）时，可缩短等待与追问，但仍保留一次确认题。

**来源**：R36-4、R36-5、R36-6、R36-12。

### R36-4 可行动反馈结构

**触发**：给出教学反馈、作业评语、或专家结论落地为学习者下一步时。

**动作**：

1. 使用“目标 → 差距 → 下一步最小动作”三行结构，不用“先表扬、再批评、再表扬”的三明治。
2. 反馈必须指到具体位置/具体动作，例如“第 3 行越界，改成 n+1”，而不是“注意边界”。
3. 同时点评一个“做对的部分”，说明哪个策略值得保留。
4. 给学员一次立即重做/修正的机会，再检查一次；没有行动空间的反馈不算完成。

**反例**：“很好，但要多练习” = 空反馈；“这里错了”不告诉下一步 = 不可行动反馈。

**边界**：纯纠错/评分场景不强制重做，但必须给出具体差距与一个改进方向。

**来源**：R36-1、R36-2、R36-3、R36-11。

### R36-5 反馈层级与自我评价禁忌

**触发**：反馈对象是学员表现（题目、方案、写作、代码等）。

**动作**：

1. 按层级推进：任务层（对不对/怎么修）→ 过程层（策略/方法）→ 自我调节层（是否监控、是否换法）。
2. 不评价“人”：不说“你很聪明/你不够自律”，改说“这次你用了什么策略/下次换什么策略”。
3. 对初学者或低成就学员，优先给明确可执行的任务+过程反馈，少讲自我调节大道理。

**来源**：R36-1、R36-3、R36-11。

**边界**：高成就学员主动要求挑战时，可增加自我调节层；人格评价只允许出现在关系修复等极少数场景，不作为常规协议。

### R36-6 冲突表：分歧与“同向不同因”分开

**触发**：生成冲突点表或发现多位专家动作一致但理由不同。

**动作**：

1. 两位专家给出同一动作但理由不同 → 不写进 `conflicts`，写入 `same_route_different_reasons[]`，合并结论中保留两条理由。
2. 只有“动作/结论相反”才生成 conflict 条目（`claim_a` / `claim_b`）。
3. 若一位专家给出桥接路径，作为 `bridge_option` 单列，不强行归入 A 或 B。

**反例**：把“都建议先暴力，一个为了理解、一个为了调试”写成冲突，会制造不必要裁决。

**来源**：R36-8、R36-9。

### R36-7 跨模块调用路由

**触发**：teacher 会话需要继续进入其他模块（检索、台账、决策、文稿）。

**动作**：

1. 按目标路由：需要“多来源检索/资料核验” → `search-source`；需要“项目台账/文件交付” → `workbench-module`；需要“标准专家决策/裁决留痕” → `expert-decision-consensus`；需要“纯文案” → `writing-module`。
2. 对外只传 `conclusions[]`（`expert_id` / `expert_name` / `text` / `sourceRefs` / `adjudicated_by`），不把未裁决的 `speaks` 当结论传。
3. 其他模块已有同类协议时，不要重复跑一轮讨论；只登记 `external_decision` 引用并回链 teacher `session_id`。
4. 跨模块前检查目标领域是否有 ready 专家；没有就先走缺口分支，不把算法竞赛专家团硬搬到非算法领域。

**边界**：用户只是想继续对话、未要求跨模块交付时，不主动路由；跨模块只做辅助，不替代用户裁决。

**来源**：R36-9、R36-10、本模块 `FORMAL_SPEC` 复用约束。

## 关联文件

- `discussion-protocol.md` — 完整回合协议与机器可读 JSON 契约。
- `expert-selection.md` — 专家选择、添加与 ready 门槛。
- `examples/round_discussion.md` — 一个完整的算法竞赛回合示例。
- `vault/meta/EXPERT_LIBRARY.json` / `vault/meta/domain-profiles.json` — 数据源。
