# Sources（dev-network）

> 本技能为“开发场景网络排障”的蒸馏产物。以下来源均为公开可回溯；核心实操规则主要来自 `CacinieP/network-troubleshoot-skill`（MIT），并用工具官方文档做交叉印证。

## 一手/行业来源

- https://github.com/CacinieP/network-troubleshoot-skill
  - `skills/network-troubleshoot.md`（症状分类、诊断命令、修复矩阵）
  - `docs/TROUBLESHOOTING_GUIDE.md`（平台分指南、工具配置）
  - `README_CN.md`（中国/GFW 场景、镜像与代理层级）
- https://curl.se/docs/manpage.html（`--verbose`、`--connect-timeout`、`--proxy`、退出码）
- https://bind9.readthedocs.io/en/latest/reference.html（dig/nslookup）
- https://docs.npmjs.com/cli/v10/using-npm/config（registry/proxy/strict-ssl）
- https://pip.pypa.io/en/stable/topics/configuration/（index-url/trusted-host）
- https://git-scm.com/docs/git-config（http.proxy/http.sslVerify）
- https://docs.docker.com/engine/daemon/proxy/（registry-mirrors/proxies）
- https://www.openssl.org/docs/manmaster/man1/openssl-s_client.html（s_client 证书检查）
- https://nodejs.org/api/errors.html（Node 网络错误码语义）

## 验证/开发底座

- `$PROJECT_ROOT/vault/skills/base/search-source/`
- `$PROJECT_ROOT/vault/skills/core-iteration/skill-verification-consensus/`
- `$PROJECT_ROOT/vault/skills/core-iteration/dev-workflow-consensus/`

## 备注

- 本技能是“可执行判断”蒸馏，不是对任一仓库的全文复制；镜像/代理指令给出可逆恢复原则，未把厂商/地区特例写成普适规则。
- 关于关闭 TLS 校验（`NODE_TLS_REJECT_UNAUTHORIZED=0`、`strict-ssl false`、`http.sslVerify false`）：仅作为开发临时排障，正文明确要求恢复并追因。
