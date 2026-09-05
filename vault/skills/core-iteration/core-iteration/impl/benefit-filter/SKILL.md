---
name: benefit-filter
description: 收益计算与交叉验证过滤器——对搜索增强捞回的原始语料做信息密度评分与多源交叉验证，只向蒸馏模块输送【已验证-高优】语料，并把【单源-存疑】打包成待验证清单。用于任何“搜索增强 → 蒸馏”管道的前置清洗。
whenToUse: - 收到【搜索增强】模块输出的原始语料块 / 语义向量 / 知识缺口清单。
---
# 收益过滤器（Yield Filter）

> 定位：这是价值驱动递归提升模块的第一道闸门。它的职责不是“尽量多留语料”，而是“只放行预期收益超过阈值的可靠知识核”。宁缺毋滥。

## 触发条件

- 收到【搜索增强】模块输出的原始语料块 / 语义向量 / 知识缺口清单。
- 蒸馏前需要判断“这批语料值不值得进入蒸馏管道”。
- 用户或调度器要求“过滤低质量、低密度、不可靠语料”。

## 输入约定

```text
输入：
  raw_corpus: [
    {
      chunk_id,
      text,
      semantic_vector?,         # 可选，用于去重与相似度
      source: { url, title, author, publisher, date, type },
      claim?: string,            # 若已提取核心主张
      gap_id?                    # 对应知识缺口
    }
  ]
  repository_corpus: [ ... ]     # 仓库既有语料/已蒸馏 Skill 的来源表
```

## 第一步：信息密度评分（0–100）

对每一块原始语料执行三个维度打分，**低于 60 分直接丢弃**，不进入交叉验证。

### 维度与权重（0–100 原始分）

每个维度先打 0–100 的原始分，再按权重加权得到密度分。**不要**把下表锚点当作“维度满分”——否则加权上限只有 34，永远过不了 60 阈值。正确读法：锚点是该维度在 0–100 标尺上的参照点。

| 维度 | 权重 | 0–100 评分锚点 |
|---|---|---|
| 反常识程度 | 0.40 | 90=能推翻常见默认假设并给出机制；65=反直觉但可被解释；40=略有新意；20=常识/复述 |
| 具体步骤数 | 0.30 | 90=≥5 个可执行原子步骤或可复现操作；65=3–4 步；40=1–2 步；20=纯观点无操作 |
| 可验证证据 | 0.30 | 90=一手数据/论文/可复现实验；65=官方文档或两份独立转述；40=单一高质量来源；20=无来源/孤证 |

```text
density_score = round(0.40 * 反常识程度_raw + 0.30 * 具体步骤数_raw + 0.30 * 可验证证据_raw)
# 三个 raw 均为 0–100；加权后总分 0–100
if density_score < 60:
    → 进入 discarded_low_density，终止后续处理
```

补充规则：

- 若语料与仓库已有语料的语义向量余弦相似度 > 0.95，且不增加新操作步骤，判为“重复”而不是新收益，密度分直接 ≤ 59。
- 若只有惊人断言但没有“如果为真会改变什么行为”的推理链，反常识程度最高只能给 65。
- 评分必须给出理由；不允许只写一个分数。

## 第二步：交叉验证匹配

只有密度 ≥ 60 的语料进入本步。对每块的**核心主张**做交叉验证。

### 2.1 独立来源判定

两个来源必须同时满足以下条件才算独立：

1. 不是同一作者/机构/通稿/同一数据库的转载；
2. 不是从同一原始材料派生出来的二手转述；
3. 至少一个来源能追溯到一手证据或可复现数据；
4. 两个来源之间没有“A 引用 B”的单向依赖。

### 2.2 判定矩阵

| 条件 | 标记 | 去向 |
|---|---|---|
| ≥2 个独立来源指向同一核心主张 | `verified-high` | 进入蒸馏管道，权重 1.0 |
| 仅 1 个来源且逻辑自洽性检验通过 | `verified-single` | 可进入蒸馏管道，但权重 0.5，必须挂“单源待证”注脚 |
| 仅 1 个来源且逻辑自洽性检验失败 | `single-doubt` | 禁止进入蒸馏管道，进入待验证清单 |
| 0 个来源 | `single-doubt` | 禁止进入蒸馏管道，进入待验证清单 |

### 2.3 逻辑自洽性检验（单源时的替代路径）

单源“惊人之语”不能只凭“听起来对”就放行。必须通过以下三项：

