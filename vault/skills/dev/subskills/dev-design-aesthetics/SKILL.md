---
name: dev-design-aesthetics
description: 设计美学/风格库子技能（已挂载）——核心内容由 ui-aesthetics-design 提供；本挂载点负责 dev 调用入口、风格分支缺口与验收追踪。
whenToUse: 用户需要设计美学/风格库、UI 视觉审查或风格分支决策时；先引已填充的 ui-aesthetics-design，再按缺口补风格库。
---

# dev-design-aesthetics · 设计美学/风格库（已挂载）

> 状态：已填充（挂载 `vault/skills/distillation/ui-aesthetics-design/`）。本挂载点不重复已蒸馏内容，只做 dev 调用与剩余缺口追踪。

## 触发条件

- 用户要求生成/审查网页组件、仪表盘、表单的视觉美感与可用性。
- 需要做配色、字体、间距、层级、控件、焦点态、动效检查。
- 需要判断某个界面属于哪种风格分支（现代/极简/数据密集/品牌强风格）。

## 核心动作

1. **引用**：直接调用已填充的 `ui-aesthetics-design`，按其“定场景 → 检查清单 → 收口”三步执行。
2. **补缺口**：只蒸馏现有 skill 未覆盖的风格库缺口（如特定产品风格、数据密集规范、暗色模式进阶）。
3. **验收**：用 `skill-verification-consensus` 检查新增规则是否有来源、有反例、是否被标为“风格分支”而非普适规则。

## 边界 / 反例

- 不重新蒸馏 `ui-aesthetics-design` 已覆盖的内容，避免重复与漂移。
- 不负责品牌 VI/Logo 设计；那是独立任务。
- 不把单一风格（零圆角/无阴影/单色等）当普适标准，必须标为风格分支并降权。
- 数据密集界面/品牌强风格需要叠加专项边界，不能直接套极简美学。

## 待补缺口（可继续蒸馏）

- 现有 skill 未覆盖的风格库：产品定制风格、暗色模式进阶、品牌风格分支
- 数据密集界面（表格/仪表盘/监控）的密度与清晰度细则
- 动效与减少动效偏好的落地检查
- 风格分支与普适规则的标记规范

## 验收标准

- 新增规则有 source_refs，触发/动作/边界三件套齐全。
- 至少 1 个反例或失效边界。
- 风格分支明确标注“这是风格选择，不是通用规则”。

## 来源

- 已填充：`vault/skills/distillation/ui-aesthetics-design/`（SKILL.md / CONSENSUS.md / SOURCES.md / examples/）
- 隐藏底座：`search-source` / `skill-verification-consensus` / `dev-workflow-consensus`
