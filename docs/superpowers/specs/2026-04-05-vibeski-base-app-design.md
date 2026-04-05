# vibeski — Base App Design Spec

**Date:** 2026-04-05
**Status:** Approved
**Source project:** secbot (Copy + Strip approach)

---

## Overview

Extract the generic full-stack AI agent architecture from secbot into a standalone repository named **vibeski** — a reusable base for rapid "vibe coding" of new AI agent applications. All security/pentest-specific code is removed; the skeleton, patterns, and wiring are preserved exactly.

---

## Deliverable

A new standalone Git repository `vibeski/` (sibling directory to secbot, or published to GitHub), ready to clone, rename, and build on.

---

## Repository Structure

```
vibeski/
├── main.py                     # Entry: python main.py / --backend / --tui
├── pyproject.toml              # Package: vibeski, CLI: vibeski / vibeski-server
├── .env.example                # Created from scratch (see Bootstrap section)
├── uv.toml
│
├── vibeski_config/             # Config module (renamed from hackbot_config)
│   └── __init__.py             # pydantic-settings + SQLite-backed persistence + multi-provider LLM
│
├── router/
│   ├── main.py                 # FastAPI app factory, CORS, request logging middleware
│   ├── chat.py                 # /api/chat (SSE streaming)
│   ├── sessions.py             # /api/sessions CRUD
│   ├── system.py               # /api/system/info, /api/system/model
│   ├── database.py             # /api/database (stats, configs)
│   ├── tools.py                # /api/tools (list, call)
│   ├── dependencies.py         # REWRITTEN — see "Rewritten Files" section
│   └── schemas.py              # Pydantic request/response schemas
│
├── core/
│   ├── models.py               # PlanResult, TodoItem, Session dataclasses (kept as-is)
│   ├── session.py              # REWRITTEN — see "Rewritten Files" section
│   └── executor.py             # TaskExecutor: layered async execution with EventBus
│
├── database/
│   ├── manager.py              # SQLite DatabaseManager (context manager, CRUD)
│   └── models.py               # STRIPPED — see "Rewritten Files" section
│
├── utils/
│   ├── logger.py               # loguru + context injection + secret sanitization
│   ├── log_context.py          # Thread-local log context (session_id, request_id, etc.)
│   ├── event_bus.py            # Pub/sub EventBus (sync + async emit)
│   ├── model_selector.py       # Multi-provider LLM factory
│   ├── config_storage.py       # Config read/write helpers
│   ├── context_info.py         # System context helpers
│   ├── embeddings.py           # Embedding utilities
│   ├── llm_http_fallback.py    # HTTP fallback for LLM providers
│   ├── loading.py              # Loading indicator helpers
│   └── tool_caller.py          # Tool invocation helpers
│
├── prompts/
│   ├── manager.py              # Prompt template manager
│   └── chain.py                # Prompt chain builder
│
├── tools/
│   ├── __init__.py
│   ├── base.py                 # BaseTool abstract class
│   ├── registry.py             # Extensible tool registry (Python entry_points)
│   ├── system_tool.py          # Example: OS info, CPU, memory (sync, no external deps)
│   ├── web_search_tool.py      # Example: DuckDuckGo search via ddgs (merged from web_search.py + web_search_ddgs.py)
│   └── web_research/
│       ├── __init__.py
│       └── page_extract_tool.py  # Example: HTTP fetch + BeautifulSoup text extraction
│
├── skills/
│   ├── __init__.py
│   ├── loader.py               # Skill loader
│   └── injector.py             # Skill injector for agent memory
│
├── vibeski_cli/                # CLI package (renamed from secbot_cli)
│   ├── __init__.py
│   ├── cli.py                  # Typer CLI: vibeski / vibeski-server commands
│   ├── launch_tui.py           # Orchestrator: start backend subprocess + TUI subprocess
│   └── log_viewer.py           # Log tail viewer (aggregates backend + TUI logs)
│
├── terminal-ui/                # TypeScript/Ink TUI (unchanged except VIBESKI_API_URL)
│   ├── package.json            # name: vibeski-terminal-ui
│   ├── tsconfig.json
│   └── src/
│       ├── cli.tsx             # Entry point
│       ├── App.tsx
│       ├── MainContent.tsx
│       ├── api.ts              # HTTP/SSE client — default URL: VIBESKI_API_URL
│       ├── config.ts
│       ├── useChat.ts
│       ├── types.ts
│       ├── events.ts
│       ├── intent.ts
│       ├── slash.ts
│       ├── sse.ts
│       ├── contentBlocks.ts
│       ├── renderMarkdown.ts
│       ├── blockDiscriminators/
│       ├── contexts/
│       ├── components/
│       └── views/
│
├── app/                        # React Native / Expo mobile app (kept as-is)
│   ├── package.json
│   ├── App.tsx
│   ├── index.ts
│   └── src/
│
├── desktop/                    # Vite/Tauri desktop app (kept as-is, Rust backend)
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── index.html
│   └── src-tauri/              # Rust Tauri backend (Cargo.toml, tauri.conf.json, src/)
│
├── data/                       # vibeski.db (gitignored)
├── logs/                       # gitignored
├── tests/
│   └── __init__.py
└── docs/
    └── QUICKSTART.md
```

