---
name: copywriting
description: 文案写作子技能——README、PR 描述、公告、PPT 文案、发布说明；重点服务 dev 的去 AI 味与可读性。
---

# 文案写作（copywriting）

> 属于 `writing-module` 子技能。
> 负责表达：把功能、结论、卖点说成人话，让读者一眼看懂、愿意读、不觉得是机器写的。
> 不负责：功能是否成立、数据是否真实、营销承诺是否兑现。

## 触发条件

- dev 模块要写 README、更新日志、PR 描述、公告、版本说明时。
- 需要把 PPT 技术页改写成“听众能跟上”的短句时。
- 用户说“这段话 AI 味太重，帮我改得像人写的”。
- 对外发布文案、开源仓库简介、插件介绍、产品页文案。
- 任何需要“短、具体、有语气”的推广/说明性文本。

## 动作

1. **解析输入**：`topic/domain/audience/type/purpose/tone/constraints`；明确读者是谁、要它们做什么。
2. **先列事实**：把可验证的功能点/数字/动作列出来；没有的事实标 `[待补]`，绝不编造。
3. **选择人味策略**：
   - 去 AI 味：删空泛词（赋能、闭环、抓手、综上所述、首先其次最后）；改用短句、具体动作、第一/第二人称、留出语气停顿。
   - 技术说明：结论先行，再给“怎么用/为什么”，代码/命令用可复制块。
   - PPT 文案：每页一句话主标题 + 不超过三行支撑；一页一个主张。
4. **给出可选风格**：如严肃版 / 轻松版 / 极简版，调用方挑选。
5. **输出**：`text` + 需补填的截图/数据/链接占位 + `notes`（说明改写了哪些 AI 腔）。

## 去 AI 味检查表

- [ ] 有没有“首先/其次/再次/综上所述/总而言之”开头？
- [ ] 有没有“赋能/抓手/闭环/颗粒度/底层逻辑/价值最大化”等空泛词？
- [ ] 有没有“值得注意的是/不难发现/众所周知”这类无效铺垫？
- [ ] 每段第一句是否为具体动作或结论，而非“由于……因此……”的套话？
- [ ] 是否有人称（你/我们）或可感知的场景，而不是主语缺失的被动句？
- [ ] 是否保留必要的技术准确度，没有为了流畅牺牲精度？

## 边界

- 不做事实调查：产品数值、性能结果、竞品对比由调用方提供；缺则 `[待补]`。
- 不夸大承诺：不写“绝对领先”“行业第一”等无法核验的表述。
- 不改变技术结论：dev 说“这个方案取舍是 X”，文案不能偷偷改成“X 最优”。
- 不伪人情味：去 AI 味是让表达自然，不是硬塞表情包或无关段子。

## 示例占位（可替换为真实场景）

```text
场景：插件发布说明
【对象】开发同行；【类型】copy；【约束】去 AI 味、不夸大
【事实】新增 /inject 命令、支持热重载、修复路由残留
【初稿】“本版本赋能了热重载能力，闭环了路由生态……”
【改写】“现在可以直接 /inject 本地插件，不用重启；顺带修了路由表残留的问题。”
```

## 反例

| 不要 | 改为 |
|---|---|
| “基于用户痛点赋能业务闭环” | “现在打开项目，点击一键生成，不用手动配置” |
| “综上所述，本方案具有显著优势” | “这套方案把启动时间从 8 秒压到 1 秒；代价是内存多占 50MB。” |
| “我们非常荣幸地宣布……” | “这个版本新增了三个命令：……” |

## 2026 深度补强（Round 32）

> 来源：Google styleguide、GDS/GOV.UK、PlainLanguage.gov、Keep a Changelog。
> 每条规则都带“触发 / 动作 / 边界”；与前面章节不重复，冲突分支按来源保留，不强行合并。

### R32-1 挖出隐藏动词（nominalization）

