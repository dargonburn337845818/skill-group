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
  queries?: [ "topic:agent-skills", "topic:dsh", ... ],   # 默认见 tools/mine_ideas.py
  limit?: 6,
  proxy_mode?: "host" | "system" | "none",
  offline?: bool,
  focus: "plugin" | "skill" | "meta-capability" | "harness"
}
```

## 工作流

1. **真实检索**：运行 `tools/mine_ideas.py --proxy-mode host --limit 6`。
2. **相关性评分**：根据 `dsh / skill / plugin / agent / harness / workflow / eval / self-improve` 等关键词打分。
3. **去重与排序**：输出 `tools/output/ideas.json` + `IDEAS.md`。
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
python3 tools/mine_ideas.py --proxy-mode host --limit 6
cat tools/output/IDEAS.md
```

## 来源

- 本地 `info-source-adapter`、`value-meta-scheduler`、`return-forensics`
- 外部：GitHub 真实检索结果（`tools/output/ideas.json` 记录来源）
