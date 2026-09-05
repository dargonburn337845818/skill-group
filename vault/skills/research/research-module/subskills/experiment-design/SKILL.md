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
- 不生成实验数据，不夸大样本量/效应量；没有真实数据时明确写“后续”。
- 不同学科有不同规范（临床报告 CONSORT、心理学 APA、机器学习基准协议等），以领域规范优先。
- 统计工具的选择要服务于研究问题；不要为了“方法高级”而使用不匹配的模型。
- 对“p 值不显著就失败”保持怀疑：可能真无效应，也可能功效不足、测量噪声、设计有缺陷——要结合设计判断。

## 2026 深度补强（Round 35）

> 本轮新增：把“样本量论证、等效性、回归系数解释、回归诊断、预注册自由度、效应量语境、多重比较、复现验收”由定性提醒升级为可勾选动作。新增来源见 `SOURCES.md` `Round 35 新增来源`。

### 1. 样本量论证：先定“最小有意义效应”，必要时做敏感性功效分析

- 不要只写“d=0.5、power=0.8、α=0.05”：这三个数只有在说明“为什么 0.5 值得检测”后才成立。
- 可执行顺序：
  1. 定义 **SESOI**（smallest effect size of interest）：低于它，即使显著也不值得写进结论；
  2. 没有可靠 SESOI 时，做 **sensitivity power analysis**：固定 α、power 与样本量，算出“当前设计能可靠检测到的最小效应”，并与实际/理论重要性比较；
  3. 报告效应量来源（文献 meta 分析 / 预实验 / 最保守猜测），并写明“若真实效应小于可检测效应，本研究只能算证据不足，不是无效应”。
- 示例：N=40/组 可检测 d≈0.63，而领域公认最小重要差异 d=0.3 → 结论写“本设计只能排除 d≥0.63 的大效应；对 d=0.3 证据不足”，不要写“未发现效应”。
- 来源：Lakens (2022) *Sample Size Justification*；Button et al. (2013) *Power failure*。

### 2. “不显著” ≠ “等效/无差异”：下等效结论请在事前设定界值并做 TOST

- p > .05 只说明“当前数据不足以拒绝 H0”；它可能是功效不足、测量噪声或真实效应小。
- 要声称“两组实际等效/无临床差异”，必须做 **equivalence testing**（例如 TOST：两个单侧检验，预设等效界值 Δ）。
- 可执行：预先设定 Δ（如均值差不超过 0.2 SD，或某个临床容忍度），报告 TOST 结果与 90% CI 是否落在 [−Δ, +Δ]；不要用“未显著”反推等效。
- 反例：p=.07 后写“两组无差异”→ 错；应写“未能拒绝无差异；当前功效不足以排除 Δ=0.2；需等效性设计”。
- 来源：Lakens, Scheel & Isager (2018) *Equivalence Testing for Psychological Research: A Tutorial*；Greenland et al. (2016)。

### 3. 回归系数：先统一单位/标准化，再解释方向与交互

- 连续预测变量的原始系数依赖单位，跨研究不可比；报告“每 1 个自然单位”或“每 1 SD”并明说。
- 有交互作用时，先对连续变量**中心化/标准化**再拟合；否则主效应只是“另一个变量=0”的条件效应，容易被误读为平均效应。
- 至少报告：系数 + 置信区间 + 单位/标准化说明 + 模型诊断；不能只报 p 或 R²。
- 示例：身高（cm）系数 0.03 与身高（m）系数 3 是同一模型；要跨研究累积必须统一到 SD 或明确单位。
- 来源：Schielzeth (2010) *Simple means to improve the interpretability of regression coefficients*。

### 4. 回归诊断：按顺序查，共线性不是“VIF>10 就删变量”

- 在解释系数前按顺序检查：
  1. 线性：残差 vs fitted 无曲线；
  2. 正态：QQ 图 / 标准化残差；
  3. 方差齐性：scale-location 图；
  4. 强影响点：Cook's distance、leverage；
  5. 共线性：VIF 或条件数。
