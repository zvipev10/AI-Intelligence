#!/usr/bin/env python3
"""Validate structured and multilingual semantic behavior over synthetic V2."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import tempfile
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def feature_names(semantic_index, text: str) -> set[str]:
    return {name for name, _ in semantic_index.dense_features(text)}


def ratio(events: list[dict], predicate) -> float:
    if not events:
        return 0.0
    return sum(1 for event in events if predicate(event)) / len(events)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    cache_dir = args.cache_dir or Path(tempfile.gettempdir()) / "serbia-v2-semantic-validation"
    if args.rebuild and cache_dir.exists():
        cache_path = cache_dir / "semantic_event_index_hybrid_embedding.pkl"
        if cache_path.exists():
            cache_path.unlink()
    os.environ["INTELLIGENCE_POC_DATASET_VERSION"] = "v2"
    os.environ["INTELLIGENCE_POC_SEMANTIC_BACKEND"] = "hybrid_embedding"
    os.environ["INTELLIGENCE_POC_SEMANTIC_INDEX"] = str(cache_dir)

    semantic_index = load_module("semantic_index", HERE / "semantic_index.py")
    server = load_module("serbia_mcp_v2_validation", HERE / "server.py")

    concept_cases = {
        "uav": ("UAV aerial observation", "concept:uav_observation"),
        "convoy": ("vehicle convoy", "concept:convoy_or_vehicle_column"),
        "formation": ("military formation", "concept:military_formation"),
        "armored": ("armored personnel carrier", "concept:armored_vehicle"),
        "air_defense": ("air defense SAM battery", "concept:air_defense"),
        "movement": ("advancing vehicle", "concept:movement"),
        "deployment": ("deployed in an assembly area", "concept:deployment_or_staging"),
        "concentration": ("force concentration", "concept:force_concentration"),
        "count": ("estimated count 7 vehicles", "object_count:7"),
        "serbian": ("Serbian Army", "concept:serbian_forces"),
        "nato_kfor": ("NATO KFOR forces", "concept:nato_kfor_forces"),
        "kosovo": ("Kosovo Police", "concept:kosovo_police"),
    }
    concept_results = {}
    for case, (text, expected) in concept_cases.items():
        features = feature_names(semantic_index, text)
        concept_results[case] = {"expected": expected, "present": expected in features}
        assert expected in features, f"Missing {expected} for {text}"

    uav_records = [event for event in server.EVENTS if event.get("observation_id")]
    assert len(server.EVENTS) == 14_800
    assert len(uav_records) == 3_800
    assert all(event.get("object_class") and event.get("estimated_object_count") for event in uav_records)
    sample_text = semantic_index.SemanticEventIndex.event_text(server.public_event(uav_records[0]))
    for marker in ("object_class", "estimated_object_count", "mobility_status", "geolocation_confidence"):
        assert marker in sample_text

    started = time.perf_counter()
    index = server.get_semantic_index()
    index_seconds = time.perf_counter() - started

    query_cases = [
        ("armored_vehicle", "armored vehicle", lambda event: event.get("object_class") == "רכב משוריין", 0.80),
        ("vehicle_convoy", "vehicle convoy", lambda event: event.get("object_class") == "שיירת כלי רכב", 0.80),
        ("roadblock", "roadblock position", lambda event: event.get("object_class") == "מחסום דרכים", 0.70),
        ("observation_post", "observation post", lambda event: event.get("object_class") == "עמדת תצפית", 0.70),
        ("deployment", "deployed staging area", lambda event: event.get("movement_status") in {"בפריסה", "בהיערכות"}, 0.55),
        ("movement", "UAV vehicle moving or withdrawing", lambda event: event.get("movement_status") in {"בתנועה", "בנסיגה"}, 0.55),
        ("count_7", "UAV estimated count 7 vehicles", lambda event: event.get("estimated_object_count") == "7", 0.60),
        ("nato_kfor", "NATO KFOR forces", lambda event: "KFOR" in str(event.get("entity_id") or ""), 0.70),
        ("kosovo_police", "Kosovo Police", lambda event: "KOSOVO-POLICE" in str(event.get("entity_id") or ""), 0.70),
    ]
    query_results = {}
    for case, query, predicate, minimum_ratio in query_cases:
        query_started = time.perf_counter()
        result = server.semantic_search_events({"query": query, "limit": args.limit})
        query_seconds = time.perf_counter() - query_started
        events = result["events"]
        precision = ratio(events, predicate)
        query_results[case] = {
            "query": query,
            "returned": len(events),
            "top_precision": round(precision, 3),
            "required_precision": minimum_ratio,
            "seconds": round(query_seconds, 3),
            "sample_event_ids": result["event_ids"][:5],
        }
        if not args.summary_only:
            print(json.dumps({case: query_results[case]}, ensure_ascii=True), flush=True)
        assert precision >= minimum_ratio, f"{case} precision {precision:.3f} < {minimum_ratio:.3f}"

    output = {
        "dataset_version": server.DATASET_VERSION,
        "rows": len(server.EVENTS),
        "uav_rows": len(uav_records),
        "backend": index.backend,
        "manifest": index.manifest,
        "index_load_or_build_seconds": round(index_seconds, 3),
        "concept_results": concept_results,
        "query_results": query_results,
    }
    print(json.dumps(output, ensure_ascii=True, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
