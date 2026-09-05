# 英伟达笔记本调优共识（完整版）

> 适用：Windows 11 笔记本 + NVIDIA GeForce（尤其 RTX 50 系、Hybrid/Optimus） + 可选 WSL2 CUDA。
> 本文遵守 `distillation-consensus`：每条规则都有触发条件、动作、反例/边界与来源；无法核验的写 `common-lore` 并降权。
> 本机器实测快照（2026-09-05，WSL2 内可见）：ASUS TX Gaming FX608LM_FX608LM，Intel Core Ultra 7 255HX，RTX 5060 Laptop GPU 8GB GDDR7，Windows 驱动 616.56 / NVIDIA App 11.0.9.251 / CUDA 13.3，单根 16GB DDR5-5600（Controller0-ChannelB-DIMM1），BIOS FX608LM.305，2560x1600 @165Hz，MUX Switch + Advanced Optimus。

---

## R0. 616.56 已知闪屏：先修 Bug，再谈“鸡血”

### R0.1 触发条件
- 当前驱动为 616.56，且桌面/浏览器/视频/游戏中出现随机闪烁、黑闪、白闪或亮度突变。
- 用户想要“性能/鸡血驱动”但担心是否该升级或回退。

### R0.2 动作
1. 确认当前驱动版本：NVIDIA App / `nvidia-smi` / PowerShell `Win32_VideoController.DriverVersion`（32.0.16.1656 = 616.56）。
2. 首选：手动安装 **GeForce Hotfix 616.86**（基于 Game Ready 616.64；修复浏览器闪烁、虚拟显示器创建失败、RDP 黑屏；支持 RTX 50/40/30；不会通过 NVIDIA App 推送）。
   - 官方客户支持页/GeForce 驱动页手动下载，不要用第三方“魔改/去签名”版。
3. 安装后确认 NVIDIA App 仍显示旧日期属正常，不代表没装上；用 `nvidia-smi` 或驱动详情确认版本为 616.86。
4. 若暂时不想装 Hotfix：
   - NVIDIA 控制面板 → 显示 → 更改分辨率 → 输出颜色深度改为 **10bpc**（如显示器/接口支持）；
   - 或开启 Windows 自动色彩管理（ACM）；
   - 或将刷新率降低一档观察；
   - 仍不行则回退到此前稳定版 **610.88**（官方驱动包手动装）。
5. 记录闪屏是否消失（最好用同一浏览器/视频/游戏场景做 A/B）。

### R0.3 边界
- “回退 610.88 可修”是社区多用户反馈，不是对所有机型/所有场景都成立；以本机实测为准。
- 616.86 是 Hotfix，QA 周期短于 WHQL；但既然是“修复显示异常”的补丁，通常值得优先试。
- 不要在 616.56 基础上叠加“非官方鸡血驱动/改 Inf/解锁软件”——这会把已知 Bug 和未知风险混在一起，无法归因。
- 10bpc 不一定在 165Hz 下可用；若 10bpc 导致刷新率降低，需要权衡“闪屏消失”与“高刷”。

### R0.4 来源
- 616.56 闪屏报道：https://www.160.com/article/13589.html ；https://www.c114.net.cn/chipnews/118456.html ；https://in.ign.com/tech/270752/nvidias-latest-game-ready-driver-update-reportedly-causes-a-screen-flickering-bug-on-8-bit-monitors
- 616.86 Hotfix 发布：https://news.17173.com/content/09052026/160253589.shtml ；https://tech.ifeng.com/c/8wAl0JyNsVo ；https://www.station-drivers.com/index.php/en/forum/nvidia-drivers-firmwares-utilities/1086-nvidia-geforce-game-ready-driver-616-86-hotfix-whql-released-2026-09-04
- 官方下载路径：https://www.nvidia.com/en-us/geforce/drivers/ （Hotfix 需手动）
- Game Ready 616.64 / DLSS5 相关：https://www.c114.net.cn/chipnews/119321.html

---

## R1. 驱动分支：按用途选，不迷信“最强”

