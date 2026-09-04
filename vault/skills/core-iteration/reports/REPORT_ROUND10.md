# 核心迭代元能力 · Round 10：真实 pipeline 执行层

> 日期：2026-09-04 ｜ 状态：信息采集 → 质量预筛 → 真实收益过滤 全链路可执行

## 新增

### GitHub 更完整适配器

- `github-commits`：仓库 commit 历史（sha/author/date/message）
- `github-pr`：PR 搜索（state/comments/labels/merged_at）
- 加上已有：repo / issues / releases / code search

### 真实收益过滤器

`tools/benefit_filter_live.py`：

- 读 `info_dump.json`
- 对每条真实语料计算 quality/density
- 输出契约：
  - `verified_high`
  - `pending_verification`
  - `discarded_low_density`
  - `yield_stats`

## 真实 live 结果

- 采集 15 条：
  - 3 GitHub repos
  - 3 GitHub issues
  - 3 GitHub releases
  - 3 GitHub commits
  - 3 GitHub PRs
- 质量预筛：avg 72.0
- 收益过滤：
  - `verified_single=15`
  - `avg_density_score=92.0`
  - `pending=0`
- 说明：当前都是单源证据，所以全部为 `verified-single`（weight 0.5），没有误判为 verified-high。

## 验证

- `run_improve_validate.py --proxy-mode host`：✅ CYCLE PASS
- `validate_contract.py`：✅ PASS
- `behavior_test.py`：✅ PASS
- workspace + vault 同步：✅

## 产物

- `tools/info_source_cli.py`（v0.5.0）
- `tools/benefit_filter_live.py`
- `tools/repo_quality.py`
- `tools/output/info_dump.json`（live 15 条）
- `REPORT_ROUND10.md`

## 下一步

1. 用真实 verified-single 语料做“蒸馏执行器”：自动把 issue/release/commit 提炼成 Node。
2. 多源交叉验证：同一主题找多个独立 repo/issue 合成 verified-high。
3. 接入 `value-iterator` 自动生成 changelog。
