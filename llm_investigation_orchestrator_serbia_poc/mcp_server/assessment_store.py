"""Durable, revisioned enemy assessments with controlled analytical overlays."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATUSES = {"draft", "current", "superseded", "closed"}
CONFIDENCE = {"low", "medium", "high"}
OVERLAY_GEOMETRY = {
    "point": "Point",
    "assessed_area": "Polygon",
    "route_axis": "LineString",
    "confidence_envelope": "Polygon",
}


def _text(value: Any, field: str, maximum: int = 4000, required: bool = False) -> str:
    result = str(value or "").strip()
    if required and not result:
        raise ValueError(f"{field} is required")
    if len(result) > maximum:
        raise ValueError(f"{field} exceeds {maximum} characters")
    return result


def _strings(value: Any, field: str, maximum: int = 100) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError(f"{field} must be an array with at most {maximum} items")
    return list(dict.fromkeys(_text(item, field, 500, True) for item in value))


def _position(value: Any) -> list[float]:
    if not isinstance(value, list) or len(value) < 2:
        raise ValueError("overlay coordinates require [longitude, latitude]")
    lon, lat = float(value[0]), float(value[1])
    if not -180 <= lon <= 180 or not -90 <= lat <= 90:
        raise ValueError("overlay coordinate is outside longitude/latitude bounds")
    return [lon, lat]


def _geometry(feature_type: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("type") != OVERLAY_GEOMETRY[feature_type]:
        raise ValueError(f"{feature_type} requires {OVERLAY_GEOMETRY[feature_type]} geometry")
    coordinates = value.get("coordinates")
    if feature_type == "point":
        normalized = _position(coordinates)
    elif feature_type == "route_axis":
        if not isinstance(coordinates, list) or not 2 <= len(coordinates) <= 200:
            raise ValueError("route_axis requires 2-200 positions")
        normalized = [_position(item) for item in coordinates]
    else:
        if not isinstance(coordinates, list) or not coordinates or not isinstance(coordinates[0], list):
            raise ValueError(f"{feature_type} requires polygon rings")
        if sum(len(ring) for ring in coordinates) > 200:
            raise ValueError("overlay polygon exceeds 200 positions")
        normalized = []
        for ring in coordinates:
            points = [_position(item) for item in ring]
            if len(points) < 4 or points[0] != points[-1]:
                raise ValueError("overlay polygon rings must be closed with at least four positions")
            normalized.append(points)
    return {"type": value["type"], "coordinates": normalized}


def normalize_assessment(payload: dict[str, Any], assessment_id: str | None = None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("assessment payload must be an object")
    status = _text(payload.get("status") or "draft", "status").lower()
    if status not in STATUSES:
        raise ValueError("invalid assessment status")
    judgments = payload.get("key_judgments") or []
    if not isinstance(judgments, list) or not judgments or len(judgments) > 20:
        raise ValueError("key_judgments requires 1-20 judgments")
    normalized_judgments = []
    evidence_ids: list[str] = []
    for index, judgment in enumerate(judgments, 1):
        if not isinstance(judgment, dict):
            raise ValueError(f"judgment {index} must be an object")
        confidence = _text(judgment.get("confidence"), "confidence").lower()
        if confidence not in CONFIDENCE:
            raise ValueError(f"judgment {index} has invalid confidence")
        ids = _strings(judgment.get("evidence_ids"), "evidence_ids")
        evidence_ids.extend(ids)
        normalized_judgments.append({
            "judgment": _text(judgment.get("judgment"), "judgment", 2000, True),
            "confidence": confidence,
            "evidence_ids": ids,
        })
    overlays = payload.get("overlays") or []
    if not isinstance(overlays, list) or len(overlays) > 20:
        raise ValueError("overlays must contain at most 20 features")
    normalized_overlays = []
    for index, overlay in enumerate(overlays, 1):
        if not isinstance(overlay, dict):
            raise ValueError(f"overlay {index} must be an object")
        feature_type = _text(overlay.get("type"), "overlay type").lower()
        if feature_type not in OVERLAY_GEOMETRY:
            raise ValueError(f"unsupported overlay type: {feature_type}")
        confidence = _text(overlay.get("confidence"), "overlay confidence").lower()
        if confidence not in CONFIDENCE:
            raise ValueError(f"overlay {index} has invalid confidence")
        ids = _strings(overlay.get("supporting_evidence_ids"), "supporting_evidence_ids")
        evidence_ids.extend(ids)
        normalized_overlays.append({
            "overlay_id": _text(overlay.get("overlay_id") or f"OVL-{index}", "overlay_id", 80, True),
            "type": feature_type,
            "meaning": _text(overlay.get("meaning"), "overlay meaning", 500, True),
            "geometry": _geometry(feature_type, overlay.get("geometry")),
            "confidence": confidence,
            "valid_from": _text(overlay.get("valid_from"), "valid_from", 80) or None,
            "valid_to": _text(overlay.get("valid_to"), "valid_to", 80) or None,
            "supporting_evidence_ids": ids,
        })
    return {
        "assessment_id": assessment_id,
        "title": _text(payload.get("title"), "title", 200, True),
        "status": status,
        "scope": {
            "location_ids": _strings((payload.get("scope") or {}).get("location_ids"), "scope.location_ids", 50),
            "entity_ids": _strings((payload.get("scope") or {}).get("entity_ids"), "scope.entity_ids", 50),
            "valid_from": _text((payload.get("scope") or {}).get("valid_from"), "scope.valid_from", 80) or None,
            "valid_to": _text((payload.get("scope") or {}).get("valid_to"), "scope.valid_to", 80) or None,
        },
        "key_judgments": normalized_judgments,
        "confidence": min((item["confidence"] for item in normalized_judgments), key=("low", "medium", "high").index),
        "alternatives": _strings(payload.get("alternatives"), "alternatives", 20),
        "contradictions": _strings(payload.get("contradictions"), "contradictions", 50),
        "intelligence_gaps": _strings(payload.get("intelligence_gaps"), "intelligence_gaps", 50),
        "indicators": _strings(payload.get("indicators"), "indicators", 50),
        "evidence_ids": list(dict.fromkeys(evidence_ids + _strings(payload.get("evidence_ids"), "evidence_ids"))),
        "overlays": normalized_overlays,
        "summary": _text(payload.get("summary"), "summary", 4000, True),
    }


class AssessmentStore:
    def __init__(self, db_path: Path | None = None):
        default = Path(__file__).resolve().parent.parent / "data" / "assessments" / "assessments.db"
        self.db_path = Path(db_path or os.environ.get("INTELLIGENCE_POC_ASSESSMENT_STORE", default))

    def initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.db_path, timeout=15)) as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS assessments (
                    assessment_id TEXT PRIMARY KEY, status TEXT NOT NULL, title TEXT NOT NULL,
                    revision INTEGER NOT NULL, payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS assessment_revisions (
                    assessment_id TEXT NOT NULL, revision INTEGER NOT NULL,
                    payload_json TEXT NOT NULL, created_at TEXT NOT NULL,
                    PRIMARY KEY (assessment_id, revision)
                );
                CREATE INDEX IF NOT EXISTS assessment_status_idx ON assessments(status);
            """)
            connection.commit()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def create(self, payload: dict[str, Any], created_by: str = "talia") -> dict[str, Any]:
        normalized = normalize_assessment(payload)
        digest = hashlib.sha256(json.dumps(normalized, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16].upper()
        assessment_id = f"ASM-{digest}"
        now = self._now()
        stored = {**normalized, "assessment_id": assessment_id, "revision": 1, "created_by": created_by,
                  "created_at": now, "updated_at": now}
        encoded = json.dumps(stored, ensure_ascii=False, sort_keys=True)
        self.initialize()
        with closing(sqlite3.connect(self.db_path, timeout=15)) as connection:
            existing = connection.execute("SELECT payload_json FROM assessments WHERE assessment_id = ?", (assessment_id,)).fetchone()
            if existing:
                return json.loads(existing[0])
            connection.execute("INSERT INTO assessments VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (assessment_id, stored["status"], stored["title"], 1, encoded, now, now))
            connection.execute("INSERT INTO assessment_revisions VALUES (?, ?, ?, ?)", (assessment_id, 1, encoded, now))
            connection.commit()
        return stored

    def get(self, assessment_id: str) -> dict[str, Any] | None:
        self.initialize()
        with closing(sqlite3.connect(self.db_path, timeout=15)) as connection:
            row = connection.execute("SELECT payload_json FROM assessments WHERE assessment_id = ?", (assessment_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def update(self, assessment_id: str, payload: dict[str, Any], expected_revision: int) -> dict[str, Any]:
        current = self.get(assessment_id)
        if current is None:
            raise LookupError("assessment not found")
        if current["revision"] != expected_revision:
            raise ValueError(f"stale assessment revision; current revision is {current['revision']}")
        merged = {**current, **payload}
        normalized = normalize_assessment(merged, assessment_id)
        revision, now = expected_revision + 1, self._now()
        stored = {**current, **normalized, "revision": revision, "updated_at": now}
        encoded = json.dumps(stored, ensure_ascii=False, sort_keys=True)
        with closing(sqlite3.connect(self.db_path, timeout=15)) as connection:
            connection.execute("UPDATE assessments SET status=?, title=?, revision=?, payload_json=?, updated_at=? WHERE assessment_id=?",
                               (stored["status"], stored["title"], revision, encoded, now, assessment_id))
            connection.execute("INSERT INTO assessment_revisions VALUES (?, ?, ?, ?)", (assessment_id, revision, encoded, now))
            connection.commit()
        return stored

    def search(self, status: str | None = None, query: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        self.initialize()
        clauses, values = [], []
        if status:
            if status not in STATUSES:
                raise ValueError("invalid assessment status")
            clauses.append("status = ?"); values.append(status)
        if query:
            clauses.append("title LIKE ?"); values.append(f"%{query}%")
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        with closing(sqlite3.connect(self.db_path, timeout=15)) as connection:
            rows = connection.execute(f"SELECT payload_json FROM assessments{where} ORDER BY updated_at DESC LIMIT ?",
                                      (*values, min(max(int(limit), 1), 500))).fetchall()
        return [json.loads(row[0]) for row in rows]

    def supersede(self, assessment_id: str, expected_revision: int) -> dict[str, Any]:
        return self.update(assessment_id, {"status": "superseded"}, expected_revision)
