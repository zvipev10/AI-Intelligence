"""Build an immutable Syria dataset revision with dedicated call locations."""

import csv
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CURRENT_DATASET = ROOT / "data/syria_cellular_records_v12"
NEW_DATASET = ROOT / "data/syria_cellular_records_v13"
CALL_LOCATIONS = {
    "REC-SYR-CALL-001": (
        "LOC-SYR-CALL-001",
        "Cellular call location — broken air conditioner",
        35.05008341925823,
        36.27154430013932,
    ),
    "REC-SYR-CALL-002": (
        "LOC-SYR-CALL-002",
        "Cellular call location — fifteen petrol units",
        34.9837599416126,
        35.889327777437586,
    ),
}


def normalized_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def update_events(path: Path) -> None:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    found = set()
    for row in rows:
        call = CALL_LOCATIONS.get(row.get("event_id", ""))
        if call is None:
            continue
        location_id = call[0]
        row["location_id"] = location_id
        row["side_a_location_id"] = location_id
        found.add(row["event_id"])
    if found != set(CALL_LOCATIONS):
        raise ValueError(f"Missing call records: {sorted(set(CALL_LOCATIONS) - found)}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_locations(path: Path) -> None:
    locations = json.loads(path.read_text(encoding="utf-8"))
    for location_id, name, latitude, longitude in CALL_LOCATIONS.values():
        locations[location_id] = {
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
            "country": "Syria",
            "type": "cellular call location",
            "precision": "user-supplied coordinate",
        }
    path.write_text(json.dumps(locations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build() -> dict:
    if NEW_DATASET.exists():
        raise ValueError(f"Refusing to overwrite immutable dataset {NEW_DATASET.name}")
    shutil.copytree(CURRENT_DATASET, NEW_DATASET)
    for name in ("events.csv", "events.en.csv"):
        update_events(NEW_DATASET / name)
    for name in ("locations.json", "locations.en.json"):
        update_locations(NEW_DATASET / name)

    profile_path = ROOT / "demo_profiles/syria.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile.update(profile_version="36", dataset_version="cellular-records-v13")
    profile["files"] = {
        "events": "data/syria_cellular_records_v13/events.csv",
        "locations": "data/syria_cellular_records_v13/locations.json",
        "entities": "data/syria_cellular_records_v13/entities.json",
    }
    profile["checksums"] = {
        key: value for key, value in profile["checksums"].items()
        if not key.startswith("data/syria_cellular_records_v12/")
    }
    profile["checksums"].update({
        path.relative_to(ROOT).as_posix(): normalized_digest(path)
        for path in NEW_DATASET.iterdir() if path.is_file()
    })
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "dataset": NEW_DATASET.name,
        "profile_version": profile["profile_version"],
        "call_locations": {
            event_id: {"location_id": values[0], "latitude": values[2], "longitude": values[3]}
            for event_id, values in CALL_LOCATIONS.items()
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