### R1.1 触发条件
- 在“游戏”和“AI/开发/创作”之间做选择，或已经装了 NVIDIA 驱动但不知道 Game Ready / Studio 哪个更适合自己。

### R1.2 动作
1. 游戏为主 → 用 NVIDIA GeForce Game Ready Driver。
2. AI/深度学习、3D 创作、视频剪辑、稳定性优先 → 用 NVIDIA Studio Driver。
3. 混合用途 → 任选一分支；CUDA 计算在两条分支上都可用，游戏和创作优化只影响各自应用。
4. 装上后如遇到厂商特色功能丢失（如 ASUS 电源模式/风扇控制异常），从 ASUS 支持页下载对应型号的原厂驱动回退。
5. 用 NVIDIA App 的驱动回滚功能保留上一版驱动，出问题可秒回。

### R1.3 边界
- 驱动分支对 CUDA/AI 吞吐几乎没有“明显差异”；不要为了 AI 专门追某一种分支。
- 笔记本上安装通用 NVIDIA 驱动可能不会保留所有 OEM 定制项；以厂商支持页为准（单源提示，见来源表，标 `verified-single`）。
- 不是越新越好；如果当前版本（如 616.56）工作正常，没必要因为“新”而升级。

### R1.4 来源
- NVIDIA App Driver Comparisons：https://www.nvidia.com/en-au/software/nvidia-app/driver-comparisons/
- NVIDIA 驱动下载页：https://www.nvidia.com/en-us/geforce/drivers/
- NVIDIA Studio Driver 616.56 页面：https://www.nvidia.com/en-eu/drivers/details/278088/
- NVIDIA 笔记本 OEM 注意事项（搜索摘要/下载结果页）：https://www.nvidia.com/download/driverResults.aspx/263200/en-us/
- ASUS FX608LM 支持页：https://www.asus.com/us/laptops/for-gaming/tuf-gaming/asus-tuf-gaming-f16-2025/helpdesk_download?model2Name=FX608LM

---

## R2. NVIDIA 控制面板电源模式：性能 / 平衡 / 降噪

### R2.1 触发条件
- 插电玩游戏、跑重型 GPU 任务，或觉得风扇太吵需要降噪。

### R2.2 动作
1. 打开 NVIDIA 控制面板 → 3D 设置 → 管理电源和显示设置（或“管理电源设置”）。
2. 若有“电源模式”选项卡，选择：
   - **性能**：最高游戏性能，风扇噪音不是问题；
   - **平衡**：功耗、噪音、游戏性能均衡；
   - **降噪**：低风扇噪音与良好性能。
3. 点击应用；游戏/任务期间用 `nvidia-smi` 或厂商监控确认功耗/频率变化。

### R2.3 边界
- 该设置只在“受支持的笔记本”上出现；部分 Optimus 机型如果显示器不接 NVIDIA 输出，控制面板部分选项不可用。
- 它改变的是 NVIDIA 侧电源策略，不等于解锁厂商锁定的 TGP；最终功耗仍受 Armoury Crate/BIOS/热设计限制。
- 电池模式下“性能”会显著增加耗电和发热，不是默认推荐。

### R2.4 来源
- NVIDIA 官方帮助（中文）：https://www.nvidia.com/content/control-panel-help/vlatest/zh-cn/mergedprojects/nv3dchs/To_set_the_power_mode_on_supported_notebooks.htm
- NVIDIA Optimus 控制面板边界说明（PDF）：http://us.download.nvidia.com/Windows/531.61/531.61-nvidia-control-panel-quick-start-guide.pdf

---

## R3. MUX Switch / Advanced Optimus：用厂商软件切 GPU 模式

### R3.1 触发条件
- 笔记本同时有 iGPU + dGPU（混合显卡），想要“最大 GPU 性能”或“更长续航”。

