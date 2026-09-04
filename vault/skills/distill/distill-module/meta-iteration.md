# 元能力迭代：复用 core-iteration，不另起炉灶

> 本文是 `distill-module` 的“元能力迭代”配套文档。
> 原则：**core-iteration 是唯一的迭代引擎；distill-module 只做 GapRequest 翻译、任务分派与回填**。

## 1. 分工边界

| 层 | 负责 | 不负责 |
|---|---|---|
| `core-iteration`（`core-iteration` / `value-meta-scheduler`） | 搜索→过滤→蒸馏→迭代→校验→调度→审计→根因的算法与轮次控制 | 理解“某个模块缺哪个子技能”、写 modules.json 回填 |
| `distill-module` | 模块缺口识别、GapRequest 归一化、决定 skill/expert、调用 core-iteration、回填注册表、更新 assignment | 重新实现六阶段、发明新契约、伪造评测 |

## 2. 把一条蒸馏任务翻译成 core-iteration 输入

### 普通模块 Gap → Skill

```json
{
  "topic": "dev.gaps: 信息安全",
  "target_skills": ["dev-security"],
  "core": false,
  "max_rounds": 1,
  "initial_draft": null,
  "info_scope": ["web", "github", "package_registry", "osv", "academic"],
  "info_depth": "balanced",
  "min_independent_sources": 2,
  "state_path": "vault/skills/dev/dev-security/round_ledger.json",
  "acceptance": ["SKILL.md + manifest 可入库", "每条规则有 source_refs 与三件套", "validate-vault OK"]
}
```

### 专家 Gap → ready 专家团

```json
{
  "topic": "前端领域专家蒸馏：dan-abramov",
  "target_skills": [],
  "target_expert": "dan-abramov",
  "core": false,
  "max_rounds": 1,
  "info_scope": ["web", "github", "academic"],
  "info_depth": "deep",
  "source_refs_hint": ["https://overreacted.io/", "https://github.com/gaearon", "https://react.dev/"],
  "acceptance": ["style 可执行且为风格推断", "sourceRefs 可回溯", "EXPERT_LIBRARY status -> ready"]
}
```

## 3. 阶段映射（distill 只调用，不实现）

| core-iteration 阶段 | 对应 skill / 工具 | distill-module 要做的 |
|---|---|---|
| 信息搜集 | `web-research-consensus` / `search-source` / `info-source-adapter` | 传入 `gap_id` 与 `source_hint`，收集 `raw_corpus` |
| 收益过滤 | `benefit-filter` / `tools/benefit_filter_live.py` | 接收 `yield_stats`，决定是否继续（verified_high < 3 → 早停） |
| 蒸馏 | `distillation-consensus` / `tools/distill_live.py` / `tools/distill_skill_package.py` | 接收 Node 列表，组装 SKILL.md + manifest |
| 迭代 | `value-iterator` / `tools/iterator_live.py` | 接收 changelog / effective_new_count，判断是否接受 |
| 校验 | `value-validator` / `tools/validator_live.py` / `skill-verification-consensus` | 接收 STOP/CONTINUE 与校验报告 |
| 调度 | `value-meta-scheduler` / `tools/meta_report.py` / `tools/scorecard.py` | 接收收敛报告；写回 round_ledger |
| 效果审计 | `value-effect-audit` / `tools/skill_effect_bench.py` | 接入真实任务包，回填 effect_ref |
| 根因 | `return-forensics` / `tools/forensics_live.py` | 边际收益下降时调用，不自己猜 |

## 4. 推荐调用序列（编排视角）

```text
1. 加载 core-iteration 正文（skill 工具或读 README/SKILL.md）
2. 生成/校准 GapRequest
3. 调用 search-source 或 info-source-adapter 采集 raw_corpus
4. 调用 benefit-filter（不可跳过）
5. 调用 distillation-consensus 生成 Nodes
6. 调用 value-iterator + value-validator + value-meta-scheduler
7. 调用 skill-verification-consensus（发布门槛）
8. 需要时长/效果数据时：
   a. python3 tools/scaffold_eval_task.py ...     # 建任务包
   b. 接入 skilljack-evals/BenchFlow 或手跑 3+3 对照
   c. python3 tools/skill_effect_bench.py --input <results.json>
9. 回填本模块注册表（modules.json / EXPERT_LIBRARY / domain-profiles）
```

