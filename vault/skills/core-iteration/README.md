# 核心迭代元能力（Core Iteration Meta-Capability）

> 六合一工具链：把外部信息与已有 Skill 草案，经过“信息搜集 → 收益过滤 → 蒸馏 → 迭代 → 校验 → 调度收尾”，递归提升为可收敛、可量化、可审计的 Skill 能力。
> 扩展层：`info-source-adapter`（真实多源执行）、`value-effect-audit`（实际效果价值）、`return-forensics`（收益下降根因 + 思维链）、`skill-verification-consensus`（检验底座）、`dev-workflow-consensus`（开发底座）。

## 目录

| 目录/文件 | 作用 |
|---|---|
| `web-research-consensus/` | 信息搜集策略：产出 `raw_corpus` + `knowledge_gaps` |
| `info-source-adapter/` | 信息搜集执行层：GitHub/OSV/包生态/学术等适配器 |
| `benefit-filter/` | 收益计算：密度评分 + 交叉验证 + `yield_stats` |
| `distillation-consensus/` | 蒸馏：把 verified 语料变成带 `trace_chain` 的 `Node` |
| `value-iterator/` | 迭代器：比较新旧节点、生成变更日志、接受/回退 |
| `value-validator/` | 校验器：四条硬规则 STOP/CONTINUE |
| `value-effect-audit/` | 实际效果审计：真实任务 + 多方交叉计算信息价值 |
| `return-forensics/` | 收益下降根因分析 + 可追溯思维链 |
| `inspiration-miner/` | GitHub 灵感工厂：挖掘插件/元能力新思路 |
| `skill-verification-consensus/` | 检验底座：证据分类、可证伪、Skill TDD、红队对抗复核 |
| `dev-workflow-consensus/` | 开发底座：规格先行、对抗审查、证据化验证、分层执行 |
| `value-meta-scheduler/` | 调度器：轮次控制、收益曲线、收敛报告、能力评分卡 |
| `examples/smoke_pipeline.md` | 六阶段干跑样例 |
| `examples/artifact_examples.md` | 六阶段产物字段样例 |
| `examples/backtest_template.md` | 真实使用回测模板 |
| `tools/scorecard.py` | 自动计算 5 维能力评分卡 |
| `tools/validate_contract.py` | 校验六阶段接口字段是否齐全 |
| `tools/behavior_test.py` | 用代码跑一轮合成六阶段行为测试 |
| `tools/info_source_cli.py` | 真实调用 GitHub/OSV/PyPI/npm/crates 等源 |
| `tools/run_improve_validate.py` | 一键“能力提升→验证”循环 |
| `tools/benefit_filter_live.py` | 对真实 raw_corpus 执行收益过滤输出 yield_stats |
| `tools/distill_live.py` | 把真实语料自动蒸馏成 Node 三件套 |
| `tools/iterator_live.py` | 真实 Nodes -> changelog/effective_new_count |
| `tools/validator_live.py` | 真实 Nodes -> CONTINUE/STOP |
| `tools/mine_ideas.py` | GitHub 灵感挖掘：`--category all/plugin/skill` 输出候选 ideas |
| `tools/skill_draft_builder.py` | 从真实 Nodes 生成可发布 Skill 草案 |
| `tools/meta_report.py` | 聚合六阶段结果输出 META_REPORT |
| `tools/skill_effect_bench.py` | A/B 量化 Skill 对模型的增强（成功率/质量/效率/覆盖/校准） |
| `tools/skilljack_runner.py` | 真实 Skill A/B runner：DeepSeek agent 循环 + loadSkill + verifier + 可选 judge |
| `tools/benchflow_runner.py` | BenchFlow 式矩阵 runner：多任务 A/B、汇总 Skill Lift、门禁 |
| `benchmarks/` | Skill A/B 基准模板 |
| `evals/` | 真实 A/B 任务包与结果：dev-security 正例/反例 + benchflow 配置与矩阵结果 |
| `tools/fixtures/` | 离线固定样本，供沙箱验证真实契约 |
| `tools/smoke_test.py` | 一键跑契约校验 + 行为测试 + 能力评分 |
| `reports/REPORT_ROUND1.md` | Round 1 迭代报告 |
| `reports/REPORT_ROUND2.md` | Round 2 迭代报告 |
| `reports/REPORT_ROUND3.md` | Round 3 收敛报告（STOP） |
| `reports/REPORT_ROUND4.md` | Round 4 信息获取范围扩展 |
| `reports/REPORT_ROUND5.md` | Round 5 元能力扩展（插件化获取/效果检验/收益根因/思维链） |
| `reports/REPORT_ROUND6.md` | Round 6 真实调用落地 + 提升/验证双循环 |
| `reports/REPORT_ROUND7.md` | Round 7 Watt host 代理真实调用打通 |
| `reports/REPORT_ROUND8.md` | Round 8 GitHub 真实数据增强 |
| `reports/REPORT_ROUND9.md` | Round 9 GitHub 多形态采集+质量预筛 |
| `reports/REPORT_ROUND10.md` | Round 10 真实 pipeline 执行层 |
| `reports/REPORT_ROUND11.md` | Round 11 真实蒸馏执行层 |
| `reports/REPORT_ROUND12.md` | Round 12 六阶段真实执行链全部打通 |
| `reports/REPORT_ROUND13.md` | Round 13 GitHub 灵感工厂 |
| `reports/REPORT_ROUND14.md` | Round 14 插件/skill 市场侦察 |
| `reports/REPORT_ROUND15.md` | Round 15 真实 Skill 草案+一键全链路 |
| `reports/` | 历史轮次报告归档（最新：ROUND17 交叉验证+实时报告、CLEANUP 减法审计） |
| `round_ledger.json` | 跨轮状态与收益曲线/评分卡 |
| `TRAINING_STATE.md` | **训练暂停与续训入口（新会话先读）** |

