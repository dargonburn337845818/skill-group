---
name: teacher-module
description: 教师模块的人名专家团 + 回合式讨论协议：按领域加载具体人名专家，每轮独立表态→冲突点表→主持人/用户裁决→带 expert_id/expert_name 的结论。用于答疑、纠偏、多专家讨论、方案分歧裁决。
whenToUse: 用户进入教师模式，需要“具体人名专家团”而不是抽象角色；或需要对一个问题做多专家独立表态、冲突裁决、结论留痕。
---

# 教师模块 · 人名专家团与回合式讨论

> 专家不是抽象角色，而是“领域 + 具体人名”。本模块负责：识别领域 → 加载已备好人名专家团 → 按回合式协议讨论 → 裁决 → 输出带专家署名的结论。
> 数据源：`vault/meta/EXPERT_LIBRARY.json`（人名专家库）与 `vault/meta/domain-profiles.json`（领域字典）。
> 标准化协议：`vault/skills/teacher/expert-team/SKILL.md`——本模块是 teacher 场景实现，dev/writing/research/distill 复用同一协议，不另造流程。

## 这是什么

- **人名专家团**：每个专家是真实公开人物，只作为“风格/方法论参考”，不伪造原话。
- **回合式讨论协议**：每轮每位专家独立表态 → 汇总冲突点表 → 主持人/用户裁决 → 每条结论标注 `expert_id` + `expert_name`。
- **专家缺口**：识别到领域但没有 ready 人名专家时，明确询问“蒸馏专家团 / 放弃专家团直接用大模型”，不静默降级。

## 何时使用

- 学生/用户拿一道题或一个方案，需要“被多位大师视角拆解”而不是单一答案。
- 存在分歧：需要保留不同立场，交给用户或主持人裁决。
- 需要可追溯的教学结论：以后能看出“是哪位专家的风格在指导”。

## 一、启动：领域识别与专家团加载

1. 使用运行时工具 **`teacher_discussion_start`**：传 `text`（自然语言）或 `domain_id`，可直接创建讨论会话并加载 ready 专家团。
2. 也可以先调用 `skill_domain_recognize`（或 `python3 scripts/domain_recognize.py --text ... --json`）查看识别结果。
3. 读取输出：
   - `decision = "expert_team"`：`experts[]` 是已 ready 的人名专家，直接使用。
   - `decision = "expert_gap"`：会话 `discussion.status = "expert_gap"`，向用户明确提问，选项为 `distill_expert` / `use_llm_directly`；**不要静默用大模型扮演专家**。
   - `decision = "ask_domain"`：询问用户具体领域，不猜测。
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

## 关联文件

- `discussion-protocol.md` — 完整回合协议与机器可读 JSON 契约。
- `expert-selection.md` — 专家选择、添加与 ready 门槛。
- `examples/round_discussion.md` — 一个完整的算法竞赛回合示例。
- `vault/meta/EXPERT_LIBRARY.json` / `vault/meta/domain-profiles.json` — 数据源。
