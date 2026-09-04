# 蒸馏模块如何为 dev / teacher / research / writing 补充内容

> 本文是 `distill-module` 的“内容补充”配套文档。
> 核心句式：**接收某模块的 GAP → 搜索/采集 → benefit-filter → 蒸馏 → 回填 modules.json 对应技能**。

## 1. 触发来源

| 来源 | 位置 | 例子 |
|---|---|---|
| 模块 `gaps` | `vault/meta/modules.json` | dev.gaps 的 `"信息安全"`、writing.gaps 的 `"提示词模板"` |
| 领域专家缺口 | `vault/meta/domain-profiles.json` | `frontend` 的 `status: "pending_distill"` |
| 用户直接点单 | 对话 | “给科研模块补一个组会研讨 subskill” |
| 路由/侧边栏 | `scripts/domain_recognize.py` | `decision="expert_gap"` + 用户选 `distill_expert` |

## 2. 完整输入 → 输出

```text
输入
  module_id + gap_id + gap 描述
  target_type = skill | expert
  已有 skill/专家清单（防重复）

输出
  1 个可入库的 Skill 包（SKILL.md + manifest.json + 可选 examples/）
  或 1 个 ready 人名专家（EXPERT_LIBRARY.json 条目）
  或 1 份“语料不足/无法回填”的诚实报告
  加 1 份回填 diff（modules.json / EXPERT_LIBRARY.json / domain-profiles.json）
```

## 3. 统一流水线（对每个 GAP 执行）

### 第 0 步 · 定目标与去重

1. 读 `modules.json` 对应模块的 `skills` 和 `gaps`；读 `EXPERT_LIBRARY.json` / `domain-profiles.json` 的专家状态。
2. 确认缺口是否已被现有 skill 覆盖：若已覆盖，只做“回填/链接”，不再重复蒸馏。
3. 明确本次产物：
   - 工作流 Skill（例如 `dev-security`）→ 落到 `vault/skills/<module>/<skill-id>/`；
   - 人名专家（例如 `dan-abramov`）→ 落到 `EXPERT_LIBRARY.json` + 对应领域 profile。

### 第 1 步 · 搜索/采集

- 调用隐藏底座 `search-source` 或 `core-iteration` 的 `web-research-consensus` / `info-source-adapter`。
- 产出 `raw_corpus` 与 `source_scope_report`；每条至少带 `url + title + publisher + evidence_rank`。
- 规则：
  - 上游一手优先：源码/commit/release/公告/论文原文/官方文档；
  - 独立来源不是“同源转载”；GitHub star / awesome 收录只当线索；
  - 专家蒸馏时只收集公开人物资料，不编造对话/语录。

### 第 2 步 · benefit-filter（硬闸门）

- 对 `raw_corpus` 做信息密度评分与多源交叉验证。
- 输出：
  - `verified_high`（≥2 独立来源或单源逻辑自洽并降权）；
  - `pending_verification`；
  - `discarded_low_density`；
  - `yield_stats`。
- **禁止跳过本步，禁止把未过滤语料直接送蒸馏。**

### 第 3 步 · 蒸馏

- 只用 `verified_high` / `verified-single` 进入 `distillation-consensus`。
- 每条原语输出 Node 三件套：`触发条件 → 动作 → 边界/反例`，并带 `source_refs` 与 `trace_chain`。
- 需要完整包时：
  ```bash
  python3 $WORKSPACE/skills/core-iteration/tools/distill_skill_package.py \
    --nodes nodes.json --id <skill-id> --description "..."
  ```
- 质量自检分 < 5/7 时不得交付。

### 第 4 步 · 迭代 + 校验

- `value-iterator`：比较新旧节点，只接受“有效新增”，强制 `CHANGELOG.md`。
- `value-validator`：四条硬规则（语义位移 / 缺口重合 / 编辑步长 / 边际收益）判定 STOP/CONTINUE。
- `skill-verification-consensus`：发布前输出校验报告（claims / checks_observed_red / evals / adversarial_review）；`overall != pass` 不得回填。

### 第 5 步 · 真实 A/B（推荐）

- 用 `scaffold_eval_task.py` 建 1+ 个任务包，1 个 anti-trigger；
- 跑无 skill/有 skill 对照，至少 3 次；接入 skilljack-evals/BenchFlow 后由 runner 汇总；
- `skill_effect_bench.py` 输出增强指数（Skill Lift）；本地 runner（skilljack_runner/benchflow_runner）未配置外部 key 时写明“外部 runner 未接入”，不用模板分数。

### 第 6 步 · 回填

回填是“发布动作”，不是“蒸馏动作”，必须发生在校验通过之后：

