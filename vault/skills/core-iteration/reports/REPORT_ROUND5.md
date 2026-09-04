# 核心迭代元能力 · Round 5：元能力扩展（执行/检验/根因/思维链）

> 日期：2026-09-04 ｜ 性质：post-convergence 扩展 ｜ 验证：contract PASS + behavior PASS

## 分析结论：需要增改什么

当前六件套已覆盖“搜→滤→蒸→迭→校→调”，但有三类真实缺口：

1. **信息搜集停留在文档层**：`web-research-consensus` 教你怎么查，但缺少“真正去 GitHub/OSV/包生态抓数据”的执行层。
2. **价值计算停留在静态预估**：`benefit-filter` 按密度/来源打分，但没有“放到真实任务里测效果”的反馈回路。
3. **收益下降无法归因**：`value-validator` 只说 STOP，不说“为什么下降、卡在哪、下一步该做什么”；知识节点也缺少从“来源→验证→应用→效果”的可追溯链条。

因此新增三个扩展元能力，并强化思维链与代码自检。

## 新增

### `info-source-adapter` v0.1.0
- 把 GitHub 搜索/代码/Issue/Release、Security Advisories、OSV、包生态、学术库、OSS 社区串成**可调用适配器**。
- 统一输出 `raw_corpus` 与 `source_scope_report`，记录查询量、限流、降级情况。
- 明确：stars/forks/downloads 不是证据，真正证据是源码/commit/release/安全公告。

### `value-effect-audit` v0.1.0
- 在真实任务中测量 Skill/节点是否真的改变行为。
- 用任务成功率 + 多方独立证据计算 `effect_score` 与 `node_info_value`。
- 输出 `feedback_to_iterator`：`promote / demote / delete / needs_more_evidence`，把“静态密度评分”升级为“实际效果打分”。

### `return-forensics` v0.1.0
- 诊断收益下降六类根因：`corpus_exhaustion`、`filter_over_tight`、`distillation_loss`、`source_saturation`、`interface_mismatch`、`scope_drift`（外加 `negative_effect`、`no_real_delta`）。
- 输出 `trace_chains`：把“来源→验证→蒸馏→应用→效果”串成可审计思维链。

## 强化

- `value-iterator` / `distillation-consensus` 的 Node 增加 `trace_chain` 与 `effect_ref?`，让每条知识都能回答“怎么来的、凭什么信、用在哪、效果如何”。
- `value-meta-scheduler` 增加“扩展元能力”表，说明三个扩展的接入时机。
- `tools/scorecard.py` 与 `tools/validate_contract.py` 扩展为 9 个 skill。
- 新增 `tools/behavior_test.py`：用代码真实跑一轮合成六阶段行为测试，验证接口与思维链字段。

## 为什么收益会减少（本轮给出的回答框架）

收益下降通常不是“没东西可学”，而是以下之一：

- **源饱和**：总在同类入口（只有博客/只有 GitHub）找，没有新独立视角 → 扩大 `info_scope`。
- **过滤过严**：大量语料被低密度/单源规则丢弃 → 用 `value-effect-audit` 复核“被丢弃的是否真的无用”。
- **蒸馏损耗**：verified 很多，但切出来的 Node 不满足三件套/不能改变行为 → 重蒸馏，而不是继续搜。
- **接口失配**：字段改名/契约断裂，导致下游拿到 null → `validate_contract` 会抓住。
- **范围漂移**：目标变了，旧节点不再相关 → 重新定义目标，保留分支。
- **纯改写**：只是换说法 → 校验器 STOP，不要粉饰。

## 验证

- `tools/validate_contract.py`：**PASS**（9 个 skill）
- `tools/behavior_test.py`：**PASS**（合成六阶段 + trace_chain 断言）
- `tools/smoke_test.py`：**PASS**
- 自动评分卡（9 skill）：总分 **146 / 180**，平均 **16.22**；原六件套仍为 **102 / 120**。

## 产物

- 正式库：`$PROJECT_ROOT/vault/skills/core-iteration/`
- 工作区源：`$WORKSPACE/skills/core-iteration/`（同步）
- 新增 skill：`info-source-adapter/`、`value-effect-audit/`、`return-forensics/`
- 新增工具：`tools/behavior_test.py`
- 报告：`REPORT_ROUND5.md`

## 下一步建议

1. 把 `info-source-adapter` 的适配器做成真正可跑的脚本/插件（GitHub API、OSV API、包元数据 API），接入 DSH 工具链。
2. 用 `value-effect-audit` 对现有六件套做一次真实使用回测，给每个节点打“实际效果分”。
3. 用 `return-forensics` 分析前三轮收益曲线，验证根因矩阵是否与实际一致。
