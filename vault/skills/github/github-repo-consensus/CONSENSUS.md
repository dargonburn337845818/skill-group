# GitHub 开源仓库共识（完整版）

> 把 GitHub 官方文档、Open Source Guides 与社区“仓库标准”类技能中的共性蒸馏为 **agent 可直接执行的检查规则**。
> 适用场景：新建开源仓库、把本地项目开源化、审查/改造已有仓库的页面向、隐私安全面、结构面与 Actions 面。
> 每条规则按 `触发 / 动作 / 边界 / 来源` 组织；来源无官方支撑的标 `common-lore`，不冒充官方。

## 0. 一句话共识

**开源仓库交付的不是“代码上传”，而是“让陌生人在 3 秒内知道这是什么、能不能用、怎么上手，并让维护者在后续不因秘密泄露/结构混乱/Action 失控而受伤。”**

四个检查面：

```text
A 页面向  → README + 仓库元数据 + 社区文件
B 隐私面  → visibility + secrets/历史清理 + 安全特性 + 漏洞上报
C 结构面  → 根目录门面 + 分目录 + 大文件策略 + 分支保护
D Action面 → workflow 组织 + secret 处理 + 最小权限 + 第三方信任边界
```

---

## 1. A 仓库页规划

### A1. README 是每个人的第一入口

- **触发**：任何公开/计划公开的仓库；有人问“这个项目能干嘛/怎么跑”。
- **动作**：
  1. 每个仓库都放 README。
  2. README 至少覆盖：项目做什么、为什么有用、如何开始、哪里求助、谁维护。
  3. 放在 `.github`、根目录或 `docs` 任一位置，GitHub 会自动展示；若多处存在，展示顺序为 `.github` → 根目录 → `docs`。
  4. 用相对链接指向仓库内文件（clone 后仍可用），不要只写 GitHub 绝对 URL。
- **边界**：
  - 超过 500 KiB 的 README 在 GitHub 上会被截断。
  - README 只放开发者上手/贡献必需信息；长文档进 `docs/` 或 Wiki。
  - 根目录 README 若与用户名同名，会成为 profile README，语义不同。
- **来源**：GitHub Docs *About READMEs*；*Best practices for repositories*（官方 consensus）。

### A2. Community Profile 是开源仓库的“体检表”

- **触发**：公开仓库想降低贡献门槛、让陌生人愿意提 PR/Issue。
- **动作**：
  1. 至少补：`README`、`LICENSE`、`CODE_OF_CONDUCT`、`CONTRIBUTING`。
  2. 再加 `SECURITY.md`（漏洞上报）和 issue/PR 模板。
  3. Issue 模板必须位于 `.github/ISSUE_TEMPLATE`，且 `.md` 模板含 `name:`/`about:` 或 `.yml` 表单含 `name:`/`description:`，才会被社区清单识别。
  4. PR 模板可放根目录、`docs` 或 `.github`；必须在默认分支上。
- **边界**：
  - 社区清单只是“推荐健康度”，不是法律/质量保证。
  - 没有许可证的仓库仍可能被使用，但“可再分发/可贡献”的意图不清晰；开源项目应尽早选 license。
- **来源**：GitHub Docs *About community profiles*、*Setting guidelines for repository contributors*、*About issue and PR templates*、*Adding a license*（官方 consensus）。

### A3. 仓库元数据（Description + Topics）决定“能不能被搜到”

- **触发**：新仓库创建时；想让项目被主题/搜索发现时。
- **动作**：
  1. Description 写“解决什么问题 + 主要技术/形态”。
  2. Topics 写用途、领域、语言，使用小写字母/数字/连字符，单个 ≤50 字符，总数 ≤20 个。
  3. Topic 名称总是公开的，即使从私有仓库创建也公开。
- **边界**：
  - Topics 不是 SEO 关键词堆砌；误导性 topic 会让访客流失。
  - 私有仓库内容不会被分析，也不会有 GitHub 自动建议 topic。
- **来源**：GitHub Docs *Classifying your repository with topics*（官方 consensus）。

### A4. 可探测的 LICENSE 会显示在仓库页顶部

