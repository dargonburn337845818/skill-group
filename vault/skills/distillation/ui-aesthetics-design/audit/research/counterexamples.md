# 反例与失效边界整理（Counterexamples & Boundaries）

> 用途：为 UI 美学设计 Skill 补充“什么时候规则失效/被误用”。
> 每条包含：id / 边界 / 触发场景 / 绕过方式 / 真实或可复现案例 / 关联规则 / 来源。
> 说明：这些反例将进入最终 `../../CONSENSUS.md` 与 `../../examples/`，不是只写正例。

## 1. ce-dark-mode-contrast
- 边界：只在浅色模式验证配色，暗色模式对比度失效。
- 触发场景：设计系统/页面只测了 light 主题，或使用固定文本色 `text-foreground` 在暗背景上仍是深色。
- 绕过方式：用语义 token（`--fg` / `--bg`）而非硬编码色值；在 light 与 dark 两套下都检查 WCAG 对比度；暗色下不要用纯黑/纯白。
- 可复现案例：Apple 官方要求“If your app supports Dark Mode, be sure to check the minimum contrast in both light and dark modes”（`developer.apple.com/help/.../sufficient-contrast-evaluation-criteria`）。
- 关联规则：ui-contrast-text / ui-contrast-nontext。

## 2. ce-data-dense-over-whitespace
- 边界：把“少即是多/大留白”套到数据密集界面，牺牲信息密度与扫描效率。
- 触发场景：仪表盘、数据表、监控台、日历；为“呼吸感”把行高/间距放大，导致一屏信息骤减、表格难扫。
- 绕过方式：数据界面用紧凑间距、清晰网格线、等宽数字、可读小号字；留白只用于组间分隔，不侵蚀行内密度。
- 可复现案例：把一个 10 行数据表按 Editorial 的 `py-16/gap-8` 排版后，屏幕只能看到 2–3 行——属于可复现的密度反效果。
- 关联规则：ui-minimalism-delete / ui-whitespace-emphasis / ui-spacing-grid。

## 3. ce-brand-style-overgeneralized
- 边界：把品牌/单风格规则（全局零圆角、无阴影、单色）误当成通用 UI 标准。
- 触发场景：直接照搬 orca-link“全局直角契约”或 Editorial“禁止圆角/阴影”到通用产品；把风格 token 当设计法。
- 绕过方式：把这类规则限定在“所选主题/品牌”层；通用规则层只保留对比度、层级、间距、可发现性等底线；用多源规范交叉校验。
- 可复现案例：在医疗/金融表单上强制零圆角无阴影后，按钮可点击感明显下降（可复现：同一界面切换两种主题对比）。
- 关联规则：node_style_editorial_sharp / node_style_tech_dark_rounded（风格分支，非通用）。

## 4. ce-a11y-style-compromise
- 边界：为了“好看/精致”把正文缩小、变淡、用极细字重，牺牲可读性。
- 触发场景：把正文设成 12px/`opacity:.4`、极细 `font-weight:200`，或用低对比灰字做必要信息。
- 绕过方式：核心正文 ≥14px 且对比 ≥4.5:1；弱化只用于辅助/非必要文本；细字体只用于大标题，不用作正文。
- 可复现案例：把登录表单标签与错误提示做成 `text-xs text-[#1C1C1C]/40`，在低视力/昏暗环境下无法辨认（可复现）。
- 关联规则：ui-type-body-scale / ui-contrast-text / ui-not-color-alone。

## 5. ce-over-consistency-stiff
- 边界：把“一致性”绝对化，导致不同语境被强塞同一模板而呆板、失去语义。
- 触发场景：把营销首页、数据后台、错误空态、长文档全部用同一组件样式，不区分场景。
- 绕过方式：一致性锁“交互模式与命名”，允许按语境调整版式/密度/语气；关键仍是同一行为同一外观。
- 可复现案例：同一卡片组件既用于 CTA 营销位又用于周报表格摘要，结果两者都显得不伦不类（可复现）。
- 关联规则：ui-consistency。

