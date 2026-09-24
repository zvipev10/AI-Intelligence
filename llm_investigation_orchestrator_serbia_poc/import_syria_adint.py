"""Create a new immutable Syria ADINT package from the supplied observation array."""
import argparse
import csv
import hashlib
import ipaddress
import json
import math
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ("observation_id", "device_id", "timestamp_utc", "brand", "model", "os", "keyboard_language", "ip", "latitude", "longitude", "accuracy_m")


def validate(rows):
    if not isinstance(rows, list) or not rows:
        raise ValueError("Expected a nonempty observation array")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != set(FIELDS):
            raise ValueError("Unexpected observation schema")
        for key in ("observation_id", "device_id", "timestamp_utc", "brand", "model", "os"):
            if not isinstance(row[key], str) or not row[key].strip():
                raise ValueError(f"Missing or invalid {key}")
        if row["observation_id"] in seen:
            raise ValueError("Duplicate observation ID")
        seen.add(row["observation_id"])
        stamp = datetime.fromisoformat(row["timestamp_utc"].replace("Z", "+00:00"))
        if stamp.utcoffset() is None:
            raise ValueError("Timestamp requires timezone")
        if row["ip"] is not None:
            ipaddress.ip_address(row["ip"])
        if row["keyboard_language"] is not None and not isinstance(row["keyboard_language"], str):
            raise ValueError("Invalid keyboard language")
        lat, lon = row["latitude"], row["longitude"]
        if (lat is None) != (lon is None):
            raise ValueError("Coordinates must be present or absent together")
        for value, bound in [(lat, 90), (lon, 180)]:
            if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or abs(value) > bound):
                raise ValueError("Invalid coordinate")
        accuracy = row["accuracy_m"]
        if accuracy is not None and (isinstance(accuracy, bool) or not isinstance(accuracy, (int, float)) or not math.isfinite(accuracy) or accuracy < 0):
            raise ValueError("Invalid accuracy")
    return rows


def build(source, root=ROOT):
    raw = source.read_bytes()
    observations = validate(json.loads(raw.decode("utf-8-sig")))
    old = root / "data/syria_network_v1"
    new = root / "data/syria_adint_v1"
    if new.exists():
        raise ValueError("Refusing to overwrite an immutable package")
    rows = list(csv.DictReader((old / "events.csv").read_text(encoding="utf-8").splitlines()))
    fields = list(dict.fromkeys([*rows[0], *FIELDS]))
    rows = [r for r in rows if r["source_type"] != "ADINT"]
    locations = json.loads((old / "locations.json").read_text(encoding="utf-8"))
    entities = json.loads((old / "entities.json").read_text(encoding="utf-8"))
    # Remove only old ADINT-only identities and locations; preserve all other source dependencies.
    used_locations = {r["location_id"] for r in rows}
    used_entities = {r["entity_id"] for r in rows}
    locations = {k: v for k, v in locations.items() if k in used_locations}
    entities = [e for e in entities if e["entity_id"] in used_entities]
    devices = {}
    points = {}
    for item in observations:
        device = item["device_id"]
        if device not in devices:
            devices[device] = "ENT-SYR-DEVICE-" + hashlib.sha256(device.encode()).hexdigest()[:16]
            entities.append({"entity_id": devices[device], "canonical_name": device, "entity_type": "device", "aliases": [device]})
        point = (item["latitude"], item["longitude"])
        location_id = ""
        if point[0] is not None:
            if point not in points:
                location_id = f"LOC-SYR-ADINT-{len(points)+1:03}"
                points[point] = location_id
                locations[location_id] = {"name": f"ADINT observation point {len(points):03}", "latitude": point[0], "longitude": point[1], "country": "Syria", "type": "ADINT observation point", "precision": "reported coordinates"}
            location_id = points[point]
        row = {key: ("" if item[key] is None else item[key]) for key in FIELDS}
        row.update(event_id="REC-SYR-ADINT-" + item["observation_id"], source_type="ADINT", source_reliability="unknown", source_reliability_label="Not specified", certainty_level="reported", entity_id=devices[device], location_id=location_id, collection_family="adint", event_summary=f"ADINT observation {item['observation_id']}: device {device}, {item['brand']} {item['model']} ({item['os']}).")
        # Compatibility aliases for existing cross-source identifier retrieval.
        row.update(advertising_id=device, ip_address=item["ip"] or "", location_accuracy_m="" if item["accuracy_m"] is None else item["accuracy_m"])
        rows.append(row)
    new.mkdir()
    (new / "ADINT.json").write_bytes(raw)
    for suffix in ("", ".en"):
        with (new / f"events{suffix}.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)
        for kind, value in (("locations", locations), ("entities", entities)):
            (new / f"{kind}{suffix}.json").write_bytes(json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8"))
    profile_path = root / "demo_profiles/syria.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile.update(profile_version="7", dataset_version="adint-v1")
    profile["files"] = {kind: f"data/syria_adint_v1/{kind}.{'csv' if kind == 'events' else 'json'}" for kind in ("events", "locations", "entities")}
    profile["checksums"] = {k: v for k, v in profile["checksums"].items() if not k.startswith("data/")}
    profile["checksums"].update({p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest() for p in new.iterdir()})
    profile_path.write_bytes(json.dumps(profile, ensure_ascii=False, indent=2).encode("utf-8"))
    return {"records": len(rows), "adint": len(observations), "new_locations": len(points), "locations": len(locations), "entities": len(entities), "source_sha256": hashlib.sha256(raw).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("source", type=Path)
    print(json.dumps(build(parser.parse_args().source), indent=2))
