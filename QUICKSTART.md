# dsh-skill-vault 快速启动

## 1. 获取插件

方式 A：从 GitHub Release 下载 DSH 插件包

```bash
# 到 Releases 页下载
# https://github.com/dargonburn337845818/skill-group/releases
# 文件：dsh-external-dsh-skill-vault-<version>.tgz
```

方式 B：直接使用仓库

```bash
git clone https://github.com/dargonburn337845818/skill-group.git
cd skill-group
bash scripts/build.sh        # 有 DSH_CHECKOUT 时；否则使用已提交的 lib/
```

## 2. 加载到 DSH

开发/自托管环境：

```bash
# 解压 tgz 后，用开发注入器加载
dev_inject_plugin /path/to/dsh-skill-vault
```

正式 profile（按 `dsh-optimization-consensus` 先隔离冒烟）：

```bash
dsh plugin add /path/to/dsh-external-dsh-skill-vault-0.0.1.tgz
```

> 运行中的 agent 会话不要热装插件；等没有 running agent 后再加载。

## 3. 开启想要的 skill

Agent 侧：

```text
skill_vault_list
skill_vault_enable teaching
skill_vault_enable teacher-consensus
skill_vault_disable distillation
```

Web 侧：

- 打开 DSH Web 界面
- 找到“技能库”面板
- 按场景勾选或一键全开/全关

## 4. 使用效果

- 开启后的 skill 会进入 `available_skills`，agent 按需用 `skill` 工具加载正文。
- 教师共识开启后，遇到拆题/教学场景时 agent 会以大师身份进行熵减盘问。
- 个人开关存在 `~/.dsh/skill-vault/enabled.json`，不会进入公开仓库。

## 5. 发布新版本（维护者）

```bash
cd $HOME/work/dsh-skill-vault
# 改源码后本地构建
bash scripts/build.sh
npm run build:client
npm pack

# 打 tag 并推送，Action 自动发布 Release
git add -A
git commit -m "release: v0.1.0"
git tag -a v0.1.0 -m "release v0.1.0"
git push origin main
git push origin v0.1.0
```

GitHub Actions 会：
1. 校验 `vault/skills`
2. 执行 `npm pack`
3. 创建 Release 并上传 `dsh-external-dsh-skill-vault-<version>.tgz`
