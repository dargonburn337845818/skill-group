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

## 2026 深度补强（Round 36）

> 本轮只补“开发模块壳如何定域、划界、挂底座、验收”的可执行规则；不重复 `search-source` / `dev-workflow-consensus` / `skill-verification-consensus` 正文。括号内为 `SOURCES.md` 的 Round 36 来源编号。

### 1. 定域公式：产物 → 主域 → 顾问

**Step 1 按交付产物分类，不按关键词分类。**

- 代码行为/逻辑 → dev-backend / dev-frontend（按领域）
- 界面/视觉/文案 → dev-design-aesthetics（或 dev-art-ppt）
- 安全/隐私 → dev-security
- 并发/锁/异步 → dev-concurrency
- 性能/资源 → dev-performance
- 测试与验证 → dev-testing
- 部署/CI/CD/可观测性 → dev-ops-sre
- 网络/访问/排障 → dev-network
- 系统设计/模块化/分布式 → dev-architecture
- LLM/Agent 工程 → dev-ai-engineering
- 去 AI 味 → dev-remove-ai-flavor

（R36-12：SWEBOK 按知识域划分；R36-05：Routing 把输入分类并交给专门后续任务）

**Step 2 复杂度分档**（R36-05、R36-08）：

- 简单/常见/低影响：直接进子技能，最小底座。
- 复杂/罕见/高影响/不可逆：必挂完整底座 + 专家团 + 多轮验证。

**Step 3 只允许一个主域拥有最终输出**；其余子域只能二选一：

- **顾问（agent-as-tool / bounded subtask）**：只回答受限子问题、不改主域文件、不接管最终交付。
- **交接（handoff）**：后续整段交付由对方负责，是一次性的控制权转移。

（R36-06：manager 用 agents-as-tools，triage 用 handoffs；R36-07：一个目标一个 handoff）

### 2. 路由健康检查清单（每次定域后 30 秒检查）

- [ ] 主域唯一，且路径存在：`vault/skills/dev/subskills/<id>/SKILL.md`
- [ ] 顾问域不超过需要，且只读对应 SKILL.md，不写跨域实现
- [ ] 子技能状态是“已蒸馏/已填充”而非“待蒸馏”；“待验证”必须显式标注（不可写“已验证”）
- [ ] 描述/触发词是否过宽或过窄：过宽会导致误触发，过窄会导致多技能同载（R36-02、R36-03）
- [ ] 若路由失败（主域无输出/不确定），回退到模块壳重新定域、使用底座兜底或上报 gap，不静默继续（R36-08）
- [ ] 未命中任何子技能 → 进 `distill-module` 补缺口，不临时在壳内实现

### 3. 模块边界四规则（把 Clean/Hexagonal 本地化）

1. **端口即边界**：跨子技能/子技能与壳之间只通过公开 SKILL.md、清单、调用路径交互；不共享内部变量/私有文件（R36-10）。
2. **依赖只向内**：子技能不得反向引用壳或其他子技能的内部实现；壳只路由与装配底座，不实现业务（R36-11）。
3. **外层不向内漏**：框架/DSH/外部数据格式不得泄漏进领域规则；跨边界传输的数据形态以“内层方便的形态”为准（R36-11）。
4. **一个子技能=一个连贯任务单元**：过窄会迫使多个技能同时加载/相互冲突，过宽会难触发；若出现“数据库查询 + 数据库管理”式合并，拆开（R36-02）。

### 4. 底座调用契约（三件套何时必挂）

- **必须挂**：复用型/将入库/被多个会话或脚本调用/构成新模块。
  1. `search-source` → `source_scope_report`
  2. `dev-workflow-consensus` → L1/L2 spec（spec/accept/do/verify）
  3. `skill-verification-consensus` → 校验报告（claim/class/proof/checks_observed_red）
- **可豁免**：一次性小脚本、只读问答、临时验证；一旦“会留下文件/再次被调用”立即升级。
- “我早就知道/这是常识”不构成跳过搜索的理由；无来源规则不得进正文。

### 5. 验收门禁四道

1. **规格门**：模块地图 + 公开接口 + L1/L2 accept 存在。
2. **审查门**：对抗审查 BLOCKER 清零（或 “none found” + 六项检查）。
3. **可证伪门**：机械检查必须“故意破坏→变红→恢复→变绿”，无 `checks_observed_red` 只能写“已运行”。
4. **终验门**：测试/冒烟真实通过 + 证据可回溯 + 无未处理边界；若在 CI 中，落成 stage/job 由机器把关（R36-09、R36-04）。
- DoD 必须是显式契约、团队/会话可见；否则容易变成“大家都觉得做完了”（R36-09）。
- 机械断言用脚本/代码判定，不交给 LLM 主观裁定；LLM 只做语义诊断（R36-04）。

### 6. 反例（不要这样做）

- ❌ “改前端样式”直接只读 dev-frontend，漏掉 ui-aesthetics-design → 应把美学作为顾问嵌入，或先转美学子技能。
- ❌ 一个任务同时加载 5 个子技能并列“并行执行” → 无唯一 owner，上下文污染；应一次一个主域 + 受限顾问。
- ❌ 路由失败后继续输出猜测 → 应 fallback 到底座或上报 gap。
- ❌ “跑通了”就写“已验证” → 没做突变测试只能写“已运行，未验证”。
- ❌ 把“首版蒸馏”说成“已通过 A/B” → 必须标“待验证”。
- ❌ 在模块壳里写业务逻辑/修改子技能内部文件 → 违反端口与依赖向内。
- ❌ 为省事把多个相邻子技能合并成一个超集 → 触发变宽、冲突变多（R36-02）。

### 7. 例行自检（Round 36）

- [ ] 定域三问已答（产物/主域/顾问或交接）
- [ ] 子技能状态与清单一致，待验证已标注
- [ ] 底座三件套在需要时已产出
- [ ] 四道门有记录或明确豁免
- [ ] 新规则有来源、有反例、不重复底座

## 来源

- `FORMAL_SPEC.md` §2/§5/§7：模块定义、Assignment、新会话开工。
- 本模块任务分派：`assignments/dev/assignment.md`（内部开发记录，未随公开仓库发布）。
- `vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`、`vault/skills/core-iteration/dev-workflow-consensus/`：隐藏底座。
- `vault/skills/distillation/ui-aesthetics-design/`：UI 美学已填充来源。
- `vault/skills/dev/subskills/*/SKILL.md`：十三个子技能正文（dev-frontend / dev-backend / dev-art-ppt / dev-security / dev-concurrency / dev-performance / dev-testing / dev-design-aesthetics / dev-remove-ai-flavor / dev-ops-sre / dev-ai-engineering / dev-architecture / dev-network）。
