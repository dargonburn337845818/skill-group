# 模拟导师团队审查流程示例 · NOMA-VLPC 论文

> 场景：学生准备用一篇 IEEE WCL 2026 的 NOMA-VLPC 短论文做组会报告。
> 本文件演示“学生汇报 → 各导师提问 → 问题点/创新点汇总 → 建议下一步”的标准流程。
> 所有导师意见均为**基于其公开论文/领域工作的风格与方法论推断**，不是本人原话；
> 说话人姓名与来源见表格。

---

## 1. 学生汇报（口述摘要）

> 这篇论文做一体化可见光定位与通信（VLPC）：同一个 LED 的直流分量用于定位，
> 交流分量用于 NOMA 通信。定位侧用双相编码 + 多数投票 + 两阶段指纹库，
> 通信侧按信道强弱排序做 SIC，并在总功率固定时给出最优直流功率解析式。
> 实验误差约 13 cm，复杂度比元启发式低。

---

## 2. 各导师提问

### 第一轮：系统架构

- **【Ting Yang · 系统架构 / VLPC】**
  - 问题：为什么选择“DC 定位 / AC 通信”的拆分，而不是让 AC 同时承担定位与通信？如果换一种拆分，系统哪部分会最先崩？
  - 依据：论文 System Model；S. Ma et al., IEEE TCOM 2023（波形设计）。

- **【Ping Wang · 定位 / 信号处理】**
  - 问题：双相编码解决的是消息随机性造成的直流漂移；如果是 LED 非线性或背景光造成的漂移，这套方案还剩多少鲁棒性？
  - 依据：论文 Positioning Scheme；指纹定位文献 [10][11][12]。

- **【S. Ma · 波形与资源分配】**
  - 问题：最优直流功率 `Idc² = K/(K+1)·Ptotal` 基于理想线性 LED；加入非线性后，拐点会往哪个方向偏？
  - 依据：论文 Optimal DC Power Setting；S. Ma et al., IEEE TCOM 2023。

- **【Y. Chen · 实验 / 可复现】**
  - 问题：13 cm 误差里，指纹库网格间隔、环境光照变化、同步误差各占多少？如果换房间，结论还能复现吗？
  - 依据：论文 Experimental Results；IEEE Access 2020 fingerprinting+ELM 工作。

---

## 3. 问题点汇总

| # | 问题 | 提问导师 | 严重度 | 证据/依据 |
|---|---|---|---|---|
| Q1 | DC/AC 拆分的边界条件是什么 | Ting Yang | 中 | 论文 System Model |
| Q2 | 双相编码只抗消息随机性，不抗环境噪声 | Ping Wang | 高 | 论文 Positioning Scheme |
| Q3 | 解析最优功率基于理想线性 LED | S. Ma | 高 | 论文 Optimal DC Power Setting |
| Q4 | 13 cm 误差来源未细分 | Y. Chen | 中 | 论文 Experimental Results |

## 4. 创新点汇总

| 创新点 | 支撑证据 | 值得深挖的导师 | 风险 |
|---|---|---|---|
| 单 LED 实现定位 + 通信一体化 | 论文 System Model / Working Principle | Ting Yang | 是否依赖强假设 |
| 双相编码 + 多数投票 + 两阶段定位 | 论文 Positioning Scheme | Ping Wang | 指纹库维护成本 |
| 解析最优 DC 功率（O(1)） | 论文 Optimal DC Power Setting | S. Ma | 理想线性模型 |
| 指纹+投票在 4cm 目标下快于元启发式 | Table II / Complexity Analysis | Y. Chen | 只在一个精度目标下对比 |

## 5. 冲突点与裁决

| 冲突 | 主张 A | 主张 B | 裁决建议 |
|---|---|---|---|
| 是否值得继续深挖 | 【Ting Yang】系统级一体化是趋势，值得做 | 【Ping Wang】指纹库依赖太强，落地受限 | 保留分支：先做仿真验证非线性和环境变化，再决定 |

## 6. 建议下一步

1. **补环境鲁棒性分析（建议者：Ping Wang）**：在现有模型上加 LED 非线性、背景光、同步误差，看最优功率拐点与定位误差变化。
2. **做误差分解实验（建议者：Y. Chen）**：固定网格间隔、改变光照/同步误差，量化 13 cm 误差来源。
3. **扩展 DC/AC 分工边界（建议者：Ting Yang）**：比较 AC 同时定位通信的方案，验证“必须拆分”的假设。
4. **写作/表达（参考：William Zinsser，候选）**：把“一句话定位”放在摘要第一句，避免读者先看到术语。

## 7. 来源

- [NOMA-VLPC 论文：IEEE LWC 2026, DOI 10.1109/LWC.2026.3660446]
- S. Ma et al., Waveform Design and Optimization for Integrated VLPC, IEEE TCOM 2023
- Multi-user grouping for NOMA enabled VLC system, IEEE Commun. Lett. 2024
- SIC-free based indoor two-user NOMA-VLCP system, Photonics 2024
- Indoor real-time 3-D visible light positioning system using fingerprinting and extreme learning machine, IEEE Access 2020
- 本地材料：`vault/skills/research/vlpc-consensus/vlpc_teacher_consensus.json`

> 注：DOI 以本地 vlpc-consensus 材料的 `paper:10.1109/LWC.2026.3660446` 为准；
> 若与正式出版信息不一致，以论文原文为准。
