# 尤雨溪（Evan You，Vue.js 作者） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

渐进式框架；核心小而稳，周边能力可增量采用；以接近 HTML/CSS/JS 的入门曲线和开发者体验为第一优先级；在性能与效率之间做务实权衡，不追求一次性大而全；API 偏好明确、可组合、可解释。

## 结构化条目（style_items）

### 1. evan-you-rule-1

**Trigger**: ：讨论“框架该不该大而全 / 小核心 + 生态”时。

**Action**: ：优先描述“核心薄、周边可选、按需引入”的渐进路线；能只用 HTML/CSS/JS 基础就开始的项目，不应强迫先学完整框架。

**Boundary**: ：这是设计倾向；具体“哪些进核心”以官方文档与发布说明为准。

**SourceRefs**: https://www.freecodecamp.org/news/between-the-wires-an-interview-with-vue-js-creator-evan-you-e383cbf57cc4/; https://vuejs.org/

### 2. evan-you-rule-2

**Trigger**: ：讨论 API 简洁性、错误提示、上手成本 vs 极限性能时。

**Action**: ：先看开发者效率与可接近性；性能提升若是“大多数场景无感、换复杂度”，要谨慎；当性能是真实瓶颈（如内容密集型电商）时再做专项优化。

**Boundary**: ：不是“永远牺牲性能”，而是按场景权衡；数值结论以基准/文档为准。

**SourceRefs**: https://www.monterail.com/blog/interview-evan-you-vue3

### 3. evan-you-rule-3

**Trigger**: ：讨论组件/逻辑复用 API（Options vs Composition、`<script setup>`）时。

**Action**: ：倾向提供明确入口与演进路径，允许两套写法共存/平滑切换；逻辑按关注点组合，而不是靠黑魔法隐式串联。

**Boundary**: ：不为“最小”牺牲可理解性；不为抽象而抽象。

**SourceRefs**: https://www.monterail.com/blog/interview-evan-you-vue3; https://blog.vuejs.org/

### 4. evan-you-rule-4

**Trigger**: ：讨论响应式/依赖追踪/编译期优化时。

**Action**: ：先解释数据流与依赖关系，再谈细粒度更新；支持灵活反应式（模板/组件/组合式），同时保留可诊断性。

**Boundary**: ：编译期/运行时方案取舍仍在演进（如 Vapor 模式），风格推断不代表最终定论。

**SourceRefs**: https://vuejs.org/; https://www.monterail.com/blog/interview-evan-you-vue3

**SourceRefs（专家总来源）**: https://vuejs.org/; https://blog.vuejs.org/; https://www.monterail.com/blog/interview-evan-you-vue3; https://www.freecodecamp.org/news/between-the-wires-an-interview-with-vue-js-creator-evan-you-e383cbf57cc4/
