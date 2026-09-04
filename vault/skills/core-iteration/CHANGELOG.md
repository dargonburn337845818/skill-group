# Core Iteration Meta-Capability · Changelog

## 2026-09-04 · Round 21 · STOP (corpus_exhausted)

- 冻结语料收敛复核：42 raw / 31 verified-high / 73 nodes，effective_new=0。
- value-validator 输出 STOP，stop_reason=corpus_exhausted；meta_report 标记 CONVERGED。
- `round_ledger.json` 更新为 Round 21 收敛状态，直观能力分 89/100。
- 最终 Skill 草案落盘：`tools/output/SKILL_DRAFT.md`（73 nodes）。
- 契约校验 / behavior / smoke 全部 PASS。

## 2026-09-04 · Round 20 · 多主题扩展 + 收敛判定补全

- 语料从 15 条 rust 单主题扩展到 42 条多语言/多主题 GitHub 情报（python/typescript/ai-agents/mcp/skills + psf/requests）。
- verified_high 从 2 提升到 31；nodes 从 17 到 73；effective_new=56；validator CONTINUE。
- `tools/meta_report.py`：支持 `--round`、`--old-nodes`，真实计算 effective_new，不再硬编码 Round 18。
- `tools/validator_live.py`：实现规则 D（effective_new≤2 且高优率<0.10 → STOP），输出稳定 stop_reason，修正 cumulative_nodes。
- 新增 `tools/output/nodes_round20_list.json` 与 `info_dump_round19.json` 基准文件。
- 契约校验 / behavior / smoke 全部 PASS。

## 2026-09-04 · Round 3 · STOP (yield_exhausted)

- 新增 `examples/backtest_template.md`：真实使用回测模板。
- 新增 `tools/smoke_test.py`：一键契约校验 + 能力评分汇总。
- 契约校验保持 PASS，评分卡 102/120（平均 17.0）。
- 理由：剩余高优率 <0.10，且本轮仅 2 个高价值新增，判定收敛。

## 2026-09-04 · Round 2

- 新增 `tools/scorecard.py` 与 `tools/validate_contract.py`。
- 新增 `examples/artifact_examples.md` 与共享 `examples/dry_run.md`。
- 4 个内部 skill 新增 SOURCES.md + 来源与可追溯小节。
- distillation 补齐触发条件；iterator 补 semver。
- 能力评分从 round0 82 提升到 102。

## 2026-09-04 · Round 1

- 六件套 SKILL.md 接口契约/输出契约对齐。
- 修正 benefit-filter 密度评分公式 bug。
- 新增 value-meta-scheduler 批量输入、能力评分卡、收敛预测、状态持久化。
- 新增各 skill CHANGELOG.md、round_ledger.json、group README、smoke_pipeline 样例。

## 2026-09-04 · Round 4 · 信息获取范围扩展（post-convergence）

- `web-research-consensus`：增加 GitHub/开源库检索入口、深度阅读规则、可信度边界。
- `benefit-filter`：增加开源/GitHub 来源质量判定，stars/forks 不作证据。
- `value-meta-scheduler`：增加 `info_scope` / `info_depth` 与广度-深度-可信度平衡策略。
- 契约校验与一键冒烟继续保持 PASS。

## 2026-09-04 · Round 5 · 元能力扩展

- 新增 `info-source-adapter`：真实多源获取执行层（GitHub/OSV/包生态/学术）。
- 新增 `value-effect-audit`：真实效果 + 多方交叉计算信息价值，反馈节点权重。
- 新增 `return-forensics`：收益下降根因分析 + 可追溯思维链。
- Node 增加 `trace_chain` / `effect_ref?`，让知识节点成为可循思维链。
- 新增 `tools/behavior_test.py`：用代码跑一轮合成行为测试。
- 扩展 scorecard/validate_contract 覆盖 9 个 skill。

## 2026-09-04 · Round 6 · 真实调用落地

- `info-source-adapter` 从文档层升级为真实调用 CLI：GitHub/OSV/PyPI/npm/crates 适配器。
- 新增 `tools/fixtures/*.json` 离线固定样本，支持沙箱内验证同一契约。
- 新增 `tools/run_improve_validate.py`：一键运行“能力提升 → 验证”循环。
- 契约校验扩展为检查必要工具文件存在；PASS。

