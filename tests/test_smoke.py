"""Smoke tests: verify vibeski imports cleanly and FastAPI app creates."""
import pytest
import tempfile
from pathlib import Path


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
