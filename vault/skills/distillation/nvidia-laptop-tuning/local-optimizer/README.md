# 本地电脑设置一键优化脚本（安全版）

> 纯 PowerShell，默认 **dry-run**；必须显式 `-Apply` 才会写设置。
> 写之前自动备份：电源方案、`.wslconfig`、相关注册表；提供 `LocalOptimizer.restore.ps1` 一键回滚。
> **不碰 BIOS、不碰驱动、不超频、不默认开启硬件加速 GPU 调度（HAGS）。**

## 它做什么（安全项）

| 项 | 动作 | 可逆 |
|---|---|---|
| 电源计划 | 备份当前方案；切到高性能（或复制当前方案为优化副本）；插电 CPU 调速 5–100%、磁盘不休眠、USB 选择性挂起关 | 可恢复原方案 |
| WSL2 | 备份并写入 `%USERPROFILE%\.wslconfig`：memory=10GB / processors=12 / swap=4GB | 可恢复/删除 |
| 游戏设置 | Game DVR 关闭、Game Mode 开启（HKCU 注册表） | 可恢复注册表 |
| HAGS | **默认不做**；显式 `-IncludeHags` 且管理员才改，需重启 | 可恢复 |

它**不会**：
- 安装/卸载驱动；
- 刷 BIOS/EC；
- 修改 G-Helper 的风扇/功耗档位；
- 自动执行 `wsl --shutdown`（除非显式 `-RestartWsl`）。

## 使用

### 1. 先测试（不写任何东西）

```powershell
Set-ExecutionPolicy -Scope Process Bypass
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\LocalOptimizer.ps1 -Test
```

输出会显示当前驱动（如果检测到 616.56 会提醒装 Hotfix）、G-Helper 是否运行、以及“计划做什么”。

### 2. 应用

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\LocalOptimizer.ps1 -Apply
```

- 只执行安全默认项：电源 + WSL + 游戏注册表；
- 备份目录：`%LOCALAPPDATA%\LocalOptimizer\backup-<时间>`；
- 日志：`%LOCALAPPDATA%\LocalOptimizer\optimizer.log`。

### 3. 回滚

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\LocalOptimizer.restore.ps1
```

- 自动选择最新备份恢复；
- 查看备份：`-ListBackups`；
- 指定某个备份：`-ManifestPath <path>`。

### 4. 可选高风险项

```powershell
# 管理员 PowerShell，且你清楚 HAGS 可能对部分驱动/软件不兼容
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\LocalOptimizer.ps1 -Apply -IncludeHags
```

## 为什么这样设计

你要求“别把电脑搞崩”，所以：

1. **默认只读**：不加 `-Apply` 绝对不会改任何东西；
2. **写前备份**：每个被修改的对象都有可恢复副本；
3. **失败可回滚**：`-RollbackOnFail` 会自动用备份清单回滚；
4. **不碰高风险层**：BIOS、驱动、HAGS、G-Helper 内部配置都不动；
5. **不打断运行中的 WSL**：`.wslconfig` 需要 `wsl --shutdown` 才生效，脚本默认只写文件并提醒你，不替你重启。

## 验证记录

- PowerShell 语法解析：OK；
- `-Test` 实际跑过：只输出预检与计划，未写任何系统设置；
- 包校验：随 `nvidia-laptop-tuning` Skill 100/100。
