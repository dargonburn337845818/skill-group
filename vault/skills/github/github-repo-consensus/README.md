# GitHub 开源仓库共识

> 从 GitHub 官方文档与社区“仓库标准”实践蒸馏出的可执行共识。
> 给 agent 用的缩写版：`SKILL.md`；完整版：`CONSENSUS.md`；来源：`SOURCES.md`。

## 解决什么

新建/改造一个开源 GitHub 仓库时，按四个面检查，避免“公开后才后悔”：

```text
A 仓库页：README、description、topics、LICENSE、CONTRIBUTING、SECURITY.md、issue/PR 模板
B 隐私/安全：visibility 后果、secret 历史清理、免费安全四件套、最小权限
C 结构：根目录门面、代码/文档/测试/示例/脚本分目录、大文件策略、分支保护
D Actions：workflow 存放与触发、secret 处理、GITHUB_TOKEN 最小权限、第三方 action pin SHA、特权 trigger 风险
```

## 文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | Agent 可调用摘要：触发、四张快速检查表、反模式、简单用户话术 |
| `CONSENSUS.md` | 完整版：每条规则含触发/动作/边界/来源，含开源前 10 项清单与 3 个样例 |
| `SOURCES.md` | 官方与社区来源清单，可审计 |
| `manifest.json` | dsh-skill-vault 元数据 |

## 使用

1. 准备开源时：先读 `SKILL.md`，按 A→B→C→D 走一遍。
2. 需要细节/争议时：读 `CONSENSUS.md` 对应小节和来源。
3. 涉及 public/private 切换、删除镜像、历史重写、公开 release：先参考 `dsh-optimization-consensus` 的“提醒用户、备份/回滚、隔离验证”。
