#!/usr/bin/env python3
"""Regression quality gate for the Serbia/Kosovo MCP tools.

The goal is to catch tool-level degradation before changing deterministic tools
into hybrid or LLM-assisted tools. It covers three layers:
1. MCP/tool contract validity.
2. Full structured-output snapshots for before/after comparison.
3. Oracle-label quality metrics for returned event IDs.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SERVER = Path(__file__).with_name("server.py")
LABELS = ROOT / "data" / "serbia_kosovo_evaluator_labels.csv"
TEST_RUNS = ROOT / "test_runs"


REQUIRED_KEYS: dict[str, set[str]] = {
    "classify_question_intent": {
        "intent",
        "recommended_mode",
        "recommended_view_hint",
        "confidence",
        "classification_source",
    },
    "plan_next_investigation_step": {"decision", "next_step_constraint"},
    "search_events": {"total", "returned", "event_ids", "events"},
    "get_events": {"events", "missing_event_ids"},
    "resolve_location": {"location_ids"},
    "resolve_event_reference": {"event_ids"},
    "find_actor_history": {"total", "returned", "event_ids", "events"},
    "aggregate_events": {"group_by", "total_events", "groups"},
    "explain_linkage": {"bridge_count", "bridges", "assessment"},
    "build_event_sequence": {"event_count", "events"},
    "resolve_entity": {"match_count", "matches"},
    "trace_identifier": {"total_mentions", "returned", "event_ids", "events"},
    "trace_semantic_clues": {
        "total_matches",
        "returned",
        "event_ids",
        "matches",
        "recommended_next_seeds",
        "new_clues_to_trace",
    },
    "find_related_events": {
        "total_candidates",
        "returned",
        "event_ids",
        "related_events",
        "recommended_next_seeds",
        "new_clues_to_trace",
    },
    "compare_location_claims": {"conflict_group_count", "conflict_groups"},
    "challenge_hypothesis": {"evidence_profile", "alternative_event_ids", "gaps"},
}


def sampling_payload(raw_text: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    try:
        params = json.loads(raw_text)
        messages = params.get("messages") or []
        if messages:
            content = (messages[0].get("content") or {}).get("text") or ""
            parsed = json.loads(content)
    except (json.JSONDecodeError, AttributeError, IndexError, TypeError):
        parsed = {}

    task = parsed.get("task")
    if task == "resolve_event_reference_terms":
        query = str(parsed.get("query") or "")
        if "חציית גבול" in query:
            return {
                "search_phrases": ["חציית גבול", "גבול", "אין לכך אימות", "מכחישים"],
                "location_terms": ["גבול"],
                "actor_terms": ["חשבונות", "מקורות אחרים"],
                "rationale": "השאילתה מחפשת טענה על גבול והצלבת אמינות.",
            }
        return {
            "search_phrases": ["ירי", "חסימה", "רכבים ביטחוניים", "אירוע טקטי"],
            "location_terms": ["זבצ׳אן"],
            "actor_terms": ["KFOR", "משטרת קוסובו"],
            "rationale": "הפניה לאירוע טקטי ליד זבצ׳אן מתורגמת לרמזי ירי, חסימה וכוחות.",
        }
    if task == "trace_semantic_clues_expand":
        return {
            "expanded_clues": ["הכחשה", "דיווח לא מאומת", "שיירה", "רכבים ביטחוניים"],
            "rationale": "הרמזים מצביעים על צורך לחפש גם שפה של הכחשה, אימות ותנועה.",
        }
    if task == "find_related_events_rerank":
        candidates = parsed.get("candidate_events") or []
        return {
            "top_event_ids": [item.get("event_id") for item in candidates[:8] if item.get("event_id")],
            "rationale": "נבחרו המועמדים הראשונים לאחר הסינון הדטרמיניסטי לצורך בדיקת יציבות.",
        }
    if task == "compare_location_claims_assess":
        return {
            "assessment": "יש דפוס של טענות דומות שמופיעות במספר מיקומים, עם אמינות או ודאות חלשה בחלק מהקבוצות.",
            "strongest_group_indexes": [0, 1],
            "caution": "אין לקבוע מיקום נכון ללא הצלבה נוספת.",
        }
    if task == "challenge_hypothesis_reasoning":
        return {
            "competing_hypotheses": ["דפוס הסלמה אמיתי", "רעש מידע סביב אירועים אזרחיים", "הפצה חוזרת של שמועות דומות"],
            "disproof_tests": ["להצליב עם מקורות אמינים", "לבדוק רצף זמן", "לחפש הכחשות", "לבדוק מיקומים סמוכים"],
            "synthesis": "הראיות תומכות בבדיקה נוספת אך אינן מכריעות ללא הצלבה בין מקורות וזמן.",
        }

    question = raw_text
    if any(term in question for term in ("תמיין", "זמן", "ציר זמן", "כרונולוג")):
        return {
            "intent": "timeline_retrieval",
            "recommended_mode": "retrieval",
            "recommended_view_hint": "timeline",
            "confidence": "גבוהה",
            "reason": "השאלה מבקשת סידור כרונולוגי של אירועים.",
        }
    if any(term in question for term in ("TOP", "מוקדי", "מיקומים", "אגרג")):
        return {
            "intent": "geographic_aggregation",
            "recommended_mode": "retrieval",
            "recommended_view_hint": "map",
            "confidence": "גבוהה",
            "reason": "השאלה מבקשת ריכוזים גאוגרפיים ואגרגציה לפי מקום.",
        }
    return {
        "intent": "investigation",
        "recommended_mode": "investigation",
        "recommended_view_hint": "evidence",
        "confidence": "גבוהה",
        "reason": "השאלה מבקשת לבדוק אמינות, קשרים, סתירות וחלופות.",
    }


def request(process: subprocess.Popen[str], payload: dict[str, Any]) -> dict[str, Any]:
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
            text = json.dumps(
                sampling_payload(json.dumps(message.get("params") or {}, ensure_ascii=False)),
                ensure_ascii=False,
            )
            process.stdin.write(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "result": {
                            "role": "assistant",
                            "content": {"type": "text", "text": text},
                            "model": "mock-sampling",
                            "stopReason": "endTurn",
                        },
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            process.stdin.flush()
            continue
        return message


def call_tool(
    process: subprocess.Popen[str],
    request_id: int,
    name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    started = time.perf_counter()
    response = request(
        process,
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    if "error" in response:
        raise RuntimeError(f"{name} failed: {response['error']}")
    return {
        "tool": name,
        "arguments": arguments,
        "elapsed_ms": round(elapsed_ms, 3),
        "structured": response["result"]["structuredContent"],
    }


def scenario_calls() -> list[tuple[str, dict[str, Any]]]:
    max_limit = 500
    evidence_ids = [
        "REC-062762",
        "REC-084560",
        "REC-017577",
        "REC-019675",
        "REC-063664",
        "REC-007880",
        "REC-065238",
        "REC-038159",
        "REC-032521",
        "REC-063921",
    ]
    return [
        ("classify_question_intent", {"question": "תראה TOP 3 מיקומים לפי כמות אירועים"}),
        ("classify_question_intent", {"question": "תמיין לפי זמן את האירועים המרכזיים כדי לקבל תמונה"}),
        (
            "classify_question_intent",
            {"question": "האם הטענה על חציית גבול מגובה במקור אמין? חפש מקורות, סתירות וחלופות."},
        ),
        ("resolve_location", {"query": "צפון מיטרוביצה זבצ׳אן זובין פוטוק לפוסאביץ׳"}),
        ("resolve_event_reference", {"query": "אירוע טקטי ליד זבצ׳אן"}),
        ("resolve_event_reference", {"query": "דיווח שקרי על חציית גבול"}),
        ("search_events", {"keywords": ["חציית גבול"], "limit": max_limit}),
        (
            "search_events",
            {
                "start_time": "2026-09-12T00:00:00Z",
                "end_time": "2026-09-22T23:59:59Z",
                "location_ids": ["LOC-001", "LOC-002", "LOC-003", "LOC-004", "LOC-005", "LOC-006"],
                "keywords": ["חציית גבול", "חסימה", "KFOR", "משטרת קוסובו", "מקורות אחרים", "חשבונות"],
                "match_all_keywords": False,
                "limit": max_limit,
            },
        ),
        ("get_events", {"event_ids": evidence_ids}),
        (
            "find_actor_history",
            {
                "actors": ["KFOR", "EULEX", "משטרת קוסובו", "מפגינים סרבים מקומיים"],
                "start_time": "2026-09-12T00:00:00Z",
                "end_time": "2026-09-22T23:59:59Z",
                "limit": max_limit,
            },
        ),
        ("aggregate_events", {"group_by": "location", "top_n": 5, "limit": max_limit}),
        ("aggregate_events", {"group_by": "municipality", "top_n": 5, "limit": max_limit}),
        ("aggregate_events", {"group_by": "source", "limit": max_limit}),
        ("aggregate_events", {"group_by": "hour", "limit": max_limit}),
        ("explain_linkage", {"first_event_id": "REC-062762", "second_event_id": "REC-084560"}),
        ("explain_linkage", {"first_event_id": "REC-017577", "second_event_id": "REC-019675"}),
        ("build_event_sequence", {"event_ids": evidence_ids}),
        ("resolve_entity", {"query": "KFOR"}),
        ("resolve_entity", {"query": "משטרת קוסובו"}),
        ("trace_identifier", {"identifier": "REC-017577", "identifier_type": "record"}),
        ("trace_identifier", {"identifier": "REC-017577", "identifier_type": "record", "include_negated": True}),
        ("trace_identifier", {"identifier": "LOC-001", "identifier_type": "location"}),
        (
            "trace_semantic_clues",
            {
                "clues": ["חציית גבול", "מקורות אחרים", "חשבונות", "KFOR", "ירי", "חסימה"],
                "start_time": "2026-09-12T00:00:00Z",
                "end_time": "2026-09-22T23:59:59Z",
                "limit": max_limit,
            },
        ),
        (
            "plan_next_investigation_step",
            {
                "objective": "בדיקת אמינות הטענה על חציית גבול והאם היא חלק מדפוס הסלמה",
                "candidate_chain_event_ids": ["REC-062762", "REC-084560", "REC-017577"],
                "pending_recommended_seeds": ["REC-019675", "REC-063664", "REC-007880"],
                "expanded_seed_event_ids": [],
                "new_clues_to_trace": ["מקורות אחרים", "חשבונות"],
                "linkage_checks_done": [],
                "semantic_calls_used": 1,
                "related_calls_used": 1,
                "tool_budget_remaining": 12,
            },
        ),
        (
            "find_related_events",
            {
                "seed_event_ids": ["REC-062762", "REC-084560", "REC-017577", "REC-019675"],
                "dimensions": ["entity", "identifier", "semantic", "time", "location"],
                "before_hours": 72,
                "after_hours": 24,
                "distance_km": 500,
                "limit": max_limit,
            },
        ),
        (
            "find_related_events",
            {
                "seed_event_ids": ["REC-062762", "REC-084560", "REC-017577", "REC-019675"],
                "dimensions": ["entity", "identifier", "semantic", "time", "location"],
                "source_types": ["טלגרם", "טיקטוק", "הודעת דובר", "שמועה מקומית"],
                "before_hours": 72,
                "after_hours": 24,
                "distance_km": 500,
                "limit": max_limit,
            },
        ),
        (
            "compare_location_claims",
            {
                "keywords": ["חציית גבול", "גבול", "מכחישים", "אין לכך אימות"],
                "start_time": "2026-09-12T00:00:00Z",
                "end_time": "2026-09-22T23:59:59Z",
                "limit": max_limit,
            },
        ),
        (
            "challenge_hypothesis",
            {
                "hypothesis": "הטענה על חציית גבול היא חלק מדפוס הסלמה מבוסס דיווחים ולא אירוע מבודד",
                "supporting_event_ids": evidence_ids,
            },
        ),
    ]


def load_labels() -> dict[str, dict[str, str]]:
    labels: dict[str, dict[str, str]] = {}
    with LABELS.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            labels[row["event_id"]] = row
    return labels


def collect_event_ids(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in {"event_id", "record_id"} and isinstance(nested, str) and nested.startswith("REC-"):
                found.append(nested)
            elif key == "event_ids" and isinstance(nested, list):
                found.extend(item for item in nested if isinstance(item, str) and item.startswith("REC-"))
            else:
                found.extend(collect_event_ids(nested))
    elif isinstance(value, list):
        for item in value:
            found.extend(collect_event_ids(item))
    return list(dict.fromkeys(found))


def as_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def event_quality(event_ids: list[str], labels: dict[str, dict[str, str]]) -> dict[str, Any]:
    labelled = [labels[event_id] for event_id in event_ids if event_id in labels]
    if not labelled:
        return {
            "event_count": len(event_ids),
            "labelled_count": 0,
            "scenario_coverage": 0,
            "avg_relevance": None,
        }

    relevance_values = [
        int(row["relevance_label"])
        for row in labelled
        if (row.get("relevance_label") or "").isdigit()
    ]
    counters = {
        "scenario_event_ids": Counter(row.get("scenario_event_id") or "unknown" for row in labelled),
        "source_reliability": Counter(row.get("source_reliability_label") or "unknown" for row in labelled),
        "ground_truth_status": Counter(row.get("ground_truth_status") or "unknown" for row in labelled),
        "misleading_type": Counter(row.get("misleading_type") or "none" for row in labelled),
    }
    return {
        "event_count": len(event_ids),
        "labelled_count": len(labelled),
        "scenario_coverage": len(counters["scenario_event_ids"]),
        "avg_relevance": round(statistics.mean(relevance_values), 3) if relevance_values else None,
        "military_related": sum(as_bool(row.get("is_military_related", "")) for row in labelled),
        "civilian_related": sum(as_bool(row.get("is_civilian_related", "")) for row in labelled),
        "rumor": sum(as_bool(row.get("is_rumor", "")) for row in labelled),
        "disinformation": sum(as_bool(row.get("is_disinformation", "")) for row in labelled),
        "possible_misidentification": sum(as_bool(row.get("possible_misidentification", "")) for row in labelled),
        "media_claimed": sum(as_bool(row.get("media_claimed", "")) for row in labelled),
        "top_scenario_event_ids": counters["scenario_event_ids"].most_common(8),
        "source_reliability": counters["source_reliability"].most_common(),
        "ground_truth_status": counters["ground_truth_status"].most_common(),
        "misleading_type": counters["misleading_type"].most_common(8),
    }


def validate_contract(result: dict[str, Any]) -> list[str]:
    tool = result["tool"]
    structured = result["structured"]
    required = REQUIRED_KEYS.get(tool, set())
    missing = sorted(key for key in required if key not in structured)
    failures = [f"{tool}: missing structured key '{key}'" for key in missing]
    if "event_ids" in structured and "returned" in structured:
        event_ids = structured.get("event_ids") or []
        returned = structured.get("returned")
        if isinstance(returned, int) and returned != len(event_ids):
            failures.append(f"{tool}: returned={returned} but event_ids has {len(event_ids)} IDs")
    if tool == "classify_question_intent" and structured.get("classification_source") not in {
        "mcp_sampling",
        "deterministic_fallback",
    }:
        failures.append(f"{tool}: unexpected classification_source={structured.get('classification_source')}")
    return failures


def compare_snapshots(current: dict[str, Any], previous_path: Path) -> dict[str, Any]:
    previous = json.loads(previous_path.read_text(encoding="utf-8"))
    previous_by_call = {
        (item["tool"], json.dumps(item["arguments"], sort_keys=True, ensure_ascii=False)): item
        for item in previous.get("results", [])
    }
    comparisons = []
    for item in current["results"]:
        key = (item["tool"], json.dumps(item["arguments"], sort_keys=True, ensure_ascii=False))
        old = previous_by_call.get(key)
        if not old:
            comparisons.append({"tool": item["tool"], "status": "new_call"})
            continue
        old_ids = set(collect_event_ids(old["structured"]))
        new_ids = set(collect_event_ids(item["structured"]))
        union = old_ids | new_ids
        comparisons.append(
            {
                "tool": item["tool"],
                "status": "matched",
                "old_event_count": len(old_ids),
                "new_event_count": len(new_ids),
                "event_overlap": len(old_ids & new_ids),
                "event_jaccard": round(len(old_ids & new_ids) / len(union), 3) if union else 1.0,
            }
        )
    return {"baseline": str(previous_path), "calls": comparisons}


def run_suite(compare: Path | None) -> dict[str, Any]:
    labels = load_labels()
    process = subprocess.Popen(
        [sys.executable, str(SERVER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    try:
        initialized = request(
            process,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {"sampling": {}},
                    "clientInfo": {"name": "regression-quality", "version": "1"},
                },
            },
        )
        tools = request(process, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        request_id = 3
        results = []
        failures = []
        for name, arguments in scenario_calls():
            item = call_tool(process, request_id, name, arguments)
            item["event_ids_seen"] = collect_event_ids(item["structured"])
            item["quality"] = event_quality(item["event_ids_seen"], labels)
            failures.extend(validate_contract(item))
            results.append(item)
            request_id += 1

        elapsed_values = [item["elapsed_ms"] for item in results]
        by_tool: dict[str, list[float]] = {}
        for item in results:
            by_tool.setdefault(item["tool"], []).append(item["elapsed_ms"])

        report = {
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "server": initialized["result"]["serverInfo"],
            "tool_count": len(tools["result"]["tools"]),
            "tools_covered": sorted(by_tool),
            "call_count": len(results),
            "failures": failures,
            "performance": {
                "total_ms": round(sum(elapsed_values), 3),
                "mean_ms": round(statistics.mean(elapsed_values), 3),
                "max_ms": round(max(elapsed_values), 3),
                "by_tool": {
                    tool: {
                        "calls": len(values),
                        "mean_ms": round(statistics.mean(values), 3),
                        "max_ms": round(max(values), 3),
                    }
                    for tool, values in sorted(by_tool.items())
                },
            },
            "quality_rollup": {
                item["tool"]: item["quality"]
                for item in results
                if item["quality"]["labelled_count"] > 0
            },
            "results": results,
        }
        if compare:
            report["comparison"] = compare_snapshots(report, compare)
        return report
    finally:
        process.terminate()
        process.wait(timeout=5)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", type=Path, help="Compare event-ID stability with an earlier JSON report")
    parser.add_argument("--json", action="store_true", help="Print full JSON report")
    args = parser.parse_args()

    TEST_RUNS.mkdir(parents=True, exist_ok=True)
    report = run_suite(args.compare)
    output_path = TEST_RUNS / f"regression_quality_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    compact = {
        "output_path": str(output_path),
        "tool_count": report["tool_count"],
        "call_count": report["call_count"],
        "failure_count": len(report["failures"]),
        "failures": report["failures"],
        "performance": report["performance"],
        "quality_tools": sorted(report["quality_rollup"]),
    }
    if "comparison" in report:
        compact["comparison"] = report["comparison"]

    print(json.dumps(report if args.json else compact, ensure_ascii=False, indent=2))
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
