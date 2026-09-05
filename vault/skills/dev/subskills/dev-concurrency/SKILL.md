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

## 2026 深度补强（Round 32）

> 本轮补强聚焦：原子内存序、异步阻塞隔离、锁内回调、死锁定位、条件变量、公平性、尾延迟测量与确定性并发验证；与上方已有规则不重复。

### 6. 原子性不是“自动正确”：必须选对内存序

- 单变量读-改-写用原子 RMW（`fetch_add`/`compare_exchange`）只保证原子；跨变量的“发布/确认/顺序”还要靠 acquire/release（或 seq_cst）配对。
- 反例：`std::atomic<bool> ready; ready.store(true, relaxed)` + 消费者 `if (ready.load(relaxed)) use(data)` —— 可能看到 `ready=true` 但 `data` 的写还未可见。
- 正确：发布侧 `data.store(42, release); ready.store(true, release);`，消费侧 `while(!ready.load(acquire)) {}`，再读 `data`。Go 中 `sync/atomic` 无 `relaxed`；Rust/C++ 必须显式选 `Ordering::Acquire/Release`，不要默认全 `Relaxed`。
- 来源：Go Memory Model、C++ memory_order、Rust std::sync::atomic。

### 7. 异步事件循环中禁止内联阻塞/CPU 重活

- 规则：async 函数内不得直接调用阻塞 IO 或大 CPU 段；用 `run_in_executor`/`to_thread`/`worker_threads`/进程池隔离，并用信号量限制并发。
- 反例：Node 事件循环里 `fs.readFileSync`/同步 JSON 大对象；Python asyncio 里 `requests.get`/`time.sleep`/大正则——都会冻结整个循环，把其他任务尾延迟拉到秒级。
- 正确：CPU 密集拆到 worker/子进程；阻塞 IO 走 executor；循环内只保留非阻塞 await。
- 来源：Node.js “Don’t Block the Event Loop”、Python asyncio Task/Executor。

### 8. 持有锁时禁止调用外部代码/回调

- 规则：临界区只做受保护数据的修改与快照；事件通知、用户回调、日志序列化、配置加载等移出锁外。
- 反例：`lock { flag = true; listeners.forEach(fn) }`——`fn` 可能反向拿锁（重入/锁序反转）或进入慢 IO；即使可重入锁也会造成不可预期的长持有。
- 正确：`lock { flag = true; snapshot = ...; }` 然后 `queue.put(event)` / 在锁外触发回调；回调本身按单线程/串行队列执行避免重入。
- 来源：Oracle Liveness、.NET Managed Threading Best Practices。

### 9. 死锁：全局锁序编号 + tryLock 超时回滚 + 线程转储定位

- 规则：给每个锁分配全局唯一序号，只按递增方向获取；需要“尝试”时用 `tryLock(timeout)`，失败则释放已持有锁、回退/退避后重试，不要原地无限循环。
- 反例：两个服务各自在回调里给对方对象加锁，静态看“都是 A→B”但运行时依赖反转；出现卡死只“重启”不抓现场。
- 正确：卡死时立即抓全量线程转储（`jstack`/`py-spy dump`/`gdb -p`/`kill -QUIT`），找循环等待关系，再改锁序或拆分回调。
- 来源：Oracle Liveness/Starvation & Livelock、Go Race Detector 的诊断思路。

### 10. 条件变量/等待：必须 while 重查谓词，防虚假唤醒与丢失唤醒

- 规则：`while (!pred(shared)) cv.wait(lock);`；谓词修改需在持锁内完成；`notify` 可在锁外（但需先有状态变更），避免 `if` 一次判断。
- 反例：`if (!ready) wait();` —— 虚假唤醒或另一线程先改状态后通知，导致醒来时谓词仍不满足，进入错误分支。
- 正确：把“等待条件”封装成 `wait_until(pred)`/`await_for` 谓词重载；Go 中 `sync.Cond` 同样要用 `for !cond { c.Wait() }`。
- 来源：C++ std::condition_variable。

### 11. 公平性/活跃性取舍：勿用无界重试与无界队列

- 规则：非公平锁通常吞吐高但可能饿写；若公平性重要，选 fair lock 或用 `tryLock`+有限退避；任何重试必须有上限与随机退避；有界队列+背压优先于无界队列。
- 反例：高竞争下“重试直到成功”会活锁；无界队列“吸收峰值”实际把内存压力和尾延迟转嫁给整个系统。
- 正确：队列满时降级/丢弃/返回 backpressure，不用无限排队；锁公平性按业务需求显式声明。
- 来源：Java ReentrantLock API、Oracle Starvation & Livelock。

### 12. 性能测量：并发伸缩曲线 + 尾延迟 + 队列深度

- 规则：基线至少测 1/2/4/8/...并发下的吞吐与 p50/p95/p99；画“线程数-吞吐”曲线；平台期即为串行瓶颈；同时记录队列长度/等待时间，别只看平均或 CPU。
- 反例：只优化平均延迟或只加线程数；p50 改善而 p99 因锁竞争/GC/排队恶化，在线服务体感仍是变慢。
- 正确：从曲线找“转折点”定位临界区；对在线系统引入 `The Tail at Scale` 式尾容忍（重试、备份请求、请求延迟上限），并防止虚假共享（缓存行填充/按核分片）。
- 来源：The Tail at Scale、LWN What every programmer should know about memory。

### 13. 并发验证：race detector + 确定性交错 + 多随机种子

- 规则：除 `go test -race`/TSAN/`jcstress` 外，还要人为制造交错：在临界区入口加短暂 sleep、用 barrier/phase 同步、固定不同随机种子跑 ≥3 轮；偶发 bug 要采集调度/转储复现。
- 反例：“review 没看到竞态”“压测跑过一次没复现”不能作为安全结论；竞态窗口平时可能极窄。
- 正确：把“并发压力测试”写进 CI，配 race detector，并对可疑锁序加静态检查/锁序编号校验。
- 来源：Go Race Detector 文、Go Memory Model 中 happens-before 验证思想。

## 来源

- [Go Blog: Race Detector](https://go.dev/blog/race-detector)
- [Go Blog: Share Memory By Communicating](https://go.dev/blog/codelab-share)
- [MDN: Concurrency in JavaScript / Worker](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Worker)
- [Java Concurrency Tutorial (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [Python docs: threading](https://docs.python.org/3/library/threading.html)
- [Rust docs: Send and Sync](https://doc.rust-lang.org/nomicon/send-and-sync.html)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/skill-verification-consensus/`
