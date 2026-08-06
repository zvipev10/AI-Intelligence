#!/usr/bin/env python3
"""Compare semantic integration tool probes against a previous server version."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MCP_DIR = ROOT / "mcp_server"
CATALOG_PATH = ROOT / "docs" / "quality" / "question_catalog_v1.json"
GOLD_PATH = ROOT / "docs" / "quality" / "semantic_tool_integration_gold_v2.json"
OUTPUT_DIR = ROOT / "docs" / "quality" / "semantic_tool_integration_runs"


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_current_server() -> ModuleType:
    sys.path.insert(0, str(MCP_DIR))
    spec = importlib.util.spec_from_file_location("current_server", MCP_DIR / "server.py")
    if not spec or not spec.loader:
        raise RuntimeError("Could not load current server module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_previous_server(commit: str) -> ModuleType:
    sys.path.insert(0, str(MCP_DIR))
    source = subprocess.check_output(
        ["git", "show", f"{commit}:llm_investigation_orchestrator_serbia_poc/mcp_server/server.py"],
        text=True,
        encoding="utf-8",
    )
    module = ModuleType(f"server_{commit}")
    module.__file__ = str(MCP_DIR / "server.py")
    exec(compile(source, str(MCP_DIR / "server.py"), "exec"), module.__dict__)
    return module


def rank_metrics(found_ids: list[str], gold_ids: list[str]) -> dict[str, Any]:
    ranks = {event_id: found_ids.index(event_id) + 1 for event_id in gold_ids if event_id in found_ids}
    return {
        "gold_count": len(gold_ids),
        "found_count": len(ranks),
        "recall": round(len(ranks) / len(gold_ids), 3) if gold_ids else None,
        "top10": sum(rank <= 10 for rank in ranks.values()),
        "top20": sum(rank <= 20 for rank in ranks.values()),
        "top50": sum(rank <= 50 for rank in ranks.values()),
        "missing_ids": [event_id for event_id in gold_ids if event_id not in ranks],
        "ranks": ranks,
    }


def extract_reason_dimensions(result: dict[str, Any]) -> list[str]:
    dimensions: list[str] = []
    for item in result.get("related_events") or []:
        for reason in item.get("reasons") or []:
            dimension = reason.get("dimension")
            if dimension and dimension not in dimensions:
                dimensions.append(dimension)
    return dimensions


def summarize_result(result: dict[str, Any], gold: dict[str, Any]) -> dict[str, Any]:
    event_ids = result.get("event_ids") or []
    if not event_ids and result.get("events"):
        event_ids = [event.get("event_id") for event in result.get("events") or [] if event.get("event_id")]
    summary = {
        "returned": result.get("returned", len(event_ids)),
        "event_ids": event_ids,
        "top10": event_ids[:10],
        "semantic_candidate_count": result.get("semantic_candidate_count"),
        "semantic_backend": result.get("semantic_backend"),
        "must_find": rank_metrics(event_ids, gold.get("must_find_event_ids") or []),
        "high_value": rank_metrics(event_ids, gold.get("high_value_event_ids") or []),
        "bad_priority_hits_top10": [
            event_id for event_id in gold.get("must_not_prioritize_event_ids", []) if event_id in event_ids[:10]
        ],
        "reason_dimensions": extract_reason_dimensions(result),
    }
    return summary


def run_probe(module: ModuleType, probe: dict[str, Any]) -> dict[str, Any]:
    if hasattr(module, "SEMANTIC_INDEX"):
        module.SEMANTIC_INDEX = None
    function = getattr(module, probe["tool"])
    return function(probe.get("arguments") or {})


def score_status(summary: dict[str, Any], gold: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "min_returned": summary["returned"] >= int(gold.get("expected_min_returned") or 0),
        "semantic_candidate_count": (
            (summary.get("semantic_candidate_count") or 0) >= int(gold.get("expected_semantic_candidate_count_min") or 0)
        ),
        "semantic_backend": (
            not gold.get("expected_semantic_backend")
            or summary.get("semantic_backend") == gold.get("expected_semantic_backend")
        ),
        "must_find_recall": summary["must_find"]["found_count"] == summary["must_find"]["gold_count"],
        "bad_priority_top10": not summary["bad_priority_hits_top10"],
        "reason_dimensions": all(
            dimension in summary.get("reason_dimensions", [])
            for dimension in gold.get("expected_reason_dimensions", [])
        ),
    }
    return {"passed": all(checks.values()), "checks": checks}


def markdown_report(result: dict[str, Any]) -> str:
    lines = [
        "# Semantic Tool Integration Comparison",
        "",
        f"Previous commit: `{result['previous_commit']}`",
        f"Current commit: `{result['current_commit']}`",
        "",
        "| Probe | Tool | Previous returned | Current returned | Previous must | Current must | Current high top20 | Current semantic candidates | Current status |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for probe in result["probes"]:
        previous = probe["previous"]["summary"]
        current = probe["current"]["summary"]
        status = "PASS" if probe["current"]["status"]["passed"] else "CHECK"
        lines.append(
            "| {id} | {tool} | {prev_ret} | {cur_ret} | {prev_must} | {cur_must} | {cur_high20} | {sem_count} | {status} |".format(
                id=probe["id"],
                tool=probe["tool"],
                prev_ret=previous["returned"],
                cur_ret=current["returned"],
                prev_must=f"{previous['must_find']['found_count']}/{previous['must_find']['gold_count']}",
                cur_must=f"{current['must_find']['found_count']}/{current['must_find']['gold_count']}",
                cur_high20=current["high_value"]["top20"],
                sem_count=current.get("semantic_candidate_count"),
                status=status,
            )
        )
    lines.extend(["", "## Notes", ""])
    for probe in result["probes"]:
        lines.append(f"- `{probe['id']}`: {probe['gold'].get('rationale')}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--previous-commit", default=None)
    parser.add_argument("--current-label", default="working_tree")
    args = parser.parse_args()

    catalog = load_json(CATALOG_PATH)
    gold = load_json(GOLD_PATH)
    previous_commit = args.previous_commit or gold["previous_reference_commit"]
    gold_by_id = {probe["id"]: probe for probe in gold["probes"]}
    catalog_by_id = {probe["id"]: probe for probe in catalog["tool_level_probes"]}

    previous_server = load_previous_server(previous_commit)
    current_server = load_current_server()

    probe_results = []
    for probe_id, gold_probe in gold_by_id.items():
        catalog_probe = catalog_by_id[probe_id]
        previous_result = run_probe(previous_server, catalog_probe)
        current_result = run_probe(current_server, catalog_probe)
        previous_summary = summarize_result(previous_result, gold_probe)
        current_summary = summarize_result(current_result, gold_probe)
        probe_results.append(
            {
                "id": probe_id,
                "tool": catalog_probe["tool"],
                "arguments": catalog_probe.get("arguments") or {},
                "gold": gold_probe,
                "previous": {"summary": previous_summary},
                "current": {"summary": current_summary, "status": score_status(current_summary, gold_probe)},
            }
        )

    output = {
        "gold_reference": str(GOLD_PATH.relative_to(ROOT)).replace("\\", "/"),
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "previous_commit": previous_commit,
        "current_commit": args.current_label,
        "probes": probe_results,
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = utc_stamp()
    json_path = OUTPUT_DIR / f"semantic_tool_integration_comparison_{stamp}.json"
    md_path = OUTPUT_DIR / f"semantic_tool_integration_comparison_{stamp}.md"
    json_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown_report(output), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
