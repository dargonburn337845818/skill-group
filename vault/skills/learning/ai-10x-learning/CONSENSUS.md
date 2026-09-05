# AI 十倍速学习 · 完整依据

> 本文件是 `SKILL.md` 的完整版：每条关键主张给出证据分级、来源、失效边界与“调度/专家团化”用法。
> 核心来源：Dan Koe《How To Learn Anything 10x Faster Than Anyone With AI》（32 分钟播客），中文改写视频为 B 站 BV1W4REYzEdx。

## 证据分级约定

- `primary`：播客原文/逐字稿（pod.wave.co 转录）或一手网页（thedankoe.com 原文）。
- `secondary`：转载、摘要、编译（modb / CoworkAI / 中文 B 站搬运）。
- `style`：按公开人物风格推断，非本人原话。

## 主张与证据

| # | 主张（触发 → 动作 → 预期） | 证据 | 级别 | 边界 |
|---|---|---|---|---|
| 1 | 当用户想“快速学会 X”时，先问“你要用 X 做出什么项目”，而不是先排课表 | 播客 12:11–17:00：“Start the project… A project creates a frame for your learning by filtering out unimportant noise.” | primary | 如果是纯知识问答，不构成学习项目；不要硬套 |
| 2 | 学习 = 目标 → 感知现状 → 误差 → 行动的反馈闭环；没有目标就没有过滤，也就没有记忆 | 播客 03:46–08:10 控制论模型：“Goal = Reference signal… Action = Behavior to close the gap.” | primary | 目标必须是“想改变什么/做出什么”，不能是模糊的“想学” |
| 3 | 记忆不是目标；只有与重要目标相关的知识会被记住 | 播客 00:00–03:45：“If you need to remember it, it's not important. If it's important, you will remember it.” | primary | 考试/法规等确需强记的场景仍需刻意练习；这不否定所有记忆 |
| 4 | 学新工具（After Effects / 吉他 / 代码）应以“成品/歌曲/项目”为起点，按需查针对性教程 | 播客 15:00–17:00 吉他例子：“You learn the first chord of the song… stack enough techniques to get the result you want.” | primary | 不是“完全不看教程”，而是“教程为项目服务”；教程大多内容可过滤 |
| 5 | 第二大脑应叫“第二潜意识”：核心是轻松存入 + 在创作时自动浮现，不是整理收藏 | 播客 17:01–32:45：“Rather than this being a second brain, I like to think of it as a second subconscious.” | primary | 没有项目/创作的笔记系统只是囤积；不应把“存了多少条”当成果 |
| 6 | Claude + Obsidian 最小可用法：建“保存想法”与“处理收件箱”两个 skill，自动打标签/回链/分类 | 播客 23:11–32:45 逐步说明 | primary | 工具本身不解决问题；必须按照“能为创作浮现”使用 |
| 7 | 在 AI 能生成一切的时代，策展 > 消费：只收藏会改变世界观/触发反应的最高杠杆想法 | 播客 32:46–37:37：“Curation matters more than ever… People follow you for your point of view.” | primary | “高杠杆”是主观判断，不应退化为“多存” |
| 8 | AI 用于去摩擦（扫描、结构、研究、事实摘要），不用于替你表达观点与信念 | 播客 37:38–44:30：“Use AI to remove friction, not to write for you. Articulate your own beliefs.” | primary | AI 仍可能幻觉；最终发布判断权在人，不因“AI 说可以”就发布 |
| 9 | 创作主题 = 已被验证的表现（performance）× 自己真正兴奋（excitement） | 播客 37:38–44:30 Step 1 | primary | 该规则适用于内容创作，不直接适用于所有学习目标 |
| 10 | 写作/创作流程：蓝图 → 大纲（Problem→Insight→Solution）→ 草稿 → 用 AI 取结构与研究方向 | 播客 37:38–44:30 Step 2–3 | primary | 这是创意工作流，不是通用学习流程；学习场景可借用“输出优先” |
| 11 | 6 个提示词（阶梯/20h/考官/一页纸/资源策展/费曼）可把 AI 变成私人教师/考官/陪练 | modb 文章 + CoworkAI 元描述 + 相关 B 站搬运 | secondary | 单源编译，未在播客逐字稿中一一对应；作为“可复制工具包”而非核心结论 |

## 调度器用法（如何接进 value-meta-scheduler / dsh-skill-router）

- **触发词**：学习、自学、AI 学习、十倍速、第二大脑、笔记、费曼、主动回忆、学习计划、怎么学。
- **路由建议**：`domain:learning`，推荐 skill `ai-10x-learning`；若用户只是“帮我搜论文/查资料”，不应被路由到此领域。
- **在核心迭代中**：把本 skill 作为“学习方法论”语料源；蒸馏时只保留有 primary 证据的 Node，二手 6 提示词降权为 `footnote`。
- **轮次控制**：若只做一次学习规划，不需要多轮递归；若持续迭代一个“AI 学习教练 Skill”，可将本包作为 initial_draft 进入 value-meta-scheduler。

## 专家团用法（如何接进 expert-team / teacher-module）

- **领域**：`learning`（AI/自我提升学习法）。
- **默认专家**：
  - `dan-koe`（Dan Koe，作者/创作者；风格参考：项目驱动、输出优先、AI 去摩擦）
  - `richard-feynman`（已有 ready；风格参考：费曼循环、简单讲清、亲自重述）
  - `andrej-karpathy`（已有 ready；风格参考：AI 工程、把 AI 当工具与本原理解，适合审查“AI 是否越界”）
- **典型冲突点**：
  - “先学基础再做事” vs “先做事再补基础”：保留为分支；一般裁决为“项目设定学习优先级，基础按需补”。
  - “AI 可以直接给结论” vs “AI 只能辅助自测”：按公开风格，Feynman/Karpathy 更倾向主动理解而非被动接收。
- **输出纪律**：所有结论带 `expert_id` + `expert_name` + `sourceRefs`；风格推断须标注“非本人原话”。

## 反模式

- 把本共识当“答案引擎”：用户问具体知识点时，不应强制走学习系统。
- 把 6 提示词当视频原文：它们是二手编译，不冒充一手。
- 把“收藏/保存”当已完成学习。
- 把“AI 写得快”当“我学会了”。
