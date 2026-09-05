# 彼得·米特里切夫（Petr，俄罗斯传奇选手） · 风格/方法论蒸馏

> 风格/方法论推断，非本人原话；来源见下方 SourceRefs。

## 立场概要

先假设简单解存在，用通过人数/最简解释做决策先验；在优化/启发式问题上关注边界与可验证性

## 结构化条目（style_items）

### 1. petr-heuristic-scoring-function-search

**Trigger**: 在 heuristic/marathon/optimization 题中，人能写出“每一步按某个打分选下一步”的贪心框架，但最优打分函数未知

**Action**: 先实现一个参数化的贪心基线（决策 = argmax 打分函数），再用 LLM/进化算法等在打分函数参数空间搜索；不必一上来就做复杂局部搜索/模拟退火

**Boundary**: 若没有可靠的贪心框架、或打分函数空间太大且单次评估极贵，参数搜索可能不如成熟的局部搜索；对需要精确最优解的普通竞赛题也不适用

**SourceRefs**: https://codeforces.com/blog/entry/137005

### 2. petr-heuristic-scoring-search

**Trigger**: heuristic/marathon 题中能写出“按某个打分选择下一步”的贪心框架，但最优打分函数未知。

**Action**: 先实现参数化贪心基线，再在打分函数参数空间用搜索/进化/LLM 自动优化，而不是一上来就做复杂局部搜索。

**Boundary**: 需要结合具体问题验证；此为风格推断，不代表该专家在所有场景的唯一做法。

**SourceRefs**: https://codeforces.com/blog/entry/137005

**SourceRefs（专家总来源）**: https://codeforces.com/profile/Petr; https://blog.mitrichev.ch/2020/04/a-cheese-week.html; https://codeforces.com/blog/entry/137005; $WORKSPACE/skills/teacher-consensus-skill/output/teacher_consensus_final.json