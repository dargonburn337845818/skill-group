# Sources（dev-concurrency）

> 来源台账。内部路径/本地文件按工作区约定解析；公开链接可在浏览器复核。

## 清单
- https://go.dev/blog/race-detector
- https://go.dev/blog/codelab-share
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Worker
- https://docs.oracle.com/javase/tutorial/essential/concurrency/
- https://docs.python.org/3/library/threading.html
- https://doc.rust-lang.org/nomicon/send-and-sync.html
- $PROJECT_ROOT/vault/skills/base/search-source/
- $PROJECT_ROOT/vault/skills/core-iteration/skill-verification-consensus/
- $PROJECT_ROOT/vault/skills/core-iteration/dev-workflow-consensus/

## 分级说明
- 本 skill 的核心规则在 `SKILL.md` 中带 `source_refs` 或来源章节；未标注来源的观点应视为待证。
- 单源结论不作为核心规则；冲突分支保留而非合并。

## Round 32 新增来源
- https://go.dev/ref/mem
- https://en.cppreference.com/w/cpp/atomic/memory_order.html
- https://doc.rust-lang.org/std/sync/atomic/index.html
- https://docs.python.org/3/library/asyncio-task.html
- https://nodejs.org/learn/asynchronous-work/dont-block-the-event-loop
- https://learn.microsoft.com/en-us/dotnet/standard/threading/managed-threading-best-practices
- https://docs.oracle.com/javase/tutorial/essential/concurrency/liveness.html
- https://docs.oracle.com/javase/tutorial/essential/concurrency/starvelive.html
- https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/locks/ReentrantLock.html
- https://en.cppreference.com/w/cpp/thread/condition_variable.html
- https://research.google/pubs/the-tail-at-scale/
- https://lwn.net/Articles/250967/

> 说明：本轮来源覆盖原子内存序（Go/C++/Rust）、异步阻塞隔离（Python/Node）、锁的活跃性与回调风险（Java/.NET）、条件变量谓词（C++/Java）、尾延迟与缓存/虚假共享（Google/LWN）。均不与原清单重复。

