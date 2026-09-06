# Steve McConnell（Code Complete 作者 / 软件构建质量）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 1. std-mcc-naming

**Trigger**: 制定命名约定/评审代码时

**Action**: 名称表达意图与角色；避免误导性缩写；用检查表/工具自动检查命名与可读性。

**Boundary**: 不同语言/生态有不同命名习惯；不要追求风格统一而牺牲领域惯用语。

**SourceRefs**: https://stevemcconnell.com/; https://www.oreilly.com/library/view/code-complete-2nd/0735619670/

## 2. std-mcc-standard-measurable

**Trigger**: 编写质量规范时

**Action**: 把“可读/可维护”翻译成可观察检查（命名规则、函数长度、圈复杂度、测试覆盖）；没有度量手段的口号为反例。

**Boundary**: 度量指标是启发式不是目标；避免为指标优化而伤害真实可读性。

**SourceRefs**: https://en.wikipedia.org/wiki/Steve_McConnell; https://www.oreilly.com/library/view/code-complete-2nd/0735619670/
