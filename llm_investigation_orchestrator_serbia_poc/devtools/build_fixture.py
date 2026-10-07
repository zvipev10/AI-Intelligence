#!/usr/bin/env python3
"""Build a fake-HL-API fixture from a demo data package (one-off, for development and CI).

The demo packages were removed from the app in the i360-only branch; get one back from Git
history, for example:

    git show main:llm_investigation_orchestrator_serbia_poc/data/syria_cellular_records_v13/events.csv > /tmp/seed/events.csv
    (same for entities.json and locations.json)

    python devtools/build_fixture.py --scenario syria --events /tmp/seed/events.csv \
        --entities /tmp/seed/entities.json --locations /tmp/seed/locations.json \
        --out devtools/fixtures/syria.json

Each CSV row becomes an i360-shaped item: the platform assigns its own ``item_id`` (a UUID),
the readable fields (time, location, text, source) sit where HL API puts them, and every
demo column is carried as an item tag, which is what ``mapping/default.json`` reads back.
"""
from __future__ import annotations

import argparse
import csv
import json
import uuid
from pathlib import Path

NAMESPACE = uuid.UUID("6f1d3c52-6a54-4d0c-9a37-2b8f0f3d1a10")

ITEM_TYPES = {
    "IPDR": "ip_session", "Cellular Geolocations": "location_report", "ADINT": "ad_event",
    "CCTV": "video", "Satellite": "image", "שיחות סלולר": "call", "Cellular Calls": "call",
}


def iso(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if value.endswith("Z") or "+" in value[10:]:
        return value
    return value + "Z"


def build(scenario: str, events_path: Path, entities_path: Path, locations_path: Path) -> dict:
    locations = json.loads(locations_path.read_text(encoding="utf-8"))
    entities = json.loads(entities_path.read_text(encoding="utf-8"))
    with events_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    items = []
    for row in rows:
        event_id = row.get("event_id") or ""
        location = locations.get(row.get("location_id") or "", {})
        lat = row.get("latitude") or location.get("latitude")
        lon = row.get("longitude") or location.get("longitude")
        tags = [{"type": key, "value": value, "source": "system"} for key, value in row.items() if value not in (None, "")]
        tags.append({"type": "scenario", "value": scenario, "source": "system"})
        parties = []
        for side in ("a", "b"):
            identifiers = [{"type": kind, "value": row.get(f"side_{side}_{column}")}
                           for kind, column in (("imei", "imei"), ("msisdn", "number"))
                           if row.get(f"side_{side}_{column}")]
            if identifiers:
                parties.append({"id": side, "role": side.upper(), "identifiers": identifiers})
        items.append({
            "item_id": str(uuid.uuid5(NAMESPACE, f"{scenario}:{event_id}")),
            "item_type": ITEM_TYPES.get(row.get("source_type") or "", "post"),
            "source_application": row.get("source_type") or None,
            "event_time": iso(row.get("timestamp_utc") or ""),
            "language": "Hebrew",
            "text": {"original": row.get("event_summary") or None, "english": row.get("event_summary") or None,
                     "transcript": row.get("call_transcript") or None},
            "location": {"point": {"lat": float(lat), "lon": float(lon)}} if lat not in (None, "") and lon not in (None, "") else None,
            "tags": tags,
            "parties": parties,
            "media": {"kind": "none", "has_thumbnail": False, "primary_file_id": None, "thumbnail_file_id": None, "file_count": 0},
        })
    instances = {"DEMO_ENTITY": [], "DEMO_LOCATION": []}
    for entity in entities:
        instances["DEMO_ENTITY"].append({
            "entity_id": str(uuid.uuid5(NAMESPACE, f"{scenario}:entity:{entity['entity_id']}")),
            "entity_type": "DEMO_ENTITY",
            "entity_name": entity.get("canonical_name") or entity["entity_id"],
            "sections": {"main": {"ref_id": entity["entity_id"], "canonical_name": entity.get("canonical_name"),
                                  "entity_type": entity.get("entity_type"), "scenario": scenario},
                         "raw": {"json": json.dumps(entity, ensure_ascii=False)}},
        })
    for location_id, location in locations.items():
        instances["DEMO_LOCATION"].append({
            "entity_id": str(uuid.uuid5(NAMESPACE, f"{scenario}:location:{location_id}")),
            "entity_type": "DEMO_LOCATION",
            "entity_name": location.get("name") or location_id,
            "sections": {"main": {"ref_id": location_id, "name": location.get("name"), "scenario": scenario,
                                  "position": {"type": "geo", "geoPoint": {"lat": location.get("latitude"), "lon": location.get("longitude")}}},
                         "raw": {"json": json.dumps(location, ensure_ascii=False)}},
        })
    return {"scenario": scenario, "items": items, "entities": instances}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--entities", type=Path, required=True)
    parser.add_argument("--locations", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    fixture = build(args.scenario, args.events, args.entities, args.locations)
    args.out.write_text(json.dumps(fixture, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{args.out}: {len(fixture['items'])} items, "
          f"{sum(len(v) for v in fixture['entities'].values())} entity instances")


if __name__ == "__main__":
    main()
