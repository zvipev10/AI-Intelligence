"""Generic timeframe-stage scenario manifests and persistent playback runs."""

from __future__ import annotations

import json
import re
import secrets
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


SCENARIO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")
RUN_ID_PATTERN = re.compile(r"^run_[A-Za-z0-9_.-]+$")
WORKSTREAM_ID_PATTERN = re.compile(r"^ws_[A-Za-z0-9_.-]+$")
INVESTIGATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")
IDEMPOTENCY_KEY_PATTERN = re.compile(r"^[A-Za-z0-9_.:-]+$")
RUN_STATUSES = {"active", "completed"}
MANIFEST_FIELDS = {"scenario_id", "version", "title", "playback_label", "scope", "stages"}
SCOPE_FIELDS = {"dataset", "layers"}
STAGE_FIELDS = {"id", "label", "from", "to"}
_STATE_LOCK = threading.RLock()


class PlaybackConflictError(ValueError):
    def __init__(self, message: str, current_revision: int):
        super().__init__(message)
        self.current_revision = current_revision


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def compact_text(value: Any, limit: int) -> str:
    return " ".join(str(value or "").split())[:limit]


def parse_utc(value: Any, field: str) -> datetime:
    text = compact_text(value, 80)
    if not text:
        raise ValueError(f"Missing {field}")
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"Invalid {field}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def canonical_utc(value: Any, field: str) -> str:
    return parse_utc(value, field).isoformat().replace("+00:00", "Z")


def normalize_scope(value: Any) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Invalid scenario scope")
    if set(value) - SCOPE_FIELDS:
        raise ValueError("Unsupported scenario scope field")
    dataset = compact_text(value.get("dataset"), 80)
    if not dataset:
        raise ValueError("Missing scenario dataset")
    layers = value.get("layers") or []
    if not isinstance(layers, list) or any(not isinstance(item, str) for item in layers):
        raise ValueError("Invalid scenario layers")
    normalized_layers = []
    for item in layers[:100]:
        layer = compact_text(item, 160)
        if layer and layer not in normalized_layers:
            normalized_layers.append(layer)
    return {"dataset": dataset, "layers": normalized_layers}


def normalize_stages(value: Any) -> list[dict]:
    if not isinstance(value, list) or not value:
        raise ValueError("Scenario requires at least one stage")
    if len(value) > 500:
        raise ValueError("Scenario has too many stages")
    stages: list[dict] = []
    seen: set[str] = set()
    previous_to: datetime | None = None
    for index, raw in enumerate(value, start=1):
        if not isinstance(raw, dict):
            raise ValueError("Invalid scenario stage")
        if set(raw) - STAGE_FIELDS:
            raise ValueError("Unsupported scenario stage field")
        stage_id = compact_text(raw.get("id"), 120)
        if not SCENARIO_ID_PATTERN.fullmatch(stage_id):
            raise ValueError("Invalid scenario stage id")
        if stage_id in seen:
            raise ValueError("Duplicate scenario stage id")
        start = parse_utc(raw.get("from"), f"stage {stage_id} from")
        end = parse_utc(raw.get("to"), f"stage {stage_id} to")
        if start >= end:
            raise ValueError("Scenario stage from must be before to")
        if previous_to is not None and start < previous_to:
            raise ValueError("Scenario stages must be ordered and non-overlapping")
        stages.append({
            "id": stage_id,
            "sequence": index,
            "label": compact_text(raw.get("label") or stage_id, 240),
            "from": start.isoformat().replace("+00:00", "Z"),
            "to": end.isoformat().replace("+00:00", "Z"),
        })
        previous_to = end
        seen.add(stage_id)
    return stages


