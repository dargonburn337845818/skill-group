# UI 美学设计 · 来源清单（SOURCES）

> 本文件列出本 Skill 使用的全部来源，按类型分组；每条标注用途、可信度与贡献点。
> 分级：`official`（官方标准/设计系统）/ `research`（一手研究）/ `book`（经典书）/ `local`（本地补充）/ `third-party`（第三方辅助，仅交叉验证）。
> `待核验` = 有公开 URL 但未取到可复核原文，不作为独立证据。

## 1. 官方标准与设计系统（official）

| 来源 | URL | 用途 / 贡献点 | 可信度 |
|---|---|---|---|
| WCAG 2.2 · Contrast (Minimum) | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum | 正文 4.5:1、大文本 3:1、不四舍五入 | 官方一手，多源核实 |
| WCAG 2.2 · Non-text Contrast | https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast | 控件/图形 3:1 | 官方一手，多源核实 |
| WCAG 2.2 · Focus Visible | https://www.w3.org/WAI/WCAG22/Understanding/focus-visible | 焦点可见、不超时 | 官方一手，多源核实 |
| WCAG 2.2 · Focus Appearance (Minimum) | https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance-minimum | 焦点环 2px 粗、状态间 3:1 | 官方一手，AAA 参考（单源待证） |
| GitHub Primer · Color Accessibility | https://primer.github.io/design/foundations/color/accessibility/ | 4.5:1/3:1、不只靠颜色 | 官方设计系统，多源核实 |
| GitHub Primer · Typography | https://primer.github.io/design/foundations/typography/ | rem token、无单位行高、4px 网格 | 官方设计系统，多源核实 |
| Tailwind CSS · Font Size | https://tailwindcss.com/docs/font-size | 14/16/18/20px 与行高基准 | 官方文档，多源核实 |
| GOV.UK Design System · Type Scale | https://design-system.service.gov.uk/styles/type-scale/ | 19px/25px 正文、标题阶梯 | 官方设计系统，多源核实 |
| Material Design · Metrics & Keylines | https://m1.material.io/layout/metrics-keylines.html | 8dp/4dp 基线网格、16dp 边距 | 官方一手，多源核实 |
| Material Design 3 · Type Scale Tokens | https://m3.material.io/styles/typography/type-scale-tokens | MD3 类型体系官方入口 | 官方（JS 渲染，数值经第三方辅助核验） |
| Apple · Sufficient Contrast Evaluation Criteria | https://developer.apple.com/help/app-store-connect/manage-app-accessibility/sufficient-contrast-evaluation-criteria | 4.5:1、暗色模式也需检查 | 官方一手，多源核实 |

## 2. 一手研究（research）

| 来源 | URL | 用途 / 贡献点 | 可信度 |
|---|---|---|---|
| NN/g · Visual Hierarchy in UX | https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ | 层级由色彩/对比/尺度/分组创建；眯眼测试 | 一手研究，多源核实 |
| NN/g · 5 Principles of Visual Design | https://www.nngroup.com/articles/principles-visual-design/ | 尺度/层级/平衡/对比/格式塔 | 一手研究，多源核实 |
| NN/g · Clickable Elements | https://www.nngroup.com/articles/clickable-elements/ | 可点击线索、感知 affordance | 一手研究，多源核实 |
| NN/g · Form White Space | https://www.nngroup.com/articles/form-design-white-space/ | 邻近性分组、表单留白 | 一手研究，多源核实 |
| NN/g · Minimalism in Web Design | https://www.nngroup.com/articles/characteristics-minimalism/ | 删除不支持任务的元素 | 一手研究，多源核实 |
| NN/g · Visual Treatments & Accessibility | https://www.nngroup.com/articles/visual-treatments-accessibility/ | 不只靠颜色、焦点态、真实用户测试 | 一手研究，多源核实 |
| NN/g · Consistency and Standards | https://www.nngroup.com/articles/consistency-and-standards/ | 一致性启发式 | 一手研究，多源核实 |
| NN/g · Flat Design | https://www.nngroup.com/articles/flat-design/ | 扁平/极简的可发现性风险 | 一手研究，多源核实 |

## 3. 经典书籍（book）

| 来源 | URL/引用 | 用途 / 贡献点 | 可信度 |
|---|---|---|---|
| Refactoring UI（Wathan & Schoger） | https://refactoringui.com/ | 少用边框、间距/留白/阴影做区分、主次 tactic | 经典书；官网可访问，书内细节 待核验 |
| Practical Typography（Butterick） | https://practicaltypography.com/ 、 https://practicaltypography.com/line-length.html | measure/行宽、字体气质、装饰体边界 | 经典书；沙箱连接超时，正文 待核验，只作风格分支 |
| Don't Make Me Think（Krug） | https://sensible.com/dont-make-me-think/ 、 https://www.amazon.com/Dont-Make-Me-Think-Usability/dp/0321965515 | 自明性、降低思考 | 官方页 待核验；概念旁证 |
| Designing Interfaces（Tidwell 等） | https://www.oreilly.com/library/view/designing-interfaces-3rd/9781492051954/ 、 https://www.amazon.com/Designing-Interfaces-Patterns-Effective-Interaction/dp/1492051969 | 交互模式、一致性 | O'Reilly 正文 待核验；概念旁证 |
| The Design of Everyday Things（Norman） | https://jnd.org/books/the-design-of-everyday-things-revised-and-expanded-edition/ | affordance / signifier | 书页 待核验；概念旁证 |

## 4. 本地补充（local，仅参考不作权威）

