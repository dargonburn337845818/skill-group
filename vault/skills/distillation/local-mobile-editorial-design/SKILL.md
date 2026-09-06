---
name: local-mobile-editorial-design
description: 本地“简约大气”离线自学包/长阅读 HTML 设计规范——用纸色/墨色/珊瑚 token、衬线标题+无衬线正文、单列编辑流、可点击卡片与本地进度保存，生成可读、可复现、可离线使用的学习工作台。
whenToUse: 用户要“本地简约大气”、“StyleKit Mobile Editorial”、“tier1 pack”风格的长阅读/离线学习 HTML；或需要用一套已归档的编辑型设计语言做自学档案、论文工作台、算法训练包。
---

# 本地简约大气设计规范（StyleKit Mobile Editorial + F-Pattern）

> 来源：本工作区已归档的 `algorithm-coaching/tier1_pack_stylekit.html`；通用规则以 `ui-aesthetics-design` 为底线。
> 本规范是**风格分支**，不是普适美学标准；数据密集/后台/品牌 VI 场景不直接套用。

## 触发条件

- 用户说“本地有一套简约大气 / 用 StyleKit / 像 tier1 pack / 做成离线自学 HTML”。
- 需要做长阅读型：学习档案、论文工作台、算法训练包、课程讲义。
- 需要“小窗能用、可勾进度、本地保存、不要花”。

## 核心 Token（唯一色板）

| Token | 值 | 用途 |
|---|---|---|
| `--paper` | `#fffdf8` | 页面底色 |
| `--ink` | `#24211f` | 正文/主文字 |
| `--ink-65` | `rgba(36,33,31,.65)` | 次级文字 |
| `--ink-45` | `rgba(36,33,31,.45)` | 弱元信息 |
| `--coral` | `#e97b61` | 强调/进度/关键 CTA |
| `--coral-deep` | `#d9644e` | hover/更强调 |
| `--sage` | `#c5d8c1` | 已完成状态 |
| `--line` | `rgba(36,33,31,.16)` | 1px 结构线 |
| `--serif` | `Georgia, "Noto Serif SC", "Songti SC", serif` | 标题 |
| `--sans` | `"Helvetica Neue", Arial, "PingFang SC", "Microsoft YaHei", sans-serif` | 正文 |

## 动作

1. **定场景**：确认是长阅读/学习档案/离线自学包；若不是，不要套本风格。
2. **复制 token**：使用上文“核心 Token”中的变量，禁止散落裸色。
3. **搭骨架**：`.shell` → `.masthead` → `.hero-title` → `.hero-sub/.meta-row` → `.progress-stick` → `.toc`。
4. **分章节**：每章 `.editorial.reveal`，内含 `.kicker` + `h2` + `.lede`；任务用 `.problem` 卡片。
5. **加交互**：`.reveal` 滚动渐入 + `localStorage` 进度 + 重置/复制按钮。
6. **过验收**：跑“验收清单”；打开 375px、720px、1280px 检查；`prefers-reduced-motion` 下确认无动画残留。
7. **引用底座**：需要更复杂的组件/图表/状态时，回到 `ui-aesthetics-design` 通用规则扩展。

## 布局骨架

1. `.shell`：单列，`max-width: 720px`，居中，左右 18px 呼吸边。
2. `.masthead`：顶部 F-pattern 信息条（大写、字距 .22em、上下 1–2px 结构线）。
3. `.hero-title`：衬线特大标题；强调词用 `.coral`。
4. `.hero-sub` + `.meta-row`：15px 次级说明 + 大写 meta 行。
5. `.progress-stick`：吸顶进度；`bar` 4px 珊瑚填充；`mini-btn` 重置/复制。
6. `.toc`：胶囊链接导航，hover 珊瑚边框。
7. `.editorial`：每个章节一块，`border-top: 1px solid var(--line)`；`.kicker` 大写珊瑚小标；`h2` 衬线；`.lede` 次级导语。
8. `.panel`：核心内容块，上下 1px 线；`.panel-label.coral` 标签。
9. `.problem`：可点击任务卡；`border-radius: 12px`；完成后 `border-left: 4px solid var(--sage)` + 浅绿底。
10. `.hint`：提示卡，珊瑚左线 2px，浅粉底。
11. `.recap`：黑色收尾卡（`background: var(--ink)`），珊瑚 kicker + 衬线引用。
12. `.footer`：大写小字，两端分布。

## 交互与无障碍

- 勾选框显示 20px，但整条 `.problem` 可点击；热区 ≥ 整行。
- `.mini-btn` 最小高 32px；小窗 480px 下保持可点。
- 滚动渐入：`.reveal` 初始 opacity 0 / translateY(14px)，进入视口加 `.visible`；`transition .55s ease`。
- `prefers-reduced-motion: reduce`：关闭所有过渡/动画，`.reveal` 强制可见。
- 进度用 `localStorage` 持久化，key 带版本；提供重置与复制按钮。
- 正文 ≥15px、行高 1.75；小窗 480px 收紧但正文不低于 15px。
- 所有状态不能只靠颜色：完成卡片有边线/底色/文字变化。

## 验收清单

- [ ] 使用上述 token，没有散落裸色/多套蓝。
- [ ] 单列阅读流；未做桌面四栏硬塞。
- [ ] 标题衬线、正文无衬线；正文 ≥15px / 行高 ≥1.75。
- [ ] 结构线 ≤1px；无重阴影/霓虹/扫描/发光。
- [ ] 触控目标可点；焦点/复选框可键盘操作。
- [ ] 进度能本地保存、可重置、可复制。
- [ ] `prefers-reduced-motion` 下无动画残留。
- [ ] 375–800px 小窗检查通过。

## 边界 / 不要用

- **不适用**：数据密集仪表盘、后台表格、监控大屏、需要多色语义图的场景。
- **不适用**：用户要求科技暗色/未来感/游戏化炫光时，换 `ui-aesthetics-design` 的 `dark-mode`/`linear-style` 分支。
- **不适用**：品牌 VI/Logo 设计——本规范只约束内容型学习页。
- 启发规则不是权威：与 WCAG/NN/g 冲突时，以通用可访问性规则优先。

## 完整样式速查

可直接抄的 CSS token 与基础 class 见同目录 `references/STYLE_REFERENCE.md`。

## 来源

- 本地样例：`algorithm-coaching/tier1_pack_stylekit.html`
- 选型说明：`dsh-skill-vault/vault/skills/distillation/ui-aesthetics-design/examples/06-inspiration-selection.md`
- 通用底线：`dsh-skill-vault/vault/skills/distillation/ui-aesthetics-design/SKILL.md`
- 本地归档规范：`dsh-deep-whale-inspect/DSH-UI-DESIGN-SPEC.md`