## 5. 可直接调用的工具路径（不复制）

```bash
# 核心工作区
CORE=$WORKSPACE/skills/core-iteration

# 契约/行为/包检查/评分
python3 $CORE/tools/validate_contract.py $CORE
python3 $CORE/tools/behavior_test.py
python3 $CORE/tools/scorecard.py $CORE
python3 $CORE/tools/skill_package_check.py <skill-dir>

# 蒸馏链路
python3 $CORE/tools/run_improve_validate.py --proxy-mode host
python3 $CORE/tools/meta_report.py --input $CORE/tools/output/info_dump.json --round <n>
python3 $CORE/tools/skill_draft_builder.py --input $CORE/tools/output/info_dump.json
python3 $CORE/tools/distill_skill_package.py --nodes nodes.json --id <id> --description "..."
python3 $CORE/tools/scaffold_eval_task.py --task-id <id> --skill-name <skill> --prompt "..." --checks "contains:..." 
python3 $CORE/tools/skill_effect_bench.py --input <results.json>
```

> `distill-module` 目录内**不创建** `benefit_filter_live.py`、`distill_live.py`、`validator_live.py` 等副本；遇到同名需求一律走上面的路径。

## 6. 专家蒸馏（domain-profiles.pending_distill → ready）

专家蒸馏与普通 skill 蒸馏共用 core-iteration，只是目标与回填不同：

1. **入口**：`scripts/domain_recognize.py` 返回 `candidate_experts`（`status=pending_distill`）。
2. **目标**：产出“该专家的可调用风格/方法论条目”，而不是一个完整子技能。
3. **语料纪律**：只使用公开资料（官方文档、访谈、讲座、代码仓库、著作）；`sourceRefs` 必须真实可回溯。
4. **蒸馏输出**：
   ```json
   {
     "expert_id": "dan-abramov",
     "style_items": [
       {
         "trigger": "用户在做 React 状态设计/可调试性讨论时",
         "action": "从心智模型与数据流原理讲，不先堆 API 细节",
         "boundary": "不适用于需要最快代码落地的场景；这是风格参考，不是本人原话",
         "source_refs": ["https://overreacted.io/", "https://react.dev/"]
       }
     ],
     "evidence": "verified-high | verified-single",
     "trace_chain": ["raw -> filter -> distill -> style_item"]
   }
   ```
5. **回填**：
   - `EXPERT_LIBRARY.json`：`status: "pending_distill" -> "ready"`，`style` 用蒸馏出的可执行描述，保留/补强 `sourceRefs`；
   - `domain-profiles.json`：若该领域所有 `expert_ids` 均 ready，`status -> "ready"`；
   - 若 `verified_high < 3`：保持 `pending_distill`，输出 `insufficient_corpus`。

## 7. 递归与轮次纪律

- 普通模块 Gap 默认 `core=false, max_rounds=1`；用户明确说“继续”才进入下一轮。
- 只有 core-iteration 自身训练才 `core=true`；distill 模块不替用户自动扩大轮次。
- 递归深度上限 5、STOP 即收尾、收益曲线必须可见——这些规则继承 core-iteration，不在本模块重复实现。

## 8. 反模式

| 反模式 | 正确做法 |
|---|---|
| 在 distill-module 新建 `my-filter.py` | 调用 core-iteration 的 `benefit_filter_live.py` |
| 自己定义 `raw_corpus2` 字段 | 沿用 core-iteration 契约字段 |
| 跳过 value-validator 直接回填 | 先跑校验，`overall=pass` 再回填 |
| 把“使用大模型直接答”当成专家蒸馏 | 那是 `use_llm_directly` 分支，不写入 EXPERT_LIBRARY |
| 样本 1 次就说有效 | 至少 3 次，或标 `single-effect` |