### R3.2 动作
1. 打开 ASUS Armoury Crate（或厂商性能软件）。
2. 找 GPU 模式 / GPU 模式切换：
   - **Ultimate / dGPU 直连 / 独显直连**：让显示器直连 NVIDIA，最高性能，适合插电游戏、重度 GPU 任务；
   - **Standard / Optimized / Hybrid**：自动在 iGPU/dGPU 间切换，续航更好；
   - **Eco**：优先 iGPU，省电。
3. 切换 Ultimate 后重启/注销，进系统后用 `nvidia-smi` 或任务管理器确认 dGPU 一直激活。
4. 跑 AI/CUDA 不必一定切 Ultimate：WSL2/CUDA 会按需唤醒 dGPU；但切 Ultimate 可避免显示链路额外开销。

### R3.3 边界
- Ultimate 模式通常提高功耗、发热、风扇噪音，并可能缩短电池续航；不要在电池上长期使用。
- 某些机型切换会要求重启；不是热切换。
- 外接显示器路由可能不同；如果切到 Ultimate 后外接屏不亮，切回 Hybrid/Standard 并用厂商说明检查。
- 本机（FX608LM）规格明确支持 MUX Switch + NVIDIA Advanced Optimus；但具体选项名以 Armoury Crate/MyASUS 当前版本为准。

### R3.4 来源
- ASUS TUF Gaming F16 (2025) 规格：https://www.asus.com/us/laptops/for-gaming/tuf-gaming/asus-tuf-gaming-f16-2025/techspec/
- NVIDIA Advanced Optimus 新闻：https://www.nvidia.com/en-au/geforce/news/rtx-laptops-advanced-optimus/
- NVIDIA Max-Q 技术页（Dynamic Boost / Advanced Optimus / Battery Boost）：https://www.nvidia.com/en-us/geforce/laptops/max-q-technologies/

---

## R4. NVIDIA App 一键自动调优：放在瓶颈排查之后

### R4.1 触发条件
- 已经确认 GPU 是当前瓶颈、温度/功耗有余量，且想要一点“免费”频率提升。

### R4.2 动作
1. 先完成 R6 的基线测量，并用监控（`nvidia-smi` / NVIDIA App Performance Panel）确认 GPU 利用率高、温度未到降频线。
2. 打开 NVIDIA App → Systems（系统）→ Performance Panel。
3. 启用 **One-Click Automatic GPU Tuning / 自动调优**；它会扫描一段时间（官方说明约 30 分钟），期间不要运行其他重负载程序、避免休眠。
4. 记录调优后的频率增量和成绩；如果提升 <1–2% 或出现不稳定，回滚。
5. 若厂商软件（Armoury Crate/OMEN Gaming Hub 等）提供显卡核心/显存频率调节，可小步试（如 +100~200MHz），同样逐级验证。

### R4.3 边界
- 不是所有笔记本/显卡都支持自动调优；找不到就不强求。
- 收益通常很小（第三方实测常见 +87MHz 量级），且会带来稳定性/保修风险。
- 如果瓶颈在内存带宽、CPU、显存不足或散热，超频几乎无效。
- 超频/调优不是“默认必做”；用户说“我感觉不对劲”或出现花屏/崩溃立即回滚。

### R4.4 来源
- NVIDIA App 10.0.1 Release Highlights：https://www.nvidia.com/uk-ua/geforce/release-notes/NVAPP/10_0_1/Web/nvapp-v10_0_1-web-release-highlights/
- NVIDIA App FAQ：https://www.nvidia.com/en-us/software/nvidia-app/faq/
- NVIDIA App 性能调优新闻：https://www.nvidia.com/en-sg/geforce/news/nvidia-app-beta-update-av1-performance-tuning/
- 第三方实测（非官方，仅作旁证）：https://m.mydrivers.com/newsview/1072900.html

---

## R5. 内存双通道：这台机器最值得优先验证的硬件项

### R5.1 触发条件
- 机器只有一根内存（当前实测：SK Hynix 16GB DDR5-5600，BANK 1 / ChannelB-DIMM1），或做 AI 训练/大模型推理时经常 OOM、数据加载慢、游戏帧时间不稳。

