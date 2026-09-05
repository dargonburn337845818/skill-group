# SOURCES

> dsh-optimization-consensus 的来源账本。此处记录 Round 37 深度补强引入的新增来源；原有来源继续保留在 `SKILL.md` / `CONSENSUS.md` 中。

## Round 37 新增来源

1. **DeepSeek Harness 插件安全第三方审计讨论（#454）**
   - URL: https://github.com/deepseek-ai/deepseek-harness/discussions/454
   - 主张：DSH 插件在宿主进程内以宿主权限运行；安装/更新/篡改/持久化/热更路径缺少签名、完整性、来源、确认门；`!!js` 配置可在加载期 RCE；安装后篡改零校验；`dsh plugin remove` 不清理 `!!js` 后门；用户 patch 热更约 15s 生效且不重启。
   - 证据类型：static + runtime（40 条攻击路径、96 条源码证据、13 个可复现 demo、8+2 次 live verification）。

2. **Fz0x00/deepseek-harness-plugin-security-audit**
   - URL: https://github.com/Fz0x00/deepseek-harness-plugin-security-audit
   - 主张：完整防御性审计报告；所有 live 测试仅使用一次性隔离 `DSH_HOME`，未触碰真实部署；提出供应链 pinning、安装/更新确认门、telemetry 敏感化等加固路线。

3. **PerryLink/dsh-plugin-certification**
   - URL: https://github.com/PerryLink/dsh-plugin-certification
   - 主张：社区插件认证 spec v1——manifest 卫生、构建卫生、OpenSSF Scorecard、npm provenance、隔离安装 smoke 五个机器可查维度，A-D 评级配安全否决；认证结果可入 registry 与 badge。

4. **Claude Code Docs — Create custom subagents**
   - URL: https://code.claude.com/docs/en/sub-agents
   - 主张：subagent 各自独立上下文、工具与权限；`description` 是委派入口，本身占上下文；自定义 subagent description 合计超过 15,000 tokens 会在启动时警告；应按模型/工具/effort 分流控制成本。

5. **Loom — Multi-Agent Orchestration Architecture**
   - URL: https://github.com/teradata-labs/loom/blob/main/docs/architecture/multi-agent.md
   - 主张：并发模型选择 `limit=5`（防死锁、压过 rate limit、留 50% 余量）；“No limit / maximum parallelism, no blocking”被明确拒绝；默认每 workflow 20 agents / 10 stages / 5 rounds，资源耗尽防护明确标注 `TODO: workflow timeout`。

6. **OpenAI Codex issue #33437 — Project-scoped subagent policy profiles**
   - URL: https://github.com/openai/codex/issues/33437
   - 主张：需要具名 agent allowlist、model/effort 不可被调用方绕过、按具名 agent/模型并发配额、配额跨会话/项目累计，而不是只靠全局 `max_threads`。

7. **OpenAI Codex issue #23479 — capacity/status preflight before spawn_agent**
   - URL: https://github.com/openai/codex/issues/23479
   - 主张：主 agent 需要可靠 capacity/status 预检，否则 spawn 失败会退化为主 agent 自己干或不委派；应区分 available/running/completed/queued，并精确回传失败原因（thread limit、quota、provider failure 等）。

8. **OpenAI Codex issue #32353 — completed agent pending mailbox pins residency slot**
   - URL: https://github.com/openai/codex/issues/32353
   - 主张：已完成 agent 的 pending queue-only mailbox 会长期占用 resident 线程槽，导致新的 `spawn_agent` 报 `agent thread limit reached`；仅看 active running 数量不能代表可用容量。

9. **pnpm install（官方文档）**
   - URL: https://pnpm.io/cli/install
   - 主张：`--frozen-lockfile` 不更新 lockfile、lockfile 与 manifest 失配即失败；`--offline` / `--force` / `--dry-run` 语义；自 v11.4.0 起 tarball integrity 不匹配是硬失败 `ERR_PNPM_TARBALL_INTEGRITY`，`--update-checksums` 是窄范围显式绕过且会打印告警。

10. **npm-ci（npm Docs）**
    - URL: https://docs.npmjs.com/cli/v12/commands/npm-ci
    - 主张：`npm ci` 严格按 lockfile 安装，会删除现有 `node_modules` 并精确重建，是干净回滚/CI 重建的官方路径。

11. **Microsoft Learn — Working across file systems（WSL）**
    - URL: https://learn.microsoft.com/en-us/windows/wsl/filesystems
    - 主张：文件应放在所在操作系统的原生文件系统（WSL 用 `/home/...`，Windows 用 `C:\...`）；跨 `/mnt/c` / `\\wsl$` 工作会损失性能，并存在大小写、权限与互操作差异。

12. **DeepSeek Harness discussion #754 — JS heap OOM 大型任务（交叉佐证）**
    - URL: https://github.com/deepseek-ai/deepseek-harness/discussions/754
    - 主张：社区报告大型任务触发 Javascript heap out of memory；作为“无界子代理/并发导致 OOM”的额外佐证，与既有 Round 0 来源交叉引用。
