"""Generate synthetic ADINT/IPDR fixtures using documentation IP addresses."""
import csv
import hashlib
import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    old = ROOT / "data/syria_convoy_v3"
    new = ROOT / "data/syria_network_v1"
    new.mkdir(exist_ok=True)
    locations = json.loads((old / "locations.json").read_text())
    entities = json.loads((old / "entities.json").read_text(encoding="utf-8"))
    lat = 35.0
    lon = 38.5
    delta = math.degrees(.5 / 6371)
    for index, (name, latitude, longitude) in enumerate([
        ("North", lat + delta, lon),
        ("East", lat, lon + delta / math.cos(math.radians(lat))),
        ("West", lat, lon - delta / math.cos(math.radians(lat))),
    ], 3):
        locations[f"LOC-SYR-{index:03}"] = {"name": f"Demo Site 1 - {name} point", "latitude": latitude, "longitude": longitude, "country": "Syria", "region": "Central Syria (synthetic demo)", "type": "demonstration observation point", "precision": "synthetic"}
    rows = list(csv.DictReader((old / "events.csv").read_text(encoding="utf-8").splitlines()))
    fields = list(rows[0]) + ["advertising_id", "ip_address", "imei", "session_start_utc", "session_end_utc", "source_port", "protocol", "bytes_up", "bytes_down", "location_accuracy_m"]
    base = datetime(2026, 9, 22, 8, tzinfo=timezone.utc)
    stamp = lambda value: value.isoformat().replace("+00:00", "Z")
    for number, location in enumerate(["LOC-SYR-001", "LOC-SYR-003", "LOC-SYR-004", "LOC-SYR-005"], 1):
        advertising_id = f"00000000-0000-4000-8000-{number:012}"
        entity = f"ENT-SYR-AD-{number:03}"
        entities.append({"entity_id": entity, "canonical_name": f"Demo advertising device {number}", "entity_type": "advertising device", "aliases": [advertising_id]})
        ip = "192.0.2.10" if number == 1 else f"198.51.100.{number}"
        rows.append({"event_id": f"REC-SYR-ADINT-{number:03}", "timestamp_utc": stamp(base + timedelta(minutes=number - 1)), "source_type": "ADINT", "source_reliability": "medium", "source_reliability_label": "Synthetic demo", "certainty_level": "observed", "entity_id": entity, "location_id": location, "event_summary": f"Synthetic advertising observation for device {advertising_id} using IP {ip}.", "collection_family": "synthetic_adint", "advertising_id": advertising_id, "ip_address": ip, "location_accuracy_m": "25", "synthetic_media": "true"})
    for number in range(1, 201):
        # Place the matching session away from the first/last row; do not label it.
        matching = number == 137
        ip = "192.0.2.10" if matching else f"203.0.113.{number}"
        start = base - timedelta(minutes=2) if matching else base + timedelta(minutes=number - 100)
        end = start + timedelta(minutes=6)
        body = f"00000000{number:06}"
        total = sum(sum(divmod(int(digit) * (2 if index % 2 else 1), 10)) for index, digit in enumerate(body))
        imei = body + str((-total) % 10)
        rows.append({"event_id": f"REC-SYR-IPDR-{number:03}", "timestamp_utc": stamp(start), "source_type": "IPDR", "source_reliability": "high", "source_reliability_label": "Synthetic demo", "certainty_level": "observed", "entity_id": "", "location_id": "", "event_summary": f"Synthetic IP session from {ip}; device IMEI {imei}.", "collection_family": "synthetic_ipdr", "ip_address": ip, "imei": imei, "session_start_utc": stamp(start), "session_end_utc": stamp(end), "source_port": str(40000 + number), "protocol": "TCP", "bytes_up": str(1000 + number * 13), "bytes_down": str(8000 + number * 31), "synthetic_media": "true"})
    for suffix in ["", ".en"]:
        with (new / f"events{suffix}.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
        for kind, value in [("locations", locations), ("entities", entities)]:
            (new / f"{kind}{suffix}.json").write_bytes(json.dumps(value, ensure_ascii=False, indent=2).encode())
    path = ROOT / "demo_profiles/syria.json"
    profile = json.loads(path.read_text(encoding="utf-8"))
    profile.update(profile_version="5", dataset_version="network-v1")
    profile["files"] = {kind: f"data/syria_network_v1/{kind}.{'csv' if kind == 'events' else 'json'}" for kind in ["events", "locations", "entities"]}
    for locale in ["en", "he"]:
        profile["sources"][locale] = [s for s in profile["sources"][locale] if s not in ["ADINT", "IPDR"]] + ["ADINT", "IPDR"]
    profile["checksums"] = {key: value for key, value in profile["checksums"].items() if not key.startswith("data/")}
    profile["checksums"].update({p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest() for p in new.iterdir()})
    path.write_bytes(json.dumps(profile, ensure_ascii=False, indent=2).encode())
    print(f"Created {len(rows)} records: 4 existing, 4 ADINT, 200 IPDR")


if __name__ == "__main__":
    main()
