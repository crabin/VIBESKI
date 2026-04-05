@echo off
REM Vibeski 可执行文件构建脚本（PyInstaller，Windows）

setlocal

echo 📦 开始构建 Vibeski 可执行文件...

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python
    exit /b 1
)

cd /d "%~dp0.."

REM 清理旧构建
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM 安装依赖
uv sync
uv pip install pyinstaller

REM 单文件可执行程序（vibeski.spec）
pyinstaller vibeski.spec

echo 完成. 可执行文件: dist\vibeski (或 dist\vibeski.exe)
dir dist

pause
