---
name: inspiration-miner
description: GitHub 灵感工厂——把 GitHub 当成高质量开源情报与插件/元能力灵感来源，通过真实仓库检索、相关性评分、候选 idea 蒸馏，反哺 DSH skill/插件/元能力的递归升级。
whenToUse: 需要从 GitHub 发现可借鉴的插件、skill、agent/harness 设计；需要为元能力寻找新思路；需要“外部灵感 → 内部改进”闭环时。
---

# 灵感挖掘器（Inspiration Miner）

> 定位：`info-source-adapter` 解决“获取信息”，本 skill 解决“从信息中获取可迁移的灵感，并驱动元能力升级”。它把 GitHub 当成“灵感工厂”，而不是只当资料库。

## 触发条件

- 用户/调度器需要“插件思路 / 新功能方向 / 元能力升级灵感”。
- 已有元能力进入瓶颈，需要外部对照。
- 需要找到与 DSH / agent skills / plugin / harness 相关的开源项目作为参照。

## 输入约定

```text
input = {
  queries?: [ "topic:agent-skills", "topic:dsh", ... ],   # 默认见 $CORE_ITERATION_ROOT/tools/mine_ideas.py
  limit?: 6,
  proxy_mode?: "host" | "system" | "none",
  offline?: bool,
  focus: "plugin" | "skill" | "meta-capability" | "harness"
}
```

## 工作流

1. **真实检索**：运行 `$CORE_ITERATION_ROOT/tools/mine_ideas.py --proxy-mode host --limit 6`。
2. **相关性评分**：根据 `dsh / skill / plugin / agent / harness / workflow / eval / self-improve` 等关键词打分。
3. **去重与排序**：输出 `$CORE_ITERATION_ROOT/tools/output/ideas.json` + `IDEAS.md`。
4. **人类/调度器挑选**：从 Top 10 中挑 1–3 个“可反哺当前元能力”的 idea。
5. **落地**：把 idea 转成改进任务或新插件/工具草案，进入 `value-iterator` / `return-forensics` 验证。
6. **记录来源**：每个 idea 保留 repo URL；不把 star/热度当证据，只当候选。

## 输出契约

```text
{
  "queries_run": n,
  "raw_items": n,
  "candidate_ideas": [
    {
      repo,
      url,
      score,
      keywords,
      suggestion,
      source_type
    }
  ],
  "selected_ideas": [ { repo, why, action, owner } ],
  "feedback_to_scheduler": "可进入下一轮 meta 迭代"
}
```

## 硬性纪律

1. **先真实检索，后蒸馏**：不要凭记忆编造 GitHub 项目。
2. **来源可追溯**：每条 idea 必须带 repo URL；否则不进入候选。
3. **热度不是证据**：stars/forks 只影响排序候选，不影响“是否值得借鉴”的最终判断。
4. **借鉴不照搬**：从开源项目提炼设计模式，不复制代码/品牌，保留 provenance。
5. **每次只落地 1–3 个 idea**：避免灵感过载。
6. **落地必须验证**：新插件/技能改动必须过 `validate_contract` / `behavior_test` / `smoke_test`。

## 边界 / 反模式

| 情况 | 处理 |
|---|---|
| 看到高 star 仓库就认为值得抄 | 不是；看其核心机制是否匹配当前缺口 |
| 只收藏不改 | 必须选 1–3 个进入落地/迭代 |
| 为了“广”而无脑加 query | 每个 query 都要能带来新独立视角 |
| 把仓库 README 当实现细节 | 回到源码/结构/文档再判断 |

## 简单用户话术

> 我会去 GitHub 搜一批 agent skill、plugin、harness 相关的真实仓库，按“能不能反哺我们的元能力”打分，挑几个最有启发性的方向给你，并带着来源和落地建议。热度和 star 只是参考，不是证据。

## 使用

```bash
python3 "\$CORE_ITERATION_ROOT/tools/mine_ideas.py" --proxy-mode host --limit 6
cat $CORE_ITERATION_ROOT/tools/output/IDEAS.md
```

