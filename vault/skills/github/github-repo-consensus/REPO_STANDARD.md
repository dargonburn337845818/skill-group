# GitHub 仓库施工标准

> 版本：v1.0（2026-09-06）
> 用途：把开源仓库从“AI 味很浓的门面”改成“专业、克制、可维护的门面”。
> 与 `CONSENSUS.md` 的关系：本文件是**施工执行标准**，`CONSENSUS.md` 是**规则与来源底座**；施工时以本文件的清单为准，规则依据回到 `CONSENSUS.md`。

## 1. 总原则

1. **3 秒原则**：陌生人打开仓库页，3 秒内应知道“这是什么、给谁用、怎么开始”。
2. **去 AI 味**：删除装饰性 emoji、口号堆叠、形容词轰炸；删除“强大”“完美”“一站式”“革命性”等未量化的宣传词。
3. **事实优先**：每个功能写成可验证的事实；每句承诺都能指向代码、命令或文档。
4. **读者优先**：面向“第一次见到这个仓库的贡献者/用户”写文本，不面向内部记忆。
5. **文本与代码分离**：README 只放门面与上手信息；长文档进 `docs/` 或独立文件；不把源码细节塞进 README。
6. **一致胜于个性**：所有仓库使用同一套标题、分段、措辞习惯，降低维护成本。

## 2. 仓库元数据（GitHub Settings）

### Description

- 单句、事实性、≤ 160 字符。
- 模板：`<工具/项目>：<解决什么>，<支持平台/形态>。`
- 避免：形容词堆砌、感叹号、emoji、空泛的“AI 驱动/强大”。
- 示例：
  - 好：`VS Code 内 Codeforces 刷题工作台：选题、翻译、测试、对拍、造数据、比赛、记录。`
  - 差：`🚀 超强 CF 刷题神器，一站式全能工作台！`

### Topics

- 只放技术性、可检索的 topic；小写、连字符；每个 ≤ 50 字符，总数 ≤ 20。
- 建议 5–12 个：语言/技术栈、运行平台、功能领域、生态名称。
- 避免：`awesome`、`ai`、`tool` 等空泛词；避免为 SEO 堆砌重复词。
- 示例：`codeforces`, `vscode-extension`, `competitive-programming`, `typescript`, `local-first`。

## 3. README 标准

### 3.1 标题区

```markdown
# <仓库名/项目名>

> 一句话定位：给谁用、解决什么、在什么平台运行。

[![License](LICENSE)](LICENSE)  <!-- 只放真实且有用的徽章 -->
```

- 只保留 LICENSE、CI、平台等有实际含义的徽章；不要为了“好看”堆一堆徽章。
- 标题不要加 `# awesome`、`# 🚀` 等。

### 3.2 标准段落顺序

```text
1. 简介（What / Why）
2. 功能（Features）
3. 安装 / 前置条件（Install / Prerequisites）
4. 快速开始（Quick Start）
5. 使用（Usage）——若内容多，只写一小节并链接 docs/
6. 文档（Documentation）——链接 docs/、Wiki、示例
7. 架构 / 目录（Architecture / Project layout）——可选、简洁
8. 开发（Development）——本地构建、测试、lint
9. 贡献（Contributing）——链接 CONTRIBUTING.md 与 PR 模板
10. 安全（Security）——链接 SECURITY.md，注明隐私承诺
11. 许可证（License）
```

### 3.3 去 AI 味的写作规则

| 做法 | 不要做 |
|---|---|
| 功能清单用 `- 动词开头短语`，每条 ≤ 30 字 | 每条都用加粗标题 + 多行解释 |
| 用“支持 / 提供 / 包含”等中性词 | 用“赋能 / 颠覆 / 神器 / 保姆级” |
| 标题用序号或简洁名词 | 标题用 `✨` `🎯` `🔥` 或“超强” |
| 长文档链接到 `docs/` | README 承载全部配置/变量/截图 |
| 中英统一（中文仓库用中文，术语保留英文） | 同一句里中英穿插频繁无规则 |
| 对开源读者解释内部生态名词 | 默认读者知道 `DSH`、`深模块` 等内部词 |

### 3.4 README 长度

- 建议 80–250 行；超过 250 行应拆分到 `docs/`。
- 超过 500 KiB 会被 GitHub 截断；不要放大量内联图片或 base64。

## 4. 社区文件标准

每个公开仓库根目录/`.github` 至少包含：

| 文件 | 必需性 | 要求 |
|---|---|---|
| `README.md` | 必需 | 按本文件第 3 节 |
| `LICENSE` | 必需 | 标准 MIT/Apache-2.0 等，文件名全大写 |
| `CONTRIBUTING.md` | 建议 | 环境、测试命令、PR 检查、隐私红线 |
| `SECURITY.md` | 建议 | 支持版本、私密上报渠道、隐私范围 |
| `CODE_OF_CONDUCT.md` | 建议 | 简短行为准则；可用 Contributor Covenant |
| `.github/ISSUE_TEMPLATE/*` | 建议 | bug/feature 模板；必填项清晰；提醒脱敏 |
| `.github/PULL_REQUEST_TEMPLATE.md` | 建议 | 变更、验证、隐私影响三块 |
| `.github/dependabot.yml` | 有依赖时建议 | npm/pip/github-actions 至少每周 |
| `.github/CODEOWNERS` | 有协作者时 | pattern + owner |

## 5. 目录与文档标准

- 根目录只放“人先看”的文件；代码/资源进 `src/`、`app/`、`docs/`、`tests/` 等。
- 长文档放 `docs/`，命名与 README 链接一致：`getting-started.md`、`configuration.md`、`troubleshooting.md`、`development.md`。
- 不在根目录堆 `design.md`、`spec.md`、`notes.md` 等内部文档；统一移到 `docs/` 或在 README 链接。
- 文档中使用相对链接；示例路径使用通用占位（如 `~/.config/...`），不硬编码个人绝对路径。

## 6. GitHub Actions 标准（施工期检查，不做大规模改动）

- workflow 默认 `permissions: contents: read`；需要写权限的 job 显式声明。
- 第三方 action 尽量 pin 到 full SHA；Dependabot 自动更新。
- secrets 只走 GitHub Secrets，严禁写入文件/日志。
- 发布 job 使用 `Release` workflow + `v*` tag；不要在每次 push 上重复打包。
- 公共仓库避免 `pull_request_target` 直接 checkout 不可信 PR 代码。

## 7. 施工流程

1. **盘点**：列出每个仓库的 README、社区文件、元数据、docs 现状。
2. **改写**：按第 3 节模板重写 README；按第 4 节补齐/统一社区文件。
3. **更新元数据**：通过 GitHub API/页面更新 description、topics。
4. **校验**：检查没有源码改动；检查 README 中的命令/链接仍真实。
5. **提交**：只提交文本/文档/元数据文件；不混入代码改动。
6. **推送**：有权限的仓库直接推送；无权限的仓库保留本地并说明。

## 8. 各仓库检查表

- [ ] README 无 emoji 标题、无夸张宣传词
- [ ] README 含简介/功能/开始/贡献/许可证
- [ ] Description 与 Topics 已更新，无空泛标签
- [ ] LICENSE、CONTRIBUTING、SECURITY 存在且内容真实
- [ ] Issue/PR 模板存在并提醒隐私脱敏
- [ ] 长文档已链接，不堆在 README
- [ ] 相对链接/命令可验证
- [ ] 未改任何源码/代码逻辑
