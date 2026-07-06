#!/usr/bin/env python3
"""Run tool-level quality probes directly against the VM-local MCP server."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "docs" / "quality" / "question_catalog_v1.json"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "quality" / "vm_tool_probe_runs"
DEFAULT_SERVER_PATHS = [
    ROOT / "mcp_server" / "server.py",
    Path("/opt/serbia-poc/mcp_server/server.py"),
]


def resolve_server_path() -> Path:
    for path in DEFAULT_SERVER_PATHS:
        if path.exists():
            return path
    return DEFAULT_SERVER_PATHS[0]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def call_tool(process: subprocess.Popen[str], request_id: int, tool: str, arguments: dict[str, Any]) -> tuple[dict[str, Any], float]:
    started = time.perf_counter()
    response = request(
        process,
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {"name": tool, "arguments": arguments},
        },
    )
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    if "error" in response:
        raise RuntimeError(json.dumps(response["error"], ensure_ascii=False))
    result = response.get("result") or {}
    structured = result.get("structuredContent")
    if structured is None:
        content = result.get("content") or []
        if content and isinstance(content[0], dict) and content[0].get("text"):
            structured = json.loads(content[0]["text"])
    return structured or {}, elapsed_ms


def summarize(tool: str, result: dict[str, Any]) -> dict[str, Any]:
    if tool == "semantic_search_events":
        return {
            "backend": result.get("semantic_backend"),
            "returned": result.get("returned"),
            "total": result.get("total"),
            "sample_ids": (result.get("event_ids") or [])[:10],
        }
    if tool == "compare_location_claims":
        conflict_groups = result.get("conflict_groups") or []
        return {
            "candidate_event_count": result.get("candidate_event_count"),
            "conflict_group_count": result.get("conflict_group_count", len(conflict_groups)),
            "returned": result.get("returned"),
            "top_claims": [
                {
                    "conflict_score": group.get("conflict_score"),
                    "event_count": group.get("event_count"),
                    "location_count": group.get("location_count"),
                    "claim_template": group.get("claim_template"),
                }
                for group in conflict_groups[:5]
            ],
        }
    if tool == "aggregate_events":
        return {
            "group_by": result.get("group_by"),
            "total_events": result.get("total_events"),
            "group_count": len(result.get("groups") or []),
            "top_groups": (result.get("groups") or [])[:5],
        }
    if tool == "search_events":
        return {
            "total": result.get("total"),
            "returned": result.get("returned"),
            "truncated": result.get("truncated"),
            "sample_ids": (result.get("event_ids") or [])[:10],
        }
    if tool == "resolve_location":
        return {
            "location_ids": result.get("location_ids") or [],
            "match_count": result.get("match_count"),
        }
    if tool == "resolve_entity":
        return {
            "match_count": result.get("match_count"),
            "entity_ids": [item.get("entity_id") for item in result.get("matches") or []],
        }
    if tool == "classify_question_intent":
        return {
            "intent": result.get("intent"),
            "recommended_mode": result.get("recommended_mode"),
            "recommended_view_hint": result.get("recommended_view_hint"),
            "tool_budget": result.get("tool_budget"),
            "classification_source": result.get("classification_source") or result.get("source"),
        }
    if tool == "plan_next_investigation_step":
        return {
            "decision": result.get("decision"),
            "next_step_constraint": result.get("next_step_constraint"),
            "required_event_ids": result.get("required_event_ids") or [],
            "required_clues": result.get("required_clues") or [],
        }
    return {"keys": sorted(result.keys())[:30]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="*", default=[])
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    probes = catalog["tool_level_probes"]
    if args.ids:
        wanted = set(args.ids)
        probes = [probe for probe in probes if probe["id"] in wanted]
        missing = wanted - {probe["id"] for probe in probes}
        if missing:
            raise SystemExit(f"Unknown probe IDs: {', '.join(sorted(missing))}")
    elif not args.all:
        raise SystemExit("Provide --ids ... or --all")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    server_path = resolve_server_path()
    process = subprocess.Popen(
        [sys.executable, str(server_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    results: list[dict[str, Any]] = []
    try:
        request(
            process,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "tool-probe-runner", "version": "1"},
                },
            },
        )
        request_id = 2
        for probe in probes:
            probe_id = probe["id"]
            tool = probe["tool"]
            arguments = probe.get("arguments") or probe.get("input") or {}
            print(f"RUN_START {probe_id}: {tool}", flush=True)
            try:
                result, elapsed_ms = call_tool(process, request_id, tool, arguments)
                record = {
                    "id": probe_id,
                    "tool": tool,
                    "status": "completed",
                    "elapsed_ms": elapsed_ms,
                    "arguments": arguments,
                    "summary": summarize(tool, result),
                    "result": result,
                }
            except Exception as exc:  # noqa: BLE001
                record = {
                    "id": probe_id,
                    "tool": tool,
                    "status": "failed",
                    "arguments": arguments,
                    "error": str(exc),
                }
            results.append(record)
            request_id += 1
            printable = {k: record.get(k) for k in ("id", "tool", "status", "elapsed_ms", "summary", "error") if k in record}
            print(json.dumps({"RUN_DONE": printable}, ensure_ascii=False), flush=True)
    finally:
        process.terminate()
        process.wait(timeout=5)

    artifact = {
        "catalog_id": catalog.get("catalog_id"),
        "recorded_at_utc": utc_now(),
        "source": "vm_local_mcp_direct",
        "probe_count": len(results),
        "completed": sum(1 for item in results if item["status"] == "completed"),
        "failed": sum(1 for item in results if item["status"] == "failed"),
        "results": results,
    }
    output_path = args.output_dir / f"tool_probes_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    output_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"OUTPUT": output_path.as_posix(), "completed": artifact["completed"], "failed": artifact["failed"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
