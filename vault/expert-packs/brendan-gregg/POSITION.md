# 布伦丹·格雷格（Brendan Gregg，性能分析/火焰图） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

先方法后工具：用 USE/TSA/Off-CPU 等方法与检查表量化利用率、饱和度、错误与线程状态，用火焰图等可视化证明热点与延迟分布，以可观测性驱动优化，拒绝拍脑袋。

## 结构化条目（style_rules / style_items）

### 1. gregg-use-method

**Trigger**: 服务器/系统性能问题早期排查，或需要快速找到资源瓶颈和错误时

**Action**: 对每个资源（CPU、磁盘、总线、内存、网络等）检查 utilization、saturation、errors；先问‘哪个资源限制了系统’，再用对应工具回答；按检查表快速扫一遍，避免漏项。

**Boundary**: 作者称 USE 能解决约 80% 的服务器问题，不是万能；它面向资源视角，线程/等待问题需 TSA/off-CPU 等方法补充。

**SourceRefs**: https://www.brendangregg.com/usemethod.html; https://www.brendangregg.com/Articles/The_USE_Method.pdf

### 2. gregg-tsa-offcpu

**Trigger**: 性能问题不在 CPU 命中里，或线程在等待/阻塞（I/O、锁、定时器、分页、调度）时

**Action**: 用 TSA 方法测每个感兴趣线程的线程状态时间（Executing、Runnable、Anonymous Paging、Sleeping、Lock、Idle），按占比从大到小深入；用 Off-CPU Analysis 捕获阻塞等待的栈与请求上下文。

**Boundary**: 需要可用的栈回溯（帧指针/JIT 符号），否则火焰图/off-CPU 可能失真；采样/跟踪有开销，生产环境要控制；off-CPU 是 CPU 分析的补充而非替代。

**SourceRefs**: https://www.brendangregg.com/tsamethod.html; https://www.brendangregg.com/offcpuanalysis.html

### 3. gregg-flamegraphs

**Trigger**: 需要知道 CPU/off-CPU/内存热点、代码路径占比，或向团队解释性能证据时

**Action**: 生成对应类型的火焰图（CPU、Off-CPU、Memory、Differential 等）；用宽度识别高频路径，结合交互缩放/搜索；同时记录采样率、环境与用途。

**Boundary**: 火焰图 x 轴是样本占比/种群，不是时间；只反映可采样栈；单独一张火焰图不能替代完整方法（需结合 USE/TSA/负载）。

**SourceRefs**: https://www.brendangregg.com/flamegraphs.html

### 4. gregg-latency-tail

**Trigger**: 评估用户体验、SLO、容量，或‘系统不慢但偶尔卡’时

**Action**: 记录并查看延迟分布（直方图、p50/p95/p99/p999）而不是只看均值；把长尾/Dropout 当作独立问题；结合周期、扰动、事件（GC、锁、I/O）定位；按延迟目标而非吞吐讲故事。

**Boundary**: 吞吐高不等于延迟好；长尾需要足够样本和真实负载；延迟优化可能以吞吐为代价，要明确取舍。

**SourceRefs**: https://www.brendangregg.com/flamegraphs.html; https://www.brendangregg.com/offcpuanalysis.html; https://www.usenix.org/conference/srecon16/program/presentation/gregg

### 5. gregg-method-first

**Trigger**: 任何性能结论、评审、排障开始前

**Action**: 先用方法论（USE/TSA/off-CPU/active benchmarking、workload characterization）定义问题与检查表，再选择工具；把每个结论落到可复现指标与证据上；避免‘用一个工具扫一遍就下结论’。

**Boundary**: 方法不能替代领域判断；不同问题类型需要不同方法；工具选择由问题决定，不是反过来。

**SourceRefs**: https://www.brendangregg.com/usemethod.html; https://www.brendangregg.com/tsamethod.html; https://www.brendangregg.com/offcpuanalysis.html

**SourceRefs（专家总来源）**: https://www.brendangregg.com/usemethod.html; https://www.brendangregg.com/Articles/The_USE_Method.pdf; https://www.brendangregg.com/flamegraphs.html; https://www.brendangregg.com/tsamethod.html; https://www.brendangregg.com/offcpuanalysis.html; https://www.usenix.org/conference/srecon16/program/presentation/gregg