- **触发**：句子里出现 `conduct a review`、`make an application`、`carry out an analysis`、`undertake the calculation of` 这类“弱动词 + 动作名词”组合。
- **动作**：把名词还原成动词，删掉 `conduct / make / carry out / undertake / perform / give / reach` 等弱动词；写 `we review`、`apply`、`we analyze`、`calculate`。
- **示例**：
  - “we need to carry out a review of the accounts” → “we need to review the accounts”
  - “make an application” → “apply”
  - “we must undertake the calculation of new figures” → “we must calculate new figures”
- **边界**：如果名词形式是约定俗成的术语/接口名（如 `code review`、`risk assessment`、`API request`），保留名称；只重写叙述性动作，不改命令、类名、标识符。

来源：PlainLanguage.gov · Avoid hidden verbs

### R32-2 拆开名词串（noun strings）

- **触发**：连续 3 个以上名词挤压在一起，例如 `Underground mine worker safety protection procedures development`。
- **动作**：先写动作/主体，再用介词和动词把关系展开；只保留必要名词。
- **示例**：
  - “Underground mine worker safety protection procedures development” → “Developing procedures to protect the safety of workers in underground mines”
  - “Draft laboratory animal rights protection regulations” → “Draft regulations to protect the rights of laboratory animals”
- **边界**：公认技术名词组合（`user interface`、`file system`、`single sign-on`、`command line interface`）保持原样；不要拆包名、路径、类名或品牌名。

来源：PlainLanguage.gov · Avoid noun strings

### R32-3 主谓宾贴紧，修饰语贴紧

- **触发**：句子被插入语拆散（“the company, at the discretion of the board, and after notice … may buy”），或 `only / always` 等修饰语位置产生歧义。
- **动作**：主语、谓语、宾语尽量挨着；把 `only / always` 放在被修饰词旁边；长条件放到句尾、拆成短句或用表格/列表。
- **示例**：
  - “you are only required to provide the following” → “you are required to provide only the following”
  - 复杂 if-then 条款改成表格：`If you submit by email → we must receive it by …`
- **边界**：如果条件只有几个词，且放在前面能避免用户误读（如“Unless you have already submitted…, you must…”），仍可前置；整体原则是“主句尽量靠前”。

来源：PlainLanguage.gov · Place words carefully

### R32-4 先主句，后例外/条件

- **触发**：句子以 `Except as…` / `Unless…` / 长 `If…` 开头，读者必须先读完条件才知道规则。
- **动作**：先把结论/主句说出来，再把例外或条件放到后面；多个条件用 `if` + 列表或表格；若例外只有几个词，前置可以避免误导时再前置。
- **示例**：
  - “Except as described in paragraph (b), the Division Manager will not begin…” → “The Division Manager will not begin… However, see paragraph (b) for an exception.”
  - 双重例外改成直观条件列表，每一条用 `if` 开头。
- **边界**：没有绝对规则，短例外前置是允许的；长且复杂的例子优先拆成列表/表格，而不是塞在一个句子里。

来源：PlainLanguage.gov · Place the main idea before exceptions and conditions

### R32-5 标题用问题或完整陈述，不用泛词

- **触发**：写 README、PR、发布说明的小节标题时出现 `General`、`Application`、`Scope`、`Introduction` 等泛词。
- **动作**：优先问句标题（“How do I install this?”）；其次用完整陈述标题（“Add useful headings”）；避免一个单词的 topic 标题；标题要短于正文；同一文档内标题唯一；一篇文档只用一个 H1。
- **示例**：
  - “Application” → “How do I apply for a grant under this part?”
  - “Indian Rights” → “How do the procedures in this part affect Indian rights?”
- **边界**：`Installation`、`Usage`、`API` 是 README 的常规入口，可用；但不要用它们替代信息本身（每个标题下面要真的有可执行内容）。