- **触发**：想明确别人能否使用/修改/再分发。
- **动作**：在根目录放 `LICENSE`（或 `LICENSE.md`，全大写），用 GitHub license picker 或标准文本。
- **边界**：自定义 license 或非标准文件名可能不被 GitHub 自动识别，页面顶部不显示 license 徽标。
- **来源**：GitHub Docs *Adding a license to a repository*（官方 consensus）。

---

## 2. B 隐私 / 安全管理

### B1. 公开前先做“秘密审计”，而不是只加 .gitignore

- **触发**：准备把 private 仓库转 public；怀疑 history 中有 token/密码/密钥。
- **动作**：
  1. 先 `git grep` / 工具扫描当前分支中的 `.env`、密钥、密码、内网地址。
  2. 建 `.gitignore` 忽略 `.env*`、密钥文件、缓存、构建产物、本地数据；已 tracked 的文件用 `git rm --cached` 后再提交 ignore 规则。
  3. 如果 secret 已进入历史：**第一步永远是 revoke/rotate**；之后才考虑 `git filter-repo --sensitive-data-removal` 重写历史。
  4. 重写历史前关闭/绕过分支保护、关闭或合并所有 open PR；重写后 force push 并通知所有协作方重新克隆。
- **边界**：
  - 只改当前文件不解决历史；fork、其他克隆、PR diff、GitHub 缓存 SHA 仍可能保留敏感数据。
  - 历史重写有高风险：commit SHA 改变、签名失效、closed PR diff 消失、协作方再 push 会把敏感数据带回来。
  - 如果 secret 已 revoke/rotate，且你不打算清历史，要明确说明这一决策及其残余风险。
- **来源**：GitHub Docs *Ignoring files*、*Removing sensitive data from a repository*（官方 consensus）。

### B2. 公开仓库的免费安全四件套至少开启

- **触发**：公开仓库创建后；审查安全设置。
- **动作**：
  1. Dependabot alerts：依赖漏洞通知。
  2. Secret scanning：扫描仓库中的 API key/token 并告警。
  3. Push protection：推送包含受支持 secret 时直接阻止。
  4. Code scanning：代码漏洞/错误扫描（公开仓库可用 GitHub Advanced Security 免费特性）。
  5. 写 `SECURITY.md`；可开 Private vulnerability reporting，让研究员私下上报。
- **边界**：
  - 这些特性不替代 2FA、访问控制、最小权限和秘密轮换。
  - 私有仓库的 Advanced Security 可能需要组织许可证/席位；公开仓库通常自动获得。
- **来源**：GitHub Docs *Best practices for repositories*、*Managing security and analysis settings*、*Quickstart for securing your repository*（官方 consensus）。

### B3. visibility 切换有明确、不可逆的后果

- **触发**：用户要 public↔private 切换前。
- **动作**：先读 GitHub Docs 后果清单，再操作；重点确认：
  - private → public：代码、forks、Actions 历史/日志全部公开；所有 push rulesets 被禁用；star/watch 清空。
  - public → private：public forks 会 detach 成独立网络；GitHub Pages 自动取消发布，若配了 custom domain 要处理 DNS 防 domain takeover；一些免费功能/Advanced Security 停止；star/watch 清空。
- **边界**：不能期望切回 private 后“收回”已经 clone/fork 的代码；公开后不可逆地进入互联网。
- **来源**：GitHub Docs *Setting repository visibility*（官方 consensus）。

### B4. 最小权限与分支保护

- **触发**：仓库有多个协作者；希望 main 不被直接 push。
- **动作**：
  1. 只给必要的人必要的角色；定期审查权限。
  2. 对 `main`/`release` 等关键分支启用保护：要求 PR 评审、要求状态检查、禁止 force push、禁止删除。
  3. 常规协作者用同仓库分支 + PR，而不是 fork（fork 主要用于非关联外部贡献者）。
- **边界**：
  - 若多个 workflow 的 job 同名，状态检查可能歧义并阻塞合并；job 名保持唯一。
  - 分支保护规则默认不限制 admin，需要时显式“do not allow bypass”。
