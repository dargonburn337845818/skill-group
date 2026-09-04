---
name: value-meta-scheduler
description: 核心迭代元能力——整合“信息搜集→收益计算/过滤→蒸馏→迭代器→决策器→调度器”的价值驱动递归提升引擎；按收益曲线自动/受控迭代，输出最终 Skill、收敛报告、收益曲线与被丢弃语料清单。
whenToUse: 需要把搜索料、外部反馈或已有草案递归提升为可收敛的 Skill；需要多轮认知收益迭代、收敛判定、收益审计时。
---

# 核心迭代元能力（Core Iteration Meta-Capability）

> 定位：本模块是「认知收益架构」的总入口，也是调度器本体。它不自己生产知识，而是把六个原子能力组织成一条可递归、可量化、可收敛的工业流水线：
>
> ```text
> 信息搜集 → 收益计算/过滤 → 蒸馏 → 迭代器 → 决策器 → 调度收尾
> ```
>
> 最高优先级：核心能力自动迭代至收敛；除此之外的 Skill 默认只跑指定轮数，是否续轮交给用户决定。

## 模块地图（六合一）

| # | 角色 | 原子技能 | 核心职责 | 关键产物 |
|---|---|---|---|---|
| 1 | 信息搜集 | `web-research-consensus` | 拆问题、精准检索、来源核验、产出知识缺口 | `raw_corpus`, `knowledge_gaps` |
| 2 | 收益计算 | `benefit-filter` | 信息密度评分、多源交叉验证、收益统计 | `verified_high`, `pending_verification`, `discarded_low_density`, `yield_stats` |
| 3 | 蒸馏 | `distillation-consensus` | 把已验证高优语料编成可执行 Skill | `skill_draft` / `new_skill` |
| 4 | 迭代器 | `value-iterator` | 比较新旧知识节点，接受或回退，强制变更日志 | `new_skill`, `changelog`, `effective_new_count` |
| 5 | 决策器 | `value-validator` | 四条硬规则判定 STOP / CONTINUE | `decision`, `triggered_rules`, `forced_review` |
| 6 | 调度器 | 本 skill 自身 | 轮次控制、递归防护、收益曲线、最终报告 | `convergence_report`, `yield_curve`, `final_skill` |

> 使用前：确认上述原子技能已启用且可由 `skill` 工具加载；若某个未出现在 `available_skills`，先启用对应 vault skill，或直接读取其 `SKILL.md` 后再继续。

## 扩展元能力（可选反馈回路）

除了六个核心阶段，以下扩展能力用于让工具链“可执行、可检验、可解释”：

| 扩展 | 作用 | 何时接入 |
|---|---|---|
| `info-source-adapter` | 把 GitHub/OSV/包生态/学术等源变成可调用适配器 | 需要真实多源抓取时，第 1 步前执行 |
| `value-effect-audit` | 用真实任务效果 + 多方证据计算信息价值 | 有真实使用/回测数据时，第 5 步后执行 |
| `return-forensics` | 收益下降根因分析 + 思维链 | 边际收益下滑 / forced_review / 意外 STOP 时 |
| `inspiration-miner` | GitHub 灵感工厂：挖掘插件/skill/元能力新思路 | 需要外部灵感、新方向、递归升级突破口时 |
| `skill-verification-consensus` | 检验底座：证据分类、可证伪、Skill TDD、红队 | 蒸馏/迭代后、发布前跑校验报告 |
| `dev-workflow-consensus` | 开发底座：规格先行、对抗审查、证据化验证 | 需要开发/重构实现而非认知蒸馏时 |

- `info-source-adapter` 产出的 `source_scope_report` 会增强 `web-research-consensus` 的 `search_meta`，用于判断“是否真的打开了新缺口”。
- `value-effect-audit` 的 `feedback_to_iterator` 会改变节点权重：promote / demote / delete / needs_evidence。
- `return-forensics` 的 `trace_chains` 会进入最终报告，作为“来源→验证→蒸馏→应用→效果”的可审计思维链。
- `skill-verification-consensus` 的输出（claims/checks_observed_red/evals/adversarial_review）作为发布门槛，不通过不得宣告交付。

