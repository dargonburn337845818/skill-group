# 安全是系统属性而不是单个产品功能：从威胁建模出发，先看链路最弱环节与失败模式；默认把信任当作待证假设，识别系统内的欺骗者；安全是持续过程而非一次性采购；把风险感知、激励与人的心理纳入安全决策；对规则系统保持“可被 hack”的视角

> 风格/方法论推断，非本人原话。

## item

**Trigger**: 评审或设计安全方案、安全产品、安全架构时

**Action**: 先做威胁建模：列出资产、攻击者、攻击面与失败模式；从系统/链路整体看安全，而不是只看某一算法或组件；寻找并加固最弱环节，避免只在最强环节上投入

**Boundary**: 风格/方法论推断，非本人原话；不用于绕过具体合规清单

**SourceRefs**: https://www.schneier.com/essays/archives/2000/04/the_process_of_secur.htm; https://www.schneier.com/news/archives/2003/09/bruce_schneier_the_e.html

## item

**Trigger**: 评估“这个产品/补丁/升级后就安全了”的宣称时

**Action**: 默认不信任“产品即安全”：安全是过程不是产品；检查监控、响应、更新、流程与人在回路，而不是把希望寄托在下一个产品或补丁上

**Boundary**: 风格参考；不表示所有安全产品无效，具体选型仍需证据与评估

**SourceRefs**: https://www.schneier.com/essays/archives/2000/04/the_process_of_secur.htm

## item

**Trigger**: 设计信任边界、权限模型、零信任或第三方接入时

**Action**: 把信任当作待证假设而非理所当然：复杂系统中总存在欺骗者/寄生虫，信任由社会机制、声誉、法律、技术与监控共同支撑；对不可信输入与不可信主体默认低信任

**Boundary**: 不是“绝对不信任任何人”，而是把信任作为安全分析起点与风险项

**SourceRefs**: https://www.schneier.com/books/liars-and-outliers-chapter1; https://www.schneier.com/news/archives/2003/09/bruce_schneier_the_e.html

## item

**Trigger**: 讨论安全措施或向非技术人群解释风险时

**Action**: 同时区分客观风险（概率、有效性）与主观感受（恐惧、心理反应）；沟通与决策中把激励机制、经济成本、人类行为纳入权衡，而不是只给数学概率

**Boundary**: 这是补充视角，不替代正式风险量化；风格推断而非原话

**SourceRefs**: https://www.schneier.com/crypto-gram/archives/2007/0228.html; https://www.schneier.com/books/beyond-fear/

## item

**Trigger**: 面对规则系统、激励结构、AI/自动化系统或复杂社会系统时

**Action**: 采用“任何系统都可被 hack”的视角：规则必有漏洞、歧义与非预期后果；先问系统允许什么、设计者没想到什么；考虑攻击者的速度、规模与自动化是否会击穿现有防御

**Boundary**: 宏观安全思维，不作具体代码级安全审计的替代

**SourceRefs**: https://www.schneier.com/essays/archives/2023/02/the-big-idea-bruce-schneier.html

## item

**Trigger**: 选择或评审密码算法、协议与实现时

**Action**: 倾向公开、经得起公开审查的算法与协议；算法只是安全链条中的一环，必须同时检查实现、协议操作、部署环境与人类操作

**Boundary**: 不提供具体算法选型认证；风格/方法论推断

**SourceRefs**: https://www.schneier.com/essays/archives/2000/04/the_process_of_secur.htm; https://www.schneier.com/news/archives/2003/09/bruce_schneier_the_e.html
