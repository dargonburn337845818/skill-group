# 真实 Skill A/B 评测接入方案

> 本文是 `distill-module` 的“真实 A/B 评测”配套文档。
> 目标：**每个回填的模块 Skill 至少有一个任务包 + 无 skill/有 skill 对照 + Skill Lift，不拿“能用”当证据**。

## 1. 现状与目标

- **现状**：core-iteration 已有四个可执行层：
  - `tools/scaffold_eval_task.py`：生成 skilljack-evals 风格任务包（Skill TDD）；
  - `tools/skilljack_runner.py`：**真实 runner**，用 DeepSeek API 跑 agent 循环（`loadSkill` / 文件 / bash），输出真实 A/B 数据；
  - `tools/benchflow_runner.py`：**BenchFlow 式矩阵 runner**，把多个任务包批量跑成 Skill Lift 矩阵并做门禁；
  - `tools/skill_effect_bench.py`：把任务级指标汇总成增强指数。
- **目标**：每个回填的模块 Skill 至少有一个任务包，经 `skilljack_runner` + `benchflow_runner` 跑出真实 Skill Lift。

## 2. 任务包规格（scaffold_eval_task.py 产物）

```text
<任务根>/evals/<task-id>/
├── task.md                 # frontmatter + prompt（prompt 不指名 skill）
│   - id / difficulty / category / expected_skill
│   - expect_skill_invocation: true|false
│   - checks / assertions / timeout_ms
├── environment/
│   └── skills/<skill-name>/ # 把被测 SKILL.md 挂到这里
│       └── .gitkeep
├── verifier/verify.mjs     # 确定性 verifier（读 SKILLJACK_OUTPUT_FILE / REWARD_FILE）
└── oracle/solve.mjs        # 参考解，oracle gate 用
```

## 3. 建任务包（一步命令）

```bash
cd $WORKSPACE/skills/core-iteration

# 常规任务：prompt 不出现 skill 名；checks 用确定性标记
python3 tools/scaffold_eval_task.py \
  --task-id dev-security-enforce \
  --skill-name dev-security \
  --prompt "给这段部署配置做安全评审，输出必须包含 CHECKLIST 与至少 3 条风险" \
  --checks "contains:CHECKLIST,files:report.md"

# 反触发任务：无关任务不应调用 skill
python3 tools/scaffold_eval_task.py \
  --task-id dev-security-anti \
  --skill-name dev-security \
  --prompt "帮我写一首关于春天的诗" \
  --anti-trigger
```

生成后：

```bash
# 挂被测 SKILL.md
cp vault/skills/dev/dev-security/SKILL.md evals/dev-security-enforce/environment/skills/dev-security/SKILL.md
```

## 4. 确定性 verifier 与 oracle gate

- `verifier/verify.mjs` 读环境变量：
  - `SKILLJACK_OUTPUT_FILE`（默认 `output.txt`）
  - `SKILLJACK_TRAJECTORY_FILE`
  - `SKILLJACK_REWARD_FILE`
- 校验步骤：
  1. 先跑 `oracle/solve.mjs`，确认 verifier 对它给 `PASS / reward 1.0`；不给 1.0 说明检查写错，先修任务。
  2. 跑“无 skill 基线”确认不是 100% 恒过（它必须能失败）。
  3. 跑“有 skill”确认确实提升；没有观察到失败或提升的检查 = 无效评测。
- 若任务复杂，把 verifier 从 `contains:SUCCESS_MARKER` 升级为检查文件内容/步骤/关键词，但必须保持确定性与可证伪。

## 5. 真实 A/B 运行

`skilljack_runner.py` 会对每个任务跑 `no-skill` 与 `with-skill` 两个真实 LLM agent 会话，默认使用 DeepSeek：

```bash
CORE=$WORKSPACE/skills/core-iteration

# 单任务 A/B（无 skill 基线 + 有 skill；默认 3 次）
python3 $CORE/tools/skilljack_runner.py \
  --task-dir evals/dev-security-enforce \
  --mode both \
  --runs 3 \
  --output bench-results/dev-security.json \
  --verbose

# 需要输出质量 judge 时
python3 $CORE/tools/skilljack_runner.py \
  --task-dir evals/dev-security-enforce \
  --mode both --runs 3 --judge --output bench-results/dev-security.json
```

产出的 `bench-results/dev-security.json` 就是 `skill_effect_bench.py` 的输入格式：

```json
{
  "tasks": [
    {
      "id": "dev-security-enforce",
      "success_without": 0.53,
      "success_with": 0.83,
      "quality_without": 52,
      "quality_with": 78,
      "efficiency_without": 9,
      "efficiency_with": 6,
      "coverage_without": 0.4,
      "coverage_with": 0.65,
      "calibration_without": 0.55,
      "calibration_with": 0.8
    }
  ]
}
```

汇总评分：

```bash
python3 $CORE/tools/skill_effect_bench.py --input bench-results/dev-security.json
```

输出 `ENHANCEMENT_REPORT.json/.md`：增强指数、无 skill/有 skill 分、逐指标增益与评级。

### 已落地示例（2026-09-04）