- **来源**：GitHub Docs *Best practices for repositories*、*About protected branches*（官方 consensus）。

---

## 3. C 结构规划

### C1. 根目录是“文件系统门面”

- **触发**：初始化仓库；访客第一次打开文件树。
- **动作**：根目录放人先看的文件：

```text
README.md            # 是什么/怎么用
LICENSE              # 再分发权限
CONTRIBUTING.md      # 贡献流程
SECURITY.md          # 漏洞上报
CODE_OF_CONDUCT.md   # 社区行为（可选但推荐）
CHANGELOG.md         # 版本变化（可选）
.gitignore           # 忽略本地/敏感/构建产物
```

- **边界**：根目录文件过多会淹没核心代码；能合并的指南（如 CONTRIBUTING + 开发文档）不要硬拆。
- **来源**：GitHub Docs *About community profiles*、*Best practices for repositories*（官方 consensus）；社区仓库标准 skill 交叉验证（style）。

### C2. 代码/文档/测试/示例/脚本按功能分目录

- **触发**：仓库开始有规模、多种类型文件并存。
- **动作**：按语言/生态常见约定分目录，例如：

```text
src/                 # 源码
docs/                # 长文档、指南、截图
tests/               # 测试
examples/            # 可运行示例
scripts/             # 开发脚本/工具
.github/             # 贡献模板与 workflows
assets/ 或 resources/# 图片/资源（注意大小）
```

- **边界**：
  - 目录划分不是越细越好；新人从树上看不懂就应合并。
  - 没有“第二个实现”时不要为未来预留抽象目录。
- **来源**：GitHub Docs *Best practices for repositories*；*How to contribute (Open Source Guides)* anatomy（风格/共识）；社区讨论（style，非官方强制）。

### C3. 大文件与仓库体积控制

- **触发**：包含二进制、模型、数据库、图片、构建产物。
- **动作**：
  1. 文件 >50 MiB 会有警告，>100 MiB 被 GitHub 阻止；浏览器上传 >25 MiB 受限。
  2. 需要跟踪大文件时用 Git LFS；也可用 Releases 分发大型二进制。
  3. 仓库建议保持 <1 GB，强建议 <5 GB；用包管理器而不是把依赖源码入库。
  4. 定期用 `git-sizer` 等工具分析体积。
- **边界**：Git 不适合做备份/大数据库共享；不要把依赖/产物当作备份。
- **来源**：GitHub Docs *About large files on GitHub*（官方 consensus）。

### C4. `.github/` 是“机器与人”的协作目录

- **触发**：需要 issue/PR 模板、workflows、社区健康文件。
- **动作**：
  - `.github/ISSUE_TEMPLATE/`：issue 模板（.md 或 .yml）
  - `.github/PULL_REQUEST_TEMPLATE.md`：PR 模板
  - `.github/workflows/`：Actions workflows
  - `.github/CODE_OF_CONDUCT.md`、`CONTRIBUTING.md` 也可放这里
- **边界**：模板必须在默认分支才生效；不要建多层复杂模板，保持贡献者能快速填写。
- **来源**：GitHub Docs *About issue and PR templates*、*Setting guidelines*（官方 consensus）。

---

## 4. D GitHub Actions 使用

### D1. workflow 的存放与触发

- **触发**：要加 CI、发布、自动检查。
- **动作**：
  1. 文件放在 `.github/workflows/*.yml|yaml`。
  2. 用 `on` 精确指定事件；用 branches/paths 过滤减少无关运行；需要手动时用 `workflow_dispatch`。
  3. 用 `name`/`run-name` 让 Actions 页可读。
- **边界**：
  - 触发条件写宽会消耗配额、放大攻击面；写太窄可能漏掉关键检查。
  - 同一事件多个触发会启动多个 run。
- **来源**：GitHub Docs *Workflow syntax*（官方 consensus）。

### D2. secrets 永远走 GitHub Secrets，且处理要防御