---

## Architecture

### Request Lifecycle (Chat)

```
User (TUI / Mobile / Desktop)
  → POST /api/chat  or  GET /api/chat/stream (SSE)
  → router/chat.py
  → core/session.py  — load or create session
  → utils/model_selector.py  — pick LLM provider from config
  → LangChain / LangGraph agent  (generic, domain-agnostic)
  → tools/registry.py  — tool calls dispatched as needed
  → utils/event_bus.py  — stream chunks to SSE response
  → database/manager.py  — persist conversation
  → SSE response to frontend
```

### Config Priority (3-tier)

```
SQLite user_configs table  >  .env file  >  hardcoded defaults
```

Runtime changes (model switch, API key update, log level) write to SQLite immediately and survive restart.

### Tool Registry

Tools register via Python `entry_points` in `pyproject.toml` under two groups:

```toml
[project.entry-points."vibeski.tools.basic"]
my_basic_tools = "mypackage.tools:MY_TOOLS"

[project.entry-points."vibeski.tools.advanced"]
my_advanced_tools = "mypackage.tools:MY_ADVANCED_TOOLS"
```

Third-party packages can add tools without modifying vibeski source code. The env var overrides are `VIBESKI_TOOL_MODULES` (basic) and `VIBESKI_TOOL_MODULES_ADVANCED` (advanced).

### Process Model

```
python main.py
  ├── subprocess: uvicorn router.main:app   (Python backend, port 8000)
  └── subprocess: npm run tui               (Ink TUI, reads VIBESKI_API_URL)
```

Desktop (Tauri) and mobile (Expo) apps connect to the same backend independently. Desktop uses `VIBESKI_DESKTOP=1` to lock host to `127.0.0.1` and disable reload.

---

## Rewritten Files

These files exist in secbot but **must be rewritten** (not just renamed) for vibeski because they contain domain-specific imports.

### `router/dependencies.py` (rewrite)

The secbot version imports 10+ security-domain agents and managers. The vibeski version contains only:

```python
# Singletons: DatabaseManager, PromptManager, a single generic LangChain/LangGraph agent
# FastAPI Depends functions: get_db_manager, get_prompt_manager, get_agent, get_session_id
# No DefenseManager, MainController, OSController, OSDetector, AuditTrail
```

### `core/session.py` (rewrite)

The secbot version imports `PlannerAgent`, `QAAgent`, `SummaryAgent`, and a domain-specific router. The vibeski version contains:

```python
# Generic SessionManager that:
# - Manages session lifecycle (create, load, save)
# - Accepts any LangChain-compatible agent via constructor injection
# - Dispatches events to EventBus (THINK_CHUNK, EXEC_RESULT, etc.)
# - Persists conversations via DatabaseManager
# No PlannerAgent, QAAgent, SummaryAgent, or message_route_with_llm imports
```

### `database/models.py` (strip)

Keep: `Conversation`, `PromptChainModel`, `UserConfig`, `AuditRecord`
Remove: `CrawlerTask`, `AttackTask`, `ScanResult` (security-domain models)

Also update `database/manager.py` to remove the corresponding table creation DDL and CRUD methods for the three stripped models.

---

## Renamed Identifiers

