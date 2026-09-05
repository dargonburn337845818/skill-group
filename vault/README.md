# dsh-skill-vault · 开源技能/语料仓库

> 你的蒸馏 skill 集中仓库：按使用场景组织，全部开源、可历史回溯。
> 插件 `@dsh-external/dsh-skill-vault` 从这里读取目录，并通过 `ctx.skills.register()` 把“已启用”的 skill 注入 DSH。

## 目录约定

```text
vault/
├── README.md
├── TAG_TAXONOMY.md               # 分类法：场景/路由/模块/标签各管什么
├── manifest.schema.json          # skill manifest 规范
├── skills/
│   ├── base/                     # 常驻底座：搜索/工作共识/DSH 运维底线（隐藏）
│   ├── core-iteration/           # 核心迭代元能力 / 价值递归提升
│   ├── dev/                      # 开发模块：dev-module + 九个子技能
│   ├── distill/                  # 蒸馏模块：distill-module 编排层
│   ├── teacher/                  # 教师模块：人名专家团 + 回合式讨论
│   ├── research/                 # 科研模块：导师团队 + 论文/组会/PPT
│   ├── writing/                  # 文稿模块：提示词/文案/文档/报告
│   ├── distillation/             # 内容蒸馏 / 知识化
│   ├── dsh-ops/                  # DSH 运维 / 工具
│   └── github/                   # GitHub 开源仓库 / 发布
├── corpus/                       # 开源训练语料 / 原始素材（可复现）
└── meta/                         # modules.json / EXPERT_LIBRARY / domain-profiles
```

规则：

1. 只允许一层场景 + 一层 skill（和 DSH 原生 skill 发现深度一致）；模块内部子技能放在 `module/subskills/`，不独立注册。
2. `SKILL.md` 是插件注册时读取正文的唯一必须文件。
3. `manifest.json` 的 `scenario` 决定主场景；`scenarios` 支持交叉检索。
4. `tags` 只做横向检索，使用受控词表，**禁止状态词/重复大类词**；规范见 `TAG_TAXONOMY.md`。
5. 个人开关状态**不提交到本仓库**，本地存在 `~/.dsh/skill-vault/enabled.json`。
6. Git 提交/推送默认交互确认（见仓库根 `scripts/push.sh`）；凭据通过 git credential helper / CI secret 提供时，可用 `--yes`/`PUSH_CONFIRM=yes` 全自动推送。不要把密码写进 agent 提示词或仓库文件。

### 易混目录说明

| 目录 | 是什么 | 不要理解成 |
|---|---|---|
| `teacher/` | 教师模块壳（多 agent 讨论协议） | 算法教学领域内容 |
| `teaching/` | 领域内容（算法教师共识等） | 教师模块壳 |
| `distill/` | 蒸馏编排层（distill-module） | 内容蒸馏算法库 |
| `distillation/` | 内容蒸馏/知识化场景 | 蒸馏编排层 |
| `core-iteration/impl/` | 核心迭代内部原语 | 独立公开 skill |

## 正式版五模块

| 场景 | 模块入口 | 子技能 / 来源 |
|---|---|---|
| `dev` | `dev-module` | 前端、后端、美术/PPT、安全、并发、性能、测试、设计美学、去 AI 味 |
| `distill` | `distill-module` | 模块缺口 → core-iteration 六阶段 → 回填 modules/EXPERT/domain |
| `teacher` | `teacher-module` | 人名专家团、回合式讨论、专家缺口分支 |
| `research` | `research-module` | 论文阅读、脉络、写作、组会、PPT、导师审查、职业路径 |
| `writing` | `writing-module` | prompt-writing、copywriting、document-report |

注册表：`vault/meta/modules.json`（五模块 + 隐藏底座 + gapProgress）。

## 已入库种子

| 场景 | skill | 说明 |
|---|---|---|
| base | search-source | 搜索与来源深模块：多源检索、归一化、来源可信度 |
| base | work-consensus | 开工/重构前工作共识：深模块、接口即测试面、模块地图 |
| base | dsh-optimization-consensus | DSH 运维与优化共识 |
| core-iteration | core-iteration | **核心迭代元能力**：搜索、过滤、蒸馏、迭代、校验、调度、审计 |
| core-iteration | dev-workflow-consensus | 开发工作流：规格先行、对抗审查、证据化验证 |
| core-iteration | skill-verification-consensus | 发布前校验：证据分类、可证伪、Skill TDD |
| dev | dev-module | 开发模块壳（九个子技能已蒸馏/挂载） |
| distill | distill-module | 蒸馏模块编排层：模块缺口 → 新 Skill / 专家 → 回填 |
| teacher | teacher-module | 人名专家团 + 回合式讨论协议 |
| research | research-module | 科研多 agent 导师团队与论文/组会流程 |
| research | vlpc-consensus | VLPC 领域共识与组会报告 |
| writing | writing-module | 文稿模块：提示词/文案/文档/报告文本服务 |
| dsh-ops | skill-management | Skill 管理方法 |
| dsh-ops | skill-vault-publish | 新蒸馏 skill 入库 dsh-skill-vault 的操作手册 |
| github | github-repo-consensus | GitHub 开源仓库页/隐私/结构/Actions 共识 |