## 6. ce-excessive-decoration-motion
- 边界：为“酷炫”堆渐变、发光、动效，干扰阅读/任务完成。
- 触发场景：把 tech-dark 的渐变/发光/动画原样用于文献阅读、数据表、表单；大量 hover 动画。
- 绕过方式：动效只用于状态反馈/层级变化；提供 `prefers-reduced-motion` 降级；装饰只放非内容区。
- 可复现案例：长文页面每段卡片带浮入动画，用户滚动时被动画打断阅读（可复现）。
- 关联规则：node_style_tech_dark_rounded / ui-minimalism-delete。

## 7. ce-single-cta-absolute
- 边界：把“一个屏幕一个主 CTA”误用于多同等重要动作的表单/工具栏。
- 触发场景：表单有“保存/取消”、工具栏有“编辑/删除/导出”、筛选器有“应用/重置”，硬把其中一个放大。
- 绕过方式：若动作同等重要，就同等视觉权重或用分组/位置区分；只在“任务主线”明确时突出一个主 CTA。
- 可复现案例：设置页把“保存”和“取消”设计成主次悬殊，用户误以为取消是次要操作（可复现）。
- 关联规则：ui-cta-hierarchy。

## 8. ce-color-only-state
- 边界：状态/差异只靠颜色，色盲或色弱用户无法区分。
- 触发场景：表单错误只变红、成功只变绿、图表分类只靠色相、选中态只换颜色。
- 绕过方式：加图标+文字、形状/描边、图案、位置；错误/成功都配文字提示；链接保留下划线等非颜色线索。
- 可复现案例：把“通过/失败”只做红绿点，灰度下两者几乎不可区分（可复现）。
- 关联规则：ui-not-color-alone。

## 9. ce-single-source-style-library
- 边界：把某个风格库/单场设计（StyleKit、Editorial、皮肤）当权威依据。
- 触发场景：看到 StyleKit 评分/风格页就引用“这风格正确”，或把本地素材当唯一标准。
- 绕过方式：本地/第三方风格只作参考；核心规则需 ≥2 个独立来源；风格评分不作为证据。
- 可复现案例：声称“Editorial 单色无圆角是美的基本原则”，但无第二来源支持，且与其他设计系统冲突（可复现为来源审计失败）。
- 关联规则：local-supplementary / node_style_*。

## 10. ce-measure-rule-overapplied
- 边界：把“正文行宽 45–75 字符”套到代码、表格、短标签、非拉丁长文。
- 触发场景：给所有文本容器设 `max-width: 65ch`，把代码/表格/短按钮也压缩。
- 绕过方式：只对长段落散文启用 measure；代码/表格/标签用自身布局；中日文按语言调宽。
- 可复现案例：代码块被 `max-width:65ch` 截断换行，阅读体验下降（可复现）。
- 关联规则：ui-type-measure（style 降权）。

## 11. ce-minimalism-destroy-discoverability
- 边界：过度极简/扁平导致可点击元素不可识别、必要分隔丢失。
- 触发场景：删除所有边框/底色/阴影，又不用留白区分可点区域；把按钮做成纯文字。
- 绕过方式：保留至少一种可点击线索（颜色/边界/背景/hover/focus）；关键分隔用空间或极轻背景。
- 可复现案例：无边框纯文字“按钮”与普通文本并排，用户找不到可点入口（可复现）。
- 关联规则：ui-minimalism-warning / ui-clickable-affordance。

## 小结

- 反例/边界数量：**11 条**（≥5 达标）。
- 每条均有：边界 / 触发场景 / 绕过方式 / 真实或可复现案例 / 关联规则。
- 覆盖范围：暗色模式、数据密集、品牌强风格、无障碍折衷、过度一致、过度装饰/动效、单一 CTA 误用、颜色唯一、单源风格库、行宽误用、极简破坏可发现性。
- 这些条目将在最终 `../../CONSENSUS.md` 的“反例与边界”章节与 `../../examples/` 中引用。
