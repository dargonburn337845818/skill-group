---
name: dev-workflow-consensus
description: 开发工作流共识——深模块优先、规格先行、对抗审查、证据化验证与分批执行的强流程；用于编码/重构/插件开发/模块设计时把“先对齐→规格→执行→验证”落到可检查步骤。
whenToUse: 开始写代码/重构/开发插件或新模块、需要制定开发计划、需要验证“是否真的完成”、或需要给开发过程加验收门禁时。
---

# 开发工作流共识（Dev Workflow Consensus）

> 定位：与 dsh-skill-router 内置开发规范互补的“可执行检查版”。
> 目标：先冻结接口与验收，再小步实现，最后用证据证明完成。

## 触发条件

- 用户要求“开发 / 编码 / 重构 / 修复 / 模块化 / 插件开发”。
- 需要把一个模糊想法变成可交付代码。
- 需要判断实现是否完成、验证是否可信、是否该交审。
- 需要给开发/重构设置门禁（spec gate、commit gate、redteam）。

## 核心流程（Frame → Interview → Plan → Spec → Review → Gate → Build → Verify → Ship）

1. **Frame（对齐）**：写北极星：为谁、什么处境、交付什么可观测结果、不做什么。
2. **Interview（拆歧义）**：用选择题逐一消解关键取舍；一次只问最高信息增益问题。
3. **Plan（模块地图）**：先画模块地图与公开接口；没有模块地图不写实现。
4. **Spec（规格化）**：L1/L2 规格必填：spec/accept/do/verify；缺一门不进入执行。
5. **Adversarial spec review（对抗审查）**：独立视角找 BLOCKER/GAP/NOTE，记录 six checks；不通过不 Gate。
6. **Gate（门禁）**：规格文件存在 + 对抗审查段落存在 + 无未决 BLOCKER，才放行。
7. **Build（执行）**：
   - 深模块优先：简单接口 + 丰富实现。
   - 接口是测试面：先用测试锁死公开接口。
   - 主线程做规划/集成/验证；复用型实现交给子代理，按模型分层（haiku 只读机械、sonnet 可编辑机械、opus 判断）。
   - 子代理：明确拥有的文件、不能碰的文件、不变量、要跑的命令；重叠文件集串行，不并行；子代理不碰 git 状态。
   - 同一文件连续改动过阈值（如第 3 次编辑）仍不收敛 → 换新 agent 接管问题，避免长循环。
8. **Verify（证据化验证）**：每个完成声明用证据分类（static/runtime/data/rendering/tooling）+ 可证伪检查；测试通过公开接口跑。
9. **Review（集成复查）**：审查范围 = 上次审查之后改过的全部内容，不是只看当前 diff；修复后必须重跑验证。
10. **Ship（终验）**：未通过终验不得宣告交付；发布前确认无 in-flight 验证、无未决 BLOCKER、证据可回溯。

## 硬性检查表

- [ ] 模块地图 + 公开接口已固定，接口通过测试锁死。
- [ ] 规格 L1/L2 有 spec/accept/do/verify；没有“先做着再看”。
- [ ] 对抗规格审查有 BLOCKER/GAP/NOTE（或 “none found” + 已跑六项检查）。
- [ ] 实现按深模块/接口/文件系统地图进行，不跨项目隐式依赖。
- [ ] 每个可机械判断的点用测试/脚本，不用“我觉得可以”。
- [ ] 每个自动检查见过变红（prove it can fail），否则只算“已运行”。
- [ ] 子代理数量有界、模型分层、重叠文件串行、不进 git 状态。
- [ ] 终验：测试通过 + 真实启动/冒烟 + 证据可回溯 + 无未处理边界。

## 输出契约（对接 core-iteration 检验/终验）

```text
{
  "spec": { "frame": {...}, "modules": [...], "accept": [...] },
  "verification": { "claims": [...], "checks_observed_red": [...], "evidence_class": "..." },
  "dod": { "tests_pass": true, "smoke_pass": true, "redteam": "pass|pending", "open_boundaries": [] }
}
```

- `checks_observed_red`：必须包含“见过失败”的关键检查；否则不得写“已验证”。
- 交给 `skill-verification-consensus` 作为发布前门禁。

## 干跑验证

- 用 `scaffold_dev_spec.py` 生成一个真实项目的规格单 + 路径手册，确认字段完整。
- 用 `skill_package_check.py` 检查生成的交付物，确认无 issue。
- 开发中每完成一块，给出对应证据类别，不要只写“已完成”。

## 可执行工具（开发底座落地）

```bash
# 生成开发规格单 + 路径手册（模块地图/公开接口/测试/约束）
python3 tools/scaffold_dev_spec.py --project /path/to/project --entry src/index.ts \
  --module "core: 核心逻辑" --module "api: 对外接口" --test "npm test"

# 发布前用检验底座做最终检查
python3 tools/skill_package_check.py <skill-or-project-dir>
```

- 规格单包含 Frame/Interview/Plan/Spec/Adversarial Review/Gate/Verify/DoD，可直接作为开发门禁。
- 路径手册与 dsh-skill-router 内置“路径手册模板”对齐。

## 边界

- 本共识是“开发强流程”，不替代领域知识；也不自动允许热更 DSH/插件。
- DSH/插件升级、热更、重启、子代理调度：必须先读 `dsh-optimization-consensus`，隔离冒烟后再落地。
- 简单一次性小脚本不必走全流程；但“会长期存在/被复用”的模块必须走接口与测试。
- 评审通过不是交付：还有终验和红队项。

## 简单用户话术

> 我会先和你把目标与边界对齐，画出模块地图和公开接口，把规格单给你确认；确认后我再小步实现，每完成一块就给出“哪种证据证明它完成了”。开发完不会直接说完成，我会做一次“故意破坏看检查会不会红”的验证，再交独立视角复查。

## 来源

- 本地 `work-consensus`：深模块、Deletion Test、接口即测试面、模块地图。
- [claude-workflow-kit](https://github.com/ncoevoet/claude-workflow-kit)：evidence-first、对抗规格审查、commit/spec gates、模型分层。
- [skilljack-evals](https://github.com/olaservo/skilljack-evals)：验证/评测的确定性门禁。
- [dsh-skill-router DEV_SPEC](https://github.com/yjh051108/dsh-routing-suite)：内置六阶段开发规范。
- 完整来源表见 `SOURCES.md`。
