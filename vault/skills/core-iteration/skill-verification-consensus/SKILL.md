---
name: skill-verification-consensus
description: 检验与验证共识——用证据分类、可证伪检查、任务先行评测与红队对抗规格审查来判断“交付物/技能是否真实可靠”；用于技能发布前校验、代码或文档验收、审计“是否真的验证过”。
whenToUse: 发布/更新 Skill 前需要检验、用户要求“校验/质检/红队/审计”、需要判断某个验证是否可信、或想给交付物建立可执行验收门槛时。
---

# 检验与验证共识（Verification Consensus）

> 目标：把“我验证过了”变成“有证据、可复现、可证伪的验证”。
> 本 skill 是核心迭代的检验底座；也适用于代码、文档、数据、插件等任何交付物。

## 触发条件

- 蒸馏/开发完成后、发布前：需要判断“这个 Skill/交付物是否真的可靠”。
- 用户说“帮我校验/质检/红队/审计/挑刺”。
- 对某个验证结论存疑：它真的跑过了吗？证据是否支持结论？
- 需要建立评测任务集（eval scenarios）测量技能增益。

## 核心公式

```text
可信验证 = 证据分类（claim class）+ 唯一可接受证明 + 可证伪检查 + 独立复现/对抗复核
```

### 证据分类与可接受证明

| 主张类型 | 唯一可接受证明 |
|---|---|
| 静态（代码/配置/结构） | 上游源码/commit/config 原文，可定位到行/版本 |
| 运行时（行为/交互） | 真实运行输出/测试记录 + 命令与退出码 |
| 数据（性能/指标/分布） | 可复算的测量数据、基准脚本、样本口径 |
| 渲染/产物（UI/文档/报表） | 实际产物截图/文件 + 生成命令与校验 |
| 工具链（依赖/版本/API） | 已安装版本/命令 `--version`/文档版本号 |

每类主张只能用表中的证明；不能用“我感觉”“README 说”替代。

## 核心动作（五步）

1. **列主张**：把交付物拆成“它声称成立”的断言，逐条标 claim class。
2. **配证明**：每条断言指定唯一可接受证明；无法配证明的降级为“未验证/待证”。
3. **可证伪检查**：对一个检查做“突变测试”：故意破坏它，确认变红；恢复，确认变绿。没见它失败的检查 = 只被运行过，不等于被验证。
4. **任务先行评测（Skill 专用）**：先写 eval 场景（prompt + 确定性 checks），跑无 skill 基线 vs 有 skill；测分辨率/技能增益，加 anti-trigger 任务防误触发。
5. **红队/对抗复核**：对规格做对抗审查（BLOCKER/GAP/NOTE），由独立视角审“改了之后是否又引入新问题”；verify=redteam 时禁止自写自过。

## 输出契约（校验报告）

```text
{
  "target": "skill-id / 模块 / 交付物",
  "claims": [
    { "claim": "...", "class": "static|runtime|data|rendering|tooling",
      "proof": "可复现证明", "verdict": "verified|unverified|failed",
      "gap": "未验证原因或缺失证据" }
  ],
  "checks_observed_red": ["check-id"],        # 做过突变测试、见过失败的检查
  "evals": { "tasks": n, "baseline": 0.xx, "with_skill": 0.xx, "lift": 0.xx,
             "anti_trigger": "pass|fail" },
  "adversarial_review": { "blockers": [], "gaps": [], "notes": [] },
  "overall": "pass|needs_work|reject",
  "next_actions": ["补证明", "补评测", "修边界", "人工复核"]
}
```

- 只有 `checks_observed_red` 中的检查才能写“已验证”；否则写“已运行，未验证”。
- `overall` 由硬门槛决定：任何 `failed` 或未完成的反向检查 → reject/needs_work。

## 可执行工具（检验底座落地）

```bash
# 1) 检查一个/一批 Skill 包的结构、manifest、三件套与来源纪律
python3 "\$CORE_ITERATION_ROOT/tools/skill_package_check.py" <skill-dir> [more-dirs...]

# 2) 为 Skill 先建评测任务（prompt + deterministic checks + anti-trigger）
python3 "\$CORE_ITERATION_ROOT/tools/scaffold_eval_task.py" --task-id my-task --skill-name my-skill \
  --prompt "真实任务描述" --checks "contains:SUCCESS_MARKER,files:out.txt"
```

- `skill_package_check.py` 输出 `ok/issues/warnings/score`，任一 issue 即 `ok=false`。
- `scaffold_eval_task.py` 生成 skilljack-evals 风格任务包；评测跑通后再进入发布。

真实 runner（本地 DeepSeek 执行层）：

```bash
# 单任务 A/B
python3 "\$CORE_ITERATION_ROOT/tools/skilljack_runner.py" --task-dir evals/<task> --mode both --runs 3 --output ab.json

# 多任务矩阵 + 门禁
python3 "\$CORE_ITERATION_ROOT/tools/benchflow_runner.py" --config benchflow.config.yaml
```

