---
name: academic-writing
description: 学术写作子技能——学术文体、摘要/引言/结论结构、LaTeX 排版与检查、引用/BibTeX 规范的可执行检查清单；不替代研究判断与实验数据核验；代码注释、日常文案等非学术写作任务不要加载。
whenToUse: 用户要写/改论文、投稿初稿、会议长文/短文、学位论文章节，或需要 LaTeX/引用规范检查时；需要把学术写作惯例变成可检查动作时。
---

# 学术写作（academic-writing）

> 属于 `writing-module` 子技能。
> 负责：把研究素材包装成**符合学术文体与出版惯例**的文稿，并给出 LaTeX/引用层面的可检查清单。
> 不负责：判断研究价值、生成实验数据、替代导师/领域专家判断。
> 与 `research/research-module/subskills/paper-writing` 的分工：那里负责“按专家视角评审/改写论文”，这里负责“通用学术表达层与排版/引用工程”；两者可以串联：先用本技能搭骨架与格式，再交给 paper-writing 做角色化精修。

## 触发条件

- 用户要写/改：摘要、引言、方法、实验、讨论、结论、投稿信、学位论文章节。
- 用户给出一个 `.tex` / `.bib` 项目，要求检查是否满足投稿格式、引用是否规范。
- 用户说“这段不像学术论文”“不知道摘要/引言怎么写”“LaTeX 引用报错”。
- 用户需要从零搭一个可编译的学术论文工程骨架。

## 核心动作

### 1. 学术文体基调

- **准确 > 漂亮**：每个断言都要有支撑；没有数据就写 `[待补]`，不写“显著提升”“首创”“填补空白”。
- **克制与限定**：用 qualify（可能、在……条件下、在……样本中），避免绝对化；结果与解释分开写。
- **时态约定**：方法/实验多用过去时；一般性事实/定义用现在时；未来工作用将来时或情态。
- **避免 AI 味腔调**：不用“总而言之/值得一提的是/赋能/闭环”等空泛高频词；用短句、名词短语和具体动词。
- **术语一致**：同一概念全文只用一种写法；首次出现给全称与缩写，之后统一用缩写。

> 边界：不同学科/期刊的时态与人称习惯不同；按目标 venue 的 author guide 为准。

### 2. 论文结构（按 IMRaD 的通用映射）

```text
Abstract  一句话背景 → 问题/目标 → 方法 → 关键结果 → 结论/意义
Introduction  背景与现状 → 明确缺口/问题 → 本文方法与思路 → 贡献列表 → 论文结构导览
Methods  可复现：设置、数据、符号、步骤、评估指标；公式与算法带编号
Results  只报告事实：数字、图、表、统计；不在这里展开解读
Discussion  解释结果、与已有工作比较、机制、局限、威胁有效性
Conclusion  总结贡献 + 主要发现 + 局限 + 未来工作；不引入新结果
```

- 非实证/理论/综述类论文可调整结构，但“摘要-引言-主体-结论”仍应清晰可识别。
- **摘要**：单段为主，150–300 词（期刊各有要求）；不要写期刊不说需要的内容（如大量创新评价）；不要在摘要里放未在正文出现的结论。
- **引言**：从问题/缺口进入，不要从“自古以来”的百科式历史开始；贡献用 3–5 条短句，可被正文对应章节验证。
- **结论**：总结而非复述摘要；明确局限与下一步；不要给出正文没有的新结果。

> 边界：学位论文、综述、短文（如 4 页会议短文）篇幅差异很大，先确认 venue 模板与字数限制。

### 3. LaTeX 工程与模板清单

