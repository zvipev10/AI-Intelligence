"""SQLite persistence for final-state attack-target candidates."""

from __future__ import annotations

import os
import sqlite3
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_DB_PATH = Path(os.environ.get(
    "INTELLIGENCE_POC_TARGET_BANK",
    "/opt/serbia-poc/data/attack_targets/attack_targets.db",
))
DEFAULT_BACKUP_DIR = Path(os.environ.get(
    "INTELLIGENCE_POC_TARGET_BACKUPS",
    "/opt/serbia-poc/backups/attack_targets",
))
ALLOWED_CONFIDENCE = frozenset({"medium", "high"})
ALLOWED_COUNT_ASSESSMENTS = frozenset({"exact", "approximate", "range", "unresolved"})
TARGET_MUTABLE_FIELDS = frozenset({
    "title", "summary", "object_class", "entity_id", "location_id", "confidence",
    "count_min", "count_max", "count_estimate", "count_assessment",
    "fusion_explanation", "mission_run_id",
})


SCHEMA = """
CREATE TABLE IF NOT EXISTS targets (
    target_id TEXT PRIMARY KEY,
    title TEXT NOT NULL CHECK(length(trim(title)) > 0),
    summary TEXT NOT NULL CHECK(length(trim(summary)) > 0),
    status TEXT NOT NULL DEFAULT 'candidate' CHECK(status = 'candidate'),
    object_class TEXT NOT NULL CHECK(length(trim(object_class)) > 0),
    entity_id TEXT,
    location_id TEXT NOT NULL CHECK(length(trim(location_id)) > 0),
    confidence TEXT NOT NULL CHECK(confidence IN ('medium', 'high')),
    count_min INTEGER CHECK(count_min IS NULL OR count_min >= 0),
    count_max INTEGER CHECK(count_max IS NULL OR count_max >= 0),
    count_estimate INTEGER CHECK(count_estimate IS NULL OR count_estimate >= 0),
    count_assessment TEXT NOT NULL CHECK(count_assessment IN ('exact', 'approximate', 'range', 'unresolved')),
    fusion_explanation TEXT NOT NULL CHECK(length(trim(fusion_explanation)) > 0),
    mission_run_id TEXT NOT NULL CHECK(length(trim(mission_run_id)) > 0),
    created_by TEXT NOT NULL CHECK(length(trim(created_by)) > 0),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    reviewed_by TEXT,
    reviewed_at TEXT,
    review_note TEXT,
    CHECK(count_min IS NULL OR count_max IS NULL OR count_min <= count_max),
    CHECK(count_estimate IS NULL OR count_min IS NULL OR count_estimate >= count_min),
    CHECK(count_estimate IS NULL OR count_max IS NULL OR count_estimate <= count_max)
);

CREATE TABLE IF NOT EXISTS target_evidence (
    target_id TEXT NOT NULL REFERENCES targets(target_id) ON DELETE CASCADE,
    record_id TEXT NOT NULL CHECK(length(trim(record_id)) > 0),
    source_group TEXT NOT NULL CHECK(length(trim(source_group)) > 0),
    source_type TEXT NOT NULL CHECK(length(trim(source_type)) > 0),
    observed_at TEXT NOT NULL CHECK(length(trim(observed_at)) > 0),
    location_id TEXT NOT NULL CHECK(length(trim(location_id)) > 0),
    reported_object TEXT NOT NULL CHECK(length(trim(reported_object)) > 0),
    reported_count INTEGER CHECK(reported_count IS NULL OR reported_count >= 0),
    relevant_text TEXT NOT NULL CHECK(length(trim(relevant_text)) > 0),
    evidence_role TEXT NOT NULL CHECK(length(trim(evidence_role)) > 0),
    added_at TEXT NOT NULL,
    PRIMARY KEY (target_id, record_id)
);

CREATE INDEX IF NOT EXISTS idx_targets_candidate_match
ON targets(object_class, entity_id, location_id, updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_target_evidence_source_group
ON target_evidence(target_id, source_group);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _required_text(value: Any, name: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        raise ValueError(f"{name} is required")
    return normalized


def _optional_text(value: Any) -> str | None:
    normalized = str(value or "").strip()
    return normalized or None


def _optional_count(value: Any, name: str) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a non-negative integer")
    normalized = int(value)
    if normalized < 0 or normalized != value:
        raise ValueError(f"{name} must be a non-negative integer")
    return normalized


def normalize_candidate(value: dict[str, Any], *, require_creator: bool) -> dict[str, Any]:
    confidence = _required_text(value.get("confidence"), "confidence")
    if confidence not in ALLOWED_CONFIDENCE:
        raise ValueError("confidence must be medium or high")
    count_assessment = _required_text(value.get("count_assessment"), "count_assessment")
    if count_assessment not in ALLOWED_COUNT_ASSESSMENTS:
        raise ValueError("count_assessment must be exact, approximate, range, or unresolved")
    count_min = _optional_count(value.get("count_min"), "count_min")
    count_max = _optional_count(value.get("count_max"), "count_max")
    count_estimate = _optional_count(value.get("count_estimate"), "count_estimate")
    if count_min is not None and count_max is not None and count_min > count_max:
        raise ValueError("count_min cannot exceed count_max")
    if count_estimate is not None and count_min is not None and count_estimate < count_min:
        raise ValueError("count_estimate cannot be below count_min")
    if count_estimate is not None and count_max is not None and count_estimate > count_max:
        raise ValueError("count_estimate cannot exceed count_max")
    result = {
        "title": _required_text(value.get("title"), "title"),
        "summary": _required_text(value.get("summary"), "summary"),
        "object_class": _required_text(value.get("object_class"), "object_class"),
        "entity_id": _optional_text(value.get("entity_id")),
        "location_id": _required_text(value.get("location_id"), "location_id"),
        "confidence": confidence,
        "count_min": count_min,
        "count_max": count_max,
        "count_estimate": count_estimate,
        "count_assessment": count_assessment,
        "fusion_explanation": _required_text(value.get("fusion_explanation"), "fusion_explanation"),
        "mission_run_id": _required_text(value.get("mission_run_id"), "mission_run_id"),
    }
    if require_creator:
        result["created_by"] = _required_text(value.get("created_by"), "created_by")
    return result


def normalize_evidence(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_id": _required_text(value.get("record_id"), "record_id"),
        "source_group": _required_text(value.get("source_group"), "source_group"),
        "source_type": _required_text(value.get("source_type"), "source_type"),
        "observed_at": _required_text(value.get("observed_at"), "observed_at"),
        "location_id": _required_text(value.get("location_id"), "location_id"),
        "reported_object": _required_text(value.get("reported_object"), "reported_object"),
        "reported_count": _optional_count(value.get("reported_count"), "reported_count"),
        "relevant_text": _required_text(value.get("relevant_text"), "relevant_text"),
        "evidence_role": _required_text(value.get("evidence_role"), "evidence_role"),
    }


class TargetBank:
    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH, backup_dir: Path | str = DEFAULT_BACKUP_DIR):
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)

    def initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._apply_mode(self.db_path.parent, 0o700)
        with self.connect() as connection:
            connection.executescript(SCHEMA)
        self._apply_mode(self.db_path, 0o600)

    @staticmethod
    def _apply_mode(path: Path, mode: int) -> None:
        try:
            path.chmod(mode)
        except OSError:
            if os.name != "nt":
                raise

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.db_path, timeout=15)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 15000")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def create_candidate(self, candidate: dict[str, Any], evidence: Iterable[dict[str, Any]]) -> dict[str, Any]:
        normalized = normalize_candidate(candidate, require_creator=True)
        normalized_evidence = [normalize_evidence(item) for item in evidence]
        if len({item["source_group"] for item in normalized_evidence}) < 2:
            raise ValueError("a candidate requires at least two independent source groups")
        if len({item["record_id"] for item in normalized_evidence}) != len(normalized_evidence):
            raise ValueError("evidence record_id values must be unique per target")
        target_id = _optional_text(candidate.get("target_id")) or f"TGT-{uuid.uuid4().hex[:12].upper()}"
        now = utc_now()
        columns = list(normalized)
        try:
            with self.connect() as connection:
                connection.execute(
                    f"INSERT INTO targets (target_id, status, created_at, updated_at, {', '.join(columns)}) "
                    f"VALUES (?, 'candidate', ?, ?, {', '.join('?' for _ in columns)})",
                    [target_id, now, now, *(normalized[column] for column in columns)],
                )
                self._insert_evidence(connection, target_id, normalized_evidence, now)
        except sqlite3.IntegrityError as exc:
            raise ValueError("candidate or evidence violates the target-bank contract") from exc
        return self.get_candidate(target_id)

    @staticmethod
    def _insert_evidence(connection: sqlite3.Connection, target_id: str, evidence: list[dict[str, Any]], now: str) -> None:
        for item in evidence:
            connection.execute(
                """INSERT INTO target_evidence (
                    target_id, record_id, source_group, source_type, observed_at, location_id,
                    reported_object, reported_count, relevant_text, evidence_role, added_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (target_id, item["record_id"], item["source_group"], item["source_type"], item["observed_at"],
                 item["location_id"], item["reported_object"], item["reported_count"], item["relevant_text"],
                 item["evidence_role"], now),
            )

    def get_candidate(self, target_id: str) -> dict[str, Any]:
        with self.connect() as connection:
            target = connection.execute("SELECT * FROM targets WHERE target_id = ?", (_required_text(target_id, "target_id"),)).fetchone()
            if target is None:
                raise ValueError("target candidate not found")
            evidence = connection.execute(
                "SELECT * FROM target_evidence WHERE target_id = ? ORDER BY observed_at, record_id", (target_id,),
            ).fetchall()
        result = dict(target)
        result["evidence"] = [dict(item) for item in evidence]
        result["source_group_count"] = len({item["source_group"] for item in result["evidence"]})
        result["source_types"] = sorted({item["source_type"] for item in result["evidence"]})
        result["evidence_count"] = len(result["evidence"])
        return result

    def search_candidates(self, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        filters = filters or {}
        clauses = ["status = 'candidate'"]
        parameters: list[Any] = []
        for field in ("object_class", "entity_id", "location_id", "mission_run_id"):
            value = _optional_text(filters.get(field))
            if value:
                clauses.append(f"t.{field} = ?")
                parameters.append(value)
        limit = int(filters.get("limit", 100))
        if limit < 1 or limit > 500:
            raise ValueError("limit must be between 1 and 500")
        parameters.append(limit)
        with self.connect() as connection:
            rows = connection.execute(
                f"""SELECT t.*, COUNT(e.record_id) AS evidence_count,
                    COUNT(DISTINCT e.source_group) AS source_group_count,
                    GROUP_CONCAT(DISTINCT e.source_type) AS source_types_csv,
                    GROUP_CONCAT(e.record_id, ',') AS evidence_record_ids_csv
                    FROM targets t LEFT JOIN target_evidence e ON e.target_id = t.target_id
                    WHERE {' AND '.join(clauses)} GROUP BY t.target_id
                    ORDER BY t.updated_at DESC, t.target_id LIMIT ?""",
                parameters,
            ).fetchall()
        results = []
        for row in rows:
            item = dict(row)
            item["source_types"] = [value for value in str(item.pop("source_types_csv") or "").split(",") if value]
            references = [value for value in str(item.pop("evidence_record_ids_csv") or "").split(",") if value]
            item["raw_data_references"] = references
            results.append(item)
        return results

    def update_candidate(self, target_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        unknown = set(changes) - TARGET_MUTABLE_FIELDS
        if unknown:
            raise ValueError(f"unsupported candidate fields: {', '.join(sorted(unknown))}")
        current = self.get_candidate(target_id)
        merged = {**current, **changes}
        normalized = normalize_candidate(merged, require_creator=False)
        now = utc_now()
        columns = list(normalized)
        with self.connect() as connection:
            cursor = connection.execute(
                f"UPDATE targets SET {', '.join(f'{column} = ?' for column in columns)}, updated_at = ? "
                "WHERE target_id = ? AND status = 'candidate'",
                [*(normalized[column] for column in columns), now, target_id],
            )
            if cursor.rowcount != 1:
                raise ValueError("target candidate not found")
        return self.get_candidate(target_id)

    def attach_evidence(self, target_id: str, evidence: Iterable[dict[str, Any]]) -> dict[str, Any]:
        normalized = [normalize_evidence(item) for item in evidence]
        if not normalized:
            raise ValueError("at least one evidence record is required")
        now = utc_now()
        try:
            with self.connect() as connection:
                exists = connection.execute(
                    "SELECT 1 FROM targets WHERE target_id = ? AND status = 'candidate'", (target_id,),
                ).fetchone()
                if not exists:
                    raise ValueError("target candidate not found")
                self._insert_evidence(connection, target_id, normalized, now)
                connection.execute("UPDATE targets SET updated_at = ? WHERE target_id = ?", (now, target_id))
        except sqlite3.IntegrityError as exc:
            raise ValueError("evidence record is already attached or violates the target-bank contract") from exc
        return self.get_candidate(target_id)

    def backup(self, retain: int = 5, protected_paths: Iterable[Path] = ()) -> Path:
        if retain < 1:
            raise ValueError("retain must be positive")
        self.initialize()
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self._apply_mode(self.backup_dir, 0o700)
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        destination = self.backup_dir / f"attack_targets-{stamp}-{uuid.uuid4().hex[:6]}.db"
        source = sqlite3.connect(self.db_path, timeout=15)
        target = sqlite3.connect(destination)
        try:
            source.backup(target)
        finally:
            target.close()
            source.close()
        self._apply_mode(destination, 0o600)
        protected = {path.resolve() for path in protected_paths}
        backups = sorted(self.backup_dir.glob("attack_targets-*.db"), key=lambda path: path.stat().st_mtime, reverse=True)
        while len(backups) > retain:
            expired = next((path for path in reversed(backups) if path.resolve() not in protected), None)
            if expired is None:
                break
            expired.unlink()
            backups.remove(expired)
        return destination

    def reset(self, *, confirm: bool) -> Path:
        if not confirm:
            raise ValueError("reset requires explicit confirmation")
        backup = self.backup()
        with self.connect() as connection:
            connection.execute("DELETE FROM targets")
        return backup

    def restore(self, source_backup: Path | str, *, confirm: bool) -> Path:
        if not confirm:
            raise ValueError("restore requires explicit confirmation")
        source_path = Path(source_backup).resolve()
        if not source_path.is_file():
            raise ValueError("restore source backup does not exist")
        safety_backup = self.backup(protected_paths=(source_path,))
        source = sqlite3.connect(f"file:{source_path.as_posix()}?mode=ro", uri=True, timeout=15)
        destination = sqlite3.connect(self.db_path, timeout=15)
        try:
            integrity = source.execute("PRAGMA integrity_check").fetchone()[0]
            if integrity != "ok":
                raise ValueError("restore source backup failed integrity check")
            source.backup(destination)
        finally:
            destination.close()
            source.close()
        self._apply_mode(self.db_path, 0o600)
        self.counts()
        return safety_backup

    def counts(self) -> dict[str, int]:
        self.initialize()
        with self.connect() as connection:
            targets = connection.execute("SELECT COUNT(*) FROM targets").fetchone()[0]
            evidence = connection.execute("SELECT COUNT(*) FROM target_evidence").fetchone()[0]
        return {"targets": targets, "evidence": evidence}
