# Return-Forensics 干跑样例

## 场景：收益下降

- 输入：本轮 effective_new=1，上轮 effective_new=10，高优剩余率 0.05。
- 预期：`root_cause` 命中“边际收益衰减/语料枯竭”，`one_action` 指向“换信息范围或补真实效果”。
- 检查：trace_chain 保留降权节点，不删历史。

## 场景：没料 vs 没转化

- 输入：raw=0 但 nodes 无变化。
- 预期：root_cause=source_saturation 而不是 distillation_loss。
