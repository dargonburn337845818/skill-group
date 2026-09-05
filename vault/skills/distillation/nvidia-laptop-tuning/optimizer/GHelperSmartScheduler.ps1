<#
.SYNOPSIS
  G-Helper 轻量智能调度守护：根据 GPU/CPU 负载、温度、重负载进程自动切换 G-Helper 性能档。

.DESCRIPTION
  设计目标：
  - 日常不“起飞”：默认 Silent/Balanced，只有重负载或高温才切到 Turbo/Custom；
  - 不做超频：只切换 G-Helper 的 BIOS 性能档（风扇/功耗/温度策略由你在 G-Helper 配置好）；
  - 轻量：纯 PowerShell，无第三方依赖，单文件运行；
  - 可验证：支持 -DryRun，只写日志不发热键，便于先观察再启用。

  前提：
  - G-Helper 必须正在运行（本项目通过模拟 G-Helper 全局热键切档）；
  - G-Helper 热键保持默认（Ctrl+Shift+Alt+F16..F20），或修改 config 后保持一致；
  - 每个档位（Silent/Balanced/Turbo/Custom1/2）的风扇曲线和功耗请在 G-Helper 里预先设置好。

.PARAMETER ConfigPath
  JSON 配置文件路径，默认与脚本同目录下的 GHelperSmartScheduler.config.json。

.PARAMETER DryRun
  只计算并记录“应该切到什么档”，不真正发送热键。

.PARAMETER IntervalSeconds
  轮询间隔（秒），默认读配置文件，未读到时用 5。
#>
param(
  [string]$ConfigPath = (Join-Path $PSScriptRoot 'GHelperSmartScheduler.config.json'),
  [switch]$DryRun,
  [int]$IntervalSeconds = -1
)

$ErrorActionPreference = 'Stop'

# ---------- 日志 ----------
$LogDir = Join-Path $env:LOCALAPPDATA 'GHelperSmartScheduler'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir 'scheduler.log'
$StateFile = Join-Path $LogDir 'state.json'

function Write-Log {
  param([string]$Message)
  $line = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
  Add-Content -Path $LogFile -Value $line -Encoding UTF8
  Write-Host $line
}

# ---------- 配置 ----------
if (-not (Test-Path $ConfigPath)) {
  Write-Log "配置文件不存在: $ConfigPath"
  exit 1
}
$cfg = Get-Content -Raw -Path $ConfigPath | ConvertFrom-Json
if ($IntervalSeconds -le 0) { $IntervalSeconds = [int]$cfg.intervalSeconds }
if ($IntervalSeconds -le 0) { $IntervalSeconds = 5 }

function Get-HotkeyVk {
  param([string]$Key)
  switch ($Key.ToUpperInvariant()) {
    'F16' { return 0x7F }
    'F17' { return 0x80 }
    'F18' { return 0x81 }
    'F19' { return 0x82 }
    'F20' { return 0x83 }
    default {
      Write-Log "不支持的 G-Helper 热键: $Key（仅支持 F16-F20）"
      return $null
    }
  }
}

