"""Validated, revisioned artifacts embedded in workstream documents."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable


ARTIFACT_TYPE = "target_assessment_lead"
ARTIFACT_STATUSES = {"active", "ready_for_assessment", "rejected", "closed"}
INDICATION_ROLES = {"supports", "contradicts", "context"}
REVISION_ACTIONS = {
    "add_indication",
    "remove_indication",
    "update_annotation",
    "update_lead_statement",
    "request_completion",
    "send_to_assessment",
    "reject",
}


@dataclass
class ArtifactConflictError(Exception):
    current_revision: int

    def __str__(self) -> str:
        return "Artifact revision conflict"


def _text(value: Any, field: str, limit: int, required: bool = False) -> str:
    text = " ".join(str(value or "").split())[:limit]
    if required and not text:
        raise ValueError(f"Missing {field}")
    return text


def _text_list(value: Any, field: str, *, item_limit: int = 1000, max_items: int = 50) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"Invalid {field}")
    if any(not isinstance(item, str) for item in value[:max_items]):
        raise ValueError(f"Invalid {field}")
    return [_text(item, field, item_limit, required=True) for item in value[:max_items]]


def _actor(value: Any, workstream: dict, *, require_human: bool = False) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Invalid actor")
    participant_id = _text(value.get("participant_id"), "actor participant_id", 120, required=True)
    participant = next(
        (item for item in workstream.get("participants") or [] if item.get("participant_id") == participant_id),
        None,
    )
    if not participant:
        raise ValueError("Actor is not a workstream participant")
    kind = participant.get("kind")
    if require_human and kind != "human":
        raise ValueError("Action requires a human participant")
    return {"participant_id": participant_id, "kind": kind}


def _confirmation(value: Any) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Missing confirmation_turn")
    return {
        "message_id": _text(value.get("message_id"), "confirmation message_id", 160, required=True),
        "text": _text(value.get("text"), "confirmation text", 2000, required=True),
    }


def _subject(value: Any, resolve_target: Callable[[str], dict | None]) -> dict | None:
    if value in (None, ""):
        return None
    if not isinstance(value, dict) or value.get("kind") != "target":
        raise ValueError("Invalid subject_reference")
    target_id = _text(value.get("target_id"), "target_id", 160, required=True)
    target = resolve_target(target_id)
    if target is None:
        raise ValueError(f"Unknown target reference: {target_id}")
    return {
        "kind": "target",
        "target_id": target_id,
        "label": _text(target.get("title") or target_id, "target label", 240),
    }


def _indication(
    value: Any,
    *,
    workstream: dict,
    resolve_event: Callable[[str, str], dict | None],
    actor: dict,
    now: str,
    id_factory: Callable[[str], str],
) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Invalid indication")
    reference = value.get("source_reference")
    if not isinstance(reference, dict) or reference.get("kind") != "event_record":
        raise ValueError("Invalid indication source_reference")
    requested_layer_id = _text(reference.get("layer_id"), "layer_id", 240)
    record_id = _text(reference.get("record_id"), "record_id", 160, required=True)
    event = resolve_event(requested_layer_id, record_id)
    if event is None:
        raise ValueError(f"Unknown event reference: {record_id}")
    layer_id = _text(
        event.get("_canonical_layer_id") or requested_layer_id,
        "canonical layer_id",
        240,
        required=True,
    )
    role = _text(value.get("role") or "context", "indication role", 30)
    if role not in INDICATION_ROLES:
        raise ValueError("Invalid indication role")
    return {
        "indication_id": id_factory("indication"),
        "source_reference": {"kind": "event_record", "layer_id": layer_id, "record_id": record_id},
        "observed_claim": _text(event.get("text") or event.get("summary") or record_id, "observed_claim", 2000),
        "observed_at": _text(event.get("timestamp_utc") or event.get("timestamp"), "observed_at", 100),
        "provenance": {
            "source_type": _text(event.get("source_type"), "source_type", 160),
            "collection_family": _text(event.get("collection_family"), "collection_family", 160),
        },
        "relevance": _text(value.get("relevance"), "relevance", 1200),
        "role": role,
        "annotation": _text(value.get("annotation"), "annotation", 2000),
        "added_by": actor,
        "added_at_utc": now,
        "state": "active",
    }


def _initial_content(
    value: Any,
    *,
    workstream: dict,
    resolve_event: Callable[[str, str], dict | None],
    resolve_target: Callable[[str], dict | None],
    actor: dict,
    now: str,
    id_factory: Callable[[str], str],
) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Invalid artifact content")
    raw_indications = value.get("indications")
    if not isinstance(raw_indications, list) or not raw_indications:
        raise ValueError("At least one indication is required")
    if len(raw_indications) > 100:
        raise ValueError("Too many indications")
    indications = [
        _indication(
            item, workstream=workstream, resolve_event=resolve_event, actor=actor, now=now,
            id_factory=id_factory,
        )
        for item in raw_indications
    ]
    record_ids = [item["source_reference"]["record_id"] for item in indications]
    if len(record_ids) != len(set(record_ids)):
        raise ValueError("Duplicate indication record_id")
    return {
        "subject_reference": _subject(value.get("subject_reference"), resolve_target),
        "lead_statement": _text(value.get("lead_statement"), "lead_statement", 3000, required=True),
        "indications": indications,
        "supporting_signals": _text_list(value.get("supporting_signals"), "supporting_signals"),
        "contradictions": _text_list(value.get("contradictions"), "contradictions"),
        "assessment_questions": _text_list(value.get("assessment_questions"), "assessment_questions"),
        "gaps": _text_list(value.get("gaps"), "gaps"),
        "assigned_to": _text(value.get("assigned_to"), "assigned_to", 120),
        "annotation": _text(value.get("annotation"), "annotation", 3000),
    }


def list_artifacts(workstream: dict) -> list[dict]:
    return deepcopy(workstream.get("artifacts") or [])


def get_artifact(workstream: dict, artifact_id: str) -> dict | None:
    return next(
        (deepcopy(item) for item in workstream.get("artifacts") or [] if item.get("artifact_id") == artifact_id),
        None,
    )


def create_artifact(
    workstream: dict,
    request: dict,
    *,
    resolve_event: Callable[[str, str], dict | None],
    resolve_target: Callable[[str], dict | None],
    now: str,
    id_factory: Callable[[str], str],
    require_human_actor: bool = True,
) -> dict:
    if workstream.get("status") == "archived":
        raise ValueError("Archived workstream cannot be updated")
    artifact_type = _text(request.get("artifact_type"), "artifact_type", 80, required=True)
    if artifact_type != ARTIFACT_TYPE:
        raise ValueError("Unsupported artifact_type")
    for existing in workstream.get("artifacts") or []:
        if existing.get("artifact_type") == artifact_type and existing.get("status") not in {"closed", "rejected"}:
            raise ValueError("An active artifact of this type already exists")
    actor = _actor(request.get("actor"), workstream, require_human=require_human_actor)
    confirmation = _confirmation(request.get("confirmation_turn"))
    content = _initial_content(
        request.get("content"), workstream=workstream, resolve_event=resolve_event,
        resolve_target=resolve_target, actor=actor, now=now, id_factory=id_factory,
    )
    artifact_id = id_factory("artifact")
    artifact = {
        "schema_version": 1,
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "status": "active",
        "revision": 1,
        "content": content,
        "created_by": actor,
        "created_at_utc": now,
        "updated_at_utc": now,
        "revisions": [{
            "revision": 1,
            "prior_revision": 0,
            "actor": actor,
            "action": "create",
            "summary": f"Created with {len(content['indications'])} indication(s)",
            "confirmation_turn": confirmation,
            "created_at_utc": now,
        }],
    }
    workstream.setdefault("artifacts", []).append(artifact)
    workstream["updated_at_utc"] = now
    return deepcopy(artifact)


def revise_artifact(
    workstream: dict,
    artifact_id: str,
    request: dict,
    *,
    resolve_event: Callable[[str, str], dict | None],
    now: str,
    id_factory: Callable[[str], str],
    require_human_actor: bool = True,
) -> dict:
    if workstream.get("status") == "archived":
        raise ValueError("Archived workstream cannot be updated")
    artifacts = workstream.get("artifacts") or []
    artifact = next((item for item in artifacts if item.get("artifact_id") == artifact_id), None)
    if artifact is None:
        raise LookupError("Artifact not found")
    expected = request.get("expected_revision")
    if not isinstance(expected, int):
        raise ValueError("Missing expected_revision")
    current = int(artifact.get("revision") or 0)
    if expected != current:
        raise ArtifactConflictError(current)
    action = _text(request.get("action"), "action", 80, required=True)
    if action not in REVISION_ACTIONS:
        raise ValueError("Unsupported artifact action")
    actor = _actor(request.get("actor"), workstream, require_human=require_human_actor)
    confirmation = _confirmation(request.get("confirmation_turn"))
    payload = request.get("payload") if isinstance(request.get("payload"), dict) else {}
    content = artifact["content"]
    if artifact.get("status") in {"rejected", "closed"}:
        raise ValueError("Closed artifact cannot be revised")
    if artifact.get("status") == "ready_for_assessment" and action != "reject":
        raise ValueError("Artifact ready for assessment cannot be revised")
    summary = action
    if action == "add_indication":
        indication = _indication(
            payload.get("indication"), workstream=workstream, resolve_event=resolve_event,
            actor=actor, now=now, id_factory=id_factory,
        )
        record_id = indication["source_reference"]["record_id"]
        if any(
            item.get("source_reference", {}).get("record_id") == record_id
            for item in content.get("indications") or []
        ):
            raise ValueError("Duplicate indication record_id")
        content.setdefault("indications", []).append(indication)
        summary = f"Added indication {record_id}"
    elif action == "remove_indication":
        indication_id = _text(payload.get("indication_id"), "indication_id", 160, required=True)
        indication = next(
            (item for item in content.get("indications") or [] if item.get("indication_id") == indication_id),
            None,
        )
        if not indication or indication.get("state") != "active":
            raise ValueError("Active indication not found")
        active_count = sum(
            1 for item in content.get("indications") or [] if item.get("state") == "active"
        )
        if active_count <= 1:
            raise ValueError("Cannot remove the last active indication")
        indication["state"] = "removed"
        indication["removed_by"] = actor
        indication["removed_at_utc"] = now
        summary = f"Removed indication {indication_id}"
    elif action == "update_annotation":
        content["annotation"] = _text(payload.get("annotation"), "annotation", 3000)
        summary = "Updated annotation"
    elif action == "update_lead_statement":
        content["lead_statement"] = _text(
            payload.get("lead_statement"), "lead_statement", 3000, required=True
        )
        summary = "Updated lead statement"
    elif action == "request_completion":
        content["assessment_questions"] = _text_list(
            payload.get("assessment_questions"), "assessment_questions"
        )
        content["gaps"] = _text_list(payload.get("gaps"), "gaps")
        summary = "Updated assessment questions and gaps"
    elif action == "send_to_assessment":
        if not any(item.get("state") == "active" for item in content.get("indications") or []):
            raise ValueError("At least one active indication is required")
        artifact["status"] = "ready_for_assessment"
        summary = "Marked ready for assessment"
    elif action == "reject":
        artifact["status"] = "rejected"
        summary = "Rejected artifact"
    new_revision = current + 1
    artifact["revision"] = new_revision
    artifact["updated_at_utc"] = now
    artifact.setdefault("revisions", []).append({
        "revision": new_revision,
        "prior_revision": current,
        "actor": actor,
        "action": action,
        "summary": summary,
        "confirmation_turn": confirmation,
        "created_at_utc": now,
    })
    workstream["updated_at_utc"] = now
    return deepcopy(artifact)
