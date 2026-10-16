"""The chat: i360's chat service answers questions, a small tool loop over HL API drives the app.

One user message is one turn (``ChatTurn.run``):

1. The message and what the app shows go to the model behind HL API ``POST /api/v1/llm/chat``
   with six tools. The model keeps no history of its own: the conversation is i360's. The model returns tool calls; HL API never runs them.
2. ``ask_i360`` sends a question to the i360 chat service (``analytics/i360-chat``, ``POST /chat/ask``,
   the user's own bearer). Its answer stream is relayed to the browser as it arrives, and the model
   gets back the answer text and the ids of the items it cited.
3. The app tools (``show_items``, ``open_layer``, ``open_item``, ``save_to_memory``) are
   checked here and sent to the browser as actions; the browser carries them out. ``save_to_memory``
   is only a proposal: the browser asks the user to confirm before anything is written.
4. The model's last text is the turn's closing note.

If the model cannot be reached, the turn falls back to asking i360 directly and showing what it cited.
Everything travels with the user's token; nothing is kept between turns on the server. The i360 chat
service holds the conversation (records on the platform); the browser only sends its conversation id,
its recent answer ids and the previous answer's cited items.
"""
from __future__ import annotations

import copy
import json
import re
import socket
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator, Protocol

from catalog_filters import resolve_layer, validate_filters
from hl.client import AuthExpired, HlClient, HlError, NotOnThisEstate, Unreachable

MAX_ROUNDS = 6
MAX_SHOWN_ITEMS = 200
MAX_CITED_FOR_MODEL = 25  # the model sees these; every cited id is still shown
# Questions i360 routes to its search leg (an investigation focus keeps them inside), tried in turn.
OVERVIEW_LISTING_QUESTIONS = ("find all items", "search all items", "find all records")
VIEWS = ("map", "timeline", "table")


class ClientGone(Exception):
    """The browser closed the answer stream: stop the turn and its upstream requests."""


# --------------------------------------------------------------------------------------------
# i360 chat service (analytics/i360-chat)
# --------------------------------------------------------------------------------------------
def parse_sse(lines: Iterator[bytes]) -> Iterator[tuple[str, Any]]:
    """``event: x`` / ``data: {...}`` blocks -> (event, data). Comments and keep-alives are skipped."""
    event, data = "", []
    for raw in lines:
        line = raw.decode("utf-8", "replace").rstrip("\r\n")
        if not line:
            if event:
                text = "\n".join(data)
                try:
                    value = json.loads(text) if text else None
                except json.JSONDecodeError:
                    value = None
                yield event, value
            event, data = "", []
        elif line.startswith(":"):
            continue
        elif line.startswith("event:"):
            event = line[6:].strip()
        elif line.startswith("data:"):
            data.append(line[5:].lstrip())
    if event:
        try:
            yield event, json.loads("\n".join(data)) if data else None
        except json.JSONDecodeError:
            yield event, None


class ChatServiceClient:
    """The i360 chat service, called with the user's bearer, exactly as freelang-search-ui does."""

    def __init__(self, base_url: str, token: str, idle_timeout: int = 300):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.idle_timeout = idle_timeout

    def _request(self, method: str, path: str, body: Any = None, headers: dict | None = None):
        request_headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            request_headers["Content-Type"] = "application/json"
        request_headers.update(headers or {})
        request = urllib.request.Request(self.base_url + path, data=data, method=method, headers=request_headers)
        try:
            return urllib.request.urlopen(request, timeout=self.idle_timeout)
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            if exc.code == 401:
                raise AuthExpired(401, "signed_out", "Sign in again.") from None
            message = raw.decode("utf-8", "replace")[:300]
            raise HlError(exc.code, "chat_service_error", message or f"chat service answered {exc.code}") from None
        except (socket.timeout, TimeoutError):
            raise Unreachable(504, "chat_service_timeout",
                              f"The i360 chat service did not answer within {self.idle_timeout:g} s") from None
        except (urllib.error.URLError, ConnectionError) as exc:
            reason = getattr(exc, "reason", exc)
            raise Unreachable(503, "chat_service_unreachable",
                              f"The i360 chat service at {self.base_url} is not reachable ({reason})") from None

    def ask(self, body: dict[str, Any], conversation_id: str | None = None) -> Iterator[tuple[str, Any]]:
        headers = {"Accept": "text/event-stream"}
        if conversation_id:
            headers["X-Chat-Conversation"] = conversation_id  # the service routes a conversation to one replica
        response = self._request("POST", "/chat/ask", body, headers)
        try:
            yield from parse_sse(iter(response.readline, b""))
        finally:
            response.close()

    def call(self, method: str, path: str, body: Any = None) -> Any:
        with self._request(method, "/chat" + path, body) as response:
            payload = response.read()
            return json.loads(payload.decode("utf-8")) if payload else {}


# --------------------------------------------------------------------------------------------
# The model behind HL API
# --------------------------------------------------------------------------------------------
class LlmClient:
    """``POST /api/v1/llm/chat``: an OpenAI-style request; HL API answers a reduced
    ``{model, content, tool_calls, finish_reason, usage}`` (unknown request fields are a 422). Tool calls
    are returned, never run."""

    def __init__(self, client: HlClient, model: str = "", path: str = "/api/v1/llm/chat", timeout: int = 0):
        if timeout and timeout > getattr(client, "timeout", 0):
            # A model round with a large tool result takes longer than HL API's usual 30 s.
            client = copy.copy(client)
            client.timeout = timeout
        self.client = client
        self.model = model
        self.path = path

    def resolve_model(self) -> str:
        if not self.model:
            listing = self.client.get("/api/v1/llm/models")
            models = (listing.get("data") or listing.get("models") or []) if isinstance(listing, dict) else listing
            first = next((m for m in models or [] if m), None) if isinstance(models, list) else None
            self.model = str(first.get("id") if isinstance(first, dict) else first or "")
        return self.model

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
        body: dict[str, Any] = {"messages": messages, "tools": tools, "tool_choice": "auto",
                                "temperature": 0.1, "stream": False}
        model = self.resolve_model()
        if model:
            body["model"] = model
        response = self.client.post(self.path, body)
        return assistant_message(response)