| 路径 | 用途 / 贡献点 | 可信度 |
|---|---|---|
| Editorial 风格规范（本机文件） | 本地：Editorial 风格 token、禁止项、正反对照（见 `audit/PROVENANCE.md`） | 本地单风格，参考 |
| StyleKit Editorial（本机文件） | 本地：色板/FAQ/提示词（见 `audit/PROVENANCE.md`） | 第三方风格库，单风格 |
| ai-ppt tech-dark / editorial 主题（本机文件） | 本地：多主题 token 与排版/质检流程（见 `audit/PROVENANCE.md`） | 本地项目实践，参考 |
| DSH 皮肤系列（本机文件） | 本地：强风格一致性、版权署名提醒（见 `audit/PROVENANCE.md`） | 本地皮肤项目，参考 |
| `audit/research/local_material_inventory.md` | 本地素材盘点：哪些可作旁证/样例/反例 | 本包审计材料（不含权威） |

## 5. 第三方辅助（third-party，不作独立证据）

| 来源 | URL | 用途 | 说明 |
|---|---|---|---|
| pub.dev · material_design M3TypeScale | https://pub.dev/documentation/material_design/latest/material_design/M3TypeScale-class.html | 辅助读取 MD3 15 个类型 token 数值 | 第三方 Dart 包 API；仅用于交叉验证，官方依据以 m3.material.io 为准 |
| StyleKit Editorial | https://www.stylekit.top/zh/styles/editorial | 单一风格示例 | 第三方风格库，不作通用证据 |

## 6. 待核验（待核验）

- Practical Typography 行宽正文（沙箱连接失败）。
- Don't Make Me Think 官方页（406）。
- Designing Interfaces O'Reilly 页（403）。
- The Design of Everyday Things 书页正文（未取）。
- Apple HIG 主排版页（JS 渲染；暂用 Apple Help 对比度页替代）。
- m3.material.io 类型 token 页静态正文（JS 渲染；用第三方辅助核验）。

## Round 35 新增来源

> 本轮于 2026-09-05 通过直接抓取/核验加入；均为公开可访问页面，服务 `SKILL.md` 中「2026 深度补强（Round 35）」的 R35-1～R35-8。
> 核验方式：HTTP 200 + 页面正文提取；来源可信度沿用本文件既有分级约定。

### 官方标准与设计系统（official）

| 来源 | URL | 用途 / 贡献点 | 可信度 |
|---|---|---|---|
| WCAG 2.2 · Text Spacing | https://www.w3.org/WAI/WCAG22/Understanding/text-spacing | 文本重排：行高 ≥1.5、段后距 ≥2×字号、字距 ≥0.12em、词距 ≥0.16em；用户发起的样式覆盖不得导致内容丢失 | 官方一手，已抓取 |
| WCAG 2.2 · Target Size (Minimum) | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum | 指针目标最小 24×24 CSS px；不足时用 24px 直径圆不重叠做间距豁免；含 5 类例外说明 | 官方一手，已抓取 |
| IBM Design Language · Color | https://www.ibm.com/design/language/color/ | 色阶步数估算对比度、渐变背景按最低对比色校核、色盲限制、色板/色族组织 | 官方设计系统，已抓取 |
| Atlassian Design System · Color | https://atlassian.design/foundations/color/ | 语义色角色（neutral/brand/information/success/warning/danger/accent）、token 命名、饱和/中性/alpha 分类 | 官方设计系统，已抓取 |

### 一手研究（research）

| 来源 | URL | 用途 / 贡献点 | 可信度 |
|---|---|---|---|
| NN/g · Contrast: One of the 3 Cs for Better Charts | https://www.nngroup.com/articles/contrast-charts/ | 先灰后彩、标注层、标题同色、callout | 一手研究，已抓取 |
| NN/g · Clutter-Free: One of the 3 Cs for Better Charts | https://www.nngroup.com/articles/clutter-charts/ | data-ink ratio、删 chartjunk、直接标签、去多余轴/网格/图例 | 一手研究，已抓取 |
| NN/g · Using Color to Enhance Your Design | https://www.nngroup.com/articles/color-enhance-design/ | 色彩 harmony、60-30-10、限约 3 色、颜色一致性、灰色按钮警示 | 一手研究，已抓取 |
| NN/g · Touch Targets on Touchscreens | https://www.nngroup.com/articles/touch-target-size/ | 触控目标 ≥1cm×1cm、Fitts 定律、位置与间距、主 CTA 更大 | 一手研究，已抓取 |
| NN/g · Executing UX Animations: Duration and Motion Characteristics | https://www.nngroup.com/articles/animation-duration/ | 100–500ms、微交互 100ms、进入/退出时长、easing、动效无障碍 | 一手研究，已抓取 |
| NN/g · The Dos and Don’ts of Pairing Typefaces | https://www.nngroup.com/articles/pairing-typefaces/ | 字体分类、多字重优先、装饰体边界、明确角色、易混字符 | 一手研究，已抓取 |
| NN/g · Legibility, Readability, and Comprehension | https://www.nngroup.com/articles/legibility-readability-comprehension/ | 大字号可缩放、高对比、纯背景、干净字体；易读/可读/理解三层 | 一手研究，已抓取 |

### 一手科研材料（research/tool）

| 来源 | URL | 用途 / 贡献点 | 可信度 |
|---|---|---|---|
| Okabe & Ito · Color Universal Design (CUD) | https://jfly.uni-koeln.de/color/ | 色盲频率与原理、冗余编码、避免同亮度不同色相、红绿限制、色盲安全色板与检查工具 | 一手科研材料，已抓取 |
