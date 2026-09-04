---
name: distillation-consensus
description: 内容蒸馏共识——把书/视频/博客/访谈/题解等高价值材料蒸馏成 agent 可调用的启发式技能，坚持来源可追溯、触发/动作/反例三件套，并用简单语言向用户给出方向与方式。用于“把材料做成 Skill/共识”或“从材料提炼可执行规则”的任务前。
---

# 蒸馏共识 · 可调用摘要

完整版见本目录的 `CONSENSUS.md`。本文件只放可执行骨架；遇到复杂/重要任务先读完整文档。

## 核心公式

```text
可执行知识 = 触发条件 + 动作 + 反例/边界 + 来源 + 简单用户话术
```

蒸馏不是摘要，不是把原文变短，而是把不可执行的内容改造成可执行的结构。

## 触发条件

- 用户要求“把材料做成 Skill / 共识”或“从材料提炼可执行规则”。
- 调度器传入 `verified_high` / `verified-single` 语料，需要产出结构化 `skill_draft`。
- 需要把书、长视频、播客、博客、访谈、题解、官方文档等高价值材料改造成 agent 可调用的启发式技能。

## 九步流水线

```text
1 定目标        → 先确定产出：工作流 Skill / 启发式规则 / 提问协议 / 机器可读 JSON？
2 选语料        → 只选高价值片段，同一主张找 2–3 个独立来源
3 切片段        → 切到最小推理单元，不整段总结
4 提原语        → 合并同一动作的不同说法；冲突保留分支，不平均
5 交叉验证      → consensus / style / warning / common-lore 分级
6 编造成品      → SKILL.md / 共识文档 / JSON / 提示词模板
7 校验          → 来源、触发、动作、边界、用户话术，3–5 个样例干跑
8 校准/回测     → 有数值时抽 20–50 样本，算命中率/提问数/校准误差
9 人类复核      → 给来源表；允许“我感觉不对劲”覆盖
```

## 输出契约（蒸馏 Node/对接 value-iterator）

蒸馏成品不能只是一段“好读的文字”，还要能机器化地比较新旧版本。每条原语必须输出成 Node：

```text
Node = {
  id,                         # 稳定 id，如 "distillation_<kebab>_<n>"
  claim: "触发条件 → 动作 → 预期结果",
  source_refs: [ ... ],
  evidence: "verified-high" | "verified-single" | "footnote",
  weight: 1.0 | 0.5 | 0.0,
  boundary: "什么情况下失效",
  provenance: "new" | "merged" | "updated" | "unchanged",
  trace_chain: [ "raw_chunk_id -> verified -> primitive -> node" ],  # 保留从原始证据到成品的链路
  effect_ref?: "value-effect-audit node_effects id"                    # 真实效果证据，可选
}
```

- `SKILL.md` 是给 agent 的可执行摘要；`CONSENSUS.md` 是完整依据；`knowledge_nodes` 列表是给 `value-iterator` 的机器可读输入。
- 每条 Node 必须三件套齐全（触发/动作/边界）才能算“有效新增”。

## 早停与降级

当本轮 `verified_high` 不足 3 条时：

1. 不要为了“交差”硬编一条 Skill。
2. 输出 `empty_draft` / `insufficient_corpus` 标记，并列出缺少哪个缺口。
3. 建议下一步为“外部搜索补源”或“人工复核单源存疑”，而不是继续蒸馏。
4. 若材料是澄清/纠错型（如修正既有规则），可仅产出 1–2 条高置信 Node 并标注 `low_corpus_accepted`。

## 蒸馏质量自检分（7 项）

编造成品时快速打分，0/1 计分，**≥5 才是可交付**：

- [ ] 1. 每条规则有 `source_refs`？
- [ ] 2. 每条规则有 trigger / action / boundary？
- [ ] 3. 没有把“不确定”写成“否”？
- [ ] 4. 没有把单一风格写成普遍共识？
- [ ] 5. 没有把推测写成专家原话？
- [ ] 6. 用户话术不含内部术语/概率？
- [ ] 7. 至少 1 个反例或失效边界？

得分 <5 时标记 `not_ready`，不得作为本轮最终版本提交给迭代器。

