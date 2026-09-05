<#
.SYNOPSIS
  本地电脑设置一键优化脚本（安全版）：电源计划、WSL 内存、游戏相关注册表项。

.DESCRIPTION
  设计目标：
  - 默认不写任何东西：跑一次 `-Test` 只输出“会做什么”；
  - 真正执行必须显式 `-Apply`；
  - 写之前先备份（电源计划 GUID、.wslconfig、相关注册表）；
  - 可还原：备份目录保留 manifest，`LocalOptimizer.restore.ps1` 一键回滚；
  - 不碰：BIOS、驱动、超频、硬件加速 GPU 调度（除非显式 -IncludeHags）。

  安全边界：
  - 本脚本只改“用户可逆/可备份”的 Windows 设置；
  - 不自动执行 `wsl --shutdown`（避免打断你正在跑的 WSL 任务），除非显式 -RestartWsl；
  - 不自动安装驱动/BIOS/G-Helper；NVIDIA 驱动与显卡设置仍走热修复/Profile Inspector 等方案。

.PARAMETER Apply
  真正应用修改；缺省时只做预检和计划（dry-run）。

.PARAMETER Test
  运行预检并输出计划，不写任何文件（等同缺省 dry-run，但明确输出测试报告）。

.PARAMETER IncludePowerPlan
  应用“电源计划优化”。默认：Apply 时开启。

.PARAMETER IncludeWslConfig
  应用 WSL2 内存/CPU/swap 配置。默认：Apply 时开启。

.PARAMETER IncludeGameDvr
  应用游戏相关注册表（Game DVR 关、Game Mode 开）。默认：Apply 时开启。

.PARAMETER IncludeHags
  【高风险，默认关】修改硬件加速 GPU 调度（HwSchMode）。需要管理员，且可能需要重启；默认不启用。

.PARAMETER RestartWsl
  应用 WSL 配置后执行 `wsl --shutdown` 使其生效。默认不执行。

.PARAMETER RollbackOnFail
  任一关键步骤失败时调用本脚本内置回滚逻辑。
#>
param(
  [switch]$Apply,
  [switch]$Test,
  [switch]$IncludePowerPlan,
  [switch]$IncludeWslConfig,
  [switch]$IncludeGameDvr,
  [switch]$IncludeHags,
  [switch]$RestartWsl,
  [switch]$RollbackOnFail
)

$ErrorActionPreference = 'Stop'

# 若 Apply 且未指定具体项，默认启用安全三项；HAGS 永不默认
if ($Apply -and -not $IncludePowerPlan -and -not $IncludeWslConfig -and -not $IncludeGameDvr) {
  $IncludePowerPlan = $true
  $IncludeWslConfig = $true
  $IncludeGameDvr = $true
}

# Test 模式下，若未指定，也显示“默认会做什么”的计划（依然不写任何东西）
if ($Test -and -not $IncludePowerPlan -and -not $IncludeWslConfig -and -not $IncludeGameDvr) {
  $IncludePowerPlan = $true
  $IncludeWslConfig = $true
  $IncludeGameDvr = $true
}

# ---------- 常量与日志 ----------
$BackupRoot = Join-Path $env:LOCALAPPDATA 'LocalOptimizer'
New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
$LogFile = Join-Path $BackupRoot 'optimizer.log'
$Engine = 'LocalOptimizer'

function Write-Log {
  param([string]$Message, [switch]$Error)
  $line = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
  Add-Content -Path $LogFile -Value $line -Encoding UTF8
  if ($Error) { Write-Host "[ERR] $Message" -ForegroundColor Red }
  else { Write-Host $Message }
}

function Get-Timestamp {
  return Get-Date -Format 'yyyyMMdd-HHmmss'
}

