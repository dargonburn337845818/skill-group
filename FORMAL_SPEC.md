# 技能路由正式版 · 蓝图（v2 Skeleton）

> 状态：骨架 v0.1
> 定位：把现有 alpha 技能库升级为“五模块 + 隐藏底座 + 过程监视器”的正式版。
> 本轮只做骨架、页面、任务分派；具体功能由多个新会话逐步实现。

## 1. 总览

正式版由**五个可组合模块**驱动，搜索 / 检验 / 开发规范作为**隐藏底座**常驻，不参与模式选择；路由/调度从“一开始不预注入”，在进程推进中按需调用技能与专家，并留下**可视化调用链**。

```text
隐藏底座（always-on, UI 不可见）
├── search-source            # 搜索
├── skill-verification-consensus  # 检验
└── dev-workflow-consensus   # 开发规范
        ▲
        │ 被五个模块按需调用
        ▼
┌────────────┬────────────┬────────────┬────────────┬────────────┐
│ dev        │ distill    │ teacher    │ research   │ writing    │
│ 开发       │ 蒸馏       │ 教师       │ 科研       │ 文稿       │
└────────────┴────────────┴────────────┴────────────┴────────────┘
```

## 2. 模块定义

| id | 中文 | 职责 | 现有 skill 填充 | assignment |
|---|---|---|---|---|
| `dev` | 开发 | 前后端、美术/PPT、编码规范、信息安全、并发/性能、测试调试、设计美学、去 AI 味 | `github-repo-consensus`, `ui-aesthetics-design` | `内部任务分派（未随公开仓库发布） dev` |
| `distill` | 蒸馏 | 继承核心迭代：元能力迭代 + 为其他模块补内容 | `core-iteration`, `distillation-consensus`, `web-research-consensus`, `value-meta-scheduler` | `内部任务分派（未随公开仓库发布） distill` |
| `teacher` | 教师 | 多领域专家视角：答疑、纠偏、规划方向、多 agent 讨论团队 | `teacher-consensus` | `内部任务分派（未随公开仓库发布） teacher` |
| `research` | 科研 | 多 agent 科研团队：读论文、理脉络、写论文、组会、PPT、模拟导师审查 | `vlpc-consensus` | `内部任务分派（未随公开仓库发布） research` |
| `writing` | 文稿 | 提示词、文案、各类文本生产；可被其他四模块复用 | `writing-module`（含 prompt/copy/document-report 子技能） | `内部任务分派（未随公开仓库发布） writing` |

## 3. 路由与进程模型（骨架契约）

### 3.1 原则

- 路由**不预注入五模块**，初始只保留隐藏底座。
- 进程由用户任务决定：任务被识别后进入某个模块，模块内的技能/专家随流程逐步加载。
- 人不需要知道内部开发进程细节，但要有**可视化调用链**。

### 3.2 进程事件（Trace Event）

```json
{
  "id": "evt_001",
  "session_id": "...",
  "ts": "2026-09-04T20:00:00Z",
  "mode": "teacher",
  "kind": "skill_loaded | expert_speak | tool_call | decision | stage",
  "actor": { "type": "skill" | "expert" | "agent" | "user", "id": "...", "name": "..." },
  "action": "读题 / 提出分支 A / 调用 scaffold_dev_spec",
  "reason": "任务需要...",
  "detail": { ... },
  "status": "running | done | rejected | adjudicated"
}
```

### 3.3 可视化契约

- 统一过程监视器（`conversation.view`）只做只读展示。
- 教师/科研模式显示“专家讨论流”：每轮每位专家发言、冲突点、裁决、采纳结论。
- 其他模式显示对应进程阶段：开发流水线、蒸馏收益曲线、文稿生成步骤。

## 4. 专家团（teacher / research）

### 4.1 统一专家库

`vault/meta/EXPERT_LIBRARY.json`

```json
{
  "experts": [
    {
      "id": "expert_algorithm",
      "name": "算法导师",
      "domain": "algorithm",
      "school": "...",
      "persona": "一句话人设",
      "style": "提问式 / 结构式 / 批判式",
      "strengths": ["...", "..."],
      "boundary": "不擅长...",
      "sourceRefs": ["..."]
    }
  ]
}
```

### 4.2 讨论协议（回合式 + 裁决）

1. 每轮：选定专家团 → 每位专家独立表态。
2. 汇总：冲突点表（claim_a / claim_b / source）。
3. 裁决：主持人（或用户）选择采纳/保留分支/驳回，并记录。
4. 输出：每条结论标注 `expert_id` 与 `expert_name`，让用户明确“是哪位专家在教导”。

### 4.3 添加/选择专家