来源：PlainLanguage.gov · Add useful headings；Google styleguide · Markdown style guide（Headings）

### R32-6 缩写与简称纪律

- **触发**：技术 README、发布说明中出现多个大写缩写、`e.g.` / `i.e.`，或长名称被硬压成没人认识的首字母缩写。
- **动作**：
  - 每页首次出现时写全称并给缩写（除非受众显然都懂 `HTTP`、`API`、`JSON`），此后用缩写。
  - 优先给“昵称”而不是生造缩写：`ESAC` → “the committee”。
  - 一份文档里的缩写尽量控制在 2–3 个以内，其余一律写全。
  - 不要用 `e.g.` / `i.e.`，写 `for example`、`such as`、`that is`。
  - 缩写内部不用句点：`BBC`，不是 `B.B.C.`。
- **示例**：
  - “Resource Advisory Council (RAC)” 后续可只用 “the Council”，不要再造 `RAC` 堆叠。
  - “COTS (commercial-off-the-shelf software)” 首次说明后，后续用 `COTS` 或 “off-the-shelf software”。
- **边界**：面对开发者受众，通用协议/工具缩写（`HTTP`、`API`、`CLI`、`JSON`）不必展开；若误判“全懂”，缩写会越用越多。

来源：PlainLanguage.gov · Minimize abbreviations；GDS · gds-style-guide-technical（Abbreviations and acronyms）

### R32-7 发布说明 / CHANGELOG 是策展，不是 git log

- **触发**：写 release notes、CHANGELOG.md、版本发布说明。
- **动作**：
  - 按版本组织，最新版本在前，每个版本带日期（推荐 ISO：`2026-09-05`）。
  - 用稳定分类：`Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security`。
  - 顶部保留 `Unreleased` 小节，收集尚未发布的变化。
  - `Deprecated`、`Removed`、breaking change 必须显式列出，不能藏在长句里。
  - 一条条目对应“跨多个 commit 的可感知差异”，不是把 git log 倒出来；过滤 merge commit、噪音提交、文档拼写改动。
- **示例**：
  ```markdown
  ## [1.2.0] - 2026-09-05

  ### Added
  - `/inject` 命令支持本地插件热加载

  ### Changed
  - 默认端口从 8080 改为 9090

  ### Removed
  - 废弃的 `--legacy` 参数（1.1.0 已标记 deprecated）
  ```
- **边界**：GitHub 自动生成的 release notes 可以作为草稿（用 `.github/release.yml` 分类），但发布前仍需人工检查：是否包含所有想发布的变更、是否泄漏不想公开的 commit。

来源：Keep a Changelog 1.1.0

### R32-8 README 最小契约 + Markdown 源可读性

- **触发**：新建/重构 `README.md`，或审查仓库文档源文件。
- **动作**：
  - README 至少包含或指向：这个包/库是什么、维护者/联系人、状态（是否 deprecated / 是否公开 release）、怎么用（可复制命令、示例代码）、相关文档链接。
  - 不重复已有的通用文档或指南：链接到 canonical 文档即可；文档变更和代码变更放同一个提交/PR。
  - Markdown 源保持可读：只用一个 H1、每个标题唯一且完整、正文约 80 列换行（链接/表格/代码块可超长）、代码块用围栏并声明语言、不留行尾空格。
- **示例**：
  ````markdown
  # my-tool

  一句话说明这个工具解决什么问题。

  ## Status
  Experimental，API 可能变化。

  ## Installation
  ```bash
  npm install my-tool
  ```

  ## Usage
  ```bash
  my-tool --dry-run
  ```

  ## Docs
  - [API reference](docs/api.md)
  ````
- **边界**：不要把 80 列规则套在 URL、表格、代码块上；README 不是全部 API 文档的存放地，深内容放 `docs/` 并链接。

来源：Google styleguide · READMEs.md；Google styleguide · Documentation Best Practices；Google styleguide · Markdown style guide