def normalize_manifest(value: Any) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Invalid scenario manifest")
    if set(value) - MANIFEST_FIELDS:
        raise ValueError("Unsupported scenario manifest field")
    scenario_id = compact_text(value.get("scenario_id"), 120)
    if not SCENARIO_ID_PATTERN.fullmatch(scenario_id):
        raise ValueError("Invalid scenario id")
    version = value.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        raise ValueError("Invalid scenario version")
    title = compact_text(value.get("title"), 240)
    if not title:
        raise ValueError("Missing scenario title")
    return {
        "schema_version": 1,
        "scenario_id": scenario_id,
        "version": version,
        "title": title,
        "playback_label": compact_text(
            value.get("playback_label") or "Historical simulation", 160
        ),
        "scope": normalize_scope(value.get("scope")),
        "stages": normalize_stages(value.get("stages")),
    }


def load_manifests(directory: Path) -> list[dict]:
    if not directory.exists():
        return []
    manifests: list[dict] = []
    identities: set[tuple[str, int]] = set()
    for path in sorted(directory.glob("*.json")):
        try:
            manifest = normalize_manifest(json.loads(path.read_text(encoding="utf-8-sig")))
        except (OSError, json.JSONDecodeError, ValueError):
            continue
        identity = (manifest["scenario_id"], manifest["version"])
        if identity in identities:
            raise ValueError(f"Duplicate scenario manifest: {identity[0]} v{identity[1]}")
        identities.add(identity)
        manifests.append(manifest)
    return sorted(manifests, key=lambda item: (item["scenario_id"], -item["version"]))


def manifest_metadata(manifest: dict) -> dict:
    return {
        "scenario_id": manifest["scenario_id"],
        "version": manifest["version"],
        "title": manifest["title"],
        "playback_label": manifest["playback_label"],
        "scope": dict(manifest["scope"]),
        "stage_count": len(manifest["stages"]),
    }


def list_scenarios(directory: Path) -> list[dict]:
    return [manifest_metadata(item) for item in load_manifests(directory)]


def get_manifest(directory: Path, scenario_id: str, version: int | None = None) -> dict | None:
    if not SCENARIO_ID_PATTERN.fullmatch(str(scenario_id or "")):
        raise ValueError("Invalid scenario id")
    matches = [item for item in load_manifests(directory) if item["scenario_id"] == scenario_id]
    if version is not None:
        matches = [item for item in matches if item["version"] == version]
    return max(matches, key=lambda item: item["version"], default=None)


def scenario_details(manifest: dict) -> dict:
    """Expose configuration metadata without releasing future stage windows."""
    return manifest_metadata(manifest)


def run_path(directory: Path, run_id: str) -> Path:
    if not RUN_ID_PATTERN.fullmatch(run_id or ""):
        raise ValueError("Invalid scenario run id")
    path = (directory / f"{run_id}.json").resolve()
    if directory.resolve() not in path.parents:
        raise ValueError("Invalid scenario run path")
    return path


def write_run(directory: Path, payload: dict) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    path = run_path(directory, payload["run_id"])
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)
    return payload


def visibility_policy_path(runs_dir: Path) -> Path:
    return runs_dir / "active_visibility.json"


def playback_visibility_policy(payload: dict, mode: str = "real_time") -> dict:
    if mode not in {"historical", "real_time"}:
        raise ValueError("Invalid intelligence mode")
    active = mode == "real_time" and payload.get("status") == "active"
    return {
        "schema_version": 1,
        "mode": mode,
        "active": active,
        "run_id": payload.get("run_id") if active else None,
        "scenario_id": payload.get("scenario_id") if active else None,
        "scenario_version": payload.get("scenario_version") if active else None,
        "dataset": (payload.get("scope") or {}).get("dataset") if active else None,
        "layers": list((payload.get("scope") or {}).get("layers") or []) if active else [],
        "visible_timeframe": dict(payload.get("visible_timeframe") or {}) if active else None,
        "revision": payload.get("revision"),
        "updated_at_utc": utc_now_iso(),
    }


