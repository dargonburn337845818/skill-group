# dsh-skill-vault · 开源技能/语料仓库

> 你的蒸馏 skill 集中仓库：按使用场景组织，全部开源、可历史回溯。
> 插件 `@dsh-external/dsh-skill-vault` 从这里读取目录，并通过 `ctx.skills.register()` 把“已启用”的 skill 注入 DSH。

## 目录约定

```text
vault/
├── README.md
├── manifest.schema.json          # skill manifest 规范
├── skills/
│   ├── teaching/                 # 教学引导 / 拆题
│   │   └── <skill-id>/
│   │       ├── SKILL.md          # 必须：agent 可调用正文
│   │       ├── manifest.json     # 必须：元数据/开关分组/来源
│   │       └── ...               # 可选资源（CONSENSUS/SOURCES/JSON）
│   ├── distillation/             # 内容蒸馏 / 知识化
│   ├── research/                 # 科研 / 组会 / 论文
│   ├── dsh-ops/                  # DSH 运维 / 工具
│   └── github/                   # GitHub 开源仓库 / 发布
├── corpus/                       # 开源训练语料 / 原始素材（可复现）
└── meta/
    └── skill-vault-publish/      # “如何入库”的元 skill
```

规则：

1. 只允许一层场景 + 一层 skill（和 DSH 原生 skill 发现深度一致）。
2. `SKILL.md` 是插件注册时读取正文的唯一必须文件。
3. `manifest.json` 的 `scenario` 决定主场景；`scenarios`/`tags` 支持交叉检索。
4. 个人开关状态**不提交到本仓库**，本地存在 `~/.dsh/skill-vault/enabled.json`。
5. Git 提交/推送一律手动（见仓库根 `scripts/push.sh`），避免密码进入 agent 会话。

## 已入库种子

| 场景 | skill | 说明 |
|---|---|---|
| teaching | teacher-consensus | 算法竞赛教师共识 · 熵减盘问 |
| distillation | distillation-consensus | 通用内容蒸馏共识 |
| research | vlpc-consensus | VLPC 领域共识与组会报告 |
| dsh-ops | dsh-optimization-consensus | DSH 运维与优化共识 |
| dsh-ops | skill-management | Skill 管理方法 |
| github | github-repo-consensus | GitHub 开源仓库页/隐私/结构/Actions 共识 |
