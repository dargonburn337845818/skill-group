# @dsh-external/dsh-skill-vault

> DSH 技能保险库：统筹你蒸馏的 skill，按场景/开关按需启用，agent 工具 + Web 可视化面板。
> 单仓库既承载插件，也承载开源 skill/语料（远程：`git@github.com:dargonburn337845818/skill-group.git`）。

## 这个模块解决什么

- 蒸馏出的 skill 越来越多后不再臃肿难查：统一放入 `vault/`，按**使用场景**组织。
- 开关粒度：**场景级开关 + 单 skill 开关**，默认可选目录，按需加载，不抢上下文。
- 启用状态持久化在本地数据目录，**不进入公开仓库**。
- 新增蒸馏产物通过 `skill_vault_add` 准备入库，**git 推送必须手动**（见 `scripts/push.sh`）。

## 架构（深模块）

```text
DSH 官方技能注册表 ctx.skills
        ▲
        │ register / dispose（只注册“已启用”的 skill）
        │
dsh-skill-vault 插件
├── src/catalog.ts    # 扫描 vault/skills/<场景>/<skill>/manifest.json+SKILL.md
├── src/manager.ts    # 开关状态（全局持久 + 会话临时）、注册/注销
├── src/tools.ts      # skill_vault_list / enable / disable / add
├── src/api.ts        # /skill-vault/api（Web 面板数据接口）
└── src/client/       # conversation.view 可视化开关面板
        ▲
        │ 读取
        │
vault/ （本仓库数据）
├── skills/<场景>/<skill>/{SKILL.md, manifest.json, ...}
├── corpus/           # 开源语料/产物
└── meta/             # 入库手册等
```

## 目录

```text
dsh-skill-vault/
├── src/                    # 插件 TS 源码
├── vault/                  # 开源 skill 仓库（可单独浏览）
│   ├── skills/teaching/    # 教学引导 / 拆题
│   ├── skills/distillation/
│   ├── skills/research/
│   ├── skills/dsh-ops/
│   ├── corpus/
│   └── manifest.schema.json
├── scripts/
│   └── push.sh             # 手动提交/推送（需要凭据，不自动跑）
└── package.json            # DSH 插件包
```

## 插件工具

| 工具 | 作用 |
|---|---|
| `skill_vault_list` | 按场景/专家/来源/启用状态查询 |
| `skill_vault_enable <target> [scope=global\|session]` | 开关一个 skill 或一个场景 |
| `skill_vault_disable <target> [scope=global\|session]` | 关闭一个 skill 或一个场景 |
| `skill_vault_add` | 把含 SKILL.md 的蒸馏目录拷贝进 vault 并生成 manifest（不 git） |

## 启用语义

- 默认：所有 skill 处于关闭状态，只出现在插件自己的目录（由工具/面板看到）。
- 打开后：插件调用 `ctx.skills.register()`，skill 进入 DSH 全局技能目录；agent 在遇到对应任务时按需用 `skill` 工具加载正文。
- `scope=global` 写入 `~/.dsh/skill-vault/enabled.json`（跨重启）。
- `scope=session` 只改当前进程内存，重启恢复全局。

## 开发与构建

```bash
# 需要 DSH source checkout（含 packages），或用 dev_build_plugin
bash scripts/build.sh
npm run build:client
```

遵循 `~/.dsh/dsh-optimization-consensus.md`：

- 不自动热装到运行中的 agent；先在隔离 `DSH_HOME` 做 dump-config + 冒烟。
- 回滚恢复实际文件，不只改 package.json pin。
- 插件不自动 push；推送前先人工 review。

## 手动推送

```bash
cd $HOME/work/dsh-skill-vault
bash scripts/push.sh
```

脚本会提示并执行 `git add -A && git commit && git push`；由于需要输入密码/SSH 密钥，它只该在外部终端人工运行。
