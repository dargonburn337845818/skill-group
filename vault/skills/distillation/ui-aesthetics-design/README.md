# UI 美学设计（ui-aesthetics-design）

> 通用网页/组件 UI 美学设计审查与生成的可执行指南。
> 入口是 `SKILL.md`；想深入看规则依据与来源，读 `CONSENSUS.md` / `SOURCES.md`；想直接看用法，读 `examples/`。

## 如何使用

1. 加载 `SKILL.md`（DSH skill 入口）。
2. 按“三步主流程 + 快速检查清单”对界面做审查或生成。
3. 需要完整依据时读 `CONSENSUS.md`；需要逐条来源时读 `SOURCES.md`。
4. 需要对照真实案例时读 `examples/`（01–06）。

## 目录

- `SKILL.md` — agent 可执行摘要（入口）
- `CONSENSUS.md` — 完整规则、证据分级、失效边界、样例对照
- `SOURCES.md` — 可审计来源清单
- `manifest.json` — vault 元数据
- `examples/` — 6 个样例（含灵感站选型实战）
- `audit/` — 构建与审计过程材料，不参与用户日常加载

## 边界

- 不负责品牌/VI/Logo；不绑定技术栈。
- 本地风格材料仅作风格参考/创作溯源，见 `audit/PROVENANCE.md`。
- 部分规则目前只有单一来源或属于风格偏好，已在 `CONSENSUS.md` 中明确标注并给出边界。
- 视觉灵感站（landing.love / land-book / awwwards / onepagelove / lapa.ninja / 21st.dev / siteinspire）只作灵感参考，不作规则证据，见 `SOURCES.md` §7。

## 发布

- 默认交互：进入 `dsh-skill-vault` 仓库目录后运行 `bash scripts/push.sh`（脚本会确认并完成 git add/commit/push）。
- 全自动：配置 git credential helper / CI secret 后，可用 `bash scripts/push.sh --yes --message "..."` 或 `PUSH_CONFIRM=yes PUSH_MESSAGE="..." bash scripts/push.sh`，护栏仍会拦截内部产物。
- 本包不默认自动 git push/commit；自动化必须显式开启。
