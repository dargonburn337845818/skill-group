<#
.SYNOPSIS
  卸载 G-Helper 智能调度守护：删除登录自启任务，可选保留日志。

.PARAMETER RemoveData
  同时删除 %LOCALAPPDATA%\GHelperSmartScheduler（日志/状态/配置）。
#>
param(
  [switch]$RemoveData
)

$TaskName = 'GHelperSmartScheduler'
$DestDir = Join-Path $env:LOCALAPPDATA 'GHelperSmartScheduler'
$schtasksExe = "$env:SystemRoot\System32\schtasks.exe"

Write-Host "删除计划任务: $TaskName"
& $schtasksExe /Delete /F /TN $TaskName
if ($LASTEXITCODE -ne 0) {
  Write-Warning '计划任务删除失败或任务不存在。'
}

if ($RemoveData) {
  if (Test-Path $DestDir) {
    Write-Host "删除目录: $DestDir"
    Remove-Item -Path $DestDir -Recurse -Force
  }
} else {
  Write-Host "保留数据目录: $DestDir"
}

Write-Host '完成。'
