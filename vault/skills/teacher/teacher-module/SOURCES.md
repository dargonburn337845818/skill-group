# 教师模块 · 来源与证据

本技能不是凭空发明协议，而是把正式规格 + 既有教师共识固化成一个可执行模块。

## 主要来源

| 来源 | 用途 |
|---|---|
| `FORMAL_SPEC.md` §4 | 专家团、回合式讨论、冲突点表、裁决、命名规范 |
| `FORMAL_SPEC.md` §4.4 | 领域识别与专家缺口：不静默降级 |
| `vault/meta/EXPERT_LIBRARY.json` | 人名专家库 source of truth |
| `vault/meta/domain-profiles.json` | 领域字典 + expert_ids + fallback 文案 |
| `$WORKSPACE/skills/teacher-consensus-skill/output/teacher_consensus_final.json` | 算法竞赛多专家共识材料 |
| `$WORKSPACE/skills/teacher-consensus-skill/content/expert_research.md` | 顶尖选手方法论的公开来源汇编 |
| `vault/skills/teaching/teacher-consensus/` | 既有算法竞赛教师共识 |

## 专家条目证据纪律

- 所有 `status=ready` 专家必须：
  - 是真实公开人物；
  - `persona_type=public-figure-style-reference`；
  - `sourceRefs` 非空且可回溯；
  - `style` 明确写为“风格/方法论推断”，不是本人原话。
- 未满足上述条件的专家保持 `pending_distill`，不进入默认专家团。

## 相关文档

- `SKILL.md` — 对外入口与执行流程。
- `discussion-protocol.md` — 回合式讨论协议与 JSON 契约。
- `expert-selection.md` — 专家选择/添加/缺口处理。
- `examples/round_discussion.md` — 完整示例。
