# 写数学论文先确定“这篇在说什么”，再写给一个具体读者；记号少而一致，定义首次出现处说清；证明要讲清推理路径，不以“显然”代替核验；草稿先快速定型，再按论证链精修。

> 风格/方法论推断，非本人原话。

## halmos-say-something

**Trigger**: 开始写数学论文/章节，或某章读完不知道“这篇在说什么”时

**Action**: 动笔前用一句话回答“这篇论文在说什么”；把主定理/主结果放到引言显眼处；每个后续章节都追问“它服务于哪一句话”；不服务的章节降为附录或删掉。

**Boundary**: 探索性笔记可以先散漫；但公开论文必须收敛到单一主 claim，且不能把“只写一个结果”误解为“只能有一个小节”。

**SourceRefs**: http://www.mat.uc.pt/~pedro/lectivos/LaTeX/how-to-write-mathematics.pdf; https://mathcomm.org/paul-halmos-on-writing-mathematics/

## halmos-write-for-reader

**Trigger**: 决定背景介绍深度、术语解释量、或“这段该不该展开”时

**Action**: 想象一个具体读者（如相邻方向的研究生/同事），而不是“所有人”；先给为什么和直觉，再给形式化；默认读者不知道你脑内的背景，但也不要重复对方已知的基础。

**Boundary**: 面向专家的理论论文可以极高密度；不要为了“照顾读者”牺牲精确性或把已知基础知识全部重述。

**SourceRefs**: https://mathcomm.org/paul-halmos-on-writing-mathematics/; http://www.mat.uc.pt/~pedro/lectivos/LaTeX/how-to-write-mathematics.pdf

## halmos-notation-minimal

**Trigger**: 符号很多、临时记号、或同一概念多个符号时

**Action**: 符号最小化：只给必须的记号；首次出现处定义；同一符号全文同一含义；只用一次的概念优先用文字表达；复合下标/多字母名字用清晰排版（如 operatorname/text）。

**Boundary**: 标准学科记号应保留；最小化不是“禁用符号”，而是不制造读者负担；若标准记号更省心，不要为了个性另造。

**SourceRefs**: http://www.mat.uc.pt/~pedro/lectivos/LaTeX/how-to-write-mathematics.pdf; https://mathcomm.org/paul-halmos-on-writing-mathematics/

## halmos-proof-communicates

**Trigger**: 写证明时公式堆积、出现“明显/显然/易得”，或读者可能看不见步骤时

**Action**: 先用自然语言一句话给出证明计划；公式之间用文字说明“这步为什么成立”；把非显然的核验单列为小引理或显示公式；把“显然”当成对读者的警告，而不是证明的一部分。

**Boundary**: 不要把每个算术步骤都展开；目标是让逻辑路径可追踪，不是把证明写成小学生作业。

**SourceRefs**: http://www.mat.uc.pt/~pedro/lectivos/LaTeX/how-to-write-mathematics.pdf; https://mathcomm.org/paul-halmos-on-writing-mathematics/

## halmos-examples

**Trigger**: 抽象定义/定理刚给出，或读者可能误解适用边界时

**Action**: 定义后紧跟一个小而具体的例子；定理后给一个极端/退化情形或反例显示边界；用例子检查符号与措辞是否自然。

**Boundary**: 例子是说明不是证明；不能把“例子里成立”当成一般成立；反例要精确且可核验。

**SourceRefs**: http://www.mat.uc.pt/~pedro/lectivos/LaTeX/how-to-write-mathematics.pdf; https://mathcomm.org/paul-halmos-on-writing-mathematics/

## halmos-rewrite-argument-first

**Trigger**: 初稿读起来像“我先做 A，再做 B”，或修改时只调措辞不改结构时

**Action**: 先快速起草，再按“论证链”而不是“时间线”重排；引言最后写；删掉不做工作的句子；以陌生读者身份重读，遇到要猜测的地方就停下来补清楚。

**Boundary**: 重写不能改变数学内容与证明强度；时间线叙事在讲“怎么想到”时可以有，但不能冒充论证结构。

**SourceRefs**: http://www.mat.uc.pt/~pedro/lectivos/LaTeX/how-to-write-mathematics.pdf; https://archive.org/download/XA889AHDH89AX8S98S88SXQ8SD9HD8Q9SQJSQ8H/%5BP.R._Halmos%5D_I_Want_to_Be_a_Mathematician_An_Aut%28BookZZ.org%29.pdf
