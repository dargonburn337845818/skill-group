# AI 行为与文件管理规范 · 完整共识

> 版本：v0.1.0（2026-09-06）
> 定位：把“AI 触及的方方面面”收敛成少数硬底线 + 可检查清单。本文是完整版，`SKILL.md` 是可执行摘要。
> 与现有规范的关系：本文**不替代**任何领域规范，只做总纲与文件管理深模块；领域细节一律回指现有 Skill/文件。

---

## 0. 为什么 AI 缺的是规范，不是信息

- AI 没有长期记忆，文件系统、目录结构、命名、交接文件就是它的长期记忆。
- 信息再多，若没有“创建时该放哪、叫什么、何时清、不碰什么”的规则，结果就是工作区越来越乱。
- 本规范的验收标准不是“文档多完整”，而是：**一个只见过目录树的新会话，能在 3 秒内知道每个文件是什么、该不该动、动完放回哪。**

---

## 1. 行为总纲（所有规范之上）

1. **优先级**：用户直接指令 > 项目指令（AGENTS/CONTEXT）> 全局共识 > 默认习惯。
2. **3 秒原则**：任何交付物/文件，读者 3 秒内应知道“这是什么、给谁、怎么用”。
3. **可追溯**：关键结论必须能指向文件/URL/来源；没有来源的一律标 `unknown` 或 `inferred`，不得伪装成事实。
4. **交付是文件/产物**：论文、代码、报告、图、技能包都要落到工作区；只回聊天不算交活。
5. **不静默破坏**：覆盖、移动、删除、重命名、改配置、切分支、推送、热更等动作，先说明影响与回滚，等确认；自动化协议里已授权的（如 repo 自动推送）按该协议执行。
6. **先修结构，别用 prompt 救结构**：目录/命名/接口/测试是主地图；长 AGENTS.md 只是补充。
7. **少而深**：宁可少数不可违反的硬规则，不要几十条永远记不住的细则；细节下沉到 `CONSENSUS.md` / 领域 Skill。
8. **一次一问**：需要用户决策时，一次只问最高信息增益的一个问题；常规分类按决策表自行处理，不反复问“放哪”。

---

## 2. 文件管理深模块（本次重点）

### 2.1 心智模型：文件系统 = AI 的记忆 + 模块地图

- 每次创建文件，等于在给 AI 写一条长期记忆；位置与文件名必须像 API 一样自解释。
- 目录名 = 概念 / 模块边界；文件名 = 该文件的唯一职责；不要出现 `utils`、`misc`、`temp`、`new`、`副本` 这类“杂物间”。
- AI 应能“只凭路径猜内容”：例如 `~/work/project/src/auth.ts` 无可疑，`~/tmp.py`、`~/\u672a\u547d\u540d.txt` 不可接受。

### 2.2 目录骨架

#### 用户主目录 `~`

| 目录 | 放什么 | 不允许放什么 |
|---|---|---|
| `~/projects/` | 长期代码/工具项目（各自 git 仓库） | 散落的单文件、临时脚本 |
| `~/work/` | 当前主工作区（多个仓库/任务共存） | 非入口数据、临时实验产物直接堆根 |
| `~/scripts/` | 一次性/主题脚本 | 与具体项目耦合的项目内脚本（应回项目） |
| `~/tools/` | 独立工具集合（如 node-project） | 大型安装包 |
| `~/installers/` | 安装包/大文件 | 已安装后长期不用的重复包 |
| `~/archive/` | 已完成、只读、需保留 | 仍在活跃修改的文件 |
| `~/data/`（可选） | 全局只读数据集 | 业务逻辑、生成物 |

#### 工作区根 `~/work/`

```text
~/work/
├── AGENTS.md                  # 工作区模块地图（人先看）
├── SKILL_MAP.md               # 技能索引（人先看）
├── HANDOFF-NEXT-SESSION.md    # 会话交接（人先看）
├── REPO_STANDARD.md / 其他标准 # 规范入口（人先看）
├── <项目目录>/                # 每个项目一个目录
├── docs/                      # 跨项目长文档（可选）
├── data/                      # 跨项目只读数据（可选）
├── reports/                   # 跨项目审计/报告（可选）
└── scratch/                   # 临时/中间物（gitignore，定期清理）
```

- **只允许“人先看”的文件留在根**：README、AGENTS、CONTEXT、SKILL_MAP、HANDOFF、标准入口。
- 数据 JSON、A/B 结果、训练脚本、审计草稿一律进 `data/`、`reports/`、`scratch/` 或所属项目。

#### 项目目录

