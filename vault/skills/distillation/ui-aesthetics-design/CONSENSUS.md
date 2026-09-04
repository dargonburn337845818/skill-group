# UI 美学设计 · 完整规则与依据（CONSENSUS）

> 本文件是 `SKILL.md` 的完整版：每条规则给来源、证据分级、失效边界与可执行检查动作。
> 证据分级：`多源核实`（≥2 独立来源或官方一手）/ `单源待证`（单一来源，降权）/ `风格分支`（风格分支，非共识）。
> 反例细节与研究附注见同目录 `audit/`（仅作审计，不作为最终用户文档）。

---

## 1. 色彩与对比

### R1.1 正文对比度 ≥4.5:1，大文本 ≥3:1
- 动作：计算前景/背景对比度；正文不能低于 4.5:1；大文本（14pt 粗体≈18.5px 或 18pt 常规≈24px）可 3:1；不要四舍五入。
- 来源：
  - https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum
  - https://primer.github.io/design/foundations/color/accessibility/
  - https://developer.apple.com/help/app-store-connect/manage-app-accessibility/sufficient-contrast-evaluation-criteria
- 证据：`多源核实`
- 失效边界：禁用/装饰文本、logo 不适用；超细字即使数值达标也可能更弱，建议留余量。

### R1.2 非文本对比度 ≥3:1
- 动作：控件边框/图标/关键图形与相邻色至少 3:1；禁用态除外。
- 来源：
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast
  - https://primer.github.io/design/foundations/color/accessibility/
- 证据：`多源核实`
- 失效边界：纯装饰、用户代理默认样式不适用；2.999:1 不达标。

### R1.3 不要只靠颜色表达状态
- 动作：错误/成功/选中加文字、图标、形状或图案；链接保留下划线等线索。
- 来源：
  - https://www.nngroup.com/articles/visual-treatments-accessibility/
  - https://primer.github.io/design/foundations/color/accessibility/
- 证据：`多源核实`
- 失效边界：纯装饰色可自由用；低风险场景可放宽，但表单/图表/工具仍应保留非颜色线索。

### R1.4 浅色与暗色模式都要验证
- 动作：用语义 token 而非硬编码色值；两套主题都测对比度。
- 来源：https://developer.apple.com/help/app-store-connect/manage-app-accessibility/sufficient-contrast-evaluation-criteria
- 证据：`单源待证`（本规则为 Apple 官方指导；WCAG 未直接给出“双主题”条款，故按单一来源保守标为「单源待证」）
- 失效边界：如果产品没有暗色模式则跳过；不要只测其中一套。

---

## 2. 字体与排版

### R2.1 正文常见基准：16px / 行高 1.5（24px）
- 动作：从 14/16/18/20px 阶梯取字号；行高用无单位比例（约 1.4–1.7）；核心正文 ≥14px。
- 来源：
  - https://tailwindcss.com/docs/font-size
  - https://design-system.service.gov.uk/styles/type-scale/
  - https://m3.material.io/styles/typography/type-scale-tokens（官方；数值另经第三方 pub.dev M3TypeScale 辅助核验）
  - https://primer.github.io/design/foundations/typography/
- 证据：`多源核实`
- 失效边界：政府级正文 19px/25px；12px 只用于辅助；不同语言可调。
- 来源说明：pub.dev 的 `material_design` Dart 包为第三方辅助文档，不作为 Material 官方依据；官方依据以 m3.material.io 为准。

### R2.2 长段落控制行宽
- 动作：长散文设 max-width（约 45–75 字符；CSS 常用 65–75ch），避免全宽长行。
- 来源：
  - https://practicaltypography.com/line-length.html
  - https://tailwindcss.com/docs/font-size
  - https://design-system.service.gov.uk/styles/type-scale/
- 证据：`单源待证`（45–75 字符为排印流派观点）
- 失效边界：代码、表格、短标签不适用；中文/日文需按语言调宽。

### R2.3 字体气质与正文可读性
- 动作：先定气质再选 1–2 款字体；正文避免装饰体/极细体；用字号/字重/字距建立层级。
- 来源：https://practicaltypography.com/ 、 https://refactoringui.com/
- 证据：`单源待证`（风格类）
- 失效边界：无唯一答案；工具型界面优先可读性而非气质。

---

## 3. 间距与布局

### R3.1 统一间距尺度（4/8/12/16/24/32/48）
- 动作：建 spacing token；所有 margin/padding/gap 从尺度取；组件对齐 4px/8dp 网格。
- 来源：
  - https://m1.material.io/layout/metrics-keylines.html
  - https://primer.github.io/design/foundations/typography/
  - https://refactoringui.com/
- 证据：`多源核实`
- 失效边界：数据密集界面可自定义更小尺度；可用性优先于网格。

