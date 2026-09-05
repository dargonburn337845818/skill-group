# Quick Use：dev-ai-engineering

> 一句话：LLM/Agent 工程子技能：LLM API 契约、上下文预算与持久化、RAG 检索、工具调用契约、Agent 循环、评测与降级/成本边界的可执行检查清单。

## 何时用

- 当任务命中 `SKILL.md` 的“触发条件 / 何时使用”时。

## 最小可复现动作

- 用户要接 LLM API、写 prompt/系统提示、做 RAG、设计工具/MCP、跑 Agent 循环。
- 需要审查一个 AI 方案：上下文会不会爆、检索会不会瞎、工具能不能被模型正确使用、失败时怎么降级。
- 用户问“这个 Agent 怎么不收敛 / 成本怎么控 / 怎么证明改进了”。
- **模型与版本显式固定**：在配置/环境记录 provider、model、版本或日期；不要只写“gpt-4”之类会漂移的短名。

## 验证方式

- 按 `SKILL.md` 的干跑/检查清单执行；
- 发布/更新前跑 `skill_package_check.py` 与本 skill 对应校验。
