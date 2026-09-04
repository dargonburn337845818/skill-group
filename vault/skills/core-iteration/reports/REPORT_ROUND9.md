# 核心迭代元能力 · Round 9：GitHub 多形态真实采集 + 质量预筛

> 日期：2026-09-04 ｜ 状态：真实 live 采集 9 条 + 质量预筛 PASS

## 新增能力

### GitHub 多形态适配器

| 子命令 | 用途 |
|---|---|
| `github` | 仓库搜索（含完整 metadata） |
| `github-issues` | Issue/PR 搜索（state/comments/labels） |
| `github-releases` | Release 列表（tag/draft/published/assets） |
| `github-code` | 代码搜索（需 `GITHUB_TOKEN`） |

### 质量预筛工具

`tools/repo_quality.py` 对真实 raw_corpus 计算 `quality_score`：

- 仓库：not archived、license、recent push、language、topics 多样性
- Issue：state、comments、labels
- Release：draft、tag、published_at
- stars/forks 仅作为 popularity signal，不计入质量分

## 真实 live 结果

- 采集 9 条：
  - 3 个 GitHub 仓库（cc-switch、rustdesk、rust-lang/rust）
  - 3 个 rust-lang/rust issue/PR
  - 3 个 Rust release（1.98.1 / 1.98.0 / 1.97.1）
- 质量预筛：**avg_score = 86.7**
- 全部通过 Watt host 代理真实返回。

## 验证

- `run_improve_validate.py --proxy-mode host`：✅ CYCLE PASS
- `validate_contract.py`：✅ PASS
- `behavior_test.py`：✅ PASS
- `repo_quality.py`：✅ 输出评分
- workspace + vault 同步：✅

## 产物

- `tools/info_source_cli.py`（v0.4.0 能力）
- `tools/repo_quality.py`
- `tools/output/info_dump.json`（live 9 条）
- `REPORT_ROUND9.md`

## 下一步

1. 把 `repo_quality` 的评分接入 `benefit-filter` 作为“真实数据预筛”输入。
2. 用真实 issue/release 语料蒸馏新的“开源项目健康度”知识节点。
3. 探索 GitHub PR / commit / star history 等更深层适配器。