## 触发条件

- 用户要求“递归提升某个核心能力 Skill”。
- 用户要求“把这堆搜索料加工成可收敛的 Skill”。
- 用户要求“给出收益曲线、轮次、边际效应、提升点”。
- 已有核心 Skill 草案，需要调度多轮搜索 / 过滤 / 蒸馏 / 迭代 / 校验。
- 其他 Skill 需要受控训练时（默认只跑指定轮数，不自动续）。

## 输入约定

```text
input = {
  topic: "要迭代成 Skill 的主题",           # 或 skill_name
  target_skills?: [ skill_name, ... ],      # 批量模式：一次调度多个 Skill（如 core-iteration 六件套）
  core: true | false,                      # true=核心能力，自动迭代至收敛；false=普通 Skill，受控轮次
  max_depth: 5,                            # 递归防护，最大 5 层
  max_rounds: <用户指定>?,                  # 普通 Skill 默认 1；核心能力默认由收敛条件决定
  initial_draft?: Skill,                   # 已有草案
  feedback?: string,                       # 用户/专家/测试反馈
  search_config?: {...},                   # 传给信息搜集（含 source_types/min_independent_sources）
  info_scope?: ["web", "github", "package_registry", "academic", "oss_community"],
  info_depth?: "quick" | "balanced" | "deep",
  state_path?: "round_ledger.json",        # 状态持久化；下一轮从该文件恢复
  user_override?: "continue" | "stop"
}
```

- 若同时传入 `target_skills`，则对每个 skill 分别维护 `round`、`yield_curve`、`final_skill`，并在总报告中给出汇总表。
- `round_ledger.json` 记录：`{ "round": n, "target_skills": { skill: { version, last_round, cumulative_nodes } }, "updated_at" }`。

## 信息获取范围与平衡策略

在保证“深度”和“可信度”的前提下扩大“广度”：

### 默认信息范围

```text
info_scope = ["web", "github", "package_registry", "academic", "oss_community"]
```

- `web`：一般网页、新闻、文档、博客（只作线索）
- `github`：仓库、源码、commit/PR/issue、release、topics、security advisories（一手为主）
- `package_registry`：npm / PyPI / Maven / crates.io / Go proxy 等生态元数据
- `academic`：论文、预印本、会议、学术数据库
- `oss_community`：RFC、邮件列表、Landscape、awesome/Curated lists、下游实际使用

### 策略选择

| info_depth | 广度 | 深度 | 可信度要求 |
|---|---|---|---|
| `quick` | 1–2 个入口 | 只看摘要/README | 只用作线索，不写死结论 |
| `balanced` | 3–5 个入口 | 读一手来源 + 至少 1 个独立旁证 | 共识结论需 verified-high |
| `deep` | 5+ 个入口 | 读源码/commit/issue + 跨生态交叉验证 | 只允许 verified-high 进核心规则 |

- 增加广度不是简单堆入口；新增入口必须能带来**新的独立视角**（不同生态、不同维护者、不同数据库），否则只是噪声。
- 增加深度前先问：这个结论将来会不会改变 agent 行为？不会就不必深挖。
- 可信度底线：GitHub stars/forks、awesome 收录、README 宣传都不算证据；必须可回溯到源码/commit/release/安全公告或独立旁证。
- `search_config.source_types` 会把 `info_scope` 传给 `web-research-consensus`；`min_independent_sources` 默认 2（deep 时 3）。

## 统一工作流（每轮）

