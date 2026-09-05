---
name: distill-module
description: 蒸馏模块——把 dev/teacher/research/writing 的 Gap 与领域专家缺口变成可入库 Skill/人名专家团的编排层；复用 core-iteration 六阶段，不重复造工具。
whenToUse: 需要为 dev/teacher/research/writing 补充技能内容、把模块 Gap 蒸馏成 Skill、把 pending_distill 专家蒸馏成 ready 专家团，或需要模块缺口→回填的完整协调时。
boundary: 只做编排与回填；不重新实现 core-iteration 工具；无 verified 证据不回填；语料不足不硬编；未接入真实 runner 不冒充 A/B。
---

# 蒸馏模块（distill-module）

> 定位：**编排层，不是新的蒸馏算法库。**
> 蒸馏模块接收“某模块还缺什么”，再调度 `core-iteration` 的搜索→收益过滤→蒸馏→迭代→校验→调度，
> 最后把产物回填到 `vault/meta/modules.json`（新 skill / 已落实 gap）或 `EXPERT_LIBRARY.json`（新 ready 专家）。
> 它不重新实现 core-iteration 已有的工具，只在“模块缺口”和“核心迭代能力”之间做编排与回填。

## 何时使用

- 用户说“给 dev/teacher/research/writing 补内容”“把某个 Gap 蒸馏成 Skill”“把候选专家蒸馏成 ready 专家团”。
- 领域识别器返回 `expert_gap`，用户选择 **蒸馏专家团**（`distill_expert`）。
- `vault/meta/modules.json` 中某模块的 `gaps` 有待落实条目；`domain-profiles.json` 中有 `status: pending_distill`。
- 刚完成一次蒸馏，需要把产物正式回填进模块注册表与验收状态。

## 一句话流程

```text
模块 GAP / pending_distill 专家
  → 定目标（skill 还是 expert）
  → 搜索/采集（search-source + info-source-adapter）
  → benefit-filter（收益过滤，不可跳过）
  → 蒸馏（distillation-consensus → Node / SKILL.md）
  → 迭代+校验（value-iterator / value-validator / skill-verification-consensus）
  → 真实 A/B（scaffold_eval_task → skilljack-evals / BenchFlow → Skill Lift）
  → 回填（modules.json / EXPERT_LIBRARY.json / domain-profiles.json / assignment.json）
```

## 输入契约（GapRequest）

任何一次蒸馏任务都被归一化为下面这个对象；缺字段先问，不静默编造。

```json
{
  "module_id": "dev | teacher | research | writing | distill | domain",
  "gap_id": "短横线 id，如 dev-security / expert-dan-abramov",
  "gap": "模块缺口的一句话描述",
  "target_type": "skill | expert",
  "skill_id": "期望产物 id（target_type=skill）",
  "expert_id": "期望专家 id（target_type=expert）",
  "existing_refs": ["已存在且不得重复实现的 skill/专家 id"],
  "acceptance": ["可测量的完成条件"],
  "priority": "p0 | p1 | p2",
  "source_hint": ["已知可信来源/公开资料路径（可选）"]
}
```

## 六步编排（每个动作都指向 core-iteration 已有实现）

