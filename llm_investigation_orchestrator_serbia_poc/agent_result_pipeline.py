"""Shared result contracts for every conversational agent."""

from __future__ import annotations

from typing import Any


DEFAULT_AGENT_ID = "general"
SUPPORTED_LAYER_KINDS = frozenset({"events", "map_locations", "aggregate_groups", "locations", "entities", "attack_targets"})
TARGET_RESULT_TOOLS = frozenset({
    "search_target_candidates", "get_target_candidate", "create_target_candidate",
    "update_target_candidate", "attach_target_evidence",
})


def normalize_location_item(item: Any, default_count: int = 0) -> dict[str, Any] | None:
    if not isinstance(item, dict):
        return None
    location_id = item.get("location_id") or item.get("key")
    location_name = item.get("location_name") or item.get("name") or item.get("label")
    if not location_id and not location_name:
        return None
    return {
        "location_id": location_id,
        "location_name": location_name or location_id,
        "latitude": item.get("latitude"),
        "longitude": item.get("longitude"),
        "municipality": item.get("municipality"),
        "count": item.get("count", default_count),
    }


def normalize_map_locations(tool: str, result: dict[str, Any]) -> list[dict[str, Any]]:
    locations = []
    for item in result.get("map_locations") or []:
        normalized = normalize_location_item(item)
        if normalized:
            locations.append(normalized)
    for item in result.get("locations") or []:
        normalized = normalize_location_item(item, default_count=1)
        if normalized:
            locations.append(normalized)
    if tool == "aggregate_events" and result.get("group_by") in {"location", "municipality"}:
        for item in result.get("groups") or []:
            normalized = normalize_location_item(item)
            if normalized:
                locations.append(normalized)
    for item in result.get("route") or []:
        normalized = normalize_location_item(item)
        if normalized:
            locations.append(normalized)
    for group in result.get("conflict_groups") or []:
        for item in group.get("locations") or []:
            normalized = normalize_location_item(item)
            if normalized:
                locations.append(normalized)

    deduped = {}
    for item in locations:
        key = item.get("location_id") or item.get("location_name")
        if key:
            existing = deduped.get(key)
            if not existing or int(item.get("count") or 0) > int(existing.get("count") or 0):
                deduped[key] = item
    return list(deduped.values())


def normalize_aggregate_groups(result: dict[str, Any]) -> list[dict[str, Any]]:
    groups = []
    group_by = result.get("group_by")
    for item in result.get("groups") or []:
        if not isinstance(item, dict):
            continue
        key = item.get("key") or item.get("label")
        label = item.get("label") or item.get("key")
        if key is None and label is None:
            continue
        groups.append({
            "key": key,
            "label": label,
            "count": item.get("count", 0),
            "group_by": group_by,
            "first_event_id": item.get("first_event_id"),
            "first_event_time": item.get("first_event_time"),
            "last_event_id": item.get("last_event_id"),
            "last_event_time": item.get("last_event_time"),
        })
    return groups


def normalize_location_layers(result: dict[str, Any]) -> list[dict[str, Any]]:
    layers = []
    for item in result.get("location_layers") or []:
        if not isinstance(item, dict) or not item.get("location_id"):
            continue
        location_id = item["location_id"]
        layers.append({
            "location_id": location_id,
            "location_name": item.get("location_name") or item.get("name") or location_id,
            "name": item.get("name") or item.get("location_name") or location_id,
            "type": item.get("type"),
            "country": item.get("country"),
            "region": item.get("region"),
            "municipality": item.get("municipality"),
            "locality": item.get("locality"),
            "precision": item.get("precision"),
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "event_count": item.get("event_count", item.get("count", 0)),
            "top_entities": item.get("top_entities") or [],
            "top_sources": item.get("top_sources") or [],
            "certainty_breakdown": item.get("certainty_breakdown") or {},
            "reliability_breakdown": item.get("reliability_breakdown") or {},
        })
    return layers


def normalize_entity_layers(result: dict[str, Any]) -> list[dict[str, Any]]:
    layers = []
    for item in result.get("entity_layers") or []:
        if not isinstance(item, dict) or not item.get("entity_id"):
            continue
        entity_id = item["entity_id"]
        layers.append({
            "entity_id": entity_id,
            "canonical_name": item.get("canonical_name") or entity_id,
            "entity_type": item.get("entity_type"),
            "confidence": item.get("confidence"),
            "basis": item.get("basis"),
            "aliases": item.get("aliases") or [],
            "event_count": item.get("event_count", item.get("count", 0)),
            "top_locations": item.get("top_locations") or [],
            "top_sources": item.get("top_sources") or [],
            "certainty_breakdown": item.get("certainty_breakdown") or {},
            "reliability_breakdown": item.get("reliability_breakdown") or {},
        })
    return layers


