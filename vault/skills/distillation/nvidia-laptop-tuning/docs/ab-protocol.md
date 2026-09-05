# A/B 验证协议：有/无 G-Helper 智能调度器

> 版本：0.4.0-草案
> 适用范围：ASUS TUF FX608LM（RTX 5060 Laptop 8GB / 16GB 单通道 / Windows 11 / 可选 WSL2）
> 目的：用可复现的“开关对照”，判断 `GHelperSmartScheduler` 对你实际使用是否有可观察收益、无收益或不确定。
> 原则：**只观测，不改系统；每个结论都要有“开/关”两侧的本机数据；未达到样本量/稳定度不下结论。**

---

## 0. 要回答的问题

- 开着智能调度器（A 臂）与关掉它、手动固定在一个 G-Helper 档位（B 臂）相比：
  - 游戏/训练的帧率或耗时是否更好？
  - 温度、功耗、内存占用是否更优？
  - 模式切换是否真的“按需”（需要时高性能、闲时安静）？
- 本协议不回答“调度器内部哪个阈值最好”，那是另一组实验。

---

## 1. 负载选择规则

### 1.1 候选负载

| 类型 | 候选 | 可重复性 | 建议 |
|---|---|---|---|
| 游戏 Benchmark | Cyberpunk 2077 内置 Benchmark / 3DMark Time Spy / Port Royal | 高（内置固定路线） | **首选 3DMark Time Spy**，官方、稳定、单次 3 分钟左右 |
| AI/训练 | 固定 PyTorch 训练脚本（同 model/batch/seed/data），或 Blender 固定渲染帧 | 高（脚本固定） | 若本轮主要验证 AI，用固定 epoch 训练 |
| 日常轻载 | 浏览器 + 文档 + 视频（固定网页/视频） | 中 | 仅作补充，不作主判据 |

### 1.2 最终选择规则

1. 同一轮 A/B 只选 **一种主负载**，不混合游戏与 AI 数据平均。
2. 可重复性排序：内置 Benchmark > 固定脚本 > 手动固定路线。
3. 主负载时长：
   - 游戏/3DMark：至少完整一轮（约 2–4 分钟），采集区间取 **180 秒**；
   - AI 训练：至少 1 个固定 epoch，建议单轮 ≤10 分钟，避免散热/功耗漂移。
4. 记录并固定负载参数：
   - 游戏：分辨率、画质档、DLSS/FSR、场景/地图、帧率上限、是否垂直同步；
   - 3DMark：Preset（Time Spy/Port Royal）、分辨率；
   - AI：模型、batch size、epoch 数、seed、数据集路径、dtype、DataLoader workers。
5. 推荐首轮：**3DMark Time Spy**（最稳定、容易复现）；若你主要做 AI，再跑一组 PyTorch 固定训练。

---

## 2. 变量隔离（只切调度器）

### 2.1 唯一自变量

| 臂 | 调度器状态 | G-Helper 档位 |
|---|---|---|
| A | **开启**（GHelperSmartScheduler 运行） | 由调度器自动切换（Silent/Balanced/Turbo/Custom） |
| B | **关闭**（停止调度器） | 手动固定为 **Balanced**（默认对照；也可按你日常习惯固定为 Turbo，但需在报告写明） |

> B 臂默认手动 Balanced 的原因：这是“没有自动调度”的日常对照。如果你日常其实是常驻 Turbo，则 B 臂应固定 Turbo，并在报告注明。

### 2.2 必须保持不变

- G-Helper 本程序**必须运行**（A/B 两臂都是），否则 A 臂无法切档、B 臂档位也会失效。
- 电源计划、Windows 设置、LocalOptimizer 在本轮期间**不做任何应用/回滚**。
- 笔记本物理条件：插电、同一电源模式、同一散热垫/桌面、同一环境温度区间。
- 后台程序：关闭浏览器、聊天、更新器、杀毒扫描、RGB 控制、下载器等；记录关闭清单。
- 屏幕亮度、声音、外设统一；不要开/关额外程序。
- 若测 AI：WSL 只保留该训练任务，不并行其他 WSL/Python 进程。
- 内存清理属于调度器自带动作，默认随 A 臂一起生效；若想单独评估“切档”而不含清内存，可临时在 config 里设 `memCleanEnabled=false` 另跑一组，但主协议默认是“完整调度器”。

