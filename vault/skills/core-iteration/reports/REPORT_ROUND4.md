# 核心迭代元能力 · Round 4：信息获取范围扩展

> 日期：2026-09-04 ｜ 类型：post-convergence extension ｜ 状态：已应用，契约 PASS

## 需求

在保证信息获取**深度**与**可信度**的前提下，扩大**广度**，重点纳入 GitHub 等高质量开源信息库。

## 改动

### web-research-consensus (v0.1.1 → v0.2.0)

- `SKILL.md` 新增“扩展信息源：GitHub / 开源库”：
  - 广度入口：仓库搜索、代码搜索、Issues/PRs、Releases、Security Advisories、包生态、awesome/Curated lists、Landscape。
  - 深度规则：读源码/commit diff/PR/issue/release/changelog，不只读 README。
  - 可信度规则：stars/forks/README 宣传不是证据；fork、镜像、同作者仓库不算独立来源；单源需带 repo + commit/tag/release。
- `CONSENSUS.md` 新增 2.6 开源代码库与 GitHub 信息源。
- `SOURCES.md` 补充 GitHub Docs、REST Search API、Security Advisories、OSV 等来源。

### benefit-filter (v0.1.1 → v0.2.0)

- 新增 2.4 开源/GitHub 来源质量判定：
  - 区分一手代码/commit/release 与 README/star。
  - 拒绝把 fork/镜像/同组织或同仓库多个页面当独立来源。
  - 要求开源条目带 `repo_url + commit/tag/release` 或 `package_name + version`。
  - 交叉验证加分：上游一手 + 包生态元数据 + 安全公告库 + 不同生态下游。

### value-meta-scheduler (v0.2.1 → v0.3.0)

- `input` 增加 `info_scope` 与 `info_depth`。
- 新增“信息获取范围与平衡策略”：
  - 默认 `["web","github","package_registry","academic","oss_community"]`。
  - `quick / balanced / deep` 三档控制广度、深度与可信度要求。
  - 明确“增加广度=增加独立视角”，否则只是噪声。

## 验证

- `tools/validate_contract.py`：**PASS**
- `tools/smoke_test.py`：**PASS**
- 能力评分卡保持不变：102 / 120（平均 17.0）；本次是信息源覆盖扩展，不是 Skill 结构能力变化。

## 产物

- 正式库：`$PROJECT_ROOT/vault/skills/core-iteration/`
- 工作区源：`$WORKSPACE/skills/`（同步完成）

## 下一步建议

- 在真实调研任务中切换 `info_depth="deep"` + `info_scope` 包含 `github`，验证是否能找到更多高质量一手证据。
- 可继续把 GitHub API/OSV 等检索入口封装成插件或脚本，进一步自动化“多入口并行检索”。