### R5.2 动作
1. 用 PowerShell/任务管理器确认内存通道数：
   ```powershell
   Get-CimInstance Win32_PhysicalMemory | Select BankLabel,DeviceLocator,Capacity,Speed,Manufacturer
   ```
   只有一根 DIMM = 单通道。
2. 购买与现有内存“同规格、同品牌/颗粒尽量一致”的第二根 DDR5-5600 SO-DIMM（本机最高可扩到 64GB，支持双通道）。
3. 安装后先跑同一基线：游戏 3 次、AI 训练吞吐 1 次；对比单通道/双通道数据。
4. 若收益明显（通常 CPU 受限场景/内存带宽敏感任务提升最大），保留；若没有提升，考虑退掉（保留原样）。

### R5.3 边界
- 这是硬件改动：先确认保修政策、自己是否具备拆机能力；ASUS 机型升级内存一般可操作，但风险自担。
- 双通道不是“所有游戏都大幅提升”；iGPU 和 CPU 受限场景收益更大，GPU 极度受限时可能不变。
- 单通道下 16GB 也够日常；不要因为“瓶颈存在”就立刻买，先验证。
- 来源上“双通道收益”多为硬件常识与第三方评测；本 skill 标记为 `common-lore + verified-single`，不作为绝对保证。

### R5.4 来源
- 本机实测内存信息（PowerShell 输出）。
- Kingston 内存兼容搜索（ASUS TUF Gaming F16 2025）：https://www.kingston.com/unitedkingdom/en/memory/search/model/111077/asus-tuf-gaming-f16-2025
- 第三方“RTX50 游戏本内存升级重要”评测：https://nb.zol.com.cn/992/9924952.html（旁证）
- ASUS 规格（支持双通道、最大 64GB）：https://www.asus.com/us/laptops/for-gaming/tuf-gaming/asus-tuf-gaming-f16-2025/techspec/

---

## R6. WSL2 内存与 CPU 限额

### R6.1 触发条件
- 在 WSL2 里跑 PyTorch/TensorFlow、编译、大数据处理，发现 `free -h` 内存只有约 8GB 且不够，或 Windows 侧被 WSL 吃满。

### R6.2 动作
1. 在 Windows 用户目录（`%UserProfile%`，如 `C:\Users\<用户名>\.wslconfig`）创建/编辑：
   ```ini
   [wsl2]
   memory=10GB        # 不要超过物理内存减去 Windows 安全余量；默认是 Windows 内存的 50%
   processors=12      # 20 线程机器可留 8 个给 Windows
   swap=4GB           # 硬盘兜底；训练建议至少 4-8GB
   ```
2. 保存后执行 `wsl --shutdown`，重新打开 WSL，用 `free -h` 确认。
3. 若跑大模型，考虑把数据/缓存放在 Linux 文件系统（`/home/...`），不要在 `/mnt/c` 频繁读写。

### R6.3 边界
- 本机只有 16GB 物理内存：给 WSL 太多会拖垮 Windows 桌面和 IDE；先从 10GB 试，观察 Windows 是否卡顿。
- `.wslconfig` 对所有 WSL2 发行版生效；修改后必须完全停掉 WSL 才生效（`wsl --shutdown`）。
- 内存不是越多越快；如果没有交换压力，加到 12GB 不一定提升训练。
- 双通道内存升级后，WSL 内存带宽也会受益，但仍受物理内存总量限制。

### R6.4 来源
- Microsoft WSL 配置官方文档：https://learn.microsoft.com/en-us/windows/wsl/wsl-config
- CUDA on WSL User Guide：https://docs.nvidia.com/cuda/wsl-user-guide/index.html

---

## R7. WSL2 CUDA：不要装 Linux NVIDIA 驱动

### R7.1 触发条件
- 在 WSL2 Ubuntu 里跑 `nvidia-smi`、PyTorch/CUDA，或看到“驱动不存在/版本不匹配”。

