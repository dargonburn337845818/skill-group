<#
.SYNOPSIS
  为 G-Helper 应用保守风扇曲线预设（可备份/回滚）。默认只预览，加 -Apply 才写入。

.DESCRIPTION
  - 读取 %APPDATA%\GHelper\config.json
  - 备份到 config.json.bak-<时间>
  - 写入 fan_profile_cpu_0/1、fan_profile_gpu_0/1（保守手绘/散热曲线）
  - 默认不动功耗限制（单位语义未知，避免整坏）；-IncludePowerLimits 可显式开启
  - 默认写后重启 G-Helper 生效；-NoRestart 可跳过
  - 回滚：用备份文件替换回 config.json 并重启 G-Helper
#>
param(
  [switch]$Apply,
  [switch]$IncludePowerLimits,
  [switch]$NoRestart
)
$ErrorActionPreference = 'Stop'
$configPath = Join-Path $env:APPDATA 'GHelper\config.json'
if (-not (Test-Path $configPath)) { Write-Error "找不到 G-Helper 配置: $configPath"; exit 1 }

# ---------- 保守预设（单位：温度°C / 风扇%） ----------
# 档案0：安静/均衡（对应 Silent/Balanced 常用）
$cpu0 = @(30,50,60,69,75,80,90,100)
$cpu0f = @(0,3,6,10,18,35,55,80)
$gpu0 = @(30,50,60,69,75,80,90,100)
$gpu0f = @(0,2,5,10,18,40,65,100)
# 档案1：性能/散热（对应 Turbo 常用）
$cpu1 = @(30,40,58,64,72,80,90,100)
$cpu1f = @(0,10,20,35,60,80,92,100)
$gpu1 = @(30,40,58,64,72,80,90,100)
$gpu1f = @(0,12,22,40,70,90,100,100)

function To-HexCurve($temps, $speeds) {
  $bytes = @()
  for ($i=0; $i -lt 8; $i++) { $bytes += [byte]$temps[$i] }
  for ($i=0; $i -lt 8; $i++) { $bytes += [byte]$speeds[$i] }
  return ([BitConverter]::ToString([byte[]]$bytes)).Replace('-','-')
}

# 预览
if (-not $Apply) {
  Write-Host '[PLAN] G-Helper 保守风扇预设'
  Write-Host ('  配置路径: {0}' -f $configPath)
  Write-Host '  档案0 (安静/均衡) CPU/GPU 风扇曲线：'
  Write-Host ('    CPU: {0} -> {1}' -f ($cpu0 -join ','), ($cpu0f -join ','))
  Write-Host ('    GPU: {0} -> {1}' -f ($gpu0 -join ','), ($gpu0f -join ','))
  Write-Host '  档案1 (性能/散热) CPU/GPU 风扇曲线：'
  Write-Host ('    CPU: {0} -> {1}' -f ($cpu1 -join ','), ($cpu1f -join ','))
  Write-Host ('    GPU: {0} -> {1}' -f ($gpu1 -join ','), ($gpu1f -join ','))
  Write-Host '  功耗限制: 默认不修改（-IncludePowerLimits 才启用）'
  Write-Host '  重启 G-Helper: 默认会重启（-NoRestart 跳过）'
  Write-Host '  要真正应用请运行: powershell ... ghelper-apply-presets.ps1 -Apply'
  exit 0
}

# ---------- 备份 ----------
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backup = "$configPath.bak-$stamp"
Copy-Item -Path $configPath -Destination $backup -Force
Write-Host "[OK] 已备份: $backup"

# ---------- 读取并写入 ----------
try {
  $cfg = Get-Content -Raw -Path $configPath | ConvertFrom-Json
  $cfg.fan_profile_cpu_0 = To-HexCurve $cpu0 $cpu0f
  $cfg.fan_profile_gpu_0 = To-HexCurve $gpu0 $gpu0f
  $cfg.fan_profile_cpu_1 = To-HexCurve $cpu1 $cpu1f
  $cfg.fan_profile_gpu_1 = To-HexCurve $gpu1 $gpu1f
  if ($IncludePowerLimits) {
    # 保守：保持与当前一致（80），如果确认单位后可再改
    foreach ($k in @('limit_total_0','limit_slow_0','limit_fast_0','limit_cpu_0','limit_total_1','limit_slow_1','limit_fast_1','limit_cpu_1')) {
      if ($cfg.PSObject.Properties[$k]) { $cfg.$k = [int]$cfg.$k }
    }
    Write-Host '[INFO] 功耗限制保持当前值（未改数值）'
  }
  $cfg | ConvertTo-Json -Depth 10 | Set-Content -Path $configPath -Encoding UTF8
  Write-Host '[OK] 已写入风扇预设'
} catch {
  Write-Host "[ERR] 写入失败，尝试恢复备份: $backup" -ForegroundColor Red
  Copy-Item -Path $backup -Destination $configPath -Force
  throw
}

# ---------- 重启 G-Helper ----------
if (-not $NoRestart) {
  Get-Process GHelper -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Start-Sleep -Milliseconds 800
  $gh = 'D:\<GHelper.exe>'
  if (Test-Path $gh) { Start-Process $gh; Write-Host '[OK] G-Helper 已重启' }
  else { Write-Host '[WARN] 未找到 D:\<GHelper.exe>，请手动启动 G-Helper' }
} else {
  Write-Host '[OK] 已写入但未重启；重启 G-Helper 后生效'
}
Write-Host '[DONE] 回滚方法: 将备份文件复制回 config.json 并重启 G-Helper'
