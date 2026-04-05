# vibeski Base App Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a standalone `vibeski` repository by copying secbot and stripping all security/pentest-specific code, leaving a reusable full-stack AI agent base app (FastAPI + Ink TUI + Expo mobile + Tauri desktop).

**Architecture:** Copy-then-strip approach. Start with a full copy of secbot, delete domain-specific directories and files, rewrite three files that have domain-specific imports, then do a global identifier rename from `secbot/hackbot` to `vibeski`.

**Tech Stack:** Python 3.10+, FastAPI, LangChain/LangGraph, SQLite, loguru, TypeScript/Ink (TUI), React Native/Expo (mobile), Vite/Tauri (desktop), uv, Node.js 18+

**Destination:** `/Users/lpb/workspace/github/agent/vibeski/`

---

## File Map

### Created (new files)
- `vibeski/.env.example` — minimum env vars for bootstrap
- `vibeski/tools/web_search_tool.py` — merged from secbot's `web_search.py` + `web_search_ddgs.py`
- `vibeski/docs/QUICKSTART.md` — developer bootstrap guide
- `vibeski/tests/test_smoke.py` — smoke tests (import + backend health)

### Rewritten (must not carry over domain imports)
- `vibeski/router/dependencies.py` — generic singleton container (DatabaseManager, PromptManager only)
- `vibeski/core/session.py` — generic SessionManager (no secbot agents)
- `vibeski/database/models.py` — strip CrawlerTask, AttackTask, ScanResult
- `vibeski/database/manager.py` — strip corresponding DDL + CRUD + stats entries

### Renamed (directory copy + rename)
- `hackbot_config/` → `vibeski_config/`
- `secbot_cli/` → `vibeski_cli/`

### Globally renamed (string replace across all files)
- `hackbot_config` → `vibeski_config`
- `secbot_cli` → `vibeski_cli`
- `secbot.db` → `vibeski.db`
- `SECBOT_` → `VIBESKI_` (env var prefixes)
- `secbot.tools.basic` → `vibeski.tools.basic`
- `secbot.tools.advanced` → `vibeski.tools.advanced`
- `SECBOT_TOOL_MODULES` → `VIBESKI_TOOL_MODULES`
- `secbot-terminal-ui` → `vibeski-terminal-ui`
- `SECBOT_API_URL` → `VIBESKI_API_URL`

### Deleted (entire directories)
`tools/pentest/`, `tools/offense/`, `tools/osint/`, `tools/web/`, `tools/cloud/`, `tools/protocol/`, `tools/reporting/`, `tools/defense/`, `tools/utility/`, `scanner/`, `defense/`, `payloads/`, `crawler/`, `controller/`, `system/`, `core/agents/`, `core/attack_chain/`, `core/patterns/`, `core/vuln_db/`

### Deleted (specific files)
`router/defense.py`, `router/network.py`, `router/agents.py`, `skills/workflow.py`, `tools/web_search.py`, `tools/web_search_ddgs.py`, `utils/audit.py`, `utils/confirmation.py`, `utils/generate_report.py`, `utils/manual_test_runner.py`, `utils/opencode_layout.py`, `utils/release_docs.py`, `utils/root_policy.py`, `utils/run_tests.py`, `utils/speech.py`, `hackbot.spec`, `assets/secbot_architecture.png`, `assets/secbot-main.png`

---

## Task 1: Copy repo and initialize fresh git history

**Files:**
- Create: `/Users/lpb/workspace/github/agent/vibeski/` (entire repo)

- [ ] **Step 1.1: Copy secbot to vibeski**

```bash
cp -r /Users/lpb/workspace/github/agent/secbot /Users/lpb/workspace/github/agent/vibeski
```

- [ ] **Step 1.2: Remove the copied git history and start fresh**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
rm -rf .git
git init
git add .
git commit -m "chore: initial copy from secbot — strip begins"
```

Expected: `[main (root-commit) xxxxxxx] chore: initial copy from secbot — strip begins`

- [ ] **Step 1.3: Verify the copy is intact**

```bash
ls /Users/lpb/workspace/github/agent/vibeski/
```

Expected: `main.py  pyproject.toml  router/  core/  database/  utils/  tools/  ...`

---

## Task 2: Delete all security-domain directories

**Files:**
- Delete: 19 directories listed in spec

- [ ] **Step 2.1: Delete domain tool directories**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
rm -rf tools/pentest tools/offense tools/osint tools/web tools/cloud tools/protocol tools/reporting tools/defense tools/utility
```

- [ ] **Step 2.2: Delete domain application directories**

```bash
rm -rf scanner defense payloads crawler controller system
```

- [ ] **Step 2.3: Delete domain core subdirectories**

```bash
rm -rf core/agents core/attack_chain core/patterns core/vuln_db
```

- [ ] **Step 2.4: Verify they are gone**

```bash
ls tools/ core/
```

Expected tools/: `__init__.py  base.py  registry.py  system_tool.py  web_research/  web_search.py  web_search_ddgs.py`
Expected core/: `__init__.py  executor.py  memory/  models.py  session.py`

- [ ] **Step 2.5: Commit**

```bash
git add -A
git commit -m "chore: remove security-domain directories"
```

---

## Task 3: Delete security-domain individual files

**Files:**
- Delete: 16 individual files

