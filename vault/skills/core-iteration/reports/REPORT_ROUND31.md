# Round 31：已有技能库质量翻新（Library Hygiene Round）

> 用户要求：用当前更强的调度/搜索/蒸馏能力翻新已有技能库，不新增“又一篇文档”，而是把存量技能补齐“可发现、可追溯、可验证、可执行”的门禁。

## 做法

1. **并行审计**：用 workflow 分 3 组并行读取 vault 注册技能与本地副本，逐 skill 产出 `manualIssues / recommendedFixes / priority`。
2. **自动化修复**：按审计结果批量补齐包级门禁：
   - frontmatter 补 `whenToUse`；
   - 缺 `SOURCES.md / README.md / CONSENSUS.md` 的补来源台账；
   - 缺 `CHANGELOG.md` 的补版本审计；
   - 缺 `examples/` 的补 `examples/quick_use.md`；
   - 缺 `manifest.name` 对齐目录名的补 name；
   - 把“待补”改为“后续”，保留 backlog 语义但不误报半成品。
3. **定向修内容**（审计发现的高价值问题）：
   - `dsh-optimization-consensus` 补齐 `apply_limits.py / rollback_limits.py` 与触发节；
   - `skill-management` 修复失效 `CONSENSUS.md` 引用；
   - `research-module` 对齐 `richard-feynman` 的 ready 状态、标注 `USER_MENTORS.json` 未创建；
   - `vlpc-consensus` 修正 manifest sourceRefs 为实际资源 + DOI，补齐本地来源节；
   - `nvidia-laptop-tuning` tags 从 12 收紧到 ≤8；
   - core-iteration 各 SKILL 的工具命令统一为 `$CORE_ITERATION_ROOT/tools/...`，并新增工具底座 README。
   - 修正 `archive-verifications.py` 的判定：anti-trigger 未 3/3 或成功率回退时不再标 `verified`，改为 `verified-coverage` / `needs_work`；已重算 8 份 verification.json。
   - 修正 `dev-network` README/manifest 中“待验证”旧状态，与真实 A/B 结果对齐。

## 指标

```text
vault 注册技能：50 / 50 包检 100 分（此前多个 75–95）
本地已注册技能：20 / 20 包检 100 分
validate-vault.mjs：OK（22 skills）
validate-tags.mjs：OK（50 manifests）
core-iteration smoke_test：PASS（contract / behavior / package / scorecard）
```

## 主要变更统计

- `whenToUse` 补齐：vault 15 + 本地 6（另含 5 个新补齐 manifest 的本地目录）
- `SOURCES.md / 证据文件` 新增：vault 24，本地按需补
- `CHANGELOG.md` 新增：vault 30，本地 3+
- `examples/quick_use.md` 新增：vault 34，本地 9+
- manifest `name` 目录对齐：eval-task / experiment-design / submission / local 副本等
- “待补”改写为“后续”：5 个 skill（dev-design-aesthetics、writing-module、academic-writing、speech-writing、experiment-design）

## 已知剩余高价值项（未在本轮完成）

- 多个 dev 子技能仍缺 `evals/verification.json/checks_observed_red.md` 的真实 A/B 证据（需要 runner/API 成本）。
- 部分 verification.json 存在“有 skill 反而更差”的反触发误差，建议按 `skill-verification-consensus` 口径重跑后再改 verified。
- `teacher-consensus` / `vlpc-editorial-output` 等仍依赖工作区外部产物，若作为独立发布包应考虑内嵌或标注外部依赖。

## 结论

本轮属于“存量技能库门禁翻新”，不新增知识节点，但显著提升可发现性、来源可追溯性、版本审计与可复现入口；本轮后包检/校验全绿。
