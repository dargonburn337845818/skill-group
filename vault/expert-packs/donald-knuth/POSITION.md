# 写作像面对面解释：先给路标，再用小例子和类比；记号小而一致、优先主动语态与可解析短句；排版与文本同等重要，公式规范、引用可解析、编译无未定义引用。

> 风格/方法论推断，非本人原话。

## knuth-signpost

**Trigger**: 写长论文/长证明，读者可能在多步论证中失焦时

**Action**: 开头给路线图（“我们先证引理 X，用它推出主定理”）；每进入一个新阶段用一句话预告；一个困难部分结束后，用一句自然语言复述“刚刚证明了什么”。

**Boundary**: 路标不是内容本身；不要在正文里反复复述整个证明，造成冗长；路标要具体到“为什么下一步”，不是“下面我们继续”。

**SourceRefs**: https://www-cs-faculty.stanford.edu/~knuth/klr.html; http://infolab.stanford.edu/TR/CS-TR-88-1193.html

## knuth-example-analogy

**Trigger**: 抽象定义/算法/记号密集段落，读者难以建立直觉时

**Action**: 给一个可手算的小例子；合适时用日常或已知问题做类比；复杂公式除符号外再用一句自然语言说明它在做什么。

**Boundary**: 类比可能误导，必须说明它在哪里失效；例子不能替代形式证明；不要把正式论证建立在类比上。

**SourceRefs**: https://www-cs-faculty.stanford.edu/~knuth/klr.html; https://oac.cdlib.org/findaid/static/ark:/13030/kt287035zn

## knuth-simple-notation

**Trigger**: 设计记号/算法中的变量名、下标、集合符号时

**Action**: 优先短而浅的记号：单字母、少量下标；首次使用处定义；全文同一概念同一符号；多字母名字用 operatorname/text 等排版，不用意大利字母堆叠；避免无意义的下标层。

**Boundary**: 领域标准记号优先保留；如果为“简单”而改动大家熟知的符号，反而增加认知成本。

**SourceRefs**: https://www-cs-faculty.stanford.edu/~knuth/klr.html; http://infolab.stanford.edu/TR/CS-TR-88-1193.html

## knuth-reader-first-active

**Trigger**: 文字以作者过程为中心、被动句多、空泛连接词多时

**Action**: 把读者的问题放前面；用主动动词；删掉“It is interesting to note / We can see / 不难看出”式元话语；每句话控制在可一次读完的复杂度。

**Boundary**: 学术文本需要精确的限定语；主动语态不是要求删掉所有 hedge；复杂技术句可按句法分段，不能为短句牺牲准确。

**SourceRefs**: https://www-cs-faculty.stanford.edu/~knuth/klr.html; https://oac.cdlib.org/findaid/static/ark:/13030/kt287035zn

## knuth-typesetting-discipline

**Trigger**: 写/修 .tex：长行、排版溢出、未定义引用、公式未编号、文献未解析时

**Action**: 重要公式用显示数学并编号；交叉引用一律 label/ref；使用可解析的 bib 或 thebibliography；编译后检查 undefined references、overfull hbox、未定义引用；保持源文件可读。

**Boundary**: 排版规范不改变内容；个别 cosmetic overfull 可以容忍，但提交前应清零未定义引用并做 clean build。

**SourceRefs**: https://www-cs-faculty.stanford.edu/~knuth/klr.html; https://www-cs-faculty.stanford.edu/~knuth/

## knuth-notation-consistency-symbols

**Trigger**: 同一概念在正文/公式/图中使用了不同记号或缩写时

**Action**: 建立一张符号表（或至少在前言集中定义）；正文、定理、算法、图注使用同一套记号；缩写首次出现给出全称，之后统一。

**Boundary**: 短论文不必单独符号表；但必须保证全文一致；不要因为“好看”在局部换记号。

**SourceRefs**: https://www-cs-faculty.stanford.edu/~knuth/klr.html; http://infolab.stanford.edu/TR/CS-TR-88-1193.html
