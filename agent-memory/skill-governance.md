# Skill Governance Memory

> 持久人类反馈文件。每次治理循环先读这里；用户反馈/覆盖也写在这里，避免只存在会话里。

## 金标准
- 新 skill 默认 `activation: catalog`，不自动进模型上下文。
- 修改 `dsh-skill-vault` / `dsh-skill-router` 前先隔离冒烟；不热更运行中 agent。
- 效果数据用 `skill_effect_log` 记录（triggered / used / outcome / task / note），落盘 `~/.dsh/skill-vault/effect-log.json`。

## 已知误触发 / 假阳性
- （暂无记录。发现后补：`<skill-id>`: 在什么任务上误触发？如何修 description/whenToUse？）

## 用户偏好与覆盖
- 2026-09-06：用户确认全局 enabled 收敛为“底座三件套 + core-iteration 场景”，不自动扩大常驻集合。
- 用户要求：涉及 `~/.dsh` 本地状态/破坏性操作要先确认，不擅自替用户改。

## 待验证 / 低置信
- `design-skill-control-loop`：尚无运行期 effect 数据，保持 catalog 关闭；积累真实使用后再考虑 enable。
- 新治理控制器 `skill_governance`：规则阈值（effect_rate>=0.5、misuse_rate<=0.3、样本>=3）为初版，需真实数据校准。

## 流量控制
- 每个 skill 最多 1 个开放变更；开放中由 `agent-memory/open-changes.json` 记录。
- 当前开放：无。

## 最近一次治理
- 日期：2026-09-06
- 传感器读数：enabled 6/24；effect-log 0 条；doctor 24/24 通过
- 采取动作：隔离冒烟通过；enabled.json 收敛；接入 skill_governance 控制器
- 遗留：正式 profile 重启后让新工具生效；积累 effect 数据后校准阈值
