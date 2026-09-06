# 专家选择与添加（Expert Selection & Addition）

> 专家库是“领域 + 具体人名”的统一库。默认专家团 = 领域 profile 中 `expert_ids` 对应的全部 ready 专家；用户可自行选择子集，也可后续自行添加新专家。

## 1. 专家条目字段（必须）

| 字段 | 要求 |
|---|---|
| `id` | 唯一、小写/连字符，如 `tourist`、`um-nik` |
| `name` | 公开姓名/常用名，如 `Um_nik` |
| `displayName` | 侧边栏/对话展示名，如 `Um_nik（Alex Danilyuk，顶尖算法选手/博主）` |
| `role` | 一句话身份，如 `算法竞赛顶尖选手 / 读题与建模风格参考` |
| `persona_type` | **固定** `public-figure-style-reference` |
| `style` | 风格/方法论推断，不是本人原话 |
| `sourceRefs` | 非空数组，至少一条可靠公开来源 |
| `status` | `ready` / `pending_distill` |

可选字段：`domains[]`、`boundary`、`note`。

## 2. Ready 门槛

只有同时满足以下条件才允许 `status = "ready"`：

- 人物是真实公开人物。
- `persona_type = "public-figure-style-reference"`。
- `sourceRefs` 非空，且能定位到公开资料。
- `style` 是风格推断，已写明“非本人原话”。

`pending_distill` 的专家不会进入默认专家团；它们只出现在 `candidate_experts`，用于提示“待蒸馏”。

## 3. 默认选择

1. 领域识别输出 `domain.expert_ids`。
2. 从 `EXPERT_LIBRARY.json` 解析对应条目。
3. 过滤 `status = "ready"` 且 `persona_type` 正确且 `sourceRefs` 非空的专家。
4. 默认全部 ready 专家进入专家团；若数量过多（如 > 8），主持人可建议用户先选 3–5 人。
5. 用户可在对话中点名子集，如“只留 tourist 和 jiangly”。

## 4. 用户选择专家（接口）

当前阶段不要求 UI，提供两种方式：

- **自然语言点名**：用户说“用 tourist 和 um-nik 就行”，会话按 `id`/`name` 匹配专家库并构建子集。
- **运行时工具**：已实现 `teacher_discussion_start`（建会话时传 `expert_ids`）与 `teacher_expert_select(session_id, expert_ids)`；agent 按上述规则直接调用即可。

若用户点名了未 ready 的专家，应在普通回复里提示该专家仍是 `pending_distill`，并给出“先蒸馏该专家 / 换用其他 ready 专家”的默认选项；不要弹 DSH 对话框。

## 5. 用户添加专家（接口）

用户/蒸馏会话向 `vault/meta/EXPERT_LIBRARY.json` 的 `experts[]` 追加条目。建议模板：

```json
{
  "id": "new-expert-id",
  "name": "Public Name",
  "displayName": "Public Name（领域 / 身份）",
  "role": "领域身份 / 风格参考",
  "persona_type": "public-figure-style-reference",
  "domains": ["algorithm"],
  "style": "基于公开资料的风格/方法论推断，不是原话",
  "boundary": "风格推断，不伪造本人原话",
  "sourceRefs": [
    "https://example.com/profile",
    "/path/to/distilled/evidence.md"
  ],
  "status": "ready"
}
```

添加步骤：

1. 确认人物真实、来源可追溯。
2. 至少整理 1 条公开来源；优先访谈/题解/官方资料。
3. 写 `style` 时区分“原话引用”与“风格推断”；本库只存风格推断。
4. 加入 `domain-profiles.json` 对应领域的 `expert_ids`。
5. 运行 `python3 scripts/domain_recognize.py --validate-data` 校验；通过后再置 `ready`。

## 6. 专家缺口处理

若领域识别成功但 `experts` 为空/全部未 ready：

- 不静默降级，不伪造人名专家。
- 默认按 `use_llm_directly` 继续，并把专家缺口记进项目台账；不弹 DSH 对话框。
- 若用户明确要求，再进入 `distill_expert` 蒸馏任务。

## 7. 边界

- 不把“算法导师”“前端专家”等抽象角色写进专家库。
- 不把个人观点伪装成公开人物原话。
- 每个 ready 专家的 `sourceRefs` 必须随讨论结论一起保留。