```text
第 0 步  初始化调度上下文
          → round = 1, depth = 0, cumulative_effective_nodes = 0
          → old_skill = initial_draft ?? 空 Skill
          → 创建收益曲线表

第 1 步  调用【信息搜集】（web-research-consensus）
          → 拆问题 → 精准检索 → 来源核验
          → 输出 raw_corpus + 知识缺口清单 knowledge_gaps

第 2 步  强制调用【收益计算/过滤】（benefit-filter）
          → 信息密度评分（<60 丢弃）
          → 交叉验证（≥2 独立来源 / 单源逻辑自洽）
          → 输出：verified_high + pending_verification + discarded_low_density + yield_stats
          → 禁止跳过本步；禁止未过滤语料直接进入蒸馏

第 3 步  仅携带 verified_high / verified-single 调用【蒸馏】（distillation-consensus）
          → 生成初版 Skill；若已有 draft，则作为下一轮合并基础
          → 单源 verified-single 只允许作为低权重注脚进入

第 4 步  调用【迭代器】（value-iterator）
          → 输入当前 Skill + 本轮 verified 语料 + 外部反馈
          → 若返回“收益不足，拒绝更新”：直接跳到第 7 步收尾（不调用决策器）

第 5 步  调用【决策器】（value-validator）
          → 输入旧版/新版 + 知识缺口清单 + 本轮收益统计
          → 输出 STOP / CONTINUE + triggered_rules + forced_review

第 6 步  调度器更新收益曲线
          → 记录：本轮原始语料数、高优命中数、丢弃低质数、有效新增节点、边际收益、累计节点
          → 执行自适应停止判断（见下）

第 7 步  判断收尾：
          → 若决策器输出 CONTINUE，且仍有未处理的 verified-high 语料，且未触发硬停止：
              回到第 1 步（round+1, depth+1）
          → 否则输出：
              最终 Skill
              收敛报告
              收益曲线表
              “本轮被丢弃的低质语料清单”
              “待验证清单”
```

### 每轮必须遵守的闸门

1. **过滤器不可跳过**：任何轮次都必须经过收益计算/过滤；禁止“为省事直接蒸馏”。
2. **只有 verified 类进入蒸馏**：`single-doubt` 只能进待验证清单/注脚，不能成为核心知识点。
3. **迭代器拒绝时不得继续**：收到“收益不足，拒绝更新”后，直接收尾，不再调用决策器。
4. **决策器 STOP 即收尾**：四条硬规则任一触发即 STOP，不允许“但我觉得还能继续”的软绕过。
5. **最大深度 5**：递归防护是硬上限，不得因“感觉还有希望”突破。
6. **收益曲线必须可见**：每轮记录，收尾时输出完整曲线表，不许只给“收敛了”结论。

## 递归防护

```text
if depth >= max_depth (默认 5):
    → 强制停止递归
    → 保留当前最优版本
    → 在收敛报告中标注 "max_depth_reached"
```

## 自适应停止（收益曲线驱动）

### 硬停止

- 校验器四条硬规则任一触发 → STOP。
- 迭代器返回“收益不足，拒绝更新” → 不进入校验，直接收尾。
- 递归深度达到 5 → STOP。
- 用户发出 `user_override: "stop"` → STOP。

### 软停止 / 强制收益评估

- 连续两轮 `effective_new_nodes < 3` → 触发强制收益评估：调度器不得自动继续，必须把收益曲线交给用户决定。
- 单轮 `effective_new_nodes = 0` 且 `verified_high_remaining_ratio < 0.10` → 直接判断为收益枯竭，建议收尾。
- 若 `discarded_low_quality / raw_corpus` 连续两轮 > 80%，且有效新增节点 < 2 → 过滤可能过严或搜索源质量差，调度器应先报告“过滤器是否过于严苛”，再决定是否继续。

### 收益曲线参考表（调度器每轮必须更新）

```text
| 轮次 | 原始语料数 | 高优命中数 | 丢弃低质数 | 有效新增节点 | 边际收益 | 累计节点 | 停止原因 |
|------|-----------|-----------|-----------|-------------|---------|---------|---------|
| 1    | ...       | ...       | ...       | ...         | ...     | ...     | ...     |
| 2    | ...       | ...       | ...       | ...         | ...     | ...     | ...     |
```

```text
边际收益(marginal_yield) = 本轮有效新增节点数 / max(1, 本轮处理的高优语料数)
边际效应趋势 = 本轮边际收益 - 上一轮边际收益
提升点 = 本轮新增节点所对应的缺口 id / 具体能力维度
```

## Skill 能力评分卡（量化提升）