| 回填目标 | 改什么 |
|---|---|
| `vault/meta/modules.json` | 对应模块 `skills` 数组追加 skill id；对应 `gaps` 条目标记落实（保留可审计措辞） |
| `vault/skills/<模块>/<skill-id>/manifest.json` | `scenario` 必须为该模块场景；`version` 从 0.1.0 起 |
| Skill 目录 | `CHANGELOG.md` / `SOURCES.md` / `examples/` 同步 |
| `EXPERT_LIBRARY.json` | 专家 `status` 从 `pending_distill` 改为 `ready`，补强 `style` 与 `sourceRefs` |
| `domain-profiles.json` | 对应领域 `status` 改为 `ready`（若其 ready 专家已齐） |
| `内部任务分派（未随公开仓库发布） <module>/assignment.json` | 若该模块交付因此闭环，更新 `status` / `owner` / `updated_at` |
| `scripts/validate-vault.mjs` 结果 | 必须 `OK: ... skill(s) validated` |

## 4. 各模块的具体补充方式

### dev —— 开发技能 / 美学 / 安全清单

- 数据源：`modules.json -> dev.gaps`（前后端规范、信息安全、并发、性能、测试、美学、去 AI 味）。
- 产物位置：`vault/skills/dev/<skill-id>/`；若 dev-module 已建立，也可作为其 `subskills/` 引用。
- 回填：
  - `modules.json -> dev.skills` 加 `dev-security`、`dev-concurrency` 等；
  - `dev.gaps` 改为“已落实：<skill-id>（feed-other-modules）”或移除（保留历史可审计）。
- 注意事项：技术规则必须能回溯到源码/官方文档；“最佳实践”要区分风格与规范。

### teacher —— 人名专家团与提问协议

- 数据源：`domain-profiles.json` 中 `expert_ids` 对应 `EXPERT_LIBRARY.json` 的 `pending_distill`；以及 `teacher.gaps` 的“专家库/讨论协议/领域多专家”。
- 产物位置：
  - 专家：写回 `EXPERT_LIBRARY.json`，不改领域字典结构；
  - 协议/子技能：`vault/skills/teacher/teacher-module/`（若存在）或 `vault/skills/teaching/`。
- 回填：
  - 专家 `status -> ready`；领域 `status -> ready`；
  - `modules.json -> teacher.skills` 加 `teacher-consensus` 之外的 ready 专家 skill 或协议文档 id。
- 专家纪律：`persona_type=public-figure-style-reference`；只做风格/方法论推断；保留 `sourceRefs`；不编造原话。

### research —— 论文/组会/PPT/导师审查

- 数据源：`research.gaps`（论文阅读与脉络梳理、组会研讨、PPT、模拟导师团队审查、科研道路规划）。
- 产物位置：`vault/skills/research/research-module/subskills/<id>/`（与现有 research-module 结构一致）或独立 skill。
- 回填：
  - `modules.json -> research.skills` 加 `paper-reading`、`group-meeting` 等；
  - `research.gaps` 标记落实；
  - 若涉及专家，`EXPERT_LIBRARY.json` 同步。
- 注意事项：科研规则必须区分“原文事实”与“风格/方法论参考”；公式/数据回原文核对。

### writing —— 文本服务子技能

- 数据源：`writing.gaps`（提示词模板、文案写作、文档/报告生成、文本接口）。
- 产物位置：`vault/skills/writing/writing-module/subskills/`（与现有 writing-module 一致）。
- 回填：
  - `modules.json -> writing.skills` 加 `prompt-writing`、`copywriting`、`document-report` 等；
  - `writing.gaps` 标记落实。
- 注意事项：distill 只负责“把结论说得清楚”，不替代 writing 的文本服务职责；回填时保持 `TextRequest`/`TextResult` 接口可复用。

### distill 自身（元能力迭代）

- distill 不给自己造新的过滤/蒸馏算法；它只负责把上面四类的缺口持续调度进 core-iteration，并用 `real-ab-bench.md` 验证产出。

## 5. 禁止事项

1. 不在 `distill-module` 下重复实现 `benefit-filter`、`distillation-consensus`、`value-iterator`、`scaffold_eval_task.py` 等已存在工具。
2. 不为了“完成任务”把无来源摘要硬编成 Skill。
3. 不把 `pending_distill` 改成 `ready`，除非专家蒸馏通过校验且有足够独立来源。
4. 不把“尚未配置外部 runner key”写成“已跑外部 skilljack-evals”；本地真实 A/B 如实标注，外部 runner 未接入也如实说明。
5. 不绕过 `scripts/validate-vault.mjs` 直接宣称回填成功。

## 6. 简单用户话术

> 我先看你这个模块到底缺哪块能力，再把“缺口”转成一次蒸馏任务：先搜来源、过滤出可信高优内容、蒸馏成可执行判断，校验通过后回填到技能清单。最后给你三样东西：新技能在哪、回填了哪些注册表、以及还缺什么证据。
