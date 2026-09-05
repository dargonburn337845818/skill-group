# 真实 Skill A/B 评测 · dev-security

> 本目录是 `skill-effect-bench / 真实 Skill A/B 评测` 的第一份真实落盘证据。
> 运行方：本地 `skilljack_runner.py` + `benchflow_runner.py`，模型：DeepSeek `deepseek-chat`，每格 3 次。

## 结果摘要（2026-09-04）

| 任务 | 无 skill 成功率 | 有 skill 成功率 | 无 skill 触发 | 有 skill 触发 |
|---|---|---|---|---|
| dev-security-enforce（安全评审） | 0% | 100% | 0% | 100% |
| dev-security-anti（写诗反触发） | 100% | 100% | 0% | 0% |

- 增强指数：**23.2%（明显增强）**
- 门禁：**PASS**（最小增益 5% 通过；anti-trigger 误触发上限 0）
- 任务成功率 +50pp；能力覆盖 0 → 50%（正例激活率 100%，反例 0%）
- 注意：LLM judge 输出的“输出质量”下降（75.8 → 66.7），效率变差（2.0 → 2.5 轮）
  —— 说明 skill 换来的是结构化与可验证覆盖，不一定是“更好看”的文本；这类指标应结合任务成功率一起看，不能只追单一分数。

## 证据文件

- `dev-security-enforce/`：正例任务包（task.md + verifier + oracle + 被测 SKILL.md）
- `dev-security-anti/`：反触发任务包
- `skills/dev-security/`：反触发 with-skill 模式挂载的 skill（共用）
- `results/dev-security.ab.json`：`skill_effect_bench.py` 输入
- `results/dev-security.combined.json`：完整矩阵 cell 明细
- `results/dev-security.result.json`：矩阵 + bench + 门禁结果
- `../tools/output/ENHANCEMENT_REPORT.md/.json`：增强指数报告

## 专家决策评测（2026-09-05）

- `expert-decision-enforce/`：正例任务——要求输出九段决策环关键阶段与 `decision_log_entry`，验证“规范流程是否被真正落到产出”。
- `expert-decision-anti/`：反触发任务——简单事实问答不应触发完整决策环。
- verifier 已做过可证伪检查：缺少阶段标记会 FAIL，完整报告 PASS；反例混入决策环标记会 FAIL。
- 待跑 A/B：`expert-decision-enforce` 需要以后补无 skill vs 有 skill 的 Skill Lift 数据。

## 复现命令

```bash
cd $PROJECT_ROOT/vault/skills/core-iteration
python3 tools/benchflow_runner.py --config evals/benchflow.config.yaml --verbose
```

依赖：`DEEPSEEK_API_KEY`（env 或 `~/.dsh/.credentials.yaml`）、Node 22+、PyYAML。

## 评测纪律

- 确定性 verifier 是权威；LLM judge 只做诊断，不参与门禁。
- 正例 verifier 已验证“oracle 通过、删掉关键标记会失败”（可证伪）。
- 反例 verifier 已验证“纯诗通过、混入安全标记会失败”。
- 任务先行：先写任务包，再跑 A/B；结果保留，不拿模板分数冒充。
