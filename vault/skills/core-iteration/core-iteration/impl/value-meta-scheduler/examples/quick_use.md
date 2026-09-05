# Quick Use：value-meta-scheduler

> 一句话：整合“信息搜集→收益计算/过滤→蒸馏→迭代器→决策器→调度器”的核心迭代元能力；按收益曲线自动/受控迭代，输出最终 Skill、收敛报告、收益曲线与被丢弃语料清单。

## 何时用

- 当任务命中 `SKILL.md` 的“触发条件 / 何时使用”时。

## 最小可复现动作

- `info-source-adapter` 产出的 `source_scope_report` 会增强 `web-research-consensus` 的 `search_meta`，用于判断“是否真的打开了新缺口”。
- `value-effect-audit` 的 `feedback_to_iterator` 会改变节点权重：promote / demote / delete / needs_evidence。
- `return-forensics` 的 `trace_chains` 会进入最终报告，作为“来源→验证→蒸馏→应用→效果”的可审计思维链。
- `skill-verification-consensus` 的输出（claims/checks_observed_red/evals/adversarial_review）作为发布门槛，不通过不得宣告交付。

## 验证方式

- 按 `SKILL.md` 的干跑/检查清单执行；
- 发布/更新前跑 `skill_package_check.py` 与本 skill 对应校验。