- [ ] **Step 3.1: Delete domain router files**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
rm -f router/defense.py router/network.py router/agents.py
```

- [ ] **Step 3.2: Delete extra tools/web_research files (keep only page_extract_tool.py)**

```bash
rm -f tools/web_research/web_research_tool.py \
      tools/web_research/api_client_tool.py \
      tools/web_research/deep_crawl_tool.py \
      tools/web_research/smart_search_tool.py
```

- [ ] **Step 3.4: Delete domain skills, tools, utils files**

```bash
rm -f skills/workflow.py
rm -f tools/web_search.py tools/web_search_ddgs.py
rm -f utils/audit.py utils/confirmation.py utils/generate_report.py
rm -f utils/manual_test_runner.py utils/opencode_layout.py utils/release_docs.py
rm -f utils/root_policy.py utils/run_tests.py utils/speech.py
```

- [ ] **Step 3.6: Delete packaging and asset files**

```bash
rm -f hackbot.spec
rm -f assets/secbot_architecture.png assets/secbot-main.png
```

- [ ] **Step 3.4: Verify router only has the kept files**

```bash
ls router/
```

Expected: `__init__.py  chat.py  database.py  dependencies.py  main.py  schemas.py  sessions.py  system.py  tools.py`

- [ ] **Step 3.5: Commit**

```bash
git add -A
git commit -m "chore: remove security-domain individual files"
```

---

## Task 4: Rename package directories

**Files:**
- Rename: `hackbot_config/` → `vibeski_config/`
- Rename: `secbot_cli/` → `vibeski_cli/`

- [ ] **Step 4.1: Rename the Python package directories**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
mv hackbot_config vibeski_config
mv secbot_cli vibeski_cli
```

- [ ] **Step 4.2: Verify**

```bash
ls -d vibeski_config vibeski_cli
```

Expected: `vibeski_cli  vibeski_config`

- [ ] **Step 4.3: Commit**

```bash
git add -A
git commit -m "chore: rename hackbot_config→vibeski_config, secbot_cli→vibeski_cli"
```

---

## Task 5: Global identifier rename across all files

**Files:**
- Modify: every `.py`, `.ts`, `.tsx`, `.toml`, `.json` file containing `secbot`, `hackbot`, or `SECBOT_`

- [ ] **Step 5.1: Write the rename script**

```bash
mkdir -p /Users/lpb/workspace/github/agent/vibeski/scripts
```

Create `/Users/lpb/workspace/github/agent/vibeski/scripts/rename_identifiers.py`:

```python
"""One-time script: rename secbot/hackbot identifiers to vibeski."""
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent

REPLACEMENTS = [
    # Python packages (order matters — longer first)
    ("hackbot_config", "vibeski_config"),
    ("secbot_cli", "vibeski_cli"),
    # Database file
    ("secbot.db", "vibeski.db"),
    # Entry-point groups
    ("secbot.tools.basic", "vibeski.tools.basic"),
    ("secbot.tools.advanced", "vibeski.tools.advanced"),
    # Env vars (SECBOT_ prefix — do before generic secbot)
    ("SECBOT_TOOL_MODULES_ADVANCED", "VIBESKI_TOOL_MODULES_ADVANCED"),
    ("SECBOT_TOOL_MODULES", "VIBESKI_TOOL_MODULES"),
    ("SECBOT_API_URL", "VIBESKI_API_URL"),
    ("SECBOT_DESKTOP", "VIBESKI_DESKTOP"),
    ("SECBOT_SERVER_HOST", "VIBESKI_SERVER_HOST"),
    ("SECBOT_SERVER_PORT", "VIBESKI_SERVER_PORT"),
    ("SECBOT_SERVER_RELOAD", "VIBESKI_SERVER_RELOAD"),
    # Generic names
    ("secbot-terminal-ui", "vibeski-terminal-ui"),
    ("secbot-cli-server", "vibeski-server"),
    ("hackbot-server", "vibeski-server"),
    ("secbot-server", "vibeski-server"),
    ("secbot-cli", "vibeski"),
    ("hackbot", "vibeski"),
    ("secbot", "vibeski"),
    ("Hackbot", "Vibeski"),
    ("HackBot", "VibeSkiBot"),
    ("HACKBOT", "VIBESKI"),
    ("SECBOT", "VIBESKI"),
]

EXTENSIONS = {".py", ".ts", ".tsx", ".toml", ".json", ".md", ".sh", ".bat", ".ps1", ".txt"}
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".ruff_cache", "dist", "secbot.egg-info"}

changed = 0
for path in ROOT.rglob("*"):
    if path.is_dir():
        continue
    if any(skip in path.parts for skip in SKIP_DIRS):
        continue
    if path.suffix not in EXTENSIONS:
        continue
    if path.name == "rename_identifiers.py":
        continue

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    new_text = text
    for old, new in REPLACEMENTS:
        new_text = new_text.replace(old, new)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"  updated: {path.relative_to(ROOT)}")
        changed += 1

print(f"\nDone. {changed} files updated.")
```

- [ ] **Step 5.2: Run the rename script**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
python scripts/rename_identifiers.py
```

Expected: output listing updated files, ending with `Done. N files updated.`

- [ ] **Step 5.3: Verify key renames**

```bash
grep -r "hackbot_config\|secbot_cli\|SECBOT_API_URL\|SECBOT_DESKTOP\|SECBOT_SERVER" \
  --include="*.py" --include="*.ts" --include="*.toml" --include="*.json" \
  /Users/lpb/workspace/github/agent/vibeski/ | grep -v ".git" | grep -v "__pycache__"
