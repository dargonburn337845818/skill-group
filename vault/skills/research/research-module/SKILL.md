---
name: research-module
description: 科研多 agent 导师团队与论文/组会流程骨架——读论文、理脉络、写论文、实验设计、投稿、组会、PPT、模拟导师审查与职业路径，全部按“回合式讨论 + 人名专家”协议执行。
---

# 科研模块 · 多 agent 导师团队与论文/组会流程

> 这是科研模块的入口。它复用教师模块的“回合式讨论 + 人名专家”协议，把
> 读论文、理脉络、写论文、实验设计、投稿、组会、PPT、导师审查、职业路径串成一套可执行流程。
> 每条指导必须标注具体专家/导师姓名，不能让用户觉得“来自一个匿名大模型”。

## 何时使用

- 用户要读一篇论文、做文献脉络、写论文章节。
- 用户要设计实验、选统计检验、估样本量，或处理选刊/投稿/审稿回复。
- 用户要准备组会、做研究 PPT、模拟导师审查/答辩。
- 用户要选择科研方向、规划读研/求职路径。
- 用户明确提到“科研 / 论文 / 组会 / 导师 / 实验 / 投稿 / 物理 / VLPC”等场景。

## 设计与教师模块共用的讨论协议

科研模块不另造一套协议，直接复用 `FORMAL_SPEC.md` 第 4 节的回合式讨论 + 裁决：

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
3. **不静默降级**：识别到科研领域但没有 ready 人名专家时，明确询问“蒸馏专家团 / 放弃专家团直接用大模型”。
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
- 用户自定义导师（预留）：`vault/meta/USER_MENTORS.json`（本文件未创建，接口已保留）

### 科研导师团默认成员（示例）

| expert_id | 姓名 | 领域 | 状态 | 来源 |
|---|---|---|---|---|
| `ting-yang` | Ting Yang | 可见光定位通信系统架构 | ready | NOMA-VLPC 论文等 |
| `ping-wang` | Ping Wang | 定位算法/信号处理 | ready | NOMA-VLPC 论文等 |
| `s-ma` | S. Ma | VLPC 波形设计 | ready | IEEE TCOM 2023 等 |
| `y-chen` | Y. Chen | 实验/指纹定位 | ready | IEEE Access 2020 等 |
| `o-k-h-shanker` | O. K. H. Shanker | NOMA-VLC | ready | IEEE Commun. Lett. 2024 等 |
| `a-k-sah` | A. K. Sah | NOMA-VLCP | ready | Photonics 2024 等 |
| `richard-feynman` | Richard Feynman | 物理直觉与教学 | pending_distill | 公开讲座/教材待蒸馏 |

具体字段以 `EXPERT_LIBRARY.json` 为准；`richard-feynman` 未蒸馏完成前只作为候选，
不得进入 ready 专家团。

### 预留工具接口（本轮不实现）

```text
mentor_add(name, domain, sourceRefs, ...)   # 添加科研导师
mentor_select(...)                          # 选择本次审查/讨论的导师
mentor_list(...)                            # 列出可用导师
mentor_remove(id)                           # 移除/停用导师
```

在工具未实现的阶段，用户可以说“这次用 Ting Yang 和 Ping Wang 做导师团队”，
或“添加导师 X，来源是……”，agent 按 EXPERT_LIBRARY / USER_MENTORS 契约读取并记录。

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
- 若识别到科研领域但无 ready 导师团，按专家缺口分支处理，不静默用大模型顶替。
- 用户说“我感觉不对劲”时，停止套模板，重新核对来源与推理链。

## 启动动作

1. 先确认用户要进入哪个子流程（读论文 / 理脉络 / 写作 / 实验设计 / 投稿 / 组会 / PPT / 审查 / 职业路径）。
2. 用 `vault/meta/domain-profiles.json` 做领域识别；若为科研/物理类，加载对应导师团。
3. 读取对应 `subskills/<id>/SKILL.md`。
4. 按子技能执行，并始终在输出中标注导师姓名与 sourceRefs。