- [ ] 内部无矛盾：该主张与自身前提、同一来源其他陈述不冲突；
- [ ] 可由已确立的第一性原理或已知机制推导，不需要隐藏的额外假设；
- [ ] 至少做一次反例搜索/反例构造，找不到明显反例。

三项全过 → `verified-single`；任一项不过 → `single-doubt`。

### 2.4 开源 / GitHub 来源的质量判定

输入中的 `source.type` 可能是 `github`、`package_registry`、`security_advisory`、`oss_community`、`docs` 等。开源来源不能只看热度，必须额外过这四问：

1. **是否一手**：结论是否来自源码/commit diff/PR 或 issue 线程/release notes/安全公告？README 和 star 数只是一手性弱信号。
2. **是否独立**：fork、镜像、同作者/同组织仓库、同一包仓库的多次转帖，都不算独立来源；要找不同维护者/不同生态/不同数据库。
3. **是否可回溯**：GitHub 条目必须带 `repo_url + commit/tag/release`，包依赖必须带 `package_name + version`；否则只能 `single-doubt`。
4. **是否活跃且一致**：仓库是否过时、是否存在 deprecation、安全公告与 README 是否矛盾；以最近 release/commit 与公告为准。

开源交叉验证加分项：

- 上游仓库一手证据 + 包生态元数据（npm/PyPI/Maven/crates/Go proxy）
- 安全公告数据库（GitHub Advisories / OSV）
- 不同生态或不同维护者的下游消费/实现
- 第三方评测或官方基准

边界：

- 两个来源如果都只是同一仓库的不同页面（README + 官网），仍算单源，不升级为 verified-high。
- “awesome 收录”和“高 star”是准入线索，不是交叉验证证据。

## 输出格式（只向蒸馏模块输送 verified 类）

```text
{
  "verified_high": [
    {
      chunk_id,
      claim,
      density_score,
      verdict: "verified-high" | "verified-single",
      independent_sources: [source_ref...],
      source_count,
      weight: 1.0 | 0.5,
      gap_id?
    }
  ],
  "conflict_branches": [
    {
      chunk_id,
      claim_a,
      claim_b,
      source_refs_a: [source_ref...],
      source_refs_b: [source_ref...],
      verdict: "both_verified" | "one_doubt" | "contradiction",
      gap_id?
    }
  ],
  "pending_verification": [
    {
      chunk_id,
      claim,
      density_score,
      verdict: "single-doubt",
      reason: "缺少独立来源" | "逻辑自洽性失败: <具体原因>",
      source_refs: [source_ref...],
      suggested_action: "外部搜索补源" | "人工复核" | "降为注脚"
    }
  ],
  "discarded_low_density": [
    { chunk_id, density_score, reason, sample_text }
  ],
  "yield_stats": {
    "raw_count": n,
    "density_pass": n,
    "verified_high_count": n,
    "verified_single_count": n,
    "pending_count": n,
    "discarded_count": n,
    "avg_density_score": 0.00,
    "remaining_verified_high": n,
    "remaining_gap_count": n,
    "verified_high_remaining_ratio": 0.00
  }
}
```

## 收益统计与剩余高优率（下游接口）

过滤器必须同时输出 `yield_stats`，供 `value-validator` 与 `value-meta-scheduler` 做收敛判断：

```text
yield_stats = {
  raw_count,                 # 本轮进入过滤器的原始语料条数
  density_pass,              # 密度 ≥60 的条数
  verified_high_count,       # 多源独立验证条数
  verified_single_count,     # 单源自洽、降权条数
  pending_count,             # single-doubt 条数
  discarded_count,           # 低密度丢弃条数
  avg_density_score,         # 通过密度闸门的平均密度分
  remaining_verified_high,   # 本轮之后仍未进入蒸馏的 verified-high 条数
  remaining_gap_count,       # 剩余知识缺口总数（含未解决缺口）
  verified_high_remaining_ratio
}

verified_high_remaining_ratio = remaining_verified_high / max(1, remaining_gap_count)
```

- `verified_high_remaining_ratio` 是调度器“矿脉是否枯竭”的核心输入，必须可复算。
- 若剩余缺口为 0，则 ratio 记为 0，不能除零。

## 2026 深度补强（Round 40）

> 定位：在原有“密度评分 → 交叉验证 → 输出”主流程上，补上四个容易漏判的维度：决策收益、证据强度分层、可证伪性、价值密度与时效。以下规则均作为前置闸或后置审计，不得绕过。

