# Sources（skill-vault-publish）

> 来源台账。内部路径/本地文件按工作区约定解析；公开链接可在浏览器复核。

## 清单
- $PROJECT_ROOT/README.md
- scripts/push.sh
- https://github.com/dargonburn337845818/skill-group.git`）

## 分级说明
- 本 skill 的核心规则在 `SKILL.md` 中带 `source_refs` 或来源章节；未标注来源的观点应视为待证。
- 单源结论不作为核心规则；冲突分支保留而非合并。

## Round 38 新增来源

> 2026 深度补强（Round 38）采用的外部来源；按主题归组，可在浏览器复核。

- **Agent Skills 官方规范与文档**
  - [Equipping agents for the real world with Agent Skills — Anthropic Engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)：Skill 目录/SKILL.md、`name`+`description` 必填、progressive disclosure 三级披露。
  - [Creating custom skills — Claude.ai Docs](https://claude.com/docs/skills/how-to)：目录结构、`name`/`description` 约束、`scripts/`/`references/`/`assets/`、打包 ZIP 根目录、ZIP 前测试、安全注意事项。
  - [Extend Claude with skills — Claude Code Docs](https://docs.claude.com/en/docs/claude-code/skills)：frontmatter 参考、`allowed-tools` 与工作区信任、`disable-model-invocation`、500 行建议、`skill-creator` 评测、移除/覆盖规则。
  - [Agent Skills Specification — agentskills.io](https://agentskills.io/specification)：`name` 1–64/小写/连字符规则、`description` 1–1024、`license`/`compatibility`/`metadata`/`allowed-tools`、正文 <5000 tokens、文件引用深度、`skills-ref validate`。

- **校验工具与版本**
  - [himself65/skill-lint](https://github.com/himself65/skill-lint)：SKILL.md 缺失/大小写、name 格式与目录失配、未知 frontmatter 字段、description 长度、空正文、引用缺失、Claude.ai 保留词与尖括号、marketplace 版本漂移。
  - [Semantic Versioning 2.0.0](https://semver.org)：MAJOR/MINOR/PATCH 递增规则与预发布/构建元数据语义。

- **发布与回滚**
  - [About releases — GitHub Docs](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)：Release 基于 Git tag、assets、安全公告用于漏洞修复发布的关联做法。
  - [About protected branches — GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)：protected branch 默认禁 force push/删除，并可要求状态检查与 PR 审核。
  - [Rollback a Deployment — GitLab Release Docs](https://gitlab-org.gitlab.io/release/docs/runbooks/rollback-a-deployment/)：回滚前检查目标包、确认无部署进行中、先通知/排空 canary、回滚后 fix-forward、post-deploy migration 是不可跨越的版本边界。
