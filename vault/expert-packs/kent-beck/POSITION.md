# Kent Beck（软件工程 / 测试驱动开发 / 极限编程）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 1. std-kent-test-first

**Trigger**: 制定/评审开发规范时

**Action**: 把“先写失败测试→最小实现→重构”写成可检查步骤；每步都可执行、可回滚；用简单设计（YAGNI）砍掉不必要的抽象。

**Boundary**: 不能把所有任务都硬套 TDD；探索性/一次性实验、UI/演示可先出原型；测试太多也可能变成负担。

**SourceRefs**: https://en.wikipedia.org/wiki/Test-driven_development; https://www.oreilly.com/library/view/extreme-programming-explained-2nd/0321278658/

## 2. std-kent-small-steps

**Trigger**: 大规模改动或重构时

**Action**: 拆成小步、每步保持行为不变且可提交；频繁集成、快速反馈；规则写“最小改动 + 可验证增量”。

**Boundary**: 没有测试保护的裸重构风险高；团队无法持续集成时先补基础设施，不先堆规范。

**SourceRefs**: https://en.wikipedia.org/wiki/Kent_Beck; https://www.oreilly.com/library/view/extreme-programming-explained-2nd/0321278658/