### R40-1 决策收益闸（Decision Delta Gate）

**动作**

1. 每条核心主张进入密度评分前，必须写一句“决策差分”：
   `if 为真 → 会改变哪个下游动作/提示词/优先级；if 为假 → 哪个动作会做错。`
2. 写不出可观察的决策差分（包括“只是涨知识”），`反常识程度_raw` 封顶 65，且 `density_score` 封顶 59，进 `discarded_low_density`，reason 必须写 `no_decision_delta`。
3. 写得出的差分写进输出 `decision_delta` 字段，供 value-validator / value-meta-scheduler 复算。

**依据**：信息价值（VOI）取决于“能否改变决策结果”，而非信息本身的惊奇度；不改变任何下游动作的信息，决策收益为零。

**反例**：某文说“某模型又涨 0.1 分”，但没有给复现配置，也没有说明会改变你的哪一条筛选规则 → 即使反常识与步骤数都很高，也必须被决策收益闸拦截。

### R40-2 证据强度分层与共同祖先塌缩（Source Lineage）

**动作**

1. 每个 source 先打强度级：A=一手数据/可复现实验/源码+commit/原始发布；B=官方文档/同行评审二手/多机构报告；C=知名行业博客/社区权威/教材；D=聚合站/自媒体/无日期匿名/纯转述。
2. 追踪每个 source 的 `root_source`（论文、仓库、数据集、官方公告等原始出处）。两个 URL 若 `root_source` 相同，即使页面不同，也合并为 1 条 `source_line`。
3. `verified-high` 的新门槛为同时满足：
   - ≥2 条不同的 `source_line`；
   - ≥1 条 A/B 级来源；
   - 加权支持度 `Σ(A=1.0, B=0.8, C=0.5, D=0.2) ≥ 2.0`。
4. 两条 D 级来源只能算 `verified-single`（0.5），不得升级为 `verified-high`。
5. 输出必须带 `source_lineage`，例如 `[S1,S4] -> root: paper#123`，供人工复算。

**依据**：证据应按似然比/权重叠加，而不是按 URL 条数线性叠加；多个源自同一原始材料的页面会产生“假多源”。

**反例**：A、B 两个站点都转载同一篇 arXiv 论文且都无复现 → `root_source` 相同，`source_line=1`，不能判 verified-high。

### R40-3 群落独立性与负向复现

**动作**

1. 给每个 source 标 `community_id`（如 `academic`、`official-docs`、`security-bulletin`、`tech-industry`、`aggregator`）。
2. 两条 `source_line` 即使 root 不同，若属于同一群落且证据链高度重叠（同行业、同评测体系、同批作者互引），有效支持按 1.5 条计，不能直接按 2 条。
3. 有“负向复现”时升级：一个来源给结论，另一个独立来源用不同数据/工具/方法复现或反向验证，且结论一致 → 标记 `reproduced: true`，可作为 `verified-high` 的强佐证（权重 1.0）。
4. 只有同一群落的重复转发、没有跨群落或跨方法证据，降回 `verified-single`。

**依据**：三角验证（triangulation）要求方法/数据/视角真正独立；同群落高频转发只是信息流的重复曝光，不是独立证据。

**反例**：同一行业号在公众号、知乎、微博各发一遍同一通稿 → URL 三个，但是同一 `community_id`、同一 `root_source`，有效来源只有 1 条。

### R40-4 可证伪性闸（Falsifiability Gate）

**动作**

1. 在“可验证证据”打分前，为每条主张写可证伪谓词：`if <claim> is true, we should observe/reproduce <specific measurable outcome>; otherwise, claim is refuted.`
2. 写不出具体可观察结果（只有“专家认为/业内共识/应该”），`可验证证据_raw` 封顶 40；不得仅因“有引用”就给 65/90。
3. 规范性/审美/价值判断不按实证证据打分，输出时标 `verdict_kind: normative`，最多 `verified-single`，并注明“需要人工/用户决策”。
4. “可复现操作”与“可验证证据”分开记录：前者是能照着做，后者是能检验真假；两者缺一时不能进 `verified-high`。

**反例**：说“这个框架性能更好”但不给 benchmark、复现命令、误差范围 → 证据分必须降到 ≤40，并进 pending，等待人工补可证伪条件。

### R40-5 价值密度与时效衰减（Value Density & Time Decay）

**动作**

