# Changelog

## 0.2.0 — 2026-09-04

- 实现教师模块运行时：`src/teacher.ts` 回合式讨论会话存储。
- 注册 agent 工具：`teacher_discussion_start` / `teacher_discussion_round` / `teacher_discussion_status` / `teacher_expert_select` / `teacher_discussion_finish`。
- 新增 HTTP API：`/skill-vault/api/teacher/start|round|select|finish|status`。
- 侧边栏过程监视器接入真实 `/teacher/status` 数据，并在不可用时回退占位。
- 更新 SKILL/discussion-protocol/expert-selection 文档为“已实现”接口。

## 0.1.0 — 2026-09-04

- 创建教师模块 teacher-module：领域识别 + 人名专家团 + 回合式讨论协议。
- 充实 `EXPERT_LIBRARY.json`：算法竞赛新增 ready 人名专家（benq / um-nik / errichto / ecnerwala / radewoosh / neal / rng-58 / petr）。
- 充实 `domain-profiles.json`：算法竞赛 expert_ids 扩展为 10 位 ready 专家。
- 新增 `discussion-protocol.md`、`expert-selection.md`、`examples/round_discussion.md`。
- 更新本地 `assignments/teacher/assignment.json` 状态为 done（内部开发记录）。