TOOL_CALL_TEXT = re.compile(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", re.S)


def assistant_message(response: Any) -> dict[str, Any]:
    """The assistant message of a completion, with tool calls normalised.

    Some served models write tool calls into the text (``<tool_call>{...}</tool_call>``) instead of
    returning them; those are lifted into ``tool_calls`` so the loop works either way.
    """
    message: dict[str, Any] = {}
    finish_reason = ""
    if isinstance(response, dict):
        choices = response.get("choices") or []
        if choices and isinstance(choices[0], dict):  # a raw OpenAI completion
            message = choices[0].get("message") or {}
            finish_reason = choices[0].get("finish_reason") or ""
        elif isinstance(response.get("message"), dict):
            message = response["message"]
        else:  # HL API's reduced answer: content and tool_calls at the top level
            message = response
        finish_reason = str(response.get("finish_reason") or finish_reason or "")
    content = message.get("content") or ""
    calls = []
    for index, call in enumerate(message.get("tool_calls") or []):
        if not isinstance(call, dict):
            continue
        function = call.get("function") or {}
        calls.append({"id": str(call.get("id") or f"call_{index}"), "name": str(function.get("name") or ""),
                      "arguments": _arguments(function.get("arguments"))})
    if not calls and isinstance(content, str):
        for index, match in enumerate(TOOL_CALL_TEXT.finditer(content)):
            try:
                parsed = json.loads(match.group(1))
            except json.JSONDecodeError:
                continue
            calls.append({"id": f"text_call_{index}", "name": str(parsed.get("name") or ""),
                          "arguments": _arguments(parsed.get("arguments"))})
        if calls:
            content = TOOL_CALL_TEXT.sub("", content).strip()
    return {"content": content if isinstance(content, str) else "", "tool_calls": calls,
            "finish_reason": finish_reason}


def _arguments(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


# --------------------------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------------------------
def _fn(name: str, description: str, properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {"type": "function", "function": {"name": name, "description": description, "parameters": {
        "type": "object", "properties": properties, "required": required or [], "additionalProperties": False}}}


VIEW_PROP = {"type": "string", "enum": list(VIEWS), "description": "map for places, timeline for sequences and calls, table for records"}

TOOLS = [
    _fn("ask_i360",
        "Ask the i360 analyst chat a question about the intelligence data (records, people, phones, places, "
        "times, connections). It searches i360 and answers with cited items. Use it for every question about "
        "the data; never answer such a question yourself.",
        {"question": {"type": "string", "description": "Ignored when the user wrote a message: i360 always gets the "
                                                       "message exactly as typed. The user's question in their own words. i360 keeps the conversation, "
                                                       "so references like 'them' or 'that day' need no rewriting. "
                                                       "Never say 'memory' or 'saved' to i360: there they mean the user's "
                                                       "own chat notes. Ask about the records linked to the investigation"},
         "entity_id": {"type": "string", "description": "For a question about one entity i360 returned "
                                                        "(his calls, where she was): its id"},
         "scope": {"type": "string", "enum": ["investigation", "layers"],
                   "description": "Where to search: 'investigation' = the records linked to the open "
                                  "investigation, when the question says so; otherwise 'layers' = the app's layers. "
                                  "i360 is never searched outside these two."}},
        ["question"]),
    _fn("show_items",
        "Show records i360 cited as a new layer in the app (from_last_answer=true takes all of them).",
        {"from_last_answer": {"type": "boolean"},
         "item_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_SHOWN_ITEMS},
         "label": {"type": "string", "description": "A short layer name a reader understands, e.g. 'Calls of 050-1234567, last week'"},
         "view": VIEW_PROP},
        ["label", "view"]),
    _fn("open_layer",
        "Open one of the app's layers (listed in the context), optionally limited to a time range.",
        {"layer": {"type": "string", "description": "The layer's id or name"},
         "view": VIEW_PROP,
         "start_time": {"type": "string", "description": "ISO 8601, UTC"},
         "end_time": {"type": "string", "description": "ISO 8601, UTC"}},
        ["layer"]),
    _fn("open_item",
        "Open one record in the record viewer: an id i360 cited, an id the user typed, or the record open in the "
        "viewer (from the context). "
        "Never make up an id.",
        {"item_id": {"type": "string"}}, ["item_id"]),
    _fn("open_entity",
        "Open a person or other entity in the viewer: an entity i360 returned (entities in its answer or the "
        "context), or an id the user typed. Never make up an id.",
        {"entity_id": {"type": "string"}}, ["entity_id"]),
    _fn("save_to_memory",
        "Propose saving a layer shown in the app to the open investigation's memory. The user must confirm; "
        "nothing is saved until they do.",
        {"layer": {"type": "string", "description": "The layer's name as shown in the app"}}, ["layer"]),
]

SYSTEM_PROMPT = """You are the assistant inside AI-Intelligence, an analyst map application on i360.
Use the fewest tool calls that fulfil the request, then stop and answer in one or two short sentences.
- You never read data yourself. Every question about the data (records, people, phones, places, times,
  connections, what the investigation holds or has saved, what a record says) goes to ask_i360. Then show
  what it cited with show_items (from_last_answer=true, a clear label, and the view that fits: map when
  places matter, timeline for sequences and calls, table otherwise).
- A question about how many, what kinds or how much data (counts, volume, types) is answered by i360's
  text: do not show the records it sampled.
- The other tools only display. For a display command (open a layer, open a cited record or the one in
  the viewer, save a layer) use the tool directly, without ask_i360. To show what the investigation
  holds, ask i360 and show what it cited.
  Use open_layer only when the user asks for a layer as a whole ("open IPDR"); a layer's records with a
  condition ("IPDR records where …", "calls with DIRECTION incoming") go to ask_i360. An opened layer is the whole answer: do not call
  show_items after it and do not describe its contents (you do not see them).
- What a tool has put on screen (the record viewer, a chat layer) is done: never show it
  again with another tool.
- People and other entities come from i360 too. "Open/show <name>" or "who is <name>": ask_i360, then
  open_entity on the entity
  it returned. If it returned several that match, list their names and ask which one. A follow-up about an
  entity i360 already returned goes to ask_i360 with its entity_id.
- What i360 found is its cited items and their count, not its prose: when it cites records for the question, show
  them, even when its text says the records "do not hold the answer" (its text describes what the records
  contain, and many records hold no text).
- "Linked record <id>" or "linked to record <id>" is a link between records: ask_i360 with scope 'layers' and the
  question as the user wrote it.
- i360 is searched only inside the app's data: our layers, or the open investigation's records when the
  question is about the investigation ("in this investigation", "linked to the investigation", "the case"). There is no wider
  search: if the user asks for data outside our layers, say the app searches only its layers.
  A follow-up keeps the scope of the question it follows. Do not ask the user where to search.
- Name the scope that was searched (this investigation or our layers).
- The conversation lives in i360: you see only the current message, the last answer's cited items and
  what the app shows. Anything about earlier turns goes to ask_i360.
If i360 says the investigation holds nothing that matches and cites records outside it, do not show
them and do not call them the investigation's records: say that nothing in the investigation matched.
To i360, what the investigation has saved is "the records linked to this investigation"; never say
"memory" or "saved" to it, because there they mean the user's own chat notes.
Never invent ids, layer names or facts. If a request is ambiguous, ask one short question instead.
Do not repeat i360's answer; it is already shown to the user."""


NO_TEXT_ANSWER = re.compile(r"\s*(these results do not hold the answer|the provided records do not contain)", re.I)

class ToolHost(Protocol):
    """What the app gives the tools. Implemented in server.py with the user's token."""

    def catalog_layers(self) -> list[dict[str, Any]]: ...
    def item_layers(self, item_ids: list[str]) -> list[dict[str, Any]]: ...
    def layers_scope(self) -> dict[str, Any] | None: ...
    def entity(self, entity_type: str, entity_id: str) -> dict[str, Any] | None: ...


# i360 is only ever asked inside the app's data: the open investigation's records or our layers (Zvika,
# 2026-10-12: "there shouldn't be an option to ask i360 for something that is not in layers").
SCOPES = {"investigation", "layers"}


@dataclass
class TurnContext:
    """What the browser sends with a message."""
    message: str
    investigation_id: str = ""
    investigation_name: str = ""
    investigation_type: str = ""
    scope: str = "investigation"
    i360_conversation_id: str = ""
    i360_scope: str = ""  # the scope the i360 conversation was last asked in
    i360_last_turns: list[str] = field(default_factory=list)
    previous_citations: list[dict[str, str]] = field(default_factory=list)
    previous_entities: list[dict[str, str]] = field(default_factory=list)
    open_layers: list[dict[str, Any]] = field(default_factory=list)
    labels: dict[str, list[str]] = field(default_factory=dict)  # i360 field -> our words for it
    viewer_item_id: str = ""
    timezone: str = ""

    @classmethod
    def from_request(cls, request: dict[str, Any]) -> "TurnContext":
        message = str(request.get("message") or "").strip()
        if not message:
            raise ValueError("Missing message")
        if len(message) > 4000:
            raise ValueError("Message too long")
        def strings(value: Any, limit: int, size: int = 240) -> list[str]:
            return [str(v)[:size] for v in (value or [])[:limit] if isinstance(v, (str, int)) and str(v).strip()] if isinstance(value, list) else []
        scope = str(request.get("scope") or "investigation")
        return cls(
            message=message,
            investigation_id=str(request.get("investigation_id") or "")[:240],
            investigation_name=str(request.get("investigation_name") or "")[:240],
            scope=scope if scope in SCOPES else "auto",
            i360_conversation_id=str(request.get("i360_conversation_id") or "")[:240],
            i360_scope=str(request.get("i360_scope") or "") if request.get("i360_scope") in SCOPES else "",
            i360_last_turns=strings(request.get("i360_last_turns"), 6),
            previous_citations=cited_items(request.get("previous_citations")),
            previous_entities=[{"id": str(e.get("id") or "")[:240], "type": str(e.get("type") or "")[:80],
                                "name": str(e.get("name") or "")[:160]}
                               for e in (request.get("previous_entities") or [])[:100]
                               if isinstance(e, dict) and str(e.get("id") or "").strip()]
                              if isinstance(request.get("previous_entities"), list) else [],
            open_layers=[layer for layer in map(open_layer, request.get("open_layers")[:40]) if layer]
                        if isinstance(request.get("open_layers"), list) else [],
            labels=labels_of(request.get("labels")),
            viewer_item_id=str(request.get("viewer_item_id") or "")[:240],
            timezone=str(request.get("tz") or "")[:64],
        )


def open_layer(layer: Any) -> dict[str, Any] | None:
    """A layer on screen as the browser sent it: its name, the filters applied in the app (the layer's filter
    panel and the results table's column filters, ``where: "table"``), its time range and counts."""
    if isinstance(layer, (str, int)):
        label = str(layer).strip()[:120]  # an older browser sends names only
        return {"label": label, "filters": []} if label else None
    if not isinstance(layer, dict) or not str(layer.get("label") or "").strip():
        return None
    filters = [{"field": str(f["field"]).strip()[:120], "value": str(f["value"]).strip()[:120],
                "where": "table" if f.get("where") == "table" else "layer"}
               for f in (layer.get("filters") or [])[:10]
               if isinstance(f, dict) and str(f.get("field") or "").strip() and str(f.get("value") or "").strip()]
    counts = {k: layer[k] for k in ("shown", "total") if isinstance(layer.get(k), int)}
    return {"label": str(layer["label"]).strip()[:120], "filters": filters,
            "start_time": str(layer.get("start_time") or "")[:40], "end_time": str(layer.get("end_time") or "")[:40],
            **counts}


def labels_of(value: Any) -> dict[str, list[str]]:
    """The i360 chat's ``labels`` the browser sent: i360 field -> the words our screen calls it by."""
    if not isinstance(value, dict):
        return {}
    labels: dict[str, list[str]] = {}
    for field_id, words in list(value.items())[:200]:
        words = [words] if isinstance(words, str) else words if isinstance(words, list) else []
        kept = [str(w).strip() for w in words[:10] if isinstance(w, str) and 0 < len(w.strip()) <= 40]
        if str(field_id).strip() and kept:
            labels[str(field_id).strip()[:200]] = kept
    return labels


def open_layer_text(layer: dict[str, Any]) -> str:
    """A layer on screen in one line. LAMBDA rows are keyed by the i360 field (i360.<path>): named as i360 does."""
    parts = []
    for f in layer.get("filters") or []:
        name = f["field"][len("i360."):] if f["field"].startswith("i360.") else f["field"]
        parts.append(f'{name} contains "{f["value"]}"' + (" (table column filter)" if f["where"] == "table" else ""))
    if layer.get("start_time") or layer.get("end_time"):
        parts.append(f"time {layer.get('start_time') or '…'} to {layer.get('end_time') or '…'}")
    shown, total = layer.get("shown"), layer.get("total")
    if parts and isinstance(shown, int) and isinstance(total, int) and shown != total:
        parts.append(f"{shown} of {total} records shown")
    return f"{layer['label']} (filtered: {'; '.join(parts)})" if parts else layer["label"]


_MEMORY_WORDS = [(re.compile(r"\b(?:the |this |our |my )?investigation'?s memory\b", re.I), "the records linked to this investigation"),
                 (re.compile(r"\b(?:the |its |our |my )?memory\b", re.I), "the records linked to this investigation"),
                 (re.compile(r"\bsaved to\b", re.I), "linked to"),
                 (re.compile(r"\b(?:saved|stored)\b", re.I), "linked")]


# "What's saved/linked/in memory?" as a whole question. A bare "What's linked" reads to i360 as an entity name.
_WHAT_IS_SAVED = re.compile(r"^\W*(?:what|which)(?:'s|\s+is|\s+are|\s+was|\s+were|\s+has\s+been|\s+have\s+been)?\s+"
                            r"(?:saved|stored|linked|kept|in\s+(?:the\s+|this\s+|our\s+|its\s+)?(?:investigation'?s\s+)?memory)\b"
                            r"(?:\s+(?:in|to|for|with)\s+(?:the|this|our)\s+investigation)?\W*$", re.I)
# Checked on LAMBDA: this wording reaches i360's search leg and cites the records; "Which records are linked
# to this investigation?" reached its overview leg, which answers in prose with no citations.
INVESTIGATION_RECORDS_QUESTION = "What records are linked in this investigation?"


# A question about what data there is overall. i360 answers its words as a text search ("75 matches") unless it is
# asked to count. A count of something named ("how many calls in June") keeps its own words.
VOLUME = re.compile(r"\b(data types?|types of data|volume|how much data|what data do we have|what do we have|"
                    r"how many records do we have)\b", re.I)
COUNT_QUESTION = "How many records are there, by type and month?"


def investigation_wording(question: str) -> str:
    """The question with i360's own words for its per-user notes ('memory', 'saved') replaced by the investigation's links."""
    if _WHAT_IS_SAVED.match(question):
        return INVESTIGATION_RECORDS_QUESTION
    for pattern, words in _MEMORY_WORDS:
        question = pattern.sub(words, question)
    return question


def cited_items(value: Any) -> list[dict[str, str]]:
    """i360 citations as the app keeps them: id, type, time and a line of text; plain ids are accepted."""
    out = []
    for entry in value[:500] if isinstance(value, list) else []:
        item = {"id": entry} if isinstance(entry, str) else entry if isinstance(entry, dict) else {}
        item_id = str(item.get("id") or "").strip()[:240]
        if item_id:
            out.append({"id": item_id, "type": str(item.get("type") or "")[:40],
                        "time": str(item.get("time") or item.get("event_time") or "")[:25],
                        "text": str(item.get("text") or item.get("title") or "")[:120]})
    return out


_ENTITY_NAME_KEYS = ("entity_name", "canonical_name", "name", "title", "label")


def answer_entities(answer: dict[str, Any]) -> list[dict[str, str]]:
    """Entities an i360 answer returned (lookup lists, entity cards; never outside_entities, which lie outside the scope), as id, type and name.

    Records arrive as citations; entities arrive elsewhere in the answer, in shapes that vary by leg, so any
    object that names an entity (entity_id, or id with entity_type) is taken, once.
    """
    found: dict[str, dict[str, str]] = {}

    def visit(value: Any, depth: int) -> None:
        if depth > 6 or len(found) >= 100:
            return
        if isinstance(value, list):
            for entry in value[:200]:
                visit(entry, depth + 1)
        elif isinstance(value, dict):
            entity_id = value.get("entity_id") or (value.get("id") if value.get("entity_type") or value.get("kind") == "entity" else None)
            if isinstance(entity_id, (str, int)) and str(entity_id).strip():
                entity_type = value.get("entity_type") or value.get("type") or ""
                name = next((value[k] for k in _ENTITY_NAME_KEYS if isinstance(value.get(k), str) and value[k].strip()), "")
                found.setdefault(str(entity_id)[:240], {"id": str(entity_id)[:240], "type": str(entity_type)[:80],
                                                        "name": str(name)[:160]})
            for key, child in value.items():
                if key not in {"citations", "content", "follow", "claims"}:
                    visit(child, depth + 1)

    for key in ("entities", "people", "cards", "lookup", "subject", "entity"):
        visit(answer.get(key), 0)
    return [e for e in found.values() if not e["type"].upper().startswith("AICHAT_")]


# What a failed step says in the panel; the technical reason goes to the step's details and the log.
FAILED_STEP = {"ask_i360": "i360 didn't answer", "show_items": "Couldn't show the records",
               "open_item": "Couldn't open the record", "open_entity": "Couldn't open that person or entity",
               "open_layer": "Couldn't open the layer", "save_to_memory": "Couldn't save to memory"}


class ChatTurn:
    """One message, start to finish. ``emit(event, data)`` writes to the browser's stream."""

    def __init__(self, llm: LlmClient | None, chat: ChatServiceClient, host: ToolHost,
                 emit: Callable[[str, Any], None], context: TurnContext, chat_model: str = ""):
        self.llm = llm
        self.chat = chat
        self.host = host
        self.emit = emit
        self.ctx = context
        self.chat_model = chat_model
        self.cited: list[dict[str, str]] = list(context.previous_citations)
        self.entities: list[dict[str, str]] = list(context.previous_entities)
        self.on_screen: set[str] = set()  # records this turn already put on screen
        self.cited_this_turn: list[str] = []
        self.has_places = False
        self.i360_conversation_id = context.i360_conversation_id
        self.i360_last_turns = list(context.i360_last_turns)
        self.i360_scope = context.i360_scope
        self.listing_trace: list[str] = []
        self.started = time.monotonic()
        self.summary: list[str] = []  # the turn in one line: "i360 · all data · 50 records → table"
        self.catalog_cache: list[dict[str, Any]] | None = None
        self.labels_cache: dict[str, list[str]] | None = None
        self.raw_test = False  # "/i360 <text>" sends the text to i360 as typed (local tests only)

    # -- the loop ---------------------------------------------------------------------------
    def run(self) -> None:
        if self.raw_test and self.ctx.message.startswith("/i360 "):
            self.raw_i360(self.ctx.message[len("/i360 "):].strip())
        elif self.llm is None:
            self.fallback("The assistant is not configured; asking i360 directly.")
        else:
            messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + self.context_text()}]
            messages.append({"role": "user", "content": self.ctx.message})
            note = ""
            for round_number in range(MAX_ROUNDS):
                try:
                    reply = self.llm.complete(messages, TOOLS)
                except AuthExpired:
                    raise
                except (NotOnThisEstate, Unreachable, HlError) as exc:
                    if round_number == 0:
                        self.fallback(f"The assistant is not available ({exc}); asking i360 directly.")
                        break
                    note = "The assistant stopped before finishing; what is shown above is complete."
                    break
                calls = reply["tool_calls"]
                if not calls and not reply["content"].strip():
                    # Nothing usable, e.g. the model spent its token budget thinking (finish_reason "length").
                    if round_number == 0:
                        self.fallback("The assistant gave no answer; asking i360 directly.")
                    else:
                        note = "The assistant stopped before finishing; what is shown above is complete."
                    break
                if not calls:
                    note = reply["content"].strip()
                    break
                messages.append({"role": "assistant", "content": reply["content"] or None, "tool_calls": [
                    {"id": c["id"], "type": "function",
                     "function": {"name": c["name"], "arguments": json.dumps(c["arguments"], ensure_ascii=False)}}
                    for c in calls]})
                for call in calls:
                    result = self.run_tool(call["name"], call["arguments"])
                    messages.append({"role": "tool", "tool_call_id": call["id"],
                                     "content": json.dumps(result, ensure_ascii=False)[:6000]})
            else:
                note = "I stopped after several steps; tell me what is still missing."
            if note:
                self.emit("note", {"text": note})
        self.emit("done", {"i360_conversation_id": self.i360_conversation_id, "i360_scope": self.i360_scope,
                           "summary": " ".join(self.summary + [f"· {time.monotonic() - self.started:.0f} s"]),
                           "i360_last_turns": self.i360_last_turns[-6:], "citations": self.cited[:500],
                           "entities": self.entities[:100]})

    def raw_i360(self, question: str) -> None:
        """Local test only (CHAT_RAW_TEST=1): the text after "/i360 " goes to i360 exactly as typed, with no
        scope, focus or model; i360's answer is shown as it came. For checking what i360 understands by itself."""
        body = {"request_id": "aii-" + uuid.uuid4().hex[:12], "question": question, "origin": "app", "medium": "auto"}
        if self.ctx.timezone:
            body["tz"] = self.ctx.timezone
        if self.i360_labels():
            body["labels"] = self.i360_labels()
        self.emit("step", {"text": "Asking i360 as typed (test, no scope)", "tool": "ask_i360", "live": True,
                           "focus": "", "scope": "", "question": question[:200]})
        answer, error, _, _ = self.stream(body, None, lambda e, d: self.emit("i360", {"event": e, "data": d}))
        if answer is None:
            self.emit("note", {"text": f"i360 gave no answer ({error or 'empty stream'})"})
            return
        cited = cited_items(answer.get("citations"))
        self.emit("step", {"text": f"i360 answered as typed · {len(cited)} cited · total {answer.get('total')}",
                           "tool": "ask_i360"})

    def fallback(self, reason: str) -> None:
        """No model: ask i360 directly and show what it cited (the plan's option 1)."""
        self.emit("step", {"text": reason})
        scope = self.ctx.scope if self.ctx.scope != "auto" else ("investigation" if self.ctx.investigation_id else "layers")
        result = self.ask_i360({"question": self.ctx.message, "scope": scope})
        if self.cited_this_turn:
            self.show_items({"from_last_answer": True, "label": self.ctx.message[:60],
                             "view": "map" if self.has_places else "table"})
        elif result.get("error"):
            self.emit("note", {"text": result["error"]})

    def context_text(self) -> str:
        lines = []
        if self.ctx.scope == "auto":
            lines.append((f"Open investigation: {self.ctx.investigation_name or self.ctx.investigation_id}. "
                          if self.ctx.investigation_id else "No investigation is open (scope 'investigation' is "
                          "unavailable and save_to_memory too). ") + "Decide ask_i360's scope from the question"
                         + (f"; the previous question searched '{self.i360_scope}'." if self.i360_scope else "."))
        elif self.ctx.investigation_id:
            lines.append(f"Open investigation: {self.ctx.investigation_name or self.ctx.investigation_id}. "
                         f"The user's chosen scope is '{self.ctx.scope}'; ask_i360 searches there.")
        else:
            lines.append(f"No investigation is open; ask_i360 searches '{self.ctx.scope}' and "
                         "save_to_memory is unavailable.")
        layers = [f"{l['id']} ({l.get('label') or ''})" for l in self.catalog()][:40]
        if layers:
            lines.append("Layers the app can open: " + "; ".join(layers))
        if self.ctx.viewer_item_id:
            lines.append(f"Record open in the viewer now: {self.ctx.viewer_item_id}")
        if self.ctx.open_layers:
            lines.append("Layers on screen now, with the filters the user applied in the app: "
                         + "; ".join(open_layer_text(layer) for layer in self.ctx.open_layers))
            lines.append("A question about a filtered layer on screen ('these', 'this layer', the filtered records) "
                         "keeps its filters: say them in ask_i360's question.")
        if self.ctx.previous_citations:
            lines.append(f"The previous i360 answer cited {len(self.ctx.previous_citations)} items "
                         "(from_last_answer=true shows them all). In order:")
            lines += [f"{n}. {c['id']} | {c['type']} | {c['time']} | {c['text']}"
                      for n, c in enumerate(self.ctx.previous_citations[:MAX_CITED_FOR_MODEL], 1)]
        if self.ctx.previous_entities:
            lines.append("Entities the previous i360 answer returned (id | type | name):")
            lines += [f"- {e['id']} | {e['type']} | {e['name']}" for e in self.ctx.previous_entities[:30]]
        if self.ctx.viewer_item_id:
            lines.append("'This record' or 'it' means the record open in the viewer.")
        elif len(self.ctx.previous_citations) == 1:
            lines.append("'This record' or 'it' means the one item the previous answer cited: open it, do not ask which.")
        elif self.ctx.previous_citations:
            lines.append("'The first/second/... record' means that item in the list above.")
        else:
            lines.append("No cited items and no record in the viewer: a request about 'this record', 'it' or "
                         "'them' goes to ask_i360, which holds the conversation. Do not ask the user which one.")
        if self.ctx.timezone:
            lines.append(f"The user's time zone: {self.ctx.timezone}.")
        return "\n".join(lines)

    def i360_labels(self) -> dict[str, list[str]]:
        """The words our screen calls i360's fields by, for the i360 chat's ``labels`` (it then reads "keyboard
        language" in a question as the field). Only fields the index has are sent (an unknown key is ignored
        there, silently), at most 40."""
        if self.labels_cache is None:
            # The same on every request: the profile's names for its fields (built once on the server), plus the
            # screen's words for them (the browser's column names, also fixed), keyed by i360's index field.
            profile = getattr(self.host, "profile_labels", None)
            mapper = getattr(self.host, "index_field", None)
            try:
                labels = {f: list(w) for f, w in ((profile() if profile else None) or {}).items()}
                dropped = []
                for path, words in self.ctx.labels.items():
                    field = mapper(path) if mapper else path
                    if not field:
                        dropped.append(path)
                        continue
                    merged = labels.setdefault(field, [])
                    merged += [w for w in words if w.lower() not in {m.lower() for m in merged}]
            except HlError:
                labels, dropped = dict(self.ctx.labels), []
            if dropped:
                self.emit("step", {"text": f"{len(dropped)} field name(s) not sent to i360 (not in its index)",
                                   "detail": ", ".join(sorted(dropped)[:20]), "log_only": True})
            self.labels_cache = {f: w[:10] for f, w in sorted(labels.items())[:40] if w}
        return self.labels_cache

    def catalog(self) -> list[dict[str, Any]]:
        if self.catalog_cache is None:
            lister = getattr(self.host, "catalog_layers", None)
            try:
                self.catalog_cache = lister() if lister else []
            except HlError:
                self.catalog_cache = []
        return self.catalog_cache

    # -- tools ------------------------------------------------------------------------------
    def run_tool(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        handler = {"ask_i360": self.ask_i360, "show_items": self.show_items, "open_layer": self.open_layer,
                   "open_item": self.open_item, "open_entity": self.open_entity,
                   "save_to_memory": self.save_to_memory}.get(name)
        if handler is None:
            return {"error": f"unknown tool {name}"}
        try:
            result = handler(args)
            if isinstance(result, dict) and result.get("error"):
                self.emit("step", {"text": FAILED_STEP.get(name, "A step failed"), "detail": str(result["error"]),
                                   "error": True, "tool": name})
            return result
        except (AuthExpired, ClientGone):
            raise
        except (HlError, ValueError) as exc:
            text = ("Couldn't reach the platform" if isinstance(exc, Unreachable)
                    else "The platform failed to answer" if isinstance(exc, HlError) and exc.status >= 500
                    else FAILED_STEP.get(name, "A step failed"))
            self.emit("step", {"text": text, "detail": f"{name}: {exc}", "error": True, "tool": name})
            return {"error": str(exc)}

    def ask_i360(self, args: dict[str, Any]) -> dict[str, Any]:
        # i360 gets the analyst's message as typed: it reads the layers (sets), the fields (labels) and the
        # conditions itself, and holds the conversation. The model's own wording is used only without a message.
        question = str(self.ctx.message or args.get("question") or "").strip()[:4000]
        # The question decides between the investigation and our layers; anything else is our layers.
        scope = str(args.get("scope") or "")
        if self.ctx.scope == "investigation" and self.ctx.investigation_id and scope != "layers":
            scope = "investigation"  # the panel's scope wins: the model may widen it to our layers, not narrow it
        elif self.ctx.scope == "layers" or scope not in SCOPES:
            scope = "layers"
        if scope == "investigation" and not self.ctx.investigation_id:
            if self.ctx.scope != "auto":
                scope = "layers"  # the panel's investigation scope with none open
            else:
                return {"error": "no investigation is open: ask the user to open one, or search our layers"}
        if self.i360_conversation_id and self.i360_scope and self.i360_scope != scope:
            # A new scope starts a new i360 conversation, so the old scope's evidence cannot leak into the answer.
            self.i360_conversation_id, self.i360_last_turns = "", []
        self.i360_scope = scope
        body: dict[str, Any] = {"request_id": "aii-" + uuid.uuid4().hex[:12], "question": question,
                                "origin": "app", "medium": "auto"}
        if self.i360_conversation_id:
            body["conversation_id"] = self.i360_conversation_id
            if self.i360_last_turns:
                body["last_turns"] = self.i360_last_turns[-6:]
        if scope == "investigation" and self.ctx.investigation_id:
            body["focus"] = {"kind": "entity", "id": self.ctx.investigation_id, "name": self.ctx.investigation_name,
                             "type": self.ctx.investigation_type, "label": "Investigation"}
            # i360 reads "memory"/"saved" as its own per-user notes and then ignores the focus.
            body["question"] = investigation_wording(question)
        elif self.i360_conversation_id:
            body["focus"] = None  # a conversation keeps its focus until it is cleared
        about = next((e for e in self.entities if e["id"] == str(args.get("entity_id") or "")), None)
        if about:
            body["entity"] = {"id": about["id"], "type": about["type"], "name": about["name"]}
        if self.ctx.timezone:
            body["tz"] = self.ctx.timezone
        if self.i360_labels():
            body["labels"] = self.i360_labels()
        scope_note = ""
        if scope == "layers":
            # Constant on every question: the scope is all our layers' records, `sets` names each layer by its
            # fields and values (i360 narrows to a layer when the question names it), `labels` names the fields.
            # The question goes as typed: i360 reads the layers and the conditions in it.
            constant = getattr(self.host, "constant_scope", None)
            layers = constant() if constant else self.host.layers_scope()
            if not layers:
                return {"error": "the app has no layers to search"}
            layers.pop("exact", None)
            body["scope"] = layers
            sets = getattr(self.host, "layer_sets", None)
            if sets and sets():
                body["sets"] = sets()
            where = " (our layers)"
        else:
            where = " (this investigation)"
        if self.chat_model:
            body["model"] = self.chat_model
        asked_at = time.monotonic()
        self.emit("step", {"text": "Asking i360" + where, "tool": "ask_i360", "live": True,
                           "focus": (body.get("focus") or {}).get("id", ""),
                           "scope": (body.get("scope") or {}).get("kind", ""), "question": body["question"][:200]})
        if scope == "layers" and VOLUME.search(question):
            body["question"] = COUNT_QUESTION  # i360's count leg, not a search for the question's words
        answer, error, _, conversation = self.stream(
            body, self.i360_conversation_id or None, lambda e, d: self.emit("i360", {"event": e, "data": d}))
        if conversation:
            self.i360_conversation_id = conversation
        if answer is not None and answer.get("turn_id"):
            self.i360_last_turns.append(str(answer["turn_id"]))
        if answer is None:
            return {"error": f"i360 gave no answer ({error or 'empty stream'})"}
        where_label = where.strip(" ()")
        citations = list({c["id"]: c for c in cited_items(answer.get("citations"))}.values())
        layer_note = ""
        named = self.layers_named(question) if body.get("focus") else []
        if named:
            # i360 does not know the app's layer names ("IPDR" is aggregated_ip_session from HOSHENTEL to it) and
            # then answers from outside the investigation. The investigation's records, listed by i360, are
            # grouped by the app's layers and the named ones kept.
            listed = self.investigation_listing(body)
            groups = self.host.item_layers([c["id"] for c in listed]) if listed else []
            keep = {str(r.get("i360_item_id")) for g in groups if g.get("label") in named for r in g.get("rows") or []}
            citations = [c for c in listed if c["id"] in keep]
            layer_note = (f"The investigation holds {len(citations)} record(s) of {', '.join(named)}"
                          + (f": {', '.join(c['id'] for c in citations[:20])}" if citations else "")
                          + ". Report this, even where i360's text differs.")
            self.emit("step", {"text": f"The investigation holds {len(citations)} {', '.join(named)} record(s)", "tool": "ask_i360"})
        elif not citations and body.get("focus") and answer.get("leg") == "overview":
            # i360 reads "what records does this investigation hold" as a request for the case brief (the
            # overview leg: counts by type, source and place, no item ids). Its search leg lists the records.
            citations = self.investigation_listing(body)
            self.emit("step", {"text": f"Listed the investigation's {len(citations)} record(s)", "tool": "ask_i360",
                               "trace": "; ".join(self.listing_trace), "log_only": True})
        if body.get("focus") and citations and not named:
            # Strict (Zvika, 2026-10-12): the investigation's records count only when they are also in our layers.
            layer_names = self.layer_names()
            groups = self.host.item_layers([c["id"] for c in citations])
            keep = {str(r.get("i360_item_id")) for g in groups if g.get("label") in layer_names
                    for r in g.get("rows") or []}
            outside = len(citations) - len([c for c in citations if c["id"] in keep])
            citations = [c for c in citations if c["id"] in keep]
            if outside:
                layer_note = (f"{outside} record(s) linked to the investigation are outside our layers and were left "
                              f"out; {len(citations)} remain. Report only these.")
                self.emit("step", {"text": f"Left out {outside} linked record(s) outside our layers",
                                   "tool": "ask_i360"})
        if answer.get("total") == 0:
            citations = []  # the "closest by meaning" records i360 cites with total 0 did not match
        ids = [c["id"] for c in citations]
        self.cited_this_turn = ids
        self.cited = citations
        cards = answer.get("cards") if isinstance(answer.get("cards"), dict) else {}
        agg = cards.get("agg") if isinstance(cards.get("agg"), dict) else {}
        entities = answer_entities(answer)
        if entities:
            self.entities = entities
        self.has_places = bool(cards.get("place") or agg.get("points") or
                               any(isinstance(b, dict) and "lat" in b for b in agg.get("buckets") or []))
        found = " · ".join(part for part in (
            f"{len(ids)} record{'' if len(ids) == 1 else 's'}" if ids or not entities else "",
            f"{len(entities)} {'person' if len(entities) == 1 else 'people/entities'}" if entities else "") if part)
        self.emit("step", {"text": f"Asked i360 ({where_label}) · {found} · {time.monotonic() - asked_at:.0f} s",
                           "tool": "ask_i360"})
        self.summary.append(f"i360 · {where_label} · {found}")
        found = answer.get("total") if isinstance(answer.get("total"), int) else len(ids)
        return {
            "found": f"i360 found {found} record(s) for this question"
                     + (f", {len(ids)} of them cited" if found > len(ids) else "")
                     + ". Its text below only describes what the records contain; say how many were found.",
            # i360 opens with "These results do not hold the answer" whenever the records hold no text (IPDR, ADINT,
            # calls), even when its filter found exactly them; the model then reports "nothing matched".
            "answer": ("(i360's text only says these records hold no text; the records themselves are the answer.)"
                       if found and NO_TEXT_ANSWER.match(str(answer.get("content") or ""))
                       else str(answer.get("content") or "")[:4000]),
            "cited_count": len(ids),
            "total": answer.get("total") or len(ids),
            "has_places": self.has_places,
            "has_time_series": bool(agg and not self.has_places),
            "has_counts": bool(agg or answer.get("counted")),
            "cited_items": citations[:MAX_CITED_FOR_MODEL],
            "entities": entities[:30],
            **({"note": layer_note} if layer_note else {}),
            **({"scope_note": scope_note} if scope_note else {}),
        }

    def stream(self, body: dict[str, Any], conversation_id: str | None,
               on_event: Callable[[str, Any], None] | None = None) -> tuple[dict[str, Any] | None, str, list[tuple[str, Any]], str]:
        """One i360 question: its answer, error, events and conversation id."""
        answer: dict[str, Any] | None = None
        error = conversation = ""
        events: list[tuple[str, Any]] = []
        for event, data in self.chat.ask(body, conversation_id):
            events.append((event, data))
            if on_event:
                on_event(event, data)
            if event == "answer" and isinstance(data, dict):
                answer = data
            elif event == "error":
                error = str((data or {}).get("message") or "error") if isinstance(data, dict) else "error"
                if isinstance(data, dict) and data.get("code") == "model_unavailable":
                    error = "the i360 chat is offline for the night"
            elif event == "done" and isinstance(data, dict) and data.get("conversation_id"):
                conversation = str(data["conversation_id"])
        return answer, error, events, conversation

    def investigation_listing(self, body: dict[str, Any]) -> list[dict[str, str]]:
        """The investigation's records as i360's search leg lists them (a fresh conversation, same focus)."""
        listing = {key: body[key] for key in ("origin", "medium", "focus", "tz", "model") if key in body}
        self.listing_trace = []
        for question_text in OVERVIEW_LISTING_QUESTIONS:
            listed = None
            ask = {**listing, "request_id": "aii-" + uuid.uuid4().hex[:12], "question": question_text}
            for event, data in self.chat.ask(ask, None):
                if event == "answer" and isinstance(data, dict):
                    listed = data
                elif event == "error":
                    self.listing_trace.append(f"error={json.dumps(data, ensure_ascii=True)[:200]}")
            self.listing_trace.append(f"{question_text!r}: leg {(listed or {}).get('leg')}")
            if listed and listed.get("leg") == "search":
                found = list({c["id"]: c for c in cited_items(listed.get("citations"))}.values())
                if found:
                    return found
        return []

    def layer_names(self) -> set[str]:
        """The app's record layers (IPDR, Cellular Calls, ...)."""
        return {str(l.get("source_type") or "") for l in self.catalog() if l.get("kind") == "events"} - {""}

    def layers_named(self, question: str) -> list[str]:
        """The app's record layers the question names (IPDR, Cellular Calls, ...), longest names first."""
        names = sorted(self.layer_names(), key=len, reverse=True)
        found, text = [], question
        for name in names:
            pattern = re.compile(rf"(?<![\w]){re.escape(name)}(?![\w])", re.IGNORECASE)
            if pattern.search(text):
                found.append(name)
                text = pattern.sub(" ", text)  # "Cellular Calls" is not also "Calls"
        return found

    def known_ids(self) -> set[str]:
        return {c["id"] for c in self.cited} | {c["id"] for c in self.ctx.previous_citations}

    def show_items(self, args: dict[str, Any]) -> dict[str, Any]:
        if args.get("from_last_answer") or not args.get("item_ids"):
            ids = [c["id"] for c in self.cited]
        else:
            requested = [str(i) for i in args.get("item_ids") or []]
            unknown = [i for i in requested if i not in self.known_ids()]
            if unknown:
                return {"error": f"{len(unknown)} ids were not cited by i360 in this conversation; use from_last_answer"}
            ids = requested
        if not ids:
            return {"error": "nothing to show: i360 cited no items in its last answer (this says nothing about "
                             "the layers on screen)"}
        new = [i for i in ids if i not in self.on_screen]
        if not new:
            return {"already_on_screen": len(ids), "note": "these records are already on screen; nothing else to do"}
        ids = new[:MAX_SHOWN_ITEMS]
        label = str(args.get("label") or "Chat results").strip()[:80]
        view = args.get("view") if args.get("view") in VIEWS else ("map" if self.has_places else "table")
        groups = self.host.item_layers(ids)
        shown = sum(len(g["rows"]) for g in groups)
        if not shown:
            return {"error": "none of the cited items could be read"}
        self.on_screen.update(str(r.get("i360_item_id")) for g in groups for r in g["rows"])
        self.emit("action", {"kind": "show_items", "label": label, "view": view, "groups": groups})
        missing = len(ids) - shown
        self.emit("step", {"text": f"Showed {shown} record{'' if shown == 1 else 's'} on the {view}"
                                   + (f" · {missing} couldn't be read" if missing else ""), "tool": "show_items"})
        self.summary.append(f"→ {view}" + (f" ({missing} missing)" if missing else ""))
        return {"shown": shown, "layers": [f"Chat: {label} · {g['label']}" if len(groups) > 1 else f"Chat: {label}" for g in groups],
                "view": view, "missing": len(ids) - shown}

    def open_layer(self, args: dict[str, Any]) -> dict[str, Any]:
        resolution = resolve_layer(str(args.get("layer") or ""), self.catalog())
        if resolution["status"] != "resolved":
            return {"status": resolution["status"], "candidates": resolution.get("candidates", []),
                    "message": "Ask the user which layer they mean; do not guess."}
        layer = resolution["layer"]
        filters = {k: args[k] for k in ("start_time", "end_time") if isinstance(args.get(k), str) and args[k].strip()}
        filters = validate_filters(filters) if filters else {}
        if filters and layer.get("kind") != "events":
            return {"error": "time filters apply only to record layers"}
        view = args.get("view") if args.get("view") in VIEWS else None
        caps = layer.get("capabilities") or {}
        if view and caps.get(view) is False:
            view = "table"
        self.emit("action", {"kind": "open_layer", "layer_id": layer["id"], "view": view, "filters": filters})
        self.emit("step", {"text": f"Opened {layer.get('label') or layer['id']}" + (" (filtered by time)" if filters else ""),
                           "tool": "open_layer"})
        return {"opened": layer["id"], "view": view, "filters": filters}

    def open_item(self, args: dict[str, Any]) -> dict[str, Any]:
        item_id = str(args.get("item_id") or "").strip()[:240]
        if not item_id:
            return {"error": "no item_id"}
        typed = len(item_id) >= 6 and item_id in self.ctx.message  # an id the user gave; reading it below checks their access
        if not typed and item_id not in self.known_ids() | self.on_screen | {self.ctx.viewer_item_id} - {""}:
            return {"error": "open_item takes an id i360 cited, the user typed, or the record in the viewer; "
                             "ask i360 to find others"}
        # The record is read only to draw it in the viewer; its fields go to the browser, not to the model.
        groups = self.host.item_layers([item_id])
        row = next((r for g in groups for r in g["rows"]), None)
        if row is None:
            return {"error": f"no readable record with id {item_id}"}
        self.on_screen.add(item_id)
        self.emit("action", {"kind": "open_item", "row": row, "group": groups[0]["label"]})
        self.emit("step", {"text": "Opened the record viewer", "tool": "open_item"})
        return {"opened": item_id, "note": "the record is open in the viewer; nothing else is needed to show it"}

    def open_entity(self, args: dict[str, Any]) -> dict[str, Any]:
        entity_id = str(args.get("entity_id") or "").strip()[:240]
        known = next((e for e in self.entities if e["id"] == entity_id), None)
        typed = len(entity_id) >= 4 and entity_id in self.ctx.message
        if not known and not typed:
            return {"error": "open_entity takes an entity i360 returned or an id the user typed; ask i360 first"}
        # Read only to draw it in the viewer, with the user's token; nothing goes back to the model.
        entity = self.host.entity(known["type"] if known else "", entity_id)
        if not entity:
            return {"error": f"no readable entity with id {entity_id}"}
        self.emit("action", {"kind": "open_entity", "entity_id": entity_id, "entity": entity})
        name = (known or {}).get("name") or entity.get("canonical_name") or entity_id
        self.emit("step", {"text": f"Opened {name}", "tool": "open_entity"})
        return {"opened": name, "note": "the entity is open in the viewer; nothing else is needed to show it"}

    def save_to_memory(self, args: dict[str, Any]) -> dict[str, Any]:
        if not self.ctx.investigation_id:
            return {"error": "no investigation is open"}
        layer = str(args.get("layer") or "").strip()[:120]
        if not layer:
            return {"error": "name the layer to save"}
        self.emit("action", {"kind": "confirm_save", "layer": layer})
        return {"status": "waiting_for_user_confirmation",
                "message": "The user sees a Confirm button; say that it is waiting for them."}
