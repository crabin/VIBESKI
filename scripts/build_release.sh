#!/bin/bash
# Vibeski 可执行文件构建脚本（PyInstaller，当前平台）

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "📦 开始构建 Vibeski 可执行文件..."

# 检查 Python
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "错误: 未找到 Python，请先安装 Python 3.10+"
    exit 1
fi

# 清理旧构建
rm -rf build dist

# 安装依赖
if command -v uv &>/dev/null; then
    uv sync
    uv pip install pyinstaller
else
    python -m pip install --upgrade pip pyinstaller
fi

# 单文件可执行程序（vibeski.spec）
pyinstaller vibeski.spec

echo "完成. 可执行文件: dist/vibeski (或 dist/vibeski.exe)"
ls -la dist/
