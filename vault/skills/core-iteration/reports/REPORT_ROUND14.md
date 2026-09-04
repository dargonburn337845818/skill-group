# 核心迭代元能力 · Round 14：GitHub 插件/skill 市场侦察

> 日期：2026-09-04 ｜ 状态：真实市场侦察工具上线

## 新增 `tools/market_scout.py`

支持两种侦察模式：

### Plugin 市场
- 查询：dsh-plugin / deepseek-harness / dsh / agent-plugin / harness
- 真实结果：30 条原始，23 个候选
- 代表项目：deepseek-harness、open-design、archify、distilly、sandbase-harness、dsh-desktop、awesome-dsh-plugin

### Skill 市场
- 查询：agent-skills / claude-skills / skills / skill-management / ai-assistant
- 真实结果：30 条原始，30 个候选
- 代表项目：ComposioHQ/awesome-claude-skills、skilldock、ruflo、anthropics/skills、VoltAgent/awesome-agent-skills

## 产物

- `tools/market_scout.py`
- `tools/output/plugin_market.json` / `PLUGIN_MARKET.md`
- `tools/output/skill_market.json` / `SKILL_MARKET.md`

## 验证

- 全部真实通过 Watt host 代理，0 失败。
- workspace + vault 同步：✅

## 下一步

从 plugin 市场中挑选 DSH 生态插件方向，作为后续插件原型选题。
