---
{
  "id": "dev-security-enforce",
  "difficulty": "medium",
  "category": "skill-eval",
  "tags": [
    "security",
    "review"
  ],
  "expected_skill": "dev-security",
  "expect_skill_invocation": true,
  "checks": [
    "contains:威胁清单",
    "contains:认证绕过",
    "contains:越权",
    "contains:信任边界",
    "contains:威胁建模",
    "contains:输入校验与输出编码",
    "contains:认证 / 授权 / 会话",
    "contains:依赖与供应链",
    "contains:密钥、配置与日志",
    "contains:RISK",
    "files:report.md"
  ],
  "timeout_ms": 300000
}
---

请对下面的部署配置做一次完整安全评审，并把评审结果写入 `report.md`。

报告必须严格包含以下五个小节，标题原样保留，每节至少给出 2 条可执行检查：
1. 威胁建模
2. 输入校验与输出编码
3. 认证 / 授权 / 会话
4. 依赖与供应链
5. 密钥、配置与日志

同时至少给出 5 条以 `RISK:` 开头的风险条目，每条指出具体配置位置与缓解措施；不要只输出泛泛结论。

配置：

```yaml
app:
  env: production
  secret: REPLACE_WITH_FAKE_SECRET
  debug: true
  admin:
    path: /admin
    token: REPLACE_WITH_FAKE_TOKEN
  cors:
    origin: "*"
  db:
    user: root
    password: REPLACE_WITH_FAKE_PASSWORD
    connection: mysql://root:root@db:3306/app
  logging:
    level: debug
    body: true
```