- **先选模板**：`article`（通用）、`IEEEtran`（IEEE）、`acmart`（ACM）、`elsarticle`（Elsevier）、`lncs`（Springer LNCS）等；按会议/期刊官方模板起手，不要自己手写复杂宏包。
- **工程可编译**：`main.tex` + `refs.bib` + `figures/`；长文档用 `\input`/`\include` 分章，避免一个文件几千行。
- **交叉引用**：章节/图/表/公式一律用 `\label{}` + `\ref{}`，禁止写死“第 3 节/图 2”。
- **参考文献**：用 `.bib` + `\bibliography{refs}` 或 `biblatex`；不要在正文手写编号列表。
- **物理量与单位**：用 `siunitx`（或按模板）统一符号、单位、有效数字；变量用数学斜体，单位用正体。
- **图片与表格**：矢量图优先（PDF/eps）；图注/表注自包含；表格用 `booktabs` 风格，不用竖线过多。
- **编译检查**：至少跑 `latexmk -pdf main.tex`（或 `pdflatex` + `bibtex` + 两次 `pdflatex`）；检查日志：
  - `undefined references` / `citation ... undefined` → 必须清零；
  - `overfull hbox` / 溢出 → 至少看是否在正文关键处；
  - 警告数量明显异常时停下，不要带病提交。

> 边界：模板细节（作者块、版权脚注、双栏、页码）由 venue 决定；本技能只给工程级检查，不替代官方模板说明。

### 4. 引用与参考文献规范

- **先定 Style**：按 venue 使用 APA / MLA / Chicago / IEEE / ACM / Nature 等；全文统一，不混用。
- **引用一手来源**：优先引用原始论文/原始数据；二手转述少用；转述必须说明原始出处。
- **关键信息完整**：作者、标题、venue/出版社、年份、卷期页、DOI/arXiv、URL（需要时）、访问日期（网络材料）。
- **防止编造**：每条参考文献必须能在 .bib 中对应真实条目；不能只写“[x]”而 bibliography 缺失。
- **BibTeX 卫生**：key 唯一且有语义（如 `authorYearKeyword`）；作者名/大小写/特殊符号注意；用 `@article`/`@inproceedings`/`@book` 等正确类型。
- **引用位置**：首次引用给出全称/缩写；图表/公式首次引用放在正文，不要只出现在标题。

> 边界：不同期刊对“能否引用 arXiv/预印本、能否用网络来源”有不同规定，投稿前查 author guide。

### 5. 输出契约

调用方传入素材后，本技能输出：

```json
{
  "text": "可提交草稿或修改建议（带 [待补] 占位）",
  "structure": "选用的结构说明与章节分工",
  "latex_checks": ["main.tex 可编译", "引用无 undefined", "图表有 label/ref", "参考文献 style 与 venue 一致"],
  "placeholders": ["需要调用方补的数据/引用/公式"],
  "notes": "学术表达、边界与核验提醒"
}
```

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “我们的方法效果比所有 SOTA 好” | 给出数据集、基线、指标、差异是否显著；无数据补 `[待补]` |
| 摘要里写“本文首创/填补空白” | 只写问题、方法、关键结果与意义；评价留给讨论/审稿 |
| 结论里出现正文没有的新实验 | 新结果放 Results/Discussion；结论只总结与展望 |
| `.bib` 文件存在但正文引用 undefined | 跑 bibtex/检查 key，确保编译日志无 undefined |
| 手写“图3”并在后文改编号 | 用 `\label`+`\ref`，编号交给 LaTeX |
| 大量使用“总而言之/众所周知” | 删掉空泛连接词，直接给具体事实与判断 |
| 把投稿模板当摆设 | 从官方模板开始，保留模板要求的作者块/摘要/关键词结构 |

## 来源

- [Purdue OWL: Abstracts](https://owl.purdue.edu/owl/graduate_writing/graduate_writing_genres/graduate_writing_genres_abstracts_new.html)
- [Purdue OWL: Organization and Structure](https://owl.purdue.edu/owl/graduate_writing/graduate_writing_topics/graduate_writing_organization_structure_new.html)
- [Nature: Formatting guide](https://www.nature.com/nature/for-authors/formatting-guide)
- [APA Style: Abstract](https://apastyle.apa.org/style-grammar-guidelines/paper-format/abstract)
- [The Chicago Manual of Style: Citation Guide](https://www.chicagomanualofstyle.org/tools_citationguide.html)
- [Overleaf: Articles (LaTeX basics)](https://www.overleaf.com/learn/latex/Articles)
- [Overleaf: Bibliography management with BibTeX](https://www.overleaf.com/learn/latex/Bibliography_management_with_bibtex)
- 本地相关：`vault/skills/writing/writing-module/`、`vault/skills/research/research-module/subskills/paper-writing/`
