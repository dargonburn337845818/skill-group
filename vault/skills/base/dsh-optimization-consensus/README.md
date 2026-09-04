# DSH 优化共识（工作区版）

这个目录是从 DeepSeek Harness 官方源码/文档/Agent Notes 蒸馏出的 **DSH 优化共识**，重点解决子代理数量、并发边界、后台任务堆积与安全运维。

## 文件

| 文件 | 用途 |
|---|---|
| `CONSENSUS.md` | 完整共识：官方机制、默认值、本机推荐值、安全应用步骤、来源 |
| `apply_limits.py` | 外部终端执行的有界配置补丁（自动备份、行级修改、保留注释、YAML 校验） |
| `rollback_limits.py` | 恢复最近一次 `apply_limits.py` 的备份 |

## 一句话结论

DSH 的子代理数量不是“一个开关”，而是分层上限：

- 单步工具池：`agent-loop.maxParallelToolCalls`（默认 10）
- 后台任务：`jobs.maxConcurrentJobsPerOwner`（默认 10）
- workflow 扇出：`maxConcurrentAgents`（默认自动 ≈核数-2）、`maxTotalAgents`（默认 1000）、`maxItemsPerCall`（默认 4096）
- 委派深度：`tool-subagent.maxDepth`（默认 3）

本机（20 核 / 7.4GB）推荐：`8 / 8 / 4 / 128 / 1024 / 2`。不要只调大 `maxParallelToolCalls` 对付大任务——它管不了后台/continuable 子代理离开后的并发。

## 当前状态

- 已爬取并整理官方源码/文档/Agent Notes。
- 已生成安全补丁脚本（`apply_limits.py`）并做过本地“复制 DSH_HOME → apply → rollback”测试。
- **未改动正式 `~/.dsh`**：当前沙箱对 `~/.dsh` 只读；按共识需要在你确认后，由外部终端执行脚本或手工合并。
