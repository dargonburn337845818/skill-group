---
name: value-iterator
description: 价值驱动迭代器——接收当前 Skill 草案与外部反馈/新验证语料，比较新旧两版知识节点数量，按收益规则决定接受或回退，并强制生成变更日志。用于核心能力 Skill 的反复精修。
---

# 迭代器（Value Iterator）

> 定位：迭代器不是“让 Skill 变的更丰富”，而是“让 Skill 变出可量化的新有效知识”。如果新版本只是把旧话换一种说法，或只塞进一些未经验证的注脚，必须拒绝更新。

## 触发条件

- 持有当前 Skill 草案，并且收到新的外部反馈或新的已验证语料。
- 调度器要求“基于本轮高优语料修订 Skill”。
- 用户要求“在这版 Skill 上继续迭代一轮”。

## 输入约定

```text
input = {
  old_skill: {
    id, version,
    text,
    knowledge_nodes: [ Node ],
    source_refs: [ ... ],
    meta: { createdAt, round }
  },
  feedback: string | [ { type: "user" | "expert" | "test", content, priority } ],
  verified_corpus: [ verified-high / verified-single 条目 ],   # 只允许来自收益过滤器
  pending_doubt_list: [ single-doubt 条目 ]                    # 只允许作为注脚候选，不计数
}
```

## 版本与持久化

- 每次接受更新必须递增版本号（**semver**）：`v{major}.{minor}.{patch}`。新增有效能力 → `minor+1`；仅修正错别字/格式 → `patch+1`；破坏性接口变更 → `major+1` 并写迁移说明。
- 变更日志不仅要内联在输出里，还要追加到 skill 目录 `CHANGELOG.md`，字段：`date, version, accepted, effective_new_count, gaps_closed`。
- 调度器应在 `round_ledger.json` 里保存每轮状态，便于下一轮从上一个版本继续，而不是从零重建。

## 反馈优先级

当多个反馈冲突时，按以下顺序处理，不平均：

```text
用户反馈 > 专家反馈 > 测试反馈
```

- 用户反馈作为硬约束：若与专家/测试冲突，用户优先，并在 changelog 写 `override: user`。
- 专家反馈高于测试反馈；测试反馈用于找出“当前版本在哪里失效”，不直接改写核心规则。
- 所有保留分歧必须进入 `Conflict Branches`，不能为了顺序而删除任一分歧。

## 核心定义

### 知识节点（Node）

一个原子、可证伪、可执行、能改变行为的规则单元：

```text
Node = {
  id,
  claim: "触发条件 → 动作 → 预期结果",
  source_refs,
  evidence: "verified-high" | "verified-single" | "footnote",
  weight: 1.0 | 0.5 | 0.0,
  boundary: "什么情况下失效",
  provenance: "new" | "merged" | "updated" | "unchanged",
  trace_chain: [ "raw_chunk_id -> verified -> primitive -> node" ],   # 可追溯思维链
  effect_ref?: "value-effect-audit 的 node_effects 条目 id"            # 实际效果证据
}
```

### 有效新增节点（Effective New Node）

同时满足：

1. 旧 Skill 中不存在同义/等价节点；
2. 证据类型为 `verified-high` 或 `verified-single`（不是纯注脚）；
3. 包含可执行的触发条件、动作、边界三件套；
4. 通过“删除测试”：删掉它，Skill 的某个可执行行为会退化。

### 待定注脚（Footnote）

来自 `single-doubt` 或 `verified-single` 的低置信补充。不计入有效新增节点，不能作为核心规则，只能挂在“待验证注脚”区。

### 增量计数细则

```text
effective_new_count = count(new added/conflict nodes) - count(old effective nodes)
```

- `updated`：核心主张不变、措辞/证据更精确 → **不计新增**。
- `merged`：把两条同义节点合并为一条 → **不计新增**，若合并后仍保留两套独立触发/边界，则只计 1 条且注明 `merged-expanded`。
- 冲突分支：若新分支独立可执行（三件套齐全）且证据为 verified-high/single，**计 1**，`provenance="conflict"`；否则计 0，只进待裁决。
- `verified-single` 新节点计 1，但必须同时挂“单源待证”注脚，并在 `risk_notes` 提示。
- 纯 `footnote` 永远不计入 `effective_new_count`。

## 处理流程

1. **标准化旧版**：把旧 Skill 解析成 Node 集合与脚注集合，去重、合并同义节点。
2. **从 verified_corpus 提取候选节点**：每块高优语料切到最小推理单元，生成候选 Node；只有三件套齐全才成为“候选有效节点”。
3. **冲突处理**：
   - 候选与旧节点核心主张相同但更精确 → 记录为 `updated`，不算新增；
   - 候选与旧节点冲突 → 保留两个分支，不平均；若新分支证据更强，标记 `conflict-candidate` 供校验器/用户裁决；
   - 候选来自 `verified-single` → 标 `weight=0.5`，仍可算有效新增，但必须挂“单源待证”注脚。
