# CHANGELOG

## 2026-09-04 · v0.2.0 · Round 6

- 实现真实调用 CLI：`tools/info_source_cli.py`（GitHub/OSV/PyPI/npm/crates）
- 实现离线 fixtures 与 `--offline` 沙箱验证模式
- 实现 `tools/run_improve_validate.py`：能力提升→验证一键循环

## 2026-09-04 · v0.3.0 · Round 8

- GitHub 适配器增加完整元数据（stars/forks/language/topics/license/pushed_at/open_issues）
- 明确 popularity_signals 只是流行度信号，不是证据
- 真实 live 调用验证通过

## 2026-09-04 · v0.4.0 · Round 9

- 新增 GitHub Issues/PR、Releases、Code Search 适配器
- 新增 tools/repo_quality.py 真实数据质量预筛
- 真实 live 采集扩展到 9 条（repo+issue+release）

## 2026-09-04 · v0.5.0 · Round 10

- 新增 GitHub commits / PR 适配器
- 新增 tools/benefit_filter_live.py：真实数据收益过滤器
- 真实 pipeline：15 条 live 语料全部通过预筛

## 2026-09-04 · v0.6.0 · Round 24

- 新增 `github-file` 适配器：通过 Contents API 拉取单个 GitHub 文件/文档，输出 `docs-file`/`code-fragment` + sha。
- SKILL.md 适配器表与命令示例同步更新。

## 2026-09-04 · v0.7.0 · Round 29

- 输出契约标题规范化为“输出契约”，新增干跑验证小节。