- **触发**：workflow 需要 token/密码/私钥。
- **动作**：
  1. 在仓库/环境/组织级配置 secret；用 `gh secret set` 也可以。
  2. 工作流文件里只写 `${{ secrets.NAME }}`，绝不写明文。
  3. 给 `GITHUB_TOKEN` 最小权限（默认 `contents: read`，按 job 提升）。
  4. 非 GitHub secret 的敏感值用 `::add-mask::VALUE` 掩码；生成的派生 secret 也注册为 secret。
  5. 不要把 JSON/XML/YAML 整块当 secret——结构化数据会大幅降低日志脱敏成功率。
  6. 定期审计 secret 是否仍需要，及时删除/轮换；可在 environment 上要求审批再暴露 secret。
- **边界**：
  - GitHub 的自动 redaction 不保证覆盖所有变换/编码/错误输出。
  - 有 write 权限的协作者可读取仓库级 secret，所以 secret 权限与仓库权限同风险。
  - 日志一旦泄露未脱敏 secret：删日志并轮换 secret，单靠删日志不够。
- **来源**：GitHub Docs *Secure use reference (Actions security hardening)*、*Using secrets in GitHub Actions*、*Use GITHUB_TOKEN for authentication*（官方 consensus）。

### D3. 第三方 action 信任边界

- **触发**：引用 `uses: some/action@...` 或复用第三方 workflow。
- **动作**：
  1. 优先 pin 到 full-length commit SHA（当前 GitHub 建议的不可变方式）；pin 前确认 SHA 来自 action 原仓库而非 fork。
  2. 若用 tag，应信任创建者（Marketplace “Verified creator” 是信号），并知道 tag 可被移动/删除。
  3. 第三方 workflow 与 action 同样处理；可用 Dependabot version updates 保持更新。
  4. 可运行 OSSF Scorecards 检查 token 权限、是否 pin、脚本注入风险。
- **边界**：
  - Dependabot 不对 pin 到 SHA 的 action 生成漏洞 alert，只对语义版本 action 告警。
  - 一个被攻破的 action 可访问仓库所有 secrets 并用 GITHUB_TOKEN 写仓库，影响很大。
- **来源**：GitHub Docs *Secure use reference*（官方 consensus）。

### D4. 不可信 PR 代码与特权 trigger

- **触发**：公开仓库接受 fork PR；需要跑测试/发布。
- **动作**：
  1. 默认用 `pull_request` 处理外部 PR（无 secret/写权限）。
  2. 避免不必要的 `pull_request_target` 和 `workflow_run`；它们有特权上下文。
  3. 若必须用 `pull_request_target`/`workflow_run`，不要 checkout 不可信 PR/artifact 代码，并参考 GitHub 的 secure usage 指南。
  4. 公共仓库不要用 self-hosted runner：任何 fork PR 都可能持久化中毒 runner；优先 GitHub-hosted ephemeral runner。
- **边界**：
  - `pull_request_target` 的历史漏洞常来自“checkout 了 PR 代码却又持有 secret”；这不是“换个 trigger 就好”，而是要隔离不可信代码。
  - 自托管 runner 就算用完销毁也难保证只跑一个 job。
- **来源**：GitHub Docs *Secure use reference*（官方 consensus）。

### D5. 防止脚本注入

- **触发**：workflow 中把 PR title/issue body/commit message 等不可信输入拼进 shell。
- **动作**：
  1. 优先写 JavaScript action 或把输入作为参数传给 action，而不是拼 shell。
  2. 内联脚本时用中间环境变量传值，再在脚本里引用 `"$VAR"`，不要直接内插。
  3. 对敏感/不可信输出做 `::add-mask::` 并人工复核 run logs。
- **边界**：直接 `run: echo ${{ github.event.issue.title }}` 属于典型注入面；即使看起来“只是打印”也可能被利用。
- **来源**：GitHub Docs *Secure use reference*（官方 consensus）。

---

## 5. 开源前 10 项总检查清单

