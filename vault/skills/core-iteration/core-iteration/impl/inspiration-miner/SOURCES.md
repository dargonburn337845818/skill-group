# inspiration-miner · 来源声明

- GitHub 真实检索结果：`tools/output/ideas.json`、`tools/output/IDEAS.md`
- 检索入口：`tools/mine_ideas.py`（调用 `info_source_cli.py`）
- 相关开源项目（示例）：anthropics/skills、deepseek-ai/deepseek-harness、ComposioHQ/awesome-claude-skills、rebelytics/one-skill-to-rule-them-all 等。

## Round 40 新增来源

> 本轮用于支撑“跨面侦察 / 预筛 / 双轴评分 / 派生溯源 / 回写闭环”的真实来源。官方文档为 `primary`，真实仓库/注册表为 `instance` 证据；star 仅作候选线索，不构成质量证据。

| 编号 | 类型 | 来源 | 支撑规则 |
|---|---|---|---|
| R40-S1 | 官方 API | GitHub REST Search endpoints — https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28 | R40-1 检索面 |
| R40-S2 | 官方语法 | GitHub 仓库搜索语法 — https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories | R40-1 / R40-3 |
| R40-S3 | 官方语法 | GitHub 代码搜索语法 — https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax | R40-1 代码面 |
| R40-S4 | 官方注册表 | MCP Registry — https://modelcontextprotocol.io/registry | R40-1 市场面 |
| R40-S5 | 官方插件市场 | Anthropic Claude Code plugin marketplaces — https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces | R40-1 / R40-2 |
| R40-S6 | 官方技能规范 | Anthropic Agent Skills overview — https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview | R40-2 / R40-3 |
| R40-S7 | 注册表 API | npm registry search API（agent skills）— https://registry.npmjs.org/-/v1/search?text=agent%20skills&size=5 | R40-1 市场面 |
| R40-S8 | 真实仓库 | VoltAgent/awesome-agent-skills — https://github.com/VoltAgent/awesome-agent-skills | R40-4 聚合仓案例 |
| R40-S9 | 真实仓库 | wshobson/agents — https://github.com/wshobson/agents | R40-1 / R40-4 插件市场案例 |
| R40-S10 | 真实仓库 | modelcontextprotocol/servers — https://github.com/modelcontextprotocol/servers | R40-1 / R40-2 参考实现 |
| R40-S11 | 真实仓库 | addyosmani/agent-skills — https://github.com/addyosmani/agent-skills | R40-2 / R40-3 工程化技能样例 |
| R40-S12 | 真实仓库 | obra/superpowers — https://github.com/obra/superpowers | R40-3 / R40-5 方法论参考 |
