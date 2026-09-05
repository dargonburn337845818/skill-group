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

## Round 40 新增来源

- https://man7.org/linux/man-pages/man5/resolv.conf.5.html（nameserver / search / ndots 语义）
- https://man.archlinux.org/man/systemd-resolved.8.en（127.0.0.53 stub、/etc/resolv.conf 四种模式、DoT/DoH、resolvectl 视角）
- https://docs.openssl.org/3.0/man1/openssl-s_client/（-servername / -showcerts / -verify_return_error / 默认不严格校验的调试行为）
- https://docs.docker.com/engine/network/drivers/bridge/（用户自定义网络自动 DNS、默认 bridge 不自动解析）
- https://docs.docker.com/reference/cli/docker/container/run/（--dns / --network 等容器级网络参数）
- https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables（GIT_SSH_COMMAND / GIT_CURL_VERBOSE 等 git 进程环境）
- https://git-scm.com/docs/git-config#Documentation/git-config.txt-GITCONFIGCOUNT（GIT_CONFIG_COUNT 运行时配置注入，不写文件）
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/407（407 + Proxy-Authenticate）
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429（429 + Retry-After）
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/502（502 网关/上游语义）
- https://pip.pypa.io/en/stable/cli/pip_install/（--index-url / --timeout / --retries 命令级参数）

备注：Round 40 重点补“诊断链谁在解析、进程级可逆修复、HTTP 状态语义、Docker/Git 命令级参数”；之前已有的 curl 手册/npm 配置等页面仍继续作为基础来源，本次按新章节重新引用。

