---
name: info-source-adapter
description: 信息获取执行层——把 GitHub/OSV/包生态/学术/OSS 社区等高质量信息源变成可调用、可归一化的检索适配器，输出 raw_corpus 与 source_scope_report；用于让“信息搜集”从文档规则变成真实可执行的多源获取。
whenToUse: 需要真正调用 GitHub、OSV、包仓库、学术库等外部信息源获取一手资料；需要把多渠道检索结果归一化成 raw_corpus；需要知道本次获取覆盖了哪些源、遇到什么限制。
---

# 信息获取适配器（Info Source Adapter）

> 定位：`web-research-consensus` 回答“怎么查、怎么可信”；本 skill 回答“实际去查什么、用什么入口、如何把结果统一喂给下游”。它是信息搜集阶段的**执行层**。

## 触发条件

- 调度器设置了 `info_scope`，需要按来源类型实际检索。
- 用户要求“查 GitHub / 查包生态 / 查安全公告 / 查论文”等具体来源。
- 需要在报告中说明“本轮查了哪些源、用了哪些查询、有哪些限制”。

## 输入约定

```text
input = {
  info_scope: ["web", "github", "package_registry", "academic", "oss_community"],
  queries: [ "搜索表达式" ],
  target_entities?: [ "repo/package/paper/author" ],
  token_env?: [ "GITHUB_TOKEN", "OSV_API_KEY" ],   # 可选，缺失时走公开接口/网页搜索
  max_per_source?: 20,
  time_window?: "recent" | "all"
}
```

## 可用适配器

| 类型 | 入口 | 主要产物 | 可信度注意 |
|---|---|---|---|
| GitHub 仓库 | GitHub Search / REST `/search/repositories` | repo_url, stars, topics, license, last_commit | stars/forks 不是证据，读 README/源码/commit |
| GitHub 代码 | Code Search / REST `/search/code` | 代码片段、文件路径、仓库 | 需要具体到 commit/路径 |
| GitHub 文件/文档 | Contents API `/repos/{repo}/contents/{path}` | 具体文件文本（docs/source/config） | evidence_rank=`docs-file`/`code-fragment`，可回溯 sha |
| GitHub Issues/PR | `repo/issues` 搜索、`/search/issues` | 已知问题、决策、维护状态 | 以 thread 为准，不只看标题 |
| Releases/Changelog | `releases` / `CHANGELOG.md` | 版本、破坏性变更、迁移 | 与代码行为交叉验证 |
| Security Advisories | GitHub Advisories、OSV API | CVE、受影响版本、修复版本 | 以公告 + 修复 commit 为准 |
| Package Registry | npm/PyPI/Maven/crates/Go proxy 元数据 API | version, dependencies, maintainers, publish date | 不看下载量当质量证据 |
| Academic | arXiv/Semantic Scholar/PubMed/Crossref | 论文、DOI、版本 | 区分预印本/同行评审 |
| OSS Community | awesome lists, Landscape, RFC, mailing list | 生态地图、路线图、讨论 | 只是线索，不是证据 |

## 真实调用（已实现工具）

本 skill 配套可执行 CLI，不再只是文档：