## 接口契约（字段必须对齐）

```text
info-source-adapter --(raw_corpus, source_scope_report)--> web-research-consensus
web-research-consensus --(raw_corpus, knowledge_gaps, search_meta)--> benefit-filter
benefit-filter         --(verified_high, conflict_branches, pending_verification,
                          discarded_low_density, yield_stats)--> distillation-consensus
distillation-consensus --(skill_draft with knowledge_nodes + trace_chain)--> value-iterator
value-iterator         --(accepted, new_skill, changelog, effective_new_count)--> value-validator
value-validator        --(decision, triggered_rules, forced_review, stop_reason)--> value-meta-scheduler
value-effect-audit     --(node_effects, feedback_to_iterator)--> value-iterator / benefit-filter
return-forensics       --(diagnosis, trace_chains)--> value-meta-scheduler / user
value-meta-scheduler   --(final_skill, convergence_report, yield_curve, capability_scorecard)--> user
```

每个阶段的具体字段定义见各 `SKILL.md`；不允许跨阶段发明未在契约中的别名。

## 运行一个批量轮次

1. 确认核心与扩展 skill 已加载或可直接读取；缺失时先处理依赖再做。
2. 设置 `input.target_skills = [...]`，可按需设置 `info_scope` / `info_depth`。
3. 每轮依次调用六阶段；`benefit-filter` 与决策器/校验器不可跳过。
4. 有真实使用数据时，调用 `value-effect-audit` 回填节点效果；收益下降时调用 `return-forensics`。
5. 每轮把 `round_ledger.json` 更新到 `state_path`；收尾输出本目录 `README.md` 下的版本表。

## 版本表

| Skill | 当前版本 | 上次变更 | 说明 |
|---|---|---|---|
| web-research-consensus | 0.3.0 | round22 | 输出契约加 `evidence_class?` / 搜索预算 / GitHub 扩展 |
| search-source | 0.3.0 | round29 | 来源台账/独立判定/搜索预算/evidence_class/输出契约/干跑 |
| info-source-adapter | 0.7.0 | round29 | 真实多源 + `github-file` 文档/源码适配器 + 输出契约/干跑 |
| benefit-filter | 0.2.0 | round4-info-scope | 密度公式修正 + OSS 质量判定 |
| distillation-consensus | 0.7.0 | round30 | Node 契约 + 成品发布门槛 + `distill_skill_package.py` + examples |
| value-iterator | 0.3.0 | round12 | 版本/反馈/计数 + Node trace_chain |
| value-validator | 0.2.0 | round12 | 降级/校准/stop_reason 映射 |
| value-effect-audit | 0.2.0 | round30 | 实际效果 + 多方交叉价值 + 干跑示例 |
| return-forensics | 0.2.0 | round30 | 收益下降根因 + 思维链 + 干跑示例 |
| value-meta-scheduler | 0.5.0 | round22 | 批量/评分卡/收敛预测/扩展检验与开发底座 |
| skill-verification-consensus | 0.3.0 | round29 | 检验底座 + `skill_package_check` / `scaffold_eval_task` + 干跑收口 |
| dev-workflow-consensus | 0.3.0 | round29 | 开发底座 + `scaffold_dev_spec` + 输出契约/干跑 |

## 自动校验

```bash
python3 tools/validate_contract.py .   # 检查六阶段契约字段
python3 tools/behavior_test.py         # 用代码跑一轮合成行为测试
python3 tools/scorecard.py .           # 输出 5 维能力评分（含基础/检验/开发底座）
python3 tools/skill_package_check.py <skill-dir>  # Skill 包结构/manifest/三件套检查
python3 tools/smoke_test.py            # 一键冒烟：契约 + 行为 + 包检查 + 评分
python3 tools/final_evolution_report.py .  # 生成直观迭代终评
```

## 信息获取范围

默认 `info_scope` 覆盖 `web / github / package_registry / academic / oss_community`，并要求：

- 广度：多入口、多生态、多数据库，入口之间要“独立视角”。
- 深度：开源结论必须能回溯到源码/commit/release/安全公告，不能只看 README/star。
- 可信度：GitHub stars/forks、awesome 收录不是证据；verified-high 需要上游一手 + 独立旁证。
- 执行：真实抓取交给 `info-source-adapter`，保留来源与限制报告。

## 状态与回溯

- `round_ledger.json`：跨轮恢复状态。
- 每个 skill 的 `CHANGELOG.md`：可审计的版本变更。
- `examples/smoke_pipeline.md`：链路干跑。
- `Node.trace_chain` / `return-forensics.trace_chains`：保留“来源→验证→蒸馏→应用→效果”的思维链。