每次收尾必须输出每个 skill 的 5 维评分。每维 0–4，总分 20：

| 维度 | 0 分 | 2 分 | 4 分 |
|---|---|---|---|
| 定位/触发 | 无触发说明 | 有触发但模糊 | 触发明确 + whenToUse |
| 可执行步骤 | 无动作 | 有步骤但不可检查 | 有可检查步骤/检查表 |
| 边界/反例 | 无边界 | 有边界但不系统 | 有反例/边界/反模式表 |
| 来源/可追溯 | 无来源 | 有部分来源 | 全部规则可回溯 |
| 接口/集成 | 无输入输出 | 有部分契约 | 与上下游字段对齐 + 干跑 |

```text
capability_gain = round_total - round0_total
improvement_delta = {
  per_skill: { "skill": {"round0": 12, "round1": 15, "delta": 3} },
  total_gain: n
}
```

评分规则：每轮由调度器按同一张表打分，避免“感觉变好了”代替量化。

## 收敛预测（预期何时停）

调度器应在报告里给出“预计还需几轮”，而不是只说“由收敛条件决定”：

```text
if 边际收益连续两轮下降 and 本轮 marginal_yield < 0.30:
    → 预计还需 1–2 轮
if marginal_yield < 0.15 or verified_high_remaining_ratio < 0.10:
    → 预计 0–1 轮（很可能本轮后 STOP）
if verified_high_remaining_ratio > 0.30 and marginal_yield 仍在上升:
    → 预计 2–3 轮
if effective_new_nodes == 0:
    → 预计 0 轮（建议立即收尾）
```

- 该预测是启发式，不是硬规则；最终以 `value-validator` 的 STOP 为准。
- 若预测与实测不符（例如预测 1 轮但连续 3 轮还有增量），要在报告中记录偏差并触发阈值校准。

## 轮次控制策略（核心 vs 非核心）

| 类型 | 默认轮次 | 自动继续 | 用户控制 |
|---|---|---|---|
| 核心能力（core=true） | 由收敛条件决定，最多 5 层 | 是，直到 STOP/收敛/深度上限 | 可随时强制 `stop`；强制评估时必须问用户 |
| 普通 Skill（core=false） | 默认 1 轮 | 否 | 必须在每轮后由用户明确说“继续”才进入下一轮 |
| 用户指定 max_rounds=N | 精确跑 N 轮 | 是，但 N 轮后必须停止 | 超过 N 需用户显式提升 N |

```text
if core == false and round >= max_rounds:
    → 停止递归
    → 输出“已到受控轮次上限，是否继续由你决定”
```

## 输出契约（收尾时）

```text
{
  "final_skill": { id, version, text, knowledge_nodes, source_refs },
  "convergence_report": {
    "stop_reason": "semantic_static" | "gap_static" | "text_static" | "yield_exhausted" |
                   "iterator_reject" | "max_depth_reached" | "user_stop" | "corpus_exhausted" | "forced_review",
    "rounds": n,
    "effective_new_nodes_total": n,
    "high_quality_hits_total": n,
    "discarded_low_quality_total": n,
    "verified_high_remaining_ratio": 0.xx,
    "forced_review": true | false,
    "improvement_points": ["缺口X→能力Y", ...],
    "expected_convergence_rounds": "0-1" | "1-2" | "2-3"
  },
  "capability_scorecard": {
    "round0": { skill: { trigger, action, boundary, traceability, integration, total } },
    "current": { skill: { trigger, action, boundary, traceability, integration, total } },
    "delta": { skill: { total: n, percent: 0.0 } }
  },
  "yield_curve": [ { round, raw_count, high_hit, discarded, new_nodes, marginal_yield, cumulative } ],
  "per_skill_yield": { "skill_name": [ ... ] },    # 批量模式
  "discarded_low_quality_list": [ { chunk_id, density_score, reason } ],
  "pending_verification_list": [ ... ],
  "next_actions": ["外部搜索补源", "人工复核单源-存疑", "降为普通注脚", "用户决定是否继续"],
  "round_control": {
    "core": true | false,
    "next_round_allowed": "auto" | "user_required" | "none"
  },
  "iteration_ledger": {
    "round": n,
    "state_path": "round_ledger.json",
    "resume": true | false
  }
}
```

