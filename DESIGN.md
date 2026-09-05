# dsh-skill-vault 设计共识

> 本文记录本次 grill-me 后确定的设计决策。它是实现与后续维护的接口契约。

## 1. 目标

为“个人蒸馏 skill 越攒越多、臃肿且难查”提供一个 DSH 深模块：

- 集中管理自己的蒸馏 skill。
- 按使用场景/领域查询。
- 场景级 + 单 skill 级开关，可持久、可会话临时。
- 教师共识等“大师指导”通过 skill 正文按需激活，不常驻上下文。
- 开源 GitHub 历史仓库，方便管理、回档、分享。

## 2. 交付范围

- 单一远程仓库：`skill-group`（插件代码 + vault 数据放一起）。
- 插件包名：`@dsh-external/dsh-skill-vault`。
- 形态：hybrid（agent 工具 + Web UI 面板）。
- 本地仓库路径：`$PROJECT_ROOT`。

## 3. 关键决策

| 决策点 | 结论 |
|---|---|
| 开关粒度 | 场景级开关 + 单 skill 开关 |
| 启用范围 | 全局持久 + 会话临时覆盖 |
| Skill 来源组织 | 集中仓库；以后蒸馏直接入库 |
| 仓库内容 | 开源训练语料 + 蒸馏产物都进仓库 |
| 领域分类 | 按用途/场景：教学引导、内容蒸馏、科研/组会/论文、DSH 运维、GitHub 开源仓库 |
| 插件形态 | hybrid（toolkit + UI） |
| Git 同步 | 本地仓库路径 + 脚本推送（默认交互确认；凭据可用时显式 `--yes` 全自动），不在 agent 会话直接持有密码 |
| 启用语义 | 进入可选目录，按需加载（不自动注入上下文） |
| 大师模式 | 技能内自带大师身份，按需激活 |
| 发现方式 | 插件运行时 `ctx.skills.register()` 为主 |
| 新增入库 | 插件准备 + 脚本提交/推送（默认交互确认；可显式全自动） |
| 配置存放 | 插件数据目录 `~/.dsh/skill-vault/enabled.json`，不进 Git |
| 首批入库 | 只入自己蒸馏的：teacher-consensus、distillation-consensus、dsh-optimization-consensus、skill-management、vlpc-consensus；不迁别人的开源项目 |

## 4. 场景 id 约定

| id | 标题 | 说明 |
|---|---|---|
| `teaching` | 教学引导 / 拆题 | 教师共识、熵减盘问 |
| `core-iteration` | 核心迭代元能力 / 价值递归提升 | 信息搜集、收益计算、蒸馏、迭代、调度、决策六合一 |
| `distillation` | 内容蒸馏 / 知识化 | 把材料变成 skill |
| `research` | 科研 / 组会 / 论文 | VLPC、物理信息、组会技巧 |
| `dsh-ops` | DSH 运维 / 工具 | 运维共识、skill 管理、vault 发布 |
| `github` | GitHub 开源仓库 / 发布 | 开源仓库页/隐私/结构/Actions 共识 |

## 5. manifest 字段

```json
{
  "id": "teacher-consensus",
  "name": "teacher-consensus",
  "title": "算法竞赛教师共识 · 熵减盘问",
  "description": "一句话说明",
  "whenToUse": "什么任务触发",
  "scenario": "teaching",
  "scenarios": ["teaching", "distillation"],
  "tags": ["算法竞赛", "教师", "熵减盘问"],
  "experts": ["tourist", "jiangly"],
  "sourceRefs": ["来源 URL/路径"],
  "activation": "catalog",
  "version": "0.1.0",
  "license": "MIT"
}
```

## 6. 插件接口

### 工具

- `skill_vault_list`
- `skill_vault_enable`
- `skill_vault_disable`
- `skill_vault_add`

### Web API

- `GET /skill-vault/api/list`
- `POST /skill-vault/api/enable` `{ target, scope }`
- `POST /skill-vault/api/disable` `{ target, scope }`

### UI 面板

- conversation.view 槽位
- 场景分组，显示 `已启用/总数`
- 每 skill 勾选框
- 场景一键全开/全关

## 7. 数据与安全

- 个人启用状态在 `~/.dsh/skill-vault/enabled.json`，不属于公开仓库。
- 插件默认不主动 push；`scripts/push.sh` 默认交互确认，凭据可用时可用 `--yes`/`PUSH_CONFIRM=yes` 全自动执行。
- 涉及 DSH 插件升级/热更，遵循 `dsh-optimization-consensus`：先备份、隔离冒烟、无 running agent、回滚实际文件。

## 8. 回滚/运维

- 插件回滚：恢复 `node_modules` 中的实际文件 + `package.json` pin，真实启动验证。
- Vault 内容回滚：git history。
- 首次推送前：`git remote add origin https://github.com/dargonburn337845818/skill-group.git`。

## 2026-09-04 与 dsh-skill-router 联动

- 新增 `base` 场景：search-source / work-consensus / dsh-optimization-consensus。
- 核心元能力改为唯一入口 `core-iteration/core-iteration`，原子 skill 移入 `impl/`。
- manifest 新增 routing / qualityCriteria / boundary / notWhenToUse / hidden。
- API 新增 `/route` 与 `/reset-base`。
- 会话页主面板由 dsh-skill-router 接管；本插件只保留设置页高级管理。
