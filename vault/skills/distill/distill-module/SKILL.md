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

## 来源

- `$PROJECT_ROOT/FORMAL_SPEC.md` 第 2 节、第 4.4 节
- `$PROJECT_ROOT/vault/meta/modules.json`
- `$PROJECT_ROOT/vault/meta/domain-profiles.json`
- `$WORKSPACE/skills/core-iteration/README.md`
- `$WORKSPACE/skills/distillation-consensus-skill/SKILL.md`
