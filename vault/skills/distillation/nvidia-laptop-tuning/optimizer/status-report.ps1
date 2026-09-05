param()

$ErrorActionPreference = 'SilentlyContinue'

# 调度器状态文件
$stateFile = Join-Path $env:LOCALAPPDATA 'GHelperSmartScheduler\state.json'
$mode = '未知'
$stateTime = '未知'
if (Test-Path $stateFile) {
  try {
    $st = Get-Content -Raw -Path $stateFile | ConvertFrom-Json
    if ($st.mode) { $mode = [string]$st.mode }
    if ($st.updated) { $stateTime = [string]$st.updated }
  } catch {}
}
Write-Host ''
Write-Host '============== 当前调度状态 =============='
Write-Host ("当前 G-Helper 档位 : {0}" -f $mode)
Write-Host ("状态更新时间        : {0}" -f $stateTime)
$lastClean = '从未'
if (Test-Path $stateFile) {
  try {
    $st2 = Get-Content -Raw -Path $stateFile | ConvertFrom-Json
    if ($st2.last_mem_clean) { $lastClean = [string]$st2.last_mem_clean }
  } catch {}
}
Write-Host ("上次内存清理        : {0}" -f $lastClean)
Write-Host ('—' * 44)

# GPU 实时指标
$smi = Get-Command 'nvidia-smi.exe' -ErrorAction SilentlyContinue
if ($smi) {
  $raw = & $smi.Source --query-gpu=utilization.gpu,temperature.gpu,power.draw,memory.used,memory.total --format=csv,noheader,nounits 2>$null
  if ($raw) {
    $parts = ($raw -split ',') | ForEach-Object { $_.Trim() }
    Write-Host ('GPU 利用率          : {0}%' -f $parts[0])
    Write-Host ('GPU 温度            : {0} C' -f $parts[1])
    Write-Host ('GPU 功耗            : {0} W' -f $parts[2])
    Write-Host ('显存占用            : {0} MB' -f $parts[3])
    Write-Host ('显存总量            : {0} MB' -f $parts[4])
  } else {
    Write-Host 'GPU 指标读取失败'
  }
} else {
  Write-Host '未找到 nvidia-smi.exe'
}

# CPU 负载
$cpuAll = Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue
if ($cpuAll) {
  $cpuAvg = ($cpuAll | Measure-Object -Property LoadPercentage -Average).Average
  if ($null -ne $cpuAvg) { Write-Host ('CPU 负载            : {0}%' -f [math]::Round($cpuAvg, 1)) }
}

# 内存占用（Windows 整机）
$os = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
if ($os -and $os.TotalVisibleMemorySize) {
  $totalMem = [double]$os.TotalVisibleMemorySize / 1MB
  $freeMem = [double]$os.FreePhysicalMemory / 1MB
  $usedMem = $totalMem - $freeMem
  $memPct = [math]::Round(($usedMem / $totalMem) * 100, 1)
  Write-Host ('内存占用            : {0}% ({1:N1} GB / {2:N1} GB)' -f $memPct, $usedMem, $totalMem)
} else {
  Write-Host '内存占用            : 读取失败'
}

# 磁盘可用（系统盘）
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Where-Object { $_.DeviceID -eq 'C:' } | Select-Object -First 1
if ($disk) {
  $freePct = [math]::Round(($disk.FreeSpace / $disk.Size) * 100, 1)
  $freeGB = [math]::Round($disk.FreeSpace / 1GB, 1)
  Write-Host ('磁盘可用            : {0}% ({1:N1} GB 可用)' -f $freePct, $freeGB)
} else {
  Write-Host '磁盘可用            : 读取失败'
}

# 调度进程# 调度进程
$self = $PID
$procs = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'powershell.exe' -and $_.CommandLine -match '-File.*GHelperSmartScheduler\.ps1' -and $_.ProcessId -ne $self }
Write-Host ('调度进程数          : {0}' -f @($procs).Count)
if ($procs) {
  $procs | ForEach-Object { Write-Host ("   PID: {0}" -f $_.ProcessId) }
}
Write-Host '=========================================='
