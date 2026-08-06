#!/usr/bin/env python3
"""Validate V2.1 cross-source fusion evidence and immutability guarantees."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
V2_DIR = ROOT / "serbian_intelligence_v2"
V21_DIR = ROOT / "serbian_intelligence_v2_1"
GENERATOR = ROOT / "generate_serbian_intelligence_v2_1.py"
MAX_DELTA_SECONDS = 8 * 60 * 60

OBJECT_CONCEPTS = {
    "שיירת כלי רכב": "concept:convoy_or_vehicle_column",
    "רכב משוריין": "concept:armored_vehicle",
    "מחסום דרכים": "concept:roadblock_position",
    "עמדת תצפית": "concept:observation_post",
    "מסוק": "concept:helicopter",
    "משאית לוגיסטית": "concept:logistics_vehicle",
    "עבודות הנדסיות": "concept:engineering_activity",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or []), list(reader)


def read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> int:
    regenerate = "--regenerate" in sys.argv[1:]
    report_path = V21_DIR / "generation_report_v2_1.json"
    v2_hashes_before = {path.name: sha256(path) for path in V2_DIR.iterdir() if path.is_file()}
    if regenerate:
        subprocess.run([sys.executable, str(GENERATOR)], check=True, stdout=subprocess.DEVNULL)
        first_regeneration = json.loads(report_path.read_text(encoding="utf-8"))["output_hashes"]
        subprocess.run([sys.executable, str(GENERATOR)], check=True, stdout=subprocess.DEVNULL)
    report = json.loads(report_path.read_text(encoding="utf-8"))

    raw_fields, rows = read_csv(V21_DIR / "north_kosovo_serbian_intelligence_v2_1_14800.csv")
    projection_fields, projections = read_csv(V21_DIR / "serbia_kosovo_events_projection_v2_1.csv")
    label_fields, labels = read_csv(V21_DIR / "serbia_kosovo_evaluator_labels_v2_1.csv")
    truth = read_jsonl(V21_DIR / "fusion_target_truth_v2_1.jsonl")
    uav = read_jsonl(V21_DIR / "serbian_uav_observations_v2_1.jsonl")
    entities = json.loads((V21_DIR / "serbia_kosovo_entities_v2_1.json").read_text(encoding="utf-8-sig"))
    locations = json.loads((V21_DIR / "serbia_kosovo_locations_v2_1.json").read_text(encoding="utf-8-sig"))

    row_by_id = {row["record_id"]: row for row in rows}
    projection_by_id = {row["event_id"]: row for row in projections}
    label_by_id = {row["record_id"]: row for row in labels}
    truth_by_id = {item["fusion_truth_id"]: item for item in truth}
    sys.path.insert(0, str(ROOT.parent / "mcp_server"))
    from semantic_index import dense_features

    assert len(rows) == 14_800
    assert len(row_by_id) == len(rows)
    assert len(projections) == len(rows)
    assert len(labels) == len(rows)
    assert len(uav) == 3_800
    assert len(truth) == 300
    assert len({item["fusion_truth_id"] for item in truth}) == len(truth)
    assert sum(row["collection_family"] == "public_source" for row in rows) == 11_000
    assert sum(row["collection_family"] == "airborne_isr_video_exploitation" for row in rows) == 3_800

    truth_field_names = {
        "fusion_truth_id",
        "fusion_truth_role",
        "same_object_truth",
        "hard_negative_for",
        "target_object_truth",
    }
    assert truth_field_names.isdisjoint(raw_fields)
    assert truth_field_names.isdisjoint(projection_fields)
    assert truth_field_names.issubset(label_fields)
    raw_json_text = (V21_DIR / "north_kosovo_serbian_intelligence_v2_1_14800.jsonl").read_text(encoding="utf-8")
    projection_text = (V21_DIR / "serbia_kosovo_events_projection_v2_1.csv").read_text(encoding="utf-8-sig")
    assert "fusion_truth_id" not in raw_json_text
    assert "FUSION-TRUTH-V2-1-" not in raw_json_text
    assert "fusion_truth_id" not in projection_text
    assert "FUSION-TRUTH-V2-1-" not in projection_text

    entity_ids = {item["entity_id"] for item in entities}
    assert all(row["entity_id"] in entity_ids for row in projections)
    assert all(row["location_id"] in locations for row in projections)

    public_language_modes = Counter()
    evidence_ids: set[str] = set()
    for item in truth:
        ids = item["evidence_record_ids"]
        assert len(ids) == 3
        assert not evidence_ids.intersection(ids)
        evidence_ids.update(ids)
        evidence = [row_by_id[record_id] for record_id in ids]
        evidence_projections = [projection_by_id[record_id] for record_id in ids]
        assert Counter(row["collection_family"] for row in evidence) == {
            "airborne_isr_video_exploitation": 1,
            "public_source": 2,
        }
        public_rows = [row for row in evidence if row["collection_family"] == "public_source"]
        assert len({row["source_type"] for row in public_rows}) == 2
        assert all(row["event_id"] == item["scenario_event_id"] for row in evidence)
        assert all(row["location_id"] == item["location_id"] for row in evidence)
        assert all(row["entity_id"] == item["entity_id"] for row in evidence_projections)
        anchor_time = parse_time(evidence[0]["timestamp"])
        assert all(
            abs((parse_time(row["timestamp"]) - anchor_time).total_seconds()) <= MAX_DELTA_SECONDS
            for row in public_rows
        )
        assert label_by_id[ids[0]]["fusion_truth_role"] == "uav_anchor"
        assert all(label_by_id[record_id]["fusion_truth_id"] == item["fusion_truth_id"] for record_id in ids)
        assert all(label_by_id[record_id]["same_object_truth"] == "true" for record_id in ids)
        for row in public_rows:
            text = row["text"]
            features = {name for name, _ in dense_features(text)}
            assert OBJECT_CONCEPTS[item["object_class"]] in features
            if "כ-" in text:
                public_language_modes["approximate"] += 1
            elif "בין " in text:
                public_language_modes["range"] += 1
            elif "ללא אפשרות לספירה מדויקת" in text:
                public_language_modes["uncertain"] += 1
    assert set(public_language_modes) == {"approximate", "range", "uncertain"}

    negatives = [label for label in labels if label["fusion_truth_role"] == "hard_negative"]
    assert len(negatives) == 100
    assert not evidence_ids.intersection(label["record_id"] for label in negatives)
    for label in negatives:
        assert label["same_object_truth"] == "false"
        assert label["hard_negative_for"] in truth_by_id
        negative_projection = projection_by_id[label["record_id"]]
        positive = truth_by_id[label["hard_negative_for"]]
        assert negative_projection["location_id"] == positive["location_id"]
        assert negative_projection["entity_id"] != positive["entity_id"]

    v2_hashes_after = {path.name: sha256(path) for path in V2_DIR.iterdir() if path.is_file()}
    assert v2_hashes_before == v2_hashes_after
    assert report["checks"]["v2_inputs_unchanged"] is True
    if regenerate:
        assert report["output_hashes"] == first_regeneration

    summary = {
        "rows": len(rows),
        "uav_rows": len(uav),
        "positive_chains": len(truth),
        "positive_evidence_records": len(evidence_ids),
        "hard_negatives": len(negatives),
        "object_distribution": dict(Counter(item["object_class"] for item in truth)),
        "public_count_language": dict(public_language_modes),
        "truth_leakage": False,
        "v2_unchanged": True,
        "deterministic_regeneration": regenerate,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
