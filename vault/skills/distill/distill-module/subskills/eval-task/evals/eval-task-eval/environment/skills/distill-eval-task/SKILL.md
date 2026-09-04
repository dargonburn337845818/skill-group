---
name: distill-eval-task
description: 评测任务包制作子技能——把 scaffold_eval_task / skilljack_runner / benchflow_runner 变成可照着做的操作手册，产出任务包、真实 A/B 对照、anti-trigger 与 Skill Lift 解读；聊天记录总结、日常摘要等非评测任务不要加载。
whenToUse: 用户要为某个 Skill 建立评测任务包、跑无 skill/有 skill 对照、做 anti-trigger 防误触发、解读 Skill Lift 或落地评测证据时。
---

# distill-eval-task · 评测任务包制作（已蒸馏）

> 定位：给 distill 模块提供“Skill 真实评测”的可执行操作手册。不复制 runner 实现，只给出调用方式、产物字段、验收口径与常见坑。
> 核心原则：**任务先行、verifier 确定、基线可失败、至少 3 次、anti-trigger 必测、诚实标注——不用模板分数冒充真实 A/B。**

## 触发条件

- 用户要给一个新蒸馏的 Skill 生成 `skilljack-evals` 风格评测任务包。
- 需要判断 Skill 是否真的有用：跑无 skill 基线 vs 有 skill，计算 Skill Lift。
- 需要防止 Skill 在无关任务上误触发（anti-trigger）。
- 需要把评测结果回填进 Skill 的 `CHANGELOG` / `benchmarks` / `qualityCriteria`。

## 前置工具路径

```bash
CORE=$WORKSPACE/skills/core-iteration
VAULT=$PROJECT_ROOT
```

三个核心工具都在 `$CORE/tools/`：
- `scaffold_eval_task.py` — 生成任务包（Skill TDD）
- `skilljack_runner.py` — 单任务/多任务真实 LLM A/B runner
- `benchflow_runner.py` — BenchFlow 式矩阵 runner + 门禁

## 步骤 1 · 任务先行：生成任务包

**先写任务，再写/改 Skill。** 一次至少两组：正向任务 + anti-trigger。

```bash
cd $CORE

# 正向任务：prompt 不能出现 skill 名；checks 用确定性标记
python3 tools/scaffold_eval_task.py \
  --task-id <skill>-enforce \
  --skill-name <skill-id> \
  --prompt "<真实任务描述，不点名 skill>" \
  --checks "contains:SUCCESS_MARKER,files:report.md"

# anti-trigger：无关任务不应调用 skill
python3 tools/scaffold_eval_task.py \
  --task-id <skill>-anti \
  --skill-name <skill-id> \
  --prompt "<明显无关请求，如写诗/起名>" \
  --anti-trigger
```

生成后把被测 Skill 挂进环境：

```bash
mkdir -p evals/<skill>-enforce/environment/skills/<skill-id>
cp $VAULT/vault/skills/<module>/<skill-id>/SKILL.md \
   evals/<skill>-enforce/environment/skills/<skill-id>/SKILL.md
```

## 任务包字段（scaffold_eval_task.py 产物）

```text
<任务根>/evals/<task-id>/
├── task.md                 # frontmatter + prompt
│   - id / difficulty / category / expected_skill
│   - expect_skill_invocation: true | false
│   - checks / assertions / timeout_ms
├── environment/
│   └── skills/<skill-name>/ # 被测 SKILL.md 挂载点（.gitkeep）
├── workspace/              # 可选种子文件
├── verifier/verify.mjs     # 确定性 verifier
└── oracle/solve.mjs        # 参考解 / oracle gate
```

关键字段含义：

