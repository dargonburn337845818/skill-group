# Eric S. Raymond（The Art of Unix Programming 作者）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 1. std-esr-filesystem

**Trigger**: 规划目录/文件/脚本时

**Action**: 目录即模块地图：一个目录一个概念；文件名说清职责；配置文件与数据分开；用小工具组合而不是大而全。

**Boundary**: 特定领域（数据密集型/游戏/UI）可能需要不同组织；不要为了“Unix 味”牺牲业务内聚。

**SourceRefs**: http://www.catb.org/~esr/writings/taoup/; https://en.wikipedia.org/wiki/The_Art_of_Unix_Programming

## 2. std-esr-critical-think

**Trigger**: 写规范时

**Action**: 先写“为什么”（问题/风险），再给检查表；反例与边界至少和正例一样重要。

**Boundary**: 规范太长会没人读；只写教条不写动机等于给 AI 一堆不可判断的词。

**SourceRefs**: http://www.catb.org/~esr/writings/taoup/