```

Expected: **no output** (all renamed)

- [ ] **Step 5.4: Verify vibeski_config is imported correctly in main.py**

```bash
grep "vibeski_config\|vibeski_cli" /Users/lpb/workspace/github/agent/vibeski/main.py
```

Expected: lines containing `from vibeski_cli.launch_tui import ...`

- [ ] **Step 5.5: Commit**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
git add -A
git commit -m "chore: rename all secbot/hackbot identifiers to vibeski"
```

---

## Task 6: Strip database/models.py

**Files:**
- Modify: `vibeski/database/models.py`

- [ ] **Step 6.1: Write the test first**

```bash
cat > /Users/lpb/workspace/github/agent/vibeski/tests/test_database_models.py << 'EOF'
"""Verify database/models.py has no domain-specific models."""
import pytest


def test_domain_models_removed():
    """CrawlerTask, AttackTask, ScanResult must not exist in models."""
    import database.models as m
    assert not hasattr(m, "CrawlerTask"), "CrawlerTask should be removed"
    assert not hasattr(m, "AttackTask"), "AttackTask should be removed"
    assert not hasattr(m, "ScanResult"), "ScanResult should be removed"


def test_base_models_kept():
    """Conversation, PromptChainModel, UserConfig, AuditRecord must exist."""
    from database.models import Conversation, PromptChainModel, UserConfig, AuditRecord
    assert Conversation
    assert PromptChainModel
    assert UserConfig
    assert AuditRecord
EOF
```

- [ ] **Step 6.2: Run test — expect it to FAIL**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_database_models.py::test_domain_models_removed -v 2>&1 | tail -5
```

Expected: `FAILED` — CrawlerTask still exists

- [ ] **Step 6.3: Edit database/models.py — remove the three domain models**

Open `vibeski/database/models.py` and delete the `CrawlerTask`, `AttackTask`, and `ScanResult` classes entirely (lines ~42–90 in the original). The file should end after `AuditRecord`.

- [ ] **Step 6.4: Run tests — expect PASS**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_database_models.py -v 2>&1 | tail -5
```

Expected: `2 passed`

- [ ] **Step 6.5: Commit**

```bash
git add database/models.py tests/test_database_models.py
git commit -m "feat: strip domain models from database/models.py"
```

---

## Task 7: Strip database/manager.py

**Files:**
- Modify: `vibeski/database/manager.py`

- [ ] **Step 7.1: Write the test**

```bash
cat > /Users/lpb/workspace/github/agent/vibeski/tests/test_database_manager.py << 'EOF'
"""Verify DatabaseManager has no domain-specific tables or methods."""
import pytest
import tempfile
from pathlib import Path


def test_domain_methods_removed():
    from database.manager import DatabaseManager
    mgr = DatabaseManager()
    assert not hasattr(mgr, "save_crawler_task"), "save_crawler_task must be removed"
    assert not hasattr(mgr, "update_crawler_task"), "update_crawler_task must be removed"
    assert not hasattr(mgr, "get_crawler_tasks"), "get_crawler_tasks must be removed"


def test_domain_tables_not_created(tmp_path):
    from database.manager import DatabaseManager
    import sqlite3
    db_path = tmp_path / "test.db"
    mgr = DatabaseManager(db_path=db_path)
    conn = sqlite3.connect(str(db_path))
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    conn.close()
    assert "crawler_tasks" not in tables
    assert "attack_tasks" not in tables
    assert "scan_results" not in tables


def test_base_methods_kept():
    from database.manager import DatabaseManager
    mgr = DatabaseManager()
    assert hasattr(mgr, "save_conversation")
    assert hasattr(mgr, "get_conversations")
    assert hasattr(mgr, "save_config")
    assert hasattr(mgr, "get_stats")
EOF
```

- [ ] **Step 7.2: Run test — expect FAIL**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_database_manager.py::test_domain_methods_removed -v 2>&1 | tail -5
```

Expected: `FAILED`

- [ ] **Step 7.3: Edit database/manager.py**

Make these changes:

1. **Imports**: remove `CrawlerTask`, `AttackTask`, `ScanResult` from the import line at the top.

2. **`_init_database()`**: remove the three `CREATE TABLE` blocks for `crawler_tasks`, `attack_tasks`, `scan_results`, and their corresponding `CREATE INDEX` statements.

3. **Remove methods**: delete `save_crawler_task`, `update_crawler_task`, `get_crawler_tasks` (approx lines 517–616 in the source).

4. **`get_stats()`**: remove the two stat queries referencing `crawler_tasks`:
   ```python
   # DELETE these lines:
   cursor.execute("SELECT COUNT(*) as count FROM crawler_tasks")
   stats["crawler_tasks"] = cursor.fetchone()["count"]
   cursor.execute("SELECT status, COUNT(*) as count FROM crawler_tasks GROUP BY status")
   stats["crawler_tasks_by_status"] = {row["status"]: row["count"] for row in cursor.fetchall()}
   ```

- [ ] **Step 7.4: Run all database tests — expect PASS**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_database_models.py tests/test_database_manager.py -v 2>&1 | tail -8
```

Expected: `5 passed`

- [ ] **Step 7.5: Commit**

```bash
git add database/manager.py database/models.py tests/test_database_manager.py
git commit -m "feat: strip domain tables and CRUD from DatabaseManager"
```

---

