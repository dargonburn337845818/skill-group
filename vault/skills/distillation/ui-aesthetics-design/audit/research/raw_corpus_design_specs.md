# Raw Corpus：设计规范与系统扫描

> 本文件是「设计规范与系统扫描」小类的原始语料。
> 记录约定：`chunk_id` / `text`（原文要点或直接引用）/ `source`（可点击 URL）/ `claim`（可蒸馏主张）/ `evidence`（证据分级）。
> evidence 定义：`verified-high` = 官方一手（权威机构/原始信源，即使单篇也算一手）或 ≥2 个独立来源交叉一致；`verified-single` = 非一手单源（已核实存在，待更多旁证）；`pending` = 来源线索/未取到可复核原文。
> 提取时间：2026-09-04。官方 JS 渲染页用辅助可读页面交叉验证；未验证项标 `pending`。

## 来源范围报告（source_scope_report · 初步）

- 已查入口：W3C WCAG 2.2 Understanding Docs、GitHub Primer Design Foundations、Tailwind CSS docs、GOV.UK Design System、Material Design（m1/m2/m3 + pub.dev M3TypeScale）、Apple Developer Help、Nielsen Norman Group。
- 检索方式：web_search + curl 直接抓取公开页面；部分 JS 渲染页（m3.material.io、Apple HIG 主排版页）未取到静态正文，已用 Apple Help 页面与 pub.dev 辅助文档交叉补证。
- 失败/降级：GitHub raw 与 wayback 在沙箱被拒（000），因此 Material/Apple 的具体数值改由官方可访问页面与辅助文档交叉验证。
- 覆盖限制：本轮聚焦“视觉/排版/无障碍/间距”指标；动效、暗色模式等后续小类补。

## Raw Corpus Entry

### 1. WCAG 2.2 · 对比度（文本）
- chunk_id: `spec_wcag_contrast_1`
- text: “The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text ... have a contrast ratio of at least 3:1.” “18 point text or 14 point bold text is judged to be large enough to require a lower contrast ratio.” “14pt and 18pt are equivalent to approximately 18.5px and 24px.” “computed values should not be rounded (e.g., 4.499:1 would not meet the 4.5:1 threshold).”
- source: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum
- claim: 正文文本对比度需 ≥4.5:1；14pt 粗体（≈18.5px）或 18pt 常规（≈24px）可视为大文本并降至 ≥3:1；对比度计算不四舍五入。
- evidence: `verified-high`（官方一手）

### 2. WCAG 2.2 · 非文本对比度（控件/图形）
- chunk_id: `spec_wcag_nontext_1`
- text: “The visual presentation of the following have a contrast ratio of at least 3:1 against adjacent color(s): User Interface Components ... Graphical Objects ... except for inactive components ...”
- source: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast
- claim: 识别控件和状态的视觉信息（不含禁用/装饰）应至少 3:1 对比度；2.999:1 不达标。
- evidence: `verified-high`（官方一手）

### 3. WCAG 2.2 · 焦点可见
- chunk_id: `spec_wcag_focus_1`
- text: “Any keyboard operable user interface has a mode of operation where the keyboard focus indicator is visible.” “The focus indicator must not be time limited.”
- source: https://www.w3.org/WAI/WCAG22/Understanding/focus-visible
- claim: 键盘可操作界面必须有可见且不超时的焦点指示器。
- evidence: `verified-high`（官方一手）

### 4. WCAG 2.2 · 焦点外观（最小面积与对比）
- chunk_id: `spec_wcag_focus_appearance_2`
- text: “When the keyboard focus indicator is visible, an area of the focus indicator meets all the following: is at least as large as the area of a 2 CSS pixel thick perimeter of the unfocused component or sub-component, and has a contrast ratio of at least 3:1 between the same pixels in the focused and unfocused states.” “Indicators that are inset further within the component ... need to be thicker than 2 CSS pixels ... The 'inset' indicator ... would need to be at least 3px thick to pass.”
- source: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance-minimum
- claim: 焦点指示器最小面积约等于 2 CSS px 粗的外轮廓周长，并与未聚焦状态同位置像素保持 ≥3:1 对比；内嵌式焦点环需更粗（如 ≥3px）。
- evidence: `verified-high`（官方一手；Level AAA 标准，与 AA 焦点可见互补）

