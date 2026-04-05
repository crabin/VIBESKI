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
