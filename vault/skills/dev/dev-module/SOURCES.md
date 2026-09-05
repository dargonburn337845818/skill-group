# Sources（dev-module）

> 来源台账。内部路径/本地文件按工作区约定解析；公开链接可在浏览器复核。

## 清单
- $PROJECT_ROOT/FORMAL_SPEC.md
- $PROJECT_ROOT/vault/skills/base/search-source/
- $PROJECT_ROOT/vault/skills/core-iteration/skill-verification-consensus/
- $PROJECT_ROOT/vault/skills/core-iteration/dev-workflow-consensus/
- $PROJECT_ROOT/vault/skills/distillation/ui-aesthetics-design/
- $PROJECT_ROOT/vault/skills/dev/subskills/

## 分级说明
- 本 skill 的核心规则在 `SKILL.md` 中带 `source_refs` 或来源章节；未标注来源的观点应视为待证。
- 单源结论不作为核心规则；冲突分支保留而非合并。


## Round 36 新增来源

> 检索方式：GitHub Search API（Watt host proxy）+ Bing/官方站点直连核验；链接均已复核可访问。编号对应 SKILL.md “2026 深度补强（Round 36）”中的 R36-xx。

| 编号 | 来源 | 链接 | 用途/证据点 | 可信级别 |
|---|---|---|---|---|
| R36-01 | Agent Skills Overview（官方标准） | https://agentskills.io/ | 技能=文件夹+SKILL.md；渐进披露；描述/正文分层 | official-standard |
| R36-02 | Agent Skills — Best practices for skill creators | https://agentskills.io/skill-creation/best-practices | 技能应是一个连贯任务单元；过窄/过宽的反例；校验清单、默认值、过程优先 | official-docs |
| R36-03 | Agent Skills — Optimizing skill descriptions | https://agentskills.io/skill-creation/optimizing-descriptions | should-trigger / should-not-trigger；train/validation 防过拟合；触发宽度诊断 | official-docs |
| R36-04 | Agent Skills — Evaluating skill output quality | https://agentskills.io/skill-creation/evaluating-skills | 机械断言用脚本；LLM 只做语义诊断；保持技能精简 | official-docs |
| R36-05 | Anthropic Engineering — Building Effective Agents | https://www.anthropic.com/engineering/building-effective-agents | Routing 工作流=分类输入交给专门子任务；简单可组合模式；先求简单再增复杂度 | official-engineering |
| R36-06 | OpenAI Agents SDK — Agent orchestration | https://openai.github.io/openai-agents-python/multi_agent/ | 两种编排：manager 用 agents-as-tools；triage 用 handoffs；专用 agent 优于通用 agent；投资 evals | official-docs |
| R36-07 | OpenAI Agents SDK — Handoffs | https://openai.github.io/openai-agents-python/handoffs/ | handoff 是给 LLM 的工具；一个目标一个 handoff；`handoff_description` 提示何时选择 | official-docs |
| R36-08 | Google ADK — Agent routing | https://google.github.io/adk-docs/agents/routing/ | 显式 router；失败后带 errorContext 重选 fallback；已试 key 不重选；按复杂度路由 | official-docs |
| R36-09 | Agile Alliance — Definition of Done | https://www.agilealliance.org/glossary/definition-of-done/ | DoD 是显式、展示、团队同意的完成条件清单；避免“共享理解”式隐性完成 | official-glossary |
| R36-10 | Alistair Cockburn — Hexagonal Architecture | https://alistair.cockburn.us/hexagonal-architecture/ | ports/adapters；内外不对称；内部不泄漏到外部；边界用端口表达 | authoritative-essay |
| R36-11 | Robert C. Martin — The Clean Architecture | https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html | Dependency Rule：依赖只向内；内部不引用外部；跨边界数据用内层形态 | authoritative-essay |
| R36-12 | IEEE Computer Society — SWEBOK v4.0a（2026-08） | https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf | 软件工程知识域/过程分类，用于开发任务分类与模块化映射 | official-standard |