### 5. GitHub Primer · 颜色对比
- chunk_id: `spec_primer_contrast_1`
- text: “The contrast requirements are: 4.5:1 for normal text; 3:1 for large text (>24px); 3:1 for UI elements and graphics; No contrast requirement for decorative and disabled elements. ... Don't rely on color alone. Show state with more than color.”
- source: https://primer.github.io/design/foundations/color/accessibility/
- claim: 设计系统把 WCAG 要求落地为：正文 4.5:1、大文本/图形/UI 元素 3:1；状态不能只靠颜色表达。
- evidence: `verified-high`（官方一手 + 与 WCAG 一致）

### 6. GitHub Primer · 排版基础
- chunk_id: `spec_primer_typography_1`
- text: “Typography design tokens use rem units for a more accessible browser zoom experience. Additionally, line height values are unitless and vary per style, making them align to the 4px grid.”
- source: https://primer.github.io/design/foundations/typography/
- claim: 排版 token 应使用 rem 以支持浏览器缩放；行高建议用无单位值并尽量对齐 4px 网格。
- evidence: `verified-high`（官方一手）

### 7. Tailwind CSS · 默认字号/行高
- chunk_id: `spec_tailwind_type_1`
- text: “text-sm font-size: var(--text-sm); /* 0.875rem (14px) */ line-height: var(--text-sm--line-height); /* calc(1.25 / 0.875) */ text-base font-size: var(--text-base); /* 1rem (16px) */ line-height: var(--text-base--line-height); /* calc(1.5 / 1) */ text-lg font-size: var(--text-lg); /* 1.125rem (18px) */ line-height: var(--text-lg--line-height); /* calc(1.75 / 1.125) */ text-xl font-size: var(--text-xl); /* 1.25rem (20px) */”
- source: https://tailwindcss.com/docs/font-size
- claim: 常见 UI 正文基准：14px/20px、16px/24px、18px/28px、20px/28px；正文用 16px 时行高约 1.5。
- evidence: `verified-high`（官方一手）

### 8. GOV.UK Design System · 字号/行高
- chunk_id: `spec_govuk_type_1`
- text: “govuk-heading-s , govuk-body 19px 25px” “govuk-body-s 16px 20px” “govuk-heading-m , govuk-body-l 24px 30px” “16 govuk-body-s 16px 20px”
- source: https://design-system.service.gov.uk/styles/type-scale/
- claim: 政府级正文默认 19px/25px（约 1.32 行高），小字 16px/20px；标题层级从 24px 到 48px。
- evidence: `verified-high`（官方一手）

### 9. Material Design 3 · 类型体系（辅助可读文档）
- chunk_id: `spec_material_type_1`
- text: “Body Large — 16sp, weight 400, tracking 0.5. Main reading text.” “Body Medium — 14sp, weight 400, tracking 0.25. Default body text.” “Body Small — 12sp, weight 400, tracking 0.4.” “Title Large — 22sp, weight 400. App bar titles.” “Label Large — 14sp, weight 500, tracking 0.1. Button labels.” “Display Large — 57sp”.
- source: https://pub.dev/documentation/material_design/latest/material_design/M3TypeScale-class.html（参考 https://m3.material.io/styles/typography/type-scale-tokens）
- claim: MD3 类型体系用 15 个 token 表达层级，正文 14–16sp，按钮 label 14sp/500；正文与标题用字号+字重+字距联合区分。
- evidence: `verified-single`（官方参考页 + 辅助文档；m3.material.io 官方 JS 页未静态取到，待后续交叉验证）