## 干跑验证（对接 core-iteration 收口）

1. 对目标 Skill 跑 `skill_package_check.py`，确认 `ok=true`。
2. 对关键检查做一次“故意破坏→变红→恢复→变绿”，把 id 记入 `checks_observed_red`。
3. 用 `scaffold_eval_task.py` 建至少 1 个 eval + 1 个 anti-trigger 场景；有 runner 时再跑基线。
4. 输出校验报告给 `core-iteration` 调度器，`overall=pass` 才允许发布。

## 质量检查表（发布门槛）

- [ ] metadata：description 第三人称、含“做什么 + 何时触发”；名称具体可读。
- [ ] Body 简短可执行：SKILL.md 偏索引/流程；细节放 references，引用只保持一层。
- [ ] 每条规则有 trigger/action/boundary/source_refs。
- [ ] 至少 1 个 eval 场景（有预期输出的确定性检查）；复杂 Skill 至少 3 个。
- [ ] 至少 1 个 anti-trigger 场景（无关任务不应触发该 skill）。
- [ ] 每个机械可判断的点已用脚本/命令，不用模型“猜”。
- [ ] 来源可追溯：不是同源转载、不是无来源断言。
- [ ] CHANGELOG/manifest 版本可审计；无死引用/过期命令。
- [ ] 有反例/失效边界；生成物经过 3 个样例干跑。

## 边界

- 本 skill 不替代领域判断；它只保证“证据链完整、验证可复现”，不保证知识本身正确。
- “验证通过”永远针对具体声明与版本；换环境/版本后需重验。
- 评测分数不是唯一标准：确定性 verifier 是权威，LLM judge 只做诊断、不改分。
- 无法找到证明时，诚实写“未验证”，不得通过措辞包装成已验证。

## 简单用户话术

> 我不会只给你一句“验证过了”。我会把结论拆成具体主张，给每条配上它唯一可接受的证据，并且做一次“故意破坏看它会不会红”的检查；只有见过它失败又能恢复的检查，我才承认它被验证过。
>
> 如果哪条你觉得不对劲，请说“我感觉不对劲”，我会重新核验而不是硬套模板。

## 2026 深度补强（Round 37）

> 本轮的硬增量：把“验证过”再分级为可观测阶梯，给每个检查定义“怎么把它弄红”，并把 Skill TDD、agent 轨迹与红队都落成可审计证据。新增来源见 `SOURCES.md`「Round 37 新增来源」。

### R37-1 验证阶梯：claim 必须带 level

在输出契约里，每条 claim 除 `class` 外增加 `level`：

| level | 含义 | 能否写 verified |
|---|---|---|
| L0 ran | 只运行过，无 oracle | 否 |
| L1 asserted | 有确定性断言，但从未见过它失败 | 否 |
| L2 mutation-observed | 做过“故意破坏→变红→恢复→变绿” | 是（默认门槛） |
| L3 reproduced | 换环境/换执行者/换 seed 复现成功 | 是（runtime/data 硬门槛） |
| L4 adversarial-pass | 独立红队按风险类目攻击未破 | 是（安全/越权/隐私/边界硬门槛） |

- 报告里 `level` 缺省即 L0；只有 L2 及以上可写 `verified`。
- `runtime`/`data` 类 claim 至少 L3；`安全、隐私、权限、注入、逃逸` 类至少 L4。
- 来源：Inspect `match/exact/pattern` 确定性 scorer、Stryker mutation testing、SWE-bench 的 `FAIL_TO_PASS/PASS_TO_PASS` 型执行验证。

### R37-2 oracle 优先级：可执行 > 人工 > 模型打分

写断言前先问“这个结论能不能用脚本判”？三类 oracle 按优先级降序：

1. **executable**：脚本/单元测试/容器内运行/JSON schema/regex/exit code（promptfoo deterministic、Inspect text-match、SWE-bench 容器内跑测试）。
2. **human**：两名独立人工按同一判据盲判；判据要提前写死。
3. **model**：LLM-as-judge / G-Eval 等概率分（DeepEval、promptfoo model-graded）。

规则：凡能写成 executable oracle 的断言，禁止把 model grader 当门禁；model grader 只能做诊断、找遗漏、排序。报告里每个断言注明 oracle 层级，出现“用 LLM judge 当唯一门禁”即降级为诊断，不算已验证。

### R37-3 Skill TDD：先留红起点，再写 skill

