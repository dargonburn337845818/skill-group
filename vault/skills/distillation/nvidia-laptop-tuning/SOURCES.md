# 来源清单（SOURCES）

> 每条来源都要可回溯；本表记录本 Skill 蒸馏时使用的公开材料。
> 标注：`官方一手` / `官方中转` / `第三方` / `实测`。
> 独立来源计数：不同机构/不同页面才算独立；同站转载不计。

## 官方 NVIDIA

| 引用 | URL | 用途 | 可信度 |
|---|---|---|---|
| NVIDIA App Driver Comparisons | https://www.nvidia.com/en-au/software/nvidia-app/driver-comparisons/ | Game Ready / Studio 两个分支定位 | 官方一手 |
| NVIDIA GeForce Drivers | https://www.nvidia.com/en-us/geforce/drivers/ | 驱动下载与分支入口 | 官方一手 |
| NVIDIA Studio Driver 616.56 | https://www.nvidia.com/en-eu/drivers/details/278088/ | 当前版本为 Studio 分支的佐证 | 官方一手 |
| NVIDIA 616.56 驱动闪屏问题报道 | https://www.160.com/article/13589.html；https://www.c114.net.cn/chipnews/118456.html；https://in.ign.com/tech/270752/nvidias-latest-game-ready-driver-update-reportedly-causes-a-screen-flickering-bug-on-8-bit-monitors | 已知 Bug 与 10bpc/ACM/回退 610.88 临时方案 | 第三方 交叉（多源一致） |
| NVIDIA GeForce Hotfix 616.86 发布 | https://news.17173.com/content/09052026/160253589.shtml；https://tech.ifeng.com/c/8wAl0JyNsVo；https://www.station-drivers.com/index.php/en/forum/nvidia-drivers-firmwares-utilities/1086-nvidia-geforce-game-ready-driver-616-86-hotfix-whql-released-2026-09-04 | 修复浏览器闪屏、虚拟显示器创建、RDP 黑屏；基于 GR 616.64 | 多源第三方 + 官方 CDN 直链 |
| Hotfix 手动下载说明 | https://www.nvidia.com/en-us/geforce/drivers/ | Hotfix 不通过 App 推送，需手动 | 官方入口 |
| NVIDIA 笔记本驱动 OEM 注意事项 | https://www.nvidia.com/download/driverResults.aspx/263200/en-us/ | “笔记本可装 GR/SD，但 OEM 定制需注意”的搜索摘要来源 | 官方页面（单源提示） |
| NVIDIA 控制面板电源模式帮助 | https://www.nvidia.com/content/control-panel-help/vlatest/zh-cn/mergedprojects/nv3dchs/To_set_the_power_mode_on_supported_notebooks.htm | 电源模式：性能/平衡/降噪 | 官方一手 |
| NVIDIA 控制面板快速指南 PDF | http://us.download.nvidia.com/Windows/531.61/531.61-nvidia-control-panel-quick-start-guide.pdf | Optimus 下显示控制可用性边界 | 官方一手 |
| NVIDIA Advanced Optimus 新闻 | https://www.nvidia.com/en-au/geforce/news/rtx-laptops-advanced-optimus/ | Advanced Optimus 原理 | 官方一手 |
| NVIDIA Max-Q Technologies | https://www.nvidia.com/en-us/geforce/laptops/max-q-technologies/ | Dynamic Boost / Advanced Optimus / Battery Boost / 功耗优化 | 官方一手 |
| NVIDIA App Release Highlights 10.0.1 | https://www.nvidia.com/uk-ua/geforce/release-notes/NVAPP/10_0_1/Web/nvapp-v10_0_1-web-release-highlights/ | Performance Panel + One-Click Automatic GPU Tuning | 官方一手 |
| NVIDIA App FAQ | https://www.nvidia.com/en-us/software/nvidia-app/faq/ | 自动 GPU 调优与系统页功能 | 官方一手 |
| NVIDIA App 性能调优新闻 | https://www.nvidia.com/en-sg/geforce/news/nvidia-app-beta-update-av1-performance-tuning/ | Performance tuning 功能发布 | 官方一手 |
| CUDA on WSL User Guide | https://docs.nvidia.com/cuda/wsl-user-guide/index.html | WSL2 使用 Windows 驱动、支持范围、限制 | 官方一手 |
| NVIDIA Reflex 低延迟平台 | https://www.nvidia.cn/geforce/news/reflex-low-latency-platform/ | 低延迟模式 / Reflex 用途 | 官方一手 |

