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
        self.session_id = session_id or str(uuid.uuid4())[:8]
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
