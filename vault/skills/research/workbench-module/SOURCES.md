# 来源表

- `expert-decision-consensus`：九段决策环、证据台账、阶段门禁、子代理执行、记忆回写
  - 源目录：`$HOME/work/skills/expert-decision-consensus/`
  - Vault：`dsh-skill-vault/vault/skills/base/expert-decision-consensus/`
- `tools/workbench_cli.py`：本模块的 CLI 实现（项目初始化、检索、核验、台账、门禁、记忆）
- `research-module`：科研导师团、论文/组会/PPT子流程
  - `dsh-skill-vault/vault/skills/research/research-module/`
- `teacher-module`：教师/专家回合式讨论协议
  - `dsh-skill-vault/vault/skills/teacher/teacher-module/`
- `dev-workflow-consensus`：开发门禁与规格前置
  - `dsh-skill-vault/vault/skills/core-iteration/dev-workflow-consensus/`
- LightRead AI 官网/博客：https://lightingread.cn/
  - “搜读写算一体、云端执行、引用可点回原文、并行智能体、阶段验收”
- 开源 Research Workbench：https://github.com/M-24rjgc/research-workbench
  - 13 阶段流水线、研究台账、三轮互盲审查、写作保真

## Round 35 新增来源

- [PRISMA 2020 statement](https://www.prisma-statement.org/prisma-2020-statement)：系统综述的检索/筛选/报告标准；用于“检索日志、筛选决定、纳入排除流”。
- [Crossref — Retraction Watch retractions now in the Crossref API](https://www.crossref.org/blog/retraction-watch-retractions-now-in-the-crossref-api/)：撤稿状态可经 Crossref 元数据核验；用于“引用核验三层检查”。
- [OpenAlex Help Center](https://help.openalex.org/hc/en-us/articles/24348257451671-Welcome-to-the-OpenAlex-help-center)：开放学术图谱 API/字段；用于多源检索、引用元数据与反向引文。
- [ISPOR — Recommendations on the Use of Structured Expert Elicitation Protocols for Healthcare Decision Making](https://www.ispor.org/heor-resources/good-practices/article/recommendations-on-the-use-of-structured-expert-elicitation-protocols-for-healthcare-decision-making)：结构化专家启发（独立判断、不平均分歧、预先定义共识规则）；用于专家团阶段。
- [RO-Crate Specification](https://www.researchobject.org/ro-crate/specification.html)：轻量研究对象打包规范（元数据、可重跑、provenance）；用于交付物打包。
- [Zenodo — How to upload and download from Zenodo](https://zenodo.org/records/6834336/files/How-to-upload-and-download-from-Zenodo.pdf)：研究数据/软件存档与 DOI；用于文件交付的稳定标识。
- [AiiDAlab — Accelerating discovery through reproducible workflows](https://pubs.rsc.org/zu/content/articlehtml/2026/dd/d5dd00567a)：可复现计算工作流实践；用于“交付物可重跑”。
- [MARTE: Malleable and Automated Reproduction for Testbed-driven Experiments](https://dl.acm.org/doi/10.1145/3736731.3746154)：实验复现与验收语义；用于门禁/复现检查。
- [Cooper — Third-Generation New Product Processes](https://onlinelibrary.wiley.com/doi/10.1111/1540-5885.1110003)：阶段-门流程（Go/Kill/Recycle）；用于阶段门禁设计。
- [Zotero Documentation](https://www.zotero.org/support/quick_start_guide)：文献管理、条目与引用；用于文献笔记原子化与回链。
- [Elicit — Introducing Elicit Research Agent](https://elicit.com/blog/introducing-elicit-research-agent)：AI 研究代理的证据聚合与可追溯；用于检索/证据工作流参照。
- [opendraft — Claim-level citation verification (two-of-three confirming sources)](https://github.com/federicodeponte/opendraft/commit/0b3a627818c9c27b6b258c8e8dffdd040519240a)：主张级引用核验采用“3 源中 2 源确认”；用于多源确认阈值。
