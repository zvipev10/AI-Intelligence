"""Neutral evidence projection and persistence for the synthetic intelligence dataset."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    from evidence_semantics import normalize_evidence_event
except ImportError:  # pragma: no cover - package-style execution fallback
    from .evidence_semantics import normalize_evidence_event


UAV_FAMILY = "airborne_isr_video_exploitation"
VALID_STATUSES = frozenset({"reported", "observed", "fused"})
VALID_CONFIDENCE = frozenset({"low", "medium", "high"})
CONTRADICTION_MARKERS = ("מכחיש", "הכחיש", "סותר", "לא אותו", "אינו אותו")


def _text(value: Any) -> str:
    return str(value or "").strip()


def _confidence(value: Any) -> str:
    normalized = _text(value).lower()
    if normalized in {"high", "confirmed", "גבוהה"}:
        return "high"
    if normalized in {"medium", "likely", "בינונית"}:
        return "medium"
    return "low"


def projected_evidence_id(record_id: str) -> str:
    return f"EVD-{record_id}"


def project_event(event: dict[str, Any]) -> dict[str, Any]:
    """Project one immutable source record into a normalized evidence object."""
    event = normalize_evidence_event(event)
    record_id = _text(event.get("event_id") or event.get("record_id"))
    if not record_id.startswith("REC-"):
        raise ValueError("evidence projection requires a canonical REC record")
    observed = _text(event.get("collection_family")) == UAV_FAMILY
    status = "observed" if observed else "reported"
    confidence_source = (
        event.get("identification_confidence") or event.get("geolocation_confidence")
        if observed else event.get("source_reliability_label") or event.get("certainty_level")
    )
    object_class = _text(event.get("object_class")) or None
    claim_type = "object_presence" if object_class else "entity_activity"
    count = event.get("estimated_object_count")
    quantity = int(count) if str(count or "").isdigit() else None
    return {
        "evidence_id": projected_evidence_id(record_id),
        "evidence_status": status,
        "claim_type": claim_type,
        "subject_entity_ids": [_text(event.get("entity_id"))] if _text(event.get("entity_id")) else [],
        "object_class": object_class,
        "object_class_resolution": event.get("object_class_resolution"),
        "location_ids": [_text(event.get("location_id"))] if _text(event.get("location_id")) else [],
        "valid_from": _text(event.get("timestamp_utc")) or None,
        "valid_to": _text(event.get("timestamp_utc")) or None,
        "confidence": _confidence(confidence_source),
        "source_record_ids": [record_id],
        "source_groups": [
            f"uav-mission:{_text(event.get('mission_id'))}"
            if observed and _text(event.get("mission_id"))
            else f"source-record:{record_id}"
        ],
        "quantity": {"estimate": quantity, "min": quantity, "max": quantity} if quantity is not None else None,
        "movement": {
            "status": _text(event.get("movement_status")) or None,
            "direction": _text(event.get("movement_direction")) or None,
        } if observed else None,
        "supporting_evidence_ids": [],
        "contradicting_evidence_ids": [],
        "summary": _text(event.get("event_summary")),
        "created_by_processor": "record-projection-v1",
        "persisted": False,
    }


def prepare_fused_object(events: Iterable[dict[str, Any]], fusion: dict[str, Any]) -> dict[str, Any]:
    rows = list(events)
    if not rows:
        raise ValueError("at least one source record is required")
    locations = {_text(row.get("location_id")) for row in rows if _text(row.get("location_id"))}
    entities = {_text(row.get("entity_id")) for row in rows if _text(row.get("entity_id"))}
    structured_objects = {_text(row.get("object_class")) for row in rows if _text(row.get("object_class"))}
    reasons = list(fusion.get("persistence_block_reasons") or [])
    if len(locations) != 1:
        reasons.append("fused evidence requires one canonical location")
    if len(entities) != 1:
        reasons.append("fused evidence requires one canonical subject entity")
    if len(structured_objects) != 1:
        reasons.append("fused evidence requires one resolved structured object class")
    record_ids = sorted({_text(row.get("event_id") or row.get("record_id")) for row in rows})
    digest = hashlib.sha256("\n".join(record_ids).encode("utf-8")).hexdigest()[:20].upper()
    timestamps = sorted(_text(row.get("timestamp_utc")) for row in rows if _text(row.get("timestamp_utc")))
    snapshots = list(fusion.get("evidence") or [])
    contradicting_records = {
        _text(row.get("event_id") or row.get("record_id"))
        for row in rows
        if any(marker in _text(row.get("event_summary")) for marker in CONTRADICTION_MARKERS)
    }
    supporting_ids = [projected_evidence_id(record_id) for record_id in record_ids if record_id not in contradicting_records]
    contradicting_ids = [projected_evidence_id(record_id) for record_id in record_ids if record_id in contradicting_records]
    source_groups = sorted({str(item.get("source_group")) for item in snapshots if item.get("source_group")})
    supporting_groups = {
        str(item.get("source_group"))
        for item in snapshots
        if item.get("source_group") and _text(item.get("event_id") or item.get("record_id")) not in contradicting_records
    }
    if len(supporting_groups) < 2:
        reasons.append("fused evidence requires at least two independent supporting source groups")
    quantity = fusion.get("quantity") or {}
    confidence = _text(fusion.get("confidence")).lower()
    return {
        "evidence_id": f"EVD-FUSED-{digest}",
        "evidence_status": "fused",
        "claim_type": "object_presence",
        "subject_entity_ids": sorted(entities),
        "object_class": next(iter(structured_objects), None),
        "location_ids": sorted(locations),
        "valid_from": timestamps[0] if timestamps else None,
        "valid_to": timestamps[-1] if timestamps else None,
        "confidence": confidence if confidence in VALID_CONFIDENCE else "low",
        "source_record_ids": record_ids,
        "source_groups": source_groups,
        "quantity": {
            "min": quantity.get("count_min"),
            "max": quantity.get("count_max"),
            "estimate": quantity.get("count_estimate"),
            "assessment": quantity.get("count_assessment"),
        },
        "movement": None,
        "supporting_evidence_ids": supporting_ids,
        "contradicting_evidence_ids": contradicting_ids,
        "summary": f"Fused {next(iter(structured_objects), 'evidence')} at {next(iter(locations), 'unknown location')} from {len(record_ids)} source records.",
        "created_by_processor": "neutral-fusion-v1",
        "persistence_eligible": bool(fusion.get("persistence_eligible")) and not reasons,
        "persistence_block_reasons": reasons,
        "persisted": False,
    }


class EvidenceStore:
    def __init__(self, db_path: Path | None = None, catalog_path: Path | None = None):
        default = Path(__file__).resolve().parent.parent / "data" / "evidence" / "evidence.db"
        self.db_path = Path(db_path or os.environ.get("INTELLIGENCE_POC_EVIDENCE_STORE", default))
        configured_catalog = os.environ.get("INTELLIGENCE_POC_EVIDENCE_CATALOG")
        self.catalog_path = Path(catalog_path or configured_catalog) if (catalog_path or configured_catalog) else None
        self._catalog_by_id: dict[str, dict[str, Any]] | None = None

    def _catalog(self) -> dict[str, dict[str, Any]]:
        if self._catalog_by_id is not None:
            return self._catalog_by_id
        rows: list[dict[str, Any]] = []
        if self.catalog_path and self.catalog_path.is_file():
            try:
                payload = json.loads(self.catalog_path.read_text(encoding="utf-8"))
                rows = payload.get("rows") if isinstance(payload.get("rows"), list) else []
            except (OSError, json.JSONDecodeError):
                rows = []
        self._catalog_by_id = {
            str(row.get("evidence_id")): row
            for row in rows
            if row.get("evidence_id") and row.get("evidence_status") == "fused"
        }
        return self._catalog_by_id

    def _stored_rows(self) -> list[dict[str, Any]]:
        if not self.db_path.is_file():
            return []
        try:
            with closing(sqlite3.connect(self.db_path, timeout=15)) as connection:
                rows = connection.execute("SELECT payload_json FROM evidence_objects").fetchall()
        except sqlite3.OperationalError:
            return []
        return [json.loads(row[0]) for row in rows]

    def initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.db_path, timeout=15)) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS evidence_objects (
                    evidence_id TEXT PRIMARY KEY,
                    evidence_status TEXT NOT NULL,
                    confidence TEXT NOT NULL,
                    location_id TEXT,
                    entity_id TEXT,
                    object_class TEXT,
                    valid_from TEXT,
                    valid_to TEXT,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            connection.execute("CREATE INDEX IF NOT EXISTS evidence_location_idx ON evidence_objects(location_id)")
            connection.execute("CREATE INDEX IF NOT EXISTS evidence_entity_idx ON evidence_objects(entity_id)")
            connection.commit()

    def put_fused(self, evidence: dict[str, Any]) -> dict[str, Any]:
        if evidence.get("evidence_status") != "fused":
            raise ValueError("only fused evidence may be persisted")
        if not evidence.get("persistence_eligible"):
            raise ValueError("fused evidence is not persistence eligible")
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        stored = {**evidence, "persisted": True}
        payload = json.dumps(stored, ensure_ascii=False, sort_keys=True)
        with closing(sqlite3.connect(self.db_path, timeout=15)) as connection:
            connection.execute("""
                INSERT INTO evidence_objects (
                    evidence_id, evidence_status, confidence, location_id, entity_id,
                    object_class, valid_from, valid_to, payload_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(evidence_id) DO UPDATE SET payload_json=excluded.payload_json,
                    confidence=excluded.confidence, valid_from=excluded.valid_from,
                    valid_to=excluded.valid_to, updated_at=excluded.updated_at
            """, (
                stored["evidence_id"], stored["evidence_status"], stored["confidence"],
                (stored.get("location_ids") or [None])[0], (stored.get("subject_entity_ids") or [None])[0],
                stored.get("object_class"), stored.get("valid_from"), stored.get("valid_to"),
                payload, now, now,
            ))
            connection.commit()
        return stored

    def get(self, evidence_id: str) -> dict[str, Any] | None:
        if self.db_path.is_file():
            try:
                with closing(sqlite3.connect(self.db_path, timeout=15)) as connection:
                    row = connection.execute("SELECT payload_json FROM evidence_objects WHERE evidence_id = ?", (evidence_id,)).fetchone()
                if row:
                    return json.loads(row[0])
            except sqlite3.OperationalError:
                pass
        return self._catalog().get(evidence_id)

    def search(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        limit = min(max(int(filters.get("limit") or 100), 1), 500)
        combined = {**self._catalog(), **{row["evidence_id"]: row for row in self._stored_rows()}}

        def matches(row: dict[str, Any]) -> bool:
            return all(
                not _text(filters.get(field)) or _text(value) == _text(filters[field])
                for field, value in (
                    ("location_id", (row.get("location_ids") or [None])[0]),
                    ("entity_id", (row.get("subject_entity_ids") or [None])[0]),
                    ("evidence_status", row.get("evidence_status")),
                )
            )

        rows = [row for row in combined.values() if matches(row)]
        rows.sort(key=lambda row: (_text(row.get("valid_from")), _text(row.get("evidence_id"))), reverse=True)
        return rows[:limit]