| secbot (source) | vibeski (target) |
|-----------------|------------------|
| `hackbot_config` | `vibeski_config` |
| `secbot_cli` | `vibeski_cli` |
| `secbot.db` | `vibeski.db` |
| `SECBOT_*` env vars | `VIBESKI_*` env vars |
| `SECBOT_TOOL_MODULES` | `VIBESKI_TOOL_MODULES` |
| `SECBOT_TOOL_MODULES_ADVANCED` | `VIBESKI_TOOL_MODULES_ADVANCED` |
| `secbot.tools.basic` entry-point group | `vibeski.tools.basic` |
| `secbot.tools.advanced` entry-point group | `vibeski.tools.advanced` |
| `hackbot` / `secbot` CLI | `vibeski` CLI |
| `hackbot-server` / `secbot-server` | `vibeski-server` |
| `secbot-terminal-ui` (package.json name) | `vibeski-terminal-ui` |
| `SECBOT_API_URL` (terminal-ui env) | `VIBESKI_API_URL` |
| `SECBOT_DESKTOP` | `VIBESKI_DESKTOP` |
| `SECBOT_SERVER_HOST/PORT/RELOAD` | `VIBESKI_SERVER_HOST/PORT/RELOAD` |
| `secbot-cli` agent_type in DB | `vibeski` |

---

## What Is Removed (vs secbot)

### Entire directories

| Path | Reason |
|------|--------|
| `tools/pentest/` | Security-domain |
| `tools/offense/` | Security-domain |
| `tools/osint/` | Security-domain |
| `tools/web/` | Security-domain |
| `tools/cloud/` | Security-domain |
| `tools/protocol/` | Security-domain |
| `tools/reporting/` | Security-domain |
| `tools/defense/` | Security-domain |
| `tools/utility/` | Evaluate per file; likely remove |
| `scanner/` | Security-domain |
| `defense/` | Security-domain |
| `payloads/` | Security-domain |
| `crawler/` | Security-domain |
| `controller/` | Security-domain |
| `system/` | Security-domain (OSController, OSDetector, system commands) |
| `core/agents/` | Security-domain agents (HackbotAgent, CoordinatorAgent, etc.) |
| `core/memory/` | KEEP — generic (DatabaseMemory wraps DatabaseManager; VectorStore is generic SQLite vec search) |
| `core/attack_chain/` | REMOVE — security-domain |
| `core/patterns/` | REMOVE — `react.py` depends on removed `core/agents/base`; `security_react.py` is security-domain |
| `core/vuln_db/` | REMOVE — security-domain |

### Specific files

| File | Reason |
|------|--------|
| `router/defense.py` | Security-domain |
| `router/network.py` | Security-domain |
| `router/agents.py` | Security-domain agent routes |
| `skills/workflow.py` | secbot-specific workflow |
| `tools/web_search.py` | Merged into `tools/web_search_tool.py` |
| `tools/web_search_ddgs.py` | Merged into `tools/web_search_tool.py` |
| `utils/audit.py` | AuditTrail is security-domain specific |
| `utils/confirmation.py` | secbot-specific user confirmation flows |
| `utils/generate_report.py` | Security report generation |
| `utils/manual_test_runner.py` | secbot-specific test utilities |
| `utils/opencode_layout.py` | secbot-specific UI layout |
| `utils/release_docs.py` | secbot-specific release tooling |
| `utils/root_policy.py` | Root privilege escalation — security-domain |
| `utils/run_tests.py` | secbot-specific test runner |
| `utils/speech.py` | Optional STT/TTS — remove for minimal base |
| `hackbot.spec` | PyInstaller spec — remove for now |
| `assets/secbot_*.png` | Replace with vibeski branding (or leave empty) |

### `database/models.py` models to strip

- `CrawlerTask`
- `AttackTask`
- `ScanResult`

Also strip the following from `database/manager.py`:
- DDL in `_init_database()`: `CREATE TABLE crawler_tasks`, `CREATE TABLE attack_tasks`, `CREATE TABLE scan_results` (and their index statements)
- CRUD methods: `save_crawler_task`, `update_crawler_task`, `get_crawler_tasks` (the only three domain-specific CRUD methods; `attack_tasks` and `scan_results` have no CRUD methods, only DDL)
- `get_stats()`: remove the three stats entries (`crawler_tasks`, `crawler_tasks_by_status`; no attack/scan stats exist)

---

## What Is Kept