| 字段 | 作用 |
|---|---|
| `expected_skill` | 声明该任务应由哪个 Skill 解决 |
| `expect_skill_invocation` | 是否期望模型在轨迹中调用 `loadSkill` |
| `checks` | `contains:...` / `files:...` 等确定性检查 |
| `assertions` | 可选 LLM judge 断言，只做诊断，不改分 |
| `timeout_ms` | 单任务超时 |
| `verifier/verify.mjs` | 权威判分：读 `SKILLJACK_OUTPUT_FILE` / `SKILLJACK_TRAJECTORY_FILE` / `SKILLJACK_REWARD_FILE` |
| `oracle/solve.mjs` | 参考解，用于确认 verifier 能对正确解给 1.0 |

> ⚠️ **默认 verifier 是占位模板**：`scaffold_eval_task.py` 生成的 `verifier/verify.mjs` 只检查 `SUCCESS_MARKER`；`--checks` 会写入 `task.md`，但 runner 在有显式 checks 时以 verifier 结果为权威。因此若你的真实检查不是 `SUCCESS_MARKER`（尤其 `contains:其他标记` / `files:...` 文件类检查），**必须同步替换 `verifier/verify.mjs`**，否则自定义 checks 会被占位 verifier 覆盖。

## 步骤 2 · verifier 与 oracle 校验（先证明检查有效）

0. **先替换占位 verifier**：若 `--checks` 不是 `SUCCESS_MARKER`，先把 `verifier/verify.mjs` 改成真正检查这些标记的版本；否则先按占位 verifier 跑通，再替换重跑。
1. **oracle gate**：先跑 `oracle/solve.mjs`，确认 verifier 对它给 `PASS` 且 reward 1.0；不给 1.0 = 检查写错。
2. **基线能失败**：跑无 skill 基线，确认不是 100% 恒过；基线不失败 = 任务太简单或 verifier 无效。
3. **有 skill 能提升**：跑有 skill，确认确实提升；没有观察到失败/提升的检查 = 无效评测。
4. 复杂任务把 verifier 从 `contains` 升级为检查文件内容/步骤/关键词，但必须保持确定性、可复现、可证伪。

手动 oracle gate 的精确命令（在任务包目录内执行）：

```bash
cd $CORE/evals/<skill>-enforce
node oracle/solve.mjs        # 生成参考输出（默认写 output.txt 的 SUCCESS_MARKER）
node verifier/verify.mjs     # 应输出 PASS 且退出码 0；否则先修 verifier/task
```

## 步骤 3 · 真实 A/B：单任务 runner

`skilljack_runner.py` 对每个任务跑 `no-skill` 与 `with-skill` 两个真实 LLM agent 会话，默认 DeepSeek。**默认跑 3 次，少于 3 次只能标 `single-effect`。**

```bash
# 单任务 A/B（无 skill 基线 + 有 skill）
python3 $CORE/tools/skilljack_runner.py \
  --task-dir evals/<skill>-enforce \
  --mode both \
  --runs 3 \
  --output bench-results/<skill>.json \
  --verbose

# 需要输出质量 judge 时（额外 API 调用）
python3 $CORE/tools/skilljack_runner.py \
  --task-dir evals/<skill>-enforce \
  --mode both --runs 3 --judge \
  --output bench-results/<skill>.json
```

其他模式：
- `--mode no-skill`：只跑基线
- `--mode with-skill`：只跑有 skill
- `--tasks-yaml <file>`：跑 skilljack-evals 的 `tasks.yaml`
- `--skill-dir <dir>`：显式指定技能目录
- `--max-steps` / `--timeout-ms`：限制 agent 步数/超时

输出是 `skill_effect_bench.py` 兼容 JSON（`--mode both`），结构示例：

```json
{
  "tasks": [
    {
      "id": "<skill>-enforce",
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

字段含义：
- `success_*`：确定性 verifier 通过率
- `quality_*`：可选 LLM judge 质量分
- `efficiency_*`：平均 agent 轮数（越低越好）
- `coverage_*`：要求/步骤覆盖度
- `calibration_*`：模型自我信心与真实正确性的校准

## 步骤 4 · BenchFlow 矩阵 runner + 门禁

多任务一张矩阵，每个任务自动跑 no-skill/with-skill，并做 Skill Lift 门禁。

```bash
# 命令行矩阵
python3 $CORE/tools/benchflow_runner.py \
  --task-dir evals/<skill>-enforce \
  --task-dir evals/<skill>-anti \
  --skill-dir $VAULT/vault/skills/<module>/<skill-id> \
  --runs 3 \
  --output results/<skill>.json

