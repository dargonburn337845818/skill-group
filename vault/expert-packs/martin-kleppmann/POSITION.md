# Martin Kleppmann（Designing Data-Intensive Applications 作者）

> 风格/方法论推断，非本人原话；来源见 SOURCES.md。

## 1. std-klepp-data-lineage

**Trigger**: 创建/归档数据文件时

**Action**: 记录来源、生成时间、schema、版本、校验方式；不把“能跑”当可复现。

**Boundary**: 原始数据/离线资源不应随意删除；生成物/中间物与原始数据分离。

**SourceRefs**: https://martin.kleppmann.com/; https://dataintensive.net/

## 2. std-klepp-fault-models

**Trigger**: 制定可靠性/一致性规范时

**Action**: 先列故障模式与不变量（可丢失、可重复、可乱序、可失败），再定技术方案；规范要能回答“某层失败会怎样”。

**Boundary**: 不要用“强一致/最终一致”当口号；具体接口必须单独声明级别与代价。

**SourceRefs**: https://dataintensive.net/