def write_playback_visibility(
    runs_dir: Path, payload: dict, mode: str = "real_time"
) -> dict:
    """Atomically publish the server-owned retrieval boundary for the active run."""
    runs_dir.mkdir(parents=True, exist_ok=True)
    policy = playback_visibility_policy(payload, mode)
    path = visibility_policy_path(runs_dir)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(policy, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)
    return policy


def write_historical_visibility(runs_dir: Path) -> dict:
    return write_playback_visibility(runs_dir, {"status": "inactive"}, "historical")


def load_playback_visibility(runs_dir: Path) -> dict | None:
    path = visibility_policy_path(runs_dir)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def load_run(directory: Path, run_id: str) -> dict | None:
    path = run_path(directory, run_id)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or payload.get("run_id") != run_id:
        return None
    return payload


def public_run(payload: dict) -> dict:
    return {key: value for key, value in payload.items() if not key.startswith("_")}


def visible_timeframe(manifest: dict, stage_index: int) -> dict:
    return {
        "from": manifest["stages"][0]["from"],
        "to": manifest["stages"][stage_index]["to"],
        "from_inclusive": True,
        "to_exclusive": True,
    }


def validate_start_request(request: Any) -> tuple[str, int | None, str | None, str, str]:
    if not isinstance(request, dict):
        raise ValueError("Invalid scenario run payload")
    scenario_id = compact_text(request.get("scenario_id"), 120)
    if not SCENARIO_ID_PATTERN.fullmatch(scenario_id):
        raise ValueError("Invalid scenario id")
    version = request.get("version")
    if version is not None and (
        not isinstance(version, int) or isinstance(version, bool) or version < 1
    ):
        raise ValueError("Invalid scenario version")
    workstream_id = compact_text(request.get("workstream_id"), 160) or None
    if workstream_id is not None and not WORKSTREAM_ID_PATTERN.fullmatch(workstream_id):
        raise ValueError("Invalid workstream id")
    investigation_id = compact_text(request.get("investigation_id"), 160)
    if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id):
        raise ValueError("Invalid investigation id")
    idempotency_key = normalize_idempotency_key(request.get("idempotency_key"))
    return scenario_id, version, workstream_id, investigation_id, idempotency_key


def normalize_idempotency_key(value: Any) -> str:
    key = compact_text(value, 160)
    if not IDEMPOTENCY_KEY_PATTERN.fullmatch(key):
        raise ValueError("Invalid idempotency key")
    return key


def find_existing_run(
    directory: Path,
    scenario_id: str,
    version: int,
    workstream_id: str | None,
    investigation_id: str,
) -> dict | None:
    if not directory.exists():
        return None
    matches: list[dict] = []
    for path in directory.glob("run_*.json"):
        payload = load_run(directory, path.stem)
        if (
            payload
            and payload.get("scenario_id") == scenario_id
            and payload.get("scenario_version") == version
            and (
                payload.get("workstream_id") == workstream_id
                if workstream_id
                else not payload.get("workstream_id")
                and payload.get("investigation_id") == investigation_id
            )
        ):
            matches.append(payload)
    return max(matches, key=lambda item: str(item.get("updated_at_utc") or ""), default=None)


def find_workstream_run(directory: Path, workstream_id: str) -> dict | None:
    if not WORKSTREAM_ID_PATTERN.fullmatch(workstream_id or "") or not directory.exists():
        return None
    matches = []
    for path in directory.glob("run_*.json"):
        payload = load_run(directory, path.stem)
        if payload and payload.get("workstream_id") == workstream_id:
            matches.append(payload)
    return max(matches, key=lambda item: str(item.get("updated_at_utc") or ""), default=None)


def find_investigation_run(directory: Path, investigation_id: str) -> dict | None:
    if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id or "") or not directory.exists():
        return None
    matches = []
    for path in directory.glob("run_*.json"):
        payload = load_run(directory, path.stem)
        if (
            payload
            and payload.get("investigation_id") == investigation_id
            and not payload.get("workstream_id")
        ):
            matches.append(payload)
    return max(matches, key=lambda item: str(item.get("updated_at_utc") or ""), default=None)


