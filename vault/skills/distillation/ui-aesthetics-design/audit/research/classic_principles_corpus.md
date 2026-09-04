# Classic UI/UX Principles Corpus（经典 UI/UX 设计原则原始语料）

> 用途：为「UI 美学设计 Skill」提供可执行的原则语料。
> 提取方式：从经典 UI/UX 书籍与 NN/g 一手文章中提炼“最小推理单元”，不是整章摘要。
> 记录约定：每个单元含 `id / context / trigger / action / why / boundary / source / grade`。
> 分级定义：
> - `consensus`：多来源/多流派公认，或官方标准+研究一致。
> - `style`：单一作者/流派的偏好，降权使用；只代表该作者或该流派。
> - `warning`：针对高发错误的警戒/反指示。
> 提取时间：2026-09-04。直接抓取的页面标“已抓取”；无法取到原文的书页标 `pending`，不编造原话。

## 1. 来源清单

| # | 标题/书名 | 作者/机构 | URL | 贡献点 | 可信度 |
|---|---|---|---|---|---|
| S1 | Refactoring UI | Adam Wathan & Steve Schoger | https://refactoringui.com/ | 面向开发者的 UI 战术：少用边框、用留白/背景/阴影做区分、把设计当具体 tactic | 官方站已抓取（HTTP 200）；书为付费电子书，书内全文未取 → 书内细节 `pending` |
| S2 | Practical Typography | Matthew Butterick | https://practicaltypography.com/ | 线上排版书：measure/行宽、行高、字体气质、装饰字体不用于正文 | 公开在线书；沙箱连接超时（HTTP 000）→ `pending` |
| S3 | Don't Make Me Think (Revisited) | Steve Krug | 官方页 https://sensible.com/dont-make-me-think/ ；Amazon 书页 https://www.amazon.com/Dont-Make-Me-Think-Usability/dp/0321965515 | 自明性、一致性、去掉不必要的思考；用户不该为“怎么点”而思考 | 官方页沙箱 406 被挡；Amazon 200；全书正文未取 → `pending` |
| S4 | Designing Interfaces (3rd ed.) | Jenifer Tidwell, Charles Brewer, Aynne Valencia | O'Reilly https://www.oreilly.com/library/view/designing-interfaces-3rd/9781492051954/ ；Amazon https://www.amazon.com/Designing-Interfaces-Patterns-Effective-Interaction/dp/1492051969 | 交互模式复用、一致性与可预期性 | O'Reilly 沙箱 403；Amazon 200；正文未取 → `pending` |
| S5 | The Design of Everyday Things (Revised & Expanded) | Don Norman | https://jnd.org/books/the-design-of-everyday-things-revised-and-expanded-edition/ | 可感知 affordance / signifier、可见性、可用性优先 | 官方书页 200；正文未取 → `pending` |
| S6 | Visual Hierarchy in UX: Definition | NN/g（Kelley Gordon） | https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ | 视觉层级用色彩/对比、尺度、分组创建；squint test | 已抓取（HTTP 200） |
| S7 | 5 Principles of Visual Design in UX | NN/g（Kelley Gordon） | https://www.nngroup.com/articles/principles-visual-design/ | 尺度/视觉层级/平衡/对比/格式塔；一个好的视觉设计通常不超过 3 种尺寸 | 已抓取（HTTP 200） |
| S8 | Beyond Blue Links: Making Clickable Elements Recognizable | NN/g（Hoa Loranger） | https://www.nngroup.com/articles/clickable-elements/ | 可点击线索：边框、颜色、大小、一致性、位置、遵循标准；感知 affordance/signifier | 已抓取（HTTP 200） |
| S9 | Group Form Elements Effectively Using White Space | NN/g（Marieke McCloskey） | https://www.nngroup.com/articles/form-design-white-space/ | 邻近性（Law of Proximity）：相关元素放近、不相关放远 | 已抓取（HTTP 200） |
| S10 | The Characteristics of Minimalism in Web Design | NN/g（Kate Moran） | https://www.nngroup.com/articles/characteristics-minimalism/ | 极简主义：删除不支持用户任务的元素/内容；负空间、少 UI、有限配色 | 已抓取（HTTP 200） |
| S11 | 5 Visual Treatments that Improve Accessibility | NN/g（Kelley Gordon） | https://www.nngroup.com/articles/visual-treatments-accessibility/ | 对比度、不只靠颜色、焦点态、真实用户测试 | 已抓取（HTTP 200） |
| S12 | Maintain Consistency and Adhere to Standards (Usability Heuristic #4) | NN/g（Jakob Nielsen） | https://www.nngroup.com/articles/consistency-and-standards/ | 一致性是可用性启发式：内部一致 + 遵循平台/惯例 | URL 已核验 200；正文未本条抓取 |
| S13 | Material Design · Metrics & Keylines | Google | https://m1.material.io/layout/metrics-keylines.html | 8dp 基线网格、4dp 图标/排印网格、16dp 边距等间距节奏 | 已抓取（HTTP 200） |
| S14 | GitHub Primer · Typography foundations | GitHub | https://primer.github.io/design/foundations/typography/ | rem 单位、无单位行高、对齐 4px 网格 | 已抓取（HTTP 200） |
| S15 | Tailwind CSS · font-size | Tailwind Labs | https://tailwindcss.com/docs/font-size | 常用 UI 正文基准：14px/20px、16px/24px、18px/28px、20px/28px | 已抓取（HTTP 200） |
| S16 | GOV.UK Design System · Type scale | GOV.UK | https://design-system.service.gov.uk/styles/type-scale/ | 政府级正文默认 19px/25px、小字 16px/20px 等 | 已抓取（HTTP 200） |

## 2. 推理单元列表

### classic_01 · 用「尺度」建立视觉层级

- **id**: `classic_01`
- **context**: 页面上元素被同等对待，用户第一眼不知道先看哪里、做什么。
- **trigger**: 一个页面/卡片里的元素视觉权重接近（同字号、同字重、同颜色、同留白），或主次关系不清晰。
- **action**:
  1. 给最重要的元素最大的相对尺寸（或最重的字重/最亮的色彩对比）。
  2. 同一屏尽量只用到 2–3 档大小；用大小层级拉开主次，不要所有元素都“用力”。
  3. 用“眯眼/模糊测试”检查：模糊后是否仍能看出最重要的元素。
- **why**: NN/g 的「尺度」原则说明“相对大小标识重要性”，大元素更易被注意；视觉层级通过 scale / value / color / spacing / placement 实现，能引导用户按意图顺序读取，降低解析成本。Refactoring UI 的「tactic 而非天赋」与 NN/g 的研究在“用对比/尺度做焦点”上一致。
- **boundary**: 不是越大越好；如果所有元素都大，等于没有层级。信息均等的地方（表格、表单字段、列表项）不应刻意放大某一项。超过 3 档尺寸会制造混乱。
- **source**: [NN/g: Visual Hierarchy in UX](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)；[NN/g: 5 Principles of Visual Design in UX](https://www.nngroup.com/articles/principles-visual-design/)；[Refactoring UI](https://refactoringui.com/)
- **grade**: `consensus`

### classic_02 · 用邻近性/留白分组，而不是全靠容器

- **id**: `classic_02`
- **context**: 表单、卡片、列表、工具栏里的元素关系含糊，用户不确定“这个标签属于哪个字段”“这个按钮作用在哪”。
- **trigger**: 相关元素与不相关元素之间距离相等；标签离字段比离相邻字段还远；按钮离它作用的对象太远。
- **action**:
  1. 把相关元素放得更近、不相关元素放得更远（Law of Proximity）。
  2. 给最重要的元素更多留白（让它“呼吸”），用它获得的注意来突出。
  3. 如果只靠留白不够，再加容器/边框/背景，但要用得克制。
- **why**: NN/g 表单研究明确“items near each other appear related”，并指出这是 Gestalt 的 Law of Proximity；视觉层级文章也说“给核心元素更多空间会获得更多注意”。
- **boundary**: 留白不是万能的：信息密集界面（数据表、仪表盘）过度留白会让信息断裂；容器/边框加太多会显得杂乱（Refactoring UI 建议少用边框）。当空间受限时，先保证分组清晰再谈呼吸感。
- **source**: [NN/g: Group Form Elements Effectively Using White Space](https://www.nngroup.com/articles/form-design-white-space/)；[NN/g: Visual Hierarchy in UX](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)；[Refactoring UI](https://refactoringui.com/)
- **grade**: `consensus`

### classic_03 · 用统一的间距尺度（4/8/16/24）而不是随意数值

- **id**: `classic_03`
- **context**: 界面里间距数值很随机（7px、11px、13px 等），元素之间没有节奏感。
- **trigger**: margin/padding 出现大量非增量数值；卡片边距、按钮内边距、列表间距互不呼应。
- **action**:
  1. 建立可复用的间距 token，采用 4px/8px 增量的尺度（如 4/8/12/16/24/32/48）。
  2. 所有 `margin` / `padding` 尽量从尺度里取，不手填任意值。
  3. 组件对齐到 4px 或 8dp 的基线网格；图标/小元素可细到 4dp。
- **why**: 统一间距形成节奏，降低视觉噪音；Material Design 的 8dp 基线网格与 4dp 排印/图标网格、GitHub Primer 的 4px 网格都是同一思路。Refactoring UI 也强调用“加更多空间”替代随意堆边框。
- **boundary**: 4px 网格不是法律；极小元素或精细排版可能需要 2px；数据密集型/紧凑型界面可自定义更小尺度。如果间距尺度导致控件过小/不可点，以可用性优先。
- **source**: [Material Design Metrics & Keylines](https://m1.material.io/layout/metrics-keylines.html)；[GitHub Primer Typography](https://primer.github.io/design/foundations/typography/)；[Refactoring UI](https://refactoringui.com/)
- **grade**: `consensus`

### classic_04 · 控制正文行宽/行高以保持可读性

- **id**: `classic_04`
- **context**: 长篇正文每行太长或太短、行高太紧，用户阅读吃力。
- **trigger**: 正文每行字符数明显过多（约 >90 字符）；行高过紧（如 <1.3）；或长文本容器宽度拉满整个屏幕。
- **action**:
  1. 给正文容器设一个最大宽度，把 measure 控制在约 45–75 字符/行。
  2. 正文行高用无单位值并留足行距；常见基准：16px 正文配 24px 行高（1.5），19px 正文配 25px 行高。
  3. 避免正文用装饰字体或极细权重。
- **why**: Butterick 的 Practical Typography 强调 measure（行宽）对可读性的影响；Tailwind 与 GOV.UK 的默认字号/行高（16/24、19/25）是 UI 级常见落地，说明“正文可读性”是被多方采用的基准。
- **boundary**: 这是一条偏**排印学派**的规则，不是对每个界面都适用；中文/日文等书写的“字符”与拉丁字符不同，需要按语言调宽。数据表格、代码、短标签不受此限制；极宽屏幕下也要靠内容容器而不是全局 padding 解决。
- **source**: [Practical Typography: Line length](https://practicaltypography.com/line-length.html)（`pending`：公开在线书章节，沙箱连接超时未取到正文）；[Tailwind CSS: font-size](https://tailwindcss.com/docs/font-size)；[GOV.UK Design System: type-scale](https://design-system.service.gov.uk/styles/type-scale/)；[Practical Typography 首页](https://practicaltypography.com/)
- **grade**: `style`
- **grade_note**: 45–75 字符的 measure 主要是 Butterick / 古典排印流派的偏好，降权使用；16/24 行高的默认是多个设计系统的共识，但“必须多少字符”不应写成普适法律。

### classic_05 · 选择与内容气质匹配的字体（字体气质）

- **id**: `classic_05`
- **context**: 界面/产品的气质（可信、技术、友好、复古、可爱）与所用字体不匹配，或正文用了装饰性字体。
- **trigger**: 选字体时只凭个人喜好/当下流行；正文用华丽手写体、花体、极细体；把适用于 logo/标题的字体直接用于长文本。
- **action**:
  1. 先明确要表达的气质（如专业可信→经典衬线/稳健无衬线；现代科技→几何无衬线；友好→圆润无衬线）。
  2. 正文必选高可读性字体（避免装饰体、过细体、过花体）。
  3. 用 1–2 款字体 + 字号/字重/字距的变化来建立层级，而不是堆很多字体。
- **why**: Practical Typography 主张排版要有目的：字体的选择本身在表达气质；装饰字体适合标题/展示，不适合正文可读性。这个判断在经典排印学派中被反复强调。
- **boundary**: 这是**风格类**判断——不同品牌/流派有不同的“气质”答案，没有唯一正确。不能为了“气质”牺牲可读性；在工具型界面（数据表、后台）应优先可读性而非气质。作者/流派的审美偏好不应上升为普适规则。
- **source**: [Practical Typography](https://practicaltypography.com/)（`pending`：公开在线书，沙箱连接超时未取到正文，未列直接引文）
- **grade**: `style`
- **grade_note**: 只代表 Butterick 及传统书籍排印流派，属于风格偏好；如需上升为共识，应再找至少 2 个独立来源交叉验证。

### classic_06 · 不要只靠颜色传达状态/差异（警戒）

- **id**: `classic_06`
- **context**: 状态（错误/成功/选中）、链接、图表分类、表单校验只靠颜色区分。
- **trigger**: 除颜色外没有其他视觉线索；色盲或低视力用户看到两种颜色但无法区分含义。
- **action**:
  1. 为重要状态添加非颜色线索：图标 + 文字、形状/描边、图案、位置。
  2. 状态不只靠“红色/绿色”表达；错误信息同时给文字提示。
  3. 检查对比度：正文 ≥4.5:1，大文本/控件 ≥3:1。
- **why**: NN/g 的视觉无障碍文章明确“不要只依赖颜色”；GitHub Primer 设计系统也写明“Don't rely on color alone. Show state with more than color”。这是多来源一致的警戒。
- **boundary**: 不是禁用颜色，而是不要“只”用颜色。纯装饰性颜色可以自由用；在信息密度极低、且用户群体无视觉障碍风险时可放宽；但工具/表单/图表仍应保留非颜色线索。
- **source**: [NN/g: 5 Visual Treatments that Improve Accessibility](https://www.nngroup.com/articles/visual-treatments-accessibility/)；[GitHub Primer: Color accessibility](https://primer.github.io/design/foundations/color/accessibility/)
- **grade**: `warning`

### classic_07 · 让可点击元素保持可识别线索（感知 affordance）

- **id**: `classic_07`
- **context**: 扁平化/极简设计让按钮、链接、卡片看起来像普通文本或纯装饰，用户不知道哪里可点。
- **trigger**: 可点击元素与静态文本无法区分；没有 hover/focus 反馈；链接不像链接；按钮没有可感知的边界。
- **action**:
  1. 保留可点击线索：颜色（如链接色）、边框/底、大小、位置、一致性、遵循 web 惯例。
  2. 给可点击元素足够大的点击/触摸区域，并补上 focus 态。
  3. 静态内容不应长得像按钮；装饰元素不应抢可点击元素的风头。
- **why**: NN/g 的 clickable elements 文章指出“Signaling clickability with cues such as borders, color, size, consistency, placement, and adherence to web standards”；Don Norman 的 affordance / signifier 说明“看起来怎样，就是教用户怎么用。”
- **boundary**: 传统蓝色链接不是唯一形式，用户对线索的认知会随时代演化；但无论用哪种风格，可点击性必须能被一眼识别。极端扁平风可以保留线索，只是不能为了视觉简约删除所有线索。
- **source**: [NN/g: Beyond Blue Links: Making Clickable Elements Recognizable](https://www.nngroup.com/articles/clickable-elements/)；[The Design of Everyday Things](https://jnd.org/books/the-design-of-everyday-things-revised-and-expanded-edition/)（`pending`：书页 200，正文未取）
- **grade**: `consensus`

### classic_08 · 移除不必要的装饰/视觉噪音（少即是多）

- **id**: `classic_08`
- **context**: 界面装饰过多，边框、阴影、配色、装饰图标叠在一起，重点难找。
- **trigger**: 一个区域用了很多边框/分隔线；装饰元素与用户任务无关；所有元素都在“用力”。
- **action**:
  1. 删除不必要边框/分隔线/阴影；用留白、背景对比、空间来替代。
  2. 删掉不支持用户任务的元素或内容。
  3. 保留重点：用留白/对比/大小把最重要的元素顶出来。
- **why**: Refactoring UI 提供具体 tactic：“Use fewer borders… too many of them can make your design feel busy and cluttered. Instead, try adding a box shadow, using contrasting background colors, or simply adding more space between elements.” NN/g 对 112 个极简站的实证也总结“minimalist strategy 是删除不支持用户任务的元素”。
- **boundary**: “删”不等于“空”。过度极简会损害可发现性（flat design 的坑：用户找不到可点元素）；关键信息、必要分隔、无障碍线索不能删。极简是策略而非目的，目标是支持任务。
- **source**: [Refactoring UI](https://refactoringui.com/)；[NN/g: The Characteristics of Minimalism in Web Design](https://www.nngroup.com/articles/characteristics-minimalism/)；[NN/g: Flat Design](https://www.nngroup.com/articles/flat-design/)
- **grade**: `consensus`

### classic_09 · 内部保持一致，降低学习成本

- **id**: `classic_09`
- **context**: 同一类元素在不同页面/状态长得不一样，用户每次都在重新学习界面。
- **trigger**: 同一动作的按钮样式不一；同类信息呈现不一；命名/图标不一；同一模式在站内来回变化。
- **action**:
  1. 为控件、状态、命名、布局建立统一的模式并复用。
  2. 同一功能在应用内所有位置使用同一“长相”。
  3. 同时遵循平台/行业惯例（如链接、按钮、表单的通用形态）。
- **why**: 一致性是 Nielsen 十大可用性启发式之一（Consistency and standards）；Krug 的“不要让我思考”和 Tidwell 的交互模式都指向：熟悉模式能减少认知负担、提升可预期性。
- **boundary**: 一致性优于变化，但不是“绝对不变”；不同目标/受众可以有意义地分群。若为了统一而把可点击元素做成不可识别、或牺牲无障碍，那一致性就过度了。
- **source**: [NN/g: Maintain Consistency and Adhere to Standards](https://www.nngroup.com/articles/consistency-and-standards/)；[Don't Make Me Think](https://sensible.com/dont-make-me-think/)（`pending`）；[Designing Interfaces](https://www.oreilly.com/library/view/designing-interfaces-3rd/9781492051954/)（`pending`）
- **grade**: `consensus`

### classic_10 · 聚焦单一主要动作（一个屏幕一个主导 CTA）

- **id**: `classic_10`
- **context**: 一个页面同时出现多个同等强度的按钮/链接，用户犹豫或错过真正重要的动作。
- **trigger**: 多个 CTA 视觉权重相同；主按钮被次要按钮淹没；用户不知道“下一步该做什么”。
- **action**:
  1. 给最期望的用户动作最高的视觉权重（主按钮实心、更大、更高对比）。
  2. 次要动作降级：文字链接、幽灵按钮、弱化颜色。
  3. 一屏尽量只有一个主导动作；如果必须并列，用间距/分组让主次可见。
- **why**: 视觉层级的核心是“引导眼睛按重要性顺序看”；NN/g 的视觉层级文章强调要让最重要的元素获得最多注意。Refactoring UI 的 tactic 也通过“对比 + 留白”让主 CTA 跳出来。
- **boundary**: 不是只能有一个按钮。购物车/表单/工具栏常有多个**同等重要**的动作；如果两个动作确实同等重要，就不该硬突出其中一个。判断标准是“哪些动作是任务主线”，而不是“有几个按钮”。
- **source**: [NN/g: Visual Hierarchy in UX](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)；[Refactoring UI](https://refactoringui.com/)
- **grade**: `consensus`

## 3. 分级汇总表

| id | 标题 | grade |
|---|---|---|
| classic_01 | 用「尺度」建立视觉层级 | consensus |
| classic_02 | 用邻近性/留白分组 | consensus |
| classic_03 | 用统一的间距尺度 | consensus |
| classic_04 | 控制正文行宽/行高 | style |
| classic_05 | 选择与内容气质匹配的字体 | style |
| classic_06 | 不要只靠颜色传达状态 | warning |
| classic_07 | 让可点击元素保持可识别线索 | consensus |
| classic_08 | 移除不必要的装饰/视觉噪音 | consensus |
| classic_09 | 内部保持一致，降低学习成本 | consensus |
| classic_10 | 聚焦单一主要动作 | consensus |

### 分布统计

- 单元总数：10
- `consensus`：7
- `style`：2
- `warning`：1

> 说明：`style` 单元（classic_04 / classic_05）只代表 Butterick 与传统排印流派，已在 `grade_note` 中降权说明；要升级为共识需补充至少 2 个独立来源。
