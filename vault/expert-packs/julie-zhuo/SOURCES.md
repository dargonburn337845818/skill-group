# Sources

## 验证方式

- 可用 URL 均通过 `curl -L -A "Mozilla/5.0" -s -o /dev/null -w "%{http_code}"` 请求返回 **HTTP 200**。
- 特别说明：`medium.com/@joulee` 与 `lg.substack.com` 直接 curl 请求被拒/超时（返回 000），因此**未列入 verified-high**；其论文内容通过可访问的官方站/访谈/二手笔记（注明原始出处）获取。
- 以下为公开材料：Julie Zhuo 个人官网、书页、Intercom 官方访谈记录，以及引用其 Substack/Medium 原文的可访问笔记页/镜像页。

## 来源表

| URL | 类型 | 用途 |
|---|---|---|
| https://www.intercom.com/blog/podcasts/podcast-julie-zhuo-on-product-design/ | 第三方官方博客访谈记录（Intercom） | 好的设计 feels obvious、设计原则要有争议、设计师/工程师配比、用户体验层级（useful→easy→feel） |
| https://www.juliezhuo.com/ | 个人官网 | 身份/角色/代表作定位 |
| https://www.juliezhuo.com/book/manager.html | 个人官网书页 | 《The Making of a Manager》要点：Purpose / People / Process、反馈、委托 |
| https://www.pelayoarbues.com/literature-notes/articles/the-looking-glass-the-craft-of-creating | 二手读书笔记/引用页（注明原出处 lg.substack.com） | 先对齐 Why + 无歧义 outcome、先定义用户旅程再定义功能 |
| https://www.pelayoarbues.com/literature-notes/articles/the-death-of-product-development-as-we-know-it | 二手读书笔记/引用页（注明原出处 lg.substack.com） | AI 时代 idea garden → prototype-and-prune → polish |
| https://www.pelayoarbues.com/literature-notes/articles/the-looking-glass-get-over-yourself | 二手读书笔记/引用页（注明原出处 lg.substack.com） | we-mentality、公司是 team 而非 family |
| https://echai.ventures/startingup/from/the-year-of-the-looking-glass-medium | 二手镜像/聚合页（引用 Medium 原文） | “测试的 bar”与“发布的 bar”分开决策 |
| https://www.amazon.com/Making-Product-Governing-Doing-ebook/dp/B077WF5J9H | 书页（Amazon） | 原书/原论文存在性参考 |

## 说明

- **verified-high 一手源**：Intercom 官方访谈、juliezhuo.com、juliezhuo.com/book/manager.html（均 HTTP 200）。
- 二手笔记/镜像源（pelayoarbues、echai）可作为补充；它们明确标注原始作者为 Julie Zhuo，但**不是一手页**，在引用时保留该层级。
- 所有 Trigger/Action/Boundary 均由上述公开材料归纳，非 Julie Zhuo 本人原话。
