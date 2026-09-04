---
name: dev-performance
description: 性能优化子技能——测量与基线、热点定位、网络/渲染/内存/数据库优化优先级、缓存边界与性能回归的可执行检查清单；先测量再优化。
whenToUse: 用户遇到响应慢、卡顿、内存高、包体大、数据库慢查询、加载延迟时；需要判断性能问题与优化优先级时。
---

# dev-performance · 性能优化（已蒸馏）

> 定位：性能问题的第一原则是**测量**。没有基线就没有优化，没有可复现用例就没有结论。
> 本子技能提供定位-分类-优先级-回归的通用方法。

## 触发条件

- 用户说“很卡 / 很慢 / 内存高 / 包大 / 数据库慢”。
- 需要做性能优化、性能评审、性能回归测试。
- 需要判断“这个性能优化值不值得做”。

## 核心动作

### 1. 建立测量与基线

- 定义指标：延迟（p50/p95/p99）、吞吐（QPS/RPS）、内存/CPU、包体、加载时间、错误率。
- 在**真实环境或可复现测试环境**采集基线；记录机器/数据规模/版本。
- 用 profiler（CPU、内存、网络、渲染）而不是猜热点。
- 优化前后同环境、同负载对比，至少 3 次。

> 边界：开发机上的秒级优化不等于生产提升；网络/DB 等外部因素必须纳入。

### 2. 热点定位与瓶颈分类

- 按“从用户到系统”分层：客户端渲染 → 网络 → 服务端 CPU/IO → 数据库/缓存 → 第三方。
- 先找数量级最大的项：一个慢 SQL 或大图/大 bundle 通常比循环微优化有效得多。
- 用火焰图/调用链/性能面板看耗时分布，而不是凭代码直觉。
- 数据库慢查询看执行计划、索引、N+1；接口慢看是否存在串行等待。

### 3. 优化优先级

- 网络与加载：压缩、HTTP/2、缓存、CDN、懒加载、关键路径优化。
- 渲染：减少重排/重绘、避免大列表全量渲染、虚拟化、减少 JS 主线程长任务。
- 内存：找泄漏（长生命周期引用、未清理定时器/监听）、减少大对象复制，防止 GC 抖动。
- 服务端：缓存热数据、异步/批处理、连接池、减少锁竞争。
- 包体：tree-shaking、代码分割、按需加载、移除重复依赖。

> 边界：优化按“可观测影响”排序，不做无证据的微优化；不要牺牲接口/可维护性除非有明确数据。

### 4. 缓存与预计算的适用边界

- 缓存用于读多写少、可容忍一定过期、可失效的数据。
- 必须设计缓存键、TTL、失效/淘汰策略；防止缓存雪崩/穿透。
- 预计算适合低频变但高频算的场景；要给出更新路径与一致性边界。
- “加缓存”不是万能：写放大、内存成本、一致性风险都要评估。

> 边界：金融/强一致场景不能无脑缓存；用缓存前明确数据一致性要求。

### 5. 性能回归落地

- 将关键指标做成自动化测试/基准，设阈值；跑不动就不算完整。
- 优化提交附上优化前后对比数据（baseline/after），并保留可复现脚本。
- CI 中放轻量性能冒烟（如 bundle 大小、关键接口延迟），重基准跑在独立环境。

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “先改成多线程再说” | 先测热点；若是 IO 等待，多线程也许有效；若是 CPU 瓶颈，多线程未必 |
| “把循环里的 if 优化一下” | 先看 profiler；局部微优化通常占比很小 |
| “直接加缓存” | 明确读多写少、TTL、失效，并评估一致性成本 |
| “优化完跑一次就宣布提升” | 至少 3 次，同环境同负载，报告 p95 等指标 |
| “只看 CPU 高不高” | 延迟/吞吐/错误率/内存都要看 |

## 来源

- [web.dev: Learn Performance](https://web.dev/learn/performance/)
- [MDN: Performance API](https://developer.mozilla.org/en-US/docs/Web/API/Performance)
- [Chrome DevTools Performance Reference](https://developer.chrome.com/docs/devtools/performance/reference)
- [PostgreSQL Docs: EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [High Performance Browser Networking](https://hpbn.co/)
- [Google SRE Workbook: Monitoring / Distributed systems](https://sre.google/workbook/)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`