```text
project/
├── README.md          # 3 秒门面：是什么/怎么跑/接口
├── AGENTS.md          # 模块地图：目录/接口/验证命令/约定
├── CONTEXT.md         # 领域术语、关键约束
├── src/ 或 app/       # 代码
├── tests/             # 测试
├── docs/              # 长文档（含架构/迁移/FAQ）
├── data/              # 数据资源（只读；查询语料不是业务逻辑）
├── scripts/           # 项目内工具脚本
├── outputs/ 或 dist/  # 生成产物（gitignore）
└── scratch/           # 临时实验（gitignore，7 天清理）
```

### 2.3 命名规范

#### 规则

1. **代码/路径名**：ASCII 小写 `kebab-case`（`auth-service.ts`），不要 `AuthService_file.ts`、`auth_service_v2_FINAL.py`。
2. **文档/人类可读文件**：可用中文，但避免空格、emoji、全角括号造成 shell/跨端问题；文件名要含主题与日期：`2026-09-06-file-management.md`。
3. **数据文件**：`<数据集>-<范围/日期>.json`，如 `cf_problems.json`；不要 `data1.json`、`new.json`。
4. **实验/AB**：`<实验名>-<日期>/`，每个 run 带编号或时间戳，例如 `ab-skill-lift-2026-09-06/run-1.log`。
5. **禁止词**：`final`、`final2`、`final_new`、`副本`、`未命名`、`新建文件夹`、`tmp`（顶层）、`test`（当正式文件）、`asdf`。
6. **版本化**：正式发布文件用 SemVer 或日期；草稿用 `draft-` 前缀；一个文件不要靠改后缀产生同义版本。

#### 正则（快速自检）

```text
项目内文件名： ^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z0-9]+)*$
文档名：      ^[0-9]{4}-[0-9]{2}-[0-9]{2}-[^/\\:*?"<>|]+\.md$
禁止：        (final|副本|未命名|新建文件夹|tmp|draft2?)
```

### 2.4 创建前决策表

| 创建物 | 位置 | 命名 |
|---|---|---|
| 新项目代码 | `~/work/<project>/src` | `module-name.ts` |
| 一次性脚本 | `~/scripts/<topic>/` | `topic/action-name.py` |
| 项目内脚本 | `project/scripts/` | `action-name.py` |
| 查询/数据集 | 项目 `data/` 或 `~/work/data/` | `dataset-scope.json` |
| 文档/报告 | 项目 `docs/` 或 `~/work/reports/` | `YYYY-MM-DD-topic.md` |
| 临时实验 | 项目 `scratch/` 或 `/tmp` | `exp-name/` |
| 规范/共识 | 技能库或 `~/work/standards/` | `kebab-consensus` |
| 归档 | `~/archive/` | `project-or-topic-YYYY-MM-DD/` |

### 2.5 清理与归档

- **每次会话结束**：把 `scratch/` 中临时文件删除或并入正式产物；更新 `HANDOFF-NEXT-SESSION.md` / `AGENTS.md`。
- **每周**：扫描 `~/work/` 根、`scratch/`、下载目录；超过 7 天未引用且无保留价值的移到 `archive/` 或删除（删除前先确认）。
- **归档规则**：归档目录视为只读；再次打开需明确“从归档恢复”，不要原地改。
- **备份**：移动/整理前先 `git status` 或建 `.bak-<date>`；绝不“先删再说”。
- **数据保留**：原始数据不删除，只有生成产物/临时物可清。

### 2.6 硬红线（不可违反）

1. 不把新文件写到 `~` 根、桌面、下载根、项目根；必须进标准目录。
2. 不静默覆盖/删除/移动用户已有文件；无备份、无确认不动。
3. 不把密钥、token、密码写进文件/仓库/日志；`.env` 只进 gitignore 且不进历史。
4. 不在仓库里提交 `outputs/`、`scratch/`、`node_modules/`、大模型权重、浏览器缓存。
5. 不创建与既有文件职责相同的“新版”；先查重，合并或更新。
6. 不把中间产物放在项目根等容易堆积的位置，尤其不带日期/主题的裸名（`a.json`、`result.json`）。
7. 不把工作区根当“数据仓库”：根目录每个文件都必须能解释“为什么在根”。
8. 不为了“整齐”一次性批量移动所有文件；小步、可回滚、分批。

### 2.7 AI 文件操作自检清单

