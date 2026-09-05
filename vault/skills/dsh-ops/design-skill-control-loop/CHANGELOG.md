# Changelog

## v0.2.0 — 2026-09-06

- 新增：`scripts/skill_governance_controller.py` 治理控制器（suggest / init / flow）。
- 新增：接入 `skill_governance` 插件工具与 `/skill-vault/api/governance`（dsh-skill-vault 0.2.0 侧）。
- 新增：`agent-memory/skill-governance.md` 与 `agent-memory/open-changes.json` 落地在技能库仓库。
- 控制器规则：效果率 ≥50% + 误触发率 ≤30% + 样本 ≥3 才建议 enable；效果率 <40% 或误触发率 >30% 建议 disable/demote；开放变更优先 flow_control。

## v0.1.0 — 2026-09-06

- 新增：`design-skill-control-loop` 首个版本。
- 来源：B 站视频 BV1Sw3H66Eav（Kyle Mistele 中配演讲）、HumanLayer `design-control-loop` / `build-iterated-agentic-loop`、HumanLayer `12-factor-agents`。
- 内容：控制论四件套映射到 DSH 技能库治理；包含审计、采访、传感器/控制器/执行器设计、阻尼器、流量控制、人类在环与边界反例。
- 入库：dsh-ops 场景，默认 `activation: catalog`。
