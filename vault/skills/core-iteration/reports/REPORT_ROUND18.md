# Round 18：标准轮次/收益/收敛报告结构

> 方向：让每轮都能看到“轮次、收益、是否收敛”。

## 新增

- `meta_report.py` 输出标准结构：
  - `round`
  - `yield_curve`（raw / verified_high / verified_single / nodes / effective_new / decision）
  - `convergence`（status / converged / stop_reason / expected）

## 当前状态

```text
Round 18
raw_count=15
verified_high=2
verified_single=15
nodes=17
effective_new=17
decision=CONTINUE
convergence=CONTINUING
root_cause=cross_verification_progress
```

## 验证

- validate_contract / behavior / smoke 均 PASS
- workspace + vault 同步 OK
