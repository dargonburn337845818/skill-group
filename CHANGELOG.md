# Changelog

## Unreleased

- 新增 DSH / DeepSeek Harness 开发与运维专家团：`tianyi-cui`、`huba-king`、`noob-stupid`、`cloga`、`sirius-wj`、`ninipa`，并在 `domain-profiles.json` 注册 `dsh-ops` 领域（status=ready）。
- 继续扩充 DSH 专家团：`leonardoxr`、`y08lin4`、`elmaxid`，`dsh-ops` 目前共 9 位 ready 专家。
- 追加 DSH Agent 团队/完整 coding agent 作者：`wowyuarm`、`huiliyi37`，`dsh-ops` 目前共 11 位 ready 专家。

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
