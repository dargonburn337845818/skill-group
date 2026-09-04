# dsh-skill-vault v0.0.1

DSH 技能保险库：统筹你蒸馏的 skill，按场景/单 skill 开关按需启用。

## 新特性

- Hybrid 插件：agent 工具 + Web 可视化开关面板
- 开源 skill vault：教师共识、蒸馏共识、DSH 运维、skill 管理、VLPC
- 场景级 + 单 skill 级开关
- 全局持久 + 会话临时覆盖
- 运行时注册：只把已启用的 skill 注入 `ctx.skills`
- 手动 git 推送脚本，不把密码/凭据交给 agent

## 快速启动

1. 下载本 Release 的 `dsh-external-dsh-skill-vault-0.0.1.tgz`。
2. 在 DSH 开发环境解压/安装该插件包（或使用 `dev_inject_plugin` 指向解压后的目录）。
3. 确认插件就绪后，使用：
   - `skill_vault_list` 查看场景与 skill
   - `skill_vault_enable teaching` 开启教学场景
   - `skill_vault_enable teacher-consensus` 开启教师共识
   - Web 端打开“技能库”面板进行可视化勾选
4. 以后新蒸馏的 skill 可用 `skill_vault_add` 准备入库，再手动 `scripts/push.sh` 提交开源。

## 仓库

- 远程：https://github.com/dargonburn337845818/skill-group.git
- 本地默认路径：`$PROJECT_ROOT`
