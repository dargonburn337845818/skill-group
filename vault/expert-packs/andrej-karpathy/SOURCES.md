# Sources（Andrej Karpathy）

验证方式：以下 URL 均经 `curl -L -A "Mozilla/5.0" -s -o /dev/null -w "%{http_code}"` 验证返回 HTTP 200；内容为公开可访问材料（HTML 正文可提取；karpathy.ai 为 SPA，正文提取受限，仅用于位置/作品列表佐证）。

| URL | 类型 | 用途 | 验证 |
|---|---|---|---|
| https://karpathy.ai/ | 作者主页 | 自述“I like to train deep neural nets”；作品/课程列表（Zero to Hero、LLM 视频、Software 2.0 链接） | HTTP 200 |
| https://karpathy.ai/zero-to-hero.html | 作者课程页 | “从零到英雄”循序渐进教学大纲，从 scratch 写 backprop/char-level LM/GPT | HTTP 200 |
| https://karpathy.github.io/2019/04/25/recipe/ | 作者博客文章（A Recipe for Training Neural Networks） | 训练流程配方：数据探索/骨架/基线/验证/过拟合单 batch；leaky abstraction 与 silent failure | HTTP 200 |
| https://karpathy.github.io/2015/05/21/rnn-effectiveness/ | 作者博客文章（RNN effectiveness） | 亲手实现 RNN/字符级语言模型，展示简单模型惊人效果与教学角度 | HTTP 200 |
| https://karpathy.bearblog.dev/blog/ | 作者新博客列表 | Software 2.0 时代后的动手/观点文章索引（LLM year review、verifiability 等） | HTTP 200 |
| https://karpathy.github.io/ | 作者旧博客列表 | 作品时间线（microgpt、recipe、RNN、PhD 生存指南等） | HTTP 200 |

备注：`github.com/karpathy`、`github.com` 各仓库、`youtube.com/@AndrejKarpathy`、`medium.com`（Software 2.0 原文）无法经 curl 验证（000），未列入 verified-high；`projecteuclid`、`statmodeling` 单篇等未通过可访问性核验。所有条目均为风格/方法论推断，非本人原话。
