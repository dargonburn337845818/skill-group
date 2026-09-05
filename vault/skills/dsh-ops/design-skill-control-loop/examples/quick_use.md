# Quick Use Example

## 场景 1：用户说“技能太多了，帮我收敛”

```
1. 读 enabled.json，统计全局 enabled 数量。
2. 列出“底座三件套”与“非当前场景”的常驻项。
3. 给用户选项：保留哪些、按需哪些、归档哪些。
4. 执行：一次只改一小批，先不热更运行中的 agent。
```

## 场景 2：用户问“这个 skill 还有用吗？”

```
1. 查看 effect-log（若无则如实说没有运行期数据）。
2. 查 CHANGELOG 与最近一轮迭代报告。
3. 用阈值判断：效果率低 / 误触发高 / 连续无行为增量 → 建议降权或归档。
4. 没有数据时，输出“当前无证据，建议先采集 1–2 周”，不直接停用。
```

## 场景 3：用户要“把视频理念做成技能”

```
1. 读取本技能 SKILL.md + 审计报告。
2. 承认来源：HumanLayer / B 站视频。
3. 产出：SKILL.md / CONSENSUS.md / SOURCES.md / manifest.json。
4. 校验：validate-vault / validate-tags / skill_package_check。
5. 入库到 dsh-ops，默认不自动 enable。
```