def find_active_run(directory: Path) -> dict | None:
    if not directory.exists():
        return None
    active = []
    for path in directory.glob("run_*.json"):
        payload = load_run(directory, path.stem)
        if payload and payload.get("status") == "active":
            active.append(payload)
    return max(active, key=lambda item: str(item.get("updated_at_utc") or ""), default=None)


def run_with_next_stage(manifests_dir: Path, payload: dict) -> dict:
    result = public_run(payload)
    manifest = get_manifest(
        manifests_dir, payload.get("scenario_id") or "", payload.get("scenario_version")
    )
    next_index = int(payload.get("current_stage_index") or 0) + 1
    next_stage = None
    if (
        payload.get("status") == "active"
        and manifest is not None
        and next_index < len(manifest["stages"])
    ):
        stage = manifest["stages"][next_index]
        next_stage = {
            "sequence": stage["sequence"],
            "timeframe": {
                "from": stage["from"],
                "to": stage["to"],
                "from_inclusive": True,
                "to_exclusive": True,
            },
        }
    result["next_stage"] = next_stage
    return result


def claim_reevaluation(directory: Path, run_id: str, revision: int) -> tuple[dict | None, bool]:
    """Claim one Moshe reevaluation per released run revision."""
    with _STATE_LOCK:
        payload = load_run(directory, run_id)
        if payload is None:
            return None, False
        claims = payload.setdefault("_reevaluations", {})
        key = str(revision)
        existing = claims.get(key)
        if isinstance(existing, dict):
            return public_run(payload), False
        claims[key] = {"status": "running", "started_at_utc": utc_now_iso()}
        write_run(directory, payload)
        return public_run(payload), True


def finish_reevaluation(
    directory: Path, run_id: str, revision: int, status: str, error: str | None = None
) -> dict | None:
    if status not in {"completed", "failed"}:
        raise ValueError("Invalid reevaluation status")
    with _STATE_LOCK:
        payload = load_run(directory, run_id)
        if payload is None:
            return None
        claims = payload.setdefault("_reevaluations", {})
        claim = claims.setdefault(str(revision), {})
        claim.update({
            "status": status,
            "completed_at_utc": utc_now_iso(),
            "error": compact_text(error, 500) if error else None,
        })
        write_run(directory, payload)
        return public_run(payload)


def start_run(
    manifests_dir: Path,
    runs_dir: Path,
    request: Any,
    workstream_validator: Callable[[str, str], bool],
) -> tuple[dict, bool]:
    scenario_id, version, workstream_id, investigation_id, key = validate_start_request(request)
    manifest = get_manifest(manifests_dir, scenario_id, version)
    if manifest is None:
        raise LookupError("Scenario not found")
    if workstream_id and not workstream_validator(workstream_id, investigation_id):
        raise LookupError("Workstream not found for investigation")
    with _STATE_LOCK:
        existing = find_existing_run(
            runs_dir, scenario_id, manifest["version"], workstream_id, investigation_id
        )
        if existing is not None:
            return public_run(existing), False
        active = find_active_run(runs_dir)
        if active is not None:
            raise PlaybackConflictError(
                "Another scenario run is already active",
                int(active.get("revision") or 1),
            )
        now = utc_now_iso()
        first_stage = manifest["stages"][0]
        run_id = (
            f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_"
            f"{secrets.token_hex(4)}"
        )
        payload = {
            "schema_version": 1,
            "run_id": run_id,
            "scenario_id": scenario_id,
            "scenario_version": manifest["version"],
            "scenario_title": manifest["title"],
            "playback_label": manifest["playback_label"],
            "scope": dict(manifest["scope"]),
            "workstream_id": workstream_id,
            "investigation_id": investigation_id,
            "status": "active",
            "current_stage_index": 0,
            "current_stage": dict(first_stage),
            "stage_count": len(manifest["stages"]),
            "visible_timeframe": visible_timeframe(manifest, 0),
            "revision": 1,
            "transition_history": [{
                "action": "start",
                "from_stage_id": None,
                "to_stage_id": first_stage["id"],
                "revision": 1,
                "idempotency_key": key,
                "created_at_utc": now,
            }],
            "created_at_utc": now,
            "updated_at_utc": now,
            "completed_at_utc": None,
            "_idempotency": {},
            "_reevaluations": {},
        }
        write_run(runs_dir, payload)
        return public_run(payload), True


