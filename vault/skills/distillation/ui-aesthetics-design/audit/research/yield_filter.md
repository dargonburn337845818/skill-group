# 收益过滤与交叉验证（Yield Filter）

> 输入：`./raw_corpus_design_specs.md`（13 条）、`./classic_principles_corpus.md`（10 条）、`./local_material_inventory.md`（4 个本地素材，不计入候选规则数）。
> 本阶段只做过滤，不写最终 SKILL/CONSENSUS。
> 过滤维度：反常识 / 可操作 / 可验证 / 多源。
> 分级：`verified-high`（≥2 个独立来源且可复核） / `verified-single`（单一可靠来源，挂“单源待证”） / `discarded`（无来源、纯推断、或仅单一风格且不可升级） / `pending`（来源存在但未取到可复核原文）。

## 一、raw_count

| 输入 | 条数 |
|---|---|
| 设计规范 raw entries | 13 |
| 经典原则推理单元 | 10 |
| 本地素材条目 | 4（单独统计，不进入候选规则） |
| **原始候选碎片合计** | **23** |

## 二、候选规则过滤表

| id | 候选主张 | 主要来源 | 判定 | 理由 |
|---|---|---|---|---|
| ui-contrast-text | 正文文本对比度 ≥4.5:1；大文本可降至 ≥3:1 | WCAG 1.4.3 / Primer / Apple | `verified-high` | 3 个独立权威来源，且三处给出同一阈值 |
| ui-contrast-nontext | 控件/图形等非文本视觉信息 ≥3:1 | WCAG 1.4.11 / Primer | `verified-high` | 2 个独立来源一致 |
| ui-focus-visible | 键盘焦点指示器必须可见且不超时 | WCAG 2.4.7 / NN/g Visual Treatments | `verified-high` | WCAG 官方标准 + NN/g“Identify Focus State”，2 个独立来源 |
| ui-focus-appearance | 焦点环面积≥2px 粗轮廓、状态间 ≥3:1；内嵌需更粗 | WCAG 2.4.13 | `verified-single` | 仅 WCAG 一手标准给出该精确指标；无第二个独立来源提供同数值，挂“单源待证” |
| ui-type-body-scale | 正文常用 16px、行高约 1.5；小字 14px/20px | Tailwind / GOV.UK / Material / Primer | `verified-high` | 4 个独立设计系统给出相近落地值 |
| ui-line-length | 正文行宽约 45–75 字符、行高≥1.3 | Practical Typography / Tailwind/GOV.UK | `verified-single` | 45–75 字符主要来自 Butterick（`pending` 未取原文）；仅 Tailwind/GOV.UK 可证“通常行高”，不能证“必须 45–75” |
| ui-font-personality | 字体选择表达气质；正文避免装饰字体 | Practical Typography | `verified-single` | 单一排印流派观点，已标 style；保留为“风格分支”而非共识 |
| ui-spacing-grid | 用 4/8dp 网格与统一间距尺度组织留白 | Material / Primer / Refactoring UI | `verified-high` | 3 个独立来源（官方设计系统 + 设计书）方向一致 |
| ui-hierarchy-scale | 用大小/字重/颜色/留白/位置建立视觉层级，优先元素更突出 | NN/g / Refactoring UI | `verified-high` | 2 个独立来源一致 |
| ui-proximity-group | 相关元素靠近、不相关远离；邻近性形成分组 | NN/g / Refactoring UI | `verified-high` | 2 个独立来源一致 |
| ui-whitespace-emphasis | 给最重要元素更多留白/空间来强调 | NN/g / Refactoring UI | `verified-high` | 2 个独立来源一致 |
| ui-clickable-affordance | 可点击元素保留可识别线索（颜色/边框/位置/惯例），静态不像按钮 | NN/g Clickable / NN/g Flat Design | `verified-high` | 2 个独立 NN/g 文章直接支持；Norman 书页 pending 作概念旁证，不单独作证据 |
| ui-minimalism | 删除不支持用户任务的装饰/元素；少即是多，但不牺牲可发现性 | Refactoring UI / NN/g Minimalism / NN/g Flat Design | `verified-high` | 3 个独立来源；反例（flat design 问题）同时保留 |
| ui-consistency | 站内一致 + 遵循平台惯例，降低学习成本 | NN/g Consistency / DMMT / Designing Interfaces | `verified-single` | 只有 NN/g 一手可复核；DMMT 与 Designing Interfaces 书页为 `pending`，暂不够升 high |
| ui-cta-hierarchy | 一个屏幕以单一主 CTA 为核心，次要动作降级 | NN/g / Refactoring UI | `verified-high` | 2 个独立来源一致；保留“同等重要动作不硬突出”的边界 |
| ui-not-color-alone | 状态/差异不能只靠颜色，需文字/图标/形状等补充 | NN/g Visual Treatments / Primer | `verified-high` | 2 个独立来源一致 |
| style-editorial-no-radius | 圆角/阴影全局禁用 | 本地 editorial-style-spec / StyleKit | `discarded` | 单风格偏好；无多源支持，不能成为通用美学规则（保留为风格分支） |
| style-editorial-single-color | 只用单色+透明度层级 | 本地 editorial / StyleKit | `discarded` | 单一风格；对数据可视化/多色产品不适用，不能进核心 |
| style-stylekit-score | StyleKit 评分（如 59/100）作为质量依据 | stylekit-editorial.html | `discarded` | 第三方风格库自评，非权威、无研究方法；不作为证据 |
| style-dsh-skin-angle | 全局归零圆角/品牌皮肤正确性 | dsh-deep-whale-inspect | `discarded` | 品牌特定（orca-link）；无通用证据 |
| method-visual-qa | 逐页截图/读图检查溢出、对齐、留白、对比度 | ai-ppt-skill | `verified-single` | 本地实践方法，可复现但无外部研究验证；作为“验证方法”旁证保留 |
| local-supplementary | 本地素材作为唯一权威来源 | local_material_inventory.md | `discarded` | 与定义冲突：本地素材只能补充，不能作为核心唯一来源 |
| apple-hig-typography | Apple HIG 具体字号/行高数值 | Apple HIG 排版页 | `pending` | 官方页 JS 渲染未取到静态正文；待补可读来源后再判 |

