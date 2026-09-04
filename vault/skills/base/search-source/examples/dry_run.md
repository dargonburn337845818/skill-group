# Search-Source 干跑样例

## 场景 1：查某个开源项目的作者指南

- 拆问题：作者如何编写/发布 Skill？
- 入口：GitHub Contents API `github-file`
- 命令：
  ```bash
  python3 tools/info_source_cli.py --proxy-mode host github-file \
    --repo WordPress/agent-skills --path docs/authoring-guide.md
  ```
- 期望：得到 `raw_corpus` 1 条，`source.evidence_rank=docs-file`，`evidence_class=static`，带有可回溯 URL。

## 场景 2：核验一个包的版本是否安全

- 入口：OSV / package registry
- 期望：若 API 不可用，`failures` 中明确记录，不伪造结果。

## 场景 3：无结果时的降级

- 行为：写“当前公开检索未发现”，而不是“不存在”。