def validate_transition_request(request: Any) -> tuple[int, str]:
    if not isinstance(request, dict):
        raise ValueError("Invalid scenario transition payload")
    revision = request.get("expected_revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise ValueError("Invalid expected revision")
    return revision, normalize_idempotency_key(request.get("idempotency_key"))


def transition_run(
    manifests_dir: Path,
    runs_dir: Path,
    run_id: str,
    request: Any,
    action: str,
) -> tuple[dict | None, bool]:
    expected_revision, key = validate_transition_request(request)
    if action not in {"advance", "complete", "reset"}:
        raise ValueError("Invalid scenario transition")
    with _STATE_LOCK:
        payload = load_run(runs_dir, run_id)
        if payload is None:
            return None, False
        if action == "reset":
            active = find_active_run(runs_dir)
            if active is not None and active.get("run_id") != run_id:
                raise PlaybackConflictError(
                    "Another scenario run is already active",
                    int(active.get("revision") or 1),
                )
        replay = (payload.get("_idempotency") or {}).get(key)
        if isinstance(replay, dict):
            if replay.get("action") != action:
                raise ValueError("Idempotency key is already bound to another action")
            stored_response = replay.get("response")
            if isinstance(stored_response, dict):
                return stored_response, True
        current_revision = int(payload.get("revision") or 0)
        if expected_revision != current_revision:
            raise PlaybackConflictError("Scenario run revision conflict", current_revision)
        manifest = get_manifest(
            manifests_dir, payload["scenario_id"], payload["scenario_version"]
        )
        if manifest is None:
            raise LookupError("Scenario manifest is unavailable")
        if payload.get("status") not in RUN_STATUSES:
            raise ValueError("Invalid scenario run status")
        now = utc_now_iso()
        previous_stage_id = (payload.get("current_stage") or {}).get("id")
        if action == "advance":
            if payload["status"] != "active":
                raise ValueError("Completed scenario run cannot advance")
            next_index = int(payload["current_stage_index"]) + 1
            if next_index >= len(manifest["stages"]):
                raise ValueError("Scenario run is already at the final stage")
            next_stage = manifest["stages"][next_index]
            payload.update({
                "current_stage_index": next_index,
                "current_stage": dict(next_stage),
                "visible_timeframe": visible_timeframe(manifest, next_index),
            })
            next_stage_id = next_stage["id"]
        elif action == "complete":
            if payload["status"] != "active":
                raise ValueError("Scenario run is already completed")
            payload["status"] = "completed"
            payload["completed_at_utc"] = now
            next_stage_id = previous_stage_id
        else:
            first_stage = manifest["stages"][0]
            payload.update({
                "status": "active",
                "current_stage_index": 0,
                "current_stage": dict(first_stage),
                "visible_timeframe": visible_timeframe(manifest, 0),
                "completed_at_utc": None,
            })
            next_stage_id = first_stage["id"]
        payload["revision"] = current_revision + 1
        payload["updated_at_utc"] = now
        payload.setdefault("transition_history", []).append({
            "action": action,
            "from_stage_id": previous_stage_id,
            "to_stage_id": next_stage_id,
            "revision": payload["revision"],
            "idempotency_key": key,
            "created_at_utc": now,
        })
        response = public_run(payload)
        payload.setdefault("_idempotency", {})[key] = {
            "action": action,
            "response": response,
        }
        write_run(runs_dir, payload)
        return response, False
