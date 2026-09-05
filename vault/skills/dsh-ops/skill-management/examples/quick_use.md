# Quick Use：skill-management

> 一句话：管理、定位、启用 DSH agent skills，指导开发一键启用 skill 的插件/功能。

## 何时用

- 当任务命中 `SKILL.md` 的“触发条件 / 何时使用”时。

## 最小可复现动作

- 用户说“管理 skill”“开启/启用 skill”“哪个 skill 适合这个任务”。
- 用户要“把本地的 SKILL.md 变成 agent 可调用的 skill”。
- 用户要“做一个 DSH 功能/插件，让我一键启用所需 skill”。
- 当前 `available_skills` 里找不到某个 skill，但工作区里有对应文件。

## 验证方式

- 按 `SKILL.md` 的干跑/检查清单执行；
- 发布/更新前跑 `skill_package_check.py` 与本 skill 对应校验。
