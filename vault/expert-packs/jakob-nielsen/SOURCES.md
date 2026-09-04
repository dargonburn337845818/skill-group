# Sources

## 验证方式

- 全部来源通过 `curl -L -A "Mozilla/5.0" -s -o /dev/null -w "%{http_code}"` 请求返回 **HTTP 200**。
- 均为公开材料：Nielsen Norman Group 官方文章/人物页。其中 `ten-usability-heuristics` 页面为 2024 年更新版（原文 1994）。
- 不把第三方书评/摘要当依据；以下均为 NN/g 署名文章。

## 来源表

| URL | 类型 | 用途 |
|---|---|---|
| https://www.nngroup.com/people/jakob-nielsen/ | 官方人物页 | 确认身份/履历/著作，佐证可用性先驱定位 |
| https://www.nngroup.com/articles/ten-usability-heuristics/ | NN/g 署名文章 | 10 usability heuristics 完整内容 |
| https://www.nngroup.com/articles/how-users-read-on-the-web/ | NN/g 署名文章 | 用户扫读行为、可扫读文案/客观语言/简练原则 |
| https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/ | NN/g 署名文章 | 5 用户曲线、多轮小测试、异质人群边界 |
| https://www.nngroup.com/articles/usability-101-introduction-to-usability/ | NN/g 署名文章 | 可用性五维、utility、用户测试三要素、迭代设计 |

## 说明

- **verified-high 源**均返回 HTTP 200，且为 NN/g 官方一手署名文章。
- 所有 Trigger/Action/Boundary 均由上述一手文章归纳，非 Nielsen 本人原话。