- 写 Skill 前先 `scaffold_eval_task.py` 建好 eval；用“无 skill”跑一次，把原始输出、失败原因保存为 `baseline_failure`。
- 若 baseline 已通过：任务太简单，或预期答案已泄漏在 prompt/skill 里；先修 eval 再进入实现。
- 实现后重跑同一批任务，输出必须是同任务 `baseline → with_skill` 对比，不能只报最终通过率。
- 红起点材料与 eval 同目录落盘，作为可审计证据；这对应 TDD 的 Red-Green-Refactor：红是起点，绿是终点，Refactor 后必须重跑绿。
- 来源：Martin Fowler《Test Driven Development》（test-first、先列测试清单）、skilljack-evals（baseline + lift）。

### R37-4 评测集三元组 + 调优/报告分离

每套 eval 至少三类任务，缺一不可：

- **target**：目标能力任务；gold/预期答案必须独立于 prompt 生成，不能从 prompt 里复制。
- **distractor / anti-trigger**：无关任务，验证不误触发、不产生伪阳性。
- **regression guard**：旧能力/旧行为不被破坏（对应 SWE-bench `PASS_TO_PASS`）。

门禁写成可执行表达式，例如 `target_task_pass_rate >= 0.8 && regression_fail == 0 && anti_trigger == pass`，禁止只写“效果明显提升”。
评测集分调优集和报告集：报告集必须来自未参与反复调参的 holdout 或新采样；同一批 20 题反复调 Skill 后报 lift 视为污染。
来源：SWE-bench、OpenAI Evals（eval 需有测试/基准）、DeepEval（reference vs referenceless、component vs trajectory）。

### R37-5 Agent/多步交付：轨迹证据 + 隔离执行

- 多步/工具型交付不能只验最终答案；证据包要含完整 trace：每步 tool call、读写路径、exit code、耗时、成本。
- 设中间断言：如“第 1 步必须读到原文件”“第 3 步不得修改 src 外文件”“最终必须产生 out.csv”。
- 可执行代码/agent 在容器或沙箱里跑，不贴生产环境截图；记录镜像/版本/seed/并发。
- 结果表达复用 `FAIL_TO_PASS + PASS_TO_PASS`：新能力通过的测试 + 旧能力不回归的测试，二者同时满足才算过。
- 来源：promptfoo「Evaluate Coding Agents」与「Sandboxed Code Evals」、SWE-bench 的 patch+test 执行框架、DeepEval trajectory metrics。

### R37-6 红队双层：审产物，也审 verifier

1. **产物红队**：按威胁类目扫（prompt injection、PII 泄露、越权/权限、提示词窃取、误导输出、错误工具调用等）；每条 finding 必须带“输入样例 / 威胁类目 / 证据片段 / 建议”。
2. **verifier 红队**：对评测器做变异——删一条断言、提高阈值、把 expected 改成永远匹配、让 verifier 变成“永远不会红”，确认评估系统会报警；否则“验证通过”只是 verifier 放行。
3. 独立视角执行：换 persona、换上下文、只给规格不给实现；作者自扫不是独立红队，不能写在 `adversarial_review` 的通过结论里。
- 来源：promptfoo LLM Red Teaming（20+ 漏洞类型）、Stryker（测试套件质量）、EvalPlus（测试覆盖不足会漏掉伪通过）。

### R37-7 伪验证反例（见到即打回）

| 现象 | 判定 |
|---|---|
| 只贴运行日志/截图，无断言 | L0，未验证 |
| “全部通过”但从未做过破坏测试 | 未知，不能写 verified |
| LLM judge 高分代替确定性 checker | 诊断，不是门禁 |
| 期望答案出现在 prompt 或 SKILL.md 里 | oracle 泄漏，eval 无效 |
| 只有新能力样例，无回归样例 | 不能断言“没破坏旧能力” |
| baseline 与 treatment 环境/版本/seed 不同 | A/B 无效 |
| 红队由作者本人、未换输入与视角 | 非独立红队 |
| 同一小测试集反复调参后报 lift | 过拟合/污染，除非有 holdout |

### R37-8 环境指纹与复现字段

运行时/数据 claim 必须记录：

- 命令与退出码；
- 环境指纹：镜像 tag、包版本、seed、并发数、网络/沙箱策略；
- 样本口径：数量、去重/过滤规则、统计方法与置信区间；
- baseline 与 treatment 必须同指纹，换环境/版本后重验，不允许“上一个环境跑过”沿用。

来源：SWE-bench（Docker 固定环境做执行验证）、promptfoo sandboxed code evals（隔离执行）。

## 来源

- [WordPress agent-skills authoring-guide](https://github.com/WordPress/agent-skills/blob/trunk/docs/authoring-guide.md)
- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [skilljack-evals README](https://github.com/olaservo/skilljack-evals)
- [claude-workflow-kit（evidence-first verification）](https://github.com/ncoevoet/claude-workflow-kit)
- [Promptfoo Red Team Coding Agents](https://www.promptfoo.dev/docs/red-team/coding-agents/)
- 完整来源表见 `SOURCES.md`。