## Task 8: Rewrite router/dependencies.py

**Files:**
- Modify: `vibeski/router/dependencies.py`

- [ ] **Step 8.1: Write the test**

```bash
cat > /Users/lpb/workspace/github/agent/vibeski/tests/test_dependencies.py << 'EOF'
"""Verify dependencies.py has no domain-specific imports."""


def test_no_domain_imports():
    """The module must import cleanly with no domain-specific symbols."""
    import router.dependencies as d
    # Must have these
    assert hasattr(d, "get_db_manager")
    assert hasattr(d, "get_prompt_manager")
    assert hasattr(d, "get_agent")
    assert hasattr(d, "get_session_id")
    # Must NOT have these
    assert not hasattr(d, "get_defense_manager")
    assert not hasattr(d, "get_main_controller")
    assert not hasattr(d, "get_os_controller")
    assert not hasattr(d, "get_os_detector")
    assert not hasattr(d, "get_agents")
EOF
```

- [ ] **Step 8.2: Run test — expect FAIL (ImportError from removed modules)**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_dependencies.py -v 2>&1 | tail -10
```

Expected: `ERROR` or `FAILED` due to import of removed `core.agents.*`

- [ ] **Step 8.3: Rewrite router/dependencies.py**

Replace the entire file content with:

```python
"""
Shared dependencies — singleton services for all routers.
"""

import uuid
from typing import Any, Optional

from database.manager import DatabaseManager
from prompts.manager import PromptManager

# Server-lifetime session ID
_session_id = str(uuid.uuid4())


class _Singletons:
    """Lazy-initialized singleton container."""

    _db_manager: Optional[DatabaseManager] = None
    _prompt_manager: Optional[PromptManager] = None

    @classmethod
    def db_manager(cls) -> DatabaseManager:
        if cls._db_manager is None:
            cls._db_manager = DatabaseManager()
        return cls._db_manager

    @classmethod
    def prompt_manager(cls) -> PromptManager:
        if cls._prompt_manager is None:
            cls._prompt_manager = PromptManager(db_manager=cls.db_manager())
        return cls._prompt_manager


def get_db_manager() -> DatabaseManager:
    return _Singletons.db_manager()


def get_prompt_manager() -> PromptManager:
    return _Singletons.prompt_manager()


def get_agent() -> Any:
    """
    Return the application's LangChain/LangGraph agent.

    TODO: Wire in your agent here. Example:
        from langchain.agents import create_react_agent
        from utils.model_selector import get_llm
        llm = get_llm()
        return create_react_agent(llm, tools=[...])
    """
    return None  # Replace with your agent implementation


def get_session_id() -> str:
    return _session_id
```

- [ ] **Step 8.4: Run test — expect PASS**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_dependencies.py -v 2>&1 | tail -5
```

Expected: `1 passed`

- [ ] **Step 8.5: Commit**

```bash
git add router/dependencies.py tests/test_dependencies.py
git commit -m "feat: rewrite router/dependencies.py — generic singletons only"
```

---

## Task 9: Rewrite core/session.py

**Files:**
- Modify: `vibeski/core/session.py`

- [ ] **Step 9.1: Write the test**

```bash
cat > /Users/lpb/workspace/github/agent/vibeski/tests/test_session.py << 'EOF'
"""Verify SessionManager is generic and has no domain agent imports."""
import pytest
import asyncio


def test_no_domain_agent_imports():
    """core.session must not import any removed agent classes."""
    import core.session as s
    assert not hasattr(s, "PlannerAgent")
    assert not hasattr(s, "QAAgent")
    assert not hasattr(s, "SummaryAgent")
    assert hasattr(s, "SessionManager")


def test_session_manager_init(tmp_path):
    """SessionManager can be instantiated with a DatabaseManager and EventBus."""
    from database.manager import DatabaseManager
    from utils.event_bus import EventBus
    from core.session import SessionManager

    db = DatabaseManager(db_path=tmp_path / "test.db")
    bus = EventBus()
    sm = SessionManager(db_manager=db, event_bus=bus)
    assert sm.session_id is not None
    session = sm.get_session()
    assert session is not None
EOF
```

- [ ] **Step 9.2: Run test — expect FAIL**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_session.py -v 2>&1 | tail -10
```

Expected: `FAILED` or `ERROR` (imports domain agents)

- [ ] **Step 9.3: Rewrite core/session.py**

Replace the entire file with:

```python
"""
SessionManager: Generic session lifecycle manager.

Manages session create/load and event dispatch.
Accepts any LangChain-compatible agent via process().
No domain-specific agent imports.
"""

import uuid
from datetime import datetime
from typing import Any, Optional

from core.models import Session
from database.manager import DatabaseManager
from database.models import Conversation
from utils.event_bus import EventBus, EventType
from utils.logger import logger


