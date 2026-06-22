from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


BASE = Path(__file__).resolve().parent
EVENTS = BASE / "events_he_large.csv"
MAPPING = BASE / "event_id_mapping_private.json"

SOURCE_PREFIX = {
    "רשומת נמל": "PORT",
    "רשומת מכס": "CUST",
    "התראה פיננסית": "FIN",
    "מטא-דאטה טלפוני": "TEL",
    "חיישן תנועה": "MOVE",
    "מצלמת דרך": "CAM",
    "יירוט אות": "SIG",
    "חיישן אקוסטי": "ACOU",
    "חיישן גבול": "BORD",
    "תצפית רחפן": "DRONE",
    "תצפית מקור": "OBS",
    "רשתות חברתיות": "SOC",
    "יומן תחזוקה": "MAINT",
    "יומן תפעול": "OPS",
    "רשומת מסירה": "DELIV",
    "רשומת עבודה": "WORK",
}


def normalize_prefix(source_type: str) -> str:
    if source_type in SOURCE_PREFIX:
        return SOURCE_PREFIX[source_type]
    ascii_name = re.sub(r"[^A-Za-z0-9]+", "", source_type.upper())
    return (ascii_name[:6] or "EVT")


def load_rows() -> list[dict[str, str]]:
    with EVENTS.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(rows: list[dict[str, str]]) -> None:
    fieldnames = ["event_id", "timestamp_utc", "source_type", "source_reliability", "entity_or_actor", "location_id", "event_summary"]
    with EVENTS.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = load_rows()
    rows.sort(key=lambda row: (row["timestamp_utc"], row["source_type"], row["entity_or_actor"], row["event_summary"]))

    counters: defaultdict[str, int] = defaultdict(int)
    mapping: dict[str, str] = {}
    reverse: dict[str, str] = {}

    for row in rows:
        old_id = row["event_id"]
        prefix = normalize_prefix(row["source_type"])
        counters[prefix] += 1
        new_id = f"{prefix}-{counters[prefix]:04d}"
        mapping[old_id] = new_id
        reverse[new_id] = old_id
        row["event_id"] = new_id

    write_rows(rows)
    MAPPING.write_text(
        json.dumps({"old_to_new": mapping, "new_to_old": reverse}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for filename in ["candidate_package_he.md", "answer_key_he_large.md"]:
        path = BASE / filename
        text = path.read_text(encoding="utf-8")
        for old_id, new_id in sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True):
            text = text.replace(old_id, new_id)
        path.write_text(text, encoding="utf-8")

    print(f"updated {len(rows)} events")
    print(f"wrote private mapping: {MAPPING.name}")


if __name__ == "__main__":
    main()
