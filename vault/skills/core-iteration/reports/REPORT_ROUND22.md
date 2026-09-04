# Round 22：基础 skill 综合迭代 · 搜索/蒸馏/检验/开发

> 用户显式覆盖 Round 21 STOP（`override: user`），并切换新的信息范围：从“单主题 GitHub 情报”转向“Agent Skill 工程化 / 验证 / 开发工作流最佳实践”。

## 输入与信息范围

- **模式**：manual + live source 采集（经 Watt host 代理读取 GitHub 一手文档）
- **信息范围**：skill authoring / skill evals / verification standards / dev workflow
- **原始语料**：10 条（`info_dump_round22.json`）
- **来源**：
  - WordPress agent-skills authoring-guide
  - Anthropic Skill authoring best practices + shipyard 摘要 + apply-anthropic
  - skilljack-evals（Skill TDD / Skill Lift / anti-trigger）
  - claude-workflow-kit（evidence-first / claim-class / gates）
  - uinaf agents skill-audit best-practices
  - Promptfoo Red Team Coding Agents
  - 本地 `work-consensus`、`dsh-optimization-consensus`

## 六阶段结果

| 阶段 | 结果 |
|---|---|
| benefit-filter | raw=10，verified_high=7，verified_single=3，pending=0（按证据分级人工过滤） |
| distillation | 5 个能力节点：`skill-verification-consensus`、`dev-workflow-consensus`、`distillation-consensus v0.5`、`search-source v0.2`、`web-research-consensus v0.3` |
| iterator | **effective_new=5**，accepted=true（4 个新增/更新能力 + 1 个契约增强） |
| validator | **CONTINUE**，未触发四条硬规则；建议下一步补真实 A/B 与路由接入 |
| forensics | root_cause=corpus_exhausted 已解除；新提示：skill 评估缺真实 Lift 数据 |
| meta_report | 直观能力分预计 90+；smoke scorecard **148/180**（较 Round21 +2） |

## 本轮交付

### 新增（2 个辅助底座）

1. **`skill-verification-consensus` v0.1.0（检验）**
   - claim-class 证据分类表（static/runtime/data/rendering/tooling）
   - prove-it-can-fail 可证伪检查
   - Skill TDD：任务先行、无 skill 基线、Skill Lift、anti-trigger、oracle gate
   - 红队对抗复核 + 发布门槛
   - 已入库 `dsh-skill-vault/vault/skills/core-iteration/skill-verification-consensus/`

2. **`dev-workflow-consensus` v0.1.0（开发）**
   - Frame→Interview→Plan→Spec→Adversarial Review→Gate→Build→Verify→Review→Ship
   - 模块地图/接口即测试面/子代理分层/churn-breaker/commit-spec gates/终验
   - 已入库 `dsh-skill-vault/vault/skills/core-iteration/dev-workflow-consensus/`

### 更新（3 个基础 skill）

3. **`distillation-consensus` v0.4.0 → v0.5.0**
   - SKILL.md 增加“成品发布门槛（Skill Packaging & Eval）”
   - CONSENSUS.md 新增第 8 节：元数据、渐进披露、任务先行评测、发布验证
   - workspace + vault impl 同步

4. **`search-source` v0.1.0 → v0.2.0**
   - 增加“来源台账与独立判定”“搜索预算”“evidence_class”
   - 引用纪律与优雅降级补充

5. **`web-research-consensus` v0.2.0 → v0.3.0**
   - `raw_corpus_entry` 输出契约增加 `evidence_class?`
   - workspace + vault impl 同步

## 验证

- `validate_contract.py`：PASS
- `behavior_test.py`：PASS
- `smoke_test.py`：contract=PASS，scorecard=148/180
- `validate-vault.mjs`：OK（11 skills validated）

## 状态与下一步

- `round_ledger.json` 更新为 Round 22，decision=CONTINUE。
- 建议下一步：
  1. 接真实 Skill 评测（skilljack-evals 风格任务包）替换模板增强指数；
  2. 将 `dev-workflow-consensus` / `skill-verification-consensus` 接入 dsh-skill-router 的 dev/core 提示（插件侧变更需按运维共识隔离冒烟）；
  3. 对搜索/蒸馏/检验三件套补 3+ 个真实 dry-run 反例。
