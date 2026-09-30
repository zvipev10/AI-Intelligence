"""Validated evidence views of existing IPDR records; never a second stored record."""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path


def interval_validation(start, end):
    if not start or not end:
        return {"state": "unknown", "duration_seconds": None, "issues": ["missing_session_time"]}
    try:
        times = [datetime.fromisoformat(str(t).replace("Z", "+00:00")) for t in (start, end)]
        if any(t.tzinfo is None for t in times):
            raise ValueError("timezone missing")
        duration = (times[1] - times[0]).total_seconds()
    except (ValueError, TypeError):
        return {"state": "invalid", "duration_seconds": None, "issues": ["invalid_session_time"]}
    if duration < 0:
        return {"state": "invalid", "duration_seconds": duration, "issues": ["reversed_session_interval"]}
    return {"state": "valid", "duration_seconds": duration, "issues": []}


def record_evidence(event):
    """An addressable REC observation, independent of identity or presence claims."""
    record_id = event.get("event_id") or event.get("record_id")
    if not str(record_id).startswith("REC-"):
        raise ValueError("IPDR evidence requires an existing REC identity")
    return {
        **event, "evidence_id": record_id, "evidence_type": "ipdr_record",
        "record_type": "network_session", "evidence_status": "observed",
        "claim_type": "network_session", "subject_entity_ids": [], "location_ids": [],
        "source_record_ids": [record_id], "supporting_evidence_ids": [],
        "contradicting_evidence_ids": [], "valid_from": event.get("start_time") or None,
        "valid_to": event.get("end_time") or None,
        "validation": interval_validation(event.get("start_time"), event.get("end_time")),
        "summary": event.get("event_summary", ""), "persisted": False,
        "created_by_processor": "ipdr-source-view-v1",
    }


def attach_package(events, events_path: Path):
    """Validate native parity before assigning package membership in memory.

    Historical datasets without a manifest retain their original representation.
    A present but invalid manifest/source is an error, never silently ignored.
    """
    manifest_path = Path(events_path).parent / "ipdr-package.json"
    if not manifest_path.is_file():
        return None
    package = json.loads(manifest_path.read_text(encoding="utf-8"))
    filename = package["filename"]
    if Path(filename).name != filename:
        raise ValueError("IPDR source filename must be local to the dataset")
    source_path = manifest_path.parent / filename
    if hashlib.sha256(source_path.read_bytes()).hexdigest() != package["sha256"]:
        raise ValueError("IPDR package checksum mismatch")
    with source_path.open(encoding="utf-8-sig", newline="") as handle:
        raw = [{k.strip(): v for k, v in row.items()} for row in csv.DictReader(handle)]
    rows = [row for row in events if row.get("source_type") == "IPDR"]
    if len(raw) != package["record_count"] or len(rows) != len(raw):
        raise ValueError("IPDR package record count mismatch")
    by_native = {row.get("source_record_id"): row for row in rows}
    if len(by_native) != len(rows) or len({r["record_id"] for r in raw}) != len(raw):
        raise ValueError("IPDR native identities are not unique")
    if len({r["event_id"] for r in rows}) != len(rows):
        raise ValueError("IPDR REC identities are not unique")
    projected = []
    for source_row, native in enumerate(raw, start=1):
        row = by_native.get(native["record_id"])
        if row is None or any(row.get("source_record_id" if key == "record_id" else key) != value for key, value in native.items()):
            raise ValueError("IPDR package native field parity failed")
        projected.append((row, {
            "package_id": package["package_id"], "ingest_batch_id": package["ingest_batch_id"],
            "evidence_type": "ipdr_record", "record_type": "network_session",
            "source_reference": {"filename": filename, "sha256": package["sha256"], "data_row": source_row},
            "validation": interval_validation(row.get("start_time"), row.get("end_time")),
        }))
    for row, metadata in projected:
        row.update(metadata)
    states = {state: sum(meta["validation"]["state"] == state for _, meta in projected) for state in ("valid", "invalid", "unknown")}
    valid_times = []
    for row in rows:
        for key in ("start_time", "end_time"):
            try:
                t = datetime.fromisoformat(row[key].replace("Z", "+00:00"))
                if t.tzinfo is not None:
                    valid_times.append(t)
            except (ValueError, TypeError):
                pass
    return {
        **package, "evidence_type": "ipdr_package", "validation_state": "verified",
        "session_validation_counts": states,
        "observed_coverage": {"from": min(valid_times).isoformat(), "to": max(valid_times).isoformat()} if valid_times else None,
        "catalog_layer_id": f"ipdr-package:{package['package_id']}",
    }