## 来源与可追溯

- 完整来源声明见本目录 `SOURCES.md`。
- 设计来源：用户规格《认知收益架构 / 价值驱动递归提升模块》+ 五个原子 skill 的接口契约。
- 外部参考：[Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)、[learn-eval-skills](https://github.com/dimayip/learn-eval-skills)、[Convergence Protocol](https://inferensys.com/glossary/recursive-error-correction/iterative-refinement-protocols/convergence-protocol)。

## 干跑验证

- 六阶段完整干跑样例见 `core-iteration/examples/smoke_pipeline.md`（Round 1 真实数据）。
- 每轮必须输出 `yield_curve`、`capability_scorecard`；批量模式要额外输出 `per_skill_yield`。

## 硬性纪律

1. **六个阶段缺一不可**：信息搜集、收益计算、蒸馏、迭代、决策、调度都必须在每轮中体现；不得跳过任何阶段假装完成。
2. **子技能按需加载**：调用前先确认对应原子 skill 可被 `skill` 工具加载；若依赖缺失，先处理依赖再继续。
3. **信息来源必须可追溯**：所有进入蒸馏的语料都必须带 source_refs；没有来源只能进待验证或丢弃。
4. **过滤器不可跳过**：任何轮次都必须经过收益过滤器；禁止“为省事直接蒸馏”。
5. **只有 verified 类进入蒸馏**：`single-doubt` 只能进待验证清单/注脚，不能成为核心知识点。
6. **迭代器拒绝时不得继续**：若收到“收益不足，拒绝更新”，直接收尾，不调用校验器。
7. **最大深度 5**：递归防护是硬上限，不得因“感觉还有希望”突破。
8. **普通 Skill 不自动续轮**：非核心 Skill 每轮结束必须把决定权交还用户。
9. **低质清单必须输出**：让用户能审查过滤器是否过于严苛；若用户认为误杀过多，可调整密度阈值或人工提升待定项。
10. **收益曲线必须可见**：调度器每轮记录，收尾时输出完整曲线表，不许只给“收敛了”结论。
11. **人类接管是元纪律**：用户说“我感觉不对劲”或要求人工覆盖时，停止自动循环，记录 `override: user/human` 后按用户决定继续。

## 反模式速查

| 反模式 | 处理 |
|---|---|
| 跳过过滤器直接蒸馏 | 违反工作流，必须回退到第 2 步 |
| 信息搜集只给二手摘要、不给可回溯来源 | 不算完成；必须回到原始出处并记录 source_refs |
| 单源存疑被计入有效新增 | 不计；只能注脚或待验证 |
| 迭代器拒绝后仍继续下一轮 | 不允许；跳收尾 |
| 决策器已 STOP 仍强制续轮 | 不允许；除非用户显式 `override: user` 并记录 |
| 普通 Skill 自动无限迭代 | 默认 1 轮，必须用户续轮 |
| 达到 5 层还继续 | 硬停，输出 max_depth_reached |
| 只报告收敛，不给出低质丢弃清单 | 必须给出，供审查过滤严苛度 |
| 连续两轮收益 <3 还自动继续 | 触发 forced_review，交用户决定 |
| 把“收益计算”和“蒸馏”混为一步 | 先算收益/过滤，再只把 verified 语料送入蒸馏 |

## 简单用户话术

> 我会把六个模块拧成一条流水线：先搜料（信息搜集），再算收益/过滤（收益计算），只让高优语料进入蒸馏，然后由迭代器决定要不要更新，最后用决策器判断这轮值不值得继续；我作为调度器控制轮次、记录收益曲线，并在该停的时候停。
>
> 核心能力我会自动磨到收敛或 5 轮上限；其他 Skill 默认只跑你指定的轮数，要不要继续完全由你决定。
>
> 收尾时我会给你：最终 Skill、收敛报告、收益曲线，以及被丢弃的低质料清单和待验证清单——你随时可以审查过滤是否太严。
