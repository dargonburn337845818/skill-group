# teacher-math-consensus（数学教师共识）

> 目录：`vault/skills/teaching/teacher-math-consensus/`
> 场景：`teaching`，也服务 `distillation` 的专家/知识蒸馏复用。
> 定位：**数学领域教学内容**，不是 teacher-module 讨论协议壳。与已有 `teacher-consensus`（算法竞赛）并列，专供证明/建模/分析。

## 这是什么

把 Polya、Tao、Zeitz、Lakatos 等公开数学方法论，按“熵减盘问”协议蒸馏成 agent 可调用的教师共识：

- 数学证明、建模、分析场景的四大方向；
- 一次一个问题、按信息增益选择下一步的 grill-me 协议；
- 带 `trigger / action / boundary / source_refs` 的数学思维原语；
- 区分“严谨前 / 严谨 / 严谨后”的学生认知阶段。

## 文件

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 主技能：教师共识 + 提问协议 + 原语种子集 + 信息论落点 |
| `manifest.json` | skill 注册元数据：scenario=teaching, activation=catalog |
| `README.md` | 本文件 |
| `SOURCES.md` | 来源台账：verified-high 来源与证据分级 |

## 何时用

- 学生问“这道证明/建模/分析题怎么想”，且你希望引导而不是给答案。
- 教学场景需要动态问题流、策略收敛、反例诊断。
- 未来把数学方法论蒸馏成 `P(feature | strategy)` 矩阵时，从这里读取原语。

## 注册状态（I03 集成）

本技能已由集成任务 I03 登记到 `vault/meta/modules.json`：

- `modes[teacher].skills` 增加 `teacher-math-consensus`；
- `modes[teacher].gaps` / `gapProgress` 增加“数学教师共识（证明/建模/分析）”条目，source 指向本目录 `SKILL.md`。

本目录不直接修改共享注册表；登记由集成会话负责。

## 边界

- 只做风格/方法论参考，不伪造大师原话。
- 不对具体题目保证“最优解法”；一切以学生当前定义、条件与数据为准。
- 不做算法竞赛替代品：算法题走 `teacher-consensus`；数学证明/建模/分析走本技能。
- 本目录不直接修改 `EXPERT_LIBRARY.json` / `domain-profiles.json` / `modules.json`；这些共享注册表由集成任务（如 I03）负责登记，本目录保持内容独立。

## 验证

```bash
cd $PROJECT_ROOT
node scripts/validate-vault.mjs
node scripts/validate-tags.mjs
```
