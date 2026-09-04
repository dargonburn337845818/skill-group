# 回合式讨论示例：算法竞赛（Round Discussion Example）

> 场景：用户问“这道树形 DP 题，我上来就想写换根合并，是不是应该先验证一下？”
> 领域：算法竞赛。默认专家团：tourist / jiangly / Um_nik / Errichto（示例只取 4 位）。
> 全部表态均为**基于公开资料的风格推断，非本人原话**；引用保留 sourceRefs。

## 第 1 轮：定主题

**主题**：拿到树形 DP 题，应“先写暴力/基线”还是“先重述模型并确认状态”？

## 独立表态

### R1 · tourist（先暴力再优化）

- **立场**：先写暴力/朴素 DP 建立正确基线，确认转移再优化。
- **理由（风格推断）**：风格上强调用暴力确认理解，再信息论式地压缩状态。
- **sourceRefs**：`https://codeforces.com/profile/tourist`；`$WORKSPACE/skills/teacher-consensus-skill/output/teacher_consensus_final.json`

### R1 · jiangly（边界完整）

- **立场**：不管先暴力还是直接优化，先把边界与空树/单点/非连通情形写完整。
- **理由（风格推断）**：风格上偏可复现、实现边界完整，避免细节翻车。
- **sourceRefs**：`https://codeforces.com/profile/jiangly`；`$WORKSPACE/skills/teacher-consensus-skill/content/expert_research.md`

### R1 · um-nik（读题重述）

- **立场**：先审问题面：为什么是树？这个限制去掉会怎样？把目标函数重述成标准 DP 模型，再决定状态。
- **理由（风格推断）**：公开材料中强调读题时追问限制与不寻常处，不按标签直接套算法。
- **sourceRefs**：`https://codeforces.com/blog/entry/113785`；`https://codeforces.com/blog/entry/62730`

### R1 · errichto（教学拆解）

- **立场**：把“换根合并”降级为“先想清楚子树贡献的合并方式”，用最小区间/小样例验证；教学上按主题拆到可训练的小步骤。
- **理由（风格推断）**：内容风格偏教学式拆解、按主题组织题单。
- **sourceRefs**：`https://codeforces.com/profile/Errichto`；`https://codeforces.com/blog/entry/144520`

## 冲突点表

| conflict_id | 冲突 | claim_a | claim_b | aligned | 来源 |
|---|---|---|---|---|---|
| c1 | 第一步做什么 | tourist：先暴力基线 | um-nik：先重述问题模型 | A：tourist, jiangly；B：um-nik | tourist profile / um-nik blog |

**说明**：tourist 与 jiangly 都强调“先有可运行基线”，um-nik 强调“动手前先建模”；errichto 处于中间，建议用小样例验证后合并。

## 裁决

- **adjudicator**：user
- **decision**：`merge`（合并）
- **reason**：先花 2 分钟把题面重述成模型并定义状态，再写一个朴素 DP 作为正确性基线；等基线通过小样例后，再做换根合并优化。

## 本轮结论（带专家署名）

### 结论 1 · um-nik

```json
{
  "conclusion_id": "concl_1",
  "round": 1,
  "expert_id": "um-nik",
  "expert_name": "Um_nik",
  "persona_type": "public-figure-style-reference",
  "text": "按 Um_nik 的读题风格：先问“为什么是树 / 去掉限制会怎样”，把目标函数重述成标准 DP 模型，再进入状态设计。",
  "sourceRefs": ["https://codeforces.com/blog/entry/113785", "https://codeforces.com/blog/entry/62730"],
  "decision": "merge",
  "adjudicated_by": "user"
}
```

### 结论 2 · tourist

```json
{
  "conclusion_id": "concl_2",
  "round": 1,
  "expert_id": "tourist",
  "expert_name": "Tourist",
  "persona_type": "public-figure-style-reference",
  "text": "按 Tourist 的风格：先写朴素 DP 作为基线，确认转移正确后再压缩状态；不要直接跳到换根合并。",
  "sourceRefs": ["https://codeforces.com/profile/tourist", "$WORKSPACE/skills/teacher-consensus-skill/output/teacher_consensus_final.json"],
  "decision": "merge",
  "adjudicated_by": "user"
}
```

### 结论 3 · jiangly（边界提醒）

```json
{
  "conclusion_id": "concl_3",
  "round": 1,
  "expert_id": "jiangly",
  "expert_name": "jiangly",
  "persona_type": "public-figure-style-reference",
  "text": "按 jiangly 的实现风格：在写 DP 前把空树、单点、根任选、重复贡献等边界想完整；实现时保留可复现的测试。",
  "sourceRefs": ["https://codeforces.com/profile/jiangly", "$WORKSPACE/skills/teacher-consensus-skill/content/expert_research.md"],
  "decision": "merge",
  "adjudicated_by": "user"
}
```

## 侧边栏过程监视器最小 payload（本示例）

```json
{
  "mode": "teacher",
  "domain": { "id": "algorithm", "name": "算法竞赛", "confidence": "high" },
  "experts": [
    { "id": "tourist", "name": "Tourist", "displayName": "Tourist（顶尖算法选手）", "status": "ready" },
    { "id": "jiangly", "name": "jiangly", "displayName": "jiangly（顶尖算法选手）", "status": "ready" },
    { "id": "um-nik", "name": "Um_nik", "displayName": "Um_nik（Alex Danilyuk，顶尖算法选手/博主）", "status": "ready" },
    { "id": "errichto", "name": "Errichto", "displayName": "Errichto（顶尖算法选手/内容创作者）", "status": "ready" }
  ],
  "discussion": {
    "status": "active",
    "current_round": 1,
    "rounds": []
  }
}
```

> 实际运行时 `rounds[]` 会按 `discussion-protocol.md` 的 Round 结构填入 speak / conflicts / adjudications / conclusions。