# ---------- 底层：模拟 Ctrl+Shift+Alt+F16..F20 ----------
if (-not ('NativeKey' -as [type])) {
  Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class NativeKey {
  [DllImport("user32.dll")]
  public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
  public const uint KEYEVENTF_KEYUP = 0x0002;
  public const byte VK_CONTROL = 0x11;
  public const byte VK_SHIFT = 0x10;
  public const byte VK_MENU = 0x12;
  public static void PressCombo(byte vk) {
    keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
    keybd_event(VK_SHIFT,   0, 0, UIntPtr.Zero);
    keybd_event(VK_MENU,    0, 0, UIntPtr.Zero);
    keybd_event(vk,         0, 0, UIntPtr.Zero);
    keybd_event(vk,         0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    keybd_event(VK_MENU,    0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    keybd_event(VK_SHIFT,   0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
  }
}
"@
}

function Send-GHelperHotkey {
  param([string]$Mode)
  $key = $cfg.hotkeys.$Mode
  if (-not $key) {
    Write-Log "配置中没有模式 $Mode 的热键"
    return
  }
  $vk = Get-HotkeyVk $key
  if ($null -eq $vk) { return }
  $ghelper = Get-Process -Name 'GHelper' -ErrorAction SilentlyContinue
  if (-not $ghelper) {
    Write-Log 'G-Helper 未运行，无法发送热键（请让 G-Helper 开机自启）'
    return
  }
  if ($DryRun) {
    Write-Log "[DRY-RUN] 要切换到 $Mode (热键 $key)"
    return
  }
  # 双击可能更稳：有些全局热键需要焦点窗口事件循环
  [NativeKey]::PressCombo([byte]$vk)
  Start-Sleep -Milliseconds 100
  [NativeKey]::PressCombo([byte]$vk)
  Write-Log "已发送热键: $Mode ($key)"
}

# ---------- 指标采集 ----------
function Get-NvidiaSmiPath {
  $cmd = Get-Command 'nvidia-smi.exe' -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }
  $fallback = 'C:\Windows\System32\nvidia-smi.exe'
  if (Test-Path $fallback) { return $fallback }
  Write-Log '未找到 nvidia-smi.exe'
  return $null
}

function Get-GpuMetrics {
  $smi = Get-NvidiaSmiPath
  if (-not $smi) { return $null }
  $raw = & $smi --query-gpu=utilization.gpu,temperature.gpu,power.draw,memory.used,clocks.sm --format=csv,noheader,nounits 2>$null
  if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($raw)) {
    Write-Log 'nvidia-smi 查询失败'
    return $null
  }
  $parts = ($raw -split ',') | ForEach-Object { $_.Trim() }
  if ($parts.Count -lt 5) { return $null }
  try {
    return [pscustomobject]@{
      GpuUtil = [double]$parts[0]
      Temp    = [double]$parts[1]
      Power   = [double]$parts[2]
      MemUsed = [double]$parts[3]
      ClockSM = [double]$parts[4]
    }
  } catch {
    Write-Log "解析 nvidia-smi 输出失败: $raw"
    return $null
  }
}

function Get-CpuLoad {
  $cpu = Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue
  if (-not $cpu) { return 0 }
  $avg = ($cpu | Measure-Object -Property LoadPercentage -Average).Average
  if ($null -eq $avg) { return 0 }
  return [double]$avg
}

function Get-MemoryUsage {
  $os = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
  if (-not $os -or -not $os.TotalVisibleMemorySize) { return 0 }
  $total = [double]$os.TotalVisibleMemorySize
  $free = [double]$os.FreePhysicalMemory
  $used = $total - $free
  $percent = ($used / $total) * 100
  return [math]::Round($percent, 1)
}

function Get-MemReductExe {
  $cfgPath = [string]$cfg.memReductExe
  if ($cfgPath -and (Test-Path $cfgPath)) { return $cfgPath }
  $candidate = 'D:\<内存工具目录>\Mem Reduct\memreduct.exe'
  if (Test-Path $candidate) { return $candidate }
  return $null
}

function Test-Admin {
  $id = [Security.Principal.WindowsIdentity]::GetCurrent()
  $pr = New-Object Security.Principal.WindowsPrincipal($id)
  return $pr.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Invoke-MemReduct {
  param([string]$Reason)
  if (-not [bool]$cfg.memCleanEnabled) { return }
  if ($DryRun) {
    Write-Log "[DRY-RUN] 内存调度: 将调用 Mem Reduct 清理（原因: $Reason）"
    return
  }
  $exe = Get-MemReductExe
  if (-not $exe) {
    Write-Log "内存调度: 未找到 Mem Reduct（$exe），跳过"
    return
  }
  if (-not (Test-Admin)) {
    Write-Log "内存调度: 当前非管理员，无法调用 Mem Reduct（需管理员）。请用管理员方式运行调度器。"
    return
  }
  try {
    Write-Log "内存调度: 正在调用 Mem Reduct /clean:0x67（原因: $Reason）"
    $proc = Start-Process -FilePath $exe -ArgumentList '/clean:0x67' -WindowStyle Hidden -PassThru -Wait
    Write-Log "内存调度: Mem Reduct 已执行，退出码 $($proc.ExitCode)"
    $script:lastMemCleanTime = Get-Date
  } catch {
    Write-Log "内存调度: 调用失败: $($_.Exception.Message)"
  }
}

function Test-HeavyProcess {
  foreach ($name in @($cfg.heavyProcesses)) {
    if (Get-Process -Name $name -ErrorAction SilentlyContinue) {
      return $true
    }
  }
  return $false
}

# ---------- 决策 ----------
function Get-DesiredMode {
  param(
    $Metrics,
    [double]$CpuLoad,
    [bool]$HeavyProcess
  )
  $thermalMode = [string]$cfg.thermalMode
  $heavyMode = [string]$cfg.heavyMode
  $balancedMode = [string]$cfg.balancedMode
  $idleMode = [string]$cfg.idleMode

  if ($Metrics) {
    if ($Metrics.Temp -ge [double]$cfg.turboTemp) {
      return $thermalMode
    }
    if ($HeavyProcess -or
        $Metrics.GpuUtil -ge [double]$cfg.heavyGpuUtil -or
        ($Metrics.GpuUtil -ge [double]$cfg.moderateGpuUtil -and $CpuLoad -ge [double]$cfg.highCpuLoad)) {
      return $heavyMode
    }
    if ($Metrics.GpuUtil -le [double]$cfg.idleGpuUtil -and
        $CpuLoad -le [double]$cfg.idleCpuLoad -and
        $Metrics.Temp -le [double]$cfg.idleTemp) {
      return $idleMode
    }
  } else {
    # nvidia-smi 不可用时，仍用进程/CPU 判断，至少不失控
    if ($HeavyProcess -or $CpuLoad -ge [double]$cfg.highCpuLoad) { return $heavyMode }
    if ($CpuLoad -le [double]$cfg.idleCpuLoad) { return $idleMode }
  }
  return $balancedMode
}

# ---------- 状态机（防抖动） ----------
$currentMode = $null
$lastMemCleanTime = Get-Date
$heavyCounter = 0
$idleCounter = 0
$lastSwitchTime = Get-Date

function Test-SwitchAllowed {
  param([string]$Desired)
  if ($Desired -eq $currentMode) { return $false }
  if ($null -eq $currentMode) { return $true }
  $elapsed = ((Get-Date) - $lastSwitchTime).TotalSeconds
  if ($elapsed -lt [double]$cfg.minSwitchIntervalSeconds) {
    return $false
  }
  return $true
}

Write-Log "===== G-Helper 智能调度启动 ====="
Write-Log "DryRun=$DryRun Interval=${IntervalSeconds}s Config=$ConfigPath"

# 读取上次状态，避免冷启动立即乱切
if (Test-Path $StateFile) {
  try {
    $prev = Get-Content -Raw -Path $StateFile | ConvertFrom-Json
    if ($prev.mode) {
      $currentMode = [string]$prev.mode
      Write-Log "恢复上次模式: $currentMode"
    }
  } catch {
    Write-Log "状态文件读取失败，冷启动为未知模式"
  }
}

while ($true) {
  $metrics = Get-GpuMetrics
  $cpuLoad = Get-CpuLoad
  $memPercent = Get-MemoryUsage
  $heavy = Test-HeavyProcess
  $desired = Get-DesiredMode -Metrics $metrics -CpuLoad $cpuLoad -HeavyProcess $heavy

  # 计数：只有持续满足才切
  $heavySustain = [int]$cfg.heavySustainSeconds
  $idleSustain = [int]$cfg.idleSustainSeconds
  if ($desired -eq [string]$cfg.heavyMode) {
    $heavyCounter += $IntervalSeconds
    $idleCounter = 0
  } elseif ($desired -eq [string]$cfg.idleMode) {
    $idleCounter += $IntervalSeconds
    $heavyCounter = 0
  } else {
    $heavyCounter = 0
    $idleCounter = 0
  }

  $summary = "gpu={0}% temp={1}C power={2}W cpu={3}% mem={4}% heavy={5} desired={6}" -f `
    ($(if ($metrics) { $metrics.GpuUtil } else { '?' })), `
    ($(if ($metrics) { $metrics.Temp } else { '?' })), `
    ($(if ($metrics) { $metrics.Power } else { '?' })), `
    ([math]::Round($cpuLoad,1)), $memPercent, $heavy, $desired
  Write-Log $summary

  # ---------- 内存调度（Mem Reduct） ----------
  if ([bool]$cfg.memCleanEnabled) {
    $memCooldown = [double]$cfg.memCleanCooldownSeconds
    $elapsedMem = ((Get-Date) - $lastMemCleanTime).TotalSeconds
    $needClean = $memPercent -ge [double]$cfg.memCleanThresholdPercent
    $needPreClean = [bool]$cfg.memCleanBeforeHeavy -and $desired -eq [string]$cfg.heavyMode -and $memPercent -ge [double]$cfg.memCleanBeforeHeavyThresholdPercent
    $cooldownOk = ($lastMemCleanTime -eq $null) -or ($elapsedMem -ge $memCooldown)
    if (($needClean -or $needPreClean) -and $cooldownOk) {
      if ($needClean) {
        Invoke-MemReduct -Reason "内存占用 ${memPercent}% ≥ ${($cfg.memCleanThresholdPercent)}%"
      } else {
        Invoke-MemReduct -Reason "即将进入重负载，先释放内存（当前 ${memPercent}%）"
      }
    }
  }

  $sustained = ($desired -eq [string]$cfg.heavyMode -and $heavyCounter -ge $heavySustain) -or
               ($desired -eq [string]$cfg.idleMode -and $idleCounter -ge $idleSustain) -or
               ($desired -ne [string]$cfg.heavyMode -and $desired -ne [string]$cfg.idleMode)

  if ($sustained -and (Test-SwitchAllowed -Desired $desired)) {
    Send-GHelperHotkey -Mode $desired
    $currentMode = $desired
    $lastSwitchTime = Get-Date
    $state = [pscustomobject]@{
      updated = (Get-Date -Format o)
      mode = $currentMode
      gpu_util = $(if ($metrics) { $metrics.GpuUtil } else { $null })
      gpu_temp = $(if ($metrics) { $metrics.Temp } else { $null })
      cpu_load = [math]::Round($cpuLoad,1)
      mem_percent = $memPercent
      last_mem_clean = $(if ($lastMemCleanTime) { $lastMemCleanTime.ToString('yyyy-MM-dd HH:mm:ss') } else { $null })
      heavy_process = $heavy
    }
    $state | ConvertTo-Json | Set-Content -Path $StateFile -Encoding UTF8
  }

  Start-Sleep -Seconds $IntervalSeconds
}
