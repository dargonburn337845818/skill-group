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

## 来源

- [MDN Web Docs: Web 开发入门/标准](https://developer.mozilla.org/)
- [React Docs: Thinking in React / Managing State](https://react.dev/learn/managing-state)
- [Vue Docs: Reactivity Fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)
- [WCAG 2.2 Understanding Docs](https://www.w3.org/WAI/WCAG22/Understanding/)
- [web.dev: Learn Accessibility](https://web.dev/learn/accessibility/)
- [web.dev: Learn Performance](https://web.dev/learn/performance/)
- [MDN: CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/dev-workflow-consensus/`
