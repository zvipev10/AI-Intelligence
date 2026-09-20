"""Bounded configuration for the additive OpenAI General experiment.

This module intentionally contains no credentials.  The production server reads
them from its service environment only when the experimental route is selected.
"""

from __future__ import annotations

import os
import json
import subprocess
import sys
import threading
import urllib.error
import urllib.request
import http.client
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OpenAIGeneralSettings:
    api_key: str
    model: str
    enabled: bool


def load_settings(environ: dict[str, str] | None = None) -> OpenAIGeneralSettings:
    """Load the opt-in experiment settings without exposing a secret in logs."""
    env = os.environ if environ is None else environ
    enabled = str(env.get("INTELLIGENCE_POC_OPENAI_GENERAL_ENABLED", "")).lower() in {
        "1", "true", "yes", "on"
    }
    return OpenAIGeneralSettings(
        api_key=str(env.get("OPENAI_API_KEY", "")).strip(),
        model=str(env.get("INTELLIGENCE_POC_OPENAI_GENERAL_MODEL", "gpt-5.6-terra")).strip(),
        enabled=enabled,
    )


def configuration_error(settings: OpenAIGeneralSettings) -> str | None:
    """Return a user-safe setup error; never include the API key itself."""
    if not settings.enabled:
        return "The OpenAI General experiment is not enabled on this server."
    if not settings.api_key:
        return "The OpenAI General experiment needs OPENAI_API_KEY on the server."
    if not settings.model:
        return "The OpenAI General experiment needs a configured model."
    return None


GENERAL_TOOL_NAMES = frozenset({
    "prepare_evidence", "prepare_fused_evidence", "get_evidence", "search_evidence",
    "trace_evidence_provenance", "present_requested_results", "present_saved_memory_layers",
    "open_catalog_layers", "classify_question_intent", "plan_next_investigation_step",
    "search_events", "semantic_search_events", "get_objects", "resolve_location",
    "resolve_event_reference", "find_actor_history", "aggregate_events", "explain_linkage",
    "build_event_sequence", "resolve_entity", "trace_identifier", "trace_semantic_clues",
    "find_related_events", "compare_location_claims", "challenge_hypothesis",
})
GENERAL_TOOL_PREFIX = "mcp_serbia_events_poc_"


class MCPToolBridge:
    """Runs the existing MCP server unchanged and exposes its allowed General tools."""

    def __init__(self, root: Path, environ: dict[str, str] | None = None, sampling_handler=None) -> None:
        self.root = Path(root)
        self.environ = {**os.environ, **(environ or {})}
        self.process: subprocess.Popen[str] | None = None
        self._next_id = 0
        self._lock = threading.RLock()
        self.calls: list[dict[str, Any]] = []
        self.sampling_handler = sampling_handler

    def __enter__(self):
        configured_path = self.environ.get("INTELLIGENCE_POC_MCP_SERVER_PATH", "").strip()
        server_path = Path(configured_path) if configured_path else self.root / "mcp_server" / "server.py"
        if not server_path.is_file():
            raise RuntimeError(f"MCP server is unavailable at {server_path}")
        self.process = subprocess.Popen(
            [sys.executable, str(server_path)], cwd=server_path.parent.parent,
            env=self.environ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", bufsize=1,
        )
        capabilities = {"sampling": {}} if self.sampling_handler else {}
        self.request("initialize", {"protocolVersion": "2025-06-18", "capabilities": capabilities, "clientInfo": {"name": "openai-general-bridge", "version": "0.1"}})
        return self

    def __exit__(self, *_args) -> None:
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait(timeout=5)

    def request(self, method: str, params: dict[str, Any]) -> Any:
        if not self.process or not self.process.stdin or not self.process.stdout:
            raise RuntimeError("MCP bridge is not running")
        with self._lock:
            self._next_id += 1
            request_id = self._next_id
            self.process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}, ensure_ascii=False) + "\n")
            self.process.stdin.flush()
            while line := self.process.stdout.readline():
                message = json.loads(line)
                if message.get("method") == "sampling/createMessage":
                    self._answer_sampling(message)
                    continue
                if message.get("id") != request_id:
                    continue
                if "error" in message:
                    raise RuntimeError(message["error"].get("message", "MCP error"))
                return message.get("result")
        raise RuntimeError("MCP bridge stopped before replying")

    def _answer_sampling(self, message: dict[str, Any]) -> None:
        if not self.process or not self.process.stdin:
            raise RuntimeError("MCP bridge is not running")
        try:
            if not self.sampling_handler:
                raise RuntimeError("Hermes sampling is not configured")
            text = self.sampling_handler(message.get("params") or {})
            reply = {"jsonrpc": "2.0", "id": message.get("id"), "result": {"role": "assistant", "content": {"type": "text", "text": text}, "model": "hermes-helper"}}
        except Exception as exc:
            reply = {"jsonrpc": "2.0", "id": message.get("id"), "error": {"code": -32000, "message": str(exc)}}
        self.process.stdin.write(json.dumps(reply, ensure_ascii=False) + "\n")
        self.process.stdin.flush()

    def function_definitions(self) -> list[dict[str, Any]]:
        tools = self.request("tools/list", {}).get("tools", [])
        return [{"type": "function", "name": f"{GENERAL_TOOL_PREFIX}{tool['name']}", "description": tool.get("description", ""), "parameters": tool.get("inputSchema", {"type": "object"})}
                for tool in tools if tool.get("name") in GENERAL_TOOL_NAMES]

    def call(self, name: str, arguments: dict[str, Any]) -> Any:
        if name.startswith(GENERAL_TOOL_PREFIX):
            name = name[len(GENERAL_TOOL_PREFIX):]
        if name not in GENERAL_TOOL_NAMES:
            raise ValueError(f"Tool is not permitted for OpenAI General: {name}")
        result = self.request("tools/call", {"name": name, "arguments": arguments})
        content = result.get("content", []) if isinstance(result, dict) else []
        text = "\n".join(str(item.get("text", "")) for item in content if isinstance(item, dict))
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = {"raw": text}
        self.calls.append({"tool": name, "arguments": arguments, "result": parsed, "is_error": bool(result.get("isError")) if isinstance(result, dict) else False})
        return parsed


