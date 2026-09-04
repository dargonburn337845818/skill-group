# 技能真实跑通底线（不可妥协）

> 本文件是 dsh-skill-vault 的硬性发布门槛。任何 Skill 未满足本门槛，只能算“草稿/待验证”，不得标记完成、不得发布。

## 底线定义

“真实跑通” = 该 Skill 在真实任务中被实际加载并产生可测结果，且通过无 Skill / 有 Skill 对照验证。

## 每个 Skill 的最低验证要求

1. **任务包**
   - 至少 1 个真实 eval 任务（prompt 不点名 skill，任务本身可完成）
   - 至少 1 个 anti-trigger 任务（无关任务不应触发该 skill）
   - verifier 使用确定性检查（marker / file / command），不依赖模型自评

2. **对照运行**
   - 无 Skill 基线 ≥3 次
   - 有 Skill ≥3 次
   - 输出 Skill Lift（通过率 / 分辨率 / 效率）
   - anti-trigger 不误触发

3. **证明文件**
   - 每个 skill 目录存放：`evals/`（任务包）、`verification.json`（运行结果）、`checks_observed_red.md`（故意破坏→变红→恢复→变绿）
   - 未放证明文件 = 未真实跑通

## 拒绝标准

- 只跑 `skill_package_check.py` 或 `validate-vault` → 不算真实跑通
- 只有 LLM judge 打分，无确定性 verifier → 不算
- 同一次运行既当基线又当有 Skill → 不算
- 无 anti-trigger → 不算
- 运行记录不可复现（无命令、无输出、无环境） → 不算

## 状态标记

- `verified`：满足全部底线
- `needs_verification`：已有 skill 内容但未跑通
- `draft`：只有文本，无证据

## 当前状态

所有已入库 skill 默认视为 `needs_verification` 或 `draft`，除非目录内有上述证明文件。

## 当前已验证

- `dev-ai-engineering`：通过真实 eval A/B + anti-trigger；证据见 `vault/skills/dev/subskills/dev-ai-engineering/evals/` 与 `verification.json`。
- `dev-ops-sre`：通过 dev-ops-eval/dev-ops-anti 3 次 A/B，Skill Lift 19.2%（明显增强），anti-trigger 误触发 0/3；证据见 `vault/skills/dev/subskills/dev-ops-sre/evals/` 与 `verification.json`。
- `dev-architecture`：通过 dev-arch-eval/dev-arch-anti 3 次 A/B，Skill Lift 8.0%（轻微增强），anti-trigger 误触发 0/3；证据见 `vault/skills/dev/subskills/dev-architecture/evals/` 与 `verification.json`。
- `experiment-design`：通过 exp-design-eval/exp-design-anti A/B，eval 覆盖率 0→1，anti-trigger 误触发 0/3；证据见 `vault/skills/research/research-module/subskills/experiment-design/evals/` 与 `verification.json`。
- `research-submission`：通过 submission-eval/submission-anti 3 次 A/B，eval 成功率 1.0，anti-trigger 误触发 0/3；证据见 `vault/skills/research/research-module/subskills/submission/evals/` 与 `verification.json`。
- `academic-writing`：通过 academic-eval/academic-anti 3 次 A/B，eval 成功率 1.0，anti-trigger 误触发 0/3；证据见 `vault/skills/writing/writing-module/subskills/academic-writing/evals/` 与 `verification.json`。
- `speech-writing`：通过 speech-eval/speech-anti 3 次 A/B，Skill Lift 7.0%（轻微增强），anti-trigger 误触发 0/3；证据见 `vault/skills/writing/writing-module/subskills/speech-writing/evals/` 与 `verification.json`。
- `teacher-math-consensus`：通过 math-consensus-eval/math-consensus-anti 3 次 A/B，Skill Lift 9.2%（轻微增强），anti-trigger 误触发 0/3；证据见 `vault/skills/teaching/teacher-math-consensus/evals/` 与 `verification.json`。
- `distill-eval-task`：通过 eval-task-eval/eval-task-anti 3 次 A/B，eval 覆盖率 0→1，anti-trigger 误触发 0/3；证据见 `vault/skills/distill/distill-module/subskills/eval-task/evals/` 与 `verification.json`。
