# Sources（Hadley Wickham）

验证方式：以下 URL 均经 `curl -L -A "Mozilla/5.0" -s -o /dev/null -w "%{http_code}"` 验证返回 HTTP 200；内容为公开可访问材料（HTML 正文可提取，PDF 为官方论文，SPA 页面正文提取受限时在用途中注明）。

| URL | 类型 | 用途 | 验证 |
|---|---|---|---|
| https://hadley.nz/ | 作者主页 | 自述：工具（计算/认知）让数据科学更容易更快更有趣；书籍入口 | HTTP 200 |
| https://r4ds.hadley.nz/ | 作者著作（R for Data Science 2e） | 数据科学流水线：导入/整理/变换/可视化/建模/沟通；可复现与认知资源管理 | HTTP 200 |
| https://vita.had.co.nz/papers/tidy-data.pdf | 作者学术论文（Tidy Data / JSS） | 整洁数据定义：变量在列、观测在行 | HTTP 200 |
| https://design.tidyverse.org/ | 作者著作（Tidy design principles） | API/函数/参数/错误的设计原则 | HTTP 200 |
| https://cran.r-project.org/web/packages/tidyverse/vignettes/manifesto.html | 作者 manifesto | 四条 tidy API 原则：复用数据结构/管道组合/函数式/为人设计 | HTTP 200 |
| https://ggplot2-book.org/ | 作者著作（ggplot2） | 图形语法与为理解数据而绘图 | HTTP 200 |
| https://adv-r.hadley.nz/ | 作者著作（Advanced R） | R 语言底层与函数式语义 | HTTP 200 |

备注：github.com/tidyverse、youtube.com 等无法经 curl 验证（000），未列入 verified-high。所有条目均为风格/方法论推断，非本人原话。