## 三、yield_stats

```text
raw_count        : 23
verified_high    : 12   # ui-contrast-text, ui-contrast-nontext, ui-focus-visible,
                        # ui-type-body-scale, ui-spacing-grid, ui-hierarchy-scale,
                        # ui-proximity-group, ui-whitespace-emphasis, ui-clickable-affordance,
                        # ui-minimalism, ui-cta-hierarchy, ui-not-color-alone
verified_single  : 5    # ui-focus-appearance, ui-line-length, ui-font-personality,
                        # ui-consistency, method-visual-qa
discarded        : 5    # style-editorial-no-radius, style-editorial-single-color,
                        # style-stylekit-score, style-dsh-skin-angle, local-supplementary
pending          : 1    # apple-hig-typography
```

## 四、冲突与边界（不平均）

### 4.1-round-vs-sharp

- **圆角/阴影**：Editorial 与 orca-link 主张“全局归零”；tech-dark 与主流设计系统（圆角 16–20px）主张“用圆角”。两派对冲，保留为两个风格分支，不揉成“圆角应适中”的伪共识。
- **极简**：NN/g Minimalism 支持“删”，NN/g Flat Design 指出“过度极简牺牲可发现性”。两条都保留：删除与可发现性并存。
- **主 CTA**：可突出单一主按钮，但“表单/工具栏存在多个同等重要动作”时不可硬突出，边界保留。
- **行宽**：45–75 字符是排印流派风格，不是所有界面（数据表、代码、短标签）的普适规则；降权。
- **单源待证清单**：ui-focus-appearance、ui-line-length、ui-font-personality、ui-consistency、method-visual-qa、apple-hig-typography。

## 五、结论

- 核心规则候选 17 条（12 high + 5 single），其中 6 条单源/待证需要在蒸馏与最终技能中明确降权或标“单源待证”。
- 无来源/纯推断/单风格主张未进入核心；本地素材全部仅作补充。
- 冲突观点保留分支，未被平均。
