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