### R7.2 动作
1. WSL2 使用 Windows 侧 NVIDIA 驱动；在 WSL 里**不要**安装 `nvidia-driver-*`、`cuda-drivers` Linux 包。
2. 保持 Windows 驱动为最新（或与 CUDA 兼容的版本）；WSL 内 `nvidia-smi` 显示的是 Windows driver + KMD。
3. WSL 内只安装 CUDA Toolkit / PyTorch 等软件栈；驱动跟 Windows 走。
4. 若 torch 报 CUDA 不可用，先检查：
   - Windows 驱动版本是否支持当前 CUDA（R495 及以后支持 WSL2）；
   - WSL 内核版本；
   - `nvidia-smi` 是否正常；再用 `torch.cuda.is_available()` 复测。
5. 当前实测：torch 2.13.0+cu130 在 WSL2 中 `cuda available=True`，GPU 为 RTX 5060 Laptop GPU，说明链路正常。

### R7.3 边界
- WSL2 的 NVIDIA-SMI 是“Limited Feature Set”，某些工具（如部分 Nsight/Profilers）在 WSL2 下支持有限；不要按 Linux 桌面环境调。
- 不要与 Windows 驱动版本混用“CUDA 13.3 Toolkit 必须配某 Windows 驱动”的绝对规则；以 CUDA on WSL 文档为准。
- 双端时间不同步、WSL 旧内核也可能造成驱动识别问题，先 `wsl --update` / 更新内核。

### R7.4 来源
- CUDA on WSL User Guide：https://docs.nvidia.com/cuda/wsl-user-guide/index.html
- Microsoft WSL 配置文档（内核/版本）：https://learn.microsoft.com/en-us/windows/wsl/wsl-config
- NVIDIA 论坛 WSL CUDA 13 兼容性讨论：https://forums.developer.nvidia.com/t/tensorflow-rtx-5090-wsl-cuda-12-installed-in-wsl-but-windows-driver-uses-cuda-13/353666/3

---

## R8. 游戏侧设置：G-Sync / Reflex / DLSS / 低延迟

### R8.1 触发条件
- 玩游戏追求流畅、低延迟；屏幕是 165Hz + G-Sync（本机规格）。

### R8.2 动作
1. 开启 G-Sync（NVIDIA 控制面板 → 显示 → G-SYNC），并在游戏内关掉垂直同步或使用 G-Sync + V-Sync on。
2. 游戏支持 Reflex 时开启 Reflex；不支持时可在 NVIDIA 控制面板把“低延迟模式”设为 On/Ultra。
3. 合理使用 DLSS/帧生成：画质与性能之间按需取舍；帧生成会引入额外延迟。
4. 用游戏内基准或第三方（PresentMon / NVIDIA FrameView / NVIDIA App Performance overlay）记录平均 FPS、1% low、帧时间 p95/p99。
5. 以“帧时间/1% low”为准，不要只看平均 FPS。

### R8.3 边界
- Reflex/低延迟在 CPU 受限或帧率已经很高时收益有限；不要期望所有游戏都提升。
- 帧生成不是“免费帧数”，会增加渲染延迟；竞技/精确操作场景慎用。
- 不是所有显示器/接口都支持 G-Sync 可变刷新率；本机规格标注 G-Sync，仍以实际驱动/接口为准。

### R8.4 来源
- NVIDIA Reflex 低延迟平台：https://www.nvidia.cn/geforce/news/reflex-low-latency-platform/
- NVIDIA Max-Q（Battery Boost/Advanced Optimus/G-SYNC 相关）：https://www.nvidia.com/en-us/geforce/laptops/max-q-technologies/
- ASUS 规格（165Hz + G-Sync + MUX/Advanced Optimus）：https://www.asus.com/us/laptops/for-gaming/tuf-gaming/asus-tuf-gaming-f16-2025/techspec/

---

## R9. 散热与功耗边界

### R9.1 触发条件
- 高负载下风扇啸叫、CPU/GPU 温度高（>90°C）、降频、电池掉电快。