```text
创建前：
□ 路径在标准目录内？
□ 文件名含主题（+日期）且无禁用词？
□ 同职责文件已存在？（先查重）
□ 是代码/数据/产物/文档哪一类，是否放对目录？
□ 是否会被 git 跟踪？不应跟踪的进 .gitignore。

创建后：
□ 临时物是否在 scratch/ 或 /tmp？
□ 是否更新了入口（README/AGENTS/CONTEXT/HANDOFF）？
□ 生成物是否可复现（README 或脚本记录了来源/参数）？

整理/移动前：
□ 已备份或可回滚？
□ 已向用户说明影响并确认（若涉及用户已有文件）？
□ 是否分批小步，而不是一把梭？
```

### 2.8 针对当前工作区的落地模板（`$HOME/work`）

现状：根目录已有项目目录 + 若干规范文件 + 零散的 `ab_*.json`、`*.md`、数据 JSON、zip。按本规范应迁移为：

```text
$HOME/work/
├── AGENTS.md
├── README.md（可选新加，指向各项目）
├── SKILL_MAP.md
├── HANDOFF-NEXT-SESSION.md
├── REPO_STANDARD.md
├── <项目目录>/            # ACM-workflow-build/、dsh-skill-vault/、skills/ 等
├── standards/             # editorial-style-spec.md、REPO_STANDARD.md 等规范入口
├── data/                  # atcoder_*.json、cf_problems.json、solvedac*.json、yukicoder*.json、ab_*.json
├── reports/               # control-loop-skill-audit-*.md、SKILL_EFFECT_REPORT.md、ab_*_result.json
├── scratch/               # 一次性实验/临时脚本
└── archive/               # 已完成 zip、旧结果
```

> 不要求一次搬完；标准落地时先建目录 `data/`、`reports/`、`standards/`、`scratch/`，把新增文件按规则放入，再分批整理存量。

---

## 3. 各领域规范索引（防止重复造轮子）

| 领域 | 规范来源 | 本规范只做 |
|---|---|---|
| 工程/编码/重构 | `work-consensus`、`dev-workflow-consensus` | 入口导航、交付物落盘约定 |
| 代码库/GitHub | `github-repo-consensus`、`REPO_STANDARD.md` | 根目录“人先看”规则、提交前安全复核 |
| 写作/文档 | `writing-module`、`editorial-style-spec.md` | 文件命名/文档位置/3 秒原则 |
| 搜索/引用 | `search-source`、`web-research-consensus` | 来源台账、不编造引用 |
| 安全/隐私 | `dev-security`、`github-repo-consensus` | 不落密钥、最小权限、日志脱敏 |
| DSH/插件运维 | `dsh-optimization-consensus` | 破坏性动作先确认、隔离冒烟、回滚 |
| 知识/技能蒸馏 | `distillation-consensus` | Skill 四件套：触发/动作/边界/来源 |
| 人机交互 | `expert-decision-consensus`、UI/UX 规范 | 一次一问、用户最终裁决、不泄露内部术语 |

---

## 4. 规范自身的元规范（以后怎么改这套规范）

1. **有缺口才新增**：先确认现有规范确实没覆盖，不做重复。
2. **可检查**：每条规范必须能翻译成“命令/文件/动作”检查；写不出检查的规则不入总册。
3. **有反例**：每条硬规则附“什么时候会翻车/什么时候不适用”。
4. **版本与来源**：修改时必须更新 `CHANGELOG.md` 与 `SOURCES.md`；无来源推断标 `inferred`。
5. **不过度约束**：新增规则前问“删掉它，混乱会回来吗？”若不会，就不加。
6. **总册短，细则深**：`SKILL.md` 保持可执行摘要；完整论证与模板进 `CONSENSUS.md`/`examples/`。

---

## 5. AI 长期记忆机制（轻量，不臃肿）

> 目标：让 AI 跨会话记得“该把文件放哪、哪些盘符已接管、哪些禁区不能碰”，但记忆文件本身保持**短、可读、单一事实源**。

### 5.1 记忆分层（三份小文件，不做数据库）

| 文件 | 位置 | 记什么 | 多大 |
|---|---|---|---|
| `AGENTS.md` | 工作区根 | 模块地图、项目入口、验证命令、关键约束 | 建议 ≤150 行 |
| `AI_MEMORY.md` | 工作区根或 `~/.dsh/` | 跨会话高信号记忆：用户偏好、安全红线、环境事实、已定决策 | 建议 ≤100 行 |
| `DRIVE_LAYOUT.md` | `standards/` | 所有盘符的用途、管理状态、禁区、最近盘点 | 建议 ≤120 行 |
| `HANDOFF-NEXT-SESSION.md` | 工作区根 | 下一次会话的“下一步 + 关键路径”，不复制已完成细节 | 建议 ≤80 行 |

