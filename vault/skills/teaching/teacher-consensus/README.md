# teacher-consensus-skill（草稿）

> 这是“算法竞赛教师共识”技能的草稿目录。
> 目标：把顶尖选手思路 + 信息论原理，蒸馏成可回测、可编译成静态软件的概率知识。

**本目录当前不修改 `knowledge-ladder-repo`。** 等蒸馏 pipeline 和概率矩阵稳定后再决定合并。

## 当前进度

- 已限速抓取 **Codeforces 423 篇博客**、14 位专家提交记录、problemset 元数据。
- 已从 423 篇中选出 **64 篇高价值博客**。
- 已完成三轮 AI 蒸馏：
  - 第一轮：抽出 **125 条候选 primitive**
  - 第二轮：按方向交叉验证合并为 **81 条**
  - 第三轮：跨方向 meta-consensus 合并为 **22 条教师共识主题**
- 按评审意见补充 3 个盲区：
  - Meet-in-the-middle / 折半搜索
  - 交互式/自适应问题的决策树与查询下界
  - 存在性判定与构造输出分离
- “人类接管”已从解题方向移入**元纪律**，不再归属四大方向。
- 可载入提示词最终为 **24 条主题 + 元纪律**。
- 信息论已写入 `SKILL.md`、`notes/info-theory-map.md`。

## 目录结构

```text
teacher-consensus-skill/
├── CP_KNOWLEDGE_CRYSTAL.md     # ★ 可载入提示词：任意智能体全文粘贴即可用
├── SKILL.md                    # 主技能：教师共识 + grill-me 提问协议 + 信息论
├── METHOD.md                   # 七步蒸馏法：从语料到概率矩阵
├── README.md                   # 本文件
├── schema/
│   └── primitive.schema.json   # 思维原语 JSON Schema
├── content/
│   ├── core_consensus.md       # 第一版核心共识内容（草稿）
│   └── expert_research.md      # 外部研究：21 条顶尖选手模式 + 信息论映射
├── examples/
│   └── sample_consensus.json   # 示例 primitive
├── prompts/
│   ├── extract_episodes.md     # 题解/访谈 → 推理片段
│   ├── cross_validate.md       # 多来源交叉验证与共识分级
│   ├── sample_calibrate.md     # OJ 题目抽样 → 校准条件概率
│   └── understand_expert_material.md  # AI 辅助读懂高手思路
├── crawlers/
│   └── crawl_cf_corpus.py      # 限速 Codeforces 语料爬虫
├── tools/
│   ├── analyze_corpus.py       # 语料关键词/跨专家矩阵
│   ├── select_high_value_blogs.py
│   ├── prepare_distill_chunks.py
│   ├── merge_primitives.py
│   └── build_final_consensus.py
├── notes/
│   └── info-theory-map.md      # 信息论概念 → 教学/软件落点
├── data/cf/                    # 原始语料 + 分析结果
└── output/                     # 蒸馏产出
    ├── teacher_consensus_final.json        # 基础 22 条教师共识主题（机器可读）
    ├── teacher_consensus_final_revised.json # 评审修订版：24 条 + 元纪律
    ├── teacher_consensus_final.md          # 同上的人类可读版
    ├── teacher_consensus.json              # 81 条方向合并版
    ├── consensus_core.md                   # 跨专家核心里程碑
    ├── knowledge_crystal_supplements.json  # 评审盲区人工补充
    └── pilot_summary.md                    # 第一批 pilot 摘要
```

## 专家名单（交叉验证来源）

tourist、jiangly、Benq、Um_nik、Errichto、Petr、maroonrk、rng_58、ecnerwala、scott_wu、tfg、Radewoosh、ksun48、neal

## 怎么用

1. **给任意智能体直接用**：把 `CP_KNOWLEDGE_CRYSTAL.md` 全文粘贴为系统提示/上下文。
2. 先读 `SKILL.md`：理解教师共识和提问协议。
3. 读 `METHOD.md`：理解从语料到概率矩阵的完整链路。
4. 最终结果在 `output/teacher_consensus_final.json`。
5. 下一步是将这些主题映射到 `knowledge-ladder-repo` 的 20 特征 / 120 算法 / 四方向，再生成矩阵补丁。

## 当前状态

- [x] 主技能文本
- [x] 蒸馏方法
- [x] primitive schema
- [x] 示例条目
- [x] 第一版核心共识内容
- [x] 外部专家研究
- [x] 限速语料爬虫（Codeforces 423 篇博客）
- [x] 全量精选 + AI 提取（125 候选）
- [x] 按方向交叉验证（81 条）
- [x] 最终 meta-consensus（22 条）
- [x] 信息论映射
- [ ] 抽样 OJ 校准
- [ ] 回测脚本
- [ ] 生成 knowledge-ladder-repo 矩阵补丁
- [ ] 合并进 knowledge-ladder-repo

## 下一步建议

1. 把最终 22 条主题映射到现有 20 个 feature 和 120 个算法。
2. 为每条主题补充 `P(feature | algorithm)` 的专家先验。
3. 用 `prompts/sample_calibrate.md` 对 OJ 题抽样校准。
4. 写回测脚本，跑 top-k 命中率与平均提问数。
5. 稳定后再决定合并进 `knowledge-ladder-repo`。
