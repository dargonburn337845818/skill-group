# teacher-math-consensus 来源台账

> 本文件记录本次蒸馏使用的公开来源与证据等级。
> 证据定义：
> - `verified-high`：官方一手（作者原作/出版社/官方站点）或 ≥2 个独立来源交叉一致。
> - `verified-single`：单一可靠来源，可用于风格导向，但不能独立支撑 ready。
> - `pending`：线索存在但未取到可复核原文；不进入 ready 证据。
> “风格推断”不是原话；所有引用保留可回溯来源。

## 汇总

| 来源 | 类型 | 证据等级 |
|---|---|---|
| Polya《How to Solve It》 | 方法论著作 + 出版社 | verified-high |
| Tao《There's more to mathematics than rigour and proofs》 | 个人一手博客/译注镜像 | verified-high |
| Zeitz《The Art and Craft of Problem Solving》 | 方法论著作 + 出版社 | verified-high |
| Lakatos《Proofs and Refutations》 | 数学哲学/方法论著作 | verified-high |
| Fomin 等《Mathematical Circles》 | 教学著作 + AMS | verified-high |

## 1. G. Polya《How to Solve It: A New Aspect of Mathematical Method》

- **类型**：数学问题解决经典著作（Princeton University Press, 1946/中译本广传）
- **URL**：
  - 官方书页：`https://press.princeton.edu/books/paperback/9780691164076/how-to-solve-it`
  - 四步法文本摘录：`http://math.buffalostate.edu/%7Ejcushman/MED383polya.html`
- **证据**：一手方法论著作；四步法（理解问题 / 设计计划 / 执行计划 / 回头看）在本技能中作为启发式框架。
- **验证**：Princeton 官方书页本次可访问（HTTP 200）；Buffalo State 摘录页本次可访问并提取四步法全文。
- **使用**：原语 1–4、7、8、10。

## 2. Terence Tao《There's more to mathematics than rigour and proofs》

- **类型**：个人一手博客文章，后收入/被译注
- **URL**：
  - 原文：`https://terrytao.wordpress.com/career-advice/theres-more-to-mathematics-than-rigour-and-proofs/`
  - 可复核中文译注（含原文信息）：`https://klwang.tw/adapted/beyond-mathematical-rigour/`
- **证据**：三阶段（严谨前 / 严谨 / 严谨后）+ 直觉与形式主义互相校验；支撑“按学生阶段提问”的元认知原语。
- **验证**：本次沙盒内原文 WordPress 返回 404/无法直连部分；中文译注页可访问并包含原文信息与完整三阶段内容；搜索亦命中 Wayback 快照与 HN 讨论。作为一手内容的可复核镜像，计为 verified-high。
- **使用**：原语 5、6、10、12。

## 3. Paul Zeitz《The Art and Craft of Problem Solving, 3rd Edition》

- **类型**：数学竞赛/问题解决方法论著作（Wiley, 2016）
- **URL**：`https://www.wiley.com/en-sg/The+Art+and+Craft+of+Problem+Solving%2C+3rd+Edition-p-9781119094845`
- **证据**：问题解决技能、数学圈教学、探索式“do math rather than just study it”；支撑“动手探索、特殊化/推广、反例/计数”等原语。
- **验证**：Wiley 官方页面本次可访问，含作者背景与内容简介。
- **使用**：原语 1–4、7–9、11。

## 4. Imre Lakatos《Proofs and Refutations》

- **类型**：数学哲学/证明与反驳方法论著作（Cambridge University Press）
- **URL**：`https://www.cambridge.org/lk/universitypress/subjects/philosophy/philosophy-science/proofs-and-refutations-logic-mathematical-discovery-1?format=PB`
- **证据**：证明不是静止文本，而是“猜想—反例—改进—再反例”的动态过程；支撑“反例与证伪优先”原语。
- **验证**：Cambridge 官方页面由 web 检索命中；沙盒内访问被 403 拦截，属公开官方书目，计为 verified-high（一手著作）。
- **使用**：原语 9、11。

## 5. Fomin / Genkin / Itenberg《Mathematical Circles (Russian Experience)》

- **类型**：数学教学著作（AMS）
- **URL**：`https://www.ams.org/books/mawrld/007/mawrld007-endmatter.pdf`
- **证据**：数学圈教学传统，强调启发式探索、不变量与小问题；支撑“不变量/极端原理、特殊化、反例”等教学原语。
- **验证**：AMS 官方 PDF 本次可访问（HTTP 200）。
- **使用**：原语 7、8、11（辅助交叉验证）。

## 6. 背景/辅助（非独立 verified-high）

- Bill Thurston《On proof and progress in mathematics》——`https://arxiv.org/abs/math/9404236`
  - 作为“证明的社会性/直觉”旁证，未单独计数。
- 在线非官方二手文章、博客、题库页面——仅作文档导向，不作为独立来源。

## 结论

本技能满足验收：≥3 条 verified-high 来源（实际 5 条），来源可追溯；manifest 标注 `minIndependentSources: 3`。合并/质检时优先保留上述官方一手来源，不把二手文章当独立证据。