- 共线性处理：
  - VIF > 10 是“需要关注”信号，不是自动删变量的判决；
  - 高共线性时系数符号/大小不稳定，**不要单独解释单个系数**；可报告联合效应、对相关变量聚类、岭/弹性网正则化或模型比较，并做敏感性分析。
- 反例：两个高度相关变量一显著一不显著，作者说“只有前者重要”→ 错；应先说明共线性导致无法可靠分离。
- 来源：Hickey et al. (2018) *Statistical primer: checking model assumptions with regression diagnostics*；Dormann et al. (2013) *Collinearity*。

### 5. 预注册：把“研究者自由度”逐项锁死，偏离透明记录

- 预注册不只是写 H1，要把可后门清单逐项写明：
  - 数据排除/异常值规则；
  - 变量变换（log、z-score、截尾）；
  - 协变量与模型族（固定/随机效应、分层）；
  - 主要/次要终点与多重比较策略；
  - 停早/扩展规则；
  - 效应量与置信区间报告方式。
- 之后改了任一决策，作为 **deviation** 记录：改了什么、为什么改、对结论有何影响；不要把偏离后的分析写成事前计划。
- 好处：审稿人能区分“验证性结论”与“探索性发现”；探索性发现应明确标注。
- 来源：Nosek et al. (2018) *The preregistration revolution*；Forstmeier et al. (2016) *Detecting and avoiding likely false-positive findings*。

### 6. 效应量：选对设计对应的效应量，小样本做偏差校正，并带置信区间与精确 p 值

- 不同设计用不同效应量：t/ANOVA 可用 Cohen's d / η²；多因素/重复测量用 **partial η²**（说明是 partial，不是总 η²）；回归用 **Cohen's f² / R²**；风险/几率用 OR/RR。
- 小样本（尤其 n<20）用 **Hedges' g** 替代 Cohen's d（校正小样本正偏）；说明用了哪个版本。
- 效应量都带 **95% CI**；CI 宽度是精度证据：窄=估计稳，宽=证据不足。报告精确 p 值（p=.031）与 CI，不要只写 p<.05。
- 反例：报“Cohen's d=0.8（大效应）”但无 CI、无 SD/校正说明 → 不可累积，且无法判断精度。
- 来源：Lakens (2013) *Calculating and reporting effect sizes*；Greenland et al. (2016)。

### 7. 多重比较：先分验证性/探索性，再选校正族，并全部报告

- 验证性主终点少：用 family-wise（Bonferroni/Holm）或闭式检验；探索性大量比较：用 FDR（Benjamini-Hochberg）并报 q 值。
- 规则：分析前写下“哪些是验证性、哪些是探索性”；探索性结果即使显著也标为“待验证发现”，不能与验证性结论并列。
- 反例：20 个终点只有 1 个显著，作者只报那 1 个并当主要发现 → 错；应报告全部终点、FDR 校正后的 q 值与校正后 CI。
- 来源：Forstmeier et al. (2016) *Detecting and avoiding likely false-positive findings*。

### 8. 复现验收：从干净环境“从零跑通”，并区分三层复现

- 三层分开报告：
  1. **Computational reproducibility**：同一数据+同一代码+同一环境，重跑出相同图/表/数值；
  2. **Analytic reproducibility**：同一数据、不同的合理分析路径，是否得到相近结论；
  3. **Replicability**：新数据/新实验能否重复结论。
- 验收标准：在**全新未配置环境**（container / 脚本重建环境）从原始数据开始跑一遍，能生成论文中全部图表数字；只有“组里能跑”不等于可复现。
- 可执行：锁 `renv`/`conda`/`Docker` + `requirements.lock`；固定随机种子与 RNG；记录数据/代码版本（commit hash）；用 CI 或脚本自动校验“空环境复跑”。
- 反例：“代码在我们组都能跑” → 环境版本、缺失数据或路径不同，仍不算复现。
- 来源：Munafò et al. (2017) *A manifesto for reproducible science*；Open Science Collaboration (2015) *Estimating the reproducibility of psychological science*。

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
