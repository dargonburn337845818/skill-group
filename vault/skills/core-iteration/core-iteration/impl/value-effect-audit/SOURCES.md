# value-effect-audit · 来源声明

| 来源 | 贡献 |
|---|---|
| 用户规格：认知收益架构 / 价值驱动递归提升模块 | 效果反馈回路设计 |
| 本地 `benefit-filter` / `value-iterator` / `value-validator` | 上游/下游接口 |
| [OpenAI: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | 用真实评测衡量 skill 能力 |
| [Convergence Protocol](https://inferensys.com/glossary/recursive-error-correction/iterative-refinement-protocols/convergence-protocol) | 迭代停止/效果确认的启发式 |

说明：效果分数公式是本模块内部设计，须配合真实任务数据校准，不视为外部共识。

## Round 40 新增来源

| 来源 | 贡献 |
|---|---|
| [Anthropic: Improving skill-creator — Test, measure, and refine Agent Skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) | skill 测试、度量、回归检测与描述改进的官方闭环 |
| [OpenAI: Build an Agent Improvement Loop with Traces, Evals, and Codex](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop) | Traces → Evals → 改进的反馈回路示例 |
| [AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688) | 多域真实任务集，交叉测量代理能力而非单点指标 |
| [SWE-bench: Can Language Models Resolve Real-world GitHub Issues?](https://github.com/SWE-bench/SWE-bench) | 真实仓库 issue 作为受控任务基准与可复现评测 |
| [Kohavi, Tang, Xu: Trustworthy Online Controlled Experiments](https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59) | A/B 实验的主指标、护栏、统计判断与常见陷阱 |
| [National Academies: Analysis Through Triangulation and Synthesis](https://www.nationalacademies.org/read/18739/chapter/9) | 混合方法评估中的三角互证与交叉验证 |
| [Huidrom & Belz: Using LLM Judgements for Sanity Checking Results and Reproducibility of Human Evaluations in NLP](https://aclanthology.org/2025.gem-1.30/) | LLM 评分与人工评估的一致性、可复现性检验 |
| [Label Studio: Static vs. dynamic benchmarks](https://labelstud.io/learningcenter/static-vs-dynamic-benchmarks/) | 静态基准泄漏问题与动态真实任务评测的必要性 |