```bash
# GitHub 仓库搜索
python3 tools/info_source_cli.py github --query "topic:rust stars:>100" --limit 10

# OSV 漏洞查询
python3 tools/info_source_cli.py osv --package requests --version 2.31.0

# 包生态元数据
python3 tools/info_source_cli.py pypi --package requests
python3 tools/info_source_cli.py npm --package typescript
python3 tools/info_source_cli.py crates --package serde

# 自动检测 Watt Toolkit / Windows 代理（默认优先 host 代理）
python3 tools/info_source_cli.py --detect-proxy
# 当前机器（WSL）实际返回:
#   system: http://127.0.0.1:26501       (系统代理，已弃用)
#   host:   http://172.30.160.1:443      (host 代理模式，默认使用)
#
# 手动指定模式:
#   --proxy-mode auto   # 默认，优先 host
#   --proxy-mode host   # 使用 Watt host 代理（curl --resolve 直连反代）
#   --proxy-mode system # 使用系统代理 http://127.0.0.1:26501
#   --proxy-mode none   # 不使用代理

# 使用 host 代理真实调用 GitHub（已实测 OK）
python3 tools/info_source_cli.py --proxy-mode host github --query "topic:rust stars:>100" --limit 10

# GitHub Issues / PR
python3 tools/info_source_cli.py --proxy-mode host github-issues --query "repo:rust-lang/rust bug" --limit 5

# GitHub Releases
python3 tools/info_source_cli.py --proxy-mode host github-releases --repo rust-lang/rust --limit 5

# GitHub Code Search（需 GITHUB_TOKEN）
GITHUB_TOKEN=xxx python3 tools/info_source_cli.py --proxy-mode host github-code --query "repo:rust-lang/rust fn main" --limit 5

# GitHub 单个文件/文档（Docs/Config/源码，Contents API，可回溯 sha）
python3 tools/info_source_cli.py --proxy-mode host github-file --repo WordPress/agent-skills --path docs/authoring-guide.md

# 对抓到的真实 raw_corpus 做质量预筛
python3 tools/repo_quality.py --input tools/output/info_dump.json --top 10

# 注意：Watt host 代理不是标准 CONNECT 代理。
# --proxy-mode host 会改用 curl --resolve 直连 TLS 反代。
# 已实测：GitHub 真实可用；OSV/PyPI/npm/crates 若未被 Watt 加速会返回明确错误。

# 沙箱/离线验证（使用 tools/fixtures/*.json）
python3 tools/info_source_cli.py --offline github --query demo

# 一键跑“能力提升 → 验证”循环
python3 tools/run_improve_validate.py --offline
```

- 真实调用：Watt host 代理可加速的域名（如 GitHub）可真实返回；未加速域名可使用 `--offline` 固定样本验证同一契约。
- 输出均为 `raw_corpus + source_scope_report`，可直接喂给 `benefit-filter`。

## 输出契约

```text
source_scope_report = {
  sources_queried: [ { type: "github", endpoint: "...", queries: n, results: n, failures: [] } ],
  total_candidates: n,
  rate_limits: [ "GitHub unauthenticated: 10 req/min", ... ],
  degradation: [ "OSV unavailable -> used web search" ],
  coverage_notes
}

raw_corpus_entry = {
  chunk_id,
  text,
  source: { type, url, title, author, publisher, date, evidence_rank },
  claim?,
  gap_id?
}
```

## 干跑验证

- 用 `github-file` 拉取一份真实文档，确认 `raw_corpus` 有 `evidence_class=static` 与可回溯 URL。
- 用 `--offline` 跑 GitHub/OSV/PyPI/npm/crates 固定样本，确认契约一致。
- 用 `skill_package_check.py` 检查接入后的 Skill 包，确认无 issue。

## 硬性纪律
2. **可归因才入库**：每条 raw_corpus 必须带真实 URL/API 返回的标识；无法归因的缓存内容不得进入。
3. **API 缺失要降级**：没有 token、限流或被拒时，切换到公开网页搜索/文档入口，并在 `degradation` 说明；不要伪造“查到了”。
4. **不把热度当证据**：stars、downloads、awesome 收录只是候选信号，进入蒸馏前仍按 `benefit-filter` 的独立性/证据规则处理。
5. **保留原始上下文**：截取代码/issue/commit 时保留上下文，避免断章取义。

## 边界 / 反模式

| 情况 | 处理 |
|---|---|
| 只有 GitHub REST 结果没有 commit/tag | 标 `single-doubt`，不直接作为核心证据 |
| 多个结果来自同一仓库/同一作者 | 合并为单源，不人为增加“多源” |
| API 返回旧数据 | 标注抓取时间，必要时到仓库当前状态复核 |
| 包元数据下载量很高 | 只说明流行度，不说明质量/正确性 |
| 为了“广”而每个源都抓一堆 | 设 `max_per_source`，优先独立视角，不堆数量 |

## 简单用户话术

> 我可以把 GitHub、漏洞公告、包仓库、论文库这些入口串起来，统一抓取并归一化成可过滤的语料；每条都会标明来源和限制，不会拿 star 数或下载量冒充证据。

## 来源

- [GitHub REST Search API](https://docs.github.com/en/rest/search/search)
- [GitHub Docs: Using GitHub code search](https://docs.github.com/en/search-github/github-code-search/using-github-code-search)
- [OSV](https://osv.dev/)
- [GitHub Security Advisories](https://github.com/advisories)
- 本地 `web-research-consensus`、`benefit-filter`