class SessionManager:
    """
    Generic session manager.

    Responsibilities:
    - Create / load sessions identified by session_id
    - Dispatch events to EventBus during response generation
    - Persist conversations to DatabaseManager

    Usage:
        sm = SessionManager(db_manager=db, event_bus=bus)
        result = await sm.process(user_input="hello", agent=my_agent)
    """

    def __init__(
        self,
        db_manager: DatabaseManager,
        event_bus: EventBus,
        session_id: Optional[str] = None,
    ) -> None:
        self.db_manager = db_manager
        self.event_bus = event_bus
        self.session_id = session_id or str(uuid.uuid4())
        self._session: Optional[Session] = None

    def get_session(self) -> Session:
        """Return current session, creating it if it does not exist."""
        if self._session is None:
            self._session = Session(id=self.session_id, agent_type="vibeski")
        return self._session

    async def process(
        self,
        user_input: str,
        agent: Any,
        agent_type: str = "vibeski",
    ) -> str:
        """
        Pass user_input to agent, persist the conversation, return the response.

        agent must implement:
            await agent.ainvoke({"input": str}) -> dict | str

        Emits EventBus events: EXEC_START, EXEC_RESULT, ERROR.
        """
        self.event_bus.emit_simple(EventType.EXEC_START, session_id=self.session_id)
        try:
            response = await agent.ainvoke({"input": user_input})
            if isinstance(response, dict):
                output = response.get("output", str(response))
            else:
                output = str(response)

            self.db_manager.save_conversation(
                Conversation(
                    agent_type=agent_type,
                    user_message=user_input,
                    assistant_message=output,
                    session_id=self.session_id,
                    timestamp=datetime.now(),
                )
            )

            self.event_bus.emit_simple(EventType.EXEC_RESULT, result=output)
            return output

        except Exception as exc:
            logger.error(f"SessionManager [{self.session_id}] error: {exc}")
            self.event_bus.emit_simple(EventType.ERROR, error=str(exc))
            raise
```

- [ ] **Step 9.4: Run tests — expect PASS**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_session.py -v 2>&1 | tail -5
```

Expected: `2 passed`

- [ ] **Step 9.5: Commit**

```bash
git add core/session.py tests/test_session.py
git commit -m "feat: rewrite core/session.py — generic SessionManager"
```

---

## Task 10: Create tools/web_search_tool.py (merged)

**Files:**
- Create: `vibeski/tools/web_search_tool.py`
- Delete: `vibeski/tools/web_search.py` (thin wrapper — already deleted in Task 3)

- [ ] **Step 10.1: Write the test**

```bash
cat > /Users/lpb/workspace/github/agent/vibeski/tests/test_tools.py << 'EOF'
"""Verify example tools load from the registry."""


def test_web_search_tool_importable():
    """web_search_tool.py must exist and export a search function."""
    from tools.web_search_tool import search
    import asyncio
    import inspect
    assert inspect.iscoroutinefunction(search)


def test_system_tool_importable():
    """system_tool.py must be importable."""
    import tools.system_tool as st
    assert st is not None


def test_page_extract_tool_importable():
    """web_research/page_extract_tool.py must be importable."""
    import tools.web_research.page_extract_tool as pet
    assert pet is not None
EOF
```

- [ ] **Step 10.2: Run test — expect FAIL (web_search_tool.py does not exist)**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_tools.py::test_web_search_tool_importable -v 2>&1 | tail -5
```

Expected: `FAILED` — ModuleNotFoundError

- [ ] **Step 10.3: Create tools/web_search_tool.py**

```python
"""
Web search tool — DuckDuckGo search with fallback.

Merges the search client (formerly web_search_ddgs.py) with the tool wrapper.
Supports: ddgs (preferred), duckduckgo-search (compat), HTML fallback.
"""
import asyncio
import re
from typing import List, Tuple
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from utils.logger import logger


def _normalize_result(r: dict) -> dict:
    return {
        "title": r.get("title", ""),
        "url": r.get("href", r.get("link", r.get("url", ""))),
        "snippet": r.get("body", r.get("snippet", "")),
    }


def _search_ddgs_sync(query: str, max_results: int) -> List[dict]:
    from ddgs import DDGS
    return [_normalize_result(r) for r in DDGS().text(query, max_results=max_results)]


def _search_duckduckgo_search_sync(query: str, max_results: int) -> List[dict]:
    from duckduckgo_search import DDGS
    with DDGS() as ddgs:
        return [_normalize_result(r) for r in ddgs.text(query, max_results=max_results)]


def _search_html_sync(query: str, max_results: int) -> List[dict]:
    url = f"https://lite.duckduckgo.com/lite/?q={quote_plus(query)}"
    req = Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; Vibeski/1.0)")
    with urlopen(req, timeout=15) as resp:
        html = resp.read().decode(errors="ignore")
    results = []
    links = re.findall(r'<a[^>]+rel="nofollow"[^>]+href="([^"]+)"[^>]*>(.+?)</a>', html, re.DOTALL)
    snippets = re.findall(r'<td[^>]*class="result-snippet"[^>]*>(.+?)</td>', html, re.DOTALL)
    for i, (link_url, title) in enumerate(links[:max_results]):
        if link_url.startswith("http"):
            results.append({
                "title": re.sub(r"<[^>]+>", "", title).strip(),
                "url": link_url,
                "snippet": re.sub(r"<[^>]+>", "", snippets[i]).strip() if i < len(snippets) else "",
            })
    return results


async def search(query: str, max_results: int = 5) -> Tuple[List[dict], str]:
    """
    Search DuckDuckGo. Returns (results, engine).
    results: [{title, url, snippet}, ...]
    engine: "ddgs" | "duckduckgo_search" | "duckduckgo_lite"
    """
    loop = asyncio.get_event_loop()
    for fn, engine in [
        (_search_ddgs_sync, "ddgs"),
        (_search_duckduckgo_search_sync, "duckduckgo_search"),
    ]:
        try:
            raw = await loop.run_in_executor(None, fn, query, max_results)
            if raw:
                return raw, engine
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"Web search [{engine}] failed: {e}")
    raw = await loop.run_in_executor(None, _search_html_sync, query, max_results)
    return raw, "duckduckgo_lite"