| 步骤 | 做什么 | 复用谁 | 关键产物 |
|---|---|---|---|
| 0 定目标 | 确认是“模块子技能”还是“人名专家”；确认不会和现有 skill 重复 | 本模块 | `GapRequest` |
| 1 搜索/采集 | 拆缺口、选独立入口、保留来源台账 | `search-source` / `web-research-consensus` / `info-source-adapter` | `raw_corpus` + `source_scope_report` |
| 2 收益过滤 | 密度评分、≥2 独立来源或单源降权；`<60` 丢弃 | `benefit-filter` | `verified_high` + `yield_stats` |
| 3 蒸馏 | 只拿 verified 语料切最小推理单元，产出 Node 三件套；可一键生成 Skill 包 | `distillation-consensus` / `tools/distill_skill_package.py` | `skill_draft` / `knowledge_nodes` |
| 4 迭代与校验 | 比较新旧、强制 changelog；四硬规则 STOP/CONTINUE；发布前跑检验底座 | `value-iterator` / `value-validator` / `skill-verification-consensus` | `new_skill` + `verification_report` |
| 5 真实 A/B（可选但推荐） | 任务先行、无 skill/有 skill 对照、anti-trigger；算 Skill Lift | `tools/scaffold_eval_task.py` + `skilljack-evals/BenchFlow` + `tools/skill_effect_bench.py` | eval 任务包 + `ENHANCEMENT_REPORT` |
| 6 回填 | 更新 `modules.json`、manifest、CHANGELOG、assignment；专家则改 `EXPERT_LIBRARY.json` / `domain-profiles.json` | 本模块（写注册表） | `backfill_diff` |

> 第 2、3 步是硬闸门：**跳过 benefit-filter 的“蒸馏”不得回填；没有 verified 证据的“专家说”不得进入 Skill**。

## 专家团调用（标准化流程）

蒸馏过程中需要“多专家判断这条知识是否值得保留/是否有分歧”时，按被蒸馏语料的领域加载专家团：

1. 算法竞赛语料 → `expert_ids=["tourist","um-nik","jiangly","benq"]` 等。
2. 前端/后端/性能/安全/AI 工程语料 → 对应 dev 领域 ready 专家。
3. 写作/科研语料 → `william-zinsser` 或 `research` 导师团。
4. 元流程/技能库设计审查 → `dsh-ops` + `ai-llm-agent` 专家。
5. 走统一 `expert-team` 协议：定域 → 加载 → 独立表态 → 冲突表 → 裁决 → 署名结论；不静默降级。

## 为四个模块补内容（详见 `feed-other-modules.md`）

| 模块 | 缺的是 | 蒸馏产物落到哪 | 回填动作 |
|---|---|---|---|
| dev | 开发规范/安全/并发/性能/测试/美学/去 AI 味 | `vault/skills/dev/` 下的子 skill | `modules.json -> dev.skills` 追加 id，`dev.gaps` 标记落实 |
| teacher | 多领域人名专家、讨论协议、提问流 | `vault/meta/EXPERT_LIBRARY.json` + `vault/skills/teacher/` | 专家 `status: pending_distill -> ready`；讨论协议写进 teacher-module |
| research | 论文阅读/脉络/写作/组会/PPT/导师审查 | `vault/skills/research/` 的子 skill | `modules.json -> research.skills` 追加 id，gaps 标记落实 |
| writing | 提示词/文案/文档/报告 | `vault/skills/writing/writing-module/subskills/` | `modules.json -> writing.skills` 追加 id，gaps 标记落实 |
| domain 共享 | 领域识别后无 ready 人名专家 | `vault/meta/EXPERT_LIBRARY.json` | `domain-profiles.json` 中该领域 `status: pending_distill -> ready` |

## 专家蒸馏（原语来自 domain-profiles）

当 `scripts/domain_recognize.py` 返回：

```text
decision = "expert_gap"
candidate_experts = [ { id: "dan-abramov", status: "pending_distill", ... } ]
fallback.options = ["distill_expert", "use_llm_directly"]
```

用户选 `distill_expert` 时，按以下步骤把候选专家蒸馏成 ready 专家团（详见 `meta-iteration.md` 的专家蒸馏小节）：

1. 读取 `EXPERT_LIBRARY.json` 中该 `expert_id` 的 `sourceRefs` 与现有 `style`。
2. 以公开访谈/文档/演讲/代码/著作原文为语料，走 搜索→过滤→蒸馏 六阶段。
3. 每条风格规则必须是 `public-figure-style-reference`：`style` = 风格/方法论推断，**不是本人原话**；保留 `sourceRefs`。
4. 蒸馏成立后回填：
   - `EXPERT_LIBRARY.json`：该专家 `status: "ready"`，补全蒸馏出的 `style` 与 `sourceRefs`；
   - `domain-profiles.json`：该领域 `status: "ready"`（若该领域全部候选专家 ready）。