### R3.2 邻近性分组
- 动作：相关元素放近、不相关放远；标签紧贴字段；按钮紧贴作用对象。
- 来源：
  - https://www.nngroup.com/articles/form-design-white-space/
  - https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
  - https://refactoringui.com/
- 证据：`多源核实`
- 失效边界：信息过密时过度留白会断裂；容器加太多会杂乱。

### R3.3 留白做强调
- 动作：给最重要元素更多空间；不够时再加极轻背景或 1px 边框。
- 来源：
  - https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
  - https://refactoringui.com/
- 证据：`多源核实`
- 失效边界：不能为留白牺牲信息密度/可点性。

---

## 4. 层级与视觉焦点

### R4.1 用大小/字重/颜色/位置制造层级
- 动作：同一屏 2–3 档强弱；眯眼测试验证；最重要元素更大/更重/更亮。
- 来源：
  - https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
  - https://www.nngroup.com/articles/principles-visual-design/
  - https://refactoringui.com/
- 证据：`多源核实`
- 失效边界：表格/表单/列表项不该刻意放大某一项；所有都大等于没层级。

### R4.2 一个屏幕一个主导 CTA
- 动作：主 CTA 最高权重，次要动作弱化；同等重要动作不硬突出。
- 来源：
  - https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
  - https://refactoringui.com/
- 证据：`多源核实`
- 失效边界：表单/工具栏多个同等重要动作时，不适用“只突出一个”。

---

## 5. 控件/表单

### R5.1 可点击元素保留线索
- 动作：颜色/边框/底色/大小/位置/平台惯例任选其一给信号；hover/focus 反馈；足够点击区域。
- 来源：
  - https://www.nngroup.com/articles/clickable-elements/
  - https://www.nngroup.com/articles/flat-design/
  - https://jnd.org/books/the-design-of-everyday-things-revised-and-expanded-edition/（书页 pending，不单独作为独立证据）
- 证据：`多源核实`
- 失效边界：传统蓝色链接不是唯一形式；但不能删除全部可点击线索。

### R5.2 同产品保持一致
- 动作：同类控件、命名、布局统一；遵循平台惯例。
- 来源：
  - https://www.nngroup.com/articles/consistency-and-standards/
  - https://sensible.com/dont-make-me-think/ （pending，待核验）
  - https://www.oreilly.com/library/view/designing-interfaces-3rd/9781492051954/ （pending，待核验）
- 证据：`单源待证`（仅 NN/g 一手可复核；后两本 pending，不计入独立证据）
- 失效边界：不是绝对不变；不同语境可有意分群；不能牺牲可发现性/无障碍。

---

## 6. 无障碍

### R6.1 焦点可见且不超时
- 动作：保留 focus 样式；键盘导航可见；不要 time-limited。
- 来源：
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-visible
  - https://www.nngroup.com/articles/visual-treatments-accessibility/
- 证据：`多源核实`
- 失效边界：鼠标用户也可能需要；不要只做 hover。

### R6.2 焦点环面积与对比
- 动作：焦点环 ≥2px 粗外轮廓，聚焦/未聚焦同位置像素 ≥3:1；内嵌焦点环需 ≥3px。
- 来源：https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance-minimum
- 证据：`单源待证`（Level AAA 参考）
- 失效边界：AA 只要求可见不超时；此条是可选的更强标准。

### R6.3 可读性优先
- 动作：核心正文 ≥14px、对比 ≥4.5:1；弱化只用于辅助文本；细字体只用于大标题。
- 来源：https://www.nngroup.com/articles/visual-treatments-accessibility/ 、 https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum
- 证据：`多源核实`
- 失效边界：品牌艺术字/海报可例外；产品功能界面不能例外。

---

## 7. 动效与装饰

### R7.1 少即是多，但不为空
- 动作：删不支持任务的内容/装饰；用留白/对比/空间替代多余边框；保留必要分隔与线索。
- 来源：
  - https://refactoringui.com/
  - https://www.nngroup.com/articles/characteristics-minimalism/
  - https://www.nngroup.com/articles/flat-design/
- 证据：`多源核实`
- 失效边界：过度极简会破坏可发现性；关键信息/无障碍线索不能删。

### R7.2 动效用于反馈而非炫技
- 动作：动效用于状态变化/层级变化；尊重 `prefers-reduced-motion`。
- 来源：
  - https://www.nngroup.com/articles/characteristics-minimalism/
  - https://www.nngroup.com/articles/flat-design/
  - 本地 ai-ppt tech-dark 主题（见 `audit/PROVENANCE.md`，风格参考）
- 证据：`单源待证`
- 失效边界：品牌展示页可适当装饰；阅读/工具界面应克制。

---

## 8. 风格分支（非共识）

