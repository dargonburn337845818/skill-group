# 检验与验证共识（完整版）

> 适用对象：任何需要“验证”的交付物——Skill、代码、文档、插件、数据、结论。
> 产出物：一套证据分类、可证伪检查、评测任务与红队复核的可执行纪律。
> 本文件遵守 `distillation-consensus`：每条规则有触发/动作/边界/来源；没有来源的只作 common-lore 并降权。

## 0. 一句话共识

```text
“验证过了”不是一句话，而是一条证据链：主张 → 唯一可接受证明 → 可证伪检查 → 独立复核。
```

## 1. 证据分类（Claim Class Proof Table）

触发：任何交付物进入验收/发布前。

动作：把交付物拆成主张，每条归入下列五类之一，并只接受表中对应证明。

| 类型 | 主张例子 | 唯一可接受证明 | 反例/不可接受 |
|---|---|---|---|
| static | “模块接口是 X”“配置在 Y 文件” | 上游源码/commit/config 原文 + 可定位路径/行号/版本 | README、star、个人记忆、“应该是” |
| runtime | “流程能跑通”“错误会抛” | 真实运行输出/测试日志 + 命令、退出码、时间戳 | 只看代码推断、只看某人在帖子里说 |
| data | “性能提升 20%”“命中率 0.8” | 可复算的测量数据、基准脚本、样本与口径 | 营销数字、无口径的“大幅” |
| rendering | “UI 长这样”“文档能打开” | 实际产物截图/文件 + 生成命令 + 打开校验 | 描述性文字、模拟截图 |
| tooling | “依赖版本支持 X”“API 可用” | 已安装版本 `--version`、官方文档版本、package-lock/OSV 记录 | “最新版就行”、无锁版本 |

边界：

- 一个主张可能涉及多类证据；每一类都要有各自证明，不能用一个证明覆盖全部。
- 来源“权威”不等于证明：官方文档也可能过时，必须以能定位的版本/命令为准。
- 证据必须可复现：换一台机器/一个版本，按命令应能得到同一结论（或明确写出环境差异）。

## 2. 可证伪检查（Prove It Can Fail）

触发：每个自动检查/测试/验证脚本进入信任体系前。

动作：

1. 找到检查所监控的文件/状态。
2. 故意破坏它（改坏一块、删一个文件、造一个反例）。
3. 确认检查变红（失败）。
4. 恢复原始状态。
5. 确认检查变绿（通过）。

结论标记：

- `checks_observed_red = [check1, check2...]`：见过失败并恢复的检查，才可写“已验证”。
- 从没见它失败的检查：只能写“已运行，未验证”。它可能一直红灯不存在，也可能检测逻辑从未被触发。

边界：

- 突变动作本身要安全：在临时副本/隔离环境做，不污染真实数据。
- 如果检查无法变红（比如总是通过），说明它没有区分能力，应该修检查而不是保留。

## 3. 任务先行评测（Skill TDD）

触发：新增/修改一个 Skill，需要知道它是否真的提升能力。

动作：

1. **先写任务包**：一个 `task.md`（prompt + checks），提示词里不点名 skill，描述真实使用场景。
2. **确定性检查**：`contains/not_contains/regex/files_exist/tool_calls` 等，避免只靠主观 judge。
3. **配对基线**：同一任务跑“无 skill”和“有 skill”两组，默认 ≥3 次 trial。
4. **算 Skill Lift**：`with_skill 分辨率 − baseline 分辨率`；同时记录 Skill Invocation Rate。
5. **加 anti-trigger 任务**：无关任务不应触发该 skill；触发即失败（防误触发）。
6. **Oracle 门**：用一个参考解验证 verifier 本身可解且不是坏检查。
7. **门禁**：CI 中用 `threshold-resolution` 和 `threshold-lift`，缺基线时 lift 门禁 fail-closed。

边界：

- judge/LLM 诊断可以解释失败原因，但不能改变奖励分数；确定性 verifier 是权威。
- 只有 skill 被调用本身不是有效信号；必须看最终任务是否真的变好。
- 评测任务提示词不得泄露 skill 名称，否则测的是“提示词提示”而非 skill 发现/执行。