- **单一事实源**：同一件事只在一个文件写；其他位置只放链接/指针。
- **指针优先**：记忆里只写“结论 + 指向详细文件”，不把完整清单塞进记忆。
- **只记行为差异**：只有“下次会改变 AI 动作”的信息才进入记忆；流水账、过程日志、全量文件列表都不进记忆。
- **过期即清**：条目 90 天未被引用则移入 `archive/` 或删除；每次会话结束只允许新增/修改 ≤3 条记忆。
- **压缩纪律**：记忆超过阈值（`AI_MEMORY.md` 100 行 / `DRIVE_LAYOUT.md` 120 行）时，把历史细节移到 `reports/` 或 `archive/`，正文只留摘要。

### 5.2 跨会话读取顺序（固定、不遍历历史）

```text
1. 读 ~/.dsh/AGENTS.md          # 全局底线
2. 读工作区 AGENTS.md / CONTEXT.md  # 模块地图
3. 读 AI_MEMORY.md              # 跨会话高信号记忆
4. 读 DRIVE_LAYOUT.md           # 盘符接管状态与禁区
5. 读 HANDOFF-NEXT-SESSION.md   # 上次留下的下一步
6. 需要细节时再读 projects/、reports/、archive/，禁止全量遍历
```

### 5.3 记忆写入纪律（防臃肿）

- 每次会话结束前问：**“这条信息如果不写，下次会不会重复踩坑/重复询问？”** 不会就不写。
- 写入格式：`触发场景 → 记忆内容 → 指向文件`，一行最多 2 句。
- 不记录：完整文件列表、每次工具调用、每次失败的中间结果、聊天记录。
- 不复制已有规范全文；记忆只放“当前环境事实 + 决策 + 指针”。
- 用户纠正偏好时必须更新 `AI_MEMORY.md`，这是最高优先级记忆。

### 5.4 与本 Skill 的关系

- `ai-behavior-standards` 是**规则**，不是记忆；规则不随环境变化。
- `AI_MEMORY.md` / `DRIVE_LAYOUT.md` 是**状态**，随整理推进更新。
- 两者分离后，AI 不会把“当前盘符状态”误当成“通用规范”。

---

## 6. 全盘符整理接管安全规范（危险动作防御）

> 目标：让 AI 可以逐步接管所有盘符的整理，但**默认只读盘点、小步移动、可回滚、不碰禁区**。

### 6.1 盘符账本（DRIVE_LAYOUT.md 核心结构）

每个盘符一行：

```text
盘符  类型        状态         已接管目录                          禁区/不碰
D:   数据盘     已盘点        D:\Projects、D:\Media、D:\Downloads   D:\Program Files、D:\WindowsApps、D:\Backup
E:   数据盘     未接管        -                                     -（接管前先盘点）
C:   系统盘     只读/不接管    -                                     C:\Windows、C:\Program Files、C:\Users\*\AppData、密钥/证书
```

- **类型**：系统盘 / 数据盘 / 移动盘 / 网络盘 / 备份盘。
- **状态**：`未接管` → `已盘点` → `已整理` → `只读`（完成后锁定）。
- **已接管目录**：AI 可以在这些目录内做移动/重命名/清理的目录白名单。
- **禁区**：AI 永远不碰的目录/文件类型，优先级高于一切整理需求。

### 6.2 接管流程（必须按顺序）

```text
0. 只读盘点     → 生成 inventory：目录树、文件数、大小、重复/大文件/旧文件候选；不改任何文件
1. 用户确认     → 确认“哪些盘符/目录允许接管”，确认黑名单与移动规则
2. 写账本       → 更新 DRIVE_LAYOUT.md：登记已接管目录与禁区
3. 预演清单     → 先生成本次要移动/重命名的 manifest（before → after）
4. 用户批准     → 涉及用户个人文件的移动/删除必须逐批确认；AI 自己生成的产物可按协议自动
5. 小步执行     → 每批 ≤50 项；每个盘符单独一批；每批执行后立即校验
6. 写审计       → 记录本批 before/after、回滚命令、异常；更新 DRIVE_LAYOUT.md 状态
7. 可回滚       → 发现异常立即停止；用审计日志恢复原路径；不允许“先删再说”
```

### 6.3 硬红线（全盘符通用，不可商量）

