---
name: dev-workflow-consensus
description: 开发工作流共识——深模块优先、规格先行、对抗审查、证据化验证与分批执行的强流程；用于编码/重构/插件开发/模块设计时把“先对齐→规格→执行→验证”落到可检查步骤。
whenToUse: 开始写代码/重构/开发插件或新模块、需要制定开发计划、需要验证“是否真的完成”、或需要给开发过程加验收门禁时。
---

# 开发工作流共识（Dev Workflow Consensus）

> 定位：与 dsh-skill-router 内置开发规范互补的“可执行检查版”。
> 目标：先冻结接口与验收，再小步实现，最后用证据证明完成。
> 本流程与 `expert-decision-consensus` 九段环同源；需要项目台账/门禁/记忆时，可加载 `workbench-module` 并用 `wb` CLI 落盘。

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
python3 "\$CORE_ITERATION_ROOT/tools/scaffold_dev_spec.py" --project /path/to/project --entry src/index.ts \
  --module "core: 核心逻辑" --module "api: 对外接口" --test "npm test"

# 发布前用检验底座做最终检查
python3 "\$CORE_ITERATION_ROOT/tools/skill_package_check.py" <skill-or-project-dir>
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

## 2026 深度补强（Round 37）

> 本轮把“规格、接口、审查、门禁、证据”从口头纪律升级为仓库内可勾选、可机器执行、可被独立复核的产物。来源见 `SOURCES.md` Round 37 新增来源。

### R37-1 规格是仓库产物，不是聊天记录

- **规则**：规格必须落成仓库文件（如 `specs/<feature>/`），包含需求、验收标准、实现方式、任务拆解；以文件形式接受 code review，允许 diff/回溯。没有规格文件，不进入实现。
- **检查清单**：规格文件已提交且路径明确；验收标准可被第三方读取；任务拆解到“可拥有文件的原子块”；实现 PR 与规格 diff 可对照。
- **反例**：只在对话里说“我按刚才讨论的做”；等上下文一丢，规格与实现分叉，且无法证明哪个是意图。

### R37-2 跨模块边界用契约测试，不是单侧 mock

- **规则**：两个模块/服务/插件之间的公开接口，除了单元测试还应定义契约（payload、状态码、错误结构、调用顺序）；生产者做 provider verification，消费者用真实契约做 consumer test，双方各自独立跑，不共享实现细节。
- **检查清单**：接口边界有契约文件或 Pact/OpenAPI 代表；生产者与消费者各有测试；破坏性变更带版本迁移/契约重新生成；不把“两边都过了单测”当作边界已锁。
- **反例**：两侧各写一套手工 mock；单测全绿，集成/发布时才暴露字段名或错误格式漂移。

### R37-3 测试按“能测全的最低层”摆金字塔

- **规则**：每个公开接口至少在一个“能完整覆盖该行为的最低层”测试；不要在每个层级重复同一断言。PR 门禁放快速测试（unit/integration/contract），慢速 e2e/性能作为发布证据单独列出。
- **检查清单**：验收标准标明了测试层级（unit/integration/e2e）；合并门禁套件有预算（如 <10 分钟）；慢测试不在每次 PR 阻塞，但发布前必须跑且有证据。
- **反例**：全量 e2e 或全量 mock；门禁套件 30 分钟没跑完，或“100% 单元测试”只测了 mock 自己。

### R37-4 代码审查要有明确可判定的通过结论

- **规则**：审查者按 Google Engineering Practices 做小变更审查（建议单一 CL 小到可读，通常远小于 400 行）：先看正确性/设计/可维护性，再给 blocking / non-blocking 评论；作者先自审；审查者不代改代码。审查结果必须是 `APPROVE` / `CHANGES REQUESTED`（或“通过但含 nit”），不能是“大概行”。
- **检查清单**：CL 体量小或已拆分；作者自审记录存在；每条 BLOCKER 映射到修复或显式延期；门禁只认明确结论。
- **反例**：评论“整体没问题，有几个建议”却未分类，门禁无法判定；或审查者直接改写代码，破坏作者所有权和复核闭环。

### R37-5 一验收标准 = 一条证据 = 一个检查（DoD 机器化）

- **规则**：每个验收标准都要写成可观测断言（命令输出、文件、指标、界面元素），并对应一个具名测试/检查/证据记录。DoD 是全组共享的清单，不是每任务临时拍脑袋。
- **检查清单**：DoD 清单在仓库可见；每条 accept 有 test/evidence id；任何延期项显式记录；测试通过不等于“验证过”——关键检查仍须 `checks_observed_red`。
- **反例**：“我觉得可以了”“上线再看”；或 DoD 写“代码已审查”，但没有任何审查结论/记录可查。

### R37-6 关键门禁上分支保护，不能靠自觉

- **规则**：把最关键的检查（lint/unit/contract/smoke）配成 GitHub required status checks；敏感目录配 CODEOWNERS；关键分支禁止 force push/自合。管理员绕过必须可审计；有 in-flight CI 时禁止合并。
- **检查清单**：门禁不是“可选检查”而是 required；敏感模块有 owner；绕过有日志；合并前确认 CI 已终态（非 running）。
- **反例**：“我们都会跑测试”，但 PR 在 CI 还在跑时合并，或勾了 skip-checks。

### R37-7 旧代码/无规格模块先写表征测试，再动刀

- **规则**：进入没有规格或历史包袱的代码时，先写表征测试（characterization tests）把“当前真实行为”（包括 bug）固定下来，再重构；若行为需要变更，必须同时改规格与测试，不偷偷改行为。
- **检查清单**：改动前每个关键行为有一条可失败的表征测试；行为变化有对应规格/验收变更；不删除旧表征测试，除非新测试覆盖同样契约。
- **反例**：没测试直接重构；重构后“测试没变化所以没问题”，实际上旧行为已被悄悄改变。

### R37-8 分层执行：共享真相写进文件，验证人 ≠ 作者

- **规则**：派生子代理前，把模块地图、接口、不变量、任务卡、命令写进仓库文件（AGENTS.md/spec/tasks）；子代理读文件而不是只读聊天；主线程负责集成并做独立验证；关键 claim 的验证者不能是写代码的同一个 agent。
- **检查清单**：共享真相在文件系统里可查；文件所有权无重叠；关键验证由主线程/独立视角跑；最终门禁看产物与证据，不看“agent 说完成”。
- **反例**：全部上下文塞在 prompt 里；长对话漂移；或同一个子代理“写完又自证通过”。

## 来源

- 本地 `work-consensus`：深模块、Deletion Test、接口即测试面、模块地图。
- [claude-workflow-kit](https://github.com/ncoevoet/claude-workflow-kit)：evidence-first、对抗规格审查、commit/spec gates、模型分层。
- [skilljack-evals](https://github.com/olaservo/skilljack-evals)：验证/评测的确定性门禁。
- [dsh-skill-router DEV_SPEC](https://github.com/yjh051108/dsh-routing-suite)：内置六阶段开发规范。
- 完整来源表见 `SOURCES.md`。
