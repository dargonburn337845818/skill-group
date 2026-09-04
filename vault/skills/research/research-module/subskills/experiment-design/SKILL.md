---
name: experiment-design
description: 实验设计/统计/可复现子技能——从变量与假设到检验、效应量、样本量、可复现清单的可执行检查流程；不替代统计教材，不伪造数据；会议纪要、文书整理等非科研实验设计任务不要加载。
whenToUse: 用户设计实验、选统计检验、解读 p 值/效应量、估样本量、写方法节、评审论文实验部分，或担心“结果可复现吗”时。
---

# 实验设计与统计可复现 · Experiment Design

> 定位：给“科研实验全流程”提供一张可执行检查表，而不是一本统计教材。
> 核心原则：**先定义问题与证据，再选统计工具；先写清楚能重复的流程，再谈结果是否漂亮。**

## 触发条件

- 用户要设计实验/仿真，决定测什么、控制什么、比较什么。
- 用户拿到了结果，要选假设检验、看显著性/效应量、评估样本量是否够。
- 用户要写论文方法节 / 实验设置 / 可复现性说明，或审查别人实验。
- 用户问“我这个 p < 0.05 是不是就够了”“需要多少个样本”。

## 核心动作

### 1. 实验设计与变量（先于数据）

1. **写清目标与假设**：先写一句可证伪的研究问题，再写 H0 / H1；H1 要在看数据前定，不能事后凑。
2. **识别变量**：
   - 自变量 / 处理 / 因子（IV）：你主动改变或分组的变量；
   - 因变量 / 结局（DV）：你测量并比较的指标；
   - 控制变量：保持不变的条件；
   - 混杂变量：可能同时影响 IV 与 DV、必须控制或随机化的因素。
3. **选择设计**：
   - 比较两类/多类：随机对照、组间/组内设计；
   - 多因子：析因设计（factorial），看主效应与交互；
   - 批量/环境差异：加入区组（blocking）与随机化（randomization）；
   - 无法随机分配：观察性研究，结论只能相关/倾向，不能直接因果。
4. **预注册/记录**：把假设、主要终点、分析方法、排除标准在开工前写下来（preregistration / protocol），避免“看到结果再定分析”。

> 边界：设计类型由研究问题与伦理/可行性决定；不能因为“好做”就换成更容易但不回答问题的设计。

### 2. 假设检验的选择

- **先看数据结构与问题**，不要“只要是差异就上 t 检验”。
- 常用对照表：

| 问题 | 常用检验 | 注意 |
|---|---|---|
| 两组均值是否不同 | 独立/配对 t 检验 | 检查正态性、方差齐性；不满足用非参数 |
| 多组均值是否不同 | ANOVA / Kruskal-Wallis | ANOVA 只告诉“有差别”，后续用校正事后比较 |
| 分类变量关联 | 卡方检验 / Fisher 精确检验 | 小样本/稀疏格子用 Fisher |
| 连续变量关系/预测 | 线性/逻辑回归 | 先看残差与过拟合，别只报 R² |
| 重复测量/时间序列 | 混合模型、GEE、重复测量 ANOVA | 需处理个体内相关 |
| 发现/探索 | 聚类、降维、可视化 | 结果是探索性，不能当验证性结论 |

- **检验假设**：独立性、正态性、方差齐性、样本量；不满足时用稳健/非参数或重新设计。
- **p 值正确读法**：p 是在 **H0 为真**时看到“比观测更极端”结果的概率；**不是** H0 为真的概率，也不是效应大小或重要性。
- **报 95% 置信区间**：区间比单个 p 值提供更多信息；同时报告效应量。

### 3. 统计显著 vs 效应量

- **统计显著 ≠ 实际重要**：大样本能让微小差异显著；小样本可能漏掉真实大效应。
- **报告效应量**：均值差 + 标准化效应量（Cohen's d），方差解释比例（η²、R²），风险比/优势比，相关系数等。
- **效应量也要置信区间**：单点效应量同样有抽样不确定性。
- **多重比较**：预先声明主要终点；探索性比较用 FDR/Bonferroni 或只看方向；不要只挑显著的报告。
- **避免“事后功效”（observed power）**：基于观测效应算出的功效没有决策价值，应在实验前用先验效应量做样本量计算。

### 4. 样本量 / 功效分析

| 输入 | 含义 |
|---|---|
| α（通常 0.05） | 允许的假阳性率 |
| Power（通常 0.80） | 真效应被检出的概率 = 1-β |
| 效应量 | 你想检测的最小有意义差异（用先验文献/预实验，不是事后） |
| 变异/波动 | 标准差、方差、事件率 |
| 设计 | 组数、配对/重复测量、协变量、失访率 |

