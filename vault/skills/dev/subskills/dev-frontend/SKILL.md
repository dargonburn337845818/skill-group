---
name: dev-frontend
description: 前端开发子技能——组件边界、状态管理、样式/响应式、可访问性与前端工程化的可执行检查清单；来源以官方文档与标准为主。
whenToUse: 用户写/改前端页面、组件、交互、状态管理、样式、可访问性或前端工程化时；需要快速判断“这条前端做法对不对/该怎么做”时。
---

# dev-frontend · 前端开发（已蒸馏）

> 定位：给 dev 模块提供“前端工程判断”的最小可执行集，不重复 UI 美学（归 dev-design-aesthetics）。
> 每条规则尽量可检查、可证伪，并给出适用边界。

## 触发条件

- 用户要写/改 React/Vue/原生 Web 组件、页面、路由、状态管理、样式、响应式或构建配置。
- 需要审查现有前端代码：组件划分是否合理、状态放哪、可访问性是否达标、性能初筛怎么做。
- 用户问“这个前端方案有没有坑 / 符不符合规范 / 下一步怎么改”。

## 核心动作

### 1. 组件边界

- **公开接口最小化**：组件对外 props 尽量少；能用派生数据就不要新增 prop；避免“透传一堆输入”的上帝组件。
- **组件职责单一**：一个组件只负责一件事；展示、容器、逻辑分层清晰，但不为了分层而分层。
- **状态归属**：只在一个地方持有状态；父组件发事件、子组件回调，不绕路改兄弟状态。
- **可测性**：组件通过公开 props/events 可被测试；不依赖私有 DOM 或内部实现来验证行为。

> 边界：这些是工程实践而非语言铁律；小型一次性页面不必套用复杂组件架构。

### 2. 状态管理与数据流

- 全局状态只在“真正跨组件/跨页面共享”时引入；本地状态留在就近组件。
- 更新状态优先使用不可变更新；避免直接 mutate props/state。
- 异步数据要有 loading / error / empty 三态，不能只写成功路径。
- 避免在 render 中做副作用；副作用放事件、effect 或显式生命周期。

> 边界：框架细节（React hooks / Vue reactive / Svelte stores）是风格分支，不在此处定死；关键是“数据流向单一、可追踪”。

### 3. 样式与响应式

- 用统一 design token（间距 4/8/12/16/24/32、字号、色板），不散落魔法值。
- 移动优先或至少明确断点；布局用 flex/grid/container query 等现代手段，避免 `<table>` 布局。
- 文本不写死 px 且可缩放；触控目标建议 ≥44×44px（平台相关，非通用硬标准）。
- 暗色模式不能只反转颜色，要重新检查对比度与强调色语义。

> 边界：品牌强风格可以打破间距规范，但必须作为“风格分支”显式声明，不能假装普适。

### 4. 可访问性（前端硬门槛）

- 所有交互元素可用键盘到达并可见焦点。
- 非文本内容必须有替代文本；图标按钮必须有 `aria-label`。
- 表单控件关联 label；错误提示不只靠颜色，还要文字/图标。
- 颜色对比正文 ≥4.5:1、大文本/图形 ≥3:1（WCAG 2.2 AA）。
- 动效尊重 `prefers-reduced-motion`；不要用闪烁内容。

> 边界：在内部工具或受控演示中可降级，但公开页面/产品页按 WCAG 执行。

### 5. 前端工程化与错误处理

- 构建/类型检查/测试作为本地命令写进 README，CI 同一条命令。
- 错误边界/错误处理覆盖运行时错误，不让白屏。
- 性能初筛：关键渲染路径、图片体积、JS 体积；先测量再优化。
- 敏感信息（token、key）绝不进前端包；环境变量只放非机密配置。

> 边界：性能与安全细节分别交给 dev-performance / dev-security；本子技能只负责“前端工程第一道闸”。

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “组件越拆越多就是好” | 拆到公开接口最小、无明显重复；不确定时先用 Deletion Test |
| “状态全部放全局 store” | 只有跨组件共享才放全局；局部状态留在组件 |
| “用 `!important` 快速覆盖” | 先查选择器优先级与 token；`!important` 只用于无法避免的第三方覆盖 |
| “只测组件内部实现” | 测试公开 props/events/渲染结果，不锁私有实现 |
| “页面能用就行，不管键盘” | 键盘可达 + 可见焦点是基本可用性，不是加分项 |
| “用 div 模拟按钮” | 原生 button 自带键盘/焦点/语义；非要自定义则补全 keyboard 行为 |

## 2026 深度补强（Round 32）

> 本轮不替代 1–5 节；补强重点是“可执行检查 + 反例”，并新增独立来源台账（见 `SOURCES.md` 的 Round 32 新增来源）。

### 6. 组件边界：组合优先于布尔旗标

