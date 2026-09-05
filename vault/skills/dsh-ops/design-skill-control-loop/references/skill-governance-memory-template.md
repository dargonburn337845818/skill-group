# Skill Governance Memory Template

> 复制到技能库仓库 `agent-memory/skill-governance.md`（或你的等效位置）。每次治理循环都读它，让它成为人类反馈的源。

```markdown
# Skill Governance Memory

## 金标准
- 哪些 skill 的写法/触发被证明好用？
- 哪些响应模板/校验命令是必须的？

## 已知误触发 / 假阳性
- `<skill-id>`: 在什么任务上误触发？如何修 description/whenToUse？

## 用户偏好与覆盖
- 用户不喜欢什么（如自动 enable、大 PR、无来源规则）？
- 用户明确 override 过的决策（记录原因）。

## 待验证 / 低置信
- `<skill-id>`: 缺什么证据？下一次治理循环要采集什么？

## 流量控制
- 当前开放变更：`skill-gov-<skill-id>` / PR 链接
- 每个 skill 最多 1 个开放变更，超限先收旧再开新。

## 最近一次治理
- 日期：YYYY-MM-DD
- 传感器读数：enabled 数量 / effect 率 / doctor 红灯
- 采取动作：一两个 skill 的 update/disable/archive
- 遗留：下一轮要处理的项
```