## 2026 深度补强（Round 40）

> 本轮目标：把“从 GitHub 找仓库”升级为“跨市场侦察 → 五分钟预筛 → 双轴评分 → 结果回写”四段闭环。以下规则在原有真实检索、来源可追溯、热度非证据等纪律之上新增，不替代旧规则。新增来源见 `SOURCES.md`「Round 40 新增来源」。

### R40-1 跨面侦察：至少覆盖 3 个信息面，才能说“市场扫过”

- **触发**：进入灵感挖掘、回答“有没有同类/可借鉴”时。
- **动作**：
  1. **仓库面**：`gh search repos "agent skills" --topic=agent-skills --sort=updated --limit 30`，记录 `fullName / pushedAt / license / archived / description`。
  2. **代码面**：`gh search code "path:SKILL.md" --limit 50`，找到真正把 skill 放进仓库的实例；按目标插件形态换成 `--filename=plugin.json`、`--filename=.mcp.json` 等。
  3. **市场/注册表面**：插件市场（如 Claude Code 插件市场）、MCP Registry（`https://modelcontextprotocol.io/registry`）、npm/PyPI 搜索（如 `curl -sS 'https://registry.npmjs.org/-/v1/search?text=agent%20skills&size=5'`），确认它是否可安装、有元数据、有版本。
  4. 聚合列表（awesome）只作为**发现索引**，不作为证据面；发现候选后必须回到 1–3 面补一手证据。
- **边界**：三个信息面各用不同语法/入口，结果不能互相替代；某面返回 0 时记 `surface_empty`，不要写成“没有生态”。awesome 列得再多也只能证明“有人整理过”。
- **反例**：只搜 GitHub 仓库名，看到 10 个高 star 仓库就结束；没有查 `SKILL.md` 代码面、没有查市场安装面，于是漏掉了“其实已有标准格式/安装器”的情报。

### R40-2 五分钟预筛：先测“能不能落地”，再决定是否深读

- **触发**：候选进入 Top N 短名单后。
- **动作**（30 秒拿到浅层证据）：

  ```bash
  gh api repos/{owner}/{repo} --jq '{license:.license.spdx_id, pushed_at, archived, open_issues_count}'
  gh api repos/{owner}/{repo}/contents --jq '.[].name'
  gh api repos/{owner}/{repo}/releases --jq 'length'   # 发布历史
  gh api repos/{owner}/{repo}/actions/runs --jq '[.[]|.conclusion] | group_by(.) | map({k:.[0], n:length})'
  ```

- **通过线**：有许可证（或明确可学习）；有可复现样本（`tests/`、`examples/`、dry-run、demo）；有安装/接入方式；近 12 个月有提交（除非机制独特）；不是 archived。
- **降级**：无 license → `license_unknown`；只有 README 无 tests/examples/CI → `readme_only`；只适配某商业闭源 harness 且我们不使用该 harness → `harness_locked`；三者之一出现即不得直接进入“高置信灵感”，必须先做低成本验证或明确标注风险。
- **边界**：预筛是“省时间的过滤”，不是终极判定；star 低/新仓库不能因为“不热”被预筛掉，预筛只查可验证的工程信号。
- **反例**：看到 5 万 star 跳过预筛直接深读两小时；最后发现无 license、无 tests、无安装文档，只能放弃——预筛 30 秒就能发现。

### R40-3 双轴评分：质量 × 缺口匹配，且每条必须有可落地的 `suggestion`

- **触发**：打分/排序阶段。
- **动作**：
  - **质量轴 0–3**：license 明确、近期维护、有测试/示例/CI、文档能回答“怎么验证”各 1 分；没有可验证证据的不给分。
  - **缺口轴 0–3**：是否命中当前元能力的真实缺口、其机制是否可脱离原 harness 移植、是否与已有规则形成行为差异，各 1 分。
  - **最终分 = 质量 × 缺口**；`quality=0` 或 `gap=0` 的候选禁止进入 `candidate_ideas`，只能标 `reference` / `risky`。
  - 每条 `candidate_idea.suggestion` 必须可执行：例如“在 SKILL.md 头部用渐进披露：先用 3 行说明何时用，再展开动作”；不许写“很有启发”。