```text
[ ] README 三段式：这是什么 / 为什么有用 / 怎么开始
[ ] Description + topics 写清用途（≤20 topics，≤50 字符）
[ ] LICENSE 已选并放根目录
[ ] CONTRIBUTING / CODE_OF_CONDUCT / SECURITY.md 已放
[ ] issue/PR 模板位于 .github/ISSUE_TEMPLATE 与默认分支
[ ] .gitignore 已忽略 .env/密钥/缓存/构建产物
[ ] 历史中的 secret 已 revoke/rotate；必要时已清历史
[ ] 公开仓库免费安全四件套已开启
[ ] 大文件用 LFS/Releases，仓库体积可控
[ ] Actions：最小权限、secrets 只走 GitHub Secrets、第三方 action pin SHA、无危险特权 trigger
```

---

## 6. 反模式速查（会翻车的做法）

| 反模式 | 正确做法 |
|---|---|
| README 写成项目说明书长篇 | README 门面化，详情进 docs/Wiki |
| 把 LICENSE/CONTRIBUTING 藏在深层目录 | 放根目录或 GitHub 识别的位置 |
| 只加 .gitignore 就公开 | 先 revoke/rotate 已泄露 secret，必要时清历史 |
| 切 public 前不检查 Actions 日志 | public 后 Actions 历史/日志对所有人可见 |
| 私有仓库直接用明文 secret 测试 | 养成“secret 只进 GitHub Secrets”习惯，避免复制到代码 |
| workflow 给 GITHUB_TOKEN 全权限 | 默认只读，job 级按需提升 |
| 第三方 action 直接 `@master`/`@main` | pin full SHA，或至少 tag + 信任作者 |
| 用 `pull_request_target` 跑外部 PR 代码 | 能不用就不用；用也要隔离不可信代码 |
| 公共仓库用 self-hosted runner | 用 GitHub-hosted ephemeral runner |
| 一次建几十个 workflow/目录 | 先最小化，跑通后再增量 |

---

## 7. 样例干跑（dry-run 验证）

### 样例 1：把一个本地 CLI 工具开源

按 A→B→C→D：

1. 写 README（安装/示例/截图）。
2. 补 MIT LICENSE、CONTRIBUTING、SECURITY.md。
3. 扫描 `.env` 与历史；revoke 老 token；加 .gitignore。
4. 目录：`src/`、`tests/`、`docs/`、`examples/`、`.github/`。
5. GitHub Actions：`ci.yml` 用 `pull_request` + `push`，`permissions: contents: read`，`actions/checkout@v4` 后跑测试。
6. 公开前再跑社区 profile check。

### 样例 2：已有仓库改造

1. 看 Community Profile 缺什么，先补 README/LICENSE/CONTRIBUTING。
2. 检查 Security 设置，开启免费四件套。
3. 检查 `.gitignore` 与历史；有 secret 先 rotate。
4. 检查 workflows 的 secret 使用与权限；把第三方 action 从 tag 改成 pin SHA。
5. 保留小步提交，每步可回滚。

### 样例 3：Agent 被要求“帮我写个发布 release 的 workflow”

1. 问清触发：手动 `workflow_dispatch` 还是 tag push。
2. workflow 放 `.github/workflows/release.yml`。
3. `permissions: contents: write` 仅在此 job 需要时；secrets 全部用 `secrets.*`。
4. 发布动作 pin SHA；若用第三方 release action，确认可信并锁版本。
5. 提醒：公开仓库的 release 会立即公开，不要把未清理的密钥/大文件打进 release asset。

---

## 8. 来源表

### 官方（高权重，consensus）

