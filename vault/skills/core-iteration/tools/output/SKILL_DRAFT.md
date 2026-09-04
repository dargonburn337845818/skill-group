---
name: live-github-intel
description: 从真实 GitHub 仓库/issue/release/commit/PR 提炼的开源情报与维护性判断规则。
whenToUse: 需要评估/理解 GitHub 开源项目、已知问题、版本变更或提交历史时。
---

# Live GitHub Intel Skill Draft

> 本草案由 `skill_draft_builder.py` 从真实 live 语料自动生成，所有 Node 均为 `verified-single`，需要多源交叉验证后才能发布为正式核心知识。

## 触发条件

- 需要评估开源仓库的 license/活跃度/生态/topics。
- 需要理解 issue/PR 讨论或 release 变更。
- 需要定位具体 commit/代码变化。

## 核心动作

1. 先回到 repo/issue/release/commit 原始 URL。
2. 用 metadata 判断健康度；stars/forks 只当流行度信号。
3. 单源信息标记 verified-single，多源一致才升级 verified-high。

## 知识节点（Node 列表）

### live_github_1
- claim: example/oss-tool: A real OSS tool for testing adapter normalization. [repo: https://github.com/example/oss-tool]
- trigger: 当需要评估/选择开源仓库时
- action: 检查 license、recent push、语言、topics、是否 archived，把 stars/forks 当流行度信号而非证据
- boundary: 单仓库单源信息；README 可能过时；需要独立旁证才能升级 verified-high
- source_refs: https://github.com/example/oss-tool

### live_github_2
- claim: example/another-tool: Second repo to prove independent entry. [repo: https://github.com/example/another-tool]
- trigger: 当需要评估/选择开源仓库时
- action: 检查 license、recent push、语言、topics、是否 archived，把 stars/forks 当流行度信号而非证据
- boundary: 单仓库单源信息；README 可能过时；需要独立旁证才能升级 verified-high
- source_refs: https://github.com/example/another-tool

### live_osv_3
- claim: CVE-2026-1: Example package has a cross-site scripting issue before version 2.0.0. [source: https://osv.dev/vulnerability/CVE-2026-1, package: example-package]
- trigger: 当发现相关外部信息时
- action: 回到原始来源阅读完整上下文
- boundary: 单源信息；需独立验证
- source_refs: https://osv.dev/vulnerability/CVE-2026-1

### live_package_registry_4
- claim: example-package: Example PyPI package for offline adapter test. [package: example-package@1.2.3, source: https://pypi.org/project/example-package/]
- trigger: 当发现相关外部信息时
- action: 回到原始来源阅读完整上下文
- boundary: 单源信息；需独立验证
- source_refs: https://pypi.org/project/example-package/

### live_package_registry_5
- claim: example-npm-pkg: Example npm package for offline adapter test. [package: example-npm-pkg@3.4.5, source: https://www.npmjs.com/package/example-npm-pkg]
- trigger: 当发现相关外部信息时
- action: 回到原始来源阅读完整上下文
- boundary: 单源信息；需独立验证
- source_refs: https://www.npmjs.com/package/example-npm-pkg

### live_package_registry_6
- claim: example-crate: Example crate for offline adapter test. [crate: example-crate, source: https://github.com/example/crate]
- trigger: 当发现相关外部信息时
- action: 回到原始来源阅读完整上下文
- boundary: 单源信息；需独立验证
- source_refs: https://github.com/example/crate

### live_github_issue_7
- claim: Example issue for offline test: Example issue for offline test
This is a real-looking issue body.
- trigger: 当需要理解已知问题/讨论/决策时
- action: 读 issue 正文、labels、评论数与关联 PR，避免只看标题
- boundary: issue 可能已过期、观点化或未被合并；单源需要交叉验证
- source_refs: https://github.com/example/repo/issues/1

### live_github_release_8
- claim: Example Release v1.0.0: Example Release v1.0.0
Breaking change and migration guide.
- trigger: 当需要确认版本、变更、迁移或安全修复时
- action: 读 release body、tag、publish date 与 assets，对照 CHANGELOG
- boundary: release notes 可能省略破坏性变更；以实际代码/commit 为准
- source_refs: https://github.com/example/repo/releases/tag/v1.0.0

### live_github_commit_9
- claim: abc123def456: fix: example commit message

Body line.
- trigger: 当需要定位具体代码改动时
- action: 读 commit message，回到 diff/sha 验证；commit 是最接近一手代码的证据
- boundary: commit message 可能简洁或误导；单个 commit 不代表完整上下文
- source_refs: https://github.com/example/repo/commit/abc123def456

### live_github_pr_10
- claim: Example PR for offline test: Example PR for offline test
This PR changes something.
- trigger: 当需要评估一个提议中的改动时
- action: 读 PR 标题/正文/diff/评论与 merged 状态
- boundary: PR 可能未合并或后来被否决；不能当作已落地事实
- source_refs: https://github.com/example/repo/pull/1

### live_github_code_11
- claim: example/repo:src/main.rs: File: src/main.rs in example/repo
fn main() { println!("hello"); }
- trigger: 当发现相关外部信息时
- action: 回到原始来源阅读完整上下文
- boundary: 单源信息；需独立验证
- source_refs: https://github.com/example/repo/blob/main/src/main.rs

## 来源与可追溯

- `tools/output/info_dump.json`
- 每个 Node 的 `trace_chain` 保留原始链路。