# 配置文件门禁
python3 $CORE/tools/benchflow_runner.py --config benchflow.config.yaml
```

`benchflow.config.yaml` 示例：

```yaml
name: <skill>-ab
tasks:
  - dir: evals/<skill>-enforce
  - dir: evals/<skill>-anti
skill_dir: vault/skills/<module>/<skill-id>
runs: 3
model: deepseek-chat
judge: false
thresholds:
  min_lift_percent: 5
  max_discovery_false_positive: 0.5
```

相关 CLI 阈值：
- `--min-lift-percent`：最低增强百分比
- `--max-discovery-false-positive`：anti-trigger 行最大误触发率

产物：
- `*.combined.json`：完整 cell 明细
- `*.ab.json`：`skill_effect_bench.py` 输入
- `*.result.json`：矩阵结果 + bench 报告 + 门禁结果
- 退出码 0 = 门禁通过，1 = 未通过

## 步骤 5 · 汇总评分：Skill Lift

```bash
python3 $CORE/tools/skill_effect_bench.py --input bench-results/<skill>.json
```

会生成 `ENHANCEMENT_REPORT.json/.md`，含：
- 增强指数（Skill Lift，百分比）
- 无 skill / 有 skill 各指标均值
- 逐指标增益与评级（如 明显增强 / 轻微增强 / 无增强）

### Skill Lift 怎么解读

- **正例成功率提升**：`success_with - success_without`，说明技能在目标任务上带来可用增益。
- **anti-trigger 误触发率**：必须低于阈值；无关任务也调用 skill = 不能发布。
- **效率**：有 skill 的轮数不显著高于无 skill，说明使用成本可控。
- **绝对门槛**：至少 3 次、基线可见失败、verifier 是权威。
- **不要**把“模型用了 skill”当成“skill 有效”：必须看 verifier 与 lift。

## 步骤 6 · 回填评测证据

| 回填位置 | 写什么 |
|---|---|
| Skill 目录 `examples/ab/` 或 `benchmarks/` | 任务包 + `ENHANCEMENT_REPORT.md` |
| `CHANGELOG.md` | `skill lift = xx%`、任务集、日期 |
| `manifest.json` `qualityCriteria` | 可加“该 skill 已在 <任务> 上达到 Skill Lift ≥ x%” |
| `value-effect-audit` 的 `node_effects` | 映射到 `promote / demote / delete / needs_more_evidence` |

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “跑 1 次成功就宣布有增益” | 至少 3 次；否则标 `single-effect` |
| “无 skill 也 100% 过” | 说明任务太简单/verifier 无效；先修任务 |
| “只写正向任务” | 必须配 anti-trigger 并检查误触发 |
| “用 LLM judge 分数当发布证据” | 确定性 verifier 是权威，judge 只做诊断 |
| “外部 runner 没配 key 就说已跑外部 skilljack-evals” | 如实写“本地 runner 真实结果 / 外部未配置” |
| “Skill Lift 高 = 知识正确” | 只证明“在该任务上有可测增益且未明显误触发” |

## 来源

- `$CORE/tools/scaffold_eval_task.py --help`
- `$CORE/tools/skilljack_runner.py --help`
- `$CORE/tools/benchflow_runner.py --help`
- `$CORE/tools/skill_effect_bench.py --help`
- `$VAULT/vault/skills/distill/distill-module/real-ab-bench.md`
- `$VAULT/vault/skills/core-iteration/skill-verification-consensus/`
- 本地底座：`$VAULT/vault/skills/base/search-source/`
