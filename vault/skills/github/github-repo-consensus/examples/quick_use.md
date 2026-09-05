# Quick Use：github-repo-consensus

> 一句话：开源 GitHub 仓库页/README/元数据、隐私与安全、目录结构、GitHub Actions 的可执行检查清单；来源可追溯，含边界与反例。

## 何时用

- 当任务命中 `SKILL.md` 的“触发条件 / 何时使用”时。

## 最小可复现动作

- 用户问“怎么给 GitHub 仓库写 README / 建页面 / 配 license / 加 contributing”。
- 用户要把一个本地项目开源化：设 license、决定 public/private、清理 secrets、建目录结构、写 Actions。
- 用户要审查已有仓库的社区健康度 / 安全设置 / Actions 是否规范。
- agent 需要一套可执行的仓库初始化/改造检查表，而不是一段泛泛而谈。

## 验证方式

- 按 `SKILL.md` 的干跑/检查清单执行；
- 发布/更新前跑 `skill_package_check.py` 与本 skill 对应校验。
