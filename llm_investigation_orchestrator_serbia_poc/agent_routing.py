"""Thread-safe agent routing and Moshe mission continuity for shared chat requests."""

from __future__ import annotations

import re
import secrets
import threading
from dataclasses import dataclass


MOSHE_AGENT_ID = "moshe"
GENERAL_AGENT_ID = "general"
MOSHE_MENTION = re.compile(r"(?<![\w\u0590-\u05ff])@משה(?![\w\u0590-\u05ff])")


@dataclass(frozen=True)
class RouteDecision:
    responding_agent: str
    conversation_id: str
    mission_run_id: str | None
    hermes_session_id: str | None
    mission_started: bool
    mission_closed: bool


@dataclass
class _ConversationRoute:
    last_agent: str = GENERAL_AGENT_ID
    mission_run_id: str | None = None
    hermes_session_id: str | None = None


def mentions_moshe(message: str) -> bool:
    """Route only an exact current-message mention; history is never inspected."""
    return bool(MOSHE_MENTION.search(str(message or "")))


class AgentRouteRegistry:
    def __init__(self) -> None:
        self._routes: dict[str, _ConversationRoute] = {}
        self._lock = threading.RLock()

    @staticmethod
    def _conversation_id(value: str | None) -> str:
        normalized = re.sub(r"[^A-Za-z0-9_.:-]+", "-", str(value or "")).strip("-")
        if not normalized:
            raise ValueError("conversation_id is required for agent routing")
        return normalized

    @staticmethod
    def _new_mission_id(conversation_id: str) -> str:
        return f"moshe-mission-{conversation_id}-{secrets.token_hex(6)}"

    def route(self, conversation_id: str, current_message: str) -> RouteDecision:
        key = self._conversation_id(conversation_id)
        with self._lock:
            current = self._routes.setdefault(key, _ConversationRoute())
            if mentions_moshe(current_message):
                started = current.last_agent != MOSHE_AGENT_ID or not current.mission_run_id
                if started:
                    current.mission_run_id = self._new_mission_id(key)
                    current.hermes_session_id = None
                current.last_agent = MOSHE_AGENT_ID
                return RouteDecision(
                    MOSHE_AGENT_ID, key, current.mission_run_id, current.hermes_session_id,
                    mission_started=started, mission_closed=False,
                )
            closed = current.last_agent == MOSHE_AGENT_ID and bool(current.mission_run_id)
            current.last_agent = GENERAL_AGENT_ID
            current.mission_run_id = None
            current.hermes_session_id = None
            return RouteDecision(
                GENERAL_AGENT_ID, key, None, None,
                mission_started=False, mission_closed=closed,
            )

    def bind_hermes_session(self, conversation_id: str, mission_run_id: str, hermes_session_id: str) -> None:
        key = self._conversation_id(conversation_id)
        session = str(hermes_session_id or "").strip()
        if not session:
            raise ValueError("hermes_session_id is required")
        with self._lock:
            current = self._routes.get(key)
            if current is None or current.last_agent != MOSHE_AGENT_ID or current.mission_run_id != mission_run_id:
                raise ValueError("Moshe mission is no longer active")
            current.hermes_session_id = session

    def clear(self, conversation_id: str) -> None:
        key = self._conversation_id(conversation_id)
        with self._lock:
            self._routes.pop(key, None)
