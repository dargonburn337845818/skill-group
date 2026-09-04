# UI 美学设计 Skill · 终验报告与审计

> 生成时间：2026-09-04T21:29:54
> 说明：本文件位于 `audit/`，仅供审计；trace_back 采用“文件名 + 可搜索 id”。

## 1. 交付清单

- 源目录：`$WORKSPACE/skills/ui-aesthetics-design/`
- vault 目录：`$PROJECT_ROOT/vault/skills/distillation/ui-aesthetics-design/`
- 文件：SKILL.md / CONSENSUS.md / SOURCES.md / manifest.json / README.md / examples/（5 个样例）/ audit/
- 状态：已通过样例干跑、vault 校验；**本报告不自动宣称最终验收通过**，等待人工复核。

## 2. 规则引用链（每条规则 trace_back）

| 条目 | CONSENSUS 规则 | 主张摘要 | 证据 | 权重 | source_refs 数 | source_note | trace_chain |
|---|---|---|---|---|---|---|---|
| node_contrast_text | R1.1 | 正文文本与背景对比度至少 4.5:1；14pt 粗体（≈18.5px）或 18pt 常规（≈24px）可视为大文本并降至 3:1。 | verified-high | 1.0 | 3 |  | research/raw_corpus_design_specs.md#spec_wcag_contrast_1 -> research/yield_filter.md#ui-contrast-text -> node_contrast_text |
| node_contrast_nontext | R1.2 | 识别控件、图标、关键图形的非文本视觉信息与相邻颜色对比至少 3:1。 | verified-high | 1.0 | 2 |  | research/raw_corpus_design_specs.md#spec_wcag_nontext_1 -> research/yield_filter.md#ui-contrast-nontext -> node_contrast_nontext |
| node_focus_visible | R6.1 | 键盘可操作界面必须提供可见且不超时的焦点指示器。 | verified-high | 1.0 | 2 |  | research/raw_corpus_design_specs.md#spec_wcag_focus_1 -> research/yield_filter.md#ui-focus-visible -> node_focus_visible |
| node_focus_appearance | R6.2 | 焦点指示器面积至少约等于 2 CSS px 粗的外轮廓周长，并在聚焦/未聚焦同位置像素间保持 ≥3:1；内嵌焦点环需更粗（如 ≥3px）。 | verified-single | 0.5 | 1 |  | research/raw_corpus_design_specs.md#spec_wcag_focus_appearance_2 -> research/yield_filter.md#ui-focus-appearance -> node_focus_appearance |
| node_type_body_scale | R2.1 | UI 正文常见基准：16px / 行高 1.5（24px）；小字 14px/20px，大文本 18px/28px；字号与行高应成组定义。 | verified-high | 1.0 | 4 | m3.material.io 为官方；pub.dev 第三方 M3TypeScale 仅作交叉验证，不作为独立来源计数。 | research/raw_corpus_design_specs.md#spec_tailwind_type_1 -> research/yield_filter.md#ui-type-body-scale -> node_type_body_scale; research/raw_corpus_design_specs.md#spec_govuk_type_1 -> research/yield_filter.md#ui-type-body-scale -> node_type_body_scale; research/raw_corpus_design_specs.md#spec_material_type_1 -> research/yield_filter.md#ui-type-body-scale -> node_type_body_scale; research/raw_corpus_design_specs.md#spec_primer_typography_1 -> research/yield_filter.md#ui-type-body-scale -> node_type_body_scale |
| node_type_measure | R2.2 | 正文行宽控制在大约 45–75 字符/行，通常用容器 max-width 而不是拉满屏幕。 | verified-single | 0.3 | 4 | 仅 Butterick（pending）支撑“45–75 字符”；Tailwind/GOV.UK 只支撑字号/行高旁证，核心数字为单源。 | research/classic_principles_corpus.md#classic_04 -> research/yield_filter.md#ui-line-length -> node_type_measure |
| node_font_personality | R2.3 | 字体选择会传达气质；正文应避免装饰体/极细体，可用 1–2 款字体配合字号/字重/字距建立层级。 | verified-single | 0.3 | 2 |  | research/classic_principles_corpus.md#classic_05 -> research/yield_filter.md#ui-font-personality -> node_font_personality |
| node_spacing_grid | R3.1 | 间距用统一尺度（4/8/12/16/24/32/48，基础 4px/8dp），组件对齐到 4px 或 8dp 网格。 | verified-high | 1.0 | 3 |  | research/raw_corpus_design_specs.md#spec_material_grid_1 -> research/yield_filter.md#ui-spacing-grid -> node_spacing_grid; research/raw_corpus_design_specs.md#spec_primer_typography_1 -> research/yield_filter.md#ui-spacing-grid -> node_spacing_grid; research/classic_principles_corpus.md#classic_03 -> research/yield_filter.md#ui-spacing-grid -> node_spacing_grid |
| node_hierarchy_scale | R4.1 | 用大小/字重/颜色/留白/位置建立视觉层级；同一屏尽量只 2–3 档强弱，并用眯眼测试验证。 | verified-high | 1.0 | 3 |  | research/raw_corpus_design_specs.md#spec_nng_hierarchy_1 -> research/yield_filter.md#ui-hierarchy-scale -> node_hierarchy_scale; research/classic_principles_corpus.md#classic_01 -> research/yield_filter.md#ui-hierarchy-scale -> node_hierarchy_scale |
| node_proximity_group | R3.2 | 相关元素放近、不相关元素放远；利用邻近性/共同区域分组，而不是全靠边框容器。 | verified-high | 1.0 | 3 |  | research/classic_principles_corpus.md#classic_02 -> research/yield_filter.md#ui-proximity-group -> node_proximity_group |
| node_whitespace_emphasis | R3.3 | 给最重要的元素更多留白/空间来强调；必要时再加极轻的背景/边框。 | verified-high | 1.0 | 2 |  | research/raw_corpus_design_specs.md#spec_nng_hierarchy_1 -> research/yield_filter.md#ui-whitespace-emphasis -> node_whitespace_emphasis; research/classic_principles_corpus.md#classic_08 -> research/yield_filter.md#ui-whitespace-emphasis -> node_whitespace_emphasis |
| node_clickable_affordance | R5.1 | 可点击元素保留可识别线索（颜色/边框/大小/位置/平台惯例）；静态内容不应长得像按钮。 | verified-high | 1.0 | 3 |  | research/classic_principles_corpus.md#classic_07 -> research/yield_filter.md#ui-clickable-affordance -> node_clickable_affordance |
| node_minimalism_delete | R7.1 | 删除不支持用户任务的装饰/元素；用留白、背景对比、空间替代多余边框/分隔线。 | verified-high | 1.0 | 3 |  | research/classic_principles_corpus.md#classic_08 -> research/yield_filter.md#ui-minimalism -> node_minimalism_delete |
| node_minimalism_warning | R7.1边界 | 极端极简/扁平会牺牲可发现性：用户找不到可点击元素、必要分隔丢失。 | verified-high | 1.0 | 3 |  | research/classic_principles_corpus.md#classic_07 -> research/yield_filter.md#ui-minimalism -> node_minimalism_warning; research/classic_principles_corpus.md#classic_08 -> research/yield_filter.md#ui-minimalism -> node_minimalism_warning |
| node_consistency | R5.2 | 同一产品内同类元素保持一致，并遵循平台/行业惯例，以降低学习成本。 | verified-single | 0.5 | 3 |  | research/classic_principles_corpus.md#classic_09 -> research/yield_filter.md#ui-consistency -> node_consistency |
| node_cta_hierarchy | R4.2 | 每个主要屏幕以单一主导 CTA 为核心；次要动作降级为文字/弱按钮。 | verified-high | 1.0 | 2 |  | research/classic_principles_corpus.md#classic_10 -> research/yield_filter.md#ui-cta-hierarchy -> node_cta_hierarchy |
| node_not_color_alone | R1.3 | 状态/差异不能只靠颜色：错误/成功/选中/链接需同时有文字、图标、形状或图案。 | verified-high | 1.0 | 2 |  | research/classic_principles_corpus.md#classic_06 -> research/yield_filter.md#ui-not-color-alone -> node_not_color_alone |
| node_style_editorial_sharp | S8.1 | 在编辑杂志/印刷风格语境下，可全局采用锐角（rounded-none）与无阴影，用透明度/边框建立层次。 | verified-single | 0.3 | 3 |  | research/local_material_inventory.md#L1-editorial-style-spec -> research/yield_filter.md#style-editorial-no-radius -> node_style_editorial_sharp; research/local_material_inventory.md#L2-stylekit-editorial -> research/yield_filter.md#style-editorial-no-radius -> node_style_editorial_sharp |
| node_style_tech_dark_rounded | S8.2 | 在科技/深色/现代风格语境下，可全局采用圆角（16–20px）、渐变、发光与玻璃卡片，用色彩梯度建立层次。 | verified-single | 0.3 | 2 |  | research/local_material_inventory.md#L3-ai-ppt-skill -> research/yield_filter.md#4.1-round-vs-sharp -> node_style_tech_dark_rounded |
| node_style_editorial_monochrome | S8.1补充 | 在单色优雅风格下，可用单一主色 + 透明度梯度（/60 /40 /10）构建视觉层级，而非彩色装饰。 | verified-single | 0.3 | 3 |  | research/local_material_inventory.md#L1-editorial-style-spec -> research/yield_filter.md#style-editorial-single-color -> node_style_editorial_monochrome; research/local_material_inventory.md#L2-stylekit-editorial -> research/yield_filter.md#style-editorial-single-color -> node_style_editorial_monochrome; research/local_material_inventory.md#L3-ai-ppt-skill -> research/yield_filter.md#style-editorial-single-color -> node_style_editorial_monochrome |
| R1.4 | R1.4 | 浅色与暗色模式都要验证 | verified-single | 0.5 | 1 | 单源：Apple 官方指导；WCAG 未直接给出双主题条款。 | research/raw_corpus_design_specs.md#spec_apple_contrast_1 -> ../SOURCES.md -> R1.4 |
| R6.3 | R6.3 | 可读性优先：核心正文 ≥14px、对比 ≥4.5:1 | verified-high | 1.0 | 2 | 由对比度/可读性研究集成，未单列节点。 | research/raw_corpus_design_specs.md#spec_wcag_contrast_1 -> ../SOURCES.md -> R6.3; research/classic_principles_corpus.md#classic_06 -> ../SOURCES.md -> R6.3 |
| R7.2 | R7.2 | 动效用于反馈而非炫技，并尊重减少动效偏好 | verified-single | 0.5 | 3 | 前三项中本地主题为风格旁证；NN/g 两条为一手研究。 | research/classic_principles_corpus.md#classic_08 -> research/yield_filter.md#ui-minimalism -> ../CONSENSUS.md#R7.2 -> R7.2; research/counterexamples.md#ce-excessive-decoration-motion -> ../CONSENSUS.md#R7.2 -> R7.2; research/local_material_inventory.md#L3-ai-ppt-skill -> ../CONSENSUS.md#R7.2 -> R7.2 |

