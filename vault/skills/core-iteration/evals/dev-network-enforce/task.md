---
{
  "id": "dev-network-enforce",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [
    "network",
    "troubleshooting"
  ],
  "expected_skill": "dev-network",
  "expect_skill_invocation": true,
  "checks": [
    "contains:DIAGNOSIS",
    "contains:RESOLUTION",
    "contains:VERIFY",
    "contains:dig",
    "files:report.md"
  ],
  "timeout_ms": 300000
}
---

我的 `npm install` 报 `ENOTFOUND registry.npmjs.org`。请按网络排障流程处理，并把完整结论写入 `report.md`。

`report.md` 必须包含以下小节（标题原样保留）：
1. DIAGNOSIS
2. RESOLUTION
3. VERIFY

DIAGNOSIS 中至少给出 3 条真实可执行的诊断命令（如 `dig`、`nslookup`、`curl`、`cat /etc/resolv.conf` 等），并说明如何判断是 DNS 问题；RESOLUTION 必须给出可逆修复步骤；VERIFY 必须给出重跑验证的命令。
