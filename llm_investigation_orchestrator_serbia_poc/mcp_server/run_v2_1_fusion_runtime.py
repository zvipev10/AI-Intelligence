#!/usr/bin/env python3
"""Public-data-only, resource-bounded target discovery for release evaluation."""

from __future__ import annotations

import argparse
import json
import os
import sys
import re
from datetime import timedelta
from pathlib import Path


def iso(value) -> str:
    return value.isoformat().replace("+00:00", "Z")


OBJECT_CUES = {
    "מחסום דרכים": ("מחסום", "חסימה", "חסם"),
    "מסוק": ("מסוק", "כלי טיס", "רוטור"),
    "משאית לוגיסטית": ("משאית", "לוגיסט"),
    "עבודות הנדסיות": ("עבודות", "הנדס", "חפירה", "דחפור"),
    "עמדת תצפית": ("תצפית", "עמדה שולטת", "נקודת תצפית"),
    "רכב משוריין": ("משוריין", "רכב ממוגן"),
    "שיירת כלי רכב": ("שיירה", "טור כלי רכב"),
}


def supports_object(item: dict, object_class: str) -> bool:
    text = re.sub(r"\s+", " ", str(item.get("event_summary") or "")).casefold()
    return any(cue.casefold() in text for cue in OBJECT_CUES.get(object_class, (object_class,)))


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
    from fusion_tools import prepare_candidate

    anchors = [event for event in server.EVENTS if event.get("collection_family") == "airborne_isr_video_exploitation" and event.get("object_class")]
    candidates = []
    for position, anchor in enumerate(anchors, 1):
        result = server.semantic_search_events({
            "seed_event_ids": [anchor["event_id"]],
            "location_ids": [anchor["location_id"]],
            "entity_ids": [anchor["entity_id"]],
            "start_time": iso(anchor["timestamp"] - timedelta(hours=8)),
            "end_time": iso(anchor["timestamp"] + timedelta(hours=8)),
            "limit": 24,
        })
        public = [
            item for item in result["events"]
            if item.get("collection_family") == "public_source"
            and float(item.get("semantic_score") or 0) >= args.minimum_score
            and supports_object(item, anchor["object_class"])
        ]
        selected, used_types = [], set()
        for item in public:
            source_type = str(item.get("source_type") or "")
            if not source_type or source_type in used_types:
                continue
            selected.append(item)
            used_types.add(source_type)
            if len(selected) == 2:
                break
        if len(selected) != 2:
            continue
        evidence = [server.public_event(anchor), *selected]
        assessment = prepare_candidate(evidence, "medium")
        if assessment["persistence_eligible"]:
            candidates.append({
                "candidate_key": anchor["event_id"],
                "object_class": anchor["object_class"],
                "entity_id": anchor["entity_id"],
                "location_id": anchor["location_id"],
                "evidence_record_ids": [item["event_id"] for item in evidence],
                "source_group_count": assessment["independent_source_group_count"],
                "quantity": assessment["quantity"],
                "public_scores": [round(float(item["semantic_score"]), 6) for item in selected],
            })
        if position % 250 == 0:
            print(json.dumps({"anchors_processed": position, "candidates": len(candidates)}), flush=True)

    payload = {"dataset_version": server.DATASET_VERSION, "dataset_rows": len(server.EVENTS), "anchors_examined": len(anchors), "candidate_count": len(candidates), "candidates": candidates}
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in payload.items() if key != "candidates"}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
