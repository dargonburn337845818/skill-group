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
python3 tools/skill_package_check.py <skill-dir> [more-dirs...]

# 2) 为 Skill 先建评测任务（prompt + deterministic checks + anti-trigger）
python3 tools/scaffold_eval_task.py --task-id my-task --skill-name my-skill \
  --prompt "真实任务描述" --checks "contains:SUCCESS_MARKER,files:out.txt"
```

- `skill_package_check.py` 输出 `ok/issues/warnings/score`，任一 issue 即 `ok=false`。
- `scaffold_eval_task.py` 生成 skilljack-evals 风格任务包；评测跑通后再进入发布。

真实 runner（本地 DeepSeek 执行层）：

```bash
# 单任务 A/B
python3 tools/skilljack_runner.py --task-dir evals/<task> --mode both --runs 3 --output ab.json

# 多任务矩阵 + 门禁
python3 tools/benchflow_runner.py --config benchflow.config.yaml
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

## 来源

- [WordPress agent-skills authoring-guide](https://github.com/WordPress/agent-skills/blob/trunk/docs/authoring-guide.md)
- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [skilljack-evals README](https://github.com/olaservo/skilljack-evals)
- [claude-workflow-kit（evidence-first verification）](https://github.com/ncoevoet/claude-workflow-kit)
- [Promptfoo Red Team Coding Agents](https://www.promptfoo.dev/docs/red-team/coding-agents/)
- 完整来源表见 `SOURCES.md`。
