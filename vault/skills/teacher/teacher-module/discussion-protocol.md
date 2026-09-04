# 回合式讨论协议（Round-Based Discussion Protocol）

> 目标：让“多位具体人名专家”对一个主题做可追溯的讨论。每轮：独立表态 → 冲突点表 → 主持人/用户裁决 → 带专家署名的结论。
> 适用：教师模式答疑、纠偏、方案评审；也可被科研/开发等模块复用。

## 1. 状态机

```text
start
  → identify_domain        # 领域识别
  → load_experts           # 加载该领域 ready 人名专家
  → expert_gap?            # 无 ready 专家时询问 distill/use_llm_directly
  → select_experts         # 默认全量，用户可点名子集
  → round_loop
       ├─ independent_speak   # 每位专家独立表态
       ├─ conflict_table      # 生成冲突点表
       ├─ adjudicate          # 主持人或用户裁决
       ├─ conclusions         # 输出带 expert_id/expert_name 的结论
       └─ more? ── yes → independent_speak
                └─ no → finish
```

## 2. 每轮执行步骤

### 2.1 定主题（Round Topic）

一轮只处理一个明确问题。例如：

- “这道题该先写暴力，还是先重述成标准模型？”
- “这个方案在并发下是否安全？”

### 2.2 独立表态（Independent Speaks）

- 每位专家**互不知晓**其他专家本轮回答，只根据自身 `style` + `sourceRefs` 给出立场。
- 表态必须标记为**风格推断**，禁止伪造原话。
- 每个 `speak` 记录：`expert_id`、`expert_name`、`persona_type`、`stance`、`claims[]`、`style_inference=true`、`sourceRefs[]`。

### 2.3 冲突点表（Conflict Table）

对同一问题，若存在不同立场或不同理由，生成冲突条目：

```json
{
  "conflict_id": "c1",
  "topic": "是否先写暴力",
  "claim_a": {
    "expert_id": "tourist",
    "expert_name": "Tourist",
    "stance": "先暴力再优化",
    "reason": "没有暴力说明还没理解问题"
  },
  "claim_b": {
    "expert_id": "um-nik",
    "expert_name": "Um_nik",
    "stance": "先审问题面并重述成标准模型",
    "reason": "很多卡壳源于读题遗漏与术语误读"
  },
  "aligned_expert_ids": ["tourist", "jiangly"],
  "aligned_expert_names": ["Tourist", "jiangly"],
  "sources": [
    "https://codeforces.com/profile/tourist",
    "https://codeforces.com/blog/entry/113785"
  ],
  "resolution": null
}
```

规则：

- 有分歧必须列出，不得抹成 50% 共识。
- 一个冲突点只放两方主立场；若存在多方，拆成多个冲突条目。
- `aligned_expert_ids` 只放真正支持该方的人，不能靠猜测。

### 2.4 裁决（Adjudication）

- 裁决人：`user`（用户）或 `host`（主持人/agent 建议）。默认建议由主持人给出，但**最终采纳标记必须记录裁决人**。
- 裁决取值：
  - `adopt_a`：采纳 claim_a。
  - `adopt_b`：采纳 claim_b。
  - `merge`：二者可合并，生成合并结论。
  - `reject`：证据不足，双双驳回。
  - `defer`：信息不足，保留分支，下一轮继续。
- 若用户未裁决，主持人不能擅自把 `defer` 写成已采纳。

```json
{
  "conflict_id": "c1",
  "adjudicator": "user",
  "decision": "merge",
  "reason": "先暴力建立基线，但读题重述要在动手前完成；两者不冲突。",
  "adjudicated_at": "2026-09-04T12:00:00Z"
}
```

### 2.5 结论（Conclusions）

每条结论必须带专家署名：

