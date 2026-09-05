# Changelog

## Unreleased
- **v0.2.7 内容蒸馏补强完成（Round 39–40，收敛）**：
  - 最后 10 个注册技能完成搜索/蒸馏补强：benefit-filter、inspiration-miner、return-forensics、value-effect-audit、value-iterator、value-validator、web-research-consensus、dev-network、eval-task、nvidia-laptop-tuning。
  - vault 正式注册技能 **50/50 全部包含内容补强章节**；包检 50/50、本地 20/20、validate-vault/tags OK。
- **v0.2.6 内容蒸馏补强（Round 36）**：
  - 第六批 6 个模块壳/协议技能：dev-design-aesthetics / expert-team / teacher-module / writing-module / dev-module / research-module。
  - 每个技能追加高质量来源蒸馏出的新规则/反例/示例并更新 SOURCES；校验全绿。
- **v0.2.4 内容蒸馏补强（Round 34）**：
  - 第四批 6 个技能：prompt-writing / document-report / speech-writing / career-path / teacher-math-consensus / submission。
  - 每个技能追加高质量来源蒸馏出的新规则/反例/示例并更新 SOURCES；校验全绿。
- **v0.2.3 内容蒸馏补强（Round 33）**：
  - 第三批 6 个技能：paper-reading / paper-writing / group-meeting / research-ppt / mentor-review / dev-art-ppt。
  - 每个技能追加高质量来源蒸馏出的新规则/反例/示例并更新 SOURCES；校验全绿。
- **v0.2.2 内容蒸馏补强（Round 32）**：
  - 对 dev-security / dev-frontend / dev-testing / dev-performance / copywriting / paper-outline 搜索并蒸馏新增 36 条可执行规则/反例/示例，新增 73 条权威来源。
  - 每个技能追加 “2026 深度补强（Round 32）” 章节并更新 SOURCES 台账；未改 manifest、未删旧内容。
  - 校验：vault 包检 50/50、本地 20/20、validate-vault/validate-tags OK。

- **v0.2.1 存量技能库质量翻新（Round 31）**：
  - 50 个 vault 注册 skill 全部补齐 `whenToUse` / `SOURCES` / `CHANGELOG` / `examples`，`skill_package_check` 100 分。
  - 修复内容级问题：`dsh-optimization-consensus` 补脚本与触发节、`skill-management` 失效引用、`research-module` 专家状态、`vlpc-consensus` 来源与 DOI、`nvidia-laptop-tuning` tags 超限、core-iteration 工具路径统一为 `$CORE_ITERATION_ROOT/tools/`。
  - 本地源目录同步补齐 manifest 与门禁，20/20 包检 100 分。
  - 校验：`validate-vault` OK（22 skills）、`validate-tags` OK（50 manifests）。

- **v0.2.0 专家团标准化与全量补全**：
  - 新增 `vault/skills/teacher/expert-team/SKILL.md`：任意模块（dev/writing/teacher/research/distill）统一的专家团调用协议。
  - 48 个专家包全部补成完整 `style_items` + `POSITION.md`（算法 10、前端 3、科研 6、性能 2 同步），不再有“待补”占位。
  - dev / writing / research / distill / teacher 模块壳与 `modules.json` 均列出默认专家团，并引用 `expert-team` 标准流程。
  - vault 设置页展示每个正式模块的“专家团”与跨模块标准流程入口。
  - 修复 `work-consensus` / `dsh-optimization-consensus` / `vlpc-consensus` 包检红灯；`validate-vault` 全绿（19 skills）。


- `dsh-optimization-consensus` 升至 0.1.1：新增 `DUAL_END_UPDATE.md`（WSL/Windows 双端交叉更新实战规范，含 15 条踩坑、标准顺序、验证与回滚清单）；同步更新 SKILL/CONSENSUS/机器级 `~/.dsh/dsh-optimization-consensus.md`。
- 新增 DSH / DeepSeek Harness 开发与运维专家团：`tianyi-cui`、`huba-king`、`noob-stupid`、`cloga`、`sirius-wj`、`ninipa`，并在 `domain-profiles.json` 注册 `dsh-ops` 领域（status=ready）。
- 继续扩充 DSH 专家团：`leonardoxr`、`y08lin4`、`elmaxid`，`dsh-ops` 目前共 9 位 ready 专家。
- 追加 DSH Agent 团队/完整 coding agent 作者：`wowyuarm`、`huiliyi37`，`dsh-ops` 目前共 11 位 ready 专家。
- 并入通用 DevOps 运维视角：`kelsey-hightower`、`charity-majors`、`cindy-sridharan`，`dsh-ops` 目前共 14 位 ready 专家（>8 时主持人建议默认选 3–5 人）。

## 0.1.0 (2026-09-04)

- 正式版五模块：dev / distill / teacher / research / writing。
- 教师运行时：领域识别、人名专家团（ready/gap 分支）、回合式讨论。
- 扩展 manifest 字段：routing / qualityCriteria / boundary / notWhenToUse / activation。
- 新增 `/skill-vault/api/route`、`/reset-base`、`/teacher/*` 端点。
- 补充社区文件、CI 与 GitHub Release 自动打包。

## 0.0.1 (2026-09-04)

- Hybrid 插件：agent 工具 + Web 可视化开关面板。
- 开源 skill vault：base / core-iteration / dev / distill / teacher / research / writing / dsh-ops / github 等场景。
- 场景级 + 单 skill 级开关；全局持久 + 会话临时覆盖。
- 教师模块：领域识别、人名专家团、回合式讨论。
- GitHub Actions：发布插件 Release。
