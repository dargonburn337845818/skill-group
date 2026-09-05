# Round 32：高质量搜索 → 内容蒸馏补强（12 个技能，两批）

> 用户明确：不是只做包级卫生，而是要“搜索更加高质量的信息填充”现有技能。本报告合并两批：第一批 6 个 + 第二批 6 个。

## 本轮做法

1. 选 6 个内容薄弱/高价值的技能：dev-security、dev-frontend、dev-testing、dev-performance、copywriting、paper-outline。
2. 每个技能派 1 个子代理：用 web_search 找 6–12 条可核验的一手/权威来源；蒸馏 4–8 条真正新增的可执行规则/反例/示例。
3. 子代理直接编辑：
   - `SKILL.md` 追加 `## 2026 深度补强（Round 32）`（保留原有内容，插入到原来源节之前）；
   - `SOURCES.md` 追加/重建 `## Round 32 新增来源` 台账。
4. 未改 manifest、未删旧内容。

## 交付增量（每技能摘要）

| Skill | 新增要点 | 来源数 |
|---|---|---|
| dev-security | R1–R8：BOLA/IDOR、Mass Assignment、输入规范化、JWT 完整校验、OAuth/OIDC PKCE、SSRF、资源/限流、SBOM/密钥生命周期 | 14 |
| dev-frontend | 组件边界组合/状态派生查询缓存/a11y 焦点与语义/性能 CLS-INP/安全 XSS-CSP/用户可见测试 | 12 |
| dev-testing | 测试尺寸、跨层去重、DB 隔离三选一、容器就绪、flaky 治理、随机顺序、单 Act、E2E 数量门禁 | 11 |
| dev-performance | 性能预算工程化、RUM/Lab 分工与 INP 拆解、LCP 优化、内存快照、EXPLAIN ANALYZE 证据链、trace/饱和度、回归护栏 | 12 |
| copywriting | 隐藏动词、名词串、主谓宾贴紧、先主句后例外、标题/缩写纪律、CHANGELOG 策展、README 最小契约 | 12 |
| paper-outline | 综述方法选择、概念分解检索、问题×方法矩阵、四类研究空白、可行性三角、limitations 反向取证、最小可证伪实验、冲突分支模板 | 12 |

## 第二批交付增量（6 个技能）

| Skill | 新增要点 | 来源数 |
|---|---|---|
| dev-backend | RFC 9457/错误语义、幂等键、expand–contract、迁移不可变、条件请求、HTTP 鉴权、OpenTelemetry 标准 | 10 |
| dev-concurrency | 内存序/acquire-release、异步阻塞隔离、锁外回调、死锁定位、条件变量 while、公平性/有界背压、尾延迟测量、race detector | 12 |
| dev-ai-engineering | capability/regression eval 分家、transcript+outcome 评分、三类 grader、eval loophole、工具输出 schema 校验、可见可审计、prompt caching 可观测、压缩审计、workflow/agent 分界、RAG 双组指标与循环检索 | 12 |
| dev-ops-sre | CI 供应链门禁、OIDC 短时凭据、镜像 SBOM/provenance、容器运行时硬门禁、指标基数、trace 采样、SLO 燃烧率、Canary 自动分析门禁 | 12 |
| dev-remove-ai-flavor | 机器残留/排版指纹、结构性 AI 把戏、无源权威与假深度、中文 AI 味专项、表演式热情、可测量验证、场景语气定标 | 10 |
| academic-writing | 摘要自包含后写、CARS 引言、结论综合、natbib/biblatex 语义引用、BibTeX 卫生、大文档分层、编译链与日志清零 | 12 |

## 验证

- vault 包检：50 / 50 仍 100 分
- 本地包检：20 / 20 仍 100 分
- `validate-vault.mjs`：OK（22 skills）
- `validate-tags.mjs`：OK（50 manifests）
- core-iteration smoke（contract/behavior/package/scorecard）：PASS

## 下一批候选

dev-backend、dev-concurrency、dev-ai-engineering、dev-ops-sre、dev-remove-ai-flavor、dev-art-ppt、academic-writing、speech-writing、research 其余子技能、teacher-math-consensus 等。
