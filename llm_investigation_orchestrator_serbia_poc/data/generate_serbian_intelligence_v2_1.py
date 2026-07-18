#!/usr/bin/env python3
"""Generate V2.1 cross-source fusion evidence from immutable V2 artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import random
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "serbian_intelligence_v2"
OUTPUT_DIR = ROOT / "serbian_intelligence_v2_1"
SEED = 20260718
POSITIVE_CHAINS = 300
HARD_NEGATIVES = 100
MAX_PUBLIC_DELTA_SECONDS = 8 * 60 * 60

RAW_CSV = "north_kosovo_serbian_intelligence_v2_14800.csv"
RAW_JSONL = "north_kosovo_serbian_intelligence_v2_14800.jsonl"
PROJECTION_CSV = "serbia_kosovo_events_projection_v2.csv"
LABELS_CSV = "serbia_kosovo_evaluator_labels_v2.csv"
UAV_JSONL = "serbian_uav_observations_v2.jsonl"
ENTITIES_JSON = "serbia_kosovo_entities_v2.json"
LOCATIONS_JSON = "serbia_kosovo_locations_v2.json"

OUTPUT_NAMES = {
    RAW_CSV: "north_kosovo_serbian_intelligence_v2_1_14800.csv",
    RAW_JSONL: "north_kosovo_serbian_intelligence_v2_1_14800.jsonl",
    PROJECTION_CSV: "serbia_kosovo_events_projection_v2_1.csv",
    LABELS_CSV: "serbia_kosovo_evaluator_labels_v2_1.csv",
    UAV_JSONL: "serbian_uav_observations_v2_1.jsonl",
    ENTITIES_JSON: "serbia_kosovo_entities_v2_1.json",
    LOCATIONS_JSON: "serbia_kosovo_locations_v2_1.json",
}

TRUTH_FIELDS = [
    "fusion_truth_id",
    "fusion_truth_role",
    "same_object_truth",
    "hard_negative_for",
    "target_object_truth",
]

TARGET_OBJECTS = {
    "שיירת כלי רכב",
    "רכב משוריין",
    "מחסום דרכים",
    "עמדת תצפית",
    "מסוק",
    "משאית לוגיסטית",
    "עבודות הנדסיות",
}

NON_TARGET_ENTITY_IDS = {
    "ENT-LOCAL-RESIDENTS",
    "ENT-LOCAL-JOURNALISTS",
    "ENT-AMBULANCES",
    "ENT-EULEX",
}

OBJECT_TERMS = {
    "שיירת כלי רכב": ["טור כלי רכב", "מספר כלי רכב שנעו יחד", "שיירה ממונעת"],
    "רכב משוריין": ["כלים משוריינים", "רכב כבד ממוגן", "כלי רכב בעלי מיגון"],
    "מחסום דרכים": ["נקודת חסימה", "חסימה מאוישת על הציר", "עמדת בידוק החוסמת את הדרך"],
    "עמדת תצפית": ["נקודת תצפית מאוישת", "עמדה שולטת לצורכי תצפית", "צוות תצפית בעמדה"],
    "מסוק": ["כלי טיס סובב כנף", "מסוק שנצפה באזור", "פעילות מסוק בגובה נמוך"],
    "משאית לוגיסטית": ["משאית אספקה", "רכב תובלה לוגיסטי", "משאית שנשאה ציוד"],
    "עבודות הנדסיות": ["פעילות הנדסית", "כלים שביצעו הכשרת שטח", "עבודות עפר והקמת מיגון"],
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


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def public_confirmation_text(row: dict, object_class: str, count: int, variant: int) -> str:
    term = OBJECT_TERMS[object_class][variant % len(OBJECT_TERMS[object_class])]
    entity = row["actor_mentioned"]
    location = row["place_name"]
    if variant % 3 == 0:
        count_text = f"כ-{count} פריטים"
    elif variant % 3 == 1:
        low = max(1, count - 2)
        high = count + 2
        count_text = f"בין {low} ל-{high} פריטים"
    else:
        count_text = "מספר פריטים, ללא אפשרות לספירה מדויקת"
    templates = [
        "פרסום פומבי מתאר {term} המזוהים עם {entity} בקרבת {location}; לפי הכותב נראו {count_text}. מועד הצילום והייחוס דורשים אימות.",
        "תושבים באזור {location} דיווחו על {term} של {entity}. ההערכה היא {count_text}, אך האיכות החזותית מוגבלת.",
        "תיעוד שהופץ ברשת מציג לכאורה {term} הקשורים ל{entity} במרחב {location}; נמסר על {count_text}. אין מקור עצמאי לקואורדינטה מדויקת.",
    ]
    return templates[variant % len(templates)].format(
        term=term,
        entity=entity,
        location=location,
        count_text=count_text,
    )


def distractor_text(row: dict, object_class: str, variant: int) -> str:
    term = OBJECT_TERMS[object_class][(variant + 1) % len(OBJECT_TERMS[object_class])]
    return (
        f"דיווח נוסף מתאר {term} של {row['actor_mentioned']} במרחב {row['place_name']}. "
        "למרות הקרבה הגאוגרפית, אין סימן המקשר את הדיווח לאותו כוח או לאותו רצף תנועה."
    )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(SEED)
    source_files = [SOURCE_DIR / name for name in OUTPUT_NAMES]
    missing = [str(path) for path in source_files if not path.exists()]
    if missing:
        raise RuntimeError(f"Missing V2 inputs: {missing}")
    source_hashes_before = {path.name: sha256(path) for path in source_files}

    raw_fields, rows = read_csv(SOURCE_DIR / RAW_CSV)
    projection_fields, projections = read_csv(SOURCE_DIR / PROJECTION_CSV)
    label_fields, labels = read_csv(SOURCE_DIR / LABELS_CSV)
    projection_by_id = {row["event_id"]: row for row in projections}
    label_by_id = {row["record_id"]: row for row in labels}
    row_by_id = {row["record_id"]: row for row in rows}

    public_by_key: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    public_by_location: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        projection = projection_by_id[row["record_id"]]
        if row["collection_family"] == "public_source":
            key = (row["event_id"], row["location_id"], projection["entity_id"])
            public_by_key[key].append(row)
            public_by_location[row["location_id"]].append(row)

    anchors = []
    for row in rows:
        projection = projection_by_id[row["record_id"]]
        if (
            row["collection_family"] == "airborne_isr_video_exploitation"
            and row["observed_object_class"] in TARGET_OBJECTS
            and projection["entity_id"] not in NON_TARGET_ENTITY_IDS
            and row["geolocation_confidence"] in {"בינונית", "גבוהה"}
            and row["identification_confidence"] in {"בינונית", "גבוהה"}
        ):
            anchors.append(row)
    rng.shuffle(anchors)

    used_public: set[str] = set()
    selected_anchor_ids: set[str] = set()
    truth_rows: list[dict] = []

    for anchor in anchors:
        projection = projection_by_id[anchor["record_id"]]
        key = (anchor["event_id"], anchor["location_id"], projection["entity_id"])
        anchor_time = parse_time(anchor["timestamp"])
        compatible = [
            row
            for row in public_by_key.get(key, [])
            if row["record_id"] not in used_public
            and abs((parse_time(row["timestamp"]) - anchor_time).total_seconds()) <= MAX_PUBLIC_DELTA_SECONDS
        ]
        compatible.sort(key=lambda row: (abs((parse_time(row["timestamp"]) - anchor_time).total_seconds()), row["record_id"]))
        pair = None
        for first_index, first in enumerate(compatible):
            for second in compatible[first_index + 1 :]:
                if first["source_type"] != second["source_type"]:
                    pair = (first, second)
                    break
            if pair:
                break
        if not pair:
            continue

        truth_id = f"FUSION-TRUTH-V2-1-{len(truth_rows) + 1:04d}"
        count = int(anchor["estimated_object_count"])
        evidence = [anchor, *pair]
        for pair_index, public_row in enumerate(pair):
            variant = len(truth_rows) * 2 + pair_index
            public_row["text"] = public_confirmation_text(public_row, anchor["observed_object_class"], count, variant)
            projection_by_id[public_row["record_id"]]["event_summary"] = public_row["text"]
            used_public.add(public_row["record_id"])

        for role, evidence_row in zip(("uav_anchor", "public_confirmation", "public_confirmation"), evidence):
            label = label_by_id[evidence_row["record_id"]]
            label.update({
                "fusion_truth_id": truth_id,
                "fusion_truth_role": role,
                "same_object_truth": "true",
                "hard_negative_for": "",
                "target_object_truth": anchor["observed_object_class"],
            })

        evidence_times = [parse_time(row["timestamp"]) for row in evidence]
        truth_rows.append({
            "fusion_truth_id": truth_id,
            "scenario_event_id": anchor["event_id"],
            "entity_id": projection["entity_id"],
            "location_id": anchor["location_id"],
            "object_class": anchor["observed_object_class"],
            "uav_estimated_object_count": count,
            "active_from_utc": min(evidence_times).isoformat().replace("+00:00", "Z"),
            "active_to_utc": max(evidence_times).isoformat().replace("+00:00", "Z"),
            "evidence_record_ids": [row["record_id"] for row in evidence],
            "public_source_types": [row["source_type"] for row in pair],
            "canonical_area_only": True,
            "truth_note": "Synthetic evaluator truth; not available to Moshe or runtime retrieval.",
        })
        selected_anchor_ids.add(anchor["record_id"])
        if len(truth_rows) == POSITIVE_CHAINS:
            break

    if len(truth_rows) < POSITIVE_CHAINS:
        raise RuntimeError(f"Only {len(truth_rows)} positive chains could be created")

    hard_negative_rows = []
    for truth in truth_rows:
        if len(hard_negative_rows) == HARD_NEGATIVES:
            break
        anchor = row_by_id[truth["evidence_record_ids"][0]]
        anchor_time = parse_time(anchor["timestamp"])
        candidates = []
        for row in public_by_location[truth["location_id"]]:
            if row["record_id"] in used_public:
                continue
            projection = projection_by_id[row["record_id"]]
            if projection["entity_id"] == truth["entity_id"]:
                continue
            delta = abs((parse_time(row["timestamp"]) - anchor_time).total_seconds())
            if delta <= MAX_PUBLIC_DELTA_SECONDS:
                candidates.append((delta, row["record_id"], row))
        if not candidates:
            continue
        _, _, distractor = min(candidates)
        distractor["text"] = distractor_text(distractor, truth["object_class"], len(hard_negative_rows))
        projection_by_id[distractor["record_id"]]["event_summary"] = distractor["text"]
        label_by_id[distractor["record_id"]].update({
            "fusion_truth_id": "",
            "fusion_truth_role": "hard_negative",
            "same_object_truth": "false",
            "hard_negative_for": truth["fusion_truth_id"],
            "target_object_truth": truth["object_class"],
        })
        used_public.add(distractor["record_id"])
        hard_negative_rows.append(distractor["record_id"])

    if len(hard_negative_rows) < HARD_NEGATIVES:
        raise RuntimeError(f"Only {len(hard_negative_rows)} hard negatives could be created")

    for label in labels:
        for field in TRUTH_FIELDS:
            label.setdefault(field, "")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUT_DIR / OUTPUT_NAMES[RAW_CSV], raw_fields, rows)
    write_jsonl(OUTPUT_DIR / OUTPUT_NAMES[RAW_JSONL], rows)
    write_csv(OUTPUT_DIR / OUTPUT_NAMES[PROJECTION_CSV], projection_fields, projections)
    write_csv(OUTPUT_DIR / OUTPUT_NAMES[LABELS_CSV], [*label_fields, *TRUTH_FIELDS], labels)
    write_jsonl(OUTPUT_DIR / "fusion_target_truth_v2_1.jsonl", truth_rows)
    for source_name in (UAV_JSONL, ENTITIES_JSON, LOCATIONS_JSON):
        shutil.copyfile(SOURCE_DIR / source_name, OUTPUT_DIR / OUTPUT_NAMES[source_name])

    source_hashes_after = {path.name: sha256(path) for path in source_files}
    output_files = sorted(path for path in OUTPUT_DIR.iterdir() if path.is_file() and path.name != "generation_report_v2_1.json")
    report = {
        "schema_version": "2.1",
        "seed": SEED,
        "rows": len(rows),
        "uav_observations": sum(row["collection_family"] == "airborne_isr_video_exploitation" for row in rows),
        "public_source_records": sum(row["collection_family"] == "public_source" for row in rows),
        "positive_fusion_chains": len(truth_rows),
        "positive_evidence_records": sum(len(row["evidence_record_ids"]) for row in truth_rows),
        "hard_negative_records": len(hard_negative_rows),
        "object_counts": dict(Counter(row["object_class"] for row in truth_rows)),
        "checks": {
            "target_rows": len(rows) == 14_800,
            "unique_record_ids": len({row["record_id"] for row in rows}) == len(rows),
            "uav_count_preserved": sum(row["collection_family"] == "airborne_isr_video_exploitation" for row in rows) == 3_800,
            "positive_chain_target": len(truth_rows) >= POSITIVE_CHAINS,
            "hard_negative_target": len(hard_negative_rows) >= HARD_NEGATIVES,
            "v2_inputs_unchanged": source_hashes_before == source_hashes_after,
        },
        "v2_input_hashes": source_hashes_before,
        "output_hashes": {path.name: sha256(path) for path in output_files},
        "notes": [
            "V1 and V2 are immutable inputs and are not rewritten.",
            "Fusion truth exists only in evaluator artifacts.",
            "Canonical locations represent areas, not observation-level coordinates.",
            "All operational events and movements are synthetic.",
        ],
    }
    if not all(report["checks"].values()):
        raise RuntimeError(f"Generation checks failed: {report['checks']}")
    (OUTPUT_DIR / "generation_report_v2_1.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