- 本轮只定义 schema；`expert add/select` 工具与 UI 由实现会话完成。
- 专家库应支持用户自行添加，且可逐步成为“专家团触手可及”。

### 4.4 领域识别与专家缺口（正式版关键）

用户说的“专家”不是抽象角色，而是**指定某一领域开始会话时，该领域具体人名专家团**。五个模块共用这一识别能力。

#### 领域识别

- 数据：`vault/meta/domain-profiles.json`。
- 策略：关键词/领域字典自动识别 + 低置信度询问纠正。
- 输入：用户首条/后续自然语言（如“这道算法竞赛题”“我在做前端”“这篇物理论文”）。
- 输出：`domain_id` + `confidence` + 该领域 `experts` 列表。

#### 专家表示（人名专家）

```json
{
  "id": "tourist",
  "name": "Tourist",
  "displayName": "Tourist（顶尖算法选手）",
  "role": "算法竞赛顶尖选手 / 风格参考",
  "persona_type": "public-figure-style-reference",
  "style": "先暴力再优化、信息论式拆题、极端简洁实现",
  "sourceRefs": ["..."],
  "status": "ready"
}
```

- `persona_type = public-figure-style-reference`：只以公开人物为“风格/方法论”参考，不编造原话；模拟时说明是风格推断，并保留 sourceRefs。
- 未定义 `persona_type` 的专家不得进入专家团。

#### 专家缺口（无专家时）

- 若识别到领域但该领域 `experts` 为空/未 ready：
  - 对话内明确询问：**“该领域暂无已备好的人名专家：蒸馏专家团 / 放弃专家团直接用大模型？”**
  - 侧边栏同步显示“专家缺口”状态。
  - 不静默降级。
- 用户选择 `distill_expert` → 进入蒸馏任务；选择 `use_llm_directly` → 无专家团，直接用大模型解答。

#### 五个模块的领域专家

- `teacher` / `research`：最依赖人名专家团（讨论、审查、风格指导）。
- `dev`：开发领域也可挂领域专家（算法、前端、安全、性能等人物）。
- `distill` / `writing`：同样受领域识别影响，但专家团可按需精简。

## 5. Assignment（任务分派包）

### 5.1 位置与格式

```text
dsh-skill-vault/内部任务分派（未随公开仓库发布） 
├── assignment.schema.json
├── domain/assignment.json + assignment.md      # 共享：领域识别 + 人名专家库
├── ui/assignment.json + assignment.md          # 共享：插件 UI 美术精修
├── dev/assignment.json + assignment.md
├── distill/assignment.json + assignment.md
├── teacher/assignment.json + assignment.md
├── research/assignment.json + assignment.md
└── writing/assignment.json + assignment.md
```

### 5.2 每包字段

```json
{
  "id": "dev",
  "title": "开发模块实现",
  "mode": "dev",
  "status": "pending | in_progress | done",
  "owner": "",
  "priority": "p0 | p1 | p2",
  "dependencies": ["base"],
  "deliverables": ["..."],
  "acceptance": ["..."],
  "files_to_create": ["..."],
  "next_conversation_bootstrap": "本包请新会话读取...",
  "updated_at": "..."
}
```

## 6. UI 骨架（本轮）

### 6.1 设置页（dsh-skill-vault settings.section）

- 只显示五个正式模块分组。
- 每个分组可展开：显示模块描述与 skill 列表（当前为 mock/占位）。
- 搜索 / 检验 / 开发规范完全隐藏（不出现在 UI）。
- alpha 旧场景完全隐藏（文件保留，不回显）。

### 6.2 会话侧栏（dsh-skill-router conversation.view）

- 统一过程监视器（mock 数据）。
- 顶部：当前模式/进程。
- 中间：调用链。
- 教师/科研：专家讨论流。
- 风格沿用现有 UI（同字体、同边框、同配色）。

## 7. 新会话如何开工

1. 读取本文件与对应 `内部任务分派（未随公开仓库发布） <module>/assignment.md`。
2. 读取 `vault/meta/modules.json` 与 `EXPERT_LIBRARY.json`（若涉及）。
3. 按 assignment 的 `files_to_create` 在对应 `vault/skills/<mode>/` 下建骨架/内容。
4. 完成后更新 assignment.json 的 `status` 与 `owner`，并在 FORMAL_SPEC.md 勾选交付项。

## 8. 验证

- `npm run build:client`（两个插件）必须通过。
- `node scripts/validate-vault.mjs` 必须 OK。
- assignment JSON 必须通过 `assignment.schema.json` 校验。
- 不热更运行中的 agent；插件安装/升级按 `dsh-optimization-consensus` 隔离冒烟。
