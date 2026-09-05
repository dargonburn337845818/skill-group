# 突变检查记录（checks_observed_red）

## check-id: dev-network-package-boundary

- 操作：临时把 SKILL.md 中所有「边界 / 反例 / 失效 / 不适用」替换为 `XYZ`。
- 期望：`skill_package_check.py` 应报 `body missing boundary/failure-mode section`。
- 实测：`ok=false`，issue 为 `body missing boundary/failure-mode section`（变红）。
- 恢复：从备份还原 SKILL.md；复跑 `skill_package_check.py`，`ok=true`、score 100（变绿）。
- 结论：该检查见过失败又恢复，可作为发布前可证伪检查。

## 静态检查记录

- `python3 scripts/domain_recognize.py --validate-data` → `OK: 15 domain(s), 54 expert(s) validated`
- `python3 tools/skill_package_check.py vault/skills/dev/subskills/dev-network` → `ok=true`, score 100
- `node scripts/validate-vault.mjs` → `OK: 19 skill(s) validated in vault/skills`
