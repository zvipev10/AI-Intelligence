"""Deterministic, evaluator-isolated fusion helpers for Moshe target candidates."""

from __future__ import annotations

import re
from statistics import median
from typing import Any, Iterable


UAV_FAMILY = "airborne_isr_video_exploitation"
PERSISTABLE_CONFIDENCE = frozenset({"medium", "high"})


def _text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def _tokens(value: Any) -> set[str]:
    return set(re.findall(r"[\w\u0590-\u05ff]+", _text(value).casefold(), re.UNICODE))


def _similarity(first: dict[str, Any], second: dict[str, Any]) -> float:
    if any(_text(first.get(key)) != _text(second.get(key)) for key in ("location_id", "entity_id", "object_class")):
        return 0.0
    left, right = _tokens(first.get("event_summary")), _tokens(second.get("event_summary"))
    return len(left & right) / len(left | right) if left and right else 0.0


def group_independent_sources(events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Group visible records without using evaluator truth or scenario metadata."""
    rows = list(events)
    if not rows:
        raise ValueError("at least one event is required")
    parent = list(range(len(rows)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(first: int, second: int) -> None:
        left, right = find(first), find(second)
        if left != right:
            parent[max(left, right)] = min(left, right)

    for index, event in enumerate(rows):
        mission_id = _text(event.get("mission_id"))
        observation_id = _text(event.get("observation_id"))
        for other_index in range(index):
            other = rows[other_index]
            other_mission = _text(other.get("mission_id"))
            other_observation = _text(other.get("observation_id"))
            same_uav_mission = (
                _text(event.get("collection_family")) == UAV_FAMILY
                and _text(other.get("collection_family")) == UAV_FAMILY
                and mission_id and mission_id == other_mission
            )
            same_observation = observation_id and observation_id == other_observation
            visible_repost = _similarity(event, other) >= 0.65
            if same_uav_mission or same_observation or visible_repost:
                union(index, other_index)

    roots = sorted({find(index) for index in range(len(rows))})
    group_number = {root: position + 1 for position, root in enumerate(roots)}
    assignments = []
    for index, event in enumerate(rows):
        root = find(index)
        representative = rows[root]
        mission = _text(representative.get("mission_id"))
        observation = _text(representative.get("observation_id"))
        if _text(representative.get("collection_family")) == UAV_FAMILY and mission:
            source_group = f"uav-mission:{mission}"
            reason = "same UAV mission collapses to one source group"
        elif observation:
            source_group = f"observation:{observation}"
            reason = "same observation identifier collapses to one source group"
        else:
            source_group = f"visible-report:{group_number[root]:03d}"
            reason = "visible report or substantially matching repost cluster"
        assignments.append({
            "record_id": _text(event.get("event_id")),
            "source_group": source_group,
            "grouping_reason": reason,
        })
    count = len({item["source_group"] for item in assignments})
    return {
        "assignments": assignments,
        "independent_source_group_count": count,
        "independence_requirement_met": count >= 2,
    }


def build_evidence_snapshots(events: Iterable[dict[str, Any]], assignments: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    groups = {item["record_id"]: item["source_group"] for item in assignments}
    snapshots = []
    for event in events:
        record_id = _text(event.get("event_id"))
        count = event.get("estimated_object_count")
        snapshots.append({
            "record_id": record_id,
            "source_group": groups[record_id],
            "source_type": _text(event.get("source_type")),
            "observed_at": _text(event.get("timestamp_utc")),
            "location_id": _text(event.get("location_id")),
            "reported_object": _text(event.get("object_class")) or "unresolved",
            "reported_count": int(count) if str(count or "").isdigit() else None,
            "relevant_text": _text(event.get("event_summary")),
            "evidence_role": "supporting",
        })
    return snapshots


def reconcile_quantity(events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    counts = [int(item["estimated_object_count"]) for item in events if str(item.get("estimated_object_count") or "").isdigit()]
    if not counts:
        return {"count_min": None, "count_max": None, "count_estimate": None, "count_assessment": "unresolved"}
    low, high = min(counts), max(counts)
    estimate = int(median(counts) + 0.5)
    if len(counts) >= 2 and low == high:
        assessment = "exact"
    elif low != high:
        assessment = "range"
    else:
        assessment = "approximate"
    return {"count_min": low, "count_max": high, "count_estimate": estimate, "count_assessment": assessment}


def prepare_candidate(events: Iterable[dict[str, Any]], confidence: str) -> dict[str, Any]:
    rows = list(events)
    grouping = group_independent_sources(rows)
    normalized_confidence = _text(confidence).lower()
    reasons = []
    if not grouping["independence_requirement_met"]:
        reasons.append("fewer than two independent source groups")
    if normalized_confidence not in PERSISTABLE_CONFIDENCE:
        reasons.append("confidence is low or unsupported; report only")
    return {
        **grouping,
        "confidence": normalized_confidence,
        "persistence_eligible": not reasons,
        "persistence_block_reasons": reasons,
        "quantity": reconcile_quantity(rows),
        "evidence": build_evidence_snapshots(rows, grouping["assignments"]),
    }


def find_duplicate_candidates(
    candidates: Iterable[dict[str, Any]], event_ids: Iterable[str], *, object_class: str, location_id: str,
    entity_id: str | None = None,
) -> dict[str, Any]:
    evidence_ids = set(event_ids)
    matches = []
    for candidate in candidates:
        if candidate.get("object_class") != object_class or candidate.get("location_id") != location_id:
            continue
        if entity_id and candidate.get("entity_id") != entity_id:
            continue
        attached = {item.get("record_id") for item in candidate.get("evidence", [])}
        overlap = sorted(evidence_ids & attached)
        matches.append({
            "target_id": candidate.get("target_id"),
            "evidence_overlap": overlap,
            "match_type": "same-evidence" if overlap else "same-assessed-target",
        })
    return {"duplicate_found": bool(matches), "matches": matches}
