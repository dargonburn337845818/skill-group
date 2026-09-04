# 技能库分类法（Tag Taxonomy）

> 本文件是 `dsh-skill-vault` 的分类契约：回答“新 skill 放哪、小标签怎么打、哪些词不许进 tags”。
> 原则：**大类（场景）决定“出现在哪”，小标签只做横向检索，不承担状态/模块/路由职责。**

## 1. 四条分类轴，各管一件事

| 轴 | 字段/位置 | 决定什么 |
|---|---|---|
| 场景 `scenario` | 目录 + `manifest.scenario` | UI 分组、场景级开关 |
| 路由 `routing` | `manifest.routing` | `base` 常驻 / `core` 核心元能力 / `domain` 领域 |
| 模块 `module` | `vault/meta/modules.json`（本地任务分派未随公开仓库发布） | 正式协作模块：dev/distill/teacher/research/writing |
| 标签 `tags` | `manifest.tags` | 只做横向检索（按主题、领域、生态找 skill） |

状态/成熟度（`activation`、`hidden`、CHANGELOG、`status`）一律不进 tags。

## 2. 新 skill 放哪：决策树

1. 所有任务都要先加载的共识/底座 → `base/`，`routing=base`，`activation=always-on`
2. 核心迭代元能力的一部分 → `core-iteration/`，`routing=core`；内部原语放 `core-iteration/impl/`，**不独立注册**
3. 五模块之一的子能力 → 对应模块目录下 `module/subskills/`，`activation=internal`
4. 跨模块复用的领域通用能力 → 选一个“第一使用场景”做目录，`scenarios` 声明交叉场景，`routing=domain`
5. DSH 运维 / 发布 / GitHub 工具 → `dsh-ops/` 或 `github/`
6. 以上都不是 → 先不入库；先回答“服务哪个模块的哪个 gap”

## 3. 标签受控词表

标签数 **≤ 8**，只允许以下五类：

| 类别 | 示例 |
|---|---|
| 领域 | 算法竞赛、前端、后端、安全、性能、数学、物理、科研、写作 |
| 能力 | 搜索、来源、核验、蒸馏、迭代、收敛、验证、评测、审计、教学 |
| 对象/产物 | PPT、API、组件、提示词、文案、报告、清单、规范 |
| 生态/标准 | GitHub、OSV、OWASP、WCAG、NNG |
| 模块复用 | dev、teacher、research、writing、distill（仅跨模块复用时） |

### 允许的固定术语（建议直接使用）

- 搜索、来源、核验、GitHub、学术
- 深模块、重构、模块地图、接口测试、AI友好
- DSH运维、热更、子代理、回滚、升级安全
- 蒸馏、元能力、迭代、收敛、价值、收益、回填、Gap、专家蒸馏
- 开发、规格、验证、红队、证据、审计、可证伪、插件
- 开发模块、子技能、入口
- 后端、API、数据模型、服务分层、前端、组件、状态管理、可访问性
- 并发、竞态、锁、异步、性能、优化、profiling、基线
- 测试、调试、flaky、最小复现
- 安全、信息安全、OWASP、威胁建模
- 美术、PPT、演示、图表
- 设计、美学、视觉、UI、无障碍、风格边界
- AI味、文案、可读性、去模板化
- 科研、论文、组会、导师团队、多agent、VLPC、物理、定位
- 教师、专家团、回合式讨论、裁决、领域识别、人名专家
- 算法竞赛、熵减盘问、信息论、拆题
- 文稿、提示词、报告、文本服务、去AI味
- skill、管理、开关、DSH插件、vault、发布、入库、git
- GitHub、开源、README、隐私、目录结构、Actions

### 禁止进 tags

- 状态词：`已蒸馏`、`已填充`、`挂载`、`底座挂载`、`done`、`pending`
- 结构/重复大类：`模块`、`编排层`、`元能力`（当它已是场景/路由时）、`开发`（当它已是 `dev` 场景时）
- 英文内部一次性术语：`trace`、`for`、`Jaccard` 除非是技术上必要的固定术语
- 把 `routing` / `activation` / `hidden` 写成 tag

## 4. 内部实现（impl / subskills）标签规则

- `core-iteration/impl/*`、`dev/subskills/*` 等内部包保留简短主题标签，但不参与公开检索。
- 公开可注册 skill 的 tags 由 `scripts/validate-tags` 校验；内部包同样禁止状态词。

## 5. 常见易混对

| 目录 | 是什么 | 不是什么 |
|---|---|---|
| `teacher/teacher-module` | 教师模块壳（多 agent 讨论协议） | 不是算法教学领域内容 |
| `teaching/teacher-consensus` | 算法教学领域内容 | 不是教师模块壳 |
| `distill/distill-module` | 蒸馏编排层 | 不是内容蒸馏算法库 |
| `distillation/ui-aesthetics-design` | 跨 dev/research 的 UI 通用能力 | 不是“内容蒸馏”主题 |
| `core-iteration/impl/*` | 核心迭代内部原语 | 不独立注册、不单独出现在 UI |

## 6. 维护

- 新增/修改 skill 时，按本文第 2、3 节走一遍。
- 提交前运行 `node scripts/validate-vault.mjs`；本仓库新增 `scripts/validate-tags.mjs` 作为 tag 专项检查。
