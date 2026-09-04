# 元能力减法审计报告

> 按 work-consensus 执行：避免臃肿，减法与加法平衡。

## 删掉的模块/工具

| 删除项 | 类型 | Deletion Test 结论 |
|---|---|---|
| `tools/repo_quality.py` | 重复实现 | `benefit_filter_live.py` 已包含同等 quality 评分；删除后复杂度不散落，保留它反而多一个入口 |
| `tools/live_pipeline.py` | 传声筒包装 | 只是顺序调用 `run_improve_validate` + `skill_draft_builder`；删除后仍需两个命令，无逻辑损失 |
| `tools/market_scout.py` | 重复/特化 | 与 `mine_ideas.py` 是同一“GitHub 灵感挖掘”的第二个实现；已合并为 `--category plugin/skill` |

## 归档/结构整理

- 15 份 `REPORT_ROUND*.md` 从根目录移到 `reports/`。
- 新增 `reports/README.md` 作为历史报告索引。
- 根目录只保留当前模块地图、版本表、工具入口。

## 合并后的工具清单（13 个）

```text
info_source_cli.py      # 真实多源采集
mine_ideas.py           # 灵感/插件/skill 市场（--category all/plugin/skill）
run_improve_validate.py # 六阶段执行+验证编排
benefit_filter_live.py  # 真实收益过滤
distill_live.py         # 真实蒸馏
iterator_live.py        # 真实迭代器
validator_live.py       # 真实校验器
forensics_live.py       # 真实收益下降根因
skill_draft_builder.py  # 真实 Skill 草案
validate_contract.py    # 契约校验
behavior_test.py        # 行为测试
scorecard.py            # 能力评分
smoke_test.py           # 一键冒烟
```

## 验证

- `validate_contract.py`：PASS
- `behavior_test.py`：PASS
- `smoke_test.py`：PASS（146/180）
- workspace + vault 同步：OK
- 无残留引用：`repo_quality / live_pipeline / market_scout` 已从活动文档清除