## 4. 红队与对抗复核

触发：规格/方案/代码在审核时；verify=redteam 的项。

动作：

- **对抗规格审查**：在规格单上专门找 BLOCKER（会阻断交付）、GAP（缺信息/缺边界）、NOTE（提醒），并记录“six checks run”或“none found”。
- **审查范围**：不是只看本次 diff，要看“上次审查之后改过的所有内容”，因为修复本身也可能引入新 bug。
- **防自证**：作者自检通过不等于验收通过；红队项必须由独立视角（另一个 agent/人/工具）裁决。
- **in-flight 阻断**：如果验证/测试仍在运行，不允许把“已通过”写进提交/发布；要等进程真正结束。
- **变更后再审**：修复后重新跑完整验证，而不是只重跑被修的那一项。

边界：

- 结构门（如“必须存在 adversarial review 段落”）只能证明产物存在，不能证明审查质量；不能把“存在”当“做得好”。
- 红队打回后，必须再次裁决；修复不是自动通过。

## 5. Skill 发布门槛清单

| # | 门槛 | 做法 |
|---|---|---|
| 1 | 元数据可发现 | `description` 第三人称，明确 what + when；名称具体、避免 helper/utils |
| 2 | 保持瘦身 | SKILL.md 简短可执行（参考 <500 行），细节放 references；引用一层深 |
| 3 | 三件套齐全 | 每条规则 trigger/action/boundary + source_refs |
| 4 | 有评测场景 | 至少 1 个 eval；复杂 skill ≥3 个；含 anti-trigger |
| 5 | 确定性优先 | 可脚本化判断用脚本/命令，不让模型猜 |
| 6 | 来源独立 | 多源交叉验证，非同源转载，无来源降权 |
| 7 | 版本可审计 | CHANGELOG/manifest 更新；无死引用/过期命令 |
| 8 | 干跑样例 | 至少 3 个样例或真实查询，确认可执行 |
| 9 | 失败模式 | 每个动作有失效边界/反例 |
| 10 | 发布门禁 | 校验报告 overall=pass；否则不发布 |

## 6. 输出契约

```text
{
  "target": "...",
  "claims": [...],
  "checks_observed_red": [...],
  "evals": {...},
  "adversarial_review": { "blockers": [], "gaps": [], "notes": [] },
  "overall": "pass|needs_work|reject",
  "next_actions": [...]
}
```

- 任一 claim `failed`，或任一必要检查没有 `checks_observed_red`，`overall` 不得为 pass。
- `next_actions` 必须具体：补什么证明、跑什么命令、补哪个场景。

## 7. 简单用户话术

> 验证不是一句话。我会把你的交付物拆成具体主张，给每条配唯一可接受证明；再做一次“故意破坏看看它会不会红”的检查，只有见过它失败又恢复的，我才写“已验证”。最后我会给 PASS/需返工/拒绝，并告诉你要补哪种证据。

## 8. 来源与参考

- [WordPress agent-skills authoring-guide](https://github.com/WordPress/agent-skills/blob/trunk/docs/authoring-guide.md)：确定性脚本、eval 场景、frontmatter 校验。
- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)：元数据、渐进披露、测试多模型。
- [skilljack-evals](https://github.com/olaservo/skilljack-evals)：任务先行、无 skill 基线、Skill Lift、anti-trigger、oracle gate。
- [claude-workflow-kit](https://github.com/ncoevoet/claude-workflow-kit)：claim-class 证明表、可证伪“prove”、对抗规格审查、commit/spec gates、in-flight 阻断。
- [Promptfoo Red Team Coding Agents](https://www.promptfoo.dev/docs/red-team/coding-agents/)：针对 agent/编码交付的安全与稳健性红队证据。
- 本地交叉验证：`distillation-consensus`（三件套/来源）、`value-validator`（四条硬规则）、`dsh-optimization-consensus`（运维安全）。