## 2026-09-04 · Round 7 · Watt host 代理真实调用打通

- host 代理模式改为 `curl --resolve` 直连 TLS 反代，不再依赖 CONNECT。
- 真实 GitHub API 调用成功，产出 live `info_dump.json`。
- 支持自动探测 WSL 中 Windows 宿主 IP。
- 对未加速的 OSV/PyPI/npm/crates 域名返回清晰错误并记录。

## 2026-09-04 · Round 8 · GitHub 真实数据增强

- GitHub 适配器输出完整仓库元数据与 popularity_signals。
- 明确 stars/forks 是流行度信号，不是核心证据。
- 真实 live 数据已记录到 tools/output/info_dump.json。

## 2026-09-04 · Round 9 · GitHub 多形态真实采集 + 质量预筛

- 新增 github-issues / github-releases / github-code 适配器。
- 新增 tools/repo_quality.py，对真实 raw_corpus 计算 quality_score。
- 真实 live 采集：9 条（3 repo + 3 issue + 3 release），质量均分 86.7。

## 2026-09-04 · Round 10 · 真实 pipeline 执行层

- 新增 github-commits / github-pr 适配器。
- 新增 tools/benefit_filter_live.py：真实 raw_corpus -> yield_stats。
- 真实 live：15 条语料（repo/issue/release/commit/PR），benefit-filter 全部进入 verified-single。

## 2026-09-04 · Round 11 · 真实蒸馏执行层

- 新增 tools/distill_live.py：把 15 条 live 语料自动转成 Node。
- 每个 Node 含 trigger/action/boundary/source/trace_chain。
- live distillation: nodes=15, with_boundary=15, avg_quality=70.0。

## 2026-09-04 · Round 12 · 真实迭代器 + 校验器

- 新增 tools/iterator_live.py：真实 Nodes -> accepted/effective_new_count/changelog。
- 新增 tools/validator_live.py：真实 Nodes -> CONTINUE/STOP。
- 六阶段真实执行链全部打通：CYCLE PASS。

## 2026-09-04 · Round 13 · GitHub 灵感工厂

- 新增 tools/mine_ideas.py：真实 GitHub 灵感挖掘。
- 新增 inspiration-miner 元能力，并接入调度器扩展表。
- 真实检索 6 组 query，30 条仓库，29 条候选 idea。

## 2026-09-04 · Round 14 · 插件/skill 市场侦察

- 新增 tools/market_scout.py（plugin + skill 双模式）。
- 真实插件市场 30 raw/23 candidates；skill 市场 30 raw/30 candidates。

## 2026-09-04 · Round 15 · 真实 Skill 草案 + 一键 pipeline

- 新增 tools/skill_draft_builder.py、tools/live_pipeline.py。
- 可以从真实 15 条语料一键生成 SKILL_DRAFT.md。

## 2026-09-04 · Round 16 · 多源交叉验证深化（元能力而非扩展）

- benefit_filter_live 按 topics 聚合独立仓库，生成 verified-high。
- distill/iterator/validator/forensics 全链路同步支持 verified-high。
- live 结果：15 单源 + 1 verified-high，CYCLE PASS。

## 2026-09-04 · Round 17 · 交叉验证增强+元能力实时报告

- benefit_filter_live 增加 language 生态聚合，verified_high=2。
- 新增 tools/meta_report.py，一键输出 META_REPORT。
- live：17 Nodes，validators CONTINUE，forensics cross_verification_progress。

## 2026-09-04 · Round 18 · 标准轮次/收益/收敛报告

- meta_report.py 增加 round/yield_curve/convergence 标准输出。
- 状态：CONTINUE，未收敛，继续多源交叉验证。

## 2026-09-04 · Round 19 · Skill 对模型增强量化

- 新增 tools/skill_effect_bench.py 与 benchmarks 模板。
- 参考 OpenAI Agent Skills Evals / Scale / skilljack-evals。
- 当前模板示例：增强指数 25.5%（明显增强）。

## 2026-09-04 · Round 22 · 基础 skill 综合迭代（override: user）

