# 核心迭代元能力 · Round 13：GitHub 灵感工厂 + 递归升级入口

> 日期：2026-09-04 ｜ 状态：真实 GitHub 灵感挖掘成功，新增 inspiration-miner 元能力

## 新增

### `tools/mine_ideas.py`

- 通过 host 代理真实搜索 6 组 GitHub query：
  - agent-skills / llm-plugin / dsh / ai-assistant / skill-management / cli plugin agent
- 对每个仓库做相关性打分（dsh / skill / plugin / agent / harness / workflow / eval / self-improve）
- 输出去重后的候选 idea：
  - `tools/output/ideas.json`
  - `tools/output/IDEAS.md`

### 新元能力 `inspiration-miner`

- 把“GitHub 灵感工厂”固化为可调用 skill
- 工作流：真实检索 → 相关性评分 → 去重排序 → 挑选 1–3 个 → 落地 → 验证
- 已接入 `value-meta-scheduler` 扩展元能力表
- `validate_contract.py` 已纳入校验

## 真实结果

- 查询：6
- 原始仓库：30
- 候选 ideas：29
- 失败：0

### 代表性灵感

| Repo | 可借鉴方向 |
|---|---|
| `deepseek-ai/deepseek-harness` | DSH 官方 harness/plugin 生态 |
| `anthropics/skills` | 官方 agent skills 组织与发现 |
| `rebelytics/one-skill-to-rule-them-all` | skill 编排/元技能 |
| `ComposioHQ/awesome-claude-skills` | skill 生态地图 |
| `ruvnet/ruflo` | agentic workflow / harness 设计 |
| `walkinglabs/learn-harness-engineering` | harness engineering 教程 |
| `anywhere-labs/dsh-desktop` | DSH desktop/plugin 生态 |

## 验证

- `validate_contract.py`：✅ PASS（含 inspiration-miner）
- `behavior_test.py`：✅ PASS
- `mine_ideas.py --proxy-mode host`：✅ 30 条真实仓库
- workspace + vault 同步：✅

## 产物

- `tools/mine_ideas.py`
- `tools/output/ideas.json`
- `tools/output/IDEAS.md`
- `inspiration-miner/`（新元能力）
- `REPORT_ROUND13.md`

## 下一步

1. 从 Top ideas 中选 1–3 个落地（例如：DSH 插件自动发现、skill 市场评估、harness 工程教程）。
2. 把选中的 idea 转成真实插件/工具原型。
3. 用 `return-forensics` 判断哪些灵感真正提升元能力。
