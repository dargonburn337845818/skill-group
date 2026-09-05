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

- **准确 > 漂亮**：每个断言都要有支撑；没有数据就写 `[后续]`，不写“显著提升”“首创”“填补空白”。
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
  "text": "可提交草稿或修改建议（带 [后续] 占位）",
  "structure": "选用的结构说明与章节分工",
  "latex_checks": ["main.tex 可编译", "引用无 undefined", "图表有 label/ref", "参考文献 style 与 venue 一致"],
  "placeholders": ["需要调用方补的数据/引用/公式"],
  "notes": "学术表达、边界与核验提醒"
}
```

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “我们的方法效果比所有 SOTA 好” | 给出数据集、基线、指标、差异是否显著；无数据补 `[后续]` |
| 摘要里写“本文首创/填补空白” | 只写问题、方法、关键结果与意义；评价留给讨论/审稿 |
| 结论里出现正文没有的新实验 | 新结果放 Results/Discussion；结论只总结与展望 |
| `.bib` 文件存在但正文引用 undefined | 跑 bibtex/检查 key，确保编译日志无 undefined |
| 手写“图3”并在后文改编号 | 用 `\label`+`\ref`，编号交给 LaTeX |
| 大量使用“总而言之/众所周知” | 删掉空泛连接词，直接给具体事实与判断 |
| 把投稿模板当摆设 | 从官方模板开始，保留模板要求的作者块/摘要/关键词结构 |

## 2026 深度补强（Round 32）

> 本轮不替代 1–5 节；补强重点是**可执行检查 + 反例**，并新增独立来源台账（见 `SOURCES.md` 的 Round 32 新增来源）。

### R32-1 摘要自包含、后写、无图/表/引用

- **触发**：写或审摘要时；摘要里出现“如图 3”“见表 2”“见第 4 节”“[12]”等依赖正文的指称。
- **动作**：
  - 摘要必须能在脱离正文的情况下被读懂：不放图、表、公式编号、章节编号、对其他文献的引用；不得已时用文字描述“我们提出的方法”，而不是“图 3”。
  - 摘要放到正文/结论定稿后再写；从 Introduction 与 Conclusion 中找 key terms 与关键数字，用自己的话改写，不要从正文 cut-paste。
  - 信息型摘要按四要素写：目的/问题 → 设计/方法（含数据、样本、关键参数）→ 主要发现（带数字或方向）→ 解释与结论；英文期刊多数 150–300 词，先查 venue。
  - 若 venue 要求关键词，摘要后列 3–6 个；关键词用可检索的概念/缩写，不全抄标题。
- **示例**：
  - 反例：`Our method outperforms baselines as shown in Fig. 3 and Table 2; the improvement is [5].`
  - 正例：`We compare ... on 21 benchmark datasets; the proposed ... reduces error by 12.4% on average.`
- **边界**：医学/部分社科期刊要求结构化摘要（Background/Methods/Results/Conclusions），按官方模板写；人文/理论型摘要可以以 thesis/background/conclusion 为主，不硬塞结果数字。
- 来源：USC Libraries – The Abstract；UNC Writing Center – Abstracts

### R32-2 引言用 CARS 三步：铺陈领域 → 指出缝隙 → 占据缝隙

- **触发**：引言写成“百科背景 + 文献堆砌”，或用户说“不知道引言从哪里开始”。
- **动作**：
  1. **Move 1·铺陈领域**：说清主题为什么重要、当前理解是什么（1–2 段，可含已有工作）。
  2. **Move 2·指出缝隙**：明确“已有研究缺什么/哪里矛盾/什么问题未答”，必要时落成一句研究问题。
  3. **Move 3·占据缝隙**：一句话说本文目标与方法、关键结果/贡献，最后给论文结构导览。
  4. 正文写完后回来改引言；此时结果已知，才能把“本文做了什么”写准。
- **示例**：
  - Move 1：`X is important because ... Existing work has focused on A and B.`
  - Move 2：`However, little is known about C in D; this gap matters because ...`
  - Move 3：`This paper ... We conduct ... Results show ... The rest is organized as follows.`
- **边界**：理论/思辨论文可用“研究问题/争论”代替“文献 gap”；综述类论文的 Move 3 变成“本综述如何组织”，而不是“我们的贡献”。
- 来源：USC Libraries – The Introduction（C.A.R.S. Model）；UNC Writing Center – Introductions

### R32-3 结论做“综合”，不做“摘要复述”

- **触发**：结论像摘要逐句复述；开头用 “In conclusion / In summary / In closing”；或在结论里第一次亮出论点。
- **动作**：
  - 第 1 段：用新的措辞回答研究问题/重申主论断。
  - 第 2 段：回答 “So What?”——把发现放到更大语境：对理论、实践、政策的意义，或对本领域文献的推进。
  - 第 3 段：给出具体局限与下一步；若 Discussion 已详述局限，用一句话指回即可，不必重复整段。
  - 避免：以 “In conclusion/In summary/In closing” 开头；在结论第一次提出 thesis；引入新证据、新子话题、新引文；只重述 thesis 而无实质推进。
- **示例**：
  - 反例：`In conclusion, this paper ... （以下逐句复述摘要）`
  - 正例：`These results suggest ... ; for practice, this implies ... ; a remaining limitation is ... ; future work should ...`
- **边界**：学位论文结论章可以更长（贡献 + 限制 + 未来工作），但“不引入新证据”仍适用；期刊若把 Discussion 与 Conclusion 合并，按模板合并，不硬分两节。
- 来源：USC Libraries – The Conclusion；UNC Writing Center – Conclusions

### R32-4 引用命令按语义分开：\citet/\citep 与 \textcite/\parencite

- **触发**：正文里所有引用都用裸 `\cite{}`；或出现 “Smith et al. (2020) [5]” 这种同时带作者与编号的重复标记。
- **动作**：
  - 作者作句子主语/叙述式引用：natbib 用 `\citet{key}`，biblatex 用 `\textcite{key}`（输出如 “Smith et al. (2020)”）。
  - 括号式引用：natbib 用 `\citep{key}`，biblatex 用 `\parencite{key}`（输出如 “(Smith et al., 2020)” 或 “[12]”）。
  - 一篇文档选一条命令族并统一；不要在相邻句子里混用 `\cite`、`\citep`、`\citet` 而不说明。
  - 作者-年份模式必须保证 `.bib` 的 `author`/`year` 字段完整，否则 `\citet` 可能输出空作者。
- **示例**：
  - 反例：`Smith et al. (2020) [5] proposed ...`
  - 正例：`\citet{smith2020} proposed ...`；`... outperforms prior work \citep{smith2020}.`
- **边界**：数字引用模板（IEEE/ACM numeric）通常正文用 `\cite`/`\parencite` 即可；若模板规定作者名单独手写，以模板为准。
- 来源：Overleaf – Natbib citation styles；Overleaf – Bibliography management with biblatex

### R32-5 BibTeX 卫生：保护大小写、语义化 key、软件/数据单独建条目

- **触发**：`.bib` 里标题大小写被样式吞掉、key 是 `ref1`，或把软件/数据集伪装成 `@article`。
- **动作**：
  - 标题中需要保留大写的专有名词/缩写用双层花括号包住：`title = {A Study of {DNA} Sequencing}`；不要指望 bib 样式替你保留。
  - key 唯一且可读：`authorYearKeyword`（如 `zhang2021graph`），不要 `ref1`/`key1`。
  - 软件/数据集单独建条目：用 `@software`（biblatex 支持）或 `@misc`/`@online`，字段至少含 `author`、`title`、`version`、`date/year`、`doi`/`url`；引用时带版本。
  - 预印本/网络资源用 `@misc`/`@online` + `eprint`/`archivePrefix`/`url`；若同一工作已正式发表，引正式版。
  - 每条 `.bib` 检查字段完整性：作者、年份、标题、venue、卷期页/DOI 至少有一项可定位。
- **示例**：
  - 反例：`@article{deep, title = {Deep Learning}, author = {...}}` 用作软件条目，无版本无 DOI。
  - 正例：`@software{scipy2021, author = {Virtanen, Pauli and others}, title = {SciPy 1.8}, version = {1.8.0}, year = {2022}, doi = {...}}`
- **边界**：venue 对预印本、软件引用政策不同（有些只允许引正式论文）；投稿前查 author guide。
- 来源：Overleaf – Bibliography management with biblatex；Overleaf – Biblatex bibliography styles；FORCE11 – Software Citation Principles

### R32-6 大文档分层：\input 与 \include(+includeonly)

- **触发**：`main.tex` 超过 2000 行、编译慢，或改一章要全量重编。
- **动作**：
  - `\input{file}` 适合小节/短内容：不强制换页、不产生独立 `.aux`、可以嵌套。
  - `\include{file}` 适合章节级：强制换页、产生独立 `.aux`，可与 `\includeonly{chap1,chap2}` 配合加速迭代；交叉引用与页码仍从旧 `.aux` 保留。
  - 图片路径集中在根文件 `\graphicspath{{figures/}}`；子文件不要写依赖“当前目录”的脆弱相对路径（除非用 subfiles/standalone 的 `\subfix`）。
  - `.bib`/`.bcf` 路径相对根文件；不要在子文件重复 `\bibliography` 或 `\addbibresource`。
  - 长文档最终提交前删掉 `\includeonly`，做一次全量 clean build。
- **示例**：`\includeonly{chapters/intro,chapters/method}` 放在 `\begin{document}` 之前。
- **边界**：`\include` 不能嵌套且强制换页；`\input` 不产生独立辅助文件；学位论文按“一章一层”即可，不要拆得过细。
- 来源：Overleaf – Management in a large project

### R32-7 按引用后端选编译链，日志核验三件套

- **触发**：切模板后引用不出现；`Citation ... undefined` 或 `Package biblatex Warning`；不确定该跑 `bibtex` 还是 `biber`。
- **动作**：
  - **BibTeX/natbib 链**：`pdflatex main` → `bibtex main` → `pdflatex main` ×2；看 `main.blg` 中的 `Warning--I didn't find a database entry` / 无 `\citation` 命令提示。
  - **biblatex 链**：`pdflatex main` → `biber main` → `pdflatex main` ×2；**不要**对 biblatex 文档跑 `bibtex`；检查 `main.blg`/`main.bcf` 与 `Package biblatex` 警告。
  - 或 `latexmk -pdf -interaction=nonstopmode main.tex`；`latexmk -c` 可清中间文件，但不要删 `.tex/.bib`；提交前做一次全量 clean build。
  - 日志清零项：`undefined` references / `Citation undefined` / 引用相关的 `Package biblatex Warning` / `Warning--`；`overfull hbox` 至少检查正文关键位置。
