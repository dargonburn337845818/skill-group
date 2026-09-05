# 开发工作流共识 · 来源清单

| 来源 | 主题 | 贡献 | 分级 |
|---|---|---|---|
| 本地 `work-consensus`（`~/.dsh/AGENTS.md` + 工作区 `AGENTS.md`） | 深模块 / 接口即测试面 / 模块地图 | 核心开发纪律 | common-lore（本地实践） |
| [claude-workflow-kit](https://github.com/ncoevoet/claude-workflow-kit) | evidence-first 开发工作流插件 | 7-phase、对抗规格审查、模型分层、churn-breaker、commit/spec gates、in-flight 阻断、claim-class 证明 | consensus |
| [WordPress agent-skills authoring-guide](https://github.com/WordPress/agent-skills/blob/trunk/docs/authoring-guide.md) | Agent 技能/工作流创作门禁 | 确定性脚本、eval 场景、Verification/Failure modes 章节 | consensus |
| [skilljack-evals](https://github.com/olaservo/skilljack-evals) | 交付物评测 | 基线对照、确定性 verifier、门禁阈值、prove/oracle | consensus |
| [dsh-skill-router](https://github.com/yjh051108/dsh-routing-suite) | DSH 内置开发规范 | 脑暴→规格→审核→执行→打卡→终验；L1/L2 规格 | common-lore（本地实现） |
| 本地 `dsh-optimization-consensus` | DSH 运维安全 | 子代理有界、隔离冒烟、不热更、回滚实际文件 | common-lore（本地实践） |

## Round 37 新增来源

| 来源 | 主题 | 贡献 | 分级 |
|---|---|---|---|
| [GitHub Spec Kit](https://github.com/github/spec-kit) + [Spec-driven development with AI](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) | 规格即仓库产物 | spec 文件/模板、spec→tasks、可 diff 可回溯、AI 协作门禁 | consensus |
| [Martin Fowler: Contract Test](https://martinfowler.com/bliki/ContractTest.html) + [Pact Docs](https://docs.pact.io/) | 接口契约测试 | 双侧契约、producer/consumer verification、避免单侧 mock 漂移 | consensus |
| [Martin Fowler: The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) | 测试分层 | 按最低可测全层选测试、快慢测试分层、避免全 e2e | consensus |
| [Google Engineering Practices: Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html) + [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) | 代码审查门禁 | 小变更、自审、blocking/non-blocking、审查结论可判定 | consensus |
| [Scrum.org: Definition of Done](https://www.scrum.org/resources/what-definition-done-0) + [Atlassian: Acceptance Criteria](https://www.atlassian.com/work-management/project-management/acceptance-criteria) | 完成定义 | 一验收一验证、可测准则、DoD 机器化 | consensus |
| [GitHub Docs: About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | 门禁机器化 | required status checks、CODEOWNERS、防绕过 | consensus |
| [Michael Feathers: Characterization Testing](https://michaelfeathers.silvrback.com/characterization-testing) | 旧代码表征测试 | 先锁现有行为再重构，行为变化须伴随规格同步 | consensus |
| [Anthropic/Claude: Steering Claude Code](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) + [AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) | AI 分层执行 | 上下文集于文件、子代理隔离、人审门禁、验证独立于作者 | consensus |
