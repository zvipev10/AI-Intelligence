#!/usr/bin/env python3
"""Score semantic_search_events backends against semantic_tool_gold_v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MCP_DIR = ROOT / "mcp_server"
sys.path.insert(0, str(MCP_DIR))

import server  # noqa: E402
from semantic_index import SemanticEventIndex  # noqa: E402


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def probe_arguments() -> dict[str, dict[str, Any]]:
    catalog = load_json(ROOT / "docs" / "quality" / "question_catalog_v1.json")
    return {probe["id"]: probe.get("arguments") or {} for probe in catalog["tool_level_probes"]}


def run_semantic_probe(index: SemanticEventIndex, probe_id: str, arguments: dict[str, Any]) -> list[str]:
    filters = {
        "start_time": arguments.get("start_time"),
        "end_time": arguments.get("end_time"),
        "location_ids": arguments.get("location_ids") or [],
        "entity_ids": arguments.get("entity_ids") or [],
        "source_types": arguments.get("source_types") or [],
        "reliabilities": arguments.get("reliabilities") or [],
        "certainty_levels": arguments.get("certainty_levels") or [],
        "keywords": arguments.get("keywords") or [],
        "match_all_keywords": bool(arguments.get("match_all_keywords", False)),
    }
    matches = index.search(arguments.get("query") or "", filters=filters, limit=arguments.get("limit") or 2000)
    return [match["event_id"] for match in matches if match.get("event_id")]


def score_backend(backend: str, gold: dict[str, Any], arguments_by_probe: dict[str, dict[str, Any]]) -> dict[str, Any]:
    records = [server.public_event(event) for event in server.EVENTS]
    index = SemanticEventIndex(
        records,
        cache_dir=ROOT / "data" / "semantic_index",
        signature=server.semantic_index_signature(),
        backend=backend,
    )
    probe_scores = []
    for probe in gold["probes"]:
        if probe["tool"] != "semantic_search_events":
            continue
        found_ids = run_semantic_probe(index, probe["id"], arguments_by_probe[probe["id"]])
        probe_scores.append(
            {
                "id": probe["id"],
                "backend": backend,
                "returned": len(found_ids),
                "must_find": rank_metrics(found_ids, probe["must_find_event_ids"]),
                "high_value": rank_metrics(found_ids, probe["high_value_event_ids"]),
                "bad_priority_hits_top10": [
                    event_id for event_id in probe.get("must_not_prioritize_event_ids", []) if event_id in found_ids[:10]
                ],
                "top10": found_ids[:10],
            }
        )
    return {"backend": backend, "index_manifest": index.manifest, "probe_scores": probe_scores}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backends", nargs="+", default=["lexical_tfidf", "dense_hash_embedding", "hybrid_embedding"])
    parser.add_argument("--output", type=Path, default=ROOT / "docs" / "quality" / "semantic_backend_score_latest.json")
    args = parser.parse_args()

    gold = load_json(ROOT / "docs" / "quality" / "semantic_tool_gold_v1.json")
    arguments_by_probe = probe_arguments()
    result = {
        "gold_reference": "docs/quality/semantic_tool_gold_v1.json",
        "results": [score_backend(backend, gold, arguments_by_probe) for backend in args.backends],
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for backend_result in result["results"]:
        print(f"## {backend_result['backend']}")
        for score in backend_result["probe_scores"]:
            print(
                score["id"],
                "must",
                f"{score['must_find']['found_count']}/{score['must_find']['gold_count']}",
                "top10/top20/top50",
                score["must_find"]["top10"],
                score["must_find"]["top20"],
                score["must_find"]["top50"],
                "high",
                score["high_value"]["top10"],
                score["high_value"]["top20"],
                score["high_value"]["top50"],
                "bad_top10",
                score["bad_priority_hits_top10"],
            )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
