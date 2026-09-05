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

## 2026 深度补强（Round 40）

> 本轮把 Anthropic 的 agent evals 方法论、统计误差建议、基础设施噪声实验，以及 SWE-bench 的 F2P/P2P 口径和 GroundEval 的确定性替代思路，折成本子技能可直接执行的检查、清单与反例。原有步骤保留，这里只做口径补充。

### 补强 1 · 先分清能力评测与回归评测，再选任务

- **能力评测（capability/quality eval）**回答“这个 Skill 能不能把本来容易失败的任务救回来”，起跑点应是低通过率，任务要选“无 skill 时会失败、有 skill 有机会成功”的坡度任务。
- **回归评测（regression eval）**回答“用了 Skill 后，原来能过的行为是否仍然能过”，应接近 100% 通过；它只用来防回退，不能用来证明增益。
- 检查清单：
  - [ ] 每个正向任务先跑无 skill 基线，确认 `0 < baseline < 1`（既不是恒过也不是恒挂）。
  - [ ] 任务集里区分“能力任务”（期望低基线）与“回归/anti 任务”（期望高通过、低误触发），并在最终报告里分别呈现。
  - [ ] 如果一个正向任务在无 skill 基线已经是 100%，只能把它的角色降为回归任务，不能算 Skill Lift 的证据。
- 反例：拿一组“有 skill 和无 skill 都能 100% 通过”的简单任务算 lift，得到 0%，并由此说“Skill 无效”。正确做法是换到有坡度、基线可见失败的能力任务，或用这批任务做回归门禁。

### 补强 2 · verifier 按 FAIL_TO_PASS / PASS_TO_PASS 成对设计

- SWE-bench 的判分口径是“修复了原来失败的测试，且没有弄坏原来通过的测试”。映射到 Skill 评测，verifier 必须同时具备两类检查：
  - **F2P（fail-to-pass）**：无 skill 时失败/缺失，有 skill 时必须通过——这是 Skill 的增益点。
  - **P2P（pass-to-pass）**：无 skill 基线已通过，有 skill 后仍必须通过——这是防回退点。
- 检查清单：
  - [ ] 每个正向任务至少含 1 个 F2P 检查；如果一个正向任务只有 P2P，说明它测不出 Skill 的独有贡献。
  - [ ] 每组 anti/回归任务至少含 1 个 P2P 检查；有 skill 后 P2P 翻车即回归。
  - [ ] 报告同时给出“F2P 通过率变化”与“P2P 回退数”，不要只报总通过率。
- 反例：verifier 只查 `contains:SUCCESS_MARKER`，模型输出一个标记但没完成真实动作也能拿 1.0；这等于用字符串偶合替代了可证伪的 F2P/P2P 行为。

### 补强 3 · 评最终状态而不是执行路径，复杂任务给 partial credit

- 确定性 verifier 优先检查**最终状态/产物**：文件内容、数据库状态、结果对象、日志事件、页面/API 状态；不要硬编码“必须先调用工具 A 再调用工具 B”的精确顺序。
- Anthropic 的实践表明：对工具调用顺序过度约束会让评测变得脆弱，模型经常用评测设计者没预料到的等价路径完成同一件事；这些“没按剧本走”的解被误判为失败，测的其实是脚手架，不是 Skill。
- 对多组件任务设置中间档分数：例如“找到并验证了客户，但退款没有处理成功”应高于“第一步就失败”。verifier 可以分层计分，输出 partial success，而不是只有一个布尔。
- 检查清单：
  - [ ] verifier 以状态/产物断言为主；只有确实要测行为习惯时才追加轨迹断言。
  - [ ] 轨迹断言允许等价路径，不使用精确工具顺序/精确工具名作为唯一门槛。
  - [ ] 复杂任务有中间档计分，报告允许看到“部分成功”比例，而非只有 0/1。
- 反例：要求“必须使用 read_file 再 edit_file 且顺序固定”；Skill 换用 grep + write_file 的等价路径后被判 0，Skill Lift 被人为压低。

### 补强 4 · A/B 环境冻结 + 基础设施错误单列

- Anthropic 的基础设施噪声实验显示：仅资源配额/执行方式不同，就能让 Terminal-Bench 2.0 的成绩波动约 6 个百分点（p < 0.01），超过许多榜单头名之间的差距。no-skill 与 with-skill 若跑在不同环境，A/B 不成立。
- 检查清单：
  - [ ] no-skill 与 with-skill 除“是否挂载被测 SKILL.md”外完全一致：同一任务目录、同一模型、同一温度、同一最大步数、同一超时、同一沙箱/镜像、同一 CPU/内存配额。
  - [ ] 每个 trial 从干净环境开始：清理临时文件、缓存、git history、残留进程；禁止跨 trial 共享状态，防止伪成功或相关失败。
  - [ ] 基础设施失败（超时、OOM、工具崩溃、网络错误）单独统计为 infra error rate，不计入 skill 成功/失败；两边 infra error 若差异大，先修环境再读 lift。
  - [ ] 结果文件记录资源规格与资源执行策略（floor/ceiling、是否允许临时超额），否则换一个环境可能重排结论。
- 反例：with-skill 跑在高配容器、no-skill 跑在低配容器，最终“有 skill 提升 6pp”，实际是资源差异；应把两臂资源一致后再跑。

### 补强 5 · 3 次只是下限：报配对差值、误差范围、pass@k / pass^k

- 3 次是“不标 single-effect”的门槛，不是统计显著性的证据；n=3 的二元通过率区间很宽（例如 3/3 的 95% CI 约 [0.29, 1.00]），只够做初步信号。
- 使用**配对差值**：同一任务、同一环境、同一模型配置下，逐任务计算 `with-skill - no-skill`，可消掉任务难度方差；报告至少给出 mean diff、逐任务配对结果，最好再给 SEM/95% CI。
- 区分两个指标并说明用哪个：
  - `pass@k`：k 次尝试中至少成功 1 次；适合“一次成功就算成功”的工具型 Skill。
  - `pass^k`：k 次尝试全部成功；适合“每次都要稳定”的发布门禁。
  - 两者随 k 增大方向相反，混用会误导结论。
- 检查清单：
  - [ ] 报告不写单个点估计，而写 `n`、pass@1/pass^k、逐任务配对差与误差范围（或明确写“当前样本未达显著，证据等级为 indicative”）。
  - [ ] 门禁阈值要用同一口径定义：如果要发布可靠性，用 pass^k 或全通过门禁；如果要证明“有机会提升”，用 pass@k 并说明。
  - [ ] 结果回填 `value-effect-audit` 时按证据等级选 `needs_more_evidence` 或 `promote`，不要把 3 次观测直接写成确定的“Skill Lift = xx%”。
- 反例：无 skill 0/3、有 skill 3/3 就写“Skill Lift 100%”。正确写法是 `n=3，观测 0→1.0，通过率 95% CI 仍可能从约 29% 到 100%，当前为 indicative`，并标注需扩大任务数/试次数后再定级。

## 来源

- `$CORE/tools/scaffold_eval_task.py --help`
- `$CORE/tools/skilljack_runner.py --help`
- `$CORE/tools/benchflow_runner.py --help`
- `$CORE/tools/skill_effect_bench.py --help`
- `$VAULT/vault/skills/distill/distill-module/real-ab-bench.md`
- `$VAULT/vault/skills/core-iteration/skill-verification-consensus/`
- 本地底座：`$VAULT/vault/skills/base/search-source/`
