# Round 33：高质量搜索 → 内容蒸馏补强（第三批 6 个技能）

> 延续 Round 32：不是包级卫生，而是继续用外部高质量来源填充已有技能。
> 本批覆盖科研子技能与 PPT/美术子技能：paper-reading、paper-writing、group-meeting、research-ppt、mentor-review、dev-art-ppt。

## 交付增量（每技能摘要）

| Skill | 新增要点 | 来源数 |
|---|---|---|
| paper-reading | 三档读法、阅读承诺、合卷重建、四栏结构化笔记、批判六问、提问模板、按论文形态换重点、证据分级 | 12 |
| paper-writing | Rule of One、C-C-C 论证链、图/表骨架先行、配图纪律、Results/Discussion 分工、摘要裁剪、修订流程、公式/单位一致性 | 11 |
| group-meeting | 主结论驱动、时间反向定内容、图表讲解顺序、提问五分类与打断边界、一次一问、对事不对人、纪要记结果、Q&A 应答四类 | 10 |
| research-ppt | 1 分钟/页、分部搭图、分心自检、认知负荷红线、论文图再设计、闪电演讲减法、可访问性与预案、演练录屏复盘 | 10 |
| mentor-review | 五维靶、问题四类、导师团定靶分工、三问框架、候选侧八项漏洞、回应五步协议、四列卡+故意卡壳、先查结果类型 | 12 |
| dev-art-ppt | 观点第一三段标题、单页锚点+眯眼测试、图表任务选择/编码优先级、What-So What-Now What、版式系统、色盲/像素安全、真实彩排、口播稿节奏 | 12 |

## 验证

- vault 包检：50 / 50 仍 100 分
- 本地包检：20 / 20 仍 100 分
- `validate-vault.mjs`：OK（22 skills）
- `validate-tags.mjs`：OK（50 manifests）
- core-iteration smoke：PASS

## 累计（Round 32 + 33）

- 已补强 18 个技能。
- 约 120 条新增可执行规则/反例/示例。
- 新增约 210 条权威来源（OWASP、Google、NIST、PLOS Comp Biol、EMBO、NN/g、Refactoring UI、OpenAI/Anthropic 等）。

## 下一批候选

dev-architecture（可继续增量）、career-path、prompt-writing、document-report、speech-writing、teacher-math-consensus、teacher-consensus、vlpc-consensus、ui-aesthetics-design（可查最新）、submission/experiment-design 等。
