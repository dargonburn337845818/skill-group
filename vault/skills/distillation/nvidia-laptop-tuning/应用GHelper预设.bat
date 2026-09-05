@echo off
chcp 936 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0optimizer\ghelper-apply-presets.ps1" -Apply
pause
