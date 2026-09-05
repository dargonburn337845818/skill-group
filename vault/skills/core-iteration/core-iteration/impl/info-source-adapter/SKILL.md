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
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" github --query "topic:rust stars:>100" --limit 10

# OSV 漏洞查询
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" osv --package requests --version 2.31.0

# 包生态元数据
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" pypi --package requests
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" npm --package typescript
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" crates --package serde

# 自动检测 Watt Toolkit / Windows 代理（默认优先 host 代理）
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" --detect-proxy
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
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" --proxy-mode host github --query "topic:rust stars:>100" --limit 10

# GitHub Issues / PR
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" --proxy-mode host github-issues --query "repo:rust-lang/rust bug" --limit 5

# GitHub Releases
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" --proxy-mode host github-releases --repo rust-lang/rust --limit 5

# GitHub Code Search（需 GITHUB_TOKEN）
GITHUB_TOKEN=xxx python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" --proxy-mode host github-code --query "repo:rust-lang/rust fn main" --limit 5

# GitHub 单个文件/文档（Docs/Config/源码，Contents API，可回溯 sha）
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" --proxy-mode host github-file --repo WordPress/agent-skills --path docs/authoring-guide.md

# 对抓到的真实 raw_corpus 做质量预筛
python3 "\$CORE_ITERATION_ROOT/tools/repo_quality.py" --input $CORE_ITERATION_ROOT/tools/output/info_dump.json --top 10

# 注意：Watt host 代理不是标准 CONNECT 代理。
# --proxy-mode host 会改用 curl --resolve 直连 TLS 反代。
# 已实测：GitHub 真实可用；OSV/PyPI/npm/crates 若未被 Watt 加速会返回明确错误。

# 沙箱/离线验证（使用 $CORE_ITERATION_ROOT/tools/fixtures/*.json）
python3 "\$CORE_ITERATION_ROOT/tools/info_source_cli.py" --offline github --query demo

# 一键跑“能力提升 → 验证”循环
python3 "\$CORE_ITERATION_ROOT/tools/run_improve_validate.py" --offline
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

## 2026 深度补强（Round 39）

> 本轮补强方向：不重复上面的“入口清单”，而是把多源结果如何**归一化、定证据类别、扛限流、可离线回归**以及如何识别“伪多源”变成可执行动作。

### 1. 来源归一化：先定实体主键，再合并多源

- 每条 `raw_corpus` 必须同时带 `source.provider`（`github` / `osv` / `npm` / `pypi` / `crates` / `go_proxy` / `arxiv` / `s2` / `crossref` / `openalex` / `oss_community`）与 `source.external_id`（GitHub repo id、OSV id、DOI、arXiv id、CVE id、`name@version`）。
- 对外给用户的 URL 用**人读 canonical URL**：GitHub 用 `html_url` 而不是 `api_url`；包用 registry 的页面/项目 URL；论文优先 DOI/arXiv id，不要把临时搜索结果页当稳定引用。
- 同一实体跨源合并时按 `provider + external_id` 分组，**不能只按名字**：同名包、同名论文在不同生态可能是两个实体。合并时保留每条来源的原始 URL 与抓取时间，不覆盖 provenance。
- 缺少 `external_id` 或 canonical URL 的条目标记 `unattributable`，按硬性纪律第 2 条不得进入正式 raw_corpus，只能进待核验区。

### 2. 证据类别：用“证据等级 + 独立验证”二维判定

| 类别 | 定义 | 能否进最终证据库 |
|---|---|---|
| `primary_official` | 官方文档 / API schema / 发布公告 / 官方 advisory / 官方 changelog | 可以 |
| `primary_author` | 作者/维护者在 README、issue、release 中的明确陈述 | 可以（需作者身份可核验） |
| `secondary_independent` | 第三方独立验证：独立审计、复现实验、OSV 交叉条目、同行评审论文（非预印本） | 可以 |
| `tertiary_clue` | 社区讨论、awesome/landscape、博客、star/downloads/citation 数 | 只作线索，不作证据 |
| `preprint` | arXiv/预印本，未经同行评审 | 可作研究线索，标 `not_peer_reviewed`，不可冒充同行评审 |