- 切换信息范围：Agent Skill 工程化 / evals / verification / dev workflow。
- 新增 `skill-verification-consensus`（检验底座）：claim-class 证明表、prove-it-can-fail、Skill TDD、红队对抗复核。
- 新增 `dev-workflow-consensus`（开发底座）：Frame→Interview→Plan→Spec→Review→Gate→Build→Verify→Review→Ship 十段强流程。
- 更新 `distillation-consensus` v0.5.0：成品发布门槛与评测任务。
- 更新 `search-source` v0.2.0：来源台账/独立判定/搜索预算/evidence_class。
- 更新 `web-research-consensus` v0.3.0：raw_corpus_entry 增加 evidence_class?。
- 全部入库 vault；validate_contract/behavior/smoke PASS，scorecard 148/180，validate-vault 11 skills OK。

## 2026-09-04 · Round 23-28 · 进化冲刺（工具化 + 收敛）

- Round 23：`scorecard.py` 扩展覆盖基础/新增底座；新增 `skill_package_check.py` 并接入 `smoke_test.py`。
- Round 24：`info_source_cli.py` 新增 `github-file` 适配器（Contents API 拉取文档/源码）；`info-source-adapter` v0.6.0。
- Round 25：新增 `distill_skill_package.py`（Nodes → 完整 Skill 包）；`distillation-consensus` v0.6.0。
- Round 26：新增 `scaffold_eval_task.py`（Skill TDD 任务包）；`skill-verification-consensus` v0.2.0。
- Round 27：新增 `scaffold_dev_spec.py`（开发规格单 + 路径手册）；`dev-workflow-consensus` v0.2.0。
- Round 28：新增 `final_evolution_report.py`（直观终评）；判定 `diminishing_returns` 停止。
- 验证：smoke PASS（scorecard 177/220，package_check PASS），validate-vault 11 skills OK。
- 收敛结论：基础能力已工具化；剩余高价值项（真实 A/B、runner 接入、插件热改）成本高，转人工/隔离阶段。

## 2026-09-04 · Round 29-30 · 指标补强 + 收敛终评

- Round 29：search-source v0.3.0 / dev-workflow v0.3.0 / skill-verification v0.3.0 补齐输出契约、干跑验证与示例。
- Round 30：return-forensics v0.2.0 / value-effect-audit v0.2.0 增加干跑示例；distillation-consensus v0.7.0 规范输出契约并补 examples。
- 终评：scorecard 204/240（12 skills），package_check PASS（95.4），综合 87/100 A 级。
- 判定 diminishing_returns，收敛收口；剩余高价值项须真实评测或插件隔离改造。


## 2026-09-04 · Round 31 · 真实 Skill A/B runner

- 新增 `tools/skilljack_runner.py`：真实 DeepSeek agent 循环（`loadSkill` / `write_file` / `read_file` / `bash`），支持 scaffold task-dir 与 skilljack tasks.yaml，输出 `skill_effect_bench.py` 输入。
- 新增 `tools/benchflow_runner.py`：BenchFlow 式多任务矩阵 + 门禁（Skill Lift、anti-trigger 误触发上限）。
- `scaffold_eval_task.py` verifier/oracle 模板改为 ESM（`import fs from 'node:fs'`）。
- 真实 smoke：DeepSeek 跑通 positive A/B，并捕获到 anti-trigger 误触发（门禁按设计 FAIL）。

## 2026-09-04 · Round 32 · 第一份真实 A/B 证据落盘

- 新增 `evals/dev-security-enforce`（正例）与 `evals/dev-security-anti`（反例）任务包、共享 `evals/skills/dev-security` 挂载。
- 用 DeepSeek `deepseek-chat` 每格 3 次跑 benchflow 矩阵：正例成功率 0% → 100%，反例误触发 0%，增强指数 **23.2%**，门禁 PASS。
- 修复 `skilljack_runner.py` 相对 `verifier/workspace/skill_dir` 路径在子进程 cwd 切换后失效的问题。
- 落盘：`evals/results/dev-security.{ab,combined,result}.json`、`evals/README.md`、`tools/output/ENHANCEMENT_REPORT.*`。
