# 蒸馏共识 · 网络来源清单

> 本清单记录本次“网络蒸馏技巧”研究曾参考的公开资料。
> 说明：这些链接用于交叉验证与继续深挖；本共识不是对任一来源的逐句搬运，而是抽取共性后重新组织。

## 内容 → Agent Skill 蒸馏

| 来源 | 主题 | 对本共识的贡献 |
|---|---|---|
| [cangjie-skill（kangarooking）](https://github.com/kangarooking/cangjie-skill) | 把书、长视频、播客等高价值内容蒸馏成可执行的 Agent Skills | “可执行 Skill”而非复述；内容片段切分 |
| [cangjie-skill SKILL.md](https://github.com/kangarooking/cangjie-skill/blob/main/SKILL.md) | 具体 skill 指令 | 触发/动作/边界/用户话术的结构化样例 |
| [仓颉 · 认知植入式思维蒸馏引擎（Yeadon8888）](https://github.com/Yeadon8888/cangjie-skill) | 让 AI“想得像他”，不只是“说得像他” | 强调思维方式/决策过程蒸馏，而非复述观点 |
| [WorkBuddyGuide 第22章：打造 Skill，将书和视频蒸馏为可执行 Skill](https://github.com/AlephAITech/WorkBuddyGuide/blob/main/docs/bluebook/%E7%AC%AC%E4%B8%89%E7%AF%87%20%E8%BF%9B%E9%98%B6%E7%AF%87%EF%BC%9A%E6%8A%8A%E6%A1%88%E4%BE%8B%E5%8F%98%E6%88%90%E8%87%AA%E5%B7%B1%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%B3%BB%E7%BB%9F/%E7%AC%AC%2022%20%E7%AB%A0%20%E6%89%93%E9%80%A0skill%EF%BC%9A%E5%B0%86%E4%B9%A6%E5%92%8C%E8%A7%86%E9%A2%91%E8%92%B8%E9%A6%8F%E4%B8%BA%E5%8F%AF%E6%89%A7%E8%A1%8C%20Skill/index.md) | 从书/视频构造可执行 Skill 的章节 | 目标先定、多轮加工、成品可执行 |
| [WorkBuddy 把书和视频蒸馏为 Skill（文章镜像）](http://www.jxxy.net/ai/paths/workbuddy-basics/workbuddy-34-build-skill/) | 入门到精通：打造 Skill | 用户侧简单语言表达方向/方式 |
| [knowledge-distillation-survey（windags-skills）](https://github.com/curiositech/windags-skills/tree/main/skills/knowledge-distillation-survey) | 知识类型与智能分解的调研 | 按知识类型选择蒸馏形态 |
| [ASPS：三层 Skill 构建框架](https://github.com/Beunec/asps) | 把技能拆成可部署工件 | 成品不能只是“一段话”，要有可部署的形态 |

## 知识蒸馏研究（跨领域启发）

| 来源 | 主题 | 对本共识的贡献 |
|---|---|---|
| [A Survey on Knowledge Distillation of Large Language Models](https://arxiv.org/html/2402.13116) | LLM 知识蒸馏综述 | “教师/学生”分层、响应/特征蒸馏等类比 |
| [A Comprehensive Survey on Knowledge Distillation](https://github.com/IPL-sharif/KD_Survey) | 通用知识蒸馏综述 | 蒸馏目标不是复制，而是迁移可复用的判断 |
| [A Comprehensive Survey on Data Distillation](https://xplorestaging.ieee.org/document/11250975) | 数据蒸馏综述 | 先选高价值样本/片段，再压缩 |

## 本地实践（交叉验证）

- `$HOME/work/teacher-consensus-skill/SKILL.md`：算法竞赛教师共识 + 信息论 + 提问协议。
- `$HOME/work/teacher-consensus-skill/METHOD.md`：七步蒸馏法（语料 → primitive → 矩阵 → 回测）。
- `$HOME/work/dsh-optimization-consensus/CONSENSUS.md`：官方文档/源码 → 可执行运维共识。
