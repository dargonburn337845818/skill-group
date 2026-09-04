# 核心迭代元能力 · Round 8：GitHub 真实数据增强

> 日期：2026-09-04 ｜ 状态：真实调用成功 + 适配器增强

## 做了什么

- GitHub 适配器现在保留完整仓库元数据：

```json
"metadata": {
  "stars": 130979,
  "forks": 0,
  "language": "Rust",
  "topics": ["ai-tools", "claude-code", "rust", "skills", ...],
  "license": "MIT",
  "created_at": "...",
  "pushed_at": "...",
  "open_issues": 0,
  "archived": false,
  "default_branch": "main"
}
```

- 新增 `popularity_signals`，明确标注：

```json
"popularity_signals": {
  "stars": 130979,
  "forks": 0,
  "note": "stars/forks are popularity signals, NOT evidence"
}
```

## 真实 live 样例

通过 Watt host 代理真实返回：

- `farion1231/cc-switch`（stars 130979, Rust, 20 topics）
- `rustdesk/rustdesk`（stars 122547, Rust）
- `rust-lang/rust`（stars 117425, Rust）

## 验证

- `info_source_cli.py --proxy-mode host github --query "topic:rust" --limit 2`：✅ 成功
- `run_improve_validate.py --proxy-mode host`：✅ CYCLE PASS
- 真实数据：`tools/output/info_dump.json`（live, 3 条）
- `validate_contract.py` / `behavior_test.py`：✅ PASS

## 下一轮方向

- 用真实元数据增加“高质量仓库”过滤规则（如 license、pushed_at、archived、topics 多样性）。
- 探索 GitHub code search、issues、releases 适配器。
- 把 OSV/PyPI/npm/crates 接入 Watt 可加速域名或直连网络。