| 编号 | 来源 | 贡献 |
|---|---|---|
| G1 | GitHub Docs: [Best practices for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories) | README、安全四件套、分支 vs fork、LFS |
| G2 | GitHub Docs: [About the repository README](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | README 内容/位置/500KiB/相对链接 |
| G3 | GitHub Docs: [About community profiles for public repositories](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories) | 社区健康文件清单 |
| G4 | GitHub Docs: [Setting guidelines for repository contributors](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors) | CONTRIBUTING 位置/入口 |
| G5 | GitHub Docs: [About issue and pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates) | 模板位置/格式要求 |
| G6 | GitHub Docs: [Adding a license to a repository](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository) | LICENSE 识别/展示 |
| G7 | GitHub Docs: [Classifying your repository with topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) | topics 规范 |
| G8 | GitHub Docs: [Managing security and analysis settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository) | 免费安全特性/私有差异 |
| G9 | GitHub Docs: [Quickstart for securing your repository](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository) | 访问管理/依赖图/告警 |
| G10 | GitHub Docs: [Adding a security policy](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy) | SECURITY.md |
| G11 | GitHub Docs: [Setting repository visibility](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility) | public/private 后果 |
| G12 | GitHub Docs: [Ignoring files](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files) | .gitignore |
| G13 | GitHub Docs: [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | 历史清理/危害/先 rotate |
| G14 | GitHub Docs: [About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) | 体积限制/LFS |
| G15 | GitHub Docs: [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | 分支保护 |
| G16 | GitHub Docs: [Secure use reference (Actions security hardening)](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/security-hardening-for-github-actions) | Actions secrets/权限/pin SHA/特权 trigger/自托管 |
| G17 | GitHub Docs: [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) | secrets 配置 |
| G18 | GitHub Docs: [Use GITHUB_TOKEN for authentication](https://docs.github.com/en/actions/security-guides/automatic-token-authentication) | GITHUB_TOKEN 最小权限 |
| G19 | GitHub Docs: [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | workflow 存放/触发/filters |

### 社区/交叉验证（style / warning）

| 编号 | 来源 | 贡献 |
|---|---|---|
| C1 | [Open Source Guides](https://opensource.guide/) / [How to contribute](https://opensource.guide/how-to-contribute/) | 开源项目 anatomy、社区健康 |
| C2 | GitHub Community Discussion: [How to write a good README?](https://github.com/orgs/community/discussions/170496) | README 实践（社区交叉） |
| C3 | GitHub Community Discussion: [How can I effectively organize folders and files in a large GitHub repository?](https://github.com/orgs/community/discussions/168684) | 目录组织（风格） |
| C4 | GitHub Community Discussion: [How can I prevent secrets from being exposed in a public repository?](https://github.com/orgs/community/discussions/187601) | 公开仓库 secret 泄漏警惕（warning） |
| C5 | GitHub Community Discussion: [What's the best way to handle sensitive information (like API keys) in my GitHub project?](https://github.com/orgs/community/discussions/167222) | 敏感信息处理（warning） |
| C6 | [GitHub Actions Supply Chain Hardening Checklist 2026](https://safeguard.sh/resources/blog/github-actions-supply-chain-hardening-checklist-2026) | Actions 供应链清单（warning 交叉） |
| C7 | [How we manage GitHub Actions](https://pkl-lang.org/blog/how-we-manage-github-actions.html) | Actions 组织/维护实践（style） |
| C8 | [GitHub Repo Guidelines (Creative Commons)](https://opensource.creativecommons.org/contributing-code/github-repo-guidelines/) | 仓库规范/结构（style） |
| C9 | [open-source-best-practices skill](https://github.com/AndreaGriffiths11/open-source-best-practices) | 开源项目启动清单（style 交叉） |
| C10 | [github-repository-standards skill](https://github.com/organvm-iv-taxis/a-i--skills/blob/main/distributions/codex/skills/github-repository-standards/SKILL.md) | 仓库标准技能（style 交叉） |
| C11 | [readme-guidelines skill](https://github.com/maximosovsky/readme-guidelines/blob/main/SKILL.md) | README 结构（style 交叉） |
| C12 | [ai-agent-rules/github-actions-workflow-rules](https://github.com/Baneeishaque/ai-agent-rules/blob/master/github-actions-workflow-rules.md) | workflow 规则（style 交叉） |

### 本地实践

- `$HOME/work/GITHUB_DESCRIPTIONS.md`：现有仓库 description 示例。
- `$HOME/work/dsh-skill-vault/`：本仓库的 README/`.github/workflows/release-plugin.yml` 是“仓库页 + Actions”实例。
- `$HOME/work/dsh-optimization-consensus/CONSENSUS.md`：与“先提醒用户、先隔离冒烟、回滚实际文件”一致的运维纪律，在公开/发布操作时同样适用。
