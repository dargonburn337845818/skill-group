# Sources（dev-design-aesthetics）

> 来源台账。内部路径/本地文件按工作区约定解析；公开链接可在浏览器复核。

## 清单
- $PROJECT_ROOT/vault/skills/distillation/ui-aesthetics-design/
- $PROJECT_ROOT/vault/skills/base/search-source/
- $PROJECT_ROOT/vault/skills/core-iteration/skill-verification-consensus/
- $PROJECT_ROOT/vault/skills/core-iteration/dev-workflow-consensus/

## 分级说明
- 本 skill 的核心规则在 `SKILL.md` 中带 `source_refs` 或来源章节；未标注来源的观点应视为待证。
- 单源结论不作为核心规则；冲突分支保留而非合并。

## Round 36 新增来源

> 本轮于 2026-09-05 通过直接抓取/核验加入；服务 `SKILL.md` 中「2026 深度补强（Round 36）」的 R36-1～R36-7。
> 核验方式：HTTP 200 + 页面正文/元数据提取；Apple HIG 与 Material Design 3 为首方页面（正文 JS 渲染），其具体动作经 NN/g 研究文章交叉核验后纳入规则。
> 可信度沿用既有分级：`official` / `research` / `third-party`。

### 官方标准与设计系统（official）

| 来源 | URL | 用途 / 贡献点 | 可信度 |
|---|---|---|---|
| Apple HIG · Dark Mode | https://developer.apple.com/design/human-interface-guidelines/dark-mode | 暗色模式官方入口：系统级暗色调色板、低光环境适配；正文 JS 渲染，具体条款经 NN/g 研究交叉核验 | 官方一手（入口），多源交叉 |
| Apple HIG · Motion | https://developer.apple.com/design/human-interface-guidelines/motion | 动效官方入口：动效用反馈/状态迁移/空间隐喻；正文 JS 渲染，具体意涵经 NN/g 研究交叉核验 | 官方一手（入口），多源交叉 |
| Material Design 3 · Motion overview | https://m3.material.io/styles/motion/overview | 动效系统官方入口：motion 表达力、可用性平衡、动效语言；正文 JS 渲染，经 NN/g 研究交叉核验 | 官方一手（入口），多源交叉 |

### 一手研究（research）

| 来源 | URL | 用途 / 贡献点 | 可信度 |
|---|---|---|---|
| NN/g · Data Tables: Four Major User Tasks | https://www.nngroup.com/articles/data-tables/ | 表格四任务：找记录/比较/单行编辑/操作；人类可读首列、列序、冻结头/首列、斑马纹/hover、隐藏列状态 | 一手研究，已抓取 |
| NN/g · Dashboards: Making Charts and Graphs Easier to Understand | https://www.nngroup.com/articles/dashboards-preattentive/ | 仪表盘定义、操作型 vs 分析型、preattentive 编码、长度/二维位置优先、颜色/形状/分组辅助 | 一手研究，已抓取 |
| NN/g · Dark Mode: How Users Think About It and Issues to Avoid | https://www.nngroup.com/articles/dark-mode-users-issues/ | 暗色动机/预期/优先级；高饱和色暗底发糊、细灰线与卡片失效、浮动组件消失、渠道不一致、扫描码反色、镜像系统、透明度文字、邮件单测 | 一手研究，已抓取 |
| NN/g · Dark Mode vs. Light Mode: Which Is Better? | https://www.nngroup.com/articles/dark-mode/ | 正/负对比极性、亮环境与暗环境感知差异、长文阅读与视力受损者的不同需求；用于暗色优先级判断 | 一手研究，已抓取 |
| NN/g · The Role of Animation and Motion in UX | https://www.nngroup.com/articles/animation-purpose-ux/ | 动效目的分类：反馈/状态变化/空间隐喻/signifier；短、轻、不抢焦点；多动画竞争注意；时间填充动画的反例 | 一手研究，已抓取 |
| NN/g · Design Systems vs. Style Guides | https://www.nngroup.com/articles/design-systems-vs-style-guides/ | 设计系统/风格指南父子关系；组件复用、减少重复变体、品牌指南要素（可访问色组合/字体/logo/图片风格） | 一手研究，已抓取 |
| NN/g · Brand Is Experience in the Digital Age | https://www.nngroup.com/articles/brand-experience-ux/ | 品牌=可视+语气+行为三通道；品牌不是 logo 或口号；UX 是品牌差异化因素 | 一手研究，已抓取 |
| NN/g · The Impact of Interaction Design on Brand Perception | https://www.nngroup.com/articles/interaction-branding/ | 交互设计（标签、预期行为、一致性）直接影响用户对品牌的情绪与感知；行为一致带来真诚/胜任感 | 一手研究，已抓取 |

### 本轮核验备注
- Apple HIG / Material Design 3 页面为 JS 渲染，未能在静态抓取中取到全量正文；本包不把它们当成“数值规则”的唯一来源，仅作为官方入口与交叉参考，量化建议仍以 NN/g 一手研究与 WCAG 为准。
- 所有 URL 本轮均返回 HTTP 200；未加入未经访问的来源。
