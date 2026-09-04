# distillation-consensus-skill

> 从网络公开实践与本地经验中提炼的**内容蒸馏共识**：
> 把书、长视频、播客、博客、访谈、题解、官方文档等材料，蒸馏成 agent 可调用的启发式技能 / 共识，
> 同时用简单语言向用户说明“方向 + 方式 + 边界”。

## 目标

不是做“摘要”，而是做“可执行知识”。每条可执行知识必须包含：

```text
触发条件 + 动作 + 反例/边界 + 来源 + 简单用户话术
```

## 文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | Agent 可调用摘要：核心公式、九步流水线、必守纪律、用户提醒模板 |
| `CONSENSUS.md` | 完整共识：定义、蒸馏循环、启发式技巧库、反模式、来源表 |
| `examples/` | 示例（后续可放 primitive JSON / 成品 SKILL 样例） |

## 怎么用

1. **给 agent 调用**：安装后调用 `skill distillation-consensus`；未安装时把本目录的 `SKILL.md` 全文粘进上下文。
2. **复杂任务**：先读 `CONSENSUS.md`，按九步流水线执行。
3. **面向用户**：使用 `CONSENSUS.md` 第 6 节的简单语言提醒模板，不要直接输出内部术语/概率。

## 安装到 DSH 技能目录（需用户确认后外部执行）

当前 `~/.dsh` 在会话沙箱中是只读的，不能从这里直接写入。确认后可在外部终端执行：

```bash
mkdir -p ~/.dsh/.agent-presets/router-standard/skills/distillation-consensus
cp $WORKSPACE/skills/distillation-consensus-skill/SKILL.md \
   ~/.dsh/.agent-presets/router-standard/skills/distillation-consensus/SKILL.md
```

重启/刷新后，`skill` 目录中应能看到 `distillation-consensus`。

## 与现有技能的关系

- `teacher-consensus-skill`：本共识在“算法竞赛教师共识”的具体应用（24 条主题 + 元纪律 + 七步法）。
- `dsh-optimization-consensus`：本共识在“DSH 运维优化”的具体应用。
- 本目录是通用层；做具体领域时先加载领域本体，再套用本共识。

## 来源

网络来源与本地实践见 `CONSENSUS.md` 第 8 节。
