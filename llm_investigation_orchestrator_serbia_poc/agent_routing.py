"""Thread-safe specialist routing and mission continuity for shared chat requests."""

from __future__ import annotations

import hashlib
import re
import secrets
import threading
from dataclasses import dataclass


MOSHE_AGENT_ID = "moshe"
TALIA_AGENT_ID = "talia"
GENERAL_AGENT_ID = "general"
OPENAI_GENERAL_AGENT_ID = "openai_general"
MOSHE_MENTION = re.compile(r"(?<![\w\u0590-\u05ff])@(משה|Moshe)(?![\w\u0590-\u05ff])", re.IGNORECASE)
TALIA_MENTION = re.compile(r"(?<![\w\u0590-\u05ff])@(טליה|Talia)(?![\w\u0590-\u05ff])", re.IGNORECASE)
OPENAI_GENERAL_MENTION = re.compile(r"(?<![\w\u0590-\u05ff])@(OpenAI|אופן\s?איי)(?![\w\u0590-\u05ff])", re.IGNORECASE)


@dataclass(frozen=True)
class RouteDecision:
    responding_agent: str
    conversation_id: str
    mission_run_id: str | None
    hermes_session_id: str | None
    openai_session_id: str | None
    mission_started: bool
    mission_closed: bool


@dataclass
class _ConversationRoute:
    last_agent: str = GENERAL_AGENT_ID
    mission_run_id: str | None = None
    hermes_session_id: str | None = None
    openai_session_id: str | None = None


def mentions_moshe(message: str) -> bool:
    """Route only an exact current-message mention; history is never inspected."""
    return bool(MOSHE_MENTION.search(str(message or "")))


def mentions_talia(message: str) -> bool:
    """Route only an exact current-message mention; history is never inspected."""
    return bool(TALIA_MENTION.search(str(message or "")))


def mentions_openai_general(message: str) -> bool:
    """Select the additive experimental General agent with an exact mention."""
    return bool(OPENAI_GENERAL_MENTION.search(str(message or "")))


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
    def _new_mission_id(conversation_id: str, agent_id: str) -> str:
        conversation_hash = hashlib.sha256(conversation_id.encode("utf-8")).hexdigest()[:16]
        return f"{agent_id}-{conversation_hash}-{secrets.token_hex(6)}"

    def route(self, conversation_id: str, current_message: str) -> RouteDecision:
        key = self._conversation_id(conversation_id)
        with self._lock:
            current = self._routes.setdefault(key, _ConversationRoute())
            requested_agent = (
                MOSHE_AGENT_ID if mentions_moshe(current_message)
                else TALIA_AGENT_ID if mentions_talia(current_message)
                else OPENAI_GENERAL_AGENT_ID if mentions_openai_general(current_message)
                else GENERAL_AGENT_ID
            )
            if requested_agent in {MOSHE_AGENT_ID, TALIA_AGENT_ID}:
                started = current.last_agent != requested_agent or not current.mission_run_id
                if started:
                    current.mission_run_id = self._new_mission_id(key, requested_agent)
                    current.hermes_session_id = None
                current.last_agent = requested_agent
                return RouteDecision(
                    requested_agent, key, current.mission_run_id, current.hermes_session_id, current.openai_session_id,
                    mission_started=started, mission_closed=False,
                )
            # Both General agents are stateless from the routing perspective. They
            # deliberately close a specialist mission but never create one themselves.
            closed = current.last_agent in {MOSHE_AGENT_ID, TALIA_AGENT_ID} and bool(current.mission_run_id)
            current.last_agent = requested_agent
            current.mission_run_id = None
            current.hermes_session_id = None
            return RouteDecision(
                requested_agent, key, None, None, current.openai_session_id,
                mission_started=False, mission_closed=closed,
            )

    def bind_hermes_session(self, conversation_id: str, mission_run_id: str, hermes_session_id: str) -> None:
        key = self._conversation_id(conversation_id)
        session = str(hermes_session_id or "").strip()
        if not session:
            raise ValueError("hermes_session_id is required")
        with self._lock:
            current = self._routes.get(key)
            if current is None or current.last_agent == GENERAL_AGENT_ID or current.mission_run_id != mission_run_id:
                raise ValueError("Specialist mission is no longer active")
            current.hermes_session_id = session

    def bind_openai_session(self, conversation_id: str, openai_session_id: str) -> None:
        key = self._conversation_id(conversation_id)
        session = str(openai_session_id or "").strip()
        if not session:
            raise ValueError("openai_session_id is required")
        with self._lock:
            current = self._routes.setdefault(key, _ConversationRoute())
            current.openai_session_id = session

    def clear(self, conversation_id: str) -> None:
        key = self._conversation_id(conversation_id)
        with self._lock:
            self._routes.pop(key, None)
