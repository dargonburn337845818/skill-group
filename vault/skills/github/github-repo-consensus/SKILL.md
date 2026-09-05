---
name: github-repo-consensus
description: GitHub 开源仓库页/README/目录结构/隐私安全/GitHub Actions 的可执行共识；用于新建或改造开源仓库时按清单检查，给 agent 即拿即用的方向、方式与边界。
whenToUse: 新建或改造 GitHub 开源仓库、写 README、清理 secrets、规划目录结构、配置 GitHub Actions 时。
---
# GitHub 开源仓库共识 · 可调用摘要

> 完整版见本目录 `CONSENSUS.md`；来源见 `SOURCES.md`；施工执行标准见 `REPO_STANDARD.md`。
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

## Agent 自动提交/推送协议（默认执行）

- 代理完成仓库代码/文档任务后，先跑该项目声明的验证（测试、lint、schema）。
- 验证通过后自动 `git add`、`git commit`、`git push` 到当前非保护分支；不要每次停下来问用户“是否推送”。
- 当前分支是受保护 `main` 时，自动创建短生命周期 feature 分支并推送/开 PR；绝不直接强推主分支。
- 推送前用 `git diff --cached` 复核：不提交密钥、本地绝对路径、内部产物/个人状态文件。
- 仓库已有 `scripts/push.sh` 时优先使用（自动化传 `--yes`/`PUSH_CONFIRM=yes`）；没有则用标准 git 命令。
- 推送失败（权限、网络、保护规则）时保留本地提交并说明原因，不要静默放弃或 force push。

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

## 2026 深度补强（Round 38）

> 面向 2026 年仓库工程化的增量检查表：Rulesets、CODEOWNERS、Dependabot 配置、Actions 默认权限、OIDC、可复用 workflow、artifact attestations、组织级默认健康文件。与上文 A–D 四张表互补，不替换旧规则；每条来源见 `SOURCES.md` 的 R38-1～R38-9。

### E1. 用 Repository Rulesets 做“可审计”的分支/推送治理

- **触发**：统一保护 main/release、禁止 force push/删除、要求签名提交、限制文件路径/大小。
- **动作**：
  1. `Settings → Rules → Rulesets` 创建（或 REST API），可覆盖单仓库/多仓库/分支/tag，甚至整个 fork network。
  2. 常用组合：`Require signed commits`、`Block force pushes`、`Require pull request + status checks`、禁止删除/重命名 tag、push rulesets 限制扩展名/路径/文件大小。
  3. 用 `fnmatch` 精确圈定（如 `releases/**/*`）；状态用 Active/Disabled 管理，不要删了再重建。
  4. 旧 branch protection 不必立即拆：与 rulesets 叠加生效，同一规则取更严格者。
- **边界**：每仓库最多 75 条 rulesets；bypass 名单只给真正需要的人；fork 网络的安全要靠 push rulesets 单独覆盖。
- **反例**：把 ruleset 设成 Disabled 当“已经配了”；只给 admin bypass；不检查 fork 是否继承相同 push 规则。

### E2. CODEOWNERS：把“谁负责这块代码”写进仓库

- **触发**：多目录/多团队仓库，想让 PR 自动找到代码责任人。
- **动作**：
  1. 文件放 `.github/CODEOWNERS`（查找顺序 `.github` → 根目录 → `docs`），且必须位于 PR base branch。
  2. 每行 `pattern @user` 或 `@org/team`；同一 pattern 要配多个 owner 时写同一行；后面的匹配覆盖前面的匹配。
  3. owner 必须有仓库 write 权限（team 本身也须可见且有 write）；再配合 ruleset/branch protection 的 “Require review from Code Owners”。
  4. 给 `/.github/CODEOWNERS` 自身也设 owner，防止有人改规则绕过评审。
- **边界**：文件 <3 MB；CODEOWNERS 语法不支持 gitignore 的 `!` 反向、`[ ]` 字符类、`\` 转义 `#`；无效行会被跳过；多位 owner 时任意一位批准即可满足要求。
- **反例**：用 `!`/`[]` 以为生效；列出没有 write 权限的人；以为 root 和 `.github` 的 CODEOWNERS 会合并（实际只取第一个找到的）。

### E3. dependabot.yml 把“依赖 + Actions 自动升级”配置化

- **触发**：想让依赖、第三方 action、被引用的可复用 workflow 自动更新，而不是人工刷。
- **动作**：
  1. 在 `.github/dependabot.yml` 写 `version: 2` + `updates:`，每个 ecosystem 一个条目。
  2. 至少加 `package-ecosystem: github-actions` + `directory: "/"` + `schedule.interval: "weekly"`（Actions 在默认 `.github/workflows`，不必再写子目录）；npm/pip/docker 等按相同模式加。
  3. 用 `open-pull-requests-limit` 控噪音、`ignore` 挡破坏性大版本、`groups` 合并批量 PR；已 pin SHA 的 action 也要看 Dependabot PR，确认版本来源。
  4. fork 上不会因为复制了 `dependabot.yml` 就自动启用，需在 fork 手动开启 Dependabot。
- **边界**：默认只更新 manifest 里显式声明的直接依赖；间接依赖需额外配置；私有 registry 需 `registries` 配置。
- **反例**：只开启 Dependabot alerts 却不配 version updates；把 `open-pull-requests-limit: 0` 当成“已配置”；忽略 Dependabot 对可复用 workflow 的引用更新。

### E4. Actions 默认权限设为只读，job 级显式声明

- **触发**：新建/审查仓库时，还没想清楚每个 job 需要什么权限。
- **动作**：
  1. `Settings → Actions → General → Workflow permissions` 选 “Read repository contents and packages permissions”（restricted）；组织级可设为更严格并禁掉 permissive 选项。
  2. 每个 job 写显式 `permissions:`，只给该 job 真正需要的：`contents: read`、`packages: write`、`id-token: write` 等。
  3. 不需要时关闭 “Allow GitHub Actions to create and approve pull requests”。
