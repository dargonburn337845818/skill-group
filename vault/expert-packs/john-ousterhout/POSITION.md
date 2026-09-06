# John Ousterhout（斯坦福教授 / A Philosophy of Software Design）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 1. std-john-deep-module

**Trigger**: 评审模块/接口设计时

**Action**: 检查：接口是否小而丰富？调用方是否需要知道内部实现细节？删除它、复杂度是否散落到 N 个调用方？满足后保留为深模块。

**Boundary**: 非所有模块都要深；单实现、极稳的浅模块可直接保留；不要把“接口行数”当深度。

**SourceRefs**: https://web.stanford.edu/~ouster/cgi-bin/book.php; https://en.wikipedia.org/wiki/John_Ousterhout

## 2. std-john-comments

**Trigger**: 写技术文档/代码注释时

**Action**: 注释写“为什么、约束、权衡、不变量”，不重述代码；错误信息要解释如何修复。

**Boundary**: 不要写流水账注释；不应让注释替代可读命名；接口契约本身应尽量在类型/签名中表达。

**SourceRefs**: https://web.stanford.edu/~ouster/cgi-bin/book.php; https://www.oreilly.com/library/view/a-philosophy-of/0132146591/
