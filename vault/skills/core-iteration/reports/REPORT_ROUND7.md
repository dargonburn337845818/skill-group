# 核心迭代元能力 · Round 7：Watt host 代理真实调用打通

> 日期：2026-09-04 ｜ 状态：真实调用成功（GitHub），提升/验证循环 PASS

## 突破

此前用 `--proxy http://172.30.160.1:443` 拿到 `Tunnel connection failed: 302 Found`，说明 Watt Toolkit host 代理**不是标准 CONNECT 代理**。
现已改为 **curl --resolve 直连 TLS 反代**：

```bash
curl -k --resolve api.github.com:443:172.30.160.1 https://api.github.com/search/repositories?q=...
```

结果：**真实 GitHub API 返回成功**，拿到了：

- `farion1231/cc-switch`
- `rustdesk/rustdesk`
- `rust-lang/rust`

## 代码改动

- `info_source_cli.py` 新增 host 代理模式：
  - `--proxy-mode host` → 自动使用 `curl --resolve` 直连 Watt 反代，而非设置 HTTP_PROXY。
  - 自动探测 WSL 中 Windows 宿主 IP（默认网关 `172.30.160.1`）。
  - `--detect-proxy` 现在返回 host 代理为 `http://172.30.160.1:443`。
  - 对不支持的域名返回清晰错误（如 pypi.org 未被 Watt host 代理加速），不再崩溃。
- `run_improve_validate.py` 已支持 `--proxy-mode host`，并在失败时按来源列出错误。

## 当前 host 代理实际可用范围

| 来源 | host 代理结果 |
|---|---|
| GitHub (`api.github.com`) | ✅ 真实成功 |
| OSV (`api.osv.dev`) | ❌ 未被加速（DNS 污染提示） |
| PyPI (`pypi.org`) | ❌ 未被加速 |
| npm (`registry.npmjs.org`) | ❌ 未被加速 |
| crates.io | ❌ 未被加速 |

## 真实调用记录

- `tools/output/info_dump.json`：`mode=live`，3 条真实 GitHub raw_corpus。
- 说明：Watt host 代理主要服务于已配置的加速域名（GitHub 等），包生态源需要另行接入或直连网络。

## 验证

- `tools/info_source_cli.py --proxy-mode host github --query "topic:rust" --limit 2`：✅ 成功
- `tools/run_improve_validate.py --proxy-mode host`：✅ CYCLE PASS（GitHub 真实数据 + 其他源失败被记录）
- `validate_contract.py`：✅ PASS
- `behavior_test.py`：✅ PASS

## 产物

- `tools/info_source_cli.py`（host 模式）
- `tools/output/info_dump.json`（真实 GitHub live dump）
- `REPORT_ROUND7.md`

## 下一步

1. 继续用真实 GitHub 数据迭代 `info-source-adapter` 的 GitHub 适配器（字段、限流、分页、认证）。
2. 如需 OSV/PyPI/npm/crates 真实调用，需要：
   - 在 Watt Toolkit 中把对应域名加入 host 代理/加速规则，或
   - 直连网络（不经代理），或
   - 用系统代理模式但只对特定进程启用（避免影响 WSL）。
