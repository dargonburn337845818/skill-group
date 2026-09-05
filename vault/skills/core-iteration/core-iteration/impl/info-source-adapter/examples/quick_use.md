# Quick Use：info-source-adapter

> 一句话：把 GitHub/OSV/包生态/学术/OSS 社区信息源变成可调用、可归一化的检索适配器，输出 raw_corpus 与 source_scope_report。

## 何时用

- 当任务命中 `SKILL.md` 的“触发条件 / 何时使用”时。

## 最小可复现动作

- 调度器设置了 `info_scope`，需要按来源类型实际检索。
- 用户要求“查 GitHub / 查包生态 / 查安全公告 / 查论文”等具体来源。
- 需要在报告中说明“本轮查了哪些源、用了哪些查询、有哪些限制”。
- 真实调用：Watt host 代理可加速的域名（如 GitHub）可真实返回；未加速域名可使用 `--offline` 固定样本验证同一契约。

## 验证方式

- 按 `SKILL.md` 的干跑/检查清单执行；
- 发布/更新前跑 `skill_package_check.py` 与本 skill 对应校验。