TOOLS = []  # Register with registry if desired
```

- [ ] **Step 10.4: Run all tool tests — expect PASS**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_tools.py -v 2>&1 | tail -8
```

Expected: `3 passed`

- [ ] **Step 10.5: Commit**

```bash
git add tools/web_search_tool.py tests/test_tools.py
git commit -m "feat: add web_search_tool.py (merged from two source files)"
```

---

## Task 11: Update tools/registry.py entry-point group names

**Files:**
- Modify: `vibeski/tools/registry.py`

The global rename in Task 5 handles `secbot.tools.basic` → `vibeski.tools.basic` and the env var renames. Verify it was applied.

- [ ] **Step 11.1: Verify the rename happened**

```bash
grep "ENTRY_POINT\|ENV_TOOL" /Users/lpb/workspace/github/agent/vibeski/tools/registry.py
```

Expected:
```
ENTRY_POINT_BASIC = "vibeski.tools.basic"
ENTRY_POINT_ADVANCED = "vibeski.tools.advanced"
ENV_TOOL_MODULES = "VIBESKI_TOOL_MODULES"
ENV_TOOL_MODULES_ADVANCED = "VIBESKI_TOOL_MODULES_ADVANCED"
```

- [ ] **Step 11.2: If not renamed correctly, fix manually**

```python
# In tools/registry.py, set:
ENTRY_POINT_BASIC = "vibeski.tools.basic"
ENTRY_POINT_ADVANCED = "vibeski.tools.advanced"
ENV_TOOL_MODULES = "VIBESKI_TOOL_MODULES"
ENV_TOOL_MODULES_ADVANCED = "VIBESKI_TOOL_MODULES_ADVANCED"
```

- [ ] **Step 11.3: Test registry imports cleanly**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run python -c "from tools.registry import ENTRY_POINT_BASIC, ENTRY_POINT_ADVANCED; print(ENTRY_POINT_BASIC, ENTRY_POINT_ADVANCED)"
```

Expected: `vibeski.tools.basic vibeski.tools.advanced`

- [ ] **Step 11.4: Commit if changed**

```bash
git add tools/registry.py
git commit -m "fix: update tools/registry.py entry-point group names to vibeski.*" || echo "Nothing to commit"
```

---

## Task 12: Update pyproject.toml

**Files:**
- Modify: `vibeski/pyproject.toml`

- [ ] **Step 12.1: Verify the global rename updated pyproject.toml**

```bash
grep "name\|scripts\|entry-points\|version\|description" /Users/lpb/workspace/github/agent/vibeski/pyproject.toml | head -20
```

Expected: `name = "vibeski"`, CLI entries `vibeski = ...` and `vibeski-server = ...`

- [ ] **Step 12.2: Remove leftover secbot package entries from [tool.setuptools]**

Open `pyproject.toml` and update the `[tool.setuptools] packages` list. Replace `secbot_cli` with `vibeski_cli` and `hackbot_config` (was renamed in Task 5 global rename) with `vibeski_config`. Also:
- Remove all security-domain package entries: `scanner`, `defense`, `payloads`, `crawler`, `controller`, `core.agents`, `core.attack_chain`, `core.patterns`, `core.vuln_db`, all `tools.pentest.*`, `tools.offense.*`, `tools.osint`, `tools.web`, `tools.cloud`, `tools.protocol`, `tools.reporting`

The kept packages list should be:
```toml
[tool.setuptools]
packages = [
    "vibeski_cli",
    "core",
    "core.memory",
    "skills",
    "vibeski_config",
    "database",
    "prompts",
    "tools",
    "tools.web_research",
    "utils",
    "router",
]
```

- [ ] **Step 12.3: Add vibeski entry-point declarations**

Add or verify this section exists:
```toml
[project.entry-points."vibeski.tools.basic"]
vibeski_system = "tools.system_tool:TOOLS"
vibeski_web_search = "tools.web_search_tool:TOOLS"

[project.entry-points."vibeski.tools.advanced"]
vibeski_page_extract = "tools.web_research.page_extract_tool:TOOLS"
```

- [ ] **Step 12.4: Verify pyproject.toml is valid**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv sync
```

Expected: `Resolved N packages` or `All requirements already satisfied`

- [ ] **Step 12.5: Commit**

```bash
git add pyproject.toml
git commit -m "chore: update pyproject.toml packages list and entry-points for vibeski"
```

---

## Task 13: Update router/main.py — remove domain routers

**Files:**
- Modify: `vibeski/router/main.py`

- [ ] **Step 13.1: Verify domain router imports were removed by rename or fix manually**

```bash
grep "defense_router\|network_router\|agents_router" /Users/lpb/workspace/github/agent/vibeski/router/main.py
```

If any lines show — remove them. The kept routers are: `chat`, `agents` (generic, if kept), `sessions`, `system`, `defense` is removed, `network` is removed, `database`, `tools`.

Actually, check which routers remain:

```bash
ls /Users/lpb/workspace/github/agent/vibeski/router/
```

Expected: `__init__.py  chat.py  database.py  dependencies.py  main.py  schemas.py  sessions.py  system.py  tools.py`

- [ ] **Step 13.2: Edit router/main.py to remove references to deleted routers**

