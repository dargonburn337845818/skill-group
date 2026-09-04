# 突变检查记录（checks observed red）

1. 初始 `scaffold_eval_task.py` 生成的 verifier 只检查 `SUCCESS_MARKER`。
2. 第一次真实 A/B：输出包含全部任务要求，但不含 `SUCCESS_MARKER` → verifier 判定 FAIL（见 `evals/dev-ai-pilot/ab.json` 旧轮次），确认检查**见过红**。
3. 替换 verifier 为真实需求标记（上下文预算/RAG/评测/降级/CHECKLIST_OK）→ 重跑 3 次全部 PASS（绿）。
4. 结论：检查可证伪；不是只跑通一次的自说自话。
