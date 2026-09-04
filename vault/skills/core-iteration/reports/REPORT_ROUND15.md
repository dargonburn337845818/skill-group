# 核心迭代元能力 · Round 15：真实 Skill 草案 + 一键全链路

> 日期：2026-09-04 ｜ 状态：六阶段 + 最终 Skill 草案可一条命令生成

## 新增

### `tools/skill_draft_builder.py`

- 从真实/离线 distilled Nodes 生成：
  - `tools/output/SKILL_DRAFT.md`
  - `tools/output/skill_draft.json`
- 自动包含 frontmatter、触发条件、核心动作、Node 列表、来源与追溯。

### `tools/live_pipeline.py`

一键执行完整真实链路：

```text
信息采集 → 质量预筛 → 收益过滤 → 蒸馏 → 迭代器 → 校验器 → 契约/行为/冒烟 → Skill 草案
```

用法：

```bash
python3 tools/live_pipeline.py --proxy-mode host
```

## 验证

- `live_pipeline.py --offline`：✅ 生成 11 Nodes + SKILL_DRAFT
- `run_improve_validate.py --proxy-mode host`：✅ CYCLE PASS
- workspace + vault 同步：✅

## 产物

- `tools/skill_draft_builder.py`
- `tools/live_pipeline.py`
- `tools/output/SKILL_DRAFT.md`
- `tools/output/skill_draft.json`
- `REPORT_ROUND15.md`

## 下一步

让 `return-forensics` 在真实 yield data 上做根因分析。
