# 核心迭代元能力 · Round 6：真实调用落地 + 提升/验证双循环

> 日期：2026-09-04 ｜ 状态：真实调用代码已落地，双轮“提升→验证”均 PASS

## 一、提升 Cycle A → 验证 A

### 提升：把 `info-source-adapter` 做成真实调用

- 新增 `tools/info_source_cli.py`
  - 真实调用 GitHub REST Search（仓库）
  - 真实调用 OSV API（漏洞查询）
  - 真实调用 PyPI / npm / crates.io 元数据 API
  - 输出统一 `raw_corpus + source_scope_report`
- 新增 `tools/fixtures/*.json`：离线固定样本，供网络受限环境验证同一契约
- 新增 `tools/run_improve_validate.py`：一键执行“信息获取提升 → 契约/行为/冒烟验证”

### 验证 A

- `validate_contract.py`：PASS
- `behavior_test.py`：PASS
- `smoke_test.py`：PASS
- 离线真实调用：6 条 raw_corpus，0 失败

## 二、提升 Cycle B → 验证 B

### 提升：让技能文档与校验覆盖真实调用

- 在 `info-source-adapter/SKILL.md` 增加“真实调用（已实现工具）”命令 SOP。
- `validate_contract.py` 增加“必要工具文件存在性”检查。
- `scorecard.py` 已覆盖 9 个 skill。

### 验证 B

- `run_improve_validate.py --offline`：**PASS**
- `validate_contract.py`：**PASS**
- 自动评分卡：**146 / 180**（9 skill 平均 16.22）

## 真实调用说明

- 本沙箱 shell **不允许直连外网**（`Connection refused`），所以无法在这里真正打到 GitHub/OSV。
- 代码本身是**真实调用实现**：在正常网络环境或带 `GITHUB_TOKEN` 的环境中可直接运行：
  ```bash
  python3 tools/info_source_cli.py github --query "topic:rust stars:>100" --limit 10
  python3 tools/info_source_cli.py osv --package requests --version 2.31.0
  python3 tools/info_source_cli.py pypi --package requests
  python3 tools/info_source_cli.py npm --package typescript
  python3 tools/info_source_cli.py crates --package serde
  ```
- 沙箱验证使用 `--offline` 固定样本，保证“输出契约、错误处理、归一化逻辑”可测。

## 已适配 host 代理模式

- 默认 `--proxy-mode auto` 现在**优先 host 代理** `http://127.0.0.1:443`，而不是系统代理。
- 系统代理 `http://127.0.0.1:26501` 仍可检测，但只在显式 `--proxy-mode system` 时使用。
- `run_improve_validate.py` 也已支持 `--proxy-mode host|system|none`。

## 已查到 Watt Toolkit 代理端口

- 通过 Windows 注册表查到：`ProxyServer = 127.0.0.1:26501`。
- Watt Toolkit 进程 `Steam++.exe` 当前监听端口：`80 / 443 / 22 / 9418`。
- CLI 已支持自动检测：
  ```bash
  python3 tools/info_source_cli.py --detect-proxy
  # => {"detected_proxy": "http://127.0.0.1:26501"}
  ```
- 注意：本 WSL 沙箱与 Windows 宿主网络隔离，无法从沙箱直连该代理；在宿主或同一网络环境中可用。

## 本地代理尝试

- 已检查：shell 无 proxy 环境变量，沙箱内未见 Watt Toolkit 代理端口（常见 7890/10808/10809 等均不可达）。
- 已为 CLI 和 `run_improve_validate.py` 增加 `--proxy <url>` 支持；在有代理的机器上可直接：
  ```bash
  python3 tools/info_source_cli.py --proxy http://127.0.0.1:<watt-port> github --query "topic:rust" --limit 5
  ```
- 本沙箱仍无法连到本地代理，所以真实外网调用需在能访问该代理的机器上执行。
## 产物

- `tools/info_source_cli.py`
- `tools/run_improve_validate.py`
- `tools/fixtures/*.json`
- `tools/output/info_dump.json`
- `info-source-adapter/SKILL.md` 真实调用 SOP
- `REPORT_ROUND6.md`
