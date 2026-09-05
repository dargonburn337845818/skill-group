@echo off
chcp 936 >nul
setlocal
set CSC=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe
if not exist "%CSC%" set CSC=C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe
echo Compiling NvidiaTuningPanel.exe (DPI aware) ...
"%CSC%" /nologo /target:winexe /out:D:\<工具目录>\NvidiaTuningPanel.exe D:\<工具目录>\src\NvidiaTuningPanel.cs /r:System.Windows.Forms.dll /r:System.Drawing.dll /win32manifest:D:\<工具目录>\src\app.manifest
if errorlevel 1 (
  echo [ERR] Build failed.
) else (
  echo [OK] Built D:\<工具目录>\NvidiaTuningPanel.exe
)
pause