| Path | Notes |
|------|-------|
| `main.py` | Entry point orchestrator |
| `vibeski_config/` | Full config system |
| `router/main.py` + core routers | chat, sessions, system, database, tools |
| `router/dependencies.py` | **Rewritten** (generic only) |
| `core/models.py` | Kept as-is |
| `core/session.py` | **Rewritten** (generic SessionManager) |
| `core/executor.py` | Kept as-is (TaskExecutor is generic) |
| `database/manager.py` | Kept, minus 3 stripped domain tables |
| `database/models.py` | **Stripped** (remove 3 domain models) |
| `utils/logger.py` | Kept as-is |
| `utils/log_context.py` | Kept as-is |
| `utils/event_bus.py` | Kept as-is |
| `utils/model_selector.py` | Kept as-is |
| `utils/config_storage.py` | Kept as-is |
| `utils/context_info.py` | Kept as-is |
| `utils/embeddings.py` | Kept as-is |
| `utils/llm_http_fallback.py` | Kept as-is |
| `utils/loading.py` | Kept as-is |
| `utils/tool_caller.py` | Kept as-is |
| `prompts/` | Kept as-is |
| `skills/loader.py`, `skills/injector.py` | Kept as-is |
| `tools/base.py`, `tools/registry.py` | Kept, entry-point group names renamed |
| `tools/system_tool.py` | Kept as example tool |
| `tools/web_research/page_extract_tool.py` | Kept as example tool |
| `vibeski_cli/` | Kept, all `secbot` references renamed |
| `terminal-ui/` | Full copy, `SECBOT_API_URL` → `VIBESKI_API_URL` |
| `app/` | Full copy as-is |
| `desktop/` | Full copy as-is (Vite/Tauri with `src-tauri/`) |
| `tests/` | Skeleton kept |

---

## Example Tools (3 included)

| Tool | File | Demonstrates |
|------|------|--------------|
| System Info | `tools/system_tool.py` | Sync tool, no external deps, `psutil` |
| Web Search | `tools/web_search_tool.py` | Async tool, ddgs library (merged from two source files) |
| Page Extract | `tools/web_research/page_extract_tool.py` | HTTP + BeautifulSoup text extraction |

---

## `.env.example` (create from scratch)

The source repo has no `.env.example` (only a gitignored `.env`). This file must be created. Minimum keys:

```dotenv
# LLM Provider: ollama / deepseek / openai / anthropic / google / zhipu / qwen / moonshot / baichuan / lingyiwanwu / custom
LLM_PROVIDER=ollama

# Database
DATABASE_URL=sqlite:///./data/vibeski.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/agent.log

# Server
VIBESKI_SERVER_HOST=0.0.0.0
VIBESKI_SERVER_PORT=8000

# Ollama (default provider)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:1b

# OpenAI-compatible providers (uncomment as needed)
# OPENAI_API_KEY=sk-...
# DEEPSEEK_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...

# Tool modules (optional — comma-separated module paths)
# VIBESKI_TOOL_MODULES=mypackage.tools
# VIBESKI_TOOL_MODULES_ADVANCED=mypackage.advanced_tools
```

---

## Bootstrap (Developer Experience)

```bash
git clone https://github.com/you/vibeski
cd vibeski
cp .env.example .env        # fill in LLM_PROVIDER + API keys
uv sync
cd terminal-ui && npm install && cd ..
python main.py              # starts backend (port 8000) + Ink TUI
```

For mobile (Expo):
```bash
cd app && npm install
npx expo start
```

For desktop (Tauri — requires Rust toolchain):
```bash
# Install Rust: https://rustup.rs
cd desktop && npm install
npm run tauri dev
```

> Desktop Tauri build is **optional for v1**. The backend and TUI work independently without it.

---

## CLI Commands

```bash
vibeski              # backend + TUI (full stack)
vibeski --backend    # backend only (port 8000, API at http://localhost:8000/docs)
vibeski --tui        # TUI only (backend must already be running)
vibeski-server       # run uvicorn directly (production / Docker use)
```

---

## Non-Goals (v1)

- No Docker setup
- No CI/CD pipeline
- No authentication/authorization layer (stub only)
- No SQLite migration system (schema created fresh on first run)
- No STT/TTS (speech.py removed)
- No PyInstaller packaging (hackbot.spec removed)
