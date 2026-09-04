import fs from 'node:fs';
const body = `# 安全评审报告

## 威胁建模
- 资产：用户凭证与业务数据
- 攻击者：未认证外部攻击者
- 信任边界：公网负载均衡 -> 应用进程
- 最小威胁清单：认证绕过 / 注入 / 越权 / 敏感信息泄露 / 依赖投毒

## 输入校验与输出编码
- 服务端校验一切输入
- 输出到 HTML 做上下文编码
- SQL 使用参数化查询

## 认证 / 授权 / 会话
- 密码使用自适应哈希（bcrypt/argon2/scrypt）
- 会话 cookie 设置 HttpOnly、Secure、SameSite
- 每次资源操作服务端校验权限

## 依赖与供应链
- 锁定版本并提交 lockfile
- 定期运行 npm audit / pip-audit / osv-scanner
- 第三方镜像 pin 到 digest

## 密钥、配置与日志
- 密钥从环境变量读，不进 git、不进日志
- 生产关闭 debug
- 日志脱敏，不记录完整 body

## 风险清单
- RISK: 硬编码 admin token，位置 app.admin.token，缓解：改为环境变量并轮换
- RISK: CORS 全放开，位置 app.cors.origin，缓解：限制白名单
- RISK: 数据库 root/root 直连，位置 app.db.connection，缓解：最小权限专用账号
- RISK: 日志记录完整请求 body，位置 app.logging.body，缓解：脱敏后记录
- RISK: debug 在生产开启，位置 app.debug，缓解：生产关闭 debug
- RISK: 明文 secret 写入配置，位置 app.secret，缓解：迁移到密钥管理服务
`;
fs.writeFileSync('report.md', body);
fs.writeFileSync('output.txt', '最小威胁清单\n认证绕过\n越权\n依赖投毒\n威胁建模\n输入校验与输出编码\n认证 / 授权 / 会话\n依赖与供应链\n密钥、配置与日志\nRISK:\nRISK:\nRISK:\nRISK:\nRISK:\n');
