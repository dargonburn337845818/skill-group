# Changelog

## 0.2.0 (2026-09-06)

- 新增 **AI 长期记忆机制**：`AI_MEMORY.md` / `DRIVE_LAYOUT.md` / `HANDOFF` 三件套，要求短、单一事实源、只记行为差异、90 天清理、超行压缩。
- 新增 **全盘符整理接管安全协议**：只读盘点 → 盘符账本 → manifest → 用户确认 → 分批 ≤50 项 → 审计可回滚；硬红线覆盖系统目录、密钥、`.git`、虚拟环境、聊天/浏览器数据。
- 新增落地记忆文件：`$HOME/work/AI_MEMORY.md`、`$HOME/work/standards/DRIVE_LAYOUT.md`，并建 `standards/`、`reports/`、`scratch/` 目录。
- 版本从 0.1.0 升到 0.2.0（能力扩展，向后兼容）。

## 0.1.0 (2026-09-06)

- 首版入库。
- 内容：AI 行为总纲 + 文件管理深模块（目录骨架、命名规范、创建决策表、清理归档、硬红线、自检清单）+ 全方面规范索引 + 规范自身元规范。
- 来源：本地已有规范（AGENTS/REPO_STANDARD/dsh-optimization/editorial/SKILL_MAP 等）+ 公开标准（FHS/Google style/12-Factor）+ 专家团结论。
- 专家团：Andrej Karpathy、Lilian Weng、Chip Huyen（第一轮）+ Kent Beck、John Ousterhout、Eric S. Raymond、Martin Kleppmann、Steve McConnell（第二轮，standards 域）。
- 冲突已裁决：硬规则与启发式分层；SKILL 少而深，CONSENSUS 放完整清单。
- 边界：不替代领域规范；文件整理分批、可回滚；涉及用户已有文件必须备份确认。