Open `router/main.py` and remove:
- `from router.defense import router as defense_router`
- `from router.network import router as network_router`
- `from router.agents import router as agents_router`
- `application.include_router(defense_router)`
- `application.include_router(network_router)`
- `application.include_router(agents_router)`

Also update the app title/description:
```python
application = FastAPI(
    title="Vibeski API",
    description="Vibeski — Full-stack AI agent base app",
    version="1.0.0",
    ...
)
```

- [ ] **Step 13.3: Test that FastAPI app creates without error**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run python -c "from router.main import app; print('App created:', app.title)"
```

Expected: `App created: Vibeski API`

- [ ] **Step 13.4: Commit**

```bash
git add router/main.py
git commit -m "feat: remove domain routers from router/main.py"
```

---

## Task 13b: Fix broken imports in router/chat.py and router/tools.py

These two routers import from deleted modules and must be fixed before the backend can start.

**Files:**
- Modify: `vibeski/router/chat.py` — remove `save_root_policy` import and `root_response` endpoint
- Modify: `vibeski/router/tools.py` — rewrite to list only the 3 example tools

- [ ] **Step 13b.1: Fix router/chat.py — remove root_policy usage**

In `router/chat.py`:
1. Remove: `from utils.root_policy import save_root_policy`
2. Remove: `from router.schemas import ... RootResponseRequest` (remove only `RootResponseRequest` from the import)
3. Remove the entire `root_response` endpoint (the `async def root_response(...)` function, ~lines 293–305)
4. Remove the `EventType.ROOT_REQUIRED` handling blocks inside the SSE generator (the `if t == EventType.ROOT_REQUIRED:` branches)

Verify the file compiles after editing:
```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run python -c "import router.chat; print('chat OK')"
```
Expected: `chat OK`

- [ ] **Step 13b.2: Rewrite router/tools.py to list example tools only**

Replace the entire `router/tools.py` with:

```python
"""
Tools router — list vibeski example tools.
"""

from fastapi import APIRouter

from tools.system_tool import TOOLS as SYSTEM_TOOLS
from tools.web_search_tool import TOOLS as WEB_SEARCH_TOOLS
from tools.web_research.page_extract_tool import TOOLS as PAGE_EXTRACT_TOOLS

router = APIRouter(prefix="/api/tools", tags=["Tools"])

_CATEGORIES = [
    ("system", "System Info", SYSTEM_TOOLS),
    ("web_search", "Web Search", WEB_SEARCH_TOOLS),
    ("web_research", "Web Research", PAGE_EXTRACT_TOOLS),
]


@router.get("", summary="List available tools")
async def list_tools():
    """Return all registered vibeski tools grouped by category."""
    categories_out = []
    tools_flat = []

    for cat_id, cat_name, tool_list in _CATEGORIES:
        items = [
            {"name": getattr(t, "name", str(t)), "description": getattr(t, "description", "")}
            for t in tool_list
        ]
        categories_out.append({
            "id": cat_id,
            "name": cat_name,
            "count": len(items),
            "tools": items,
        })
        tools_flat.extend([{**item, "category": cat_name} for item in items])

    return {
        "total": len(tools_flat),
        "categories": categories_out,
        "tools": tools_flat,
    }
```

Note: `TOOLS = []` in each example tool file means the lists will be empty until tools are registered. That's correct for a base app — the route works without crashing.

- [ ] **Step 13b.3: Verify both routers import cleanly**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run python -c "import router.chat; import router.tools; print('Both routers OK')"
```

Expected: `Both routers OK`

- [ ] **Step 13b.4: Commit**

```bash
git add router/chat.py router/tools.py
git commit -m "fix: remove domain imports from router/chat.py and router/tools.py"
```

---

## Task 14: Create .env.example

**Files:**
- Create: `vibeski/.env.example`

- [ ] **Step 14.1: Create .env.example**

Create `/Users/lpb/workspace/github/agent/vibeski/.env.example` with:

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

- [ ] **Step 14.2: Verify it is not gitignored (must be tracked)**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
git check-ignore -v .env.example
```

Expected: **no output** (not ignored — it should be committed)

If gitignored, open `.gitignore` and remove or scope the `.env*` rule to `.env` only (not `.env.example`).

- [ ] **Step 14.3: Commit**

```bash
git add .env.example
git commit -m "chore: add .env.example with minimum required config keys"
```

---

## Task 15: Update terminal-ui API URL env var

**Files:**
- Modify: `vibeski/terminal-ui/src/api.ts`
- Modify: `vibeski/terminal-ui/src/config.ts` (if it references SECBOT_API_URL)
- Verify: `vibeski/terminal-ui/package.json` name field

The global rename in Task 5 should have handled `SECBOT_API_URL` → `VIBESKI_API_URL`. This task verifies and fixes any misses.

- [ ] **Step 15.1: Verify terminal-ui references**

```bash
grep -r "SECBOT\|secbot\|hackbot" /Users/lpb/workspace/github/agent/vibeski/terminal-ui/ 2>/dev/null | grep -v node_modules
```

Expected: **no output**

- [ ] **Step 15.2: Verify package.json name**

```bash
grep '"name"' /Users/lpb/workspace/github/agent/vibeski/terminal-ui/package.json
```

Expected: `"name": "vibeski-terminal-ui"`

- [ ] **Step 15.3: If any renames were missed, fix and commit**

```bash
# If there were misses:
git add terminal-ui/
git commit -m "fix: rename remaining SECBOT_ references in terminal-ui" || echo "Nothing to commit"
```

---

## Task 16: Create docs/QUICKSTART.md

**Files:**
- Create: `vibeski/docs/QUICKSTART.md`

- [ ] **Step 16.1: Create QUICKSTART.md**

```markdown
# Vibeski Quick Start

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (`pip install uv`)
- Node.js 18+ and npm

