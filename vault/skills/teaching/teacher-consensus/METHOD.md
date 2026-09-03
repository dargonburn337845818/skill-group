# 蒸馏方法：从顶尖选手的思路到静态概率矩阵

> 本文件是对 `SKILL.md` 的展开。它回答一个问题：
> 如何把 tourist、jiangly 等选手“很少写出来”的直觉，变成可回测、可编译进静态软件的概率结构？

---

## 0. 核心判断

顶尖选手的解题思路不能靠“读完几篇博客就总结”，也不能靠“把专家语录堆成一篇长文”。

真正可用的蒸馏是三步：

```text
专家文本 + 信息论框架
   → 可审计的思维原语（primitive）
   → 可计算的条件概率 P(feature | algorithm)
   → 可回测的熵减盘问流程
```

---

## 1. 冻结本体（Ontology）

在开始收集语料前，先确定“我们要蒸馏成什么东西”。

建议直接复用 `knowledge-ladder-repo` 已有的结构，不要另造新体系：

- 4 个方向：编码压缩 / 传播松弛 / 剪枝决策 / 变换域映射
- 20 个基础特征问题（shape / metric / scale / monotonic / dependency …）
- 120 个本地算法
- 熵减引擎：贝叶斯更新 + 信息增益选问题

专家文本先映射进这套本体。只有当一个想法被多个独立来源支持、且无法装入现有 feature 时，才新增 feature。

---

## 2. 建语料库

### 2.1 优先级

1. **选手亲写的题解 / editorial**
   - Codeforces、AtCoder、Topcoder 官方题解
   - 高端选手在博客里对某道题的完整分析
2. **访谈 / 赛后总结**
   - tourist 的 TCO 访谈、Codeforces 采访
   - jiangly 的代码风格和解题习惯相关讨论
3. **提交记录 + diff**
   - 能反推“先写什么、后优化什么”
4. **信息论著作**
   - Shannon《通信的数学理论》
   - Cover & Thomas《Elements of Information Theory》
   - MacKay《Information Theory, Inference, and Learning Algorithms》
   - Jaynes《Probability Theory: The Logic of Science》
   - Li & Vitányi《Kolmogorov Complexity》

### 2.2 采集原则

- 每个原始想法都要有来源。
- 同一想法至少找 2–3 个独立来源，再升为 `consensus`。
- 无法追溯的圈内共识标记为 `common-lore`，并降低进入矩阵的权重。

---

## 3. 切成推理片段（Episode）

一篇题解不要整体“总结”，要切成可标注的最小推理单元：

```text
问题上下文
→ 我观察到什么
→ 我暂时试了什么
→ 为什么有效 / 失效
→ 最终选了什么
→ 什么边界会推翻这个想法
```

示例：

```text
原文：
  “Since the answer is monotone, we can binary search the minimum number of days.”

Episode：
  trigger: 求最早可行天数，可行性随天数单调
  action: 二分答案
  direction: 剪枝决策
  feature: monotonic
  counterexample: 如果 check 不可贪心/不单调，二分失效
```

---

## 4. 聚合成思维原语（Primitive）

把多个 episode 中“同一件事的不同说法”合并，生成 primitive。

### 合并规则

- 先去重：不同专家说“先写暴力”和“先做 naive”，是同一原语。
- 拆分：一个长原语如果包含两种独立动作，要拆成两个。
- 记录分歧：如果专家 A 主张先构造，专家 B 主张先搜索，不要平均，保留为两个 branch。

### 输出结构

每个 primitive 使用 `SKILL.md` 中的 JSON schema。  
建议单独维护一个 `teacher_consensus.json`，然后通过脚本合并进 `feature_algorithm_matrix.json`。

---

## 5. 共识分级

