<#
.SYNOPSIS
  回滚 LocalOptimizer 的一键优化：按最近的备份清单恢复电源方案、.wslconfig 与注册表。

.DESCRIPTION
  使用说明：
  - 不加参数：自动选择最新备份目录并恢复；
  - -ManifestPath：指定某个 manifest.json 恢复；
  - -ListBackups：仅列出可用备份，不恢复。
#>
param(
  [string]$ManifestPath,
  [switch]$ListBackups
)

$ErrorActionPreference = 'Stop'
$BackupRoot = Join-Path $env:LOCALAPPDATA 'LocalOptimizer'
$LogFile = Join-Path $BackupRoot 'restore.log'

function Write-Log {
  param([string]$Message)
  $line = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
  Add-Content -Path $LogFile -Value $line -Encoding UTF8
  Write-Host $line
}

function Invoke-Restore {
  param([string]$Path)
  Write-Log "开始恢复: $Path"
  $m = Get-Content -Raw -Path $Path | ConvertFrom-Json

  if ($m.powerSchemeOriginal) {
    & powercfg /setactive $m.powerSchemeOriginal | Out-Null
    Write-Log "已恢复电源方案: $($m.powerSchemeOriginal)"
  }

  if ($m.hasWslConfig) {
    $src = Join-Path $m.dir 'wslconfig.backup'
    if (Test-Path $src) {
      Copy-Item -Path $src -Destination (Join-Path $env:USERPROFILE '.wslconfig') -Force
      Write-Log '已恢复 .wslconfig'
    } else {
      Write-Log '备份中的 wslconfig.backup 不存在，跳过'
    }
  } elseif (-not $m.hasWslConfig -and $m.created) {
    $wslconf = Join-Path $env:USERPROFILE '.wslconfig'
    if (Test-Path $wslconf) {
      Remove-Item -Path $wslconf -Force -ErrorAction SilentlyContinue
      Write-Log '已删除本次创建的 .wslconfig'
    }
  }

  foreach ($prop in $m.PSObject.Properties) {
    if ($prop.Name -like 'reg_*') {
      $regPath = [string]$prop.Value
      if (Test-Path $regPath) {
        & reg.exe import $regPath | Out-Null
        Write-Log "已导入注册表备份: $regPath"
      }
    }
  }

  Write-Log '恢复完成。'
}

if ($ListBackups) {
  Write-Log '可用备份:'
  Get-ChildItem $BackupRoot -Directory -Filter 'backup-*' | Sort-Object Name -Descending | ForEach-Object {
    $mf = Join-Path $_.FullName 'manifest.json'
    if (Test-Path $mf) {
      $m = Get-Content -Raw -Path $mf | ConvertFrom-Json
      Write-Log "  $($_.Name)  created=$($m.created)"
    } else {
      Write-Log "  $($_.Name)  (无 manifest)"
    }
  }
  return
}

if (-not $ManifestPath) {
  $latest = Get-ChildItem $BackupRoot -Directory -Filter 'backup-*' | Sort-Object Name -Descending | Select-Object -First 1
  if (-not $latest) {
    Write-Log '未找到备份目录。'
    exit 1
  }
  $ManifestPath = Join-Path $latest.FullName 'manifest.json'
}

if (-not (Test-Path $ManifestPath)) {
  Write-Log "manifest 不存在: $ManifestPath"
  exit 1
}

Invoke-Restore -Path $ManifestPath