### 2.3 开关命令（Windows 侧）

开启调度器（A 臂）：

```powershell
# 命令行直接跑
powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "D:\<工具目录>\optimizer\GHelperSmartScheduler.ps1"
# 或通过计划任务
schtasks /Run /TN GHelperSmartScheduler
```

关闭调度器（B 臂）：

```powershell
schtasks /End /TN GHelperSmartScheduler
schtasks /Change /TN GHelperSmartScheduler /DISABLE
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'powershell.exe' -and $_.CommandLine -like '*GHelperSmartScheduler.ps1*' -and $_.ProcessId -ne $PID } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
```

确认当前状态（每次样本前后都要跑）：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\<工具目录>\optimizer\status-report.ps1"
```

> 判据：`调度进程数` 为 1 = A 臂；为 0 = B 臂；`当前 G-Helper 档位` 在 B 臂应显示你手动固定的档位。

---

## 3. 交替顺序与随机化

### 3.1 顺序规则

- 每对样本 = 同一批环境下的 1 次 A + 1 次 B。
- 对内顺序随机：用抛硬币或 PowerShell `Get-Random -Minimum 1 -Maximum 3`，且建议采用 **ABBA / BAAB** 交替，抵消时间漂移。
- 样本间冷却：至少 **5 分钟**，或等 GPU 温度回落到“样本开始前 ±5°C”。
- 6 样本示例顺序：`A B B A B A`、`B A A B A B` 等（随机生成后写进报告）。

### 3.2 环境漂移控制

- 尽量同一时间段（如每天同一小时）完成一批；
- 每批记录房间温度、开始/结束时间；
- 若中途温度/背景显著变化，该样本作废重跑。

---

## 4. 指标定义与采集来源

### 4.1 硬件/系统指标（采样间隔：1 秒）

| 指标 | 单位 | 采集命令/来源 | 汇总口径 |
|---|---|---|---|
| GPU 利用率 | % | `nvidia-smi --query-gpu=utilization.gpu,temperature.gpu,power.draw,memory.used,memory.total,clocks.sm --format=csv,noheader,nounits` | 平均 / 峰值 |
| GPU 温度 | °C | 同上（`temperature.gpu`） | 平均 / 峰值 / 超过 88°C 秒数 |
| GPU 功耗 | W | 同上（`power.draw`） | 平均 / 峰值 |
| 显存占用 | MB | 同上（`memory.used`） | 平均 |
| 系统内存 | % | `Get-CimInstance Win32_OperatingSystem`（`TotalVisibleMemorySize` / `FreePhysicalMemory`） | 平均 |
| CPU 负载 | % | `Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average` | 平均 / 峰值 |
| 当前档位/切换 | 次 | `%LOCALAPPDATA%\GHelperSmartScheduler\state.json`（`mode`/`updated`）、`scheduler.log` 中 `已发送热键` | 各档位耗时占比、切换次数 |
| 可选：磁盘可用 | % | `Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3"`（只观测） | 报告附带 |

> exact JSON/CSV 由下一小类的 `ab-measure.ps1` 自动落盘；本协议先固定字段。

### 4.2 性能指标（按负载类型）

| 负载 | 指标 | 来源 | 说明 |
|---|---|---|---|
| 游戏/3DMark | 平均帧率 (avg FPS)、1% low、帧时间 p95 | 内置 Benchmark 报告；或 PresentMon / MSI Afterburner + RTSS / CapFrameX | 优先使用同一个工具的同一口径 |
| AI/训练 | 每 epoch 耗时、samples/s、loss | 训练脚本自身输出 | 固定同样 epoch 数与 seed |
| 可选 | OSD 截图 | G-Helper OSD（`Ctrl+Shift+Alt+O`） | 记录实际档位与温度 |

### 4.3 模式分布（必记）

- 从 `state.json` / `scheduler.log` 统计 A 臂各档位（Silent/Balanced/Turbo/Custom）耗时占比；
- B 臂固定档位占比 = 100%。
- 这是判断“调度器是否真的按需”的关键，不能只看平均帧率。

---

## 5. 样本量