## 1. Clone and configure

```bash
git clone https://github.com/you/vibeski
cd vibeski
cp .env.example .env
# Edit .env: set LLM_PROVIDER and add your API key
```

## 2. Install dependencies

```bash
uv sync
cd terminal-ui && npm install && cd ..
```

## 3. Run

```bash
python main.py            # backend (port 8000) + Ink TUI
```

Or separately:

```bash
python main.py --backend  # backend only
python main.py --tui      # TUI only (backend must be running)
```

API docs: http://localhost:8000/docs

## Mobile (Expo)

```bash
cd app && npm install && npx expo start
```

## Desktop (Tauri — requires Rust)

```bash
# Install Rust: https://rustup.rs
cd desktop && npm install && npm run tauri dev
```

## Adding your own tools

1. Create a class inheriting `tools.base.BaseTool`
2. Declare it in `pyproject.toml`:
   ```toml
   [project.entry-points."vibeski.tools.basic"]
   my_tools = "mypackage.tools:MY_TOOLS"
   ```
3. Run `uv sync` — tools are auto-discovered on next start
```

- [ ] **Step 16.2: Commit**

```bash
git add docs/QUICKSTART.md
git commit -m "docs: add QUICKSTART.md"
```

---

## Task 17: Smoke test — backend starts and health check passes

**Files:**
- Create: `vibeski/tests/test_smoke.py`

- [ ] **Step 17.1: Write smoke tests**

```bash
cat > /Users/lpb/workspace/github/agent/vibeski/tests/test_smoke.py << 'EOF'
"""Smoke tests: verify vibeski imports cleanly and FastAPI app creates."""
import pytest


def test_vibeski_config_imports():
    """vibeski_config must import without error."""
    from vibeski_config import settings
    assert settings is not None
    assert settings.database_url.startswith("sqlite")


def test_router_app_creates():
    """FastAPI app must create without error."""
    from router.main import app
    assert app.title == "Vibeski API"


def test_health_endpoint():
    """Health check endpoint must return 200."""
    from fastapi.testclient import TestClient
    from router.main import app
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_tools_importable():
    """All example tools must import cleanly."""
    import tools.system_tool
    import tools.web_search_tool
    import tools.web_research.page_extract_tool


def test_database_manager_creates(tmp_path):
    """DatabaseManager must initialize and create tables."""
    from database.manager import DatabaseManager
    db = DatabaseManager(db_path=tmp_path / "smoke.db")
    stats = db.get_stats()
    assert "conversations" in stats
    assert "crawler_tasks" not in stats
EOF
```

- [ ] **Step 17.2: Run smoke tests**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/test_smoke.py -v 2>&1
```

Expected: `5 passed`

If `test_health_endpoint` fails due to remaining broken imports in routers, trace the import error and fix the specific file.

- [ ] **Step 17.3: Run all tests**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv run pytest tests/ -v 2>&1 | tail -15
```

Expected: All tests pass (no failures).

- [ ] **Step 17.4: Commit**

```bash
git add tests/test_smoke.py
git commit -m "test: add smoke tests — all pass"
```

---

## Task 18: Final cleanup

- [ ] **Step 18.1: Remove the rename script (one-time use)**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
rm scripts/rename_identifiers.py
rmdir scripts 2>/dev/null || true
```

- [ ] **Step 18.2: Check for any leftover `secbot`/`hackbot` references in Python files**

```bash
grep -rn "hackbot\|secbot\|Hackbot\|Secbot" \
  /Users/lpb/workspace/github/agent/vibeski/ \
  --include="*.py" --include="*.toml" \
  | grep -v ".git" | grep -v "__pycache__" | grep -v "test_" | grep -v ".egg-info"
```

Fix any remaining references found.

- [ ] **Step 18.3: Verify uv.lock is consistent**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
uv lock
```

Expected: no errors

- [ ] **Step 18.4: Final commit**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
git add -A
git commit -m "chore: final cleanup — vibeski base app ready"
```

- [ ] **Step 18.5: Tag v1.0.0**

```bash
cd /Users/lpb/workspace/github/agent/vibeski
git tag v1.0.0
```

---

## Verification Checklist

After all tasks complete, verify:

```bash
cd /Users/lpb/workspace/github/agent/vibeski

# 1. All tests pass
uv run pytest tests/ -v

# 2. Backend starts (Ctrl+C to stop)
uv run python main.py --backend &
sleep 5
curl http://localhost:8000/health
kill %1

# 3. No broken imports
uv run python -c "
from vibeski_config import settings
from router.main import app
from core.session import SessionManager
from database.manager import DatabaseManager
from tools.registry import ENTRY_POINT_BASIC
print('All imports OK')
print('LLM provider:', settings.llm_provider)
print('DB:', settings.database_url)
print('Tools group:', ENTRY_POINT_BASIC)
"
```

Expected output:
```
All imports OK
LLM provider: ollama (or whatever .env says)
DB: sqlite:///./data/vibeski.db
Tools group: vibeski.tools.basic
```
