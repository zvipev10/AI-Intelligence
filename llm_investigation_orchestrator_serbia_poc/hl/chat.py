"""The chat: i360's chat service answers questions, a small tool loop over HL API drives the app.

One user message is one turn (``ChatTurn.run``):

1. The message, a short history and what the app shows go to the model behind HL API
   ``POST /api/v1/llm/chat`` with six tools. The model returns tool calls; HL API never runs them.
2. ``ask_i360`` sends a question to the i360 chat service (``analytics/i360-chat``, ``POST /chat/ask``,
   the user's own bearer). Its answer stream is relayed to the browser as it arrives, and the model
   gets back the answer text and the ids of the items it cited.
3. The app tools (``show_items``, ``open_layer``, ``open_item``, ``show_memory``, ``save_to_memory``) are
   checked here and sent to the browser as actions; the browser carries them out. ``save_to_memory``
   is only a proposal: the browser asks the user to confirm before anything is written.
4. The model's last text is the turn's closing note.

If the model cannot be reached, the turn falls back to asking i360 directly and showing what it cited.
Everything travels with the user's token; nothing is kept between turns on the server (the browser
sends the history and the previous answer's ids with every message).
"""
from __future__ import annotations

import json
import re
import socket
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator, Protocol

from catalog_filters import resolve_layer, validate_filters
from hl.client import AuthExpired, HlClient, HlError, NotOnThisEstate, Unreachable

MAX_ROUNDS = 6
MAX_SHOWN_ITEMS = 200
MAX_CITED_FOR_MODEL = 60
MAX_HISTORY = 12
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
        except (urllib.error.URLError, socket.timeout, ConnectionError):
            raise Unreachable(503, "chat_service_unreachable", "The i360 chat service is not reachable") from None

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

    def __init__(self, client: HlClient, model: str = "", path: str = "/api/v1/llm/chat"):
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
        {"question": {"type": "string", "description": "The question, in the user's words plus anything from the conversation it needs"},
         "scope": {"type": "string", "enum": ["investigation", "all"],
                   "description": "investigation: only the open investigation's saved items; all: all data the user can see"}},
        ["question"]),
    _fn("show_items",
        "Show records as a new layer in the app. Use the ids i360 cited (from_last_answer=true takes all of them).",
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
        "Open one record in the record viewer. Only ids i360 cited in this conversation.",
        {"item_id": {"type": "string"}}, ["item_id"]),
    _fn("show_memory",
        "Open layers saved in the open investigation's memory (names from the context, or 'all').",
        {"layers": {"type": "array", "items": {"type": "string"}}}, ["layers"]),
    _fn("save_to_memory",
        "Propose saving a layer shown in the app to the open investigation's memory. The user must confirm; "
        "nothing is saved until they do.",
        {"layer": {"type": "string", "description": "The layer's name as shown in the app"}}, ["layer"]),
]

SYSTEM_PROMPT = """You are the assistant inside AI-Intelligence, an analyst map application on i360.
You do not know the data. The i360 chat does: for any question about records, people, phones, places,
times or connections, call ask_i360, then present what it found with show_items (from_last_answer=true,
a clear label, and the view that fits: map when places matter, timeline for sequences and calls, table
otherwise). For commands about the app (open a layer, open a record, switch view, show saved layers,
save a layer) use the app tools directly without asking i360. Never invent ids, layer names or facts.
If a request is ambiguous, ask one short question instead of guessing.
Finish with one or two short sentences saying what you showed; do not repeat i360's answer."""


class ToolHost(Protocol):
    """What the app gives the tools. Implemented in server.py with the user's token."""

    def catalog_layers(self) -> list[dict[str, Any]]: ...
    def item_layers(self, item_ids: list[str]) -> list[dict[str, Any]]: ...
    def memory_layers(self, investigation_id: str) -> list[dict[str, Any]]: ...


