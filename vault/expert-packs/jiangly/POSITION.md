# 蒋凌宇（jiangly，中国顶尖算法选手） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

代码风格与解题习惯参考，强调可复现、边界完整

## 结构化条目（style_items）

### 1. jiangly-judge-display-large-int-bug

**Trigger**: 在线判题/IDE 中看到奇怪 N/A、显示错误或答案不匹配，尤其是大整数（约 10^16）或长整型输出时。

**Action**: 先怀疑并排除评测环境/显示 bug：换到标准环境、本地验证、用文件/无 UI 判题输出；不要把环境误判当作题目或算法错误。

**Boundary**: 并非所有 N/A 都是环境 bug；算法错误、精度问题、未定义行为也可能产生类似现象，必须有具体证据才能归因到环境。

**SourceRefs**: https://codeforces.com/blog/entry/93511

### 2. jiangly-human-takeover-environment

**Trigger**: 遇到在线评测显示异常、可疑非标准术语、缺题解或赛制/环境不熟。

**Action**: 先本地/标准环境复现判别环境 bug；非标准术语先查题面定义；无题解时公开问具体题；正式赛前在目标平台跑通编译运行管线；该人工接管时不要继续死磕。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/93511; https://codeforces.com/blog/entry/142536; https://codeforces.com/blog/entry/55506; https://codeforces.com/blog/entry/61066

### 3. jiangly-mirror-contest-real-environment

**Trigger**: 想检验团队在真实比赛节奏/赛制下的水平，而不只是刷题；需要综合排名和多个时间窗口自评

**Action**: 参加/组织未公开的镜像赛（如 Universal Cup），使用 DOMjudge、最后一小时封榜、多个时间窗和综合 rating board 来模拟真实比赛并自评

**Boundary**: 镜像赛只是训练形式，不能替代对具体解题能力/专题弱点的针对性训练；若只想练算法题，真实赛制反而可能分散有限时间

**SourceRefs**: https://codeforces.com/blog/entry/111672

### 4. jiangly-real-env-mirror-pipeline

**Trigger**: 要参加使用不熟悉环境/平台/赛制的正式赛，或团队需要检验真实比赛节奏下的水平；需要把本地/评测机的编译运行方式提前跑通。

**Action**: 提前在目标平台/操作系统上把编译、运行、输入重定向与输出命令跑通成可复制管线；条件允许时参加/组织镜像赛，使用 DOMjudge、最后一小时封榜、多时间窗与综合 rating board 模拟真实赛制并自评。

**Boundary**: 若已非常熟悉该环境，或比赛提供云端/预置环境，额外准备本地管线收益很低；镜像赛只是训练形式，不能替代对具体解题能力/专题弱点的针对性训练。

**SourceRefs**: https://codeforces.com/blog/entry/111672; https://codeforces.com/blog/entry/61066

**SourceRefs（专家总来源）**: https://codeforces.com/profile/jiangly; $WORKSPACE/skills/teacher-consensus-skill/output/teacher_consensus_final.json; $WORKSPACE/skills/teacher-consensus-skill/content/expert_research.md; https://codeforces.com/blog/entry/93511; https://codeforces.com/blog/entry/142536; https://codeforces.com/blog/entry/55506; https://codeforces.com/blog/entry/61066; https://codeforces.com/blog/entry/111672