### S8.1 锐角/无阴影（Editorial）
- 动作：仅在选定“编辑杂志/作品集”风格时用：圆角归零、无阴影、单色+透明度、衬线标题。
- 来源：本地 Editorial 风格规范与 StyleKit Editorial 文件（见 `audit/PROVENANCE.md`）、https://www.stylekit.top/zh/styles/editorial
- 证据：`单源待证` / 风格分支
- 失效边界：数据密集/多色产品、现代圆角风格不适用；不当普适标准。

### S8.2 圆角/渐变/发光（tech-dark）
- 动作：仅在选定“科技/深色/现代”风格时用：深色渐变底、圆角 16–20px、半透明卡片、青蓝强调。
- 来源：本地 ai-ppt tech-dark 主题（见 `audit/PROVENANCE.md`）、`audit/research/local_material_inventory.md`
- 证据：`单源待证` / 风格分支
- 失效边界：印刷/单色优雅风格不适用；不应作为通用美学。

---

## 9. 反例与失效边界（速查）

| 反例 | 触发 | 绕过 |
|---|---|---|
| 暗色模式失效 | 只测浅色、硬编码色值 | 语义 token + 双主题测对比 |
| 数据密集界面被过度留白 | 把极简套到表格/仪表盘 | 紧凑间距、清晰网格、保留密度 |
| 品牌风格被普适化 | 照搬零圆角/无阴影到通用产品 | 限定为主题层，保留通用底线 |
| 无障碍折衷 | 正文缩小变淡、细字重 | 核心正文 ≥14px、对比 ≥4.5:1 |
| 过度一致导致呆板 | 营销页/数据后台同模板 | 锁交互模式，允许语境差异 |
| 过度装饰/动画 | 阅读/表单堆渐变发光 | 动效只用于反馈，尊重 reduced-motion |
| 单一 CTA 绝对化 | 表单/工具栏多个同等动作 | 同等重要则同等权重/分组 |
| 只靠颜色 | 错误/成功只红绿 | 加文字/图标/形状 |
| 单源风格库当权威 | 拿 StyleKit 评分当证据 | 核心规则需 ≥2 独立来源，风格仅参考 |
| 行宽误用 | 代码/表格套 65ch | 只对长散文启用，代码按自身布局 |
| 极简破坏可发现性 | 按钮像文本，无焦点态 | 保留至少一种可点击线索 + focus |

---

## 10. 样例对照（问题 → 规则 → 改进）

### Example A：登录卡片
- 问题：正文灰字 `#999` 在白底上，标签 12px，只有一个“登录”按钮也特别小。
- 命中：R1.1 对比、R2.1 字号、R6.1 焦点、R5.1 可点击。
- 改进：正文/标签对比 ≥4.5:1；标签与输入 14–16px；主按钮加大并填充主色；输入框 focus 加 2px 环。

### Example B：数据表格
- 问题：为了“极简”删除所有网格线、行高 1.8，10 行数据要滚两屏。
- 命中：R7.1 少即是多边界、R3.1 间距密度、反例：数据密集界面不应过度留白（关联 R3.2 分组边界）。
- 改进：行高 1.4，保留表头/行间细分割线，分组间距 16px，表格字号 14px，不放大行距。

### Example C：状态提示
- 问题：成功/失败只用绿色/红色圆点。
- 命中：R1.3 不只靠颜色、R1.2 非文本对比。
- 改进：绿/红点旁加图标+文字；圆点与背景 ≥3:1；失败信息给具体文字。

### Example D：品牌杂志页
- 问题：把 Editorial 的“无圆角无阴影单色”直接用于电商数据分析盘。
- 命中：S8.1 风格分支、R1.3 不只靠颜色、R5.1 可点击线索、反例：把品牌风格误当通用标准。
- 改进：保留杂志风格的标题/留白作为主题层；数据区恢复紧凑网格、多色语义与可点击线索；不把单色当通用标准。

### Example E：深色模式
- 问题：浅色模式正文 `#333` 通过，切暗色后仍是深色文字。
- 命中：R1.4 双主题验证、R2.1 语义 token、R1.1 正文对比度。
- 改进：使用 `--fg`/`--bg` token；暗色下反转前景/背景，重新测对比度。

---

## 11. 用户话术

> 我会按“色彩对比、字体、间距、层级、控件、无障碍、动效与装饰、反例”八块检查；每个问题都会告诉你：命中哪条规则、依据从哪来、边界在哪。涉及风格（圆角/无阴影/单色等），我会明确说“这是风格选择，不是通用规则”。

## 12. 来源分层

- **官方规范/标准**：W3C WCAG、Apple、GOV.UK、Tailwind、Primer、Material。
- **一手研究/文章**：Nielsen Norman Group。
- **经典书籍**：Refactoring UI、Practical Typography、Don't Make Me Think、Designing Interfaces、The Design of Everyday Things（部分书页 pending）。
- **本地/补充**：editorial-style-spec、stylekit、ai-ppt-skill、dsh-deep-whale-inspect（仅风格参考，不作权威）。
