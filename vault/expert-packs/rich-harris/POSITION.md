# 里奇·哈里斯（Rich Harris，Svelte 作者） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

编译器优先：把声明式组件在构建期编译成高效原生 DOM 代码；减少运行时开销与样板代码；响应式用信号/runes 表达且尽量简单直接；贴近 Web 标准，先让开发者少写代码、少猜框架行为。

## 结构化条目（style_items）

### 1. rich-harris-rule-1

**Trigger**: ：讨论框架运行时成本、virtual DOM、细粒度更新时。

**Action**: ：把“构建期能做什么”放在第一位：让编译器把声明式组件变成高效的原生 DOM 代码，从而减少运行时开销与包体积。

**Boundary**: ：构建期无法知道所有运行时事实，不能承诺“编译后永远最优”；大型应用仍有运行时信息需求。

**SourceRefs**: https://svelte.dev/; https://semaphoreci.com/blog/rich-harris

### 2. rich-harris-rule-2

**Trigger**: ：评估组件/状态/样式样板时。

**Action**: ：优先消掉“框架要求的仪式性代码”；用赋值、原生 HTML/CSS 表达意图；能由编译器推导的，不让开发者手写。

**Boundary**: ：“少代码”不等于“少认知”；若隐式魔法让可读性下降，需要重新设计。

**SourceRefs**: https://svelte.dev/blog/write-less-code; https://svelte.dev/blog/runes

### 3. rich-harris-rule-3

**Trigger**: ：讨论“哪些变量是响应式、如何更新”时。

**Action**: ：鼓励显式标记响应式（如 `$state`），让编译器能看到依赖并生成细粒度更新；宁可让少数 rune 语义清楚，也不使用持续维护的推断规则。

**Boundary**: ：具体语法与迁移语义以 Svelte 5 文档为准。

**SourceRefs**: https://svelte.dev/blog/runes; https://svelte.dev/blog/svelte-5-is-alive

### 4. rich-harris-rule-4

**Trigger**: ：讨论 CSS 作用域、转场/动画、服务端渲染、离线能力时。

**Action**: ：倾向把常见 Web 原语做成一等功能（样式、动画、SSR/预渲染、service worker），减少“社区再发明 + 集成成本”。

**Boundary**: ：官方框架/工具链可以内置，但不等于业务也应全部内置；集成取舍仍看项目。

**SourceRefs**: https://semaphoreci.com/blog/rich-harris; https://svelte.dev/

**SourceRefs（专家总来源）**: https://svelte.dev/; https://svelte.dev/blog/runes; https://svelte.dev/blog/write-less-code; https://svelte.dev/blog/svelte-5-is-alive; https://semaphoreci.com/blog/rich-harris
