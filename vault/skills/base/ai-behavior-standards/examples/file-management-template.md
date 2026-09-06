# 文件管理模板（可直接复制到工作区）

```text
# 工作区根（~/work 或 ~/<workspace>）
AGENTS.md            # 模块地图
README.md            # 工作区入口（可选）
SKILL_MAP.md         # 技能索引
HANDOFF-NEXT-SESSION.md
standards/           # 规范入口：REPO_STANDARD.md、editorial-style-spec.md 等
data/                # 跨项目只读数据
reports/             # 跨项目报告/审计
scratch/             # 临时/一次性质（gitignore，定期清理）
archive/             # 已完成、只读
<project>/
```

# 项目模板
```text
<project>/
├── README.md
├── AGENTS.md
├── CONTEXT.md
├── src/
├── tests/
├── docs/
├── data/
├── scripts/
├── outputs/          # .gitignore
└── scratch/          # .gitignore
```

# 命名速查
```text
代码：module-name.ts / auth-service.ts
数据：dataset-scope.json / cf_problems.json
文档：2026-09-06-file-management.md
实验：ab-skill-lift-2026-09-06/run-1.log
禁止：final / final2 / 副本 / 未命名 / 新建文件夹 / tmp / result.json
```

# 每次创建文件前的问题
```text
1. 它属于哪个项目/主题？
2. 文件名是什么（含主题/日期，无禁用词）？
3. 放哪个标准目录？
4. 是代码/数据/产物/文档哪一类？
5. 同名/同职责文件已存在吗？
6. 需要被 git 跟踪吗？不应跟踪的进 .gitignore。
7. 什么时候清理或归档？
```