- 任务包：`core-iteration/evals/dev-security-enforce`（正例）+ `core-iteration/evals/dev-security-anti`（反例）。
- 结果：增强指数 **23.2%**（明显增强），门禁 PASS；正例成功率 0% → 100%，反例误触发 0%。
- 完整矩阵与门禁：`core-iteration/evals/results/dev-security.result.json`；复现入口 `core-iteration/evals/benchflow.config.yaml`。

## 6. skilljack-evals 兼容

- 本仓库的 `skilljack_runner.py` 已实现与 skilljack-evals 同维度的评测：discoverability（`loadSkill` 是否被真实调用）、adherence（verifier/LLM judge）、output quality（可选 judge）。
- 外部 `@skilljack/evals` CLI 仍可作为备选 runner，但它需要 Anthropic/OpenAI/OpenRouter 等 key；本机没有这些 key，因此默认使用 DeepSeek 本地 runner。
- `scaffold_eval_task.py` 生成的 `task.md` 会被 `skilljack_runner.py` 直接消费；`--tasks-yaml` 也支持技能方提供的 skilljack YAML 任务文件。
- 若未来配置了外部 key，可用真实 CLI 跑同一任务集，再把结果接入 `skill_effect_bench.py` 对比。

## 7. BenchFlow 矩阵 runner（已实现）

`benchflow_runner.py` 就是本地 BenchFlow 式编排层：

```bash
CORE=$WORKSPACE/skills/core-iteration

# 多个任务包一张矩阵：每个任务都自动跑 no-skill/with-skill
python3 $CORE/tools/benchflow_runner.py \
  --task-dir evals/dev-security-enforce \
  --task-dir evals/dev-security-anti \
  --skill-dir vault/skills/dev/dev-security \
  --runs 3 \
  --output results/dev-security.json

# 门禁：增强指数 + anti-trigger 误触发上限
python3 $CORE/tools/benchflow_runner.py \
  --config benchflow.config.yaml
```

`benchflow.config.yaml` 示例：

```yaml
name: dev-security-ab
tasks:
  - dir: evals/dev-security-enforce
  - dir: evals/dev-security-anti
skill_dir: vault/skills/dev/dev-security
runs: 3
model: deepseek-chat
judge: false
thresholds:
  min_lift_percent: 5
  max_discovery_false_positive: 0.5
```

产出：

- `*.combined.json`：完整 cell 明细；
- `*.ab.json`：`skill_effect_bench.py` 输入；
- `*.result.json`：矩阵结果 + bench 报告 + 门禁结果；
- 退出码 0=门禁通过，1=未通过。

边界：BenchFlow 只负责调度与门禁，**不替代 verifier/学理判断**；门禁阈值不得由“感觉”定。

## 8. 回填评估证据

评测完成并满足门槛后：

| 回填位置 | 写什么 |
|---|---|
| Skill 目录 `examples/ab/` 或 `benchmarks/` | 任务包 + `ENHANCEMENT_REPORT.md` |
| `CHANGELOG.md` | 记录 `skill lift = xx%`、任务集、日期 |
| `manifest.json` `qualityCriteria` | 可加“该 skill 已在 <任务> 上达到 Skill Lift ≥ x%” |
| `value-effect-audit` 的 `node_effects` | 把任务结果映射到 `promote / demote / delete / needs_more_evidence` |

## 9. 评测纪律（等价于发布门槛）

1. **任务先行**：先写任务包，再写/改 SKILL.md；避免“先有结论再找证据”。
2. **无 skill 基线必须能失败**：跑不到失败说明任务太简单或 verifier 无效。
3. **至少 3 次**：1 次成功不算增强；样本 <3 只能标 `single-effect`。
4. **anti-trigger 必测**：无关任务不得触发 skill；不通过则不得发布。
5. **确定 verifier 是权威**：LLM judge 只做诊断，不改分；verifier 崩溃时必须按“未验证”处理，不得当作 FAIL 硬吞。
6. **诚实标注**：本地 runner 已真实调用 DeepSeek；外部 skilljack-evals/BenchFlow 未配置 key 时如实写“未接外部 runner”，不用模板分数冒充真实 A/B。
7. **评测通过 ≠ 知识正确**：只证明“这个 Skill 在该任务上有可测增益，且未明显误触发”。

## 10. 验证命令清单

```bash
CORE=$WORKSPACE/skills/core-iteration

# 1) 任务包脚手架
python3 $CORE/tools/scaffold_eval_task.py --task-id <id> --skill-name <skill> --prompt "..." --checks "..."
python3 $CORE/tools/scaffold_eval_task.py --task-id <id>-anti --skill-name <skill> --prompt "..." --anti-trigger

# 2) 真实 runner：单任务 A/B
python3 $CORE/tools/skilljack_runner.py --task-dir <task-dir> --mode both --runs 3 --output <bench.json>

# 3) 真实 runner：多任务矩阵 + 门禁
python3 $CORE/tools/benchflow_runner.py --config benchflow.config.yaml

# 4) 包结构/契约
python3 $CORE/tools/skill_package_check.py <skill-dir>
python3 $CORE/tools/validate_contract.py $CORE

# 5) 汇总
python3 $CORE/tools/skill_effect_bench.py --input <bench.json>

# 6) 仓库级校验
cd $PROJECT_ROOT && node scripts/validate-vault.mjs
```
