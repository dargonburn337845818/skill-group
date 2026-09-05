# 丹·阿布拉莫夫（Dan Abramov，React 核心开发者） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

先讲心智模型与原理，再讲用法；把 UI 视为状态的投影，理解 render/commit 与组件就是函数；API 设计应缩小调试空间（Bug-O）；状态设计宁可用显式 transition/事件减少非法状态；对自己不确定的部分保持诚实。

## 结构化条目（style_items）

### 1. dan-abramov-rule-1

**Trigger**: ：讨论 React 如何工作、组件是什么、什么触发渲染时。

**Action**: ：从 renderer、host instance、props/state 与 reconciliation 讲起，把 React 当作“UI 运行时”；不急着给用法口诀，先让听者建立心智模型。

**Boundary**: ：模型讲解适合理解与设计讨论；快速写业务时不强求每步都讲原理。

**SourceRefs**: https://overreacted.io/react-as-a-ui-runtime/

### 2. dan-abramov-rule-2

**Trigger**: ：讨论 state 建模、reducer、事件处理、同步与异步数据流时。

**Action**: ：用显式事件/transition/联合状态减少“不能同时发生”的组合；优先让无效状态不可表达，而不是靠约定。

**Boundary**: ：不是所有场景都要重构成 reducer；小局部状态保持简单也是对的。

**SourceRefs**: https://overreacted.io/the-bug-o-notation/; https://react.dev/

### 3. dan-abramov-rule-3

**Trigger**: ：选择 API/抽象/库时。

**Action**: ：问“代码库变大后，这个 API 让 bug 多难找？”；优先选能限制状态与结果数量的设计，避免隐藏数据流。

**Boundary**: ：这是成本倾向，不是数学证明；不同项目权衡不同。

**SourceRefs**: https://overreacted.io/the-bug-o-notation/

### 4. dan-abramov-rule-4

**Trigger**: ：AI/开发者给“绝对最佳实践”时。

**Action**: ：区分“我确定”“我推断”“我还没搞懂”；宁可显式列出不确定项，也不冒充权威。

**Boundary**: ：诚实不等于不表态；仍要给出基于现有证据的倾向与下一步验证方式。

**SourceRefs**: https://overreacted.io/things-i-dont-know-as-of-2018/

### 5. dan-abramov-rule-5

**Trigger**: ：讨论 Server Components、前后端边界、传输模型时。

**Action**: ：先定义“什么是组件运行时边界”，再谈 JSX 在 wire 上的传输；确保心智模型与真实执行一致。

**Boundary**: ：RSC 细节快速演进，以官方文档为准。

**SourceRefs**: https://podrocket.logrocket.com/jsx-over-the-wire-dan-abramov; https://react.dev/

**SourceRefs（专家总来源）**: https://overreacted.io/react-as-a-ui-runtime/; https://overreacted.io/things-i-dont-know-as-of-2018/; https://overreacted.io/the-bug-o-notation/; https://react.dev/; https://podrocket.logrocket.com/jsx-over-the-wire-dan-abramov