### R9.2 动作
1. 垫高/使用散热底座，确保进风口和出风口不被挡住。
2. 插电时用厂商“性能/增强”模式，而不是“静音/Eco”；必要时自定义风扇曲线。
3. 用 `nvidia-smi` 看 `power.draw`、`temperature.gpu`、`clocks.sm`；若温度接近降频点，先降画质/功率，再考虑超频。
4. 清理灰尘/更换硅脂属于深度维护，先看是否有保修/拆机经验。

### R9.3 边界
- “温度高”不等于“必须换硅脂”；笔记本 80–90°C 是常见工作区间，要看是否降频。
- 性能模式会增大噪音和功耗；不要在电池、图书馆、会议场景使用。
- 散热改造可能影响保修；先用软件/垫高方案，若无效再考虑硬件。

### R9.4 来源
- 本机 `nvidia-smi` 实测（P2 空闲，65–76°C，18W 左右）。
- ASUS Armoury Crate 使用指南：https://rog.asus.com/vn/articles/guides/cach-su-dung-armoury-crate-tren-laptop-gaming-rog/
- NVIDIA Max-Q 技术页（功耗/散热/动态加速）：https://www.nvidia.com/en-us/geforce/laptops/max-q-technologies/

---

## R10. 验证纪律：先基线，一次一个变量

### R10.1 触发条件
- 任何调优前后；尤其是“我改了设置感觉变好了”的时候。

### R10.2 动作
1. 定义可复现任务：
   - 游戏：固定同一场景/同一段回放/同一画质，跑 3 次，记录 avg FPS、1% low、p95/p99 帧时间、GPU/CPU 占用。
   - AI：固定模型、batch、数据、随机种子，记录训练耗时/吞吐（samples/s 或 step/s），跑 2–3 次取中位数。
   - 通用：`nvidia-smi --query-gpu=...`（功率/温度/显存/频率）与 `free -h`。
2. 只改一个变量：MUX 或驱动或电源或内存或 WSL 配置，一次一个。
3. 改后重复同样任务；收益≥噪声且无回归才保留，否则回滚。
4. 记录环境（是否插电、风扇模式、室温、后台程序）与日期，方便审计。

### R10.3 边界
- 单次“感觉流畅”不是证据；至少要 3 次并看长尾。
- 无法稳定复现的任务（联网、多开、随机负载）不适合做 A/B；先固定可控场景。
- 硬件升级（加内存）后也应重测，不因“按理应该提升”就视为完成。

### R10.4 来源
- 本 Skill 的“专家讨论”署名结论（教师回合 R1）：John Carmack 与 Brendan Gregg 均要求先测量、一次只改一个变量、关注帧时间/长尾；见 `audit/expert_discussion_round1.md`。
- John Carmack 风格来源：https://koder.ai/blog/john-carmack-performance-engineering-mindset-real-time-graphics
- Brendan Gregg 方法论来源：https://www.brendangregg.com/usemethod.html；https://www.brendangregg.com/tsamethod.html

---

## R11. G-Helper 参数调优（不超频，允许大风扇声）

### R11.1 触发条件
- 用户使用 G-Helper（华硕轻薄/游戏本控制工具），已经能接受较大风扇噪音，想要“参数上的最优解”而不是超频。

### R11.2 动作
1. **GPU Mode：保持 Ultimate / dGPU 直连**（你已做）。这确保显示链路不经过 iGPU，是性能侧最优。
2. **分场景选档，不要日常常驻 Turbo**：
   - 日常/轻度：**Balanced**（或 Custom 1），风扇曲线偏安静；
   - 重型游戏/训练：临时切 **Turbo**（`Fn+F5` 或 G-Helper 热键），用完切回 Balanced；
   - 如果 G-Helper 有 **Custom 1/2**：做一套“高功耗 + 高温才拉高风扇”的自定义档，作为“按需起飞”档。
3. **自定义风扇曲线（在 Balanced/Custom 档里做）**：不要用 BIOS 默认 Turbo 曲线；设温和温度点，让风扇只在温度起来后才加速。参考曲线：
   - ≤60°C：20–25%；
   - 65°C：35%；
   - 70°C：50%；
   - 75°C：70%；
   - 80°C：85%；
   - 85°C 及以上：100%。
