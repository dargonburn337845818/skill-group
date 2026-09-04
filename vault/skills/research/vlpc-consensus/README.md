# NOMA-VLPC 论文总结 · 交付清单

本目录由以下工作流生成：

1. 读取 `D:\<论文资料目录>` 中的论文 PDF 与学长 PPT 模板；
2. 确定论文内容与领域；
3. 按 `distillation-consensus` 共识蒸馏该领域可执行知识；
4. 克隆并载入 `xzzcy0517/ai-ppt-skill`；
5. 从 StyleKit Editorial 页面提取设计 token，新增 `ai-ppt-skill/themes/editorial.md` 主题；
6. 用 Editorial 风格生成 HTML、口述稿与可编辑 PPTX。

## 文件

| 文件 | 说明 |
|---|---|
| `00-论文内容与领域判定.md` | 论文基本信息、领域、贡献、关键结果、阅读顺序 |
| `01-相关文献与可访问来源.md` | 相关论文、中文/开放获取入口、关键研究者、找论文路径 |
| `02-VLPC领域教师共识.md` | Agent 辅导用领域共识：触发/动作/边界/来源/用户话术 + 提问协议 + 反例 |
| `03-vlpc_teacher_consensus.json` | 同一共识的机器可读版本（primitive 结构） |
| `04-组会报告技巧共识.md` | 组会文献报告方法论：结构、时间、PPT 原则、应对提问、Agent 辅导纪律 |
| `05-组会模拟问答准备.md` | 针对本论文的 13 个组会模拟问题与参考答案 |
| `06-组会报告Agent提示词.md` | 可直接粘贴给 Agent 的提示词，让它按组会报告方式辅导你 |
| `slides.html` | Editorial 风格 HTML 演示页（10 页详细学习版，可在浏览器打开预览、`?slide=N` 单页查看） |
| `口述稿.md` | 10 页详细版口述稿，适合照读，已写入 PPTX 演讲者备注 |
| `NOMA-VLPC_论文总结_Editorial.pptx` | 可编辑的 Editorial 风格 PPT（10 页详细学习版，16:9，带备注） |
| `build_editorial_pptx.py` | Linux 环境下由 HTML 内容镜像生成 10 页原生 PPTX 的脚本 |
| `slides_组会模板.html` | **6 页组会报告模板版** HTML，按学长 PPT 结构：封面→引言→做了什么→怎么做（定位）→怎么做（通信）→实验与讨论 |
| `口述稿_组会模板.md` | 6 页组会报告口述稿，已写入对应 PPTX 备注 |
| `NOMA-VLPC_组会报告_学长模板版.pptx` | **推荐用于组会汇报的 6 页 PPT**，Editorial 风格，可编辑 |
| `build_groupmeeting_pptx.py` | 生成 6 页组会报告 PPTX 的脚本 |

## 关于 ai-ppt-skill

- 已克隆到：`$WORKSPACE/ai-ppt-skill`
- 已新增主题：`$WORKSPACE/ai-ppt-skill/themes/editorial.md`
- 已更新 `SKILL.md` 风格表，加入 `editorial`。
- 当前 DSH 技能目录只读，无法自动安装到全局；如需全局载入，可把该目录复制到你的 Agent Skill 目录（如 `~/.agents/skills/ai-ppt`、`~/.claude/skills/ai-ppt`）。

## 转换说明

- 官方 `html_to_ppt.py` 依赖 macOS + Chrome（截图式 PPT）。
- 当前 Linux 环境没有 Chrome，因此本目录额外生成了**可编辑的原生 PPTX**（python-pptx），风格与 `slides.html` 一致。
- 若你之后在 Mac 上运行官方脚本：
  ```bash
  AI_PPT_SKILL_DIR=$WORKSPACE/ai-ppt-skill
  python3 "$AI_PPT_SKILL_DIR/scripts/html_to_ppt.py" slides.html 输出.pptx --notes 口述稿.md
  ```
- 改版建议：只改 `slides.html` / `口述稿.md`，再重跑脚本；不要直接编辑 PPT 里的图片版。

## 原始文件位置

论文与学长 PPT 在 `$MOUNT_D/本科生进组看论文`，当前挂载为只读；本目录产物在 `$WORKSPACE/vlpc-editorial-output`，请自行复制回 Windows 目标目录。
