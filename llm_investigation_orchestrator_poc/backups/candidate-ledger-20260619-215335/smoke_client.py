#!/usr/bin/env python3
"""Minimal MCP protocol smoke check for the read-only intelligence server."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SERVER = Path(__file__).with_name("server.py")


def request(process: subprocess.Popen[str], payload: dict) -> dict:
    assert process.stdin is not None
    assert process.stdout is not None
    process.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
    process.stdin.flush()
    line = process.stdout.readline()
    if not line:
        stderr = process.stderr.read() if process.stderr is not None else ""
        raise RuntimeError(f"MCP server exited before responding: {stderr}")
    return json.loads(line)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    process = subprocess.Popen(
        [sys.executable, str(SERVER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    try:
        initialized = request(process, {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "smoke", "version": "1"}},
        })
        tools = request(process, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        classified = request(process, {
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "classify_question_intent", "arguments": {"question": "תראה TOP 3 מיקומים לפי כמות אירועים"}},
        })
        location = request(process, {
            "jsonrpc": "2.0", "id": 4, "method": "tools/call",
            "params": {"name": "resolve_location", "arguments": {"query": "בית שאן"}},
        })
        anchor = request(process, {
            "jsonrpc": "2.0", "id": 5, "method": "tools/call",
            "params": {"name": "resolve_event_reference", "arguments": {"query": "אירוע הגבול"}},
        })
        events = request(process, {
            "jsonrpc": "2.0", "id": 6, "method": "tools/call",
            "params": {"name": "search_events", "arguments": {
                "start_time": "2026-05-17T18:00:00Z", "end_time": "2026-05-18T01:05:00Z",
                "location_ids": ["L-202", "L-204", "L-206", "L-207", "L-203"], "limit": 20,
            }},
        })
        entity = request(process, {
            "jsonrpc": "2.0", "id": 7, "method": "tools/call",
            "params": {"name": "resolve_entity", "arguments": {"query": "אופק מטענים"}},
        })
        identifier = request(process, {
            "jsonrpc": "2.0", "id": 8, "method": "tools/call",
            "params": {"name": "trace_identifier", "arguments": {"identifier": "OF-4482", "identifier_type": "container"}},
        })
        related = request(process, {
            "jsonrpc": "2.0", "id": 9, "method": "tools/call",
            "params": {"name": "find_related_events", "arguments": {
                "seed_event_ids": ["BORD-0001"], "before_hours": 6, "after_hours": 2,
                "distance_km": 15, "limit": 20,
            }},
        })
        challenged = request(process, {
            "jsonrpc": "2.0", "id": 10, "method": "tools/call",
            "params": {"name": "challenge_hypothesis", "arguments": {
                "hypothesis": "רצף תנועה חריג הגיע לאזור בית שאן",
                "supporting_event_ids": ["SIG-0002", "ACOU-0137", "BORD-0001", "DRONE-0001"],
            }},
        })
        actor_history = request(process, {
            "jsonrpc": "2.0", "id": 11, "method": "tools/call",
            "params": {"name": "find_actor_history", "arguments": {
                "actors": ["אופק לוגיסטיקה"],
                "start_time": "2026-05-17T06:00:00Z", "end_time": "2026-05-17T13:00:00Z", "limit": 30,
            }},
        })
        linkage = request(process, {
            "jsonrpc": "2.0", "id": 12, "method": "tools/call",
            "params": {"name": "explain_linkage", "arguments": {
                "first_event_id": "PORT-0090",
                "second_event_id": "CUST-0101",
            }},
        })
        semantic = request(process, {
            "jsonrpc": "2.0", "id": 13, "method": "tools/call",
            "params": {"name": "trace_semantic_clues", "arguments": {
                "clues": ["משאבות", "מחסן 11", "דרך צדדית", "מטען מכוסה", "משאיות"],
                "start_time": "2026-05-17T00:00:00Z",
                "end_time": "2026-05-18T12:00:00Z",
                "limit": 50,
            }},
        })
        planner = request(process, {
            "jsonrpc": "2.0", "id": 14, "method": "tools/call",
            "params": {"name": "plan_next_investigation_step", "arguments": {
                "objective": "בדיקת רצף סביב OF-4482 לכיוון אירוע הגבול",
                "candidate_chain_event_ids": ["PORT-0090", "CUST-0101", "FIN-0098"],
                "pending_recommended_seeds": ["OBS-0002", "MOVE-0134", "SIG-0002"],
                "expanded_seed_event_ids": [],
                "new_clues_to_trace": ["מחסן", "מטען מכוסה"],
                "linkage_checks_done": [],
                "semantic_calls_used": 1,
                "related_calls_used": 1,
                "tool_budget_remaining": 12,
            }},
        })
        summary = {
            "server": initialized["result"]["serverInfo"],
            "tool_count": len(tools["result"]["tools"]),
            "classified_intent": classified["result"]["structuredContent"]["intent"],
            "resolved_locations": location["result"]["structuredContent"]["location_ids"],
            "anchor_ids": anchor["result"]["structuredContent"]["event_ids"],
            "search_total": events["result"]["structuredContent"]["total"],
            "sample_event_ids": events["result"]["structuredContent"]["event_ids"][:5],
            "resolved_entity": entity["result"]["structuredContent"]["matches"][0]["entity_id"],
            "identifier_event_ids": identifier["result"]["structuredContent"]["event_ids"],
            "related_event_ids": related["result"]["structuredContent"]["event_ids"][:8],
            "challenge_alternatives": challenged["result"]["structuredContent"]["alternative_event_ids"][:5],
            "expanded_actors": actor_history["result"]["structuredContent"]["expanded_actors"],
            "linkage_assessment": linkage["result"]["structuredContent"]["assessment"],
            "semantic_event_ids": semantic["result"]["structuredContent"]["event_ids"][:8],
            "planner_next_step": planner["result"]["structuredContent"]["next_step_constraint"],
            "planner_required_event_ids": planner["result"]["structuredContent"]["required_event_ids"],
        }
        assert summary["tool_count"] == 15
        assert summary["classified_intent"] == "geographic_aggregation"
        assert summary["resolved_entity"] == "ENT-OFK"
        assert summary["identifier_event_ids"] == ["PORT-0090", "CUST-0101"]
        assert "ACOU-0137" in related["result"]["structuredContent"]["event_ids"]
        assert "DRONE-0001" in related["result"]["structuredContent"]["event_ids"]
        assert challenged["result"]["structuredContent"]["evidence_profile"]["source_type_count"] >= 3
        assert summary["expanded_actors"] == ["אופק לוגיסטיקה", "אופק מטענים"]
        assert "MOVE-0134" in actor_history["result"]["structuredContent"]["event_ids"]
        assert linkage["result"]["structuredContent"]["bridge_count"] >= 1
        assert "SIG-0002" in semantic["result"]["structuredContent"]["event_ids"]
        assert "ACOU-0137" in semantic["result"]["structuredContent"]["event_ids"]
        assert planner["result"]["structuredContent"]["next_step_constraint"] == "expand_pending_recommended_seeds"
        assert planner["result"]["structuredContent"]["challenge_hypothesis_allowed"] is False
        assert planner["result"]["structuredContent"]["required_event_ids"] == ["OBS-0002", "MOVE-0134", "SIG-0002"]
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    finally:
        process.terminate()
        process.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