## 3. 完整来源表

完整分组来源表见 `../SOURCES.md`；核心来源包括：
- 官方规范：WCAG 2.2、GitHub Primer、Tailwind、GOV.UK、Material Design、Apple
- 研究：Nielsen Norman Group 8 篇
- 书籍：Refactoring UI、Practical Typography、Don't Make Me Think、Designing Interfaces、The Design of Everyday Things
- 本地补充：editorial-style-spec、stylekit、ai-ppt、dsh-deep-whale（仅参考/审计，见 PROVENANCE.md）

## 4. 蒸馏自检与干跑

- 蒸馏质量自检分：**7/7**
- 样例：5 个（登录卡片/数据表/状态提示/风格边界/深色模式），每个命中 ≥3 条规则
- 规则触发矩阵：21 条规则全部有触发场景、可执行动作、可用边界（见 `research/dry_run_report.md`）
- vault 校验：`OK: 12 skill(s) validated in vault/skills`（validate-vault.mjs）

## 5. 未决边界 / 单源待证 / 冲突分支

### 5.1 单源待证（weight 0.3–0.5）

- `node_focus_appearance`（R6.2）：焦点指示器面积至少约等于 2 CSS px 粗的外轮廓周长，并在聚焦/未聚焦同位置像素间保持 ≥3:1；内嵌焦点环需更粗（如 ≥3px）。；权重 0.5
- `node_type_measure`（R2.2）：正文行宽控制在大约 45–75 字符/行，通常用容器 max-width 而不是拉满屏幕。；权重 0.3；仅 Butterick（pending）支撑“45–75 字符”；Tailwind/GOV.UK 只支撑字号/行高旁证，核心数字为单源。
- `node_font_personality`（R2.3）：字体选择会传达气质；正文应避免装饰体/极细体，可用 1–2 款字体配合字号/字重/字距建立层级。；权重 0.3
- `node_consistency`（R5.2）：同一产品内同类元素保持一致，并遵循平台/行业惯例，以降低学习成本。；权重 0.5
- `node_style_editorial_sharp`（S8.1）：在编辑杂志/印刷风格语境下，可全局采用锐角（rounded-none）与无阴影，用透明度/边框建立层次。；权重 0.3
- `node_style_tech_dark_rounded`（S8.2）：在科技/深色/现代风格语境下，可全局采用圆角（16–20px）、渐变、发光与玻璃卡片，用色彩梯度建立层次。；权重 0.3
- `node_style_editorial_monochrome`（S8.1补充）：在单色优雅风格下，可用单一主色 + 透明度梯度（/60 /40 /10）构建视觉层级，而非彩色装饰。；权重 0.3
- `R1.4`（双主题验证）：单源 Apple 官方指导；权重 0.5
- `R7.2`（动效反馈）：单源/风格；权重 0.5