## 成品发布门槛（Skill Packaging & Eval）

蒸馏出“可读文档”还不等于“可发布 Skill”。发布前额外检查：

1. **元数据可发现**：`description` 第三人称，写明“做什么 + 何时触发”；名称具体，避免 `helper/utils` 类通用名。
2. **保持瘦身**：SKILL.md 做索引与流程，细节放 `references/`；引用尽量一层深；可脚本化判断用脚本，不用散文反复描述。
3. **有评测场景**：先写 1 个 eval 任务（prompt + 确定性 checks）；复杂 Skill 至少 3 个，并加 1 个 anti-trigger（无关任务不该触发）。
4. **配对基线**：同一任务跑“无 skill”与“有 skill”，默认 3 次，算 Skill Lift；只报“能用”不算证据。
5. **来源独立**：≥2 个独立来源或单源降权；不是同源转载。
6. **版本可审计**：CHANGELOG / manifest 同步；无死引用、无过期命令。
7. **交给检验底座**：发布前用 `skill-verification-consensus` 跑一次校验报告（claims / checks_observed_red / evals / adversarial_review）。

> 边界：评测通过不等于知识正确；它只证明“这个 Skill 在任务上确实带来可测增益，且没有明显误触发”。



1. **来源可追溯**：每条必须有 source_refs；没有来源只能标 `common-lore` 并降权。
2. **不编造专家原话**：区分“原文引用”和“我的推断”；不确定就写 `inferred`。
3. **不平均分歧**：专家 A 主张 X、专家 B 主张 Y，保留两个分支，不要揉成 50% 共识。
4. **每条都要有失效边界**：只给正向例子的规则会误导人。
5. **用户只看到简单语言**：不要输出内部 feature 名、算法名、概率值；只给方向 + 方式 + 边界。
6. **一次只问一个高信息增益问题**：与用户交互时，不要同时抛一串提示。
7. **“不确定”是弱证据**：不要把它当“否”，按 `0.5*yes + 0.5*no` 更新。
8. **人类接管是元纪律**：用户说“我感觉不对劲”时停下来重新审视，不是算法选项。

## 干跑验证

- 六阶段完整干跑样例见 `core-iteration/examples/smoke_pipeline.md`。
- 交付前用 3–5 个样例干跑，并给出蒸馏质量自检分；低于 5/7 不得提交给迭代器。
- 如需一键生成完整 Skill 包（SKILL/CONSENSUS/SOURCES/manifest/examples），可先 `python3 tools/distill_skill_package.py --nodes nodes.json --id <id> --description \"...\"`，再用 `skill_package_check.py` 验证。

## 简单用户提醒模板

开始前：

> 我会先挑高价值片段，再提炼成可执行的判断方法，不会给你一整篇复述。

交付时：

> 我给你的是三样东西：方向（现在往哪边想）、方式（下一步怎么做）、边界（什么时候这条路不通）。

分歧时：

> 如果哪条和你的直觉冲突，请说“我感觉不对劲”，我会停下来检查是不是我蒸馏错了，而不是硬套模板。

## 反模式速查

| 反模式 | 处理 |
|---|---|
| 把摘要当蒸馏 | 补触发/动作/边界，否则删 |
| 无来源“专家说” | 标 `common-lore` 并降权；编造的删 |
| 平均分歧 | 保留分支 |
| 只给正向例子 | 补反例 |
| 长文没有可执行步骤 | 压成骨架 |
| 跳过校验/回测 | 用样例干跑，有数值就抽样校准 |
| 给用户泄露术语/概率 | 翻译成简单方向与方式 |
| 一次问太多问题 | 只有一个最高信息增益问题 |

## 来源

网络参考详见 `CONSENSUS.md` 第 8 节，包括：

- cangjie-skill（把书/视频/播客蒸馏成可执行 Skill）
- WorkBuddyGuide 第22章（打造 Skill：将书和视频蒸馏为可执行 Skill）
- knowledge-distillation-survey（windags-skills）
- LLM/Data Knowledge Distillation 综述（跨领域启发）
- 本地 `teacher-consensus-skill` 与 `dsh-optimization-consensus` 实践
