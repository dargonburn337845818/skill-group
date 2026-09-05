# Sources — Design Skill Control Loop

## Primary

- HumanLayer / skills（官方仓库）
  - `design-control-loop`：https://github.com/humanlayer/skills/tree/main/plugins/design-control-loop
  - `build-iterated-agentic-loop`：https://github.com/humanlayer/skills/tree/main/plugins/build-iterated-agentic-loop
  - `control-loop-taxonomy.md`：https://github.com/humanlayer/skills/blob/main/plugins/design-control-loop/skills/design-control-loop/references/control-loop-taxonomy.md
  - `design-control-loop/SKILL.md`：https://github.com/humanlayer/skills/blob/main/plugins/design-control-loop/skills/design-control-loop/SKILL.md
- HumanLayer / 12-factor-agents
  - README：https://github.com/humanlayer/12-factor-agents
  - Factor 3 Own your context window：https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-03-own-your-context-window.md
  - Factor 8 Own your control flow：https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-08-own-your-control-flow.md
  - Factor 10 Small, focused agents：https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-10-small-focused-agents.md

## Local evidence

- 本机审计报告：`$HOME/work/control-loop-skill-audit-2026-09-06.md`
- 当前全局启用状态：`~/.dsh/skill-vault/enabled.json`
- 路由器源码：`$HOME/work/dsh-skill-router/src/router.ts`
- 保险库源码：`$HOME/work/dsh-skill-vault/src/manager.ts`（运行期 register 逻辑）
- 技能库校验脚本：`$HOME/work/dsh-skill-vault/scripts/validate-vault.mjs`

## Video

- B 站视频 BV1Sw3H66Eav（中配 Kyle Mistele）：
  - 页面：https://www.bilibili.com/video/BV1Sw3H66Eav/
  - API 元数据：https://api.bilibili.com/x/web-interface/view?bvid=BV1Sw3H66Eav
  - 本项目使用本地 Whisper 转写，未引用未经核验的 AI 摘要。

## Note

- HumanLayer 的 skill 是针对“代码库/CI”的；本 skill 只借鉴其控制论结构和模板，不照搬其工具链（react-doctor / CodeLayer / GitHub Actions）。
- 本 skill 对 DSH 技能库的“控制器/执行器”给出的是方向和接口，不替代用户对人的确认。