def normalize_typed_layers(value: Any) -> list[dict[str, Any]]:
    """Validate generic layer envelopes without interpreting agent-specific data."""
    layers = []
    for item in value or []:
        if not isinstance(item, dict):
            continue
        kind = str(item.get("kind") or "").strip()
        rows = item.get("rows")
        if kind not in SUPPORTED_LAYER_KINDS or not isinstance(rows, list):
            continue
        layer = dict(item)
        layer["kind"] = kind
        layer["rows"] = rows
        layers.append(layer)
    return layers


def normalize_attack_targets(
    audit_records: Any,
    *,
    locations: dict[str, dict[str, Any]] | None = None,
    entities: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build presentation-ready target rows from successful target-tool results."""
    locations = locations or {}
    entities = entities or {}
    by_id: dict[str, dict[str, Any]] = {}
    for record in audit_records or []:
        if not isinstance(record, dict) or record.get("is_error") or record.get("tool") not in TARGET_RESULT_TOOLS:
            continue
        result = record.get("result") or {}
        if not isinstance(result, dict):
            continue
        candidates = result.get("candidates") or []
        if not isinstance(candidates, list):
            candidates = []
        if isinstance(result.get("candidate"), dict):
            candidates = [*candidates, result["candidate"]]
        for candidate in candidates:
            if not isinstance(candidate, dict) or not candidate.get("target_id"):
                continue
            target_id = str(candidate["target_id"])
            previous = by_id.get(target_id, {})
            merged = {**previous, **candidate}
            if previous.get("evidence") and not candidate.get("evidence"):
                merged["evidence"] = previous["evidence"]
            location_id = str(merged.get("location_id") or "")
            entity_id = str(merged.get("entity_id") or "")
            location = locations.get(location_id, {})
            entity = entities.get(entity_id, {})
            evidence = merged.get("evidence") if isinstance(merged.get("evidence"), list) else []
            raw_references = merged.get("raw_data_references") if isinstance(merged.get("raw_data_references"), list) else []
            raw_references = list(dict.fromkeys([*raw_references, *(item.get("record_id") for item in evidence if isinstance(item, dict) and item.get("record_id"))]))
            source_types = merged.get("source_types") if isinstance(merged.get("source_types"), list) else []
            source_types = list(dict.fromkeys([*source_types, *(item.get("source_type") for item in evidence if isinstance(item, dict) and item.get("source_type"))]))
            merged.update({
                "location_name": location.get("name") or merged.get("location_name") or location_id,
                "latitude": location.get("latitude", merged.get("latitude")),
                "longitude": location.get("longitude", merged.get("longitude")),
                "entity_name": entity.get("canonical_name") or merged.get("entity_name") or entity_id or None,
                "evidence": evidence,
                "raw_data_references": raw_references,
                "source_types": source_types,
                "evidence_count": merged.get("evidence_count", len(evidence)),
                "source_group_count": merged.get("source_group_count", len({item.get("source_group") for item in evidence if isinstance(item, dict) and item.get("source_group")})),
            })
            by_id[target_id] = merged
    return list(by_id.values())


def build_agent_result(
    payload: dict[str, Any],
    *,
    responding_agent: str = DEFAULT_AGENT_ID,
    session_id: str | None = None,
    mission_run_id: str | None = None,
    layers: Any = None,
) -> dict[str, Any]:
    """Add the shared agent envelope while retaining the legacy result shape."""
    result = dict(payload)
    result["responding_agent"] = str(responding_agent or DEFAULT_AGENT_ID)
    result["session_id"] = session_id or result.get("session_id") or result.get("run_id")
    normalized_layers = normalize_typed_layers(layers if layers is not None else result.get("layers"))
    if normalized_layers:
        result["layers"] = normalized_layers
    elif "layers" in result:
        result["layers"] = []
    if mission_run_id:
        result["mission_run_id"] = mission_run_id
    else:
        result.pop("mission_run_id", None)
    return result
