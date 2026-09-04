# Sources（Andrew Gelman）

验证方式：以下 URL 均经 `curl -L -A "Mozilla/5.0" -s -o /dev/null -w "%{http_code}"` 验证返回 HTTP 200；内容为公开可访问材料（贝叶斯工作流书站为 HTML 正文，博客内容取自 RSS feed，BDA3 为书页，OSF 文件为 PDF）。

| URL | 类型 | 用途 | 验证 |
|---|---|---|---|
| https://avehtari.github.io/Bayesian-Workflow/ | 贝叶斯工作流书站（Gelman et al. co-author） | 迭代建模/模型检查/模拟实验；明确“not a checklist or cookbook” | HTTP 200 |
| https://avehtari.github.io/Bayesian-Workflow/coronavirus/coronavirus.html | 贝叶斯工作流 case study（Ch 19） | 分层模型构建、测量误差/代表性偏差、预测检查 | HTTP 200 |
| https://statmodeling.stat.columbia.edu/feed/ | Gelman 博客 RSS feed（全文内容） | 工作流、显著性怀疑、影响点、诚实表达等一手博客语料 | HTTP 200 |
| https://aaltodoc.aalto.fi/items/dcfa9513-b4bc-44b3-ba2d-1594a010bd3c/full | Aalto 发表记录（Statistical workflow，Gelman/Vehtari/McElreath） | 统计工作流：描述/建模/计算/诊断一体 | HTTP 200 |
| https://www.amazon.com/Bayesian-Data-Analysis-3rd/dp/1439840954 | BDA3 书页 | 贝叶斯数据分析教材出处；覆盖先验/后验/模型检查 | HTTP 200 |
| https://files.osf.io/v1/resources/ktc3e_v2/providers/osfstorage/67a0c7f8e7c507e44344d531?action=download&direct&version=1 | 作者书籍 PDF（Gelman & Hill） | 回归/多层模型与贝叶斯方法的一手资料 | HTTP 200 |

备注：blog 单篇文章 URL、projecteuclid 全文页返回 403/anti-bot，未列入 verified-high；`github.com`、`youtube.com` 等无法经 curl 验证（000），未列入。所有条目均为风格/方法论推断，非本人原话。
