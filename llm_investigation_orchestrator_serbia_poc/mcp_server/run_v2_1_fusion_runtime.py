#!/usr/bin/env python3
"""Public-data-only, resource-bounded target discovery for release evaluation."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--module-dir", type=Path, required=True)
    parser.add_argument("--minimum-score", type=float, default=0.18)
    args = parser.parse_args()

    os.environ["INTELLIGENCE_POC_DATASET_VERSION"] = "v2.1"
    os.environ["INTELLIGENCE_POC_SEMANTIC_BACKEND"] = "lexical_tfidf"
    os.environ["INTELLIGENCE_POC_SEMANTIC_INDEX"] = str(args.cache_dir)
    sys.path.insert(0, str(args.module_dir))
    import server

    anchors = [event for event in server.EVENTS if event.get("collection_family") == "airborne_isr_video_exploitation" and event.get("object_class")]
    candidates = []
    for position, anchor in enumerate(anchors, 1):
        assessment = server.prepare_target_candidate({
            "event_ids": [anchor["event_id"]], "confidence": "medium", "discover_corroboration": True,
        })
        if assessment["persistence_eligible"]:
            evidence_ids = [item["record_id"] for item in assessment["evidence"]]
            candidates.append({
                "candidate_key": anchor["event_id"],
                "object_class": anchor["object_class"],
                "entity_id": anchor["entity_id"],
                "location_id": anchor["location_id"],
                "evidence_record_ids": evidence_ids,
                "source_group_count": assessment["independent_source_group_count"],
                "quantity": assessment["quantity"],
                "pair_score": assessment["discovery"]["selected_pair_score"],
                "ambiguity_margin": assessment["discovery"]["ambiguity_margin"],
            })
        if position % 250 == 0:
            print(json.dumps({"anchors_processed": position, "candidates": len(candidates)}), flush=True)

    payload = {"dataset_version": server.DATASET_VERSION, "dataset_rows": len(server.EVENTS), "anchors_examined": len(anchors), "candidate_count": len(candidates), "candidates": candidates}
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in payload.items() if key != "candidates"}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
