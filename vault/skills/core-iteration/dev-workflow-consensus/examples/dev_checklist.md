# 开发门禁检查表（示例）

## 规格前

- [ ] 北极星：为谁 / 处境 / 可观测结果 / 非目标
- [ ] 模块地图：模块 / 职责 / 公开接口 / 测试入口
- [ ] Deletion Test 结论：删掉会不会让复杂度散落？

## 规格

- [ ] L1/L2 spec / accept / do / verify 齐全
- [ ] accept 可被第三方检查，不写“看着没问题”

## 对抗审查

- [ ] 独立视角给出 BLOCKER / GAP / NOTE（或“none found” + six checks）
- [ ] BLOCKER 已清零才进入 Gate

## 执行

- [ ] 子代理简报含文件所有权/不变量/命令/验收
- [ ] 模型分层（haiku/sonnet/opus）按职责
- [ ] 重叠文件串行；子代理不碰 git
- [ ] 同一文件第 3 次不收敛 → churn-breaker 换 agent

## 验证

- [ ] 测试通过公开接口
- [ ] 关键检查 checks_observed_red 非空（故意破坏→变红→恢复→变绿）
- [ ] 无 in-flight 验证时才能标 PASS

## 终验

- [ ] 真实启动/冒烟通过
- [ ] accept 逐条有证据
- [ ] redteam 项已独立裁决
- [ ] 模块地图 / README / 路径手册已同步
