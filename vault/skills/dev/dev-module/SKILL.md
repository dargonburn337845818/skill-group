---
name: dev-module
description: 开发模块壳——dev 模式入口，挂载隐藏底座与十三个已蒸馏/已挂载子技能；提供子技能清单与调用路径，不重复底座内容。
whenToUse: 用户任务进入“开发”模块（编码、重构、前端/后端、安全、并发/性能、测试、设计美学、去 AI 味、部署/CI/CD/可观测性、系统设计/分布式、LLM/Agent 工程）时，先加载本模块壳，再按需进入子技能。
---

# 开发模块壳（Dev Module Shell）

> 定位：正式版五模块之一“开发”的入口。本文件是模块壳，不重复隐藏底座内容，不实现业务功能。
> 状态：模块壳已就绪；十三个子技能已完成首版蒸馏（其中 dev-design-aesthetics 挂载 ui-aesthetics-design；dev-network 为网络排障子技能）。

## 触发条件

- 用户任务属于开发域：写代码、重构、模块化、插件开发、前端/后端、美术/PPT、安全、并发、性能、测试、设计美学、去 AI 味、部署/CI/CD/可观测性、系统设计/分布式、LLM/Agent 工程、网络排障/网络访问。
- 需要从 dev 模式进入具体子技能，或需要判断该调用哪个开发子技能。
- 需要给开发任务挂上隐藏底座：先检索、再按强流程开发、最后做可证伪校验。

## 核心动作

1. **定域**：判断用户任务落在哪个子技能（见下表），直接读取对应 SKILL.md。
2. **挂底座**：按需调用隐藏底座——`search-source`（查资料/来源）、`dev-workflow-consensus`（Frame→Spec→Gate→Verify）、`skill-verification-consensus`（发布前校验）。
3. **执行或补蒸馏**：已蒸馏子技能直接按正文执行；若仍有新缺口，按子技能内“待蒸馏/补缺口”占位继续走 distill 流程，不假装已完成。

## 子技能清单

| id | 状态 | 路径 |
|---|---|---|
| dev-frontend | 已蒸馏 | `vault/skills/dev/subskills/dev-frontend/` |
| dev-backend | 已蒸馏 | `vault/skills/dev/subskills/dev-backend/` |
| dev-art-ppt | 已蒸馏 | `vault/skills/dev/subskills/dev-art-ppt/` |
| dev-security | 已蒸馏 | `vault/skills/dev/subskills/dev-security/` |
| dev-concurrency | 已蒸馏 | `vault/skills/dev/subskills/dev-concurrency/` |
| dev-performance | 已蒸馏 | `vault/skills/dev/subskills/dev-performance/` |
| dev-testing | 已蒸馏 | `vault/skills/dev/subskills/dev-testing/` |
| dev-design-aesthetics | 已填充（挂载 ui-aesthetics-design） | `vault/skills/dev/subskills/dev-design-aesthetics/` |
| dev-remove-ai-flavor | 已蒸馏 | `vault/skills/dev/subskills/dev-remove-ai-flavor/` |
| dev-ops-sre | 已蒸馏 | `vault/skills/dev/subskills/dev-ops-sre/` |
| dev-ai-engineering | 已蒸馏 | `vault/skills/dev/subskills/dev-ai-engineering/` |
| dev-architecture | 已蒸馏 | `vault/skills/dev/subskills/dev-architecture/` |
| dev-network | 已蒸馏 | `vault/skills/dev/subskills/dev-network/` |

## 专家团调用（标准化流程）

开发模块需要多人名专家视角评审架构/安全/性能/前端/后端/运维/AI 工程时，直接复用 `teacher` 场景的 `expert-team` 标准协议，不另造流程：

1. 按任务域通过 `expert_team_start(text=...)` 或 `domain_id` 加载默认专家团（frontend/backend/security/performance/devops/ai-llm-agent/data-science/product-ux/dsh-ops 均已 ready）。
2. 例：后端架构评审 → `expert_team_start(text="后端架构评审", expert_ids=["martin-fowler"])`；前端框架取舍 → `expert_ids=["evan-you","rich-harris","dan-abramov"]`。
3. 输出必须带 `expert_id` / `expert_name`，保留分歧与 sourceRefs；无 ready 专家走 `expert_gap`，不静默用大模型顶替。

## 隐藏底座调用路径

- 搜索：`vault/skills/base/search-source/`
- 检验：`vault/skills/core-iteration/skill-verification-consensus/`
- 开发规范：`vault/skills/core-iteration/dev-workflow-consensus/`
- 已填充美学：`vault/skills/distillation/ui-aesthetics-design/`
- PPT/演示生产：`$WORKSPACE/ai-ppt-skill/`

## 边界 / 反例

- 本模块不重复底座内容；不把 `search-source` / `dev-workflow-consensus` / `skill-verification-consensus` 的规则再抄一遍。
- 子技能是首版蒸馏，不替代真实 A/B 评测；本地 runner 已接入（skilljack_runner/benchflow_runner），未实际跑过 A/B 的子技能仍需在证据中标注“待验证”；新增的 dev-ops-sre / dev-ai-engineering / dev-architecture 同样遵守此原则。
- 子技能间边界以各自 SKILL.md 的“与相邻子技能边界”为准；模块壳不重复 backend/concurrency/performance/testing/security 与新子技能之间的划界。
- 不把“首版蒸馏”宣称成“已通过真实 A/B”；也无来源的规则不得进入正文。
- DSH/插件热更、重启、子代理调度先读 `dsh-optimization-consensus`，不在此模块内处理。
- 简单一次性小脚本不必走完整开发强流程；长期复用的模块才需要 L1/L2 规格与测试。

## 来源

- `FORMAL_SPEC.md` §2/§5/§7：模块定义、Assignment、新会话开工。
- 本模块任务分派：`assignments/dev/assignment.md`（内部开发记录，未随公开仓库发布）。
- `vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`、`vault/skills/core-iteration/dev-workflow-consensus/`：隐藏底座。
- `vault/skills/distillation/ui-aesthetics-design/`：UI 美学已填充来源。
- `vault/skills/dev/subskills/*/SKILL.md`：十三个子技能正文（dev-frontend / dev-backend / dev-art-ppt / dev-security / dev-concurrency / dev-performance / dev-testing / dev-design-aesthetics / dev-remove-ai-flavor / dev-ops-sre / dev-ai-engineering / dev-architecture / dev-network）。