- **边界**：有仓库 write 权限的人仍可编辑 workflow 扩大 token 权限；仓库级默认不是防维护者的边界，组织级锁定才更可靠。
- **反例**：依赖默认 permissive “以后再说”；发布 job 写 `permissions: write-all`；让自动化的 GITHUB_TOKEN 能创建/批准 PR。

### E5. 云部署优先 OIDC，而不是长期云 secret

- **触发**：workflow 要推 AWS/Azure/GCP、访问 Vault、登录云容器仓库。
- **动作**：
  1. 只在需要云的 job 写 `permissions: id-token: write`（通常再配合 `contents: read`）。
  2. 用官方 login action（如 `aws-actions/configure-aws-credentials`、`azure/login`、`google-github-actions/auth`）走 OIDC。
  3. 云侧 trust policy 收紧：限制到具体 `repository`、`environment`、`ref`/`job_workflow_ref`，不要用整仓库+任意分支的通配。
  4. 不把长期云密钥复制成 GitHub secret；OIDC token 一次 job 有效。
- **边界**：OIDC 不替代云侧权限设计；私有仓库/自建云同样要先配 IdP；`id-token` 只在需要的 job 给。
- **反例**：所有 job 都加 `id-token: write`；云 trust 写 `repo:owner/repo:ref:refs/heads/*`；一边用 OIDC 一边仍留长期 key 兜底。

### E6. 可复用 workflow：SHA pin、最小传参，不要无脑 `secrets: inherit`

- **触发**：多个仓库/团队共享同一套 CI、发布、安全检查逻辑。
- **动作**：
  1. 被复用文件放 `.github/workflows/reusable-*.yml`，`on` 里写 `workflow_call` 并声明 `inputs`/`secrets`。
  2. 调用方用 `uses: owner/repo/.github/workflows/x.yml@<full-SHA>`；同仓库内优先 `$/.github/workflows/x.yml`（同 commit，不能带 `@ref`）。
  3. 用 `with`/`secrets` 显式传最小数据；`secrets: inherit` 仅限同组织/企业且确实需要全部 secrets 时使用。
  4. 外部/不可信仓库的 reusable workflow 按第三方代码对待：先审后 pin，更新前再看 diff。
- **边界**：`.github/workflows` 下不支持子目录；`on.workflow_call` 不能传 environment secrets，若被复用 workflow 在 job 上写 `environment:` 会改用该环境 secret。
- **反例**：调用 `@main`/`@v1` 可变 ref；对公共 consumer 开 `secrets: inherit`；把敏感 secret 作为普通 input 传进去。

### E7. 发布产物加 artifact attestations（可验证的构建出处）

- **触发**：发布二进制、npm/container 包、带哈希的 manifest，期望用户能验证“谁、在哪个 commit、用什么 workflow 构建”。
- **动作**：
  1. 在发布/打包 job 用 GitHub 官方 `attest-build-provenance` 类 action 生成 attestation；通常需要 `permissions: id-token: write`（按文档还可加 `attestations: write`）。
  2. 需要时附带 SBOM；消费者用 `gh attestation verify` 验证。
  3. 把“验证”写进消费流程，而不是只生成不校验。
- **边界**：attestation 证明“来自哪里/怎么构建”，不等于“没有漏洞”；不要给频繁测试构建、源码/文档/图片等单独签名；public 仓库走 Sigstore Public Good Instance（透明日志公开），private 仓库走 GitHub Sigstore instance（无公开透明日志）。
- **反例**：签了从不验证；把测试构建当发布产物签；声称“有 attestation = 安全”。

### E8. 组织级 `.github` 默认社区健康文件：一处维护，全组织生效

- **触发**：个人/组织有多个仓库，不想在几十个仓库里重复维护 CONTRIBUTING/SECURITY/模板。
- **动作**：
  1. 创建公开的 `.github` 仓库，放入 `CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`SECURITY.md`、`SUPPORT.md`、`FUNDING.yml`、issue/PR 模板与 `config.yml`。
  2. 默认文件只被“没有自己对应文件”的仓库继承；仓库自己的文件覆盖默认文件。
  3. 若仓库自己有 `.github/ISSUE_TEMPLATE` 目录，默认 issue 模板整组不再使用（这是覆盖语义，不是合并）。
- **边界**：`.github` 仓库必须是 public；不能做默认 `LICENSE`，license 必须逐个仓库放；默认文件不出现在各仓库 clone/文件浏览器/包下载中。
- **反例**：把 `.github` 建为 private（默认文件不生效）；只放 README 就以为社区清单齐全；期望默认 issue 模板与仓库自己的模板自动合并。

### Round 38 快速钩子

```text
[ ] Rulesets 覆盖受保护分支，状态 Active，bypass 受控
[ ] CODEOWNERS 放 .github，owner 均有 write 权限且自身也有 owner
[ ] dependabot.yml 含 github-actions ecosystem 并定期检查
[ ] Actions 默认权限只读；高危 job 显式 permissions
[ ] 云部署走 OIDC，无长期云 secret
[ ] 复用 workflow 用 SHA pin，不无脑 secrets: inherit
[ ] 发布产物带 attestation，消费方验证
[ ] 组织有公开 .github 默认健康文件
```

## 来源（完整见 SOURCES.md）

- GitHub Docs: [Best practices for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
- GitHub Docs: [About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- GitHub Docs: [Community profiles](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories)
- GitHub Docs: [Managing security and analysis settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository)
- GitHub Docs: [Secure use reference / Actions security hardening](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- GitHub Docs: [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