1. 计算 `new_actionable_ratio = 新增可执行动作数 / 总句子数`；<0.2 时 `density_score` 封顶 59，reason 写 `dilute_background`。
2. 计算 `density_per_token = density_score / token_count`；多候选得分相近时，优先 `density_per_token` 高的；同时输出 `token_cost`。
3. 时效敏感类主张（API/安全/性能对比/最新法规与排名）必须带 `as_of` 日期：
   - 最近一次独立验证日期距当前 > 12 个月 → 最高只评 `verified-single`（0.5），不能 `verified-high`；
   - 无任何带日期来源 → 升为 `single-doubt`，reason 写 `unverifiable_as_of`。
4. 稳定类主张（数学、经典机制、长期共识）允许旧来源进 `verified-high`，但输出标 `stable_claim: true`。

**反例**：2023 年的某 API 性能基准被两篇 2026 年的二手文章互相引用 → 因领域时效衰减，最多 `verified-single`（0.5），不能作为当前核心规则。

### R40 检查清单（放行前五问）

- [ ] 决策差分：为真会改变哪个具体动作？
- [ ] 证伪谓词：什么可观察结果会推翻它？
- [ ] 血缘：所有 source 的 `root_source` 是否唯一且独立？
- [ ] 群落：是否来自不同社区/生态/方法，而非同源转发？
- [ ] 时效：以当前决策时点看，证据是否仍然有效？

五问全过才允许 `verified-high`；任一不过按对应规则降级为 `verified-single`/`single-doubt`/`discarded_low_density`。

### R40 新增反模式速查

| 反模式 | R40 处理 |
|---|---|
| 多个 URL 同根同社群就当作多来源 | 用 `source_line`/`root_source` 塌缩，只计 1 条 |
| “有引用”就当作可验证 | 必须先写证伪谓词；不可证伪则证据分封顶 40 |
| 分数高但无决策影响 | 过决策收益闸；写不出决策差分就封顶 59 |
| 旧来源在快变领域仍给 high | 按 12 个月时效规则降为 verified-single 或 single-doubt |

## 来源与可追溯

- 完整来源声明见本目录 `SOURCES.md`。
- 设计来源：用户规格《认知收益架构 / 价值驱动递归提升模块》；交叉验证规则继承 `distillation-consensus` 与 `web-research-consensus`。
- 外部参考：[OpenAI Agent Skills Evals](https://developers.openai.com/blog/eval-skills)、[learn-eval-skills](https://github.com/dimayip/learn-eval-skills)。

## 干跑验证

- 六阶段完整干跑样例见 `core-iteration/examples/smoke_pipeline.md`。
- 每次过滤至少要有一张 `yield_stats` 表；若 `verified_high_remaining_ratio` 为 0 或 <0.10，要在报告里提示“矿脉接近枯竭”。

## 硬性纪律

1. **只输送 verified 类**：`single-doubt` 和 `discarded_low_density` 一律不得进入蒸馏模块。
2. **单源逻辑自洽也要降权**：`verified-single` 进入蒸馏时权重 = 0.5，不得作为核心规则的唯一依据。
3. **来源可追溯**：每个 verified 条目必须带可回溯 source_refs；没有 source_refs 的语料禁止标记为 verified。
4. **不平均分歧**：两个独立来源主张冲突时，保留分支，不揉成 50% 共识；两个分支分别判定。
5. **人类接管是元纪律**：用户/调度器说“这个我复核过”或“我感觉不对劲”时，允许人工把 `single-doubt` 临时提升为 `verified-single`，但必须在输出中写明 `override: human`。

## 反模式速查

| 反模式 | 处理 |
|---|---|
| 分数高就放行，不看来源 | 必须再过交叉验证；无来源只能单源-存疑 |
| 把同一通稿/同一数据库转载当成 2 个来源 | 不算独立，继续找真正独立的信源 |
| “专家说”但没有具体出处 | 密度分证据项 0 分，大概率被丢弃 |
| 把摘要当知识核 | 没有触发/动作/边界，具体步骤数最多 40 分 |
| 害怕丢料而放低 60 分阈值 | 不放低；放低的唯一方式是用户显式覆盖并记录 |

## 简单用户话术

> 我会先做两道闸：一是算信息密度（反常识、可操作、可验证），低于 60 直接丢；二是交叉验证，只有至少两个独立来源、或单源但逻辑自洽的“高优语料”才会进入蒸馏。单源存疑的我单独打包给你，不会混进核心规则。
