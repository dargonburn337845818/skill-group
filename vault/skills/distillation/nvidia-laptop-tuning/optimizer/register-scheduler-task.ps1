param(
  [string]$TaskName = 'GHelperSmartScheduler',
  [string]$ScriptPath = (Join-Path $PSScriptRoot 'GHelperSmartScheduler.ps1')
)

$ErrorActionPreference = 'Stop'

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
try {
  $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest
  Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Force | Out-Null
  Write-Output "OK task=$TaskName (RunLevel=Highest)"
} catch {
  Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Force | Out-Null
  Write-Output "OK task=$TaskName (RunLevel=default, Mem Reduct 可能无权限)"
}
Write-Output "script=$ScriptPath"
