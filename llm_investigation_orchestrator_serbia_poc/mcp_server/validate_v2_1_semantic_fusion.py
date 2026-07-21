#!/usr/bin/env python3
"""Smoke-test semantic recovery of evaluator-known V2.1 evidence chains."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chains", type=int, default=20)
    parser.add_argument("--minimum-recall", type=float, default=0.95)
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--details", action="store_true")
    args = parser.parse_args()

    os.environ["INTELLIGENCE_POC_DATASET_VERSION"] = "v2.1"
    os.environ.setdefault("INTELLIGENCE_POC_SEMANTIC_BACKEND", "hybrid_embedding")
    os.environ.setdefault(
        "INTELLIGENCE_POC_SEMANTIC_INDEX",
        str(args.cache_dir or Path(tempfile.gettempdir()) / "serbia-v2-1-semantic-validation"),
    )
    sys.path.insert(0, str(HERE))
    import server

    truth_path = ROOT / "data" / "serbian_intelligence_v2_1" / "fusion_target_truth_v2_1.jsonl"
    with truth_path.open("r", encoding="utf-8") as stream:
        truth = [json.loads(line) for line in stream if line.strip()]
    selected = truth[: max(1, min(args.chains, len(truth)))]

    load_started = time.perf_counter()
    index = server.get_semantic_index()
    load_seconds = time.perf_counter() - load_started
    recalled = 0
    possible = 0
    query_seconds = []
    per_chain = []
    for item in selected:
        anchor_id, *public_ids = item["evidence_record_ids"]
        query_started = time.perf_counter()
        result = server.semantic_search_events({
            "seed_event_ids": [anchor_id],
            "location_ids": [item["location_id"]],
            "entity_ids": [item["entity_id"]],
            "start_time": item["active_from_utc"],
            "end_time": item["active_to_utc"],
            "limit": 20,
        })
        query_seconds.append(time.perf_counter() - query_started)
        found = len(set(public_ids).intersection(result["event_ids"]))
        recalled += found
        possible += len(public_ids)
        per_chain.append({"fusion_truth_id": item["fusion_truth_id"], "recalled": found, "possible": len(public_ids)})

    recall = recalled / possible if possible else 0.0
    assert recall >= args.minimum_recall, f"Recall {recall:.3f} below {args.minimum_recall:.3f}"
    output = {
        "dataset_version": server.DATASET_VERSION,
        "rows": len(server.EVENTS),
        "chains": len(selected),
        "recalled_public_confirmations": recalled,
        "possible_public_confirmations": possible,
        "recall": round(recall, 3),
        "index_load_seconds": round(load_seconds, 3),
        "query_seconds_min": round(min(query_seconds), 3),
        "query_seconds_max": round(max(query_seconds), 3),
        "manifest": index.manifest,
    }
    if args.details:
        output["per_chain"] = per_chain
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