- 可执行：当组件开始出现 `variant`/`size`/`mode`/`showX` 等并行开关，或一个展示形态需要改组件内部多处 if/switch 时，先拆子组件并用 `children`/slot/命名插槽组合；不要继续堆 prop。
- 检查：新增形态只需在调用方组合既有子组件就完成 → 边界健康；必须改组件内部渲染分支 → 边界已破，抽出去。
- 反例：`<Card showHeader showFooter isEditable isCollapsible>` 无法预知组合效果；正确：`<Card><CardHeader .../><CardBody>…</CardBody><CardFooter .../></Card>`。
- 来源：Vue Slots、React Docs Thinking in React（已有，组件边界）。

### 7. 状态管理：渲染期派生，不用 effect 同步 state

- 可执行：能从 props/现有 state 计算得到的值，在 render 顶部计算或记忆化；不要把“过滤、排序、格式化结果”同步进另一个 state。
- 反例：`useEffect(() => setFiltered(list.filter(...)), [list])` 会多一次整树渲染；正确：`const filtered = useMemo(() => list.filter(...), [list])`。
- 来源：React Docs You Might Not Need an Effect、Keeping Components Pure。

### 8. 状态管理：服务端状态走缓存协议，不复制进本地 state

- 可执行：服务端数据用 TanStack Query/SWR/Apollo 等查询缓存；更新/失效用 `invalidateQueries`/refetch；不要复制到 `useState` 后手工同步。
- 反例：把 API 响应放进组件 state，另一个组件改了数据后原组件 stale；或者每个页面重复请求同一接口。
- 来源：TanStack Query React Overview。

### 9. 可访问性：弹层必须管焦点，关闭后还焦点

- 可执行：模态 dialog 打开时焦点进入弹层并 trap；关闭/ESC 后焦点回到触发元素；优先原生 `<dialog>` 或 ARIA APG 对话框模式；背景不能只 `aria-hidden` 而不管焦点。
- 反例：点“关闭”后焦点掉到 body，Tab 进入不可见区域；或只给遮罩设 `aria-hidden`，屏幕阅读器仍能读到背景内容。
- 来源：WAI ARIA APG、MDN dialog role。

### 10. 可访问性：语义优先，自动化 a11y 进 CI

- 可执行：能用原生 HTML 就用原生（`button`/`nav`/`main`/`label`），ARIA 只补缺失语义；CI 跑 axe/Lighthouse/Playwright accessibility，把已知违规当门禁。
- 反例：给 div 加 `role="button"` 却不实现键盘/焦点；到处用 `aria-label` 覆盖可见文本/占位符当 label。
- 来源：WAI ARIA APG、Playwright Accessibility Testing。

### 11. 性能：先防 CLS/INP，再谈微优化

- 可执行：图片/视频标注 `width`/`height` 或 `aspect-ratio`；字体用 `font-display: swap` 并必要时 preload；长列表用虚拟化或 `content-visibility: auto` + `contain-intrinsic-size` 预留尺寸；LCP 图用 `fetchpriority="high"`/preload，非首屏图懒加载。
- 反例：不设尺寸的图片让首屏跳动；首屏一次渲染 1000 行导致 INP 卡顿；字体 FOIT 白屏。
- 来源：MDN content-visibility、web.dev Learn Performance（已有）。

### 12. 安全：默认转义 + 白名单 sanitize + CSP + 外链防反向 tabnabbing

- 可执行：用户内容默认文本转义，富文本用 DOMPurify 等白名单 sanitize；配置 CSP（`default-src 'self'`，避免 `unsafe-inline`/`unsafe-eval`）；`target="_blank"` 必须带 `rel="noopener noreferrer"`；`window.open`/redirect 的 URL 协议必须白名单；依赖漏洞用 `npm audit`/`pnpm audit` 入 CI。
- 反例：`v-html`/`dangerouslySetInnerHTML` 直渲染接口 HTML；CSP 开后门 `unsafe-inline` 又依赖它防 XSS；把 access token 放 `localStorage` 且无 CSP/转义。
- 来源：OWASP XSS Prevention、OWASP CSP Cheat Sheet、MDN rel=noopener。

### 13. 测试：以用户可见行为为准，并覆盖错误/空/加载态

- 可执行：查询用 `getByRole`/`getByLabelText`/`getByText` 等用户可见方式；`getByTestId` 只在非语义元素无其他查询方式时作最后手段；每个核心组件至少覆盖正常/空/加载/错误 + 键盘操作；核心用户流用 Playwright e2e，并把 a11y 自动化纳入同一流水线。
- 反例：断言组件私有 state、mock 子组件实现、用 class/样式断言；只测 happy path，错误态留到线上。
- 来源：Testing Library Guiding Principles、Playwright Accessibility Testing。

## 来源

- [MDN Web Docs: Web 开发入门/标准](https://developer.mozilla.org/)
- [React Docs: Thinking in React / Managing State](https://react.dev/learn/managing-state)
- [Vue Docs: Reactivity Fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)
- [WCAG 2.2 Understanding Docs](https://www.w3.org/WAI/WCAG22/Understanding/)
- [web.dev: Learn Accessibility](https://web.dev/learn/accessibility/)
- [web.dev: Learn Performance](https://web.dev/learn/performance/)
- [MDN: CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/dev-workflow-consensus/`