- **边界**：质量与缺口是两轴，高分低匹配不能靠“反正很优秀”进入；低分高匹配也不能靠“看起来有用”跳过证据。
- **反例**：一个 10 万 star 的通用设计系统打了 10 分，但我们的缺口是“skill 市场筛选”，没有一条建议能落到 trigger/action/boundary——它只是参考，不是灵感。

### R40-4 派生仓溯源：聚合仓/分叉/“全家桶”只当发现入口，不当原创证据

- **触发**：候选是 awesome list、插件市场聚合仓、fork、或一个仓库塞了几百个第三方 skill。
- **动作**：
  1. 用 `gh api repos/{owner}/{repo} --jq '{is_fork, parent: .parent.full_name}'` 看是否 fork；fork 优先看上游。
  2. 看目录是否按“创作者/来源”组织，统计 `SKILL.md` 数量与提交历史是否多为批量导入；若是，则**每条机制都要溯源到最初作者/上游仓库**再评分。
  3. 聚合仓里 license 不明确的第三方内容不能转化为本技能规则；至少确认上游 license 与出处，否则标 `provenance_gap`。
- **边界**：聚合列表是“雷达”，不是“源头”；不要把聚合仓的 star 算作其内单个 skill 的质量。
- **反例**：看到“1000+ skills 全家桶”就当作一个新范式，实际是聚合了社区已有 skill，且大量内容 license 不明，无法作为可迁移证据。

### R40-5 反哺回写：落地后必须留下 `landed_as` 与 `behavior_diff`，没有回写的轮次不算“灵感产出”

- **触发**：选定 idea 进入落地，或一轮结束。
- **动作**：
  1. 给每个 selected idea 回写：`landed_as`（具体文件/规则 id/插件名）、`behavior_diff`（before→after 一个可观察差异）、`source_health`（URL 是否仍有效、repo 是否 archived）、`next_check`（下一次验证时间）。
  2. 落地失败的记 `revert_reason`；探索过但没采用的记 `not_adopted_reason`；不要静默删除。
  3. 每轮收尾做“再发现护栏”：先 grep 本地 `ideas.json/CHANGELOG` 是否已有相同 `repo URL + 机制`，已有 `landed_as`/`revert_reason` 的不得重复入选，除非出现新的独立证据。
  4. 连续 3 轮只有新增 idea、没有 `landed_as` 行为变化 → 判定为 **发现-落地断裂**，应暂停采集、先修评分与预筛，而不是继续“收藏更多”。
- **边界**：回写不是文档义务，而是把“灵感”变成可审计行为的证明；没有回写，`ideas.json` 只是收藏夹。
- **反例**：仓库里存了 50 个“灵感”，却没有一个 `landed_as`；调度器看到搜索量继续增加，实际元能力没有任何行为差异。

### R40-6 反例速查（30 秒降级表）

| 表面信号 | 判定 |
|---|---|
| 高 star 但搜索不到 `SKILL.md` / manifest | 降 `marketing`，回到代码面验证 |
| awesome 列表收录 | 只当索引，必须去原仓找一手机制 |
| archived / 12 个月未 push | `stale`；除非机制独特，不作长期依赖 |
| 无 license 的 skill/插件 | `license_unknown`；学习可以，落地先确认 |
| 分数只来自 star/forks | 违规打分，要求补 quality/gap 证据 |
| 派生/聚合仓被当作原创 | 先溯源上游再定级 |
| 只新增“真不错”没有 `suggestion` | 不算候选 idea，记为 `reference` |

## 来源

- 本地 `info-source-adapter`、`value-meta-scheduler`、`return-forensics`
- 外部：GitHub 真实检索结果（`$CORE_ITERATION_ROOT/tools/output/ideas.json` 记录来源）