- **最低 3 对**（3 次 A + 3 次 B），**建议 5 对**。
- 每对必须是同一环境/同一时段下完成，不能用跨天数据直接拼。
- 若同臂内 3 次结果的相对标准差 >5%（帧率/温度/功耗任一），视为噪声大，需增加样本或更换负载。
- 报告必须写明 `n=` 与每样本原始数据路径。

---

## 6. 判定规则

### 6.1 噪声定义

- 某指标同臂内 3 次相对标准差（SD/Mean）>5% → 该指标噪声大，不用于下结论。
- 环境温度变化 >3°C、背景进程变化、样本作废 → 该样本不计入。

### 6.2 收益判定（性能方向）

| 结论 | 条件 |
|---|---|
| **有收益** | 主性能指标提升 ≥3%（游戏平均帧率或 1% low；AI epoch 耗时缩短 ≥3%），且温度/功耗无恶化（恶化 ≤5%），且模式分布显示“重负载确实上了高档次、轻负载保持安静” |
| **无收益** | 性能差异 <1%，或差异落在噪声区间内 |
| **不确定** | 性能有提升但温度/功耗明显恶化 >5%；或数据波动大；或样本 <3 对；或 A/B 两臂档位分布几乎一样（说明调度器没实际改变行为） |

### 6.3 额外观察（不直接定胜负）

- 若 A 臂平均帧率略低，但 1% low 更好 / 温度更低 / 更安静，应记为“体验可能更好但峰值性能略降”，单独说明。
- 内存清理收益单独看：记录 A 臂 `last_mem_clean` 与内存均值，不混入“切档收益”。

---

## 7. Windows 侧执行步骤

### 7.1 准备（一次）

1. 打开 G-Helper，确认运行中、热键默认、各档位风扇/功耗配置好。
2. 确定主负载与参数，写进报告。
3. 关闭后台程序，插电，固定环境。
4. 建数据目录：`D:\<工具目录>\ab-data\<日期>\`。

### 7.2 每个样本

1. 记录开始时间、环境温度、后台清单、调度器状态（`status-report.ps1`）。
2. 确认臂：A = 启动调度器；B = 停止调度器并手动切到 Balanced（或你指定的固定档）。
3. 空载等待 **120 秒**（让机器稳定）。
4. 预热 **30 秒**（或使用 Benchmark 自带预热）。
5. 正式采集 **180 秒**（或完整 Benchmark/epoch）。
6. 结束采集，记录 `status-report.ps1` 与性能工具输出。
7. 空载等待 **60 秒**，再冷却至温度回落 ±5°C。
8. 保存原始数据到 `D:\<工具目录>\ab-data\<日期>\arm-X-run-N.*`。

### 7.3 随机顺序示例

```powershell
$arms = @('A','B','A','B','B','A')  # 随机生成，写入报告
```

### 7.4 报告模板

- 每样本：臂、时间、平均帧率/1% low、GPU 温度 avg/max、功耗 avg/max、内存 avg、档位分布、备注。
- 汇总：每臂均值 ± SD；按第 6 节给出“有收益/无收益/不确定”。

---

## 8. 边界与风险

- **不超频、不改 G-Helper 内部配置、不控制磁盘/网络**；只观测。
- 调度器依赖 G-Helper 运行；G-Helper 未启动时 A 臂无效。
- 模拟热键可能被其他程序占用；A 臂样本前确认档位真的变化（看 `state.json`/日志）。
- 16GB 单通道内存是显著硬件瓶颈；本协议测量的是“调度器开关”的影响，不能用来证明“加内存没有用”。
- 散热/环境温度是最大干扰源；必须记录并控制。
- 本协议只提供证据链，不承诺收益；没有足够数据时结论 = 不确定。

---

## 9. 依据文件（本仓库）

- 调度器：`D:\<工具目录>\optimizer\GHelperSmartScheduler.ps1` + `GHelperSmartScheduler.config.json`
- 状态查询：`D:\<工具目录>\optimizer\status-report.ps1`
- 本地优化（本轮不启用）：`D:\<工具目录>\local-optimizer\LocalOptimizer.ps1`
- 调度状态/日志：`%LOCALAPPDATA%\GHelperSmartScheduler\state.json`、`scheduler.log`
- 下一小类将提供自动采集脚本 `optimizer/ab-measure.ps1`，本协议是它的字段与判定契约。
