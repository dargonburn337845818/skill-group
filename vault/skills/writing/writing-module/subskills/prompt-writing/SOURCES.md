# Sources（prompt-writing）

> 来源台账。公开链接可在浏览器复核；核心规则在 `SKILL.md` 的 Round 34 深度补强节带来源标注。

## Round 34 新增来源

| # | 来源 | 贡献规则 |
|---|---|---|
| 1 | [OpenAI Cookbook · Building resilient prompts using an evaluation flywheel](https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel) | 固定测试集、定义成功标准、版本化 prompt、对比回归；一次只改一处并保留回退 |
| 2 | [OpenAI · Prompt engineering guide](https://platform.openai.com/docs/guides/prompt-engineering) | 清晰指令、分隔指令与数据、让模型先问澄清问题、拆分复杂任务 |
| 3 | [Anthropic · Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) | 分节组织（标签/XML）、角色与边界、迭代测试 |
| 4 | [Anthropic · Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | 角色定义、具体直接、正面指令、think/show your work 的使用边界 |
| 5 | [Google · Gemini prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) | 给上下文与示例、明确输出格式、正负例并用、复杂任务分步 |
| 6 | [Microsoft Learn · Prompt engineering techniques (Azure OpenAI)](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering) | 目标明确、拆任务、给示例、系统消息、迭代评估与温度调整 |
| 7 | [Prompting Guide · Techniques (DAIR.AI)](https://www.promptingguide.ai/techniques) | 角色提示、few-shot、CoT、自洽性、ReAct 等技法分类与适用边界 |
| 8 | [Wei et al. · Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) | 多步推理需先列中间步骤；提供样例化的思维链可提升推理准确率 |
| 9 | [Wang et al. · Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) | 多次采样取多数/共识，降低单路径推理错误；用于高利害判断与评测 |
| 10 | [Yao et al. · ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) | 推理—行动交替并维护最新状态；多轮/工具场景下要更新“已知/待办” |
