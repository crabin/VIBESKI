.PHONY: help install build clean test dev

help:
	@echo "Vibeski 构建和开发命令"
	@echo ""
	@echo "可用命令:"
	@echo "  make install   - 安装依赖 (使用 uv)"
	@echo "  make build     - 构建 Python 包"
	@echo "  make clean     - 清理构建文件"
	@echo "  make test      - 运行测试"
	@echo "  make dev       - 启动开发服务器 (backend + TUI)"

install:
	uv sync

build:
	uv run python -m build

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

test:
	uv run pytest tests/ -v

dev:
	uv run python main.py

