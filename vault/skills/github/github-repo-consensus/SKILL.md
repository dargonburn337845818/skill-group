---
name: github-repo-consensus
description: GitHub 开源仓库页/README/目录结构/隐私安全/GitHub Actions 的可执行共识；用于新建或改造开源仓库时按清单检查，给 agent 即拿即用的方向、方式与边界。
---

# GitHub 开源仓库共识 · 可调用摘要

> 完整版见本目录 `CONSENSUS.md`；来源见 `SOURCES.md`。
> 核心：**先让访客 3 秒看懂“这是什么”，再用结构/安全/Actions 降低维护成本，最后才谈自动化。**

## 触发条件

- 用户问“怎么给 GitHub 仓库写 README / 建页面 / 配 license / 加 contributing”。
- 用户要把一个本地项目开源化：设 license、决定 public/private、清理 secrets、建目录结构、写 Actions。
- 用户要审查已有仓库的社区健康度 / 安全设置 / Actions 是否规范。
- agent 需要一套可执行的仓库初始化/改造检查表，而不是一段泛泛而谈。

## 一句话结论

开源仓库成功 = 四个可检查面：

```text
A 页面向：README 讲清 是什么/为什么/怎么跑/哪里求助
B 隐私面：public 前先清理 secrets，开启免费安全特性，写 SECURITY.md
C 结构面：根目录放 README/LICENSE/CONTRIBUTING，代码/文档/测试/模板分目录
D Action面：.github/workflows 用最小权限、secrets 不进文件、第三方 action 锁 SHA
```

## 快速检查表

### A. 仓库页规划（README + 元数据）

1. 每个仓库都建 README；放在 `.github`、根目录或 `docs`，GitHub 会自动展示。
2. README 回答：项目做什么、为什么有用、怎么开始、哪里求助、谁维护。
3. 长文档放 `docs/` 或 Wiki，README 只放“开发者上手必需”的信息。
4. 仓库描述 + topics 写清用途；topics 小写/数字/连字符，≤50 字符，≤20 个。
5. 补 LICENSE、CONTRIBUTING、CODE_OF_CONDUCT、SECURITY.md、issue/PR 模板，完成 Community Profile。
6. 仓库内相对链接优先（clone 后仍可用）；README 超过 500 KiB 会被截断。

### B. 隐私 / 安全管理

1. 公开前先扫历史：`.gitignore` 提前忽略 `.env`、密钥、缓存、构建产物；已提交的敏感文件先 revoke/rotate 再考虑 `git filter-repo` 清历史。
2. 公开仓库至少启用（免费）：Dependabot alerts、Secret scanning、Push protection、Code scanning。
3. 写 `SECURITY.md`，说明支持版本与漏洞上报渠道；可开 Private vulnerability reporting。
4. 明白 visibility 切换的后果：public 后代码/forks/Actions 日志全公开，push rulesets 会被禁用，star/watch 清空。
5. 权限最小化：仓库可访问人员、分支保护、必要评审；不要给多余写权限。

### C. 结构规划

1. 根目录放“人先看”的文件：`README.md`、`LICENSE`、`CONTRIBUTING.md`、`SECURITY.md`、`.gitignore`、`CHANGELOG.md`。
2. 代码、文档、测试、示例、脚本分目录：常见 `src/`、`docs/`、`tests/`、`examples/`、`scripts/`、`.github/`。
3. `.github/` 放贡献者/自动化文件：`ISSUE_TEMPLATE/`、`PULL_REQUEST_TEMPLATE.md`、`workflows/`、`CODE_OF_CONDUCT.md`。
4. 大文件用 Git LFS；仓库建议保持 <1 GB，超 100 MiB 会被阻止。
5. 主分支加保护：要求 PR 评审、状态检查通过；常规协作者用分支 PR，而不是 fork。

### D. GitHub Actions 使用

1. workflow 文件放 `.github/workflows/*.yml|yaml`；用 `on` 精确指定触发事件/分支/路径。
2. 敏感信息只放 GitHub Secrets，绝不要明文写进 workflow；不要用 JSON/XML/YAML 整块塞 secret（易导致脱敏失败）。
3. 给 `GITHUB_TOKEN` 最小权限（默认 `contents: read`，按 job 临时提升）。
4. 第三方 action 优先 pin 到 full-length commit SHA；用 Dependabot 自动更新。
5. 避免在公共仓库用 `pull_request_target`/`workflow_run` 直接 checkout 不可信 PR 代码；公共仓库不要用 self-hosted runner。
6. 不可信输入进 shell 脚本时，用 action 参数或中间环境变量 + `::add-mask::`，防脚本注入。

## 边界 / 反模式

| 场景 | 不要做 |
|---|---|
| README 写满项目历史、配置细节 | 不要；README 是“门面”，长文档进 docs/ 或 Wiki |
| 把 `.env` 加到 .gitignore 但已提交过 | 不够；已进历史的 secret 仍需 revoke/rotate，必要时重写历史 |
| 只用“清当前文件”就公开 | 不够；fork、克隆、PR 里的历史仍可能保留敏感数据 |
| 给所有公开仓库都开最贵安全特性 | 不必；先按免费四件套 + SECURITY.md，按需再加入高级特性 |
| 在 Actions 里把 secret 直接拼进 shell 命令 | 高风险；考虑注册 mask、避免结构化 secret |
| 依赖第三方 action 的 tag 而信任来源 | 有风险；tag 可被移动，pin SHA 才不可变 |
| 仓库超大才处理 | 越晚越难；用 LFS/releases/包管理器控制体积 |

## 简单用户话术

> 我给你的是三样东西：方向（先把门面 README 和社区文件补上），方式（按 A→B→C→D 四张清单逐项检查），边界（什么时候不要自动公开、不要清历史、不要上自托管 runner）。
>
> 如果哪条和你的直觉冲突，请说“我感觉不对劲”，我会停下来重查来源/方案，而不是硬套模板。

## 来源（完整见 SOURCES.md）

- GitHub Docs: [Best practices for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
- GitHub Docs: [About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- GitHub Docs: [Community profiles](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories)
- GitHub Docs: [Managing security and analysis settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository)
- GitHub Docs: [Secure use reference / Actions security hardening](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- GitHub Docs: [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
