#!/bin/bash
# Vibeski 构建脚本（源码分发包 sdist/wheel）
# 推荐使用: uv run python -m build

set -e

echo "🚀 开始构建 Vibeski..."

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查 Python
echo -e "${YELLOW}检查 Python...${NC}"
if command -v python3 &>/dev/null; then
  python_version=$(python3 --version 2>&1)
elif command -v python &>/dev/null; then
  python_version=$(python --version 2>&1)
else
  echo "错误: 未找到 Python，请先安装 Python 3.10+"
  exit 1
fi
echo "$python_version"

# 清理旧构建
echo -e "${YELLOW}清理旧的构建文件...${NC}"
rm -rf build/ dist/ *.egg-info

# 优先使用 uv，否则用 pip
if command -v uv &>/dev/null; then
  echo "使用 uv 构建..."
  uv run python -m build
else
  echo "安装构建工具..."
  python -m pip install --upgrade pip build wheel
  python -m build
fi

echo "✅ 构建完成!"
echo "构建产物:"
ls -la dist/
