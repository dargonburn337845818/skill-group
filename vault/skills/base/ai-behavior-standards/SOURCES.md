# 来源账本 · ai-behavior-standards

> 每条规则按证据来源分级：A=一手/官方，B=二手/综述/访谈，C=类比/本地实践推断。
> 无来源或推断内容在正文标 `inferred`。

## 一级：本地已有规范（直接继承）

| 引用 | 证据级别 | 支撑的规则 |
|---|---|---|
| `~/.dsh/AGENTS.md` | A（用户全局共识） | 深模块、Deletion Test、接口即测试面、文件系统即模块地图、AI 即新人 |
| `$HOME/work/AGENTS.md` | A（工作区共识） | 工作区模块地图、每个项目独立模块、不跨项目隐式依赖 |
| `$HOME/work/REPO_STANDARD.md` | A（用户已写规范） | 根目录只放“人先看”文件、长文档进 docs、自动提交协议、仓库施工标准 |
| `$HOME/work/dsh-optimization-consensus.md` | A（用户已写规范） | 破坏性操作先说明、运行中禁止热更、隔离冒烟、回滚 |
| `$HOME/work/editorial-style-spec.md` | A（用户已写规范） | 文档风格、禁止夸张/装饰、层次与留白 |
| `$HOME/work/SKILL_MAP.md` | A（用户已写规范） | Skill 触发/动作/边界/来源四件套、管理反模式 |
| `$HOME/work/HANDOFF-NEXT-SESSION.md` | A（实践） | 跨会话交接文件、关键路径记录、下一步清单 |
| `$HOME/work/AI_MEMORY.md` | A（新落地记忆） | 轻量跨会话记忆：只记高信号、安全红线、环境事实、指针 |
| `$HOME/work/standards/DRIVE_LAYOUT.md` | A（新落地账本） | 全盘符授权依据：类型/状态/已接管目录/禁区/最近操作 |
| `dsh-skill-vault/vault/skills/base/work-consensus/SKILL.md` | A（技能库） | 模块地图、真接缝、深模块 |
| `dsh-skill-vault/vault/skills/core-iteration/dev-workflow-consensus/SKILL.md` | A（技能库） | 规格先行、对抗审查、证据化验证 |
| `dsh-skill-vault/vault/skills/github/github-repo-consensus/SKILL.md` | A（技能库） | GitHub 根目录结构、隐私安全、目录决策 |
| `skills/distillation-consensus-skill/CONSENSUS.md` | A（技能库） | 蒸馏四件套、来源可追溯、不平均分歧 |

## 二级：公开标准/指南

| 引用 | 证据级别 | 支撑的规则 |
|---|---|---|
| [Filesystem Hierarchy Standard](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard) | B（标准百科） | 目录职责分离、系统目录与用户目录边界 |
| [Ubuntu FHS 文档](https://ubuntu.com/project/docs/how-ubuntu-is-made/concepts/filesystem-hierarchy-standard) | B（官方文档转述） | `/home`、`/tmp`、`/opt`、`/var` 等目录职责 |
| [Google developer style guide · Filenames](https://developers.google.com/style/filenames) | B（官方风格指南） | 文件名大小写、连字符、避免空格/特殊字符 |
| [The Art of Unix Programming](https://en.wikipedia.org/wiki/The_Art_of_Unix_Programming) | C（经典书籍/百科） | Unix 哲学：一个程序做一件事、文本接口、可组合 |
| [12-Factor App](https://12factor.net/) | B（官方方法论） | 构建/发布/运行分离、配置注入、日志输出 |
| [Martin Fowler](https://martinfowler.com/) | B（专家官网） | 模块依赖、重构边界、角色接口 |

## 三级：专家团风格推断（非本人原话）

本次教师会话 rounds 的专家立场与结论（2026-09-06）：

| 专家 | 立场 | 来源 |
|---|---|---|
| Andrej Karpathy | 规范要少而深；文件命名是 AI 的长期记忆接口；目录即自解释结构 | [karpathy.ai](https://karpathy.ai/) |
| Lilian Weng | 文件管理需创建→归属→命名→清理→审计闭环，带反例 | [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) |
| Chip Huyen | 用可检查目录模板/命名/清理周期落地，不靠品味 | [Machine Learning Design](https://huyenchip.com/2023/05/02/machine-learning-design.html) |

> 说明：专家立场是按公开风格的 `public-figure-style-reference` 推断，不代表本人正式评审；冲突（规范多少才合适）已由主持人裁决为“少而深的硬底线 + 完整检查表”。

### 规范编写专家团（2026-09-06，standards 域）

| 专家 | 立场 | 来源 |
|---|---|---|
| Kent Beck | 每条规范可翻译成可执行动作/失败场景；先最小规则再加检查表 | [Kent Beck](https://en.wikipedia.org/wiki/Kent_Beck) |
| John Ousterhout | 规范是接口：少而深、命名/目录自解释、规则讲为什么 | [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) |
| Eric S. Raymond | 用约定而非配置；目录=职责、文件名=接口；先讲风险再给检查表 | [The Art of Unix Programming](http://www.catb.org/~esr/writings/taoup/) |
| Martin Kleppmann | 数据/产物必须来源、版本、schema、校验；原始数据/生成物/临时物分离 | [Designing Data-Intensive Applications](https://dataintensive.net/) |
| Steve McConnell | 规范可度量可检查；阈值是启发式不是教条，需注明可调整 | [Steve McConnell](https://stevemcconnell.com/) |

> 裁决：硬规则（机器可检查）与启发式（可调整建议）分层；SKILL 少而深，CONSENSUS 放完整清单。

## 待验证 / 降权项

- “7 天清理 scratch” 是本机实践推值，非外部标准，属于 `inferred`。
- “工作区根目录只放人先看文件” 是本地 `REPO_STANDARD.md` 与 work-consensus 的组合推导，非 FHS 原文。
- “所有项目默认 src/tests/docs/data/outputs/scratch” 是常见工程布局，不是强制标准；不同项目可覆盖。