5. 若语料不足 3 条 verified-high，输出 `insufficient_corpus`，**不把 pending_distill 改成 ready**。

## 元能力迭代：只复用 core-iteration

- `distill-module` 不内置“搜索/过滤/蒸馏/迭代/校验”算法，不另起炉灶。
- 完整调度契约与轮次控制见 `core-iteration`（`value-meta-scheduler`）。
- 本模块只负责：把 GapRequest 翻译成 `core-iteration` 的 `input`，再把它输出的 `final_skill` 翻译成 vault 注册表回填。
- 工具调用统一指向 `$WORKSPACE/skills/core-iteration/tools/`，不在本模块下重复建同名脚本。
- 详细映射见 `meta-iteration.md`。

## 真实 A/B 评测接入方案

- 任务包：`python3 $WORKSPACE/skills/core-iteration/tools/scaffold_eval_task.py --task-id <id> --skill-name <skill> --prompt "..." --checks "contains:...,files:..."`。
- 产物是 **skilljack-evals 风格任务包**：`task.md` + `environment/skills/<skill>/` + `verifier/verify.mjs` + `oracle/solve.mjs`。
- 本地真实 runner 已接入：`core-iteration/tools/skilljack_runner.py`（DeepSeek agent 循环 + loadSkill + verifier + 可选 judge）与 `benchflow_runner.py`（矩阵 + 门禁）；已用 `dev-security` 正例/反例任务包跑出真实 Skill Lift（23.2%，门禁 PASS）。
- 外部 `skilljack-evals` CLI 仍作为备选；未配置 Anthropic/OpenAI key 时如实写“外部 runner 未接”，不得用模板分数冒充真实 A/B。完整方案与命令见 `real-ab-bench.md`。
- 完整方案与命令见 `real-ab-bench.md`。

## 输出契约（BackfillResult）

每轮蒸馏收尾必须输出可审计的回填结果：

```json
{
  "gap_id": "...",
  "target_type": "skill | expert",
  "produced": {
    "skill_id": "..." | "expert_id": "...",
    "dir": "vault/skills/<module>/<id>",
    "manifest": {"id": "...", "scenario": "..."},
    "knowledge_nodes": 0,
    "source_refs": 0,
    "verification": "pass | needs_work | reject",
    "eval": {"tasks": 0, "baseline": null, "with_skill": null, "lift": null}
  },
  "backfilled": {
    "modules_json": ["新增 skill id", "gaps 标记"],
    "expert_library": ["status -> ready"],
    "domain_profiles": ["domain status -> ready"],
    "assignment": {"id": "...", "status": "done"}
  },
  "validation": "validate-vault OK"
}
```

## 边界与反模式

| 情况 | 处理 |
|---|---|
| 只想“给一段总结”而不是可执行 Skill | 拒绝回填；补 trigger/action/boundary/source |
| 跳过 benefit-filter 直接蒸馏 | 强制回退到第 2 步 |
| verified_high 不足 3 条 | 输出 `insufficient_corpus`，不硬编 |
| 领域缺专家但用户选 `use_llm_directly` | 不进入本模块，直接用模型；不静默标记 ready |
| 已有 core-iteration 工具 | 直接调用，不复制实现 |
| 只跑 1 次就说“有增益” | 至少 3 次；否则标 `single-effect` |
| 评测通过但不等于知识正确 | 如实写“只证明该任务上有可测增益” |

## 启动动作

