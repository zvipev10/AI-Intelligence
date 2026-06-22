#!/usr/bin/env python3
"""Benchmark the synthetic intelligence MCP tools with a broad scenario."""

from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


SERVER = Path(__file__).with_name("server.py")


def request(process: subprocess.Popen[str], payload: dict[str, Any]) -> dict[str, Any]:
    assert process.stdin is not None
    assert process.stdout is not None
    process.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
    process.stdin.flush()
    line = process.stdout.readline()
    if not line:
        stderr = process.stderr.read() if process.stderr is not None else ""
        raise RuntimeError(f"MCP server exited before responding: {stderr}")
    return json.loads(line)


def call_tool(process: subprocess.Popen[str], request_id: int, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    response = request(process, {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    })
    elapsed_ms = (time.perf_counter() - started) * 1000
    if "error" in response:
        raise RuntimeError(response["error"])
    structured = response["result"]["structuredContent"]
    return {
        "tool": name,
        "arguments": arguments,
        "elapsed_ms": elapsed_ms,
        "summary": summarize_result(name, structured),
    }


def summarize_result(name: str, result: dict[str, Any]) -> dict[str, Any]:
    if name == "classify_question_intent":
        return {
            "intent": result.get("intent"),
            "mode": result.get("recommended_mode"),
            "tool_budget": result.get("tool_budget"),
        }
    if name in {"search_events", "find_actor_history"}:
        return {
            "total": result.get("total"),
            "returned": result.get("returned"),
            "sample_event_ids": (result.get("event_ids") or [])[:5],
        }
    if name == "get_events":
        return {
            "returned": len(result.get("events") or []),
            "missing": result.get("missing_event_ids") or [],
        }
    if name == "resolve_location":
        return {"location_ids": result.get("location_ids") or []}
    if name == "resolve_event_reference":
        return {"event_ids": result.get("event_ids") or []}
    if name == "aggregate_events":
        return {
            "group_by": result.get("group_by"),
            "total_events": result.get("total_events"),
            "top_groups": (result.get("groups") or [])[:5],
        }
    if name == "explain_linkage":
        return {
            "bridge_count": result.get("bridge_count"),
            "strongest_bridge": (result.get("strongest_bridge") or {}).get("bridge_type"),
            "assessment": result.get("assessment"),
        }
    if name == "build_event_sequence":
        return {
            "event_count": result.get("event_count"),
            "start_time": result.get("start_time"),
            "end_time": result.get("end_time"),
        }
    if name == "resolve_entity":
        return {
            "match_count": result.get("match_count"),
            "matches": [item.get("entity_id") for item in result.get("matches") or []],
        }
    if name == "trace_identifier":
        return {
            "total_mentions": result.get("total_mentions"),
            "returned": result.get("returned"),
            "event_ids": result.get("event_ids") or [],
            "excluded_negated_mentions": result.get("excluded_negated_mentions"),
        }
    if name == "trace_semantic_clues":
        return {
            "total_matches": result.get("total_matches"),
            "returned": result.get("returned"),
            "sample_event_ids": (result.get("event_ids") or [])[:8],
            "recommended_next_seeds": [item.get("event_id") for item in result.get("recommended_next_seeds") or []],
            "new_clues_to_trace": result.get("new_clues_to_trace") or [],
        }
    if name == "plan_next_investigation_step":
        return {
            "decision": result.get("decision"),
            "next_step_constraint": result.get("next_step_constraint"),
            "required_event_ids": result.get("required_event_ids") or [],
            "required_clues": result.get("required_clues") or [],
            "blocked_tool_families": result.get("blocked_tool_families") or [],
        }
    if name == "find_related_events":
        return {
            "total_candidates": result.get("total_candidates"),
            "returned": result.get("returned"),
            "sample_event_ids": (result.get("event_ids") or [])[:8],
            "recommended_next_seeds": [item.get("event_id") for item in result.get("recommended_next_seeds") or []],
            "new_clues_to_trace": result.get("new_clues_to_trace") or [],
        }
    if name == "challenge_hypothesis":
        profile = result.get("evidence_profile") or {}
        return {
            "event_count": profile.get("event_count"),
            "source_type_count": profile.get("source_type_count"),
            "alternative_count": len(result.get("alternative_event_ids") or []),
            "gap_count": len(result.get("gaps") or []),
        }
    return {}


def scenario_calls() -> list[tuple[str, dict[str, Any]]]:
    max_limit = 500
    evidence_ids = [
        "PORT-0090", "CUST-0101", "FIN-0098", "TEL-0112", "MOVE-0134",
        "OBS-0002", "CAM-0153", "SIG-0002", "ACOU-0137", "BORD-0001",
        "DRONE-0001", "FIN-0144", "TEL-0152",
    ]
    return [
        ("classify_question_intent", {"question": "תראה TOP 3 מיקומים לפי כמות אירועים"}),
        ("classify_question_intent", {"question": "האם אירוע הגבול הוא אירוע מקומי או חלק מדפוס רחב יותר? חפש קשרים נסתרים וחלופות."}),
        ("resolve_location", {"query": "חיפה בית שאן מעבר הגבול צומת גולני"}),
        ("resolve_event_reference", {"query": "אירוע הגבול"}),
        ("search_events", {"limit": max_limit}),
        ("search_events", {
            "start_time": "2026-05-15T00:00:00Z",
            "end_time": "2026-05-19T23:59:59Z",
            "location_ids": ["L-201", "L-202", "L-203", "L-204", "L-206", "L-207", "L-208"],
            "keywords": ["מכולה", "משאיות", "מטען", "מחסן", "כבדים", "מעבר"],
            "match_all_keywords": False,
            "limit": max_limit,
        }),
        ("get_events", {"event_ids": evidence_ids}),
        ("find_actor_history", {
            "actors": ["אופק לוגיסטיקה", "אופק מטענים", "יחידת תיאום מכס חיפה", "קואופרטיב דלק העמק"],
            "start_time": "2026-05-15T00:00:00Z",
            "end_time": "2026-05-19T23:59:59Z",
            "limit": max_limit,
        }),
        ("aggregate_events", {"group_by": "location", "top_n": 3, "limit": max_limit}),
        ("aggregate_events", {"group_by": "source", "limit": max_limit}),
        ("aggregate_events", {"group_by": "actor", "limit": max_limit}),
        ("explain_linkage", {"first_event_id": "PORT-0090", "second_event_id": "CUST-0101"}),
        ("explain_linkage", {"first_event_id": "OBS-0002", "second_event_id": "CAM-0153"}),
        ("build_event_sequence", {"event_ids": evidence_ids}),
        ("resolve_entity", {"query": "אופק מטענים"}),
        ("resolve_entity", {"query": "א. לוי"}),
        ("trace_identifier", {
            "identifier": "OF-4482",
            "identifier_type": "container",
            "start_time": "2026-05-16T00:00:00Z",
            "end_time": "2026-05-18T23:59:59Z",
            "source_types": ["רישום נמל", "רישום מכס", "חיישן תנועה"],
        }),
        ("trace_identifier", {"identifier": "OF-4482", "identifier_type": "container", "include_negated": True}),
        ("trace_identifier", {"identifier": "מחסן 11", "identifier_type": "warehouse"}),
        ("trace_semantic_clues", {
            "clues": ["משאבות", "מחסן 11", "דרך צדדית", "מטען מכוסה", "משאיות", "כלי רכב כבדים"],
            "start_time": "2026-05-17T00:00:00Z",
            "end_time": "2026-05-18T12:00:00Z",
            "limit": max_limit,
        }),
        ("plan_next_investigation_step", {
            "objective": "בדיקת רצף סביב OF-4482 לכיוון אירוע הגבול",
            "candidate_chain_event_ids": ["PORT-0090", "CUST-0101", "FIN-0098"],
            "pending_recommended_seeds": ["OBS-0002", "MOVE-0134", "SIG-0002"],
            "expanded_seed_event_ids": [],
            "new_clues_to_trace": ["מחסן", "מטען מכוסה"],
            "linkage_checks_done": [],
            "semantic_calls_used": 1,
            "related_calls_used": 1,
            "tool_budget_remaining": 12,
        }),
        ("find_related_events", {
            "seed_event_ids": ["BORD-0001", "DRONE-0001", "ACOU-0137", "OBS-0002"],
            "dimensions": ["entity", "identifier", "semantic", "time", "location"],
            "before_hours": 72,
            "after_hours": 24,
            "distance_km": 500,
            "limit": max_limit,
        }),
        ("find_related_events", {
            "seed_event_ids": ["BORD-0001", "DRONE-0001", "ACOU-0137", "OBS-0002"],
            "dimensions": ["entity", "identifier", "semantic", "time", "location"],
            "source_types": ["מטא-דאטה טלפוני", "יירוט אות", "התראה פיננסית"],
            "before_hours": 72,
            "after_hours": 24,
            "distance_km": 500,
            "limit": max_limit,
        }),
        ("challenge_hypothesis", {
            "hypothesis": "רצף רב-מקורי סביב OF-4482 קשור לאירוע הגבול",
            "supporting_event_ids": evidence_ids,
        }),
    ]


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((pct / 100) * (len(ordered) - 1))))
    return ordered[index]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=3, help="Number of benchmark rounds")
    parser.add_argument("--json", action="store_true", help="Print full JSON result")
    args = parser.parse_args()

    process = subprocess.Popen(
        [sys.executable, str(SERVER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    try:
        request(process, {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "benchmark", "version": "1"},
            },
        })
        calls = scenario_calls()
        results = []
        request_id = 2
        for round_index in range(args.rounds):
            for name, tool_args in calls:
                results.append({"round": round_index + 1, **call_tool(process, request_id, name, tool_args)})
                request_id += 1

        by_tool: dict[str, list[float]] = {}
        for result in results:
            by_tool.setdefault(result["tool"], []).append(result["elapsed_ms"])

        summary = {
            "rounds": args.rounds,
            "call_count": len(results),
            "tools_covered": sorted(by_tool),
            "overall": {
                "total_ms": round(sum(item["elapsed_ms"] for item in results), 3),
                "mean_ms": round(statistics.mean(item["elapsed_ms"] for item in results), 3),
                "p50_ms": round(percentile([item["elapsed_ms"] for item in results], 50), 3),
                "p95_ms": round(percentile([item["elapsed_ms"] for item in results], 95), 3),
                "max_ms": round(max(item["elapsed_ms"] for item in results), 3),
            },
            "by_tool": {
                tool: {
                    "calls": len(values),
                    "mean_ms": round(statistics.mean(values), 3),
                    "p50_ms": round(percentile(values, 50), 3),
                    "p95_ms": round(percentile(values, 95), 3),
                    "max_ms": round(max(values), 3),
                }
                for tool, values in sorted(by_tool.items())
            },
            "sample_results": results[:len(calls)],
        }

        if args.json:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            print(f"Rounds: {summary['rounds']} | Calls: {summary['call_count']}")
            print("Overall:", json.dumps(summary["overall"], ensure_ascii=False))
            for tool, stats in summary["by_tool"].items():
                print(f"{tool}: {json.dumps(stats, ensure_ascii=False)}")
        return 0
    finally:
        process.terminate()
        process.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