@dataclass
class TurnContext:
    """What the browser sends with a message."""
    message: str
    history: list[dict[str, str]] = field(default_factory=list)
    investigation_id: str = ""
    investigation_name: str = ""
    investigation_type: str = ""
    scope: str = "investigation"
    i360_conversation_id: str = ""
    previous_citations: list[dict[str, str]] = field(default_factory=list)
    open_layers: list[str] = field(default_factory=list)
    timezone: str = ""

    @classmethod
    def from_request(cls, request: dict[str, Any]) -> "TurnContext":
        message = str(request.get("message") or "").strip()
        if not message:
            raise ValueError("Missing message")
        if len(message) > 4000:
            raise ValueError("Message too long")
        history = []
        for entry in (request.get("history") or [])[-MAX_HISTORY:]:
            if isinstance(entry, dict) and entry.get("role") in {"user", "assistant"} and isinstance(entry.get("content"), str):
                history.append({"role": entry["role"], "content": entry["content"][:2000]})
        def strings(value: Any, limit: int, size: int = 240) -> list[str]:
            return [str(v)[:size] for v in (value or [])[:limit] if isinstance(v, (str, int)) and str(v).strip()] if isinstance(value, list) else []
        scope = str(request.get("scope") or "investigation")
        return cls(
            message=message, history=history,
            investigation_id=str(request.get("investigation_id") or "")[:240],
            investigation_name=str(request.get("investigation_name") or "")[:240],
            scope=scope if scope in {"investigation", "all"} else "investigation",
            i360_conversation_id=str(request.get("i360_conversation_id") or "")[:240],
            previous_citations=cited_items(request.get("previous_citations")),
            open_layers=strings(request.get("open_layers"), 40),
            timezone=str(request.get("tz") or "")[:64],
        )


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
        self.cited_this_turn: list[str] = []
        self.has_places = False
        self.i360_conversation_id = context.i360_conversation_id
        self.catalog_cache: list[dict[str, Any]] | None = None

    # -- the loop ---------------------------------------------------------------------------
    def run(self) -> None:
        if self.llm is None:
            self.fallback("The assistant is not configured; asking i360 directly.")
        else:
            messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + self.context_text()}]
            messages += self.ctx.history
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
                                     "content": json.dumps(result, ensure_ascii=False)[:12000]})
            else:
                note = "I stopped after several steps; tell me what is still missing."
            if note:
                self.emit("note", {"text": note})
        self.emit("done", {"i360_conversation_id": self.i360_conversation_id, "citations": self.cited[:500]})

    def fallback(self, reason: str) -> None:
        """No model: ask i360 directly and show what it cited (the plan's option 1)."""
        self.emit("step", {"text": reason})
        result = self.ask_i360({"question": self.ctx.message, "scope": self.ctx.scope})
        if self.cited_this_turn:
            self.show_items({"from_last_answer": True, "label": self.ctx.message[:60],
                             "view": "map" if self.has_places else "table"})
        elif result.get("error"):
            self.emit("note", {"text": result["error"]})

    def context_text(self) -> str:
        lines = []
        if self.ctx.investigation_id:
            lines.append(f"Open investigation: {self.ctx.investigation_name or self.ctx.investigation_id}. "
                         f"ask_i360 scope defaults to '{self.ctx.scope}'.")
        else:
            lines.append("No investigation is open; ask_i360 searches all data and show_memory/save_to_memory are unavailable.")
        layers = [f"{l['id']} ({l.get('label') or ''})" for l in self.catalog()][:40]
        if layers:
            lines.append("Layers the app can open: " + "; ".join(layers))
        if self.ctx.open_layers:
            lines.append("Layers on screen now: " + "; ".join(self.ctx.open_layers))
        if self.ctx.previous_citations:
            lines.append(f"The previous i360 answer cited {len(self.ctx.previous_citations)} items "
                         "(from_last_answer=true shows them all). In order:")
            lines += [f"{n}. {c['id']} | {c['type']} | {c['time']} | {c['text']}"
                      for n, c in enumerate(self.ctx.previous_citations[:MAX_CITED_FOR_MODEL], 1)]
        if self.ctx.timezone:
            lines.append(f"The user's time zone: {self.ctx.timezone}.")
        return "\n".join(lines)

    def catalog(self) -> list[dict[str, Any]]:
        if self.catalog_cache is None:
            try:
                self.catalog_cache = self.host.catalog_layers()
            except HlError:
                self.catalog_cache = []
        return self.catalog_cache

    # -- tools ------------------------------------------------------------------------------
    def run_tool(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        handler = {"ask_i360": self.ask_i360, "show_items": self.show_items, "open_layer": self.open_layer,
                   "open_item": self.open_item, "show_memory": self.show_memory,
                   "save_to_memory": self.save_to_memory}.get(name)
        if handler is None:
            return {"error": f"unknown tool {name}"}
        try:
            return handler(args)
        except (AuthExpired, ClientGone):
            raise
        except (HlError, ValueError) as exc:
            self.emit("step", {"text": f"{name} failed: {exc}", "error": True})
            return {"error": str(exc)}

    def ask_i360(self, args: dict[str, Any]) -> dict[str, Any]:
        question = str(args.get("question") or self.ctx.message).strip()[:4000]
        scope = args.get("scope") if args.get("scope") in {"investigation", "all"} else self.ctx.scope
        body: dict[str, Any] = {"request_id": "aii-" + uuid.uuid4().hex[:12], "question": question,
                                "origin": "ai-intelligence", "medium": "auto"}
        if self.i360_conversation_id:
            body["conversation_id"] = self.i360_conversation_id
        if scope == "investigation" and self.ctx.investigation_id:
            body["focus"] = {"kind": "entity", "id": self.ctx.investigation_id, "name": self.ctx.investigation_name,
                             "type": self.ctx.investigation_type, "label": "Investigation"}
        if self.ctx.timezone:
            body["tz"] = self.ctx.timezone
        if self.chat_model:
            body["model"] = self.chat_model
        self.emit("step", {"text": "Asking i360" + (" (this investigation)" if body.get("focus") else " (all data)"),
                           "tool": "ask_i360"})
        answer: dict[str, Any] | None = None
        error = ""
        for event, data in self.chat.ask(body, self.i360_conversation_id or None):
            self.emit("i360", {"event": event, "data": data})
            if event == "answer" and isinstance(data, dict):
                answer = data
            elif event == "error":
                error = str((data or {}).get("message") or "error") if isinstance(data, dict) else "error"
            elif event == "done" and isinstance(data, dict) and data.get("conversation_id"):
                self.i360_conversation_id = str(data["conversation_id"])
        if answer is None:
            return {"error": f"i360 gave no answer ({error or 'empty stream'})"}
        citations = list({c["id"]: c for c in cited_items(answer.get("citations"))}.values())
        ids = [c["id"] for c in citations]
        self.cited_this_turn = ids
        self.cited = citations
        cards = answer.get("cards") if isinstance(answer.get("cards"), dict) else {}
        agg = cards.get("agg") if isinstance(cards.get("agg"), dict) else {}
        self.has_places = bool(cards.get("place") or agg.get("points") or
                               any(isinstance(b, dict) and "lat" in b for b in agg.get("buckets") or []))
        return {
            "answer": str(answer.get("content") or "")[:4000],
            "cited_count": len(ids),
            "total": answer.get("total") or len(ids),
            "has_places": self.has_places,
            "has_time_series": bool(agg and not self.has_places),
            "cited_items": citations[:MAX_CITED_FOR_MODEL],
        }

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
            return {"error": "nothing to show: i360 cited no items"}
        ids = ids[:MAX_SHOWN_ITEMS]
        label = str(args.get("label") or "Chat results").strip()[:80]
        view = args.get("view") if args.get("view") in VIEWS else ("map" if self.has_places else "table")
        groups = self.host.item_layers(ids)
        shown = sum(len(g["rows"]) for g in groups)
        if not shown:
            return {"error": "none of the cited items could be read"}
        self.emit("action", {"kind": "show_items", "label": label, "view": view, "groups": groups})
        self.emit("step", {"text": f"Showed {shown} records as '{label}' on the {view}", "tool": "show_items"})
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
        item_id = str(args.get("item_id") or "").strip()
        if item_id not in self.known_ids():
            return {"error": "that id was not cited by i360 in this conversation"}
        groups = self.host.item_layers([item_id])
        row = next((r for g in groups for r in g["rows"]), None)
        if row is None:
            return {"error": "the record could not be read"}
        self.emit("action", {"kind": "open_item", "row": row, "group": groups[0]["label"]})
        self.emit("step", {"text": "Opened the record viewer", "tool": "open_item"})
        return {"opened": item_id}

    def show_memory(self, args: dict[str, Any]) -> dict[str, Any]:
        if not self.ctx.investigation_id:
            return {"error": "no investigation is open"}
        saved = self.host.memory_layers(self.ctx.investigation_id)
        if not saved:
            return {"error": "this investigation has no saved layers"}
        wanted = [str(n) for n in args.get("layers") or []]
        if not wanted or any(n.strip().lower() == "all" for n in wanted):
            chosen = saved
        else:
            chosen, problems = [], []
            for name in wanted:
                resolution = resolve_layer(name, [{"id": s["id"], "label": s.get("label") or s["id"]} for s in saved])
                if resolution["status"] == "resolved":
                    chosen.append(next(s for s in saved if s["id"] == resolution["layer"]["id"]))
                else:
                    problems.append({"requested": name, "candidates": resolution.get("candidates", [])})
            if problems:
                return {"status": "clarification_required", "problems": problems,
                        "saved_layers": [s.get("label") for s in saved][:30]}
        self.emit("action", {"kind": "show_memory", "ids": [s["id"] for s in chosen]})
        self.emit("step", {"text": f"Opened {len(chosen)} saved layer(s)", "tool": "show_memory"})
        return {"opened": [s.get("label") for s in chosen]}

    def save_to_memory(self, args: dict[str, Any]) -> dict[str, Any]:
        if not self.ctx.investigation_id:
            return {"error": "no investigation is open"}
        layer = str(args.get("layer") or "").strip()[:120]
        if not layer:
            return {"error": "name the layer to save"}
        self.emit("action", {"kind": "confirm_save", "layer": layer})
        return {"status": "waiting_for_user_confirmation",
                "message": "The user sees a Confirm button; say that it is waiting for them."}