class HermesSamplingHelper:
    """Use Hermes only for MCP sampling requested by an otherwise unchanged tool."""

    def __init__(self, config: dict[str, Any]) -> None:
        if config.get("transport") != "direct":
            raise RuntimeError("The experimental Hermes sampling helper requires direct VM transport")
        self.host = str(config["remote_host"])
        self.port = int(config["remote_port"])
        self.api_key = str(config["api_key"])

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        connection = http.client.HTTPConnection(self.host, self.port, timeout=45)
        try:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body else None
            connection.request(method, path, body=data, headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"})
            response = connection.getresponse()
            payload = response.read().decode("utf-8", errors="replace")
            if response.status >= 400:
                raise RuntimeError(f"Hermes helper failed ({response.status}): {payload[:500]}")
            return json.loads(payload)
        finally:
            connection.close()

    def sample(self, params: dict[str, Any]) -> str:
        system_prompt = str(params.get("systemPrompt") or "")
        messages = params.get("messages") or []
        prompt = "\n".join(str((item.get("content") or {}).get("text") or "") for item in messages if isinstance(item, dict))
        created = self._request("POST", "/v1/runs", {
            "input": prompt,
            "instructions": system_prompt + "\nReturn only the requested content. Do not call tools.",
            "conversation_history": [],
            "session_id": f"openai-mcp-sample-{int(time.time() * 1000)}",
        })
        run_id = created["run_id"]
        deadline = time.time() + 60
        while time.time() < deadline:
            status = self._request("GET", f"/v1/runs/{run_id}")
            if status.get("status") == "completed":
                return str(status.get("output") or "")
            if status.get("status") in {"failed", "cancelled"}:
                raise RuntimeError(str(status.get("error") or "Hermes helper failed"))
            time.sleep(0.5)
        raise TimeoutError("Hermes sampling helper timed out")


class OpenAIGeneralClient:
    """Small Agents API harness; app-owned chat context is supplied per question."""

    base_url = "https://api.openai.com/v1"

    def __init__(self, settings: OpenAIGeneralSettings, bridge: MCPToolBridge) -> None:
        self.settings, self.bridge = settings, bridge

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        request = urllib.request.Request(self.base_url + path, data=data, method=method, headers={
            "Authorization": f"Bearer {self.settings.api_key}", "Content-Type": "application/json", "OpenAI-Beta": "agents=v1",
        })
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                payload = response.read().decode("utf-8")
                return json.loads(payload) if payload.strip() else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:1000]
            raise RuntimeError(f"OpenAI Agents request failed ({exc.code}): {detail}") from exc

    def _stream(self, method: str, path: str, body: dict[str, Any] | None = None):
        """Yield JSON SSE payloads from the Agents session event stream."""
        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        request = urllib.request.Request(self.base_url + path, data=data, method=method, headers={
            "Authorization": f"Bearer {self.settings.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "OpenAI-Beta": "agents=v1",
        })
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                data_lines: list[str] = []
                for raw_line in response:
                    line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
                    if not line:
                        if data_lines:
                            payload = "\n".join(data_lines)
                            data_lines = []
                            if payload != "[DONE]":
                                yield json.loads(payload)
                        continue
                    if line.startswith("data:"):
                        data_lines.append(line[5:].lstrip())
                if data_lines:
                    payload = "\n".join(data_lines)
                    if payload != "[DONE]":
                        yield json.loads(payload)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:1000]
            raise RuntimeError(f"OpenAI Agents stream failed ({exc.code}): {detail}") from exc

    def investigate(self, prompt: str, context: str, *, instructions: str, session_id: str | None = None) -> dict[str, Any]:
        session_id = str(session_id or "").strip()
        if session_id:
            self._request("POST", f"/agents/sessions/{session_id}/events", {"events": [{
                "type": "agent.session.input.message",
                "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt}]}],
            }]})
            stream = self._stream("GET", f"/agents/sessions/{session_id}/events")
        else:
            if not instructions.strip():
                raise ValueError("OpenAI General requires the shared General-agent instructions")
            user_text = f"{context}\n\n--- Current analyst question ---\n{prompt}"
            stream = self._stream("POST", "/agents/sessions", {
                "stream": True,
                "environment": {"type": "none"},
                "agent": {"model": self.settings.model, "instructions": instructions, "tools": self.bridge.function_definitions()},
                "input": user_text,
            })
        deadline = time.time() + 180
        completed = False
        handled_calls: set[str] = set()
        while not completed:
            if time.time() >= deadline:
                raise TimeoutError("OpenAI General exceeded the three-minute runtime limit")
            resume_stream = False
            for message in stream:
                event_type = str(message.get("type") or "")
                session = message.get("session") if isinstance(message.get("session"), dict) else {}
                session_id = str(session.get("id") or message.get("session_id") or session_id)
                if event_type in {"error", "agent.session.failed", "agent.session.turn.failed", "agent.session.turn.cancelled"}:
                    error = message.get("error") or message.get("turn", {}).get("error") or "OpenAI session turn failed"
                    if isinstance(error, dict):
                        error = error.get("message") or error.get("code") or "OpenAI session turn failed"
                    raise RuntimeError(str(error))
                if event_type == "agent.session.requires_action":
                    if not session_id:
                        raise RuntimeError("OpenAI requested a tool before returning a session id")
                    state = self._request("GET", f"/agents/sessions/{session_id}")
                    for action in state.get("required_actions") or []:
                        call_id = str(action.get("call_id") or "")
                        if action.get("type") != "function_call" or not call_id or call_id in handled_calls:
                            continue
                        handled_calls.add(call_id)
                        try:
                            output = self.bridge.call(str(action["name"]), action.get("arguments") or {})
                            event = {"type": "agent.session.input.tool_result", "turn_id": action["turn_id"], "call_id": call_id, "success": True, "output": json.dumps(output, ensure_ascii=False)}
                        except Exception as exc:
                            event = {"type": "agent.session.input.tool_result", "turn_id": action["turn_id"], "call_id": call_id, "success": False, "error": str(exc)}
                        self._request("POST", f"/agents/sessions/{session_id}/events", {"events": [event]})
                    resume_stream = True
                    break
                if event_type == "agent.session.turn.completed":
                    completed = True
                    break
            if completed:
                break
            if not session_id:
                raise RuntimeError("OpenAI event stream ended before creating a session")
            # After a tool result, attach to the session's event stream for the
            # resumed turn. This avoids treating an idle session as completion.
            if resume_stream:
                stream = self._stream("GET", f"/agents/sessions/{session_id}/events")
            else:
                raise RuntimeError("OpenAI event stream ended before turn completion")
        items = self._request("GET", f"/agents/sessions/{session_id}/items?order=desc&limit=100").get("data", [])
        answer = ""
        for item in items:
            if item.get("type") != "message" or item.get("role") != "assistant":
                continue
            answer = "\n".join(part.get("text", "") for part in item.get("content", []) if isinstance(part, dict) and part.get("type") == "output_text").strip()
            if answer:
                break
        if not answer:
            raise RuntimeError("OpenAI completed without a final assistant answer")
        final_state = self._request("GET", f"/agents/sessions/{session_id}")
        return {"answer": answer, "openai_session_id": session_id, "tool_calls": self.bridge.calls, "usage": final_state.get("usage", {})}