### 10. Material Design · 基线网格与间距
- chunk_id: `spec_material_grid_1`
- text: “All components align to an 8dp square baseline grid for mobile, tablet, and desktop. Iconography in toolbars align to a 4dp square baseline grid. Type aligns to a 4dp baseline grid.” “Screen edge left and right margins: 16dp” “Vertical spacing ... Toolbar: 56dp ... Subtitle: 48dp ... List item: 72dp” “Space between content areas: 8dp”
- source: https://m1.material.io/layout/metrics-keylines.html
- claim: 组件排布以 8dp 网格对齐，字号/图标可细到 4dp；常用页面边距 16dp、内容块间距 8dp、列表项 72dp 等被作为尺寸阶梯。
- evidence: `verified-high`（官方一手，静态可读）

### 11. Apple Developer · 对比度评估
- chunk_id: `spec_apple_contrast_1`
- text: “Most modern accessibility guidelines recommend a minimum contrast ratio of '4.5 to 1 between foreground text and its background' based on a formula provided by the World Wide Web Consortium's (W3C's) Web Content Accessibility Guidelines.” “If your app supports Dark Mode, be sure to check the minimum contrast in both light and dark modes.”
- source: https://developer.apple.com/help/app-store-connect/manage-app-accessibility/sufficient-contrast-evaluation-criteria
- claim: Apple 官方采纳正文 4.5:1 对比度建议，并要求在浅色与深色模式都检查对比度。
- evidence: `verified-high`（官方一手 + 与 WCAG 一致）

### 12. Nielsen Norman Group · 视觉层级
- chunk_id: `spec_nng_hierarchy_1`
- text: “A clear visual hierarchy guides the eye to the most important elements on the page. It can be created through variations in color and contrast, scale, and grouping.” “Consider emphasizing the most important aspect of your design by giving it more space.” “The Squint Test: ... squint or apply a slight blur to the design to get an idea of the conveyed grid.”
- source: https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
- claim: 视觉层级通过色彩/对比、缩放、分组（邻近与共同区域）创建；最优先元素应获得更多空间；可用“眯眼测试”快速目测层级。
- evidence: `verified-high`（一手文章）

### 13. Nielsen Norman Group · 视觉设计五原则
- chunk_id: `spec_nng_principles_1`
- text: “The principles of scale, visual hierarchy, balance, contrast, and Gestalt increase usability when applied correctly.” “Proximity refers to the fact that items that are visually closer together are perceived as part of the same group.”
- source: https://www.nngroup.com/articles/principles-visual-design/
- claim: 视觉设计五大可复用原则：尺度、视觉层级、平衡、对比、格式塔；邻近性能帮助用户把控件与标签看成一组。
- evidence: `verified-high`（一手文章）

## 待补充来源（不计数）

- Apple HIG 主排版页 `https://developer.apple.com/design/human-interface-guidelines/typography`：JS 渲染，未取到静态正文；具体字号/行高数值留待后续小类补，本文件仅作线索。

## 小结（本小类可复核指标）

- 对比度：正文 ≥4.5:1（WCAG 1.4.3 / Primer / Apple）；大文本与非文本控件 ≥3:1（WCAG 1.4.11 / Primer）。
- 字号：正文 16px 为常见基准（Tailwind/GOV.UK/Material 14–16sp 范围；见 spec_tailwind_type_1 / spec_govuk_type_1 / spec_material_type_1）。
- 行高：16px 正文配 24px 行高（1.5）是常见默认；GOV.UK 正文 19px/25px（spec_tailwind_type_1 / spec_govuk_type_1）。
- 间距：8dp/4px 网格为通用基线；页面边距约 16dp、块间距 8dp（spec_material_grid_1 / spec_primer_typography_1）。
- 焦点：必须可见且不超时（WCAG 2.4.7）；面积约 2px 粗轮廓，且与未聚焦状态同位置像素保持 ≥3:1（WCAG 2.4.13，spec_wcag_focus_appearance_2）。
- 层级：色彩/对比/缩放/分组创建；NN/g 眯眼测试可复核（spec_nng_hierarchy_1 / spec_nng_principles_1）。