### 5.2 冲突分支（保留不平均）

- 极简：`node_minimalism_delete` ↔ `node_minimalism_warning`
- 圆角/阴影：`node_style_editorial_sharp` ↔ `node_style_tech_dark_rounded`
- 单色风格：`node_style_editorial_monochrome` 为风格分支，不作为通用规则
- 行宽：R2.2 长散文 45–75 字符 ↔ 数据表/代码/短标签不适用（见 `research/counterexamples.md#ce-measure-rule-overapplied`）
- 单一 CTA：R4.2 突出一个主 CTA ↔ 表单/工具栏多个同等重要动作时不硬突出（见 `research/counterexamples.md#ce-single-cta-absolute`）
- 一致性：R5.2 同产品一致 ↔ 不同语境可有意分群（见 `research/counterexamples.md#ce-over-consistency-stiff`）

### 5.3 其他未决

- Practical Typography / DMMT / Designing Interfaces / Norman 书页正文未取，作为 pending，不单独作为证据。
- Apple HIG 主排版页为 JS 渲染，暂用 Apple Help 对比度页替代。
- m3.material.io 类型 token 页为 JS 渲染，用第三方 pub.dev 辅助核验（不作官方依据）。

## 6. 人工复核入口

> 请人/用户复核：如果对任何规则、分级、来源或边界“**我感觉不对劲**”，可直接提出，我会停止当前结论并重新检查，不硬套模板。
> 建议复核点：① 单源规则是否应继续补源；② 风格分支是否该保留；③ 样例改进是否与实际产品语境匹配；④ 是否需要真实 A/B 数据替代当前“干跑+自检”。
