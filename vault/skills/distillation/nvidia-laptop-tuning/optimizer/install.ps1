<#
.SYNOPSIS
  安装 G-Helper 智能调度守护到 %LOCALAPPDATA%\GHelperSmartScheduler，并注册 Windows 登录自启任务。

.DESCRIPTION
  把 GHelperSmartScheduler.ps1 和 config 复制到用户本地目录，然后创建计划任务：
  - 任务名：GHelperSmartScheduler
  - 触发：用户登录时
  - 运行：powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File <脚本>
  - 权限：当前用户，无需管理员（如果 schtasks 提示失败，可右键用 PowerShell 管理员运行）。

  执行前请确保：
  1. G-Helper 已安装并设置为开机自启；
  2. G-Helper 的热键保持默认（Ctrl+Shift+Alt+F16..F20）或已按 config 修改。
#>
$ErrorActionPreference = 'Stop'

$SourceDir = $PSScriptRoot
$DestDir = Join-Path $env:LOCALAPPDATA 'GHelperSmartScheduler'
New-Item -ItemType Directory -Force -Path $DestDir | Out-Null

Copy-Item -Path (Join-Path $SourceDir 'GHelperSmartScheduler.ps1') -Destination $DestDir -Force
Copy-Item -Path (Join-Path $SourceDir 'GHelperSmartScheduler.config.json') -Destination $DestDir -Force

$ScriptPath = Join-Path $DestDir 'GHelperSmartScheduler.ps1'
$TaskName = 'GHelperSmartScheduler'
$Action = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`""

Write-Host "复制到: $DestDir"
Write-Host "创建计划任务: $TaskName"
$schtasksExe = "$env:SystemRoot\System32\schtasks.exe"
& $schtasksExe /Create /F /TN $TaskName /TR $Action /SC ONLOGON /RL LIMITED
if ($LASTEXITCODE -ne 0) {
  Write-Warning 'schtasks 创建失败。可能需要以管理员身份运行本脚本，或手动创建计划任务。'
  exit 1
}

Write-Host ''
Write-Host '安装完成。'
Write-Host '建议先用 DryRun 观察一轮：'
Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`" -DryRun -IntervalSeconds 5"
Write-Host '确认无误后再通过“任务计划程序”启动正式任务。'
Write-Host ''
Write-Host '如需立即启动正式任务：'
Write-Host "  schtasks /Run /TN $TaskName"