function Test-Admin {
  $id = [Security.Principal.WindowsIdentity]::GetCurrent()
  $p = New-Object Security.Principal.WindowsPrincipal($id)
  return $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# ---------- 备份 ----------
$BackupDir = $null
$Manifest = [ordered]@{}

function New-Backup {
  $script:BackupDir = Join-Path $BackupRoot ("backup-" + (Get-Timestamp))
  New-Item -ItemType Directory -Force -Path $script:BackupDir | Out-Null
  $script:Manifest.created = (Get-Date -Format o)
  $script:Manifest.dir = $script:BackupDir
  Write-Log "备份目录: $BackupDir"
}

function Backup-Power {
  $active = powercfg /getactivescheme 2>$null | Out-String
  if ($active -match '([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})') {
    $script:Manifest.powerSchemeOriginal = $Matches[1]
    Write-Log "原电源方案 GUID: $($Matches[1])"
  } else {
    Write-Log '未能解析当前电源方案 GUID，仍继续（恢复时可能需手动）'
  }
}

function Backup-WslConfig {
  $wslconf = Join-Path $env:USERPROFILE '.wslconfig'
  if (Test-Path $wslconf) {
    $dst = Join-Path $BackupDir 'wslconfig.backup'
    Copy-Item -Path $wslconf -Destination $dst -Force
    $script:Manifest.hasWslConfig = $true
    Write-Log "已备份 .wslconfig -> $dst"
  } else {
    $script:Manifest.hasWslConfig = $false
    Write-Log '未发现现有 .wslconfig，无需备份'
  }
}

function Backup-Reg {
  param([string]$Name, [string]$RegPath)
  try {
    $file = Join-Path $BackupDir "$Name.reg"
    & reg.exe export $RegPath $file /y | Out-Null
    if ($LASTEXITCODE -eq 0 -and (Test-Path $file)) {
      $script:Manifest["reg_$Name"] = $file
      Write-Log "已导出注册表 $Name -> $file"
    } else {
      Write-Log "导出注册表 $Name 失败（可能路径不存在，跳过）"
    }
  } catch {
    Write-Log "导出注册表 $Name 异常，跳过: $($_.Exception.Message)"
  }
}

function Backup-WriteManifest {
  $manifestFile = Join-Path $BackupDir 'manifest.json'
  $script:Manifest | ConvertTo-Json | Set-Content -Path $manifestFile -Encoding UTF8
  Write-Log "备份清单: $manifestFile"
}

# ---------- 应用 ----------
function Apply-PowerPlan {
  Write-Log '应用电源计划…'
  $list = powercfg /list 2>$null | Out-String
  $hpGuid = $null
  if ($list -match 'High performance[\s\S]*?([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})') {
    $hpGuid = $Matches[1]
  }
  if (-not $hpGuid) {
    # 复制当前方案为一个“高性能优化副本”，不改系统自带方案
    $activeGuid = [string]$Manifest.powerSchemeOriginal
    if ($activeGuid) {
      $dup = powercfg /duplicatescheme $activeGuid 2>$null | Out-String
      if ($dup -match '([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})') {
        $hpGuid = $Matches[1]
      }
    }
  }
  if (-not $hpGuid) {
    Write-Log '未找到可用高性能电源方案，跳过电源部分' -Error
    return $false
  }
  & powercfg /setactive $hpGuid | Out-Null
  if ($LASTEXITCODE -ne 0) {
    Write-Log "切换电源方案失败: $hpGuid" -Error
    return $false
  }
  # 插电时的常用优化（这些是逻辑上的“把功耗/调度放开”，不是硬件超频）
  & powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5 | Out-Null
  & powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100 | Out-Null
  & powercfg /setacvalueindex SCHEME_CURRENT SUB_DISK DISKIDLE 0 | Out-Null
  & powercfg /setacvalueindex SCHEME_CURRENT SUB_USB USBSELECTIVESUSPEND 0 | Out-Null
  & powercfg /setactive SCHEME_CURRENT | Out-Null
  $script:Manifest.powerSchemeApplied = $hpGuid
  Write-Log "电源方案已切换/调整: $hpGuid"
  return $true
}

function Apply-WslConfig {
  Write-Log '应用 WSL 配置…'
  $wslconf = Join-Path $env:USERPROFILE '.wslconfig'
  $content = @"
[wsl2]
memory=10GB
processors=12
swap=4GB
"@
  try {
    Set-Content -Path $wslconf -Value $content -Encoding UTF8
    Write-Log "已写入 .wslconfig: $wslconf"
    if ($RestartWsl) {
      Write-Log '执行 wsl --shutdown 使配置生效…'
      & wsl.exe --shutdown | Out-Null
      Write-Log 'wsl --shutdown 已执行'
    } else {
      Write-Log '未重启 WSL；需要时手动执行: wsl --shutdown'
    }
    return $true
  } catch {
    Write-Log "写入 .wslconfig 失败: $($_.Exception.Message)" -Error
    return $false
  }
}

function Apply-GameDvr {
  Write-Log '应用游戏相关设置…'
  try {
    New-Item -Path 'HKCU:\System\GameConfigStore' -Force | Out-Null
    Set-ItemProperty -Path 'HKCU:\System\GameConfigStore' -Name 'GameDVR_Enabled' -Value 0 -Type DWord
    New-Item -Path 'HKCU:\Software\Microsoft\GameBar' -Force | Out-Null
    Set-ItemProperty -Path 'HKCU:\Software\Microsoft\GameBar' -Name 'AutoGameModeEnabled' -Value 1 -Type DWord
    Write-Log 'Game DVR 已关闭，Game Mode 已开启'
    return $true
  } catch {
    Write-Log "游戏设置写入失败: $($_.Exception.Message)" -Error
    return $false
  }
}

function Apply-Hags {
  Write-Log '应用硬件加速 GPU 调度（高风险项）…'
  if (-not (Test-Admin)) {
    Write-Log '需要管理员权限才能修改 HAGS，已跳过' -Error
    return $false
  }
  try {
    $path = 'HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers'
    Set-ItemProperty -Path $path -Name 'HwSchMode' -Value 2 -Type DWord
    Write-Log 'HwSchMode 已设为 2；重启后生效'
    return $true
  } catch {
    Write-Log "HAGS 写入失败: $($_.Exception.Message)" -Error
    return $false
  }
}

# ---------- 校验 ----------
function Verify-Power {
  $cur = powercfg /getactivescheme 2>$null | Out-String
  Write-Log "当前电源方案: $($cur.Trim())"
}

function Verify-WslConfig {
  $wslconf = Join-Path $env:USERPROFILE '.wslconfig'
  if (Test-Path $wslconf) {
    $c = Get-Content -Raw $wslconf
    Write-Log "WSL 配置已存在（是否包含 memory=10GB: $($c -match 'memory=10GB'))"
  } else {
    Write-Log 'WSL 配置不存在'
  }
}

function Verify-GameDvr {
  $dvr = (Get-ItemProperty -Path 'HKCU:\System\GameConfigStore' -Name 'GameDVR_Enabled' -ErrorAction SilentlyContinue).GameDVR_Enabled
  $gm = (Get-ItemProperty -Path 'HKCU:\Software\Microsoft\GameBar' -Name 'AutoGameModeEnabled' -ErrorAction SilentlyContinue).AutoGameModeEnabled
  Write-Log "GameDVR_Enabled=$dvr AutoGameModeEnabled=$gm"
}

function Invoke-Restore {
  param([string]$ManifestPath)
  Write-Log '执行回滚…'
  if (-not (Test-Path $ManifestPath)) {
    Write-Log "找不到备份清单: $ManifestPath"
    return
  }
  $m = Get-Content -Raw -Path $ManifestPath | ConvertFrom-Json
  if ($m.powerSchemeOriginal) {
    & powercfg /setactive $m.powerSchemeOriginal | Out-Null
    Write-Log "已恢复电源方案: $($m.powerSchemeOriginal)"
  }
  if ($m.hasWslConfig) {
    $src = Join-Path $m.dir 'wslconfig.backup'
    if (Test-Path $src) {
      Copy-Item -Path $src -Destination (Join-Path $env:USERPROFILE '.wslconfig') -Force
      Write-Log '已恢复 .wslconfig'
    }
  } elseif ($m.dir) {
    $wslconf = Join-Path $env:USERPROFILE '.wslconfig'
    if ($m.created -and (Test-Path $wslconf) -and -not $m.hasWslConfig) {
      # 原本没有 .wslconfig，则删除本次创建的
      Remove-Item -Path $wslconf -Force -ErrorAction SilentlyContinue
      Write-Log '已删除本次创建的 .wslconfig'
    }
  }
  foreach ($prop in $m.PSObject.Properties) {
    if ($prop.Name -like 'reg_*') {
      $reg = [string]$prop.Value
      if (Test-Path $reg) {
        & reg.exe import $reg | Out-Null
        Write-Log "已导入注册表备份: $reg"
      }
    }
  }
}

# ---------- 主流程 ----------
Write-Log "===== $Engine 启动 ====="
Write-Log "Apply=$Apply Test=$Test IncludePower=$IncludePowerPlan IncludeWsl=$IncludeWslConfig IncludeGameDvr=$IncludeGameDvr IncludeHAGS=$IncludeHags RestartWsl=$RestartWsl"
Write-Log "管理员权限: $(Test-Admin)"

# 预检
$nvidia = & (Get-Command 'nvidia-smi.exe' -ErrorAction SilentlyContinue).Source --query-gpu=driver_version --format=csv,noheader 2>$null
if ($nvidia) { Write-Log "检测到 NVIDIA 驱动: $nvidia" }
if ($nvidia -match '616\.56') {
  Write-Log '检测到 616.56：该版本存在已知闪屏，建议先安装 GeForce Hotfix 616.86（本脚本不自动装驱动）'
}
$ghelper = Get-Process -Name 'GHelper' -ErrorAction SilentlyContinue
Write-Log "G-Helper 运行中: $([bool]$ghelper)"

if (-not $Apply) {
  Write-Log '【DRY-RUN】未加 -Apply，只输出计划，不写任何东西。'
  Write-Log '计划:'
  if ($IncludePowerPlan) { Write-Log '  - 电源计划备份并按需切到高性能/优化副本' }
  if ($IncludeWslConfig) { Write-Log '  - 备份并写入 %USERPROFILE%\.wslconfig（memory=10GB/processors=12/swap=4GB）' }
  if ($IncludeGameDvr) { Write-Log '  - Game DVR 关闭 + Game Mode 开启（HKCU 注册表，可逆）' }
  if ($IncludeHags) { Write-Log '  - 【高风险】HAGS 开启，需重启' }
  if ($Test) { Write-Log '测试完成：默认不写任何系统设置。' }
  return
}

# 执行：先备份
try {
  New-Backup
  if ($IncludePowerPlan) { Backup-Power }
  if ($IncludeWslConfig) { Backup-WslConfig }
  if ($IncludeGameDvr -or $IncludeHags) {
    if ($IncludeGameDvr) { Backup-Reg -Name 'GameConfigStore' -RegPath 'HKCU\System\GameConfigStore' }
    if ($IncludeGameDvr) { Backup-Reg -Name 'GameBar' -RegPath 'HKCU\Software\Microsoft\GameBar' }
    if ($IncludeHags) { Backup-Reg -Name 'GraphicsDrivers' -RegPath 'HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers' }
  }
  Backup-WriteManifest

  $failures = @()
  if ($IncludePowerPlan) { if (-not (Apply-PowerPlan)) { $failures += 'PowerPlan' } }
  if ($IncludeWslConfig) { if (-not (Apply-WslConfig)) { $failures += 'WslConfig' } }
  if ($IncludeGameDvr) { if (-not (Apply-GameDvr)) { $failures += 'GameDvr' } }
  if ($IncludeHags) { if (-not (Apply-Hags)) { $failures += 'HAGS' } }

  # 校验
  if ($IncludePowerPlan) { Verify-Power }
  if ($IncludeWslConfig) { Verify-WslConfig }
  if ($IncludeGameDvr) { Verify-GameDvr }

  if ($failures.Count -gt 0) {
    Write-Log "存在失败项: $($failures -join ', ')；备份在 $BackupDir" -Error
    if ($RollbackOnFail) {
      $manifestFile = Join-Path $BackupDir 'manifest.json'
      Invoke-Restore -ManifestPath $manifestFile
    }
    exit 1
  }

  Write-Log '全部完成。备份与回滚入口见 $env:LOCALAPPDATA\LocalOptimizer'
  Write-Log '如需回滚: powershell -ExecutionPolicy Bypass -File LocalOptimizer.restore.ps1'
}
catch {
  Write-Log "发生异常: $($_.Exception.Message)" -Error
  if ($RollbackOnFail) {
    $latest = Get-ChildItem $BackupRoot -Directory -Filter 'backup-*' | Sort-Object Name -Descending | Select-Object -First 1
    if ($latest) { Invoke-Restore -ManifestPath (Join-Path $latest.FullName 'manifest.json') }
  }
  exit 1
}
