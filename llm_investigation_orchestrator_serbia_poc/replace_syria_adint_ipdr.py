"""Build an immutable Syria dataset revision from supplied ADINT and IPDR files."""

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path

from import_syria_adint import validate as validate_adint


ROOT = Path(__file__).resolve().parent
CURRENT_DATASET = ROOT / "data/syria_cellular_records_v1"
NEW_DATASET = ROOT / "data/syria_cellular_records_v12"
EXPECTED_IPDR_FIELDS = (
    "start_time", "end_time", "ip_source", "ip_target", "ip_public", "ip_private",
    "ip_out", "record_id", "source_port", "target_port", "public_port", "protocol",
    "bytes_sent", "bytes_received", "source_system", "imei", "mac", "SUBNETMASK",
)


def normalized_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def load_ipdr(path: Path) -> list[dict[str, str]]:
    rows = list(csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines()))
    if not rows or tuple(key.strip() for key in rows[0]) != EXPECTED_IPDR_FIELDS:
        raise ValueError("Unexpected IPDR source schema")
    identifiers = [row.get("record_id", "").strip() for row in rows]
    if not all(identifiers) or len(identifiers) != len(set(identifiers)):
        raise ValueError("IPDR record IDs must be populated and unique")
    return rows


def project_events(folder: Path, adint: list[dict], ipdr: list[dict[str, str]]) -> None:
    with (CURRENT_DATASET / "events.csv").open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        events = list(reader)
    adint_by_id = {row["observation_id"]: row for row in adint}
    ipdr_by_id = {row["record_id"]: row for row in ipdr}
    seen_adint, seen_ipdr = set(), set()
    for event in events:
        if event.get("source_type") == "ADINT":
            item = adint_by_id.get(event.get("observation_id", ""))
            if item is None:
                raise ValueError(f"Missing ADINT observation {event.get('observation_id')}")
            seen_adint.add(item["observation_id"])
            for key, value in item.items():
                event[key] = "" if value is None else str(value)
            event["ip_address"] = event["ip"]
            event["location_accuracy_m"] = event["accuracy_m"]
            event["event_summary"] = (
                f"ADINT observation {item['observation_id']}: device {item['device_id']}, "
                f"{item['brand']} {item['model']} ({item['os']})."
            )
        elif event.get("source_type") == "IPDR":
            item = ipdr_by_id.get(event.get("source_record_id", ""))
            if item is None:
                raise ValueError(f"Missing IPDR record {event.get('source_record_id')}")
            seen_ipdr.add(item["record_id"])
            for key, value in item.items():
                event["source_record_id" if key == "record_id" else key.strip()] = value
            event["timestamp_utc"] = item["start_time"]
            event["session_start_utc"] = item["start_time"]
            event["session_end_utc"] = item["end_time"]
            event["ip_address"] = item["ip_public"]
            event["bytes_up"] = item["bytes_sent"]
            event["bytes_down"] = item["bytes_received"]
            event["event_summary"] = (
                f"IPDR session {item['record_id']} from {item['ip_source']} to {item['ip_target']}; "
                f"public IP {item['ip_public']}; {item['protocol']}; source system {item['source_system']}."
            )
    if seen_adint != set(adint_by_id) or seen_ipdr != set(ipdr_by_id):
        raise ValueError("Source records and canonical events do not have one-to-one parity")
    for suffix in ("", ".en"):
        with (folder / f"events{suffix}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(events)


def write_ipdr_package(folder: Path, source: Path, rows: list[dict[str, str]]) -> None:
    checksum = hashlib.sha256(source.read_bytes()).hexdigest()
    fingerprint = checksum[:12].upper()
    package = json.loads((CURRENT_DATASET / "ipdr-package.json").read_text(encoding="utf-8"))
    package.update({
        "package_id": f"IPDRPKG-HOSHENTEL-{fingerprint}",
        "ingest_batch_id": f"IPDRBATCH-{fingerprint}",
        "sha256": checksum,
        "record_count": len(rows),
        "chain_of_custody_note": "Supplied CSV preserved byte-for-byte. Earlier acquisition and custody details are unavailable.",
    })
    (folder / "ipdr-package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")


def build(adint_source: Path, ipdr_source: Path) -> dict:
    if NEW_DATASET.exists():
        raise ValueError(f"Refusing to overwrite immutable dataset {NEW_DATASET.name}")
    adint_raw = adint_source.read_bytes()
    adint = validate_adint(json.loads(adint_raw.decode("utf-8-sig")))
    ipdr = load_ipdr(ipdr_source)
    shutil.copytree(CURRENT_DATASET, NEW_DATASET)
    (NEW_DATASET / "ADINT.json").write_bytes(adint_raw)
    (NEW_DATASET / "IPDR-expanded.csv").write_bytes(ipdr_source.read_bytes())
    project_events(NEW_DATASET, adint, ipdr)
    write_ipdr_package(NEW_DATASET, ipdr_source, ipdr)
    profile_path = ROOT / "demo_profiles/syria.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile.update(profile_version="35", dataset_version="cellular-records-v12")
    profile["files"] = {
        "events": "data/syria_cellular_records_v12/events.csv",
        "locations": "data/syria_cellular_records_v12/locations.json",
        "entities": "data/syria_cellular_records_v12/entities.json",
    }
    profile["checksums"] = {
        key: value for key, value in profile["checksums"].items()
        if not key.startswith("data/syria_cellular_records_v1/")
    }
    profile["checksums"].update({
        path.relative_to(ROOT).as_posix(): normalized_digest(path)
        for path in NEW_DATASET.iterdir() if path.is_file()
    })
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "dataset": NEW_DATASET.name,
        "adint_records": len(adint),
        "ipdr_records": len(ipdr),
        "adint_sha256": hashlib.sha256(adint_raw).hexdigest(),
        "ipdr_sha256": hashlib.sha256(ipdr_source.read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("adint", type=Path)
    parser.add_argument("ipdr", type=Path)
    print(json.dumps(build(parser.parse_args().adint, parser.parse_args().ipdr), indent=2))
