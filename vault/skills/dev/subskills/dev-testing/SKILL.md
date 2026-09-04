---
name: dev-testing
description: 测试调试子技能——测试分层、公开接口测试、夹具隔离、flaky 治理与调试最小复现的可执行检查清单；测试锁接口行为，不锁内部实现。
whenToUse: 用户写测试、修 flaky、做调试、设计可测接口或评估覆盖率时；需要判断测试方案与调试路径时。
---

# dev-testing · 测试调试（已蒸馏）

> 定位：测试是对**公开行为**的契约，不是对内部实现的合影。覆盖率是参考，不是完成标准。
> 原则：每个测试必须能变红，锁对外可观测行为；调试先做最小复现，再二分定位。

## 触发条件

- 用户要写单元/集成/E2E 测试、设计测试夹具、评估覆盖、修复 flaky。
- 遇到“偶现失败”“本地过了 CI 挂了”“很难复现”的调试问题。
- 需要判断“这个模块该测什么、怎么测才有效”。

## 核心动作

### 1. 测试分层与选择

- 单元测试：纯逻辑/算法/核心规则，快、确定、内存小。
- 集成测试：跨模块/真实数据库/外部服务通过测试替身或少样本真实依赖。
- E2E 测试：用户关键旅程，数量少、慢、易 flaky，只保关键路径。
- 按风险分配：核心规则多测；装饰/外部展示少测；不要追求所有分支覆盖率。

> 边界：测试金字塔是实践参考，不是铁律；先看行为契约在哪层最容易锁住。

### 2. 测试公开接口

- 测试通过公开 API/CLI/组件 props 触发，不依赖私有函数、内部 state、DOM 细节。
- 断言可观测结果（返回值、输出、状态变更、副作用），不测“是否调用了某内部方法”。
- 每个测试必须先见失败（可证伪），再修绿；否则测试可能是无效的。
- 命名表达行为：`test('用户输入非法时返回 400')`，而不是 `test('function x')`。

> 边界：为了测试加 getter/setter 暴露内部状态，是坏味道；应重构接口而非穿透。

### 3. 夹具、隔离与确定性

- 每个测试独立数据，不依赖执行顺序；用 setup/teardown 清理。
- 时间/随机数/网络/文件系统注入 fake 或固定种子，保证确定性。
- 外部依赖用契约测试或测试替身；不要直接连生产服务。
- 测试数据要小且能快速失败；避免超大 fixture 掩盖问题。

### 4. Flaky 治理

- 先稳定复现：记录失败日志、环境、随机种子、执行顺序。
- 常见原因：共享状态、时间依赖、并发/顺序依赖、外部网络、资源限制、未清理资源。
- 修复后不能只“重跑过了”；要解释根因，并加确定性防护。
- 对慢/不稳定测试做隔离或标记；不要让 flaky 污染主流水线。

### 5. 调试最小复现

- 先拿最小可复现用例：删除无关代码、固定输入、固定并发/顺序、抓完整日志。
- 二分定位：注释/拆分/打印/断点/日志逐步缩小范围。
- 区分环境差异：本地 vs CI、版本、依赖、并发、时区、数据。
- 修 bug 后补回归测试，确保同一问题不会再进来。

## 反例 / 边界

| 反例 | 正确做法 |
|---|---|
| “覆盖率 100% 就完成了” | 覆盖率是信号；要看测试是否锁住行为、能变红 |
| “测试写很多但没有断言” | 每个测试必须有明确可观测断言 |
| “测试调用私有方法省事” | 测试公开接口；私有逻辑通过公开行为验证 |
| “flaky 就重跑一下” | 找根因 + 确定性防护；否则风险仍在 |
| “遇到 bug 直接改代码不写复现” | 先最小复现，再加回归测试 |

## 来源

- [Martin Fowler: TestPyramid](https://martinfowler.com/bliki/TestPyramid.html)
- [Google Testing Blog: Flaky Tests](https://testing.googleblog.com/2016/05/flaky-tests-part-2-classifying-flaky.html)
- [Jest Docs: Testing Basics](https://jestjs.io/docs/getting-started)
- [pytest Docs: Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [Vitest Docs](https://vitest.dev/)
- [Kent Beck: Test Driven Development (book)](https://www.amazon.com/Test-Driven-Development-Addison-Wesley-Signature/dp/0321146530)
- 本地底座：`vault/skills/base/search-source/`、`vault/skills/core-iteration/dev-workflow-consensus/`