- **示例**：
  - 反例：对 `\addbibresource{refs.bib}` 的 biblatex 文档跑 `bibtex main`，引用仍 undefined。
  - 正例：`latexmk -pdf -interaction=nonstopmode main.tex`，再看日志确认引用解析。
- **边界**：`latexmk` 是否自动调 `biber` 取决于版本/`latexmkrc`；不确定时直接按显式 `bibtex`/`biber` 命令跑一遍。Overleaf 自动处理编译流程，但日志仍要人工看。
- 来源：CTAN – latexmk；Overleaf – Errors；Overleaf – Bibliography management with biblatex

## 来源

- [Purdue OWL: Abstracts](https://owl.purdue.edu/owl/graduate_writing/graduate_writing_genres/graduate_writing_genres_abstracts_new.html)
- [Purdue OWL: Organization and Structure](https://owl.purdue.edu/owl/graduate_writing/graduate_writing_topics/graduate_writing_organization_structure_new.html)
- [Nature: Formatting guide](https://www.nature.com/nature/for-authors/formatting-guide)
- [APA Style: Abstract](https://apastyle.apa.org/style-grammar-guidelines/paper-format/abstract)
- [The Chicago Manual of Style: Citation Guide](https://www.chicagomanualofstyle.org/tools_citationguide.html)
- [Overleaf: Articles (LaTeX basics)](https://www.overleaf.com/learn/latex/Articles)
- [Overleaf: Bibliography management with BibTeX](https://www.overleaf.com/learn/latex/Bibliography_management_with_bibtex)
- 本地相关：`vault/skills/writing/writing-module/`、`vault/skills/research/research-module/subskills/paper-writing/`
