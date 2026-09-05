# 训练模式固化状态（Resume Guide）

> 本文件作用是：**随时停止，新会话可无缝继续**。
> 真正持久化的东西：所有 skill、工具、报告、评分器都在本目录与 vault/ 中；本文件只是“怎么续”的入口。

## 当前训练状态

- **训练轮次**：Round 40（内容蒸馏补强，已收敛）
- **状态**：已收敛（50/50 注册技能完成内容补强）
- **收敛状态**：CONVERGED（stop_reason=`all_registered_skills_content_enhanced`）
- **本轮内容**：存量技能库门禁翻新——vault 50 个注册 skill 与本地 20 个已注册 skill 全部通过 `skill_package_check` 100 分；`validate-vault` OK（22 skills）、`validate-tags` OK（50 manifests）、core-iteration `smoke_test` PASS。
- **直观能力分**：95 / 100（质量翻新后）
- **当前指标**：
  - vault 注册技能：50 个，包检 100/100
  - 本地已注册技能：20 个，包检 100/100
  - scorecard: 193/240（核心元能力 11 项，比 Round 30 +4）
  - 可执行工具：13 个
- **Skill 增强指数**：真实 A/B 仍以 dev-security 23.2% 为已落盘样例（`evals/`）。

## Round 32 内容蒸馏补强（第一批）

- 两批共 12 个技能：dev-security / dev-frontend / dev-testing / dev-performance / copywriting / paper-outline / dev-backend / dev-concurrency / dev-ai-engineering / dev-ops-sre / dev-remove-ai-flavor / academic-writing。
- 每技能追加 4–8 条可执行规则/反例/示例，新增约 145 条权威来源；SKILL/SOURCES 已更新，包检与 vault 校验全绿。
- 第三批（Round 33）另补 paper-reading / paper-writing / group-meeting / research-ppt / mentor-review / dev-art-ppt，详见 `reports/REPORT_ROUND33.md`。
- 当前累计：18 个技能完成内容补强，约 120 条新规则，约 212 条权威来源。

## Round 33 内容蒸馏补强（第三批）

- 6 个技能：paper-reading / paper-writing / group-meeting / research-ppt / mentor-review / dev-art-ppt。
- 每个技能搜索 10–12 条权威/一手来源并蒸馏 4–8 条新增规则；SKILL/SOURCES 已更新，全部包检 100 分。

## Round 34 内容蒸馏补强（第四批）

- 6 个技能：prompt-writing / document-report / speech-writing / career-path / teacher-math-consensus / submission。
- 累计 24 个技能完成内容补强，约 160 条规则，约 310 条权威来源；详见 `reports/REPORT_ROUND34.md`。

## Round 36 内容蒸馏补强（第六批）

- 6 个模块壳/协议技能：dev-design-aesthetics / expert-team / teacher-module / writing-module / dev-module / research-module。
- 累计 36 个技能完成内容补强，约 230 条规则，约 470 条权威来源；详见 `reports/REPORT_ROUND36.md`。

## Round 39–40：全量注册技能内容补强收敛

- 最后一批 10 个注册技能完成高质量搜索/蒸馏补强，至此 vault 正式注册技能 **50/50 全部包含内容补强章节**。
- 包检 50/50 100 分、本地 20/20 100 分、validate-vault/tags OK。
- 详见 `reports/REPORT_ROUND40.md`。

## Round 31 质量翻新内容

- 并行审计 3 组，产出逐 skill 修复建议。
- 批量补齐 `whenToUse` / `SOURCES` / `CHANGELOG` / `examples`。
- 修复内容级问题：dsh-optimization 脚本缺失、skill-management 失效引用、research-module 专家状态冲突、vlpc 来源可追溯、nvidia tags 超限、core-iteration 工具路径统一。
- 详见 `reports/REPORT_ROUND31.md`。

## 已固化的执行模式

### 执行模式：提升 → 验证 循环

```bash
cd $HOME/work/skills/core-iteration

# 1) 包检 / 校验
python3 tools/smoke_test.py
python3 tools/skill_package_check.py $HOME/work/dsh-skill-vault/vault/skills --recursive

# 2) 生成标准报告
python3 tools/meta_report.py --input tools/output/info_dump.json --round 31

# 3) 生成 Skill 草案/完整包
python3 tools/skill_draft_builder.py --input tools/output/info_dump.json
python3 tools/distill_skill_package.py --nodes tools/output/nodes_round22_list.json --id my-skill --description "..."
python3 tools/scaffold_eval_task.py --task-id my-task --skill-name my-skill --prompt "..."
python3 tools/scaffold_dev_spec.py --project /path/to/project --entry src/index.ts --test "npm test"

# 4) 量化 Skill 对模型增强（A/B 模板）
python3 tools/skill_effect_bench.py --input benchmarks/skill_benchmark_template.json
```

### 可选：灵感/市场侦察（按需，不膨胀）

```bash
python3 tools/mine_ideas.py --proxy-mode host --category all
```

## 新会话如何续训

1. 读取本文件。
2. 读取 `README.md` 的模块地图。
3. 读取 `reports/REPORT_ROUND30.md` 了解上一轮收敛，`reports/REPORT_ROUND31.md` 了解本轮质量翻新。
4. 读取 `round_ledger.json` 了解持久化状态（Round 31 library_hygiene_complete）。
5. 若要继续高价值迭代：
   - 优先给未验证 dev 子技能补真实 A/B：`scaffold_eval_task.py` → `skilljack_runner.py` → `benchflow_runner.py` → `skill_effect_bench.py`；
   - 或做插件侧集成（dsh-skill-router dev 路由）——必须按 `dsh-optimization-consensus` 隔离冒烟；
   - 若只是复核当前结果，不需要重跑。

## 停止/恢复

- 停止：直接结束会话即可；文件已落盘。
- 恢复：新会话按上面步骤继续，不需要重做。
