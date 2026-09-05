# Changelog

## 0.1.0 (2026-09-05)

- 首版蒸馏 `dev-network`：
  - 六步工作流：Collect → Classify → Diagnose → Analyze → Resolve → Verify。
  - 症状分类表：连通性 / DNS / 代理 / TLS / HTTP / 防火墙 / 包管理器。
  - 根因→可逆修复矩阵，覆盖 npm、pip、Git、Docker、代理层级、证书、GFW。
  - 来源：CacinieP/network-troubleshoot-skill + 工具官方文档。
- 真实 A/B：`benchflow_runner`（DeepSeek, runs=3）通过——dev-network-enforce 成功率 0.667→1.0、覆盖 0.0→1.0；anti-trigger 误触发 0；增强指数 16.8%（明显增强），门禁 PASS。
- 状态：`verified`。