4. **温度上限**：设 **85–87°C**（略高于默认目标），避免 BIOS 为了“压到很低温度”而提前把风扇拉满。
5. **功耗限制**：日常 Balanced 用“默认/适中”；重型档再放开到最高可用；这属于“解锁可使用功耗”，不是超频。
6. **不要碰** GPU/显存频率、电压、时钟偏移等“超频类”滑块——你已明确不超频；这些参数留给 NVIDIA App 自动调优或未来有证据再试。
7. **显示**：保持 165Hz，G-Sync 开启；若 Hotfix 后仍闪屏，可在 G-Helper/Windows 里先降到 144Hz/60Hz 作为隔离变量。
8. **电池策略**：插电时关闭“GPU Power Saver / Optimus 自动切换”类的省电选项，避免负载时切回 iGPU。
9. 每项改动后跑同一基准，确认风扇噪音可接受、温度未到降频线、帧时间/训练吞吐没有回退。

### R11.3 边界
- G-Helper 是第三方工具，不是 ASUS 官方 Armoury Crate；更新节奏、错误边界可能不同于原厂。出现控制异常时回 Armoury Crate/MyASUS 排查。
- 不是所有型号都暴露相同选项（CPU PPT、SPL、GPU Power Saver 等）；找不到就说明该型号不支持，不要用注册表/改 BIOS 强开。
- 大风扇声≠性能一定更好：散热已经足够时，继续拉风扇/功耗只是增加噪音；以温度、功率、帧率和“降频点”为证据。
- 不要在 Hotfix 之前叠一堆参数改动；先排除 616.56 已知闪屏，再调 G-Helper。

### R11.4 来源
- G-Helper 官方仓库：https://github.com/seerge/g-helper
- G-Helper GPU Mode 说明（DeepWiki）：https://deepwiki.com/seerge/g-helper/3.2-gpu-mode-management
- 中文使用指南：https://blog.csdn.net/gitblog_00597/article/details/160292215
- 第三方调优文章：http://www.ldpk.cn/news/28235

---

## R12. 知识型深度参数：NVIDIA Profile Inspector + 游戏组合

### R12.1 触发条件
- 用户想比控制面板更细地调每个游戏的参数，但**明确不超频**；或游戏出现着色器编译卡顿、GPU 利用率高但帧时间不稳。

### R12.2 动作
1. 下载并运行 NVIDIA Profile Inspector（便携、不改系统文件；仅写入 NVIDIA 驱动 profile）。
2. 对**单个游戏**建/选 profile，只调以下“参数型”项：
   - `Power Management Mode` = **Prefer Maximum Performance**（插电游戏用；桌面/浏览器留 Default）。
   - `Low Latency Mode` = **Ultra** 或 **On**（配合 Reflex 优先）。
   - `Frame Rate Limit` ≈ **157/158**（比 165Hz 略低，配合 G-Sync，避免 V-Sync 延迟）。
   - `Shader Cache` 开启并调大（减少首进/切换场景的着色器编译卡顿）。
   - `Texture Filtering - Quality` = **High Performance**（可换来帧率，画质略有损失；只对吃性能的游戏用）。
3. 游戏/Q 组合验证：
   - G-Sync on + 帧率上限 157 + 游戏内 V-Sync off；
   - 支持 Reflex 的用 Reflex，不支持的用 Low Latency Ultra；
   - DLSS/帧生成按需开启；帧生成会加延迟，必须配合 Reflex/帧率上限。
4. 全局配置保持“防御性”：不把性能档全局应用到浏览器/桌面，否则增加待机功耗与风扇噪音。

### R12.3 边界
- Profile Inspector 是第三方工具，不是 NVIDIA 官方 App；它改的是驱动 profile，可能被驱动更新重置。使用前备份 profile。
- 不碰 `CudaForceP2State`、时钟偏移、电压偏移等不确定/超频类字段；本技能只推荐有公开文档且效果可测的项。
- 帧率上限不是越高越好；超过显示器刷新率只会增加功耗和热量，不增加可见流畅度。
- 着色器缓存过大也可能占用磁盘；根据游戏数量设置 5–10GB 即可。

