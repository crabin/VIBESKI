"""
Chat router — SSE streaming interface using SessionManager.
"""

import asyncio
import json
import traceback
import uuid
from typing import Any, AsyncGenerator

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from router.dependencies import get_agent
from router.schemas import ChatRequest, ChatResponse
from core.session import SessionManager
from database.manager import DatabaseManager
from utils.event_bus import EventBus, EventType, Event
from utils.logger import logger

router = APIRouter(prefix="/api/chat", tags=["Chat"])


def _event_to_sse(event: Event) -> tuple[str, dict] | None:
    """Map EventBus events to SSE (event_name, data)."""
    t, d = event.type, event.data
    if t == EventType.EXEC_START:
        return ("action_start", {"detail": d.get("detail", "")})
    if t == EventType.EXEC_RESULT:
        return ("action_result", {"result": d.get("result", "")})
    if t == EventType.ERROR:
        return ("error", {"error": d.get("error", "")})
    return None


async def _sse_generator(request: ChatRequest) -> AsyncGenerator[dict, None]:
    """SSE event generator for chat."""
    yield {
        "event": "connected",
        "data": json.dumps({"message": "stream started"}, ensure_ascii=False),
    }

    queue: asyncio.Queue = asyncio.Queue()
    request_id = str(uuid.uuid4())[:8]
    event_bus = EventBus()

    def on_bus_event(event: Event):
        mapped = _event_to_sse(event)
        if mapped:
            sse_name, sse_data = mapped
            queue.put_nowait({"event": sse_name, "data": sse_data})

    for et in (EventType.EXEC_START, EventType.EXEC_RESULT, EventType.ERROR):
        event_bus.subscribe(et, on_bus_event)

    db_manager = DatabaseManager()
    session_manager = SessionManager(db_manager=db_manager, event_bus=event_bus)

    final_response: list[str] = []

    async def _run():
        try:
            agent = get_agent()
            if agent is None:
                response = "No agent configured. Please implement get_agent() in router/dependencies.py."
            else:
                response = await session_manager.process(request.message, agent=agent)
            final_response.append(response)
        except Exception as e:
            queue.put_nowait({
                "event": "error",
                "data": {"error": str(e), "traceback": traceback.format_exc()},
            })
        finally:
            if final_response:
                queue.put_nowait({
                    "event": "response",
                    "data": {"content": final_response[0]},
                })
            queue.put_nowait({"event": "done", "data": {}})

    task = asyncio.create_task(_run())

    try:
        while True:
            item = await queue.get()
            yield {
                "event": item["event"],
                "data": json.dumps(item["data"], ensure_ascii=False),
            }
            if item["event"] == "done":
                break
    finally:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


@router.post("", summary="Streaming chat (SSE)")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint using SessionManager.
    Returns text/event-stream with SSE events.
    """
    return EventSourceResponse(_sse_generator(request))


@router.post("/sync", response_model=ChatResponse, summary="Sync chat")
async def chat_sync(request: ChatRequest):
    """
    Synchronous chat endpoint.
    """
    try:
        agent = get_agent()
        if agent is None:
            return ChatResponse(response="No agent configured.", agent="none")

        db_manager = DatabaseManager()
        event_bus = EventBus()
        session_manager = SessionManager(db_manager=db_manager, event_bus=event_bus)
        response = await session_manager.process(request.message, agent=agent)
        return ChatResponse(response=response, agent="vibeski")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {e}")