4. **生成新版本**：旧版 + 全部有效变更 + 可选脚注，得到 `new_skill`。
5. **计算节点增量**：
   ```text
   effective_new_count = count(new_skill.effective_nodes) - count(old_skill.effective_nodes)
   footnote_added_count = count(new_skill.footnotes) - count(old_skill.footnotes)
   ```
6. **执行收益拒绝规则（硬逻辑）**：
   ```text
   if effective_new_count < 2 and 所有新增节点均来自 single-doubt/footnote:
       → 拒绝本轮迭代
       → 回退到 old_skill
       → 向调度器发送信号: "收益不足，拒绝更新"
     否则:
       → 接受新版本
       → 输出变更日志
   ```
   - 说明：如果新增节点少于 2 个，但其中至少 1 个是 validated（verified-high/verified-single）有效节点，可以接受，但要在日志中标注“低增量接受，建议下一轮强制收益评估”。
   - 如果新增节点全部来自单源-存疑（`single-doubt`），即使数量 ≥ 2，也**不得作为核心规则**；只能作为脚注，不计入有效新增。
7. **生成变更日志**：必须包含下表，且每条变更可回溯。

## 变更日志格式

```text
## 变更日志 v{old} → v{new}

### Added (有效新增)
| node_id | claim 摘要 | 证据 | 来源 | 权重 | 对应缺口 |
|---|---|---|---|---|---|

### Updated / Merged
| node_id | 旧 | 新 | 原因 |

### Conflict Branches (保留分歧)
| node_id | 分支A | 分支B | 证据强度 | 待裁决 |

### Footnotes (待定注脚)
| node_id | 内容 | 来源 | 为何不升级为核心 |

### Removed
| node_id | 原因 |

### Rejected / Rollback
- 若触发“收益不足，拒绝更新”，写明：effective_new_count, 新增来源构成, 回退原因。
```

## 来源与可追溯

- 完整来源声明见本目录 `SOURCES.md`。
- 设计来源：用户规格《认知收益架构 / 价值驱动递归提升模块》；Node 三件套继承 `distillation-consensus`。
- 外部参考：[Prompt Versioning in Production](https://www.respan.ai/articles/prompt-versioning)、[Version & Rollback LLM Agent Prompts](https://www.arthur.ai/column/version-rollback-prompts-llm-agents)。

## 干跑验证

- 六阶段完整干跑样例见 `core-iteration/examples/smoke_pipeline.md`。
- 每次接受/拒绝都要生成 changelog 并更新 `CHANGELOG.md`；没有 changelog 视为未完成。

## 输出信号契约

```text
{
  "accepted": true | false,
  "signal": "ok" | "收益不足，拒绝更新",
  "old_version": "...",
  "new_version": "...",        # accepted=false 时回退为 old_version
  "effective_new_count": n,
  "footnote_added_count": m,
  "node_delta": { "added": [], "updated": [], "merged": [], "removed": [], "footnotes": [] },
  "changelog": "...",
  "risk_notes": ["单源待证注脚未计数", "..."]
}
```

## 硬性纪律

1. **拒绝必须回退**：一旦触发“收益不足”，不得保留新版本的任何有效节点增量；旧版原样返回。
2. **变更日志必须生成**：无论接受还是拒绝，都必须输出日志；日志是调度器与用户审计的唯一依据。
3. **不把脚本当收益**：`single-doubt` 即使写成正式条文，也不算有效新增；它只能出现在“待验证注脚”区。
4. **保留分歧**：冲突观点不合并、不平均、不删；留分支给校验器。
5. **人工覆盖优先**：用户显式要求接受低增量版本时，可以接受，但要在 changelog 中写 `override: user`，并触发强制收益评估。

## 反模式速查

| 反模式 | 处理 |
|---|---|
| 把“改写得更顺”当迭代 | 不算有效新增；触发收益不足则回退 |
| 用单一来源塞满新章节 | 标为脚注/单源-存疑，不计有效新增 |
| 拒绝时仍偷偷留下部分新内容 | 不允许；必须整体回退 |
| 只给增删，不说明为什么 | 不是合格迭代器；补 changelog |
| 一有冲突就选一个“看起来更合理” | 保留分支，交给校验/用户裁决 |

## 简单用户话术

> 我每一次迭代都会先数“有效新增知识节点”：只有能变成可执行规则、且有验证来源的才算数。如果新版只是换说法，或者新增的全是单源存疑内容，我会拒绝更新、退回旧版，并告诉你收益不足。每次都会给你一份变更日志，谁加的、加在哪、证据是什么，都能查。
