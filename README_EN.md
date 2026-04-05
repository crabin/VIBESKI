<div align="center">

<h1 style="font-size: 3em; font-weight: bold; margin-bottom: 10px;">
  Vibeski
</h1>

<p style="font-size: 1.2em; color: #666; margin-bottom: 20px;">
  <strong>Full-Stack AI Agent Base Application Framework</strong>
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
  <a href="README.md">中文</a> | <a href="README_JA.md">日本語</a> | English
</p>

</div>

---

# Vibeski

A reusable full-stack AI Agent base application framework for rapid "vibe coding" of new applications.

## Features

- **Unified Backend**: FastAPI with REST + SSE interfaces, shared by CLI/TUI, mobile, and desktop clients
- **Multi-LLM Support**: Built-in support for Ollama, DeepSeek, OpenAI, Anthropic, Google, and more
- **Session Management**: Persistent conversations with SQLite storage
- **Event-Driven Architecture**: Real-time streaming via EventBus and SSE
- **Extensible Tool System**: Register custom tools via Python entry_points
- **Multiple Frontends**:
  - Terminal TUI (TypeScript/Ink)
  - Mobile App (React Native/Expo)
  - Desktop App (Tauri + Vite)
- **Configuration Persistence**: SQLite-backed user preferences with 3-tier priority (DB > .env > defaults)

## Architecture

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

## Quick Start

### 1. Clone and Configure

```bash
git clone https://github.com/crabin/VIBESKI.git
cd vibeski
cp .env.example .env
# Edit .env: set LLM_PROVIDER and add your API key
```

### 2. Install Dependencies

```bash
# Python dependencies
uv sync

# Terminal UI dependencies
cd terminal-ui && npm install && cd ..
```

### 3. Run

```bash
python main.py            # backend (port 8000) + Ink TUI
```

Or run separately:

```bash
python main.py --backend  # backend only
python main.py --tui      # TUI only (backend must be running)
```

API docs: http://localhost:8000/docs

### 4. Mobile (Expo)

```bash
cd app && npm install && npx expo start
```

### 5. Desktop (Tauri - requires Rust)

```bash
# Install Rust: https://rustup.rs
cd desktop && npm install && npm run tauri dev
```

## Adding Custom Tools

1. Create a class inheriting `tools.base.BaseTool`
2. Register in `pyproject.toml`:
   ```toml
   [project.entry-points."vibeski.tools.basic"]
   my_tools = "mypackage.tools:MY_TOOLS"
   ```
3. Run `uv sync` — tools are auto-discovered on next start

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider: ollama/deepseek/openai/anthropic/google/... | `ollama` |
| `DATABASE_URL` | SQLite database path | `sqlite:///./data/vibeski.db` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `VIBESKI_SERVER_HOST` | Backend host | `0.0.0.0` |
| `VIBESKI_SERVER_PORT` | Backend port | `8000` |
| `OLLAMA_BASE_URL` | Ollama service URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Default Ollama model | `gemma3:1b` |

## Project Structure

```
vibeski/
├── main.py                 # Entry point
├── vibeski_config/         # Configuration (pydantic-settings + SQLite)
├── router/                 # FastAPI routes (chat, sessions, tools, system)
├── core/                  # Session manager, executor, models
├── database/              # SQLite models and manager
├── tools/                 # Tool registry and example tools
├── prompts/               # Prompt templates
├── skills/                # Skill loader and injector
├── utils/                 # Shared utilities (logger, event_bus, model_selector)
├── vibeski_cli/            # CLI commands and TUI launcher
├── terminal-ui/           # TypeScript/Ink terminal UI
├── app/                   # React Native/Expo mobile app
├── desktop/              # Tauri desktop app
└── docs/                  # Documentation
```

## CLI Commands

```bash
vibeski              # backend + TUI (full stack)
vibeski --backend    # backend only (port 8000, API at http://localhost:8000/docs)
vibeski --tui        # TUI only (backend must already be running)
vibeski-server       # run uvicorn directly (production / Docker use)
```

## Documentation

| Document | Description |
|----------|-------------|
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | Quick start guide |
| [docs/API.md](docs/API.md) | API documentation |
| [docs/LLM_PROVIDERS.md](docs/LLM_PROVIDERS.md) | LLM provider configuration |
| [docs/OLLAMA_SETUP.md](docs/OLLAMA_SETUP.md) | Local Ollama setup |
| [docs/TOOL_EXTENSION.md](docs/TOOL_EXTENSION.md) | Tool extension guide |

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

**crabin**

- GitHub: [@crabin](https://github.com/crabin)
- Email: [cralpbin@gmail.com](mailto:cralpbin@gmail.com)