1. 读取 `vault/meta/modules.json`，找到缺口所在模块与 `gaps`。
2. 若来源是领域专家缺口，读取 `vault/meta/domain-profiles.json` 与 `EXPERT_LIBRARY.json`。
3. 读取本模块三个配套文档：
   - `feed-other-modules.md`：模块缺口 → 新 skill/专家 → 回填
   - `meta-iteration.md`：复用 core-iteration 的调用方式
   - `real-ab-bench.md`：真实 A/B 接入方案
4. 按 `examples/distill_task.md` 的样例把本次任务归一化，再进入六步编排。
5. 完成后运行 `node scripts/validate-vault.mjs`，并更新本地 `assignments/distill/assignment.json`（内部开发记录，未随公开仓库发布）。

## 2026 深度补强（Round 38）

> 本轮针对编排层最易翻车的六个场景补强可执行规则：**来源独立性、缺口去重、专家证据分级、评测卫生、回填事务、审计轨迹**。不改变既有流程，每条都带反例与来源。

### R38-1 来源台账：先证明“这是独立来源”，再算证据数

- 每条 `raw_corpus` 条目必须记录六元组：`canonical_url` / `title` / `publisher` / `publication_date` / `access_date` / `evidence_class`；无法补全 `access_date` 的来源按 `verify-needed` 处理，不标 `verified`。
- 同文转载、镜像站、聚合页只算 **1 个来源**；独立来源 = 不同出版方/作者的一手或二手材料，不是同一篇文章的 N 个 URL。
- 链接失效时用 `web.archive.org` 快照回溯，并在台账记录快照日期；没有亲自打开过的 URL 不得进入 `verified_high`。
- 反例：3 个博客都在转述同一篇官方文章，不能算 3 条独立证据；更多独立来源要点见 [CRAAP Test](https://open.oregonstate.education/goodargument/chapter/craap-test/)。

### R38-2 缺口去重/重叠闸门：先判“该新建还是该扩展”

- 蒸馏前对 `existing_refs` 与目标模块已有 skill 做语义重叠扫描（关键词层、节点层、条目层三层都要看）。
- 重叠 >60%：不新建 skill，把缺口标记为“已覆盖/并入 <skill-id>”；重叠 30–60%：只蒸馏“增量节点”，并在产出中写明“本产物不包含已有内容”。
- 新 skill 的 `description` 必须能一句话区分于同模块所有 skill；区分不出来 = 重复。
- 反例：已有 `dev-security` 再建 `dev-secure-config`，两者检查清单几乎相同；Skill 边界与格式参考 [OpenAI · Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) 与 [OWASP Universal Skill Format](https://owasp.org/www-project-agentic-skills-top-10/universal-skill-format.html)。

### R38-3 专家蒸馏证据分级：Tier A/B/C，别用聚合语录升级 ready

- `public-figure-style-reference` 证据分三档：
  - **Tier A**：本人官方文档/著作/亲手维护代码仓库/亲自主讲演讲与逐字稿/个人博客原文；
  - **Tier B**：主流媒体专访、正式访谈出版物、同行学术分析；
  - **Tier C**：聚合语录、二手转述、SEO 文章、单一博客转载。
- 每条 style rule 至少需要 **1 条 Tier A 或 2 条互相独立的 Tier B**；Tier C 只能做旁证，不能单独支撑 `status: ready`。
- 输出必须写 `inferred`（风格/方法论推断），不得写成“他说过……”；保留原文链接与访问日期。
- 反例：用某个“10 条名言”聚合页作为唯一来源，把 `pending_distill` 改成 `ready`。来源判断见 [CRAAP Test](https://open.oregonstate.education/goodargument/chapter/craap-test/) 与 [Where did this come from?](https://ouci.dntb.gov.ua/en/works/4KQLJBq9/)。

### R38-4 评测卫生：防泄漏、防恒过、防单次运气

- 任务 prompt 不得包含被测 skill 名称/关键词/示例路径；一旦出现即视为 leakage，需重建任务，不能“先跑再说”。参考 [OpenAI Evaluation Best Practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) 与 [Anthropic Demystifying Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)。
- 无 skill 基线必须能失败：`no-skill success == 100%` 时先修 verifier/任务难度，不计为有效评测（环境与任务设计要点见 [LangChain: How We Build Agent Environments & Tasks](https://www.langchain.com/blog/building-agent-environments-and-tasks)）。
- anti-trigger 误触发率必须低于配置阈值（默认 ≤0.5）；即使正例 Skill Lift 很高，误触发超标也禁止回填。
- 每次 A/B 必须在台账记录：模型、temperature、seed、日期、每 run 原始结果；<3 runs 只能标 `single-effect`，不得写“有增益”。
- 反例：用同一个任务既调 skill 又做发版评测，或只挑最好的一次 run 写进 `ENHANCEMENT_REPORT`。

### R38-5 回填事务化：一个 gap 一个 diff，验证不过就整体回滚

- 回填 = 发布动作，必须一个 gap 对应一个可审查 diff：`modules.json` + 新 skill 目录 + `manifest.json` + `CHANGELOG.md` + `SOURCES.md`（专家时另含 `EXPERT_LIBRARY.json` / `domain-profiles.json`）同批更新。
- 更新后必须跑 `node scripts/validate-vault.mjs`；失败则**整体回滚本次 diff**，不得留下“模块已登记但目录/manifest 缺失”的半成品。
- 新 skill 的 manifest 字段必须与同模块兄弟 skill 一致（id/scenario/version/sourceRefs/qualityCriteria 等）；缺字段先补模板再登记，格式对齐参考 [OWASP Universal Skill Format v1.0](https://owasp.org/www-project-agentic-skills-top-10/universal-skill-format.html)。
- 反例：只把 skill id 塞进 `modules.json`，忘记写 manifest；validation 失败后仍宣称“已回填”。

### R38-6 审计轨迹：负结果也落盘，缺字段按“未验证”处理

- 每轮结束写 `round_ledger.json` / 证据台账：命令与工具路径、输入/输出摘要、verified 数量、decision（continue / stop / insufficient_corpus / blocked）、来源数、评测数。可复现性要点参考 [What Do ML Researchers Mean by Reproducible?](https://ar5iv.labs.arxiv.org/html/2412.03854)。
- `BackfillResult` 中 `verification` / `eval` / `validation` 缺省或 null = **未验证**，不得显示为“已完成”；`insufficient_corpus` 也要写进台账，避免下轮重复搜索同一条死路。评测污染与基线设计可参考 [MMLU-CF: A Contamination-free Benchmark](https://ar5iv.labs.arxiv.org/html/2412.15194)。
- 外部 runner 未配置 key 时，台账同时写 `external_runner: "not_configured"` 与 `local_runner: "ran"`；不得写“已接入外部 skilljack-evals”。
- 反例：结论写“A/B 已接入”，但结果文件只有一张空表格。

### Round 38 新增检查清单

- [ ] 每个来源有 `canonical_url + access_date + publisher`，同文转载未重复计数
- [ ] 重叠扫描完成，结论是“新建 / 扩展 / 已覆盖”，不是重复 skill
- [ ] 专家规则有 Tier A/B 证据且标注 `inferred`，无聚合语录单源升级
- [ ] eval prompt 无泄漏；基线可失败；anti-trigger 达标；≥3 runs
- [ ] 一个 gap 一个 diff；`validate-vault.mjs` OK；失败已整体回滚
- [ ] `BackfillResult` 无空字段；负结果也写入 `round_ledger`

## 来源

- `$PROJECT_ROOT/FORMAL_SPEC.md` 第 2 节、第 4.4 节
- `$PROJECT_ROOT/vault/meta/modules.json`
- `$PROJECT_ROOT/vault/meta/domain-profiles.json`
- `$WORKSPACE/skills/core-iteration/README.md`
- `$WORKSPACE/skills/distillation-consensus-skill/SKILL.md`