- **正确姿势**：实验前用功效分析估算 N，并把公式/参数写进方法节。
- **样本量不足**：不能“先跑再说”；小样本结果可能只是噪声。
- **样本量过大不等于更好**：超大样本会把几乎没实际意义的差异检验成显著；要结合效应量解释。
- **现实调整**：预留脱落/无效样本；多个主要指标时按多重比较调整。

### 5. 可复现性清单

**数据层**

- [ ] 原始数据保留，不覆盖不删除；记录每个变量的含义、单位、取值。
- [ ] 数据字典/codebook：字段、类型、缺失编码、单位、来源。
- [ ] 清洗脚本化：所有缺失/异常/剔除都有规则与理由，不手动在 Excel 里悄悄改。
- [ ] 元数据与许可清楚，尽量遵循 FAIR（Findable、Accessible、Interoperable、Reusable）。
- [ ] 敏感/受限数据给出访问条件与伪数据示例。

**代码层**

- [ ] 版本控制（git）；分析脚本从原始数据到表格/图的完整链路，不能“半手工”。
- [ ] 固定版本：语言、依赖、随机种子、随机数生成器、运行环境（container/环境文件）。
- [ ] README 写明“怎么装上、怎么跑、多久跑完、输出在哪”。
- [ ] 随机实验设 seed；需要随机性却不可复现时明确标注。

**流程/报告层**

- [ ] 预注册：假设、主要终点、分析方法、停早/排除规则。
- [ ] 方法节写清楚：样本来源、分组/随机化、盲法、参数、统计检验、效应量、软件与版本。
- [ ] 负面/失败结果也报告，不因“不显著”就丢弃。
- [ ] 区分 `reproducibility`（同数据同分析复现同一结果）与 `replicability`（新数据/新实验得到一致结论）。

> 原则：**别人能否按你的描述重跑出一样的图/表/结论**，是比“p<0.05”更硬的可复现性标准。

## 反例 / 常见错误

| 反例 | 正确做法 |
|---|---|
| 跑很多检验，只报显著的那个 | 预先声明主终点；探索性结果标注为探索，并做多重比较校正 |
| 看到结果再编假设（HARKing） | 假设在数据收集/分析前写进预注册 |
| 用“p<0.05”当成效应存在/重要 | 同时报效应量与置信区间，区分统计与实际意义 |
| 用事后功效证明样本够 | 实验前用先验效应量做功效分析 |
| 显著了就说因果 | 观察性数据只能说关联；因果需随机化/设计/理论 |
| 异常值随手删 | 先写剔除标准；做敏感性分析 |
| 只报一个漂亮的 R²，不检查残差/过拟合 | 报模型诊断、交叉验证或独立验证 |
| 数据在 Excel 里手改、代码不可得 | 全链路脚本化 + 版本控制 + 固定环境 |
| “本地能跑就行” | 提供可复现环境与运行说明，最好 CI/容器验证 |

## 边界

- 本技能是**检查框架**，不是统计教材；复杂设计（贝叶斯、生存分析、临床等效、高维组学）需查专门标准或咨询统计师。
- 不生成实验数据，不夸大样本量/效应量；没有真实数据时明确写“待补”。
- 不同学科有不同规范（临床报告 CONSORT、心理学 APA、机器学习基准协议等），以领域规范优先。
- 统计工具的选择要服务于研究问题；不要为了“方法高级”而使用不匹配的模型。
- 对“p 值不显著就失败”保持怀疑：可能真无效应，也可能功效不足、测量噪声、设计有缺陷——要结合设计判断。

## 来源

- [NIST/SEMATECH Engineering Statistics Handbook（DOE / 假设检验 / 统计过程）](https://www.itl.nist.gov/div898/handbook/)
- [Ten Simple Rules for Reproducible Computational Research (PLOS Comput Biol)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285)
- [Good Enough Practices in Scientific Computing (PLOS Comput Biol)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510)
- [Why Most Published Research Findings Are False (PLOS Medicine)](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124)
- [The FAIR Guiding Principles for scientific data management and stewardship (Scientific Data)](https://www.nature.com/articles/sdata201618)
- [GO FAIR: FAIR Principles](https://www.go-fair.org/fair-principles/)
- [Reproducibility and Replicability in Science (National Academies)](https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science)
- [Sample size determination: a practical guide for health researchers (Europe PMC)](https://europepmc.org/article/MED/36909790)
- [The ASA Statement on p-Values: Context, Process, and Purpose](https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108)
- [False-Positive Psychology: Undisclosed Flexibility in Data Collection and Analysis](https://doi.org/10.1177/0956797611417632)
