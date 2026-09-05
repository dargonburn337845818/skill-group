# dsh-skill-vault

> DSH 技能保险库：统一管理蒸馏出的 skill，按场景/单 skill 开关启用，并提供 agent 工具与 Web 面板。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 简介

dsh-skill-vault 是 DSH（DeepSeek Harness）生态中的技能库插件。它把分散的 skill 按“使用场景”组织，并提供场景级与单 skill 级开关。启用状态保存在本地数据目录，不进入公开仓库。

本仓库同时承载插件源码与开源 skill/语料，远程仓库为 [skill-group](https://github.com/dargonburn337845818/skill-group)。

## 功能

- **统一存放**：将蒸馏出的 skill 放入 `vault/`，按场景组织，避免目录臃肿。
- **按需启用**：场景级开关 + 单 skill 开关，默认关闭，不抢上下文。
- **Agent 工具**：查询、启用、禁用、入库。
- **Web 面板**：可视化开关面板，可与过程监视器联动。
- **人工推送**：新增 skill 通过 `skill_vault_add` 准备入库，实际 git 推送必须人工执行。

## Agent 工具

| 工具 | 作用 |
|---|---|
| `skill_vault_list` | 按场景/专家/来源/启用状态查询 |
| `skill_vault_enable <target> [scope=global\|session]` | 开启一个 skill 或一个场景 |
| `skill_vault_disable <target> [scope=global\|session]` | 关闭一个 skill 或一个场景 |
| `skill_vault_add` | 将含 SKILL.md 的蒸馏目录复制进 vault 并生成 manifest（不提交 git） |

## 启用语义

- 默认：所有 skill 关闭，只出现在插件目录中。
- 开启后：插件调用 `ctx.skills.register()`，skill 进入 DSH 全局技能目录。
- `scope=global` 写入 `~/.dsh/skill-vault/enabled.json`，跨重启生效。
- `scope=session` 只影响当前进程，重启恢复全局状态。

## 仓库结构

```text
src/                 # 插件 TypeScript 源码
vault/               # 开源 skill 仓库
├── skills/          # 按场景组织的技能包
├── corpus/          # 开源语料/产物
└── manifest.schema.json
scripts/             # 构建、校验、手动推送
tests/               # 插件与 vault 校验测试
lib/                 # 预构建产物（提交到仓库）
```

## 开发与构建

```bash
bash scripts/build.sh
npm run build:client
npm test
```

遵循 `dsh-optimization-consensus`：

- 不自动热装到运行中的 agent；
- 先在隔离 `DSH_HOME` 做配置导出与冒烟；
- 回滚恢复实际文件，不只改 package.json pin；
- 插件不自动 push，推送前先人工 review。

## 快速启动与发布

- [QUICKSTART.md](QUICKSTART.md)：安装、加载、开启 skill、发布新版本。
- [DESIGN.md](DESIGN.md)：模块设计说明。
- 推送 `v*` tag 后，`.github/workflows/release-plugin.yml` 会校验 vault、打包并创建 GitHub Release。

## 手动推送

```bash
bash scripts/push.sh
```

脚本会提示并执行 `git add -A && git commit && git push`；需要在外部终端人工运行。

## 贡献与安全

- 贡献流程：[CONTRIBUTING.md](CONTRIBUTING.md)
- 漏洞上报：[SECURITY.md](SECURITY.md)
- 社区行为：[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- 公开仓库不发布内部开发产物：`assignments/` 与顶层 `evals/` 已通过 `.gitignore` 排除。

## 许可证

[MIT](LICENSE)
