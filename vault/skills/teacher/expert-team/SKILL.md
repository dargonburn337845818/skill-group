---
name: expert-team
description: 任意模块通用的人名专家团标准化流程——领域识别、加载 ready 专家、回合式表态、冲突裁决、署名结论；dev/writing/teacher/research/distill 均可复用。
whenToUse: 开发、文稿、教师、科研、蒸馏等模块需要多位真实公开人物风格参考来评审方案、拆解问题、生成署名意见、保留分歧时。
---

# 专家团标准化流程（Expert Team Protocol）

> 目标：让“专家团”不再是 teacher 模块私有能力，而是 dev / writing / teacher / research / distill 共用的标准流程。
> 数据源：`vault/meta/EXPERT_LIBRARY.json`（人名专家库）+ `vault/meta/domain-profiles.json`（领域字典）。
## 触发条件

- 任何模块（dev/writing/teacher/research/distill）需要“多位真实公开人物风格参考”时。
- 需要对方案/产物做多视角评审、拆解、纠偏、分歧裁决时。
- 需要把“某专家怎么看”写成带署名的结论并保留来源时。

> 运行时：直接复用 `teacher_discussion_start / teacher_discussion_round / teacher_expert_select / teacher_discussion_status` 等工具与 `/skill-vault/api/teacher/*` HTTP 接口。

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

## 来源

- `vault/meta/EXPERT_LIBRARY.json`
- `vault/meta/domain-profiles.json`
- `vault/skills/teacher/teacher-module/discussion-protocol.md`
- `vault/skills/teacher/teacher-module/expert-selection.md`
- `vault/skills/research/research-module/SKILL.md`（科研复用示例）
