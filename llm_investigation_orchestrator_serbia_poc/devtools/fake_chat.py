"""Stand-ins for the chat's two upstreams, for development and CI only.

- ``scripted_completion``: what ``POST /api/v1/llm/chat`` on the fake HL API answers. Not a model: a
  few fixed rules that exercise the app's tool loop the way a model would (ask i360, then show what it
  cited; open a layer for "open ..."; open a record for "open the first/second ..."; save for "save ...").
- ``FakeChatService``: the i360 chat service (``analytics/i360-chat``) as freelang-search-ui sees it:
  ``POST /chat/ask`` streams ``status``, ``token``, ``answer`` (text, citations, cards) and ``done`` over
  SSE; ``POST /chat/actions`` answers a confirmed tag or note. It cites fixture items whose English text
  shares a word with the question.

The real contracts are read from freelang-search-ui's client and HL API's capability map, not from the
services themselves; recorded answers from LAMBDA are the check on these fakes.
"""
from __future__ import annotations

import json
import re
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

STOP_WORDS = {"what", "which", "where", "when", "show", "were", "with", "from", "that", "this", "there",
              "about", "have", "does", "near", "into", "they", "them", "their", "please", "tell"}


def _call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    return {"id": "call_" + uuid.uuid4().hex[:8], "type": "function",
            "function": {"name": name, "arguments": json.dumps(arguments)}}


def _completion(content: str | None = None, calls: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    message: dict[str, Any] = {"role": "assistant", "content": content}
    if calls:
        message["tool_calls"] = calls
    return {"id": "chatcmpl-fake", "object": "chat.completion", "model": "fake-model",
            "choices": [{"index": 0, "message": message, "finish_reason": "tool_calls" if calls else "stop"}]}


def scripted_completion(body: dict[str, Any]) -> dict[str, Any]:
    messages = body.get("messages") or []
    user = next((m.get("content") or "" for m in reversed(messages) if m.get("role") == "user"), "")
    text = user.lower()
    tool_results = []
    for message in messages[[i for i, m in enumerate(messages) if m.get("role") == "user"][-1] + 1:] if any(m.get("role") == "user" for m in messages) else []:
        if message.get("role") == "tool":
            try:
                tool_results.append(json.loads(message.get("content") or "{}"))
            except json.JSONDecodeError:
                tool_results.append({})
    last = tool_results[-1] if tool_results else None
    if last is None:
        if text.startswith("save"):
            return _completion(None, [_call("save_to_memory", {"layer": user.split(" ", 1)[-1]})])
        if text.startswith("open the first") or text.startswith("open the second"):
            cited = re.findall(r"^\d+\. (\S+) \|", messages[0].get("content") or "", re.M)
            index = 0 if "first" in text else 1
            if len(cited) <= index:
                return _completion("There is no such record in the last answer.")
            return _completion(None, [_call("open_item", {"item_id": cited[index]})])
        if text.startswith("open "):
            match = re.match(r"open (?:the )?(.+?)(?: layer)?(?: on the (map|timeline|table))?$", text)
            layer, view = (match.group(1), match.group(2)) if match else (text[5:], None)
            return _completion(None, [_call("open_layer", {"layer": layer, **({"view": view} if view else {})})])
        return _completion(None, [_call("ask_i360", {"question": user})])
    if "answer" in last and "cited_count" in last:
        if not last.get("cited_count"):
            return _completion("i360 found nothing to show.")
        view = "map" if last.get("has_places") else "table"
        return _completion(None, [_call("show_items", {"from_last_answer": True, "label": user[:40], "view": view})])
    if "shown" in last:
        return _completion(f"Showed {last['shown']} records on the {last.get('view')}.")
    if last.get("status") == "waiting_for_user_confirmation":
        return _completion("Click Confirm to save it.")
    if last.get("error"):
        return _completion(f"That did not work: {last['error']}")
    return _completion("Done.")


class FakeChatService:
    def __init__(self, estate):
        self.estate = estate
        self.asks: list[dict[str, Any]] = []
        self.actions: list[dict[str, Any]] = []
        self.conversations: dict[str, list[str]] = {}

    def cite(self, question: str) -> list[dict[str, Any]]:
        words = {w for w in re.findall(r"[a-z]{4,}", question.lower()) if w not in STOP_WORDS}
        hits = []
        for item in sorted(self.estate.items.values(), key=lambda i: str(i.get("event_time") or ""), reverse=True):
            english = str((item.get("text") or {}).get("english") or "").lower()
            if words and words & set(re.findall(r"[a-z]{4,}", english)):
                hits.append(item)
            if len(hits) >= 12:
                break
        return hits

    def answer(self, body: dict[str, Any]) -> list[tuple[str, Any]]:
        self.asks.append(body)
        question = str(body.get("question") or "")
        if "fail" in question.lower():
            return [("status", {"text": "Searching…"}), ("error", {"message": "model unavailable"})]
        hits = self.cite(question)
        conversation = str(body.get("conversation_id") or "conv-" + uuid.uuid4().hex[:8])
        self.conversations.setdefault(conversation, []).append(question)
        content = (f"I found {len(hits)} records about this [1]." if hits else "I found nothing about this.")
        points = [{"id": i["item_id"], "lat": i["location"]["point"]["lat"], "lon": i["location"]["point"]["lon"],
                   "time": i.get("event_time")}
                  for i in hits if ((i.get("location") or {}).get("point") or {}).get("lat") is not None]
        cards = {"agg": {"kind": "geo", "total": len(hits), "points": points}} if points else {}
        return [
            ("status", {"text": "Searching…", "steps": [{"tool": "items.search", "summary": f"{len(hits)} hits"}]}),
            ("token", {"text": content[:12]}), ("token", {"text": content[12:]}),
            ("answer", {"content": content, "total": len(hits), "turn_id": "AICHAT_MSG_" + uuid.uuid4().hex[:6],
                        "citations": [{"id": i["item_id"], "type": i.get("item_type"), "time": i.get("event_time"),
                                       "text": str((i.get("text") or {}).get("english") or "")[:120]} for i in hits],
                        "cards": cards, "follow": ["Show them on the map", "Who is involved?"]}),
            ("done", {"conversation_id": conversation}),
        ]


class FakeChatHandler(BaseHTTPRequestHandler):
    service: FakeChatService

    def log_message(self, fmt, *args):
        pass

    def _json(self, status: int, value: Any) -> None:
        body = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            user = self.service.estate.user(self.headers.get("Authorization"))
        except Exception:  # noqa: BLE001 - the fake estate's ApiError: no or unknown token
            user = None
        if not user:
            return self._json(401, {"error": "unauthorised"})
        length = int(self.headers.get("Content-Length", "0") or 0)
        body = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        if self.path == "/chat/ask":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            self.wfile.write(b": keep-alive\n\n")
            for event, data in self.service.answer(body):
                self.wfile.write(f"event: {event}\ndata: {json.dumps(data)}\n\n".encode("utf-8"))
                self.wfile.flush()
            return
        if self.path == "/chat/actions":
            self.service.actions.append(body)
            verb = "Tagged" if body.get("kind") == "tag" else "Annotated"
            return self._json(200, {"ok": True, "line": f"{verb} {len(body.get('ids') or [])} records.", "result": {}})
        return self._json(404, {"error": "not_found"})


def make_chat_server(host: str, port: int, estate) -> tuple[ThreadingHTTPServer, FakeChatService]:
    service = FakeChatService(estate)
    handler = type("BoundFakeChatHandler", (FakeChatHandler,), {"service": service})
    server = ThreadingHTTPServer((host, port), handler)
    server.daemon_threads = True
    return server, service
