<#
.SYNOPSIS
  A/B 测量脚本：记录 GPU/CPU/内存/温度/功耗等指标，只观测，不做任何优化动作。

.DESCRIPTION
  配套 ab-protocol.md 使用。支持：
  - -Arm baseline/tuned（baseline=无调度器，tuned=有调度器）
  - -Duration 采集时长（秒）
  - -Interval 采样间隔（秒，默认 1）
  - -OutputDir 输出目录
  - -DryRun 只打印计划，不采集、不创建目录

  本脚本不会：切换 G-Helper 档位、调用 Mem Reduct、写注册表、修改系统设置。
#>
param(
  [ValidateSet('baseline','tuned')]
  [string]$Arm = 'baseline',
  [int]$Duration = 180,
  [int]$Interval = 1,
  [string]$OutputDir = 'D:\<工具目录>\ab-data',
  [switch]$DryRun
)

$ErrorActionPreference = 'Continue'
$PowerShellExe = (Get-Process -Id $PID).Path

# ---------- DryRun：只打印计划 ----------
if ($DryRun) {
  $samples = [math]::Ceiling($Duration / [math]::Max(1, $Interval))
  Write-Host '[DRY-RUN] A/B 测量计划'
  Write-Host ('  Arm              : {0}' -f $Arm)
  Write-Host ('  Duration         : {0} 秒' -f $Duration)
  Write-Host ('  Interval         : {0} 秒' -f $Interval)
  Write-Host ('  预计采样点       : {0}' -f $samples)
  Write-Host ('  OutputDir        : {0}' -f $OutputDir)
  Write-Host ('  将采集字段       : timestamp, arm, gpu_util, gpu_temp_c, gpu_power_w, vram_used_mb, cpu_load, mem_pct, mem_used_gb, mem_total_gb, clock_sm_mhz')
  Write-Host ('  系统状态         : 只读 nvidia-smi / WMI / state.json / status-report；不切换档位、不清理内存、不改注册表')
  Write-Host '  [DRY-RUN] 完成，未采集任何数据，未创建目录。'
  exit 0
}

# ---------- 目录与文件 ----------
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$armCode = if ($Arm -eq 'tuned') { 'A' } else { 'B' }
if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null }
$csvPath = Join-Path $OutputDir ("ab-{0}-{1}.csv" -f $armCode, $stamp)
$metaPath = Join-Path $OutputDir ("ab-{0}-{1}.meta.json" -f $armCode, $stamp)
$statusPath = Join-Path $OutputDir ("ab-{0}-{1}.status.txt" -f $armCode, $stamp)
$statePath = Join-Path $env:LOCALAPPDATA 'GHelperSmartScheduler\state.json'

# ---------- CSV 头 ----------
$header = 'timestamp,arm,gpu_util,gpu_temp_c,gpu_power_w,vram_used_mb,cpu_load,mem_pct,mem_used_gb,mem_total_gb,clock_sm_mhz'
Set-Content -Path $csvPath -Value $header -Encoding UTF8

# ---------- 状态快照（开头） ----------
function Write-StatusSnapshot([string]$path) {
  try {
    $sr = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\<工具目录>\optimizer\status-report.ps1' 2>&1 | Out-String
    Set-Content -Path $path -Value $sr -Encoding UTF8
  } catch {
    Set-Content -Path $path -Value ('status-report 调用失败: ' + $_.Exception.Message) -Encoding UTF8
  }
}
Write-StatusSnapshot $statusPath

# ---------- 元数据 ----------
$meta = [ordered]@{
  script       = 'ab-measure.ps1'
  arm          = $Arm
  armCode      = $armCode
  started      = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
  durationSec  = $Duration
  intervalSec  = $Interval
  outputDir    = $OutputDir
  csv          = $csvPath
  statusReport = $statusPath
  schedulerState = $null
  note         = '只观测；不切换 G-Helper、不清理内存、不改注册表'
}

# 读取调度器 state.json（只读）
if (Test-Path $statePath) {
  try {
    $st = Get-Content -Raw -Path $statePath | ConvertFrom-Json
    $meta.schedulerState = [ordered]@{
      mode = $st.mode
      updated = $st.updated
      last_mem_clean = $st.last_mem_clean
    }
  } catch { }
}

# ---------- 采集循环 ----------
$startTime = Get-Date
$deadline = $startTime.AddSeconds($Duration)
$sampleNo = 0
while ((Get-Date) -lt $deadline) {
  $sampleNo++
  $now = Get-Date
  $ts = $now.ToString('yyyy-MM-dd HH:mm:ss.fff')

  # GPU（nvidia-smi）
  $gpuUtil = ''; $gpuTemp = ''; $gpuPower = ''; $vramUsed = ''; $clockSm = ''
  $smi = Get-Command 'nvidia-smi.exe' -ErrorAction SilentlyContinue
  if ($smi) {
    $raw = & $smi.Source --query-gpu=utilization.gpu,temperature.gpu,power.draw,memory.used,memory.total,clocks.sm --format=csv,noheader,nounits 2>$null
    if ($LASTEXITCODE -eq 0 -and $raw) {
      $parts = ($raw -split ',') | ForEach-Object { $_.Trim() }
      if ($parts.Count -ge 6) {
        $gpuUtil  = $parts[0]; $gpuTemp = $parts[1]; $gpuPower = $parts[2]
        $vramUsed = $parts[3]; $clockSm = $parts[5]
      }
    }
  }

  # CPU（WMI）
  $cpuLoad = ''
  try {
    $cpu = Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue | Measure-Object -Property LoadPercentage -Average
    if ($cpu -and $null -ne $cpu.Average) { $cpuLoad = [math]::Round([double]$cpu.Average, 1) }
  } catch { }

  # 内存（WMI）
  $memPct = ''; $memUsedGb = ''; $memTotalGb = ''
  try {
    $os = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
    if ($os -and $os.TotalVisibleMemorySize) {
      $totalKb = [double]$os.TotalVisibleMemorySize
      $freeKb = [double]$os.FreePhysicalMemory
      $usedKb = $totalKb - $freeKb
      $memPct = [math]::Round(($usedKb / $totalKb) * 100, 1)
      $memUsedGb = [math]::Round($usedKb / 1MB, 2)
      $memTotalGb = [math]::Round($totalKb / 1MB, 2)
    }
  } catch { }

  # 追加一行 CSV
  $line = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}' -f $ts, $armCode, $gpuUtil, $gpuTemp, $gpuPower, $vramUsed, $cpuLoad, $memPct, $memUsedGb, $memTotalGb, $clockSm
  Add-Content -Path $csvPath -Value $line -Encoding UTF8

  if ($sampleNo -eq 1 -or ($sampleNo % 10) -eq 0) {
    Write-Host ("[{0}] samples={1} cpu={2}% mem={3}% gpuTemp={4}C" -f $ts, $sampleNo, $cpuLoad, $memPct, $gpuTemp)
  }

  # 等下一个间隔（最后一轮不必等）
  if ((Get-Date) -lt $deadline) { Start-Sleep -Seconds $Interval }
}

# ---------- 结束快照与元数据 ----------
$statusEndPath = Join-Path $OutputDir ("ab-{0}-{1}.status-end.txt" -f $armCode, $stamp)
Write-StatusSnapshot $statusEndPath
$meta.finished = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
$meta.samples = $sampleNo
$meta.statusReportEnd = $statusEndPath
$meta | ConvertTo-Json -Depth 4 | Set-Content -Path $metaPath -Encoding UTF8

Write-Host ''
Write-Host "[OK] 测量完成: $csvPath"
Write-Host "[OK] 元数据: $metaPath"