## 官方 Microsoft

| 引用 | URL | 用途 | 可信度 |
|---|---|---|---|
| WSL advanced settings (.wslconfig) | https://learn.microsoft.com/en-us/windows/wsl/wsl-config | `memory` / `processors` / `swap` 默认值与配置方法 | 官方一手 |

## ASUS / 厂商

| 引用 | URL | 用途 | 可信度 |
|---|---|---|---|
| ASUS TUF Gaming F16 (2025) 规格 | https://www.asus.com/us/laptops/for-gaming/tuf-gaming/asus-tuf-gaming-f16-2025/techspec/ | 明确 RTX 5060 Laptop 115W、MUX + Advanced Optimus、165Hz G-Sync | 厂商一手 |
| ASUS FX608LM 支持/下载页 | https://www.asus.com/us/laptops/for-gaming/tuf-gaming/asus-tuf-gaming-f16-2025/helpdesk_download?model2Name=FX608LM | 原厂驱动/BIOS 回退入口 | 厂商一手 |
| ASUS Armoury Crate 指南 | https://rog.asus.com/vn/articles/guides/cach-su-dung-armoury-crate-tren-laptop-gaming-rog/ | 性能模式/监控/风扇 | 厂商转述（指南） |
| Kingston 内存兼容搜索 | https://www.kingston.com/unitedkingdom/en/memory/search/model/111077/asus-tuf-gaming-f16-2025 | 第二根内存兼容性入口 | 第三方兼容工具 |

## 实测（本机）

| 项目 | 值 | 方法 |
|---|---|---|
| 主机 | ASUSTeK TX Gaming FX608LM_FX608LM | PowerShell Win32_ComputerSystem |
| BIOS | FX608LM.305（2025-04-28） | PowerShell Win32_BIOS |
| GPU | NVIDIA GeForce RTX 5060 Laptop GPU 8151 MiB | `nvidia-smi` / PowerShell |
| Windows 驱动 | 32.0.16.1656 = 616.56，2026-08-20 | PowerShell Win32_VideoController |
| WSL 驱动 | KMD 616.56，CUDA UMD 13.4 | `nvidia-smi` |
| 内存 | 一根 SK Hynix 16GB DDR5-5600，BANK 1 / ChannelB-DIMM1 | PowerShell Win32_PhysicalMemory |
| 显示器 | 2560x1600 @165Hz | PowerShell VideoModeDescription/CurrentRefreshRate |
| WSL 内存 | 7.4Gi total / 2.0Gi swap | `free -h` |
| PyTorch | torch 2.13.0+cu130，cuda available True | `python3 -c` 实测 |
| 基准 | 4096x4096 fp32 matmul ≈ 9.2 TFLOPS（单次 5 次取均值） | PyTorch 实测 |

## G-Helper / 华硕控制

| 引用 | URL | 用途 | 可信度 |
|---|---|---|---|
| G-Helper 官方仓库 | https://github.com/seerge/g-helper | G-Helper 功能与支持型号 | GitHub 一手（第三方工具） |
| G-Helper GPU Mode 管理 | https://deepwiki.com/seerge/g-helper/3.2-gpu-mode-management | Ultimate/Standard/Eco 模式说明 | 第三方归纳 |
| G-Helper 中文使用指南 | https://blog.csdn.net/gitblog_00597/article/details/160292215 | 性能/风扇/功耗设置操作 | 第三方 |
| G-Helper 调优指南 | http://www.ldpk.cn/news/28235 | 华硕 G-Helper 设置与调优 | 第三方 |

## NVIDIA Profile Inspector / 深度参数

| 引用 | URL | 用途 | 可信度 |
|---|---|---|---|
| Profile Inspector 调参指南 | https://profileinspector.org/tweak-gpu-settings/ | 帧率上限、AA/纹理/V-Sync、G-Sync 兼容 | 第三方（工具向） |
| Profile Inspector 着色器缓存指南 | https://profileinspector.org/shader-cache/ | 减少着色器编译卡顿 | 第三方（工具向） |

