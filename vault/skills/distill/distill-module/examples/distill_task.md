# 蒸馏任务样例：模块缺口 → 新 Skill / 专家 → 回填

> 本文是 `distill-module` 的参考样例。每个字段都可替换为真实任务。
> 样例只演示编排与回填，不替代真实搜索、过滤、蒸馏与校验。

## 样例 A：为 dev 模块蒸馏“信息安全”

### 1. 输入（GapRequest）

```json
{
  "module_id": "dev",
  "gap_id": "dev-security",
  "gap": "信息安全：配置/依赖/接口层面的可执行安全判断",
  "target_type": "skill",
  "skill_id": "dev-security",
  "existing_refs": ["github-repo-consensus", "search-source"],
  "acceptance": [
    "SKILL.md + manifest.json 可入库 vault/skills/dev/dev-security",
    "每条规则有 trigger/action/boundary/source_refs",
    "validate-vault OK"
  ],
  "priority": "p1",
  "source_hint": ["OSV", "GitHub Security Advisories", "OWASP", "npm/PyPI 安全公告"]
}
```

### 2. 执行流水线

| 阶段 | 动作 | 产物 |
|---|---|---|
| 采集 | 用 `search-source` / `info-source-adapter` 查 OSV、GitHub Security Advisories、官方文档 | `raw_corpus`（含 evidence_class） |
| 过滤 | `benefit-filter` 密度评分与交叉验证 | `verified_high`：≥2 独立来源；`known_good` 与 `known_bad` 分离 |
| 蒸馏 | `distillation-consensus` 生成 Node：触发（评审依赖时）→ 动作（锁版本+查 CVE+看修复 commit）→ 边界（内部私有依赖无公告时用单源降权） | `knowledge_nodes` |
| 迭代/校验 | `value-iterator` / `value-validator` / `skill-verification-consensus` | `new_skill` + `verification_report: pass` |
| A/B | `scaffold_eval_task.py` 建 `dev-security-enforce` + `dev-security-anti`；跑 3+3 | 任务包 + Skill Lift 报告 |
| 回填 | 写 `vault/skills/dev/dev-security/`；更新 `modules.json` | 新 skill 可被 vault 发现 |

### 3. 回填 diff（示例）

```jsonc
// vault/meta/modules.json -> modes[dev]
{
  "skills": ["github-repo-consensus", "ui-aesthetics-design", "dev-security"],
  "gaps": [
    // "信息安全"               -> 改为：
    "信息安全（已落实：dev-security / distill-module）"
  ]
}
```

## 样例 B：把 pending_distill 专家蒸馏成 ready

### 1. 输入

- 领域识别结果：
  ```json
  {
    "domain": { "id": "frontend", "status": "pending_distill" },
    "candidate_experts": [{ "id": "dan-abramov", "status": "pending_distill" }],
    "fallback": { "options": ["distill_expert", "use_llm_directly"] }
  }
  ```
- 用户选择：`distill_expert`。

### 2. 执行

| 阶段 | 动作 | 产物 |
|---|---|---|
| 定目标 | 目标 = 可执行的“React 风格/方法论参考”，不是完整子技能 | `expert_id: dan-abramov` |
| 采集 | 公开资料：`https://overreacted.io/`、`https://react.dev/`、`https://github.com/gaearon` | `raw_corpus` + `source_refs` |
| 过滤 | 只保留可支持风格推断的证据；无公开来源的语录一律不进 | `verified-high` style 条目 |
| 蒸馏 | 每条 style 写成：触发（做状态设计/讲原理时）/ 动作（先讲心智模型与数据流）/ 边界（快速落地产出时不要求深讲） | `style_items` |
| 校验 | `skill-verification-consensus` 检查来源回溯、persona_type、不编造原话 | `verification_report: pass` |
| 回填 | 更新 `EXPERT_LIBRARY.json` 与 `domain-profiles.json` | `status -> ready` |

### 3. 回填 diff（示例）

```jsonc
// vault/meta/EXPERT_LIBRARY.json -> experts[dan-abramov]
{
  "id": "dan-abramov",
  "status": "ready",
  "style": "做 React 状态设计时先讲心智模型与数据流；调试性优先；从原理讲清 API",
  "sourceRefs": [
    "https://overreacted.io/",
    "https://react.dev/",
    "https://github.com/gaearon"
  ],
  "note": "风格/方法论参考，不是本人原话"
}

// vault/meta/domain-profiles.json -> domains[frontend]
{
  "id": "frontend",
  "status": "ready",
  "note": "候选专家已蒸馏为 ready"
}
```

### 4. 早停分支

如果该专家可回溯的 `verified_high` 不足 3 条：

```json
{
  "ok": false,
  "reason": "insufficient_corpus",
  "missing": ["独立访谈原文", "演讲/文本方法论证据", "代码/官方文档旁证"],
  "next": ["继续搜索公开资料", "或用户选择 use_llm_directly"]
}
```

此时 **不得** 把 `pending_distill` 改成 `ready`。

## 样例 C：writing 模块 Gap 回填（文本接口视角）

- Gap：`writing.gaps -> "提示词模板"`。
- 执行仍走 采集→过滤→蒸馏→校验→A/B→回填，但蒸馏目标从“领域知识”变成“文本服务的可复用模板”。
- 回填到 `vault/skills/writing/writing-module/subskills/prompt-writing/`，并在 `modules.json -> writing.skills` 加 `prompt-writing`。
- 边界：模板必须调用方补齐素材；不编造事实、不抹平多专家分歧。

## 通用收尾检查表

- [ ] GapRequest 已归一化（module_id / gap_id / target_type）
- [ ] 所有阶段调用 core-iteration 现有实现，无重复工具
- [ ] benefit-filter 未被跳过
- [ ] 产物有 source_refs + trigger/action/boundary
- [ ] 校验报告 `overall=pass`（或如实 `needs_work`）
- [ ] A/B：任务包存在；本地 skilljack_runner/benchflow_runner 已跑出真实 Skill Lift；外部 runner未配置 key 时如实标注
- [ ] `modules.json` / `EXPERT_LIBRARY.json` / `domain-profiles.json` 已更新
- [ ] `node scripts/validate-vault.mjs` 输出 OK
- [ ] `内部任务分派（未随公开仓库发布） distill/assignment.json` 状态与日期已更新
