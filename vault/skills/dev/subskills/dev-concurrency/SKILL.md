---
name: dev-concurrency
description: 并发调优子技能——共享状态/原子性、锁与并发原语、异步模型、死锁/活锁/饥饿、并发性能测量的可执行检查清单；先测再优化。
whenToUse: 用户处理多线程、异步、锁、竞态、死锁、队列或并行性能时；需要判断并发方案与并发 bug 时。
---

# dev-concurrency · 并发调优（已蒸馏）

> 定位：把“并发正确性”与“并发性能”分开。先证明没有竞态，再谈快不快。
> 核心原则：**共享可变状态最小化；锁要短且有序；永远用可复现的并发压力测试验证。**

## 触发条件

- 用户要写/审多线程、多进程、异步/协程、事件循环、锁、队列、并发任务。
- 遇到偶发 crash、数据错乱、死锁、卡死、资源耗尽。
- 需要判断“这个并发方案是否安全 / 性能是否值得”。

## 核心动作

### 1. 共享状态与原子性

- 优先减少共享可变状态：不可变对象、消息传递、每线程/每请求隔离。
- 读-改-写必须原子：用原子类型/原子操作或锁；不要在检查后再操作（TOCTOU）。
- 集合/缓存共享时，用线程安全容器或加锁；迭代期间不能裸修改。
- 使用正式的内存模型/同步原语，不用“巧合安全”的近似。

> 边界：并发 bug 常常只在特定调度/负载下出现，代码 review 不够，必须跑 race detector / 并发压力。

### 2. 锁与并发原语选择

- 锁粒度：保护什么数据就锁什么；不要用大锁包全场。
- 锁顺序：多个锁必须全库统一顺序；否则死锁风险。
- 短临界区：不在锁内做 IO、网络、用户代码（可能重入/慢）。
- 优先用语言提供的原语：互斥锁、读写锁、信号量、无锁队列；自己实现 spin lock 要非常谨慎。
- 无锁/原子只适合单变量；多变量一致性仍需要锁或事务。

> 边界：“用锁就行”不是结论；要说明锁的粒度、顺序、持有时间与公平性。

### 3. 异步模型

- 异步不等于并发安全；事件循环中不要阻塞线程，也不要让共享状态被并发修改。
- 回调地狱用 async/await 或 promise/协程表达顺序依赖；错误处理必须盖到每个 await/链尾。
- 异步任务注意取消、超时、重试与资源释放；不要创建无限任务。
- 共享内存的异步多线程仍要同步；单线程事件循环中也要防重入。

> 边界：不同语言（Go goroutine / JS event loop / Python asyncio / Rust tokio）模型不同，规则要按模型落地，不泛泛而谈。

### 4. 死锁、活锁与饥饿

- 死锁检测：锁顺序图 + 超时 + 工具；不要只靠“多试几次”。
- 活锁/饥饿：重试要有退避与上限；公平锁考虑等待队列。
- 资源池（线程池/连接池）要设上限与排队策略，防止资源耗尽导致级联失败。
- 有超时的地方要处理超时后的清理，不能留下半完成状态。

### 5. 并发性能测量

- **先测再优化**：记录基线（吞吐、延迟、CPU/内存、资源上限），再改。
- 压力测试必须可复现：固定并发数、数据规模、持续时间、随机种子；至少 3 次。
- 用 profiler / race detector / 调度器跟踪定位热点与虚假共享。
- 优化要以可观测指标为证：延迟分位（p50/p95/p99）、吞吐、错误率；不要只看 CPU。

> 边界：并发优化很容易把正确性改坏；每步优化要有测试把关，且要保留回退点。

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “加个锁就安全了” | 说明锁的粒度/顺序/持有时间；用 race detector 验证 |
| “用多线程就一定快” | 先测串行基线；线程开销/锁竞争可能更慢 |
| “死锁重启就好了” | 重现实例 + 锁顺序分析；用超时/检测 |
| “异步就不会阻塞” | 异步也可能因 CPU/IO 调度和锁竞争而阻塞 |
| “并发测试过了就稳” | 至少 3 次 + 不同负载/种子，并跑 race detector |

## 来源

- [Go Blog: Race Detector](https://go.dev/blog/race-detector)
- [Go Blog: Share Memory By Communicating](https://go.dev/blog/codelab-share)
- [MDN: Concurrency in JavaScript / Worker](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Worker)
- [Java Concurrency Tutorial (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [Python docs: threading](https://docs.python.org/3/library/threading.html)
- [Rust docs: Send and Sync](https://doc.rust-lang.org/nomicon/send-and-sync.html)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`