## PyTorch / AI 调优

| 引用 | URL | 用途 | 可信度 |
|---|---|---|---|
| PyTorch CUDA 内存/分配器 | https://docs.pytorch.org/docs/stable/notes/cuda.html | allocator、expandable_segments、内存优化 | 官方文档 |
| PyTorch backends TF32 | https://docs.pytorch.ac.cn/docs/stable/backends.html | TF32 开关 | 官方文档 |
| NVIDIA CUDA 内存问题 | https://docs.nvidia.com/dl-cuda-graph/troubleshooting/memory-issues.html | 显存错误排查 | 官方文档 |

## 第三方旁证（非独立权威）

| 引用 | URL | 用途 | 可信度 |
|---|---|---|---|
| 快科技/中关村在线：RTX 50 游戏本性能提升 | https://m.mydrivers.com/newsview/1072900.html | 自动调优 +87MHz 量级、厂商超频入口存在 | 第三方（非官方） |
| ZOL：RTX 50 游戏本升级内存重要 | https://nb.zol.com.cn/992/9924952.html | 单通道/双通道差异旁证 | 第三方（非官方） |
| NVIDIA 开发者论坛 WSL CUDA13 讨论 | https://forums.developer.nvidia.com/t/tensorflow-rtx-5090-wsl-cuda-12-installed-in-wsl-but-windows-driver-uses-cuda-13/353666/3 | WSL CUDA 驱动版本兼容实际案例 | 论坛（旁证） |

## 专家讨论（风格/方法论，非本人原话）

- John Carmack / Brendan Gregg 审查结论记录：`audit/expert_discussion_round1.md`（教师会话 R1）。
- 风格来源：
  - John Carmack：https://koder.ai/blog/john-carmack-performance-engineering-mindset-real-time-graphics；https://www.youtube.com/watch?v=I845O57ZSy4；https://github.com/id-Software/DOOM
  - Brendan Gregg：https://www.brendangregg.com/usemethod.html；https://www.brendangregg.com/tsamethod.html；https://www.brendangregg.com/flamegraphs.html


## Round 40 新增来源

| 引用 | URL | 用途 | 可信度 |
|---|---|---|---|
| Microsoft: Enable NVIDIA CUDA on WSL 2 | https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl | WSL CUDA 前置：Windows 11/10 21H2+、WSL 内核 ≥5.10.43.3、`wsl cat /proc/version` 校验 | 官方一手 |
| Microsoft: GPU accelerated ML training in WSL | https://learn.microsoft.com/en-us/windows/wsl/tutorials/gpu-compute | WSL2 + Docker + NVIDIA Container Toolkit 的安装步骤与容器运行方式 | 官方一手 |
| Microsoft: WSL Troubleshooting | https://learn.microsoft.com/en-us/windows/wsl/troubleshooting | `wsl --version` / `wsl --update` / `wsl --shutdown` / `wsl -l -v` 等诊断命令 | 官方一手 |
| Microsoft: Using Device Manager to Uninstall Devices and Driver Packages | https://learn.microsoft.com/en-us/windows-hardware/drivers/install/using-device-manager-to-uninstall-devices-and-driver-packages | 驱动包卸载/`pnputil /delete-driver` / Windows 自动重装风险 | 官方一手 |
| NVIDIA Developer: GPU in Windows Subsystem for Linux (WSL) | https://developer.nvidia.com/cuda/wsl | WSL2 用 Windows GeForce/Quadro 驱动、CUDA/DirectML、NGC 容器 | 官方一手 |
| NVIDIA: CUDA Toolkit Release Notes | https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html | CUDA Toolkit 与最低驱动版本、minor version compatibility 核对 | 官方一手 |
| Microsoft: DXGI_GPU_PREFERENCE | https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_6/ne-dxgi1_6-dxgi_gpu_preference | 按应用 GPU 偏好：HIGH_PERFORMANCE=dGPU、MINIMUM_POWER=iGPU | 官方一手 |
