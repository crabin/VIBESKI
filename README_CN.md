<div align="center">

<h1 style="font-size: 3em; font-weight: bold; margin-bottom: 10px;">
  Vibeski
</h1>

<p style="font-size: 1.2em; color: #666; margin-bottom: 20px;">
  <strong>全栈 AI Agent 基础应用框架</strong>
</p>

<p>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python">
  </a>
  <a href="pyproject.toml">
    <img src="https://img.shields.io/badge/version-1.0.0-brightgreen.svg" alt="Version">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  </a>
  <a href="https://github.com/crabin/VIBESKI/releases">
    <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  </a>
</p>

<p>
  <a href="https://github.com/langchain-ai/langchain">
    <img src="https://img.shields.io/badge/LangChain-0.1%2B-blueviolet.svg" alt="LangChain">
  </a>
  <a href="https://github.com/langchain-ai/langgraph">
    <img src="https://img.shields.io/badge/LangGraph-0.2%2B-00BFFF.svg" alt="LangGraph">
  </a>
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg" alt="FastAPI">
  </a>
  <a href="https://www.sqlite.org/">
    <img src="https://img.shields.io/badge/SQLite-3.x-003B57.svg" alt="SQLite">
  </a>
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/badge/uv-latest-2E86C1.svg" alt="uv">
  </a>
  <a href="https://github.com/vadimdemedes/ink">
    <img src="https://img.shields.io/badge/Ink-4.4%2B-FF69B4.svg" alt="Ink">
  </a>
</p>

<p>
  <a href="README.md">中文</a> | English
</p>

</div>

---

# Vibeski

一个可复用的全栈 AI Agent 基础应用框架，用于快速"vibe coding"新应用。

## 特性

- **统一后端**: FastAPI 提供 REST + SSE 接口，CLI/TUI、移动端和桌面客户端共用
- **多 LLM 支持**: 内置支持 Ollama、DeepSeek、OpenAI、Anthropic、Google 等
- **会话管理**: SQLite 持久化存储对话历史
- **事件驱动架构**: 通过 EventBus 和 SSE 实现实时流式输出
- **可扩展工具系统**: 通过 Python entry_points 注册自定义工具
- **多前端支持**:
  - 终端 TUI (TypeScript/Ink)
  - 移动应用 (React Native/Expo)
  - 桌面应用 (Tauri + Vite)
- **配置持久化**: SQLite 支持用户偏好设置，三级优先级 (DB > .env > 默认值)

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontends                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                    │
│  │ Terminal │ │  Mobile   │ │ Desktop  │                    │
│  │  (Ink)   │ │  (Expo)   │ │ (Tauri)  │                    │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘                    │
│           │              │              │                     │
│           └──────────────┴─────────────────────────────────┘
│                          │                                │
│                          ▼                                │
│               ┌────────────────────────────┐                │
│               │      FastAPI Backend       │                │
│               │  ┌──────────────────────┐ │                │
│               │  │  Session Manager     │ │                │
│               │  ├──────────────────────┤ │                │
│               │  │  Event Bus           │ │                │
│               │  ├──────────────────────┤ │                │
│               │  │  Tool Registry      │ │                │
│               │  └──────────────────────┘ │                │
│               └────────────────────────────┘                │
│                          │                                │
│                          ▼                                │
│               ┌────────────────────────────┐                │
│               │       SQLite Storage       │                │
│               │  ┌──────────────────────┐ │                │
│               │  │  Conversations       │ │                │
│               │  ├──────────────────────┤ │                │
│               │  │  User Configs        │ │                │
│               │  ├──────────────────────┤ │                │
│               │  │  Prompt Chains       │ │                │
│               │  └──────────────────────┘ │                │
│               └────────────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## 快速开始

### 1. 克隆并配置

```bash
git clone https://github.com/crabin/VIBESKI.git
cd vibeski
cp .env.example .env
# 编辑 .env: 设置 LLM_PROVIDER 并添加你的 API key
```

### 2. 安装依赖

```bash
# Python 依赖
uv sync

# 终端 UI 依赖
cd terminal-ui && npm install && cd ..
```

### 3. 运行

```bash
python main.py            # 后端 (端口 8000) + Ink TUI
```

或分开运行:

```bash
python main.py --backend  # 仅后端
python main.py --tui      # 仅 TUI (后端必须已运行)
```

API 文档: http://localhost:8000/docs

### 4. 移动端 (Expo)

```bash
cd app && npm install && npx expo start
```

### 5. 桌面端 (Tauri - 需要 Rust)

```bash
# 安装 Rust: https://rustup.rs
cd desktop && npm install && npm run tauri dev
```

## 添加自定义工具

1. 创建继承 `tools.base.BaseTool` 的类
2. 在 `pyproject.toml` 中注册:
   ```toml
   [project.entry-points."vibeski.tools.basic"]
   my_tools = "mypackage.tools:MY_TOOLS"
   ```
3. 运行 `uv sync` — 工具会在下次启动时自动发现

## 环境变量

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `LLM_PROVIDER` | LLM 提供商: ollama/deepseek/openai/anthropic/google/... | `ollama` |
| `DATABASE_URL` | SQLite 数据库路径 | `sqlite:///./data/vibeski.db` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `VIBESKI_SERVER_HOST` | 后端主机 | `0.0.0.0` |
| `VIBESKI_SERVER_PORT` | 后端端口 | `8000` |
| `OLLAMA_BASE_URL` | Ollama 服务 URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | 默认 Ollama 模型 | `gemma3:1b` |

## 项目结构

```
vibeski/
├── main.py                 # 入口点
├── vibeski_config/         # 配置 (pydantic-settings + SQLite)
├── router/                 # FastAPI 路由 (chat, sessions, tools, system)
├── core/                  # 会话管理器、执行器、模型
├── database/              # SQLite 模型和管理器
├── tools/                 # 工具注册和示例工具
├── prompts/               # 提示词模板
├── skills/                # 技能加载器和注入器
├── utils/                 # 共享工具 (logger, event_bus, model_selector)
├── vibeski_cli/            # CLI 命令和 TUI 启动器
├── terminal-ui/           # TypeScript/Ink 终端 UI
├── app/                   # React Native/Expo 移动应用
├── desktop/              # Tauri 桌面应用
└── docs/                  # 文档
```

## CLI 命令

```bash
vibeski              # 后端 + TUI (全栈)
vibeski --backend    # 仅后端 (端口 8000, API 在 http://localhost:8000/docs)
vibeski --tui        # 仅 TUI (后端必须已运行)
vibeski-server       # 直接运行 uvicorn (生产环境 / Docker 使用)
```

## 文档

| 文档 | 描述 |
|------|------|
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | 快速开始指南 |
| [docs/API.md](docs/API.md) | API 文档 |
| [docs/LLM_PROVIDERS.md](docs/LLM_PROVIDERS.md) | LLM 提供商配置 |
| [docs/OLLAMA_SETUP.md](docs/OLLAMA_SETUP.md) | 本地 Ollama 设置 |
| [docs/TOOL_EXTENSION.md](docs/TOOL_EXTENSION.md) | 工具扩展指南 |

## 开源协议

MIT License - 详见 [LICENSE](LICENSE)。

## 作者

**crabin**

- GitHub: [@crabin](https://github.com/crabin)
- Email: [cralpbin@gmail.com](mailto:cralpbin@gmail.com)
