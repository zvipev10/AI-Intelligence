#!/usr/bin/env python3
"""Minimal MCP protocol smoke check for the Serbia/Kosovo POC server."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SERVER = Path(__file__).with_name("server.py")

def mock_sampling(message: dict) -> dict:
    parsed = {}
    try:
        params = message.get("params") or {}
        content = ((params.get("messages") or [])[0].get("content") or {}).get("text") or ""
        parsed = json.loads(content)
    except (json.JSONDecodeError, AttributeError, IndexError, TypeError):
        parsed = {}
    task = parsed.get("task")
    if task == "trace_semantic_clues_expand":
        return {"expanded_clues": ["הכחשה", "דיווח לא מאומת"], "rationale": "בדיקת אמינות דורשת גם רמזי הכחשה ואימות."}
    if task == "find_related_events_rerank":
        candidates = parsed.get("candidate_events") or []
        return {"top_event_ids": [item.get("event_id") for item in candidates[:5] if item.get("event_id")], "rationale": "מעדיף מועמדים עם קשרים דטרמיניסטיים חזקים."}
    if task == "compare_location_claims_assess":
        return {"assessment": "יש פיזור גאוגרפי של טענות דומות.", "strongest_group_indexes": [0], "caution": "אין אמת קרקע בכלי."}
    if task == "challenge_hypothesis_reasoning":
        return {"competing_hypotheses": ["דפוס אמיתי", "רעש מידע"], "disproof_tests": ["הצלבת מקורות"], "synthesis": "נדרשת הצלבה נוספת."}
    if task == "resolve_event_reference_terms":
        return {
            "search_phrases": ["חציית גבול", "אין לכך אימות"],
            "location_terms": ["גבול"],
            "actor_terms": ["מקורות אחרים"],
            "rationale": "הפניה ממוקדת בטענת גבול לא מאומתת.",
        }
    return {
        "intent": "investigation",
        "recommended_mode": "investigation",
        "recommended_view_hint": "evidence",
        "confidence": "גבוהה",
        "reason": "השאלה מבקשת לבדוק אמינות, מקורות, סתירות וחלופות.",
    }

def request(process: subprocess.Popen[str], payload: dict) -> dict:
    assert process.stdin is not None
    assert process.stdout is not None
    process.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
    process.stdin.flush()
    while True:
        line = process.stdout.readline()
        if not line:
            stderr = process.stderr.read() if process.stderr is not None else ""
            raise RuntimeError(f"MCP server exited before responding: {stderr}")
        message = json.loads(line)
        if message.get("method") == "sampling/createMessage":
            sample = mock_sampling(message)
            process.stdin.write(json.dumps({
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {
                    "role": "assistant",
                    "content": {"type": "text", "text": json.dumps(sample, ensure_ascii=False)},
                    "model": "mock-sampling",
                    "stopReason": "endTurn",
                },
            }, ensure_ascii=False) + "\n")
            process.stdin.flush()
            continue
        return message

def call(process, request_id, name, arguments):
    return request(process, {"jsonrpc":"2.0", "id":request_id, "method":"tools/call", "params":{"name":name, "arguments":arguments}})

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    process = subprocess.Popen([sys.executable, str(SERVER)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    try:
        initialized = request(process, {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{"sampling":{}},"clientInfo":{"name":"smoke","version":"1"}}})
        tools = request(process, {"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}})
        classified = call(process, 3, "classify_question_intent", {"question":"האם הטענה על חציית גבול מגובה במקור אמין? חפש מקורות, סתירות וחלופות."})
        location = call(process, 4, "resolve_location", {"query":"צפון מיטרוביצה"})
        events = call(process, 5, "search_events", {"keywords":["חציית גבול"], "limit":50})
        aggregate = call(process, 6, "aggregate_events", {"group_by":"location", "keywords":["חסימה"], "limit":500, "top_n":5})
        identifier = call(process, 7, "trace_identifier", {"identifier":"REC-017577", "identifier_type":"record", "limit":50})
        semantic = call(process, 8, "trace_semantic_clues", {"clues":["חציית גבול", "מקורות אחרים", "חשבונות", "KFOR"], "limit":100})
        related = call(process, 9, "find_related_events", {"seed_event_ids": (semantic["result"]["structuredContent"].get("event_ids") or [])[:3], "dimensions":["semantic","time","location","entity"], "before_hours":12, "after_hours":12, "limit":100})
        geo_conflicts = call(process, 10, "compare_location_claims", {"keywords":["חציית גבול", "גבול", "מכחישים"], "limit":5})
        challenge = call(process, 11, "challenge_hypothesis", {"hypothesis":"בדיקת חציית גבול לא מאומתת", "supporting_event_ids": (semantic["result"]["structuredContent"].get("event_ids") or [])[:5]})
        summary = {
            "server": initialized["result"]["serverInfo"],
            "tool_count": len(tools["result"]["tools"]),
            "classified_intent": classified["result"]["structuredContent"]["intent"],
            "classification_source": classified["result"]["structuredContent"].get("classification_source"),
            "resolved_locations": location["result"]["structuredContent"].get("location_ids", [])[:5],
            "search_total": events["result"]["structuredContent"].get("total"),
            "aggregate_groups": aggregate["result"]["structuredContent"].get("groups", [])[:3],
            "identifier_ids": identifier["result"]["structuredContent"].get("event_ids", [])[:5],
            "semantic_ids": semantic["result"]["structuredContent"].get("event_ids", [])[:8],
            "semantic_llm_source": semantic["result"]["structuredContent"].get("llm_assist_source"),
            "related_ids": related["result"]["structuredContent"].get("event_ids", [])[:8],
            "related_llm_source": (related["result"]["structuredContent"].get("llm_rerank") or {}).get("source"),
            "geo_conflict_groups": geo_conflicts["result"]["structuredContent"].get("conflict_group_count", 0),
            "geo_llm_source": (geo_conflicts["result"]["structuredContent"].get("llm_assessment") or {}).get("source"),
            "geo_conflict_ids": (
                (geo_conflicts["result"]["structuredContent"].get("conflict_groups") or [{}])[0].get("event_ids") or []
            )[:8],
            "challenge_llm_source": (challenge["result"]["structuredContent"].get("llm_challenge") or {}).get("source"),
        }
        assert summary["tool_count"] == 16
        assert summary["classified_intent"] == "investigation"
        assert summary["classification_source"] == "mcp_sampling"
        assert summary["resolved_locations"]
        assert summary["search_total"] > 0
        assert summary["semantic_ids"]
        assert summary["semantic_llm_source"] == "mcp_sampling"
        assert summary["related_llm_source"] == "mcp_sampling"
        assert summary["geo_llm_source"] == "mcp_sampling"
        assert summary["challenge_llm_source"] == "mcp_sampling"
        assert summary["geo_conflict_groups"] > 0
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    finally:
        process.terminate()
        process.wait(timeout=5)

if __name__ == "__main__":
    raise SystemExit(main())