| 级别 | 判定标准 | 矩阵处理 |
|---|---|---|
| consensus | ≥2 个独立来源，且圈内普遍认可 | 直接进入主矩阵 |
| style | 单专家偏好 | 可作为“风格分支”，低权重 |
| warning | 常见错误 | 作为反指示，用于“我感觉不对劲”诊断 |
| common-lore | 无直接引用，但符合常识 | 中等置信，需回测验证才可升 consensus |

不要给“风格”和“共识”同样高的权重，否则会制造虚假的确定性。

---

## 6. 量化：从 primitive 到概率

这是整个方法中最关键、也最容易被跳过的一步。

### 6.1 三路概率

```text
P_final(feature | algorithm)
= α · P_expert
+ β · P_oj_stats
+ γ · P_sample_calibration
```

- `P_expert`：从 primitive 中提炼的专家直觉概率。
- `P_oj_stats`：现有 `algorithm_prior.json` 中的标签/组合统计。
- `P_sample_calibration`：从 OJ 抽样题目，让老师/AI 回答 feature 问题后统计出的经验频率。

权重初始建议：

```text
α = 0.3
β = 0.3
γ = 0.4
```

如果某个 primitive 的 `confidence` 很低，就把 α 降下来。

### 6.2 抽样校准

对于一个算法簇（例如“二分答案”），做法：

1. 从 Codeforces / AtCoder / DMOJ 中抽出 20–50 道带该算法标签的题。
2. 让老师或 AI 阅读题面，逐个回答：
   - 这题是否有单调性？
   - 是否是多查询？
   - 是否允许离线预处理？
   - …
3. 统计每个 feature 的真值比例，做 Beta 平滑：

```text
P_calibrated = (count_true + prior_strength * P_expert) / (count_total + prior_strength)
```

这一步能把“专家觉得是这样”变成“数据证明是这样”。

### 6.3 新 feature 的准入

新增一个 feature 前，要满足：

1. 有至少 2 个独立专家 primitive 支持。
2. 在抽样数据中能区分出不同算法（即 `I(feature; algorithm)` 明显大于 0）。
3. 能在回测中降低平均提问数或提高 top-k 命中率。

否则它就是“听起来很酷但没用”的问题，应该删掉。

---

## 7. 回测与迭代

### 7.1 回测集

选 50–100 道已知道题目标签的题目：

- 包含不同难度、不同算法簇。
- 不要只选“擅长领域”的题，要故意包含冷门组合。

### 7.2 指标

| 指标 | 说明 |
|---|---|
| Top-1 / Top-3 命中率 | 最终候选算法是否覆盖真实算法 |
| 平均提问数 | 是更省问题，还是更啰嗦 |
| 收敛熵 | 停止时是否真的够确定 |
| 用户“不对劲”率 | 是否频繁触发人类接管 |
| 校准误差 | 预测概率与真实标签频率的偏差 |

### 7.3 迭代顺序

```text
先跑一轮基线（现有矩阵）
→ 加入 primitive 后跑一轮
→ 只保留让指标变好的 primitive
→ 有争议的 primitive 进入“shadow 模式”不展示
→ 再跑 2–3 轮，稳定后编译成静态 JSON
```

---

## 8. 最终产物

建议目录：

```text
teacher-consensus-skill/
├── SKILL.md                    # 教师共识 + 提问协议
├── METHOD.md                   # 本文件
├── schema/
│   └── primitive.schema.json   # primitive 校验 schema
├── examples/
│   └── sample_consensus.json   # 示例 primitive
├── prompts/
│   ├── extract_episodes.md     # 题解 → episode 提取 prompt
│   ├── cross_validate.md       # 多源交叉验证 prompt
│   └── sample_calibrate.md     # OJ 抽样校准 prompt
└── output/
    ├── teacher_consensus.json  # 机器可读共识
    └── matrix_patches.json     # 对现有矩阵的增量修正
```

在未稳定前，不要直接改动 `knowledge-ladder-repo`。  
先在草稿目录跑完 `extract → validate → calibrate → backtest`，再决定合并。
