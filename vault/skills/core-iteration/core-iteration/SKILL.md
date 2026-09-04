---
name: core-iteration
description: 核心迭代元能力深模块——把“搜索→过滤→蒸馏→迭代→校验→调度→审计→根因”封装为一个对外入口，用于创建/精修 Skill、价值驱动的递归提升和知识收益闭环。
whenToUse: 用户要把材料做成 Skill、要迭代/校验/收敛某个 Skill、要判断继续迭代还是停止、要审计知识来源与效果时。
---

# 核心迭代元能力（Core Iteration）

> 定位：这是技能库唯一的“价值驱动递归提升”入口。它不暴露十个小 skill，而是按阶段组织内部实现。
> 内部实现：`impl/` 下的 benefit-filter、distillation-consensus、value-iterator、value-validator、value-meta-scheduler、value-effect-audit、return-forensics、inspiration-miner、info-source-adapter、web-research-consensus。

## 触发条件

- 用户要求“把这份材料蒸馏成 Skill / 共识 / 知识节点”。
- 用户要求“继续迭代 / 收敛判断 / 收益回测 / 根因分析”。
- 需要从搜索语料中筛选高优、交叉验证、生成绩效曲线和变更日志。
- 用户说“这版 Skill 是否该停 / 是否有效”。

## 动作（外部可见的统一流程）

1. **定目标**：先确认产出是工作流 Skill、启发式规则、提问协议，还是机器可读 JSON。
2. **搜索与来源**：调用 `search-source` 底座获取 raw_corpus 与来源报告。
3. **过滤**：密度评分（反常识/可操作/可验证），多源交叉验证，输出 verified_high / pending / discarded。
4. **蒸馏**：把 verified 语料切到最小推理单元，产出带 `trace_chain` 的 Node（触发/动作/边界/来源）。
5. **迭代**：比较新旧节点，只有真实“有效新增”才接受；强制变更日志。
6. **校验**：语义位移、缺口重合、编辑步长、边际收益四条硬规则；STOP/CONTINUE。
7. **效果/根因**：有真实任务时回填 effect；收益下降时跑 forensics 定位根因。
8. **调度收尾**：输出收敛报告、收益曲线、最终 Skill、丢弃清单与能力评分。

## 边界

- 没有 verified 证据的“专家说”不能进入核心规则；单源必须降权并挂“单源待证”。
- 本模块是做“认知收益”的，不是日常开发流程；开发/重构走 dsh-skill-router 的开发强流程。
- 如果材料不足 3 条 verified-high，应输出 insufficient_corpus，不要为了交差硬编 Skill。
- 用户说“我感觉不对劲”时停止，允许人工覆盖并记录 override。

## 验收/质量门槛（qualityCriteria）

- 每条规则必须有 source_refs 且三件套齐全（trigger/action/boundary）。
- 核心规则默认要求 ≥2 个独立来源；单源只能降权或作为注脚。
- 不平均分歧：冲突保留分支，不揉成 50% 共识。

## 用户话术

> 我会先把材料拆成可执行判断，再按“来源是否可信、是否真的能改变行为”过滤；只有验证过的高优语料才会变成 Skill 规则，最后给你方向、方式和边界。
