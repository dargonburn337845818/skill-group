# 教师模块 · 来源与证据

本技能不是凭空发明协议，而是把正式规格 + 既有教师共识固化成一个可执行模块。

## 主要来源

| 来源 | 用途 |
|---|---|
| `FORMAL_SPEC.md` §4 | 专家团、回合式讨论、冲突点表、裁决、命名规范 |
| `FORMAL_SPEC.md` §4.4 | 领域识别与专家缺口：不静默降级 |
| `vault/meta/EXPERT_LIBRARY.json` | 人名专家库 source of truth |
| `vault/meta/domain-profiles.json` | 领域字典 + expert_ids + fallback 文案 |
| `$WORKSPACE/skills/teacher-consensus-skill/output/teacher_consensus_final.json` | 算法竞赛多专家共识材料 |
| `$WORKSPACE/skills/teacher-consensus-skill/content/expert_research.md` | 顶尖选手方法论的公开来源汇编 |
| `vault/skills/teaching/teacher-consensus/` | 既有算法竞赛教师共识 |

## 专家条目证据纪律

- 所有 `status=ready` 专家必须：
  - 是真实公开人物；
  - `persona_type=public-figure-style-reference`；
  - `sourceRefs` 非空且可回溯；
  - `style` 明确写为“风格/方法论推断”，不是本人原话。
- 未满足上述条件的专家保持 `pending_distill`，不进入默认专家团。

## 相关文档

- `SKILL.md` — 对外入口与执行流程。
- `discussion-protocol.md` — 回合式讨论协议与 JSON 契约。
- `expert-selection.md` — 专家选择/添加/缺口处理。
- `examples/round_discussion.md` — 完整示例。


## Round 36 新增来源

| 编号 | 来源 | 用途 |
|---|---|---|
| R36-1 | Hattie, J. & Timperley, H. (2007). The Power of Feedback. Review of Educational Research, 77(1), 81–112. DOI: 10.3102/003465430298487, https://doi.org/10.3102/003465430298487 | 反馈三问题与任务/过程/自我调节分层 |
| R36-2 | Black, P. & Wiliam, D. (1998). Assessment and Classroom Learning. Assessment in Education: Principles, Policy & Practice, 5(1), 7–74. DOI: 10.1080/0969595980050102 | 形成性评价：反馈用于调整教学 |
| R36-3 | Nicol, D.J. & Macfarlane-Dick, D. (2006). Formative assessment and self-regulated learning: a model and seven principles of good feedback practice. Studies in Higher Education, 31(2), 199–218. DOI: 10.1080/03075070600572090 | 七条反馈原则、自我调节 |
| R36-4 | Chin, C. (2007). Teacher questioning in science classrooms: Approaches that stimulate productive thinking. Journal of Research in Science Teaching, 44(6), 815–843. DOI: 10.1002/tea.20171 | 提问类型与促进思考 |
| R36-5 | Rowe, M.B. (1986). Wait Time: Slowing Down May Be A Way of Speeding Up! Journal of Teacher Education, 37(1), 43–50. DOI: 10.1177/002248718603700110 | 等待时间 ≥3 秒 |
| R36-6 | Tofade, T., Elsner, J. & Haines, S.T. (2013). Best Practice Strategies for Effective Use of Questions as a Teaching Tool. American Journal of Pharmaceutical Education, 77(7), 155. DOI: 10.5688/ajpe777155 | 提问分层、开放题、停顿 |
| R36-7 | Hasson, F., Keeney, S. & McKenna, H. (2000). Research guidelines for the Delphi survey technique. Journal of Advanced Nursing, 32(4), 1008–1015. DOI: 10.1046/j.1365-2648.2000.t01-1-01567.x | Delphi 专家选择/匿名/多轮 |
| R36-8 | Okoli, C. & Pawlowski, S.D. (2004). The Delphi method as a research tool: an example, design considerations and applications. Information & Management, 42(1), 15–29. DOI: 10.1016/j.im.2003.11.002 | 专家选取标准、流程设计 |
| R36-9 | Johnson, D.W. & Johnson, R.T. (2009). Energizing Learning: The Instructional Power of Conflict. Educational Researcher, 38(1), 37–51. DOI: 10.3102/0013189X08330540 | 建设性冲突、分歧教学 |
| R36-10 | Du, Y., Li, S., Torralba, A., Tenenbaum, J.B. & Mordatch, I. (2023). Improving Factuality and Reasoning in Language Models through Multiagent Debate. arXiv:2305.14325. DOI: 10.48550/arXiv.2305.14325 | 多智能体独立表态/辩论提升可靠性 |
| R36-11 | Education Endowment Foundation. Teaching and Learning Toolkit: Feedback. https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/feedback | 反馈高影响、焦点任务/策略、可行动 |
| R36-12 | Wilberding, E. (2021). Maieutic Questioning. In Socratic Methods in the Classroom. Routledge. DOI: 10.4324/9781003238089-4 | 苏格拉底/产婆式追问 |
