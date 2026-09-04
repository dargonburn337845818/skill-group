# 网络信息搜集共识（web-research-consensus）

> 把“可靠来源判断、精确检索、高效核验”蒸馏成 agent 可调用的执行清单。

## 文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | Agent 可调用摘要：触发、四步流程、检查表、反例 |
| `CONSENSUS.md` | 完整版：方法、边界、来源表、校验方法 |
| `SOURCES.md` | 来源分级表，便于审计 |
| `examples/dry_run.md` | 3 个典型场景干跑样例 |

## 一句话

```text
可靠结论 = 一手来源 + 独立交叉验证 + 原始语境 + 明确的确定性标记
```

## 入库

此目录是蒸馏产物源目录；用 `skill_vault_add` 可复制进 `dsh-skill-vault/vault/skills/research/web-research-consensus/`。