### R12.4 来源
- Profile Inspector 使用指南：https://profileinspector.org/tweak-gpu-settings/
- Profile Inspector 着色器缓存指南：https://profileinspector.org/shader-cache/
- 官方 3D 设置帮助（控制面板等价项）：https://www.nvidia.com/content/control-panel-help/vlatest/zh-cn/mergedprojects/nv3dchs/To_set_the_power_mode_on_supported_notebooks.htm

---

## R13. 8GB VRAM 下的 AI/深度学习调优（不换硬件）

### R13.1 触发条件
- RTX 5060 Laptop 只有 8GB 显存；跑训练/微调时 OOM、显存碎片化、吞吐低，但暂时不加内存/不换硬件。

### R13.2 动作
1. **启用 TF32/BF16 数学**：
   ```python
   torch.backends.cuda.matmul.allow_tf32 = True
   torch.backends.cudnn.allow_tf32 = True
   torch.set_float32_matmul_precision('high')   # 内部用 TF32
   ```
2. **混合精度训练**：
   ```python
   from torch.amp import autocast, GradScaler
   scaler = GradScaler('cuda')
   with autocast('cuda', dtype=torch.bfloat16):
       loss = model(x)
   scaler.scale(loss).backward(); scaler.step(opt); scaler.update()
   ```
   （RTX 50 支持 bf16；若模型不支持则用 fp16。）
3. **显存分配器防碎化**：
   ```bash
   export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
   # 若仍碎片化：max_split_size_mb:128
   ```
4. **降低显存占用**：减小 batch、梯度累积、`torch.compile(mode="reduce-overhead")`、对权重做 offload/量化；只在必要时 `torch.cuda.empty_cache()`。
5. **DataLoader**：`pin_memory=True`、`num_workers>0`、`persistent_workers=True`；大训练集放 Linux 文件系统。
6. **监控**：`nvidia-smi dmon` 或 Python `torch.cuda.memory_summary()`；不要只看“没报错”，要看显存峰值与 GPU 利用率。

### R13.3 边界
- TF32/BF16 会改变数值精度；对精度敏感的科学计算要对比验证，不能只图快。
- `expandable_segments` 与 `max_split_size_mb` 不要同时无脑开；先试 `expandable_segments:True`，观察显存峰值。
- 8GB 是硬限制：混合精度只能延后 OOM，不能无中生有；大模型需量化/offload/换卡。
- WSL2 下 `nvidia-smi` 为 Limited Feature Set，某些 profiler 功能不可用；用 Python 侧指标为主。

### R13.4 来源
- PyTorch CUDA 内存/分配器文档：https://docs.pytorch.org/docs/stable/notes/cuda.html
- PyTorch backends TF32 文档：https://docs.pytorch.ac.cn/docs/stable/backends.html
- NVIDIA CUDA 内存问题文档：https://docs.nvidia.com/dl-cuda-graph/troubleshooting/memory-issues.html

---

## 证据分级

| 等级 | 含义 | 本 Skill 使用 |
|---|---|---|
| verified-high | ≥2 个独立权威来源或官方一手且有交叉 | R2、R3、R6、R7、R8 大部分 |
| verified-single | 单一权威来源或官方一手但无独立旁证 | R1 的 OEM 注意事项、R4 的自动调优部分 |
| common-lore | 行业常识/经验，无强来源，已降权 | R5 双通道收益、R9 散热常识 |
| inferred | 从公开实践推断，非本人原话 | R10 专家风格规则 |

## 自检分（蒸馏质量）

- [x] 每条规则有 source_refs
- [x] 每条规则有 trigger/action/boundary
- [x] 不确定/单源已标注，未写成“确定”
- [x] 没有把单一风格写成普遍共识
- [x] 没有把推测写成专家原话
- [x] 用户话术无内部术语/概率
- [x] 至少 1 个反例或失效边界

> 自检：7/7。