```json
{
  "conclusion_id": "concl_1",
  "round": 1,
  "expert_id": "um-nik",
  "expert_name": "Um_nik",
  "persona_type": "public-figure-style-reference",
  "text": "按 Um_nik 的读题风格，先对限制词和术语做审问，再把题面重述成标准模型。",
  "sourceRefs": [
    "https://codeforces.com/blog/entry/113785",
    "https://codeforces.com/blog/entry/62730"
  ],
  "decision": "merge",
  "adjudicated_by": "user"
}
```

规则：

- 无专家署名的结论不能称为“专家结论”；可标 `actor: host` 作为主持建议。
- 每条 `sourceRefs` 必须能回溯到该专家的公开资料。
- 若采纳了合并结论，也要标注来源专家与裁决人。

## 3. 机器可读 JSON 契约

### 3.1 DiscussionSession（侧边栏监视器读取）

```json
{
  "mode": "teacher",
  "session_id": "teacher_20260904_001",
  "domain": {
    "id": "algorithm",
    "name": "算法竞赛",
    "confidence": "high",
    "status": "ready"
  },
  "experts": [
    {
      "id": "tourist",
      "name": "Tourist",
      "displayName": "Tourist（顶尖算法选手）",
      "role": "算法竞赛顶尖选手 / 风格参考",
      "persona_type": "public-figure-style-reference",
      "status": "ready",
      "sourceRefs": []
    }
  ],
  "discussion": {
    "status": "active",
    "current_round": 2,
    "rounds": [],
    "gap_fallback": null
  }
}
```

字段说明：

| 字段 | 类型 | 说明 |
|---|---|---|
| `mode` | string | 固定 `teacher` |
| `domain` | object | 当前领域，来自领域识别结果 |
| `experts` | array | 已选专家团（ready 且被用户选择） |
| `discussion.status` | string | `active` / `finished` / `expert_gap` |
| `discussion.current_round` | number | 当前轮号 |
| `discussion.rounds` | array | 每轮完整记录 |
| `discussion.gap_fallback` | object/null | 专家缺口时的二选一询问 |

### 3.2 Round 完整记录

```json
{
  "round": 1,
  "topic": "该题应先暴力还是先重述模型？",
  "status": "adjudicated",
  "speaks": [],
  "conflicts": [],
  "adjudications": [],
  "conclusions": []
}
```

- `speaks`：本轮全部独立表态。
- `conflicts`：冲突点表。
- `adjudications`：裁决记录（可多条）。
- `conclusions`：本轮采纳结论。

### 3.3 侧边栏渲染建议

- 顶部：当前领域、专家团名（`displayName` 列表）。
- 讨论流：按 `round` 分组，每条显示 `R{round}` + 专家名 + 立场 + 裁决标记。
- 冲突条目：显示 `claim_a` / `claim_b` 两行与来源，未裁决的标 `defer`。
- 专家缺口：显示 `discussion.status = "expert_gap"` 与 `gap_fallback` 文案，不显示伪专家结论。

## 4. 与现网 API 的对接（已实现）

- 领域/专家团：`GET /skill-vault/api/domain/status` 返回 `profiles` 与 `experts`。
- 讨论会话（当前领域 + 专家团 + 每轮记录）：
  - `GET /skill-vault/api/teacher/status?session_id=...`
  - `POST /skill-vault/api/teacher/start`
  - `POST /skill-vault/api/teacher/round`
  - `POST /skill-vault/api/teacher/select`
  - `POST /skill-vault/api/teacher/finish`
- Agent 工具已注册：`teacher_discussion_start` / `teacher_discussion_round` / `teacher_discussion_status` / `teacher_expert_select` / `teacher_discussion_finish`。
- 侧边栏 `conversation.view` 会优先读取 `/skill-vault/api/teacher/status`，失败时回退示例占位。

## 5. 防坑

- 不要让专家“互相看到后再改口”；独立表态是协议核心。
- 不要为了和谐删除冲突；冲突是信息。
- 不要伪造 `sourceRefs`；没有来源的立场只能作为 `common-lore` 并降权。
- 用户选择 `use_llm_directly` 后，不要再显示“专家团”，直接切换为普通 LLM 回答模式。