1. **不自动删除**：只移到 `_trash/` 或 `archive/`，保留期默认 30 天；删除必须用户明确确认。
2. **不碰系统/程序目录**：`C:\Windows`、`Program Files`、`Program Files (x86)`、`WindowsApps`、系统 `AppData`、注册表、引导文件、虚拟内存。
3. **不碰敏感物**：`.ssh`、`.gnupg`、密钥/证书/密码/令牌、`.git`、`node_modules`、虚拟环境、`.env`、浏览器配置文件、微信/QQ/Discord 等应用数据。
4. **不修改文件内容**：只移动/重命名，不重写文件、不转换格式、不压缩可执行文件、不修改元数据（除非用户明确要求）。
5. **不跨盘符乱挪程序**：程序和系统安装由安装器管理；跨盘符移动只用于文档/媒体/数据/项目等明确资产。
6. **不做隐式覆盖**：目标路径已有同名/同职责文件时停止，标记冲突，不覆盖。
7. **不越权**：未写入 `DRIVE_LAYOUT.md` 的目录 = 未授权，AI 不得整理。
8. **每步可回滚**：无审计日志、无 before/after 清单、无回滚命令，就不执行。

### 6.4 自动 vs 人工的边界

| 场景 | AI 可自动 | 必须用户确认 |
|---|---|---|
| AI 自己创建的临时/中间产物 | 可移入 `scratch/` 或清理（仍留日志） | — |
| 明显垃圾/临时文件（缓存、日志、崩溃 dump） | 可移入 `_trash/`（不删） | — |
| 用户个人文档/照片/下载/桌面 | — | 逐批确认 |
| 程序/系统/配置/密钥 | — | 永远不碰 |
| 跨盘符大迁移 | — | 先盘点、先批准、分批 |
| 删除任何文件 | — | 必须确认 |

### 6.5 审计与记忆更新

- 每次整理后：`DRIVE_LAYOUT.md` 只更新“状态/要点”，完整明细写 `reports/drive-audit-<date>.md` 或 `archive/`。
- `AI_MEMORY.md` 只写一条：`已完成 <盘符> <目录> 整理，状态=<xxx>，详情见 <审计文件>`。
- 若 30 天无动作，AI 应提醒“是否继续接管下一个盘符”，而不是默默扫描全盘。

---

## 7. 来源

### 本地已有规范（一级来源）

- `~/.dsh/AGENTS.md`：深模块、Deletion Test、接口即测试面、文件系统即模块地图、AI 即新人。
- `$HOME/work/AGENTS.md`：工作区模块地图与约束。
- `$HOME/work/REPO_STANDARD.md`：GitHub 仓库施工标准、根目录规则、自动提交协议。
- `$HOME/work/dsh-optimization-consensus.md`：DSH 运维、子代理上限、隔离冒烟与回滚。
- `$HOME/work/editorial-style-spec.md`：文档/视觉风格规范。
- `$HOME/work/SKILL_MAP.md`：技能地图与蒸馏结构。
- `$HOME/work/HANDOFF-NEXT-SESSION.md`：跨会话交接实践。
- `$HOME/work/dsh-skill-vault/vault/skills/base/work-consensus/SKILL.md`
- `$HOME/work/dsh-skill-vault/vault/skills/core-iteration/dev-workflow-consensus/SKILL.md`
- `$HOME/work/dsh-skill-vault/vault/skills/github/github-repo-consensus/SKILL.md`
- `$HOME/work/skills/distillation-consensus-skill/CONSENSUS.md`
- `$HOME/work/skills/dsh-optimization-consensus/CONSENSUS.md`

### 外部公开来源（文件管理/规范）

- [Filesystem Hierarchy Standard — Wikipedia](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard)
- [Ubuntu Filesystem Hierarchy Standard](https://ubuntu.com/project/docs/how-ubuntu-is-made/concepts/filesystem-hierarchy-standard)
- [Google developer documentation style guide · Filenames and file types](https://developers.google.com/style/filenames)
- [The Art of Unix Programming（Unix 哲学）](https://en.wikipedia.org/wiki/The_Art_of_Unix_Programming)
- [12-Factor App（配置与产物分离）](https://12factor.net/)
- [Martin Fowler · Refactoring / Module Dependencies](https://martinfowler.com/)
- [Andrej Karpathy · 公开演讲与博客](https://karpathy.ai/)
- [Lilian Weng · LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [Chip Huyen · Machine Learning Design](https://huyenchip.com/2023/05/02/machine-learning-design.html)

### 专家团结论（2026-09-06 教师会话）

- Karpathy：规范要少而深，文件命名是 AI 的长期记忆接口；硬规则少，结构自解释。
- Lilian Weng：必须覆盖创建→归属→清理→审计闭环，带反例与失效边界。
- Chip Huyen：用可检查目录模板、命名规则、清理周期与自检清单落地，不靠个人品味。
- 裁决：采用“少而深的硬底线 + 完整检查表”的合并方案。