- 蒸馏门槛：最终证据库只收前三类；`tertiary_clue` 与 `preprint` 只能在线索表出现，且必须标注“未经独立验证”。
- 反例：Semantic Scholar 的 `citationCount` 不是质量证据；arXiv 列表里的论文不是“已发表”；OSV 的 `aliases` 是同一漏洞的不同编号，不是多条独立证据。

### 3. 限流先行：读 header 再决定，不靠蒙

- GitHub 未认证：搜索类 10 req/min，REST core 约 60 req/hr（认证后按当期文档）。每次请求后记录 `x-ratelimit-remaining`、`x-ratelimit-reset`、`retry-after`。
- 收到 429/403/abuse 后：先把失败写进 `source_scope_report.rate_limits`，按 `retry-after` 退避；**不要立即重试同一请求，更不要吞掉失败继续抓**。
- 对按小时限流的源做 token bucket 或固定速率整形，不是简单 `sleep(1)` 循环。
- OSV/PyPI/npm/crates/arXiv/Crossref 等免费接口也都有礼貌并发与 User-Agent 要求；不要多线程无节制打爆。
- 降级顺序固定为：官方 API → 官方网页/文档 → 可信第三方镜像/网页搜索 → `--offline` fixture；每一级降级都必须写入 `degradation`。

### 4. 离线验证：fixtures 要“真”，断言要“锁契约”

- `fixtures/*.json` 必须来自**真实响应快照**（含 status、关键 headers、body），不要手造“理想 JSON”；至少覆盖成功、未认证限流、缺 token、空结果、schema 变化（缺失/新增字段）五类。
- 离线断言至少要锁：必需字段存在、`external_id` 跨条目唯一、canonical URL 非空、降级路径 `degradation` 非空、`rate_limits` 有数值可复核。
- 外部 API 改字段时，离线测试应先变红，再更新适配器与 fixture；不要直接“容错掉新字段”而失去回归保护。
- CI 用 `--offline` + fixtures 做契约回归；真实调用只做冒烟，避免把网络抖动当适配器失败。

### 5. 多源独立性检查：同一上游只算一源

- 汇总后按 `source.provider + owner/org + author/group` 做独立主体分组；同一仓库、同一作者、同一上游数据库（如 PyPI JSON 与该项目 README 指向同一项目）只算 1 个独立视角。
- 报告里给 `independent_sources`，而不是只用 `total_candidates` 或来源数宣称“多源佐证”；至少 2 个不相关主体才可称“多源交叉”。
- 反例：一个组织的 3 个仓库、同一作者的 3 篇论文、同一条 issue 下的 3 条评论，都不构成 3 个独立来源。

### 6. 查询审计与反例

- 每个查询记录：`raw_query`、`normalized_query`、`endpoint`、`total_count`、`returned_count`、`deduped_count`、`failures`、`truncated`。
- 未认证搜索 API 的 `total_count` 是“命中数”不是“全量可获取数”；超过 `max_per_source` 必须标记 `truncated=true`，不能用 `total_count` 冒充“已全量覆盖”。
- 反例：把 `stargazers_count` / downloads / `citationCount` 当质量证据；把 issue 标题当结论；从 500 条命中只抓前 10 条却写“已覆盖全部”；把 `aliases` 当多条独立证据。

## 来源

- [GitHub REST Search API](https://docs.github.com/en/rest/search/search)
- [GitHub Docs: Using GitHub code search](https://docs.github.com/en/search-github/github-code-search/using-github-code-search)
- [OSV](https://osv.dev/)
- [GitHub Security Advisories](https://github.com/advisories)
- 本地 `web-research-consensus`、`benefit-filter`
