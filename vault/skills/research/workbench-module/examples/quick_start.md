# Workbench 快速开始

> 假设课题：下周组会要讲“LLM Agent 的评测方法”。

```bash
# 1. 建项目
wb init llm-agent-survey --title "LLM Agent 评测综述"

# 2. 定目标
wb brief llm-agent-survey \
  --goal "找到 5-8 篇关键论文，整理成可讲的组会材料" \
  --non-goal "不做全领域综述" \
  --non-goal "不写完整投稿论文"

# 3. 多源检索
wb search "LLM agent evaluation benchmark" --source arxiv,openalex,crossref --limit 8

# 4. 核验引用
wb verify "10.1145/3711896.3736570"

# 5. 挂证据
wb claim llm-agent-survey "现有评测大多面向单任务，缺少长程任务评测" \
  --source "https://doi.org/10.1145/3711896.3736570" --tag gap

# 6. 专家团独立表态
#  teacher_discussion_start(text="LLM Agent 评测综述", domain_id="research")

# 7. 记录冲突与裁决
wb conflict llm-agent-survey --topic "是否包含长程任务" \
  --claim-a "必须包含长程任务，是当前缺口" \
  --claim-b "先聚焦经典单任务，避免发散"

wb decision llm-agent-survey "以长程任务为主线，经典单任务作为背景" \
  --resolution merge --adjudicator user --conflict conf-001

# 8. 排计划
wb todo llm-agent-survey add "读 5 篇核心论文并建证据表"
wb todo llm-agent-survey add "整理组会 PPT 大纲"

# 9. 阶段门禁
wb gate llm-agent-survey --stage "1 evidence" --item "关键引用可核验" \
  --pass-gate --evidence "5 条引用均通过 Crossref/OpenAlex 核验"

# 10. 记忆回写
wb memory llm-agent-survey add "用户下周组会，需要能讲出‘为什么这个 gap 重要’"
wb memory llm-agent-survey search "组会"

# 11. 随时看状态
wb status llm-agent-survey --verbose
```

> 之后重开会话：直接 `wb status llm-agent-survey` 就能继续，不用从聊天记录里翻。
