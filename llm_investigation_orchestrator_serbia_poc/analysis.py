"""Pure functions over UI rows: layers, entity and location summaries, links, saved-item payloads.

Nothing here does I/O. Rows come from ``hl.items`` (i360 items mapped to the old CSV shape),
entities and locations from i360 entity records, reviews from ``hl.state``. The logic is
carried over from the former file-based ``server.py`` with the file reading removed.
"""
from __future__ import annotations

import math
import re
import secrets
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any

from catalog_filters import filter_rows, validate_filters
from link_graph import build_links, derive_subscriber_identity

INVESTIGATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")


def normalize_locale(value: Any) -> str:
    locale = str(value or "").strip().lower()
    return locale if locale in {"he", "en"} else "he"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def compact_text(value: Any, limit: int) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def new_item_id(prefix: str) -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{secrets.token_hex(3)}"


# --------------------------------------------------------------------------------------
# Dataset assembly
# --------------------------------------------------------------------------------------
def entity_db(entities: list[dict[str, Any]], reviews: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    approvals = approved_identities(reviews)
    result = {}
    for item in entities:
        if not item.get("entity_id"):
            continue
        copied = dict(item)
        telecom = copied.get("telecom") if isinstance(copied.get("telecom"), dict) else {}
        copied["telecom"] = {k: v for k, v in telecom.items() if k != "extracted_subscriber_identity"}
        result[str(copied["entity_id"])] = apply_entity_telecom_approval(copied, approvals.get(str(copied["entity_id"]), {}))
    return result


def approved_identities(reviews: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    approved = {}
    for review in reviews.values():
        if review.get("review_state") != "approved":
            continue
        entity_id = str((review.get("subject") or {}).get("object_id") or review.get("entity_id") or "")
        value = (review.get("claim") or {}).get("value") or review
        if entity_id and isinstance(value, dict):
            approved[entity_id] = {
                "msisdn": value.get("msisdn"), "imsi": value.get("imsi"),
                "method": review.get("rule_id") or review.get("method"),
                "supporting_record_ids": review.get("supporting_record_ids") or [],
                "approved_at_utc": review.get("reviewed_at_utc") or review.get("approved_at_utc"),
                "source": "analyst_derivation_review",
            }
    return approved


def apply_entity_telecom_approval(entity: dict[str, Any], approval: dict[str, Any]) -> dict[str, Any]:
    telecom = entity.get("telecom") if isinstance(entity.get("telecom"), dict) else {}
    if not telecom:
        return entity
    approved_identity = {
        key: approval[key] for key in ("msisdn", "imsi", "method", "supporting_record_ids", "approved_at_utc", "source")
        if approval.get(key) not in (None, "", [])
    }
    if not approved_identity.get("msisdn") and not approved_identity.get("imsi"):
        return entity
    resolved = {**telecom, "approved_subscriber_identity": approved_identity}
    resolved.update({key: approved_identity[key] for key in ("msisdn", "imsi") if approved_identity.get(key)})
    resolved.pop("extracted_subscriber_identity", None)
    return {**entity, "telecom": resolved}


def apply_graph_entity_links(events: list[dict[str, Any]], entities: dict[str, dict[str, Any]],
                             locations: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Project field-backed links onto rows for the viewers; returns the links."""
    links = build_links(events, entities, locations)
    by_id = {str(e.get("event_id")): e for e in events if e.get("event_id")}
    for link in links:
        start, end = link.get("from") or {}, link.get("to") or {}
        record_id = str(start.get("object_id") or "")
        target_id = str(end.get("object_id") or "")
        if start.get("object_type") == "raw_record" and end.get("object_type") == "raw_record":
            for current_id, linked_id, current_field, linked_field in (
                (record_id, target_id, start.get("field"), end.get("field")),
                (target_id, record_id, end.get("field"), start.get("field")),
            ):
                current = by_id.get(current_id)
                if current is not None:
                    current.setdefault("observed_record_links", []).append({
                        "link_id": link.get("link_id"), "record_id": linked_id, "rule_id": link.get("rule_id"),
                        "record_field": current_field, "linked_record_field": linked_field,
                        "matched_value": link.get("matched_value"),
                    })
            continue
        event = by_id.get(record_id)
        if event is None or end.get("object_type") != "entity":
            continue
        event.setdefault("related_entity_ids", []).append(target_id)
        entity = entities.get(target_id, {})
        event.setdefault("observed_entity_links", []).append({
            "link_id": link.get("link_id"), "entity_id": target_id,
            "entity_name": entity.get("canonical_name", target_id), "entity_type": entity.get("entity_type", ""),
            "rule_id": link.get("rule_id"), "record_field": start.get("field"), "entity_field": end.get("field"),
            "matched_value": link.get("matched_value"),
        })
        if start.get("field") == "side_a_imei":
            event["side_a_entity_id"] = target_id
            event["side_a_entity_name"] = entity.get("canonical_name", target_id)
    for event in events:
        if isinstance(event.get("related_entity_ids"), list):
            event["related_entity_ids"] = list(dict.fromkeys(event["related_entity_ids"]))
        for key, fields in (("observed_entity_links", ("link_id", "rule_id", "entity_id", "record_field")),
                            ("observed_record_links", ("link_id", "record_id"))):
            if isinstance(event.get(key), list):
                seen: set = set()
                unique = []
                for item in event[key]:
                    marker = tuple(item.get(f) for f in fields)
                    if marker not in seen:
                        seen.add(marker)
                        unique.append(item)
                event[key] = unique
    return links


def enrich_rows(rows: list[dict[str, Any]], locations: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    for event in rows:
        location = locations.get(event.get("location_id") or "", {})
        event["location_name"] = location.get("name", event.get("location_id") or "")
        event["location_type"] = location.get("type", event.get("location_type", ""))
        if not event.get("latitude") and location.get("latitude") is not None:
            event["latitude"] = str(location.get("latitude"))
            event["longitude"] = str(location.get("longitude"))
        for side in ("a", "b"):
            side_location_id = event.get(f"side_{side}_location_id") or ""
            event[f"side_{side}_location_name"] = locations.get(side_location_id, {}).get("name", side_location_id)
    return sorted(rows, key=lambda item: str(item.get("timestamp_utc") or ""))


class Dataset:
    """Everything one user may see, assembled once per snapshot."""

    def __init__(self, rows: list[dict[str, Any]], entities: list[dict[str, Any]],
                 locations: dict[str, dict[str, Any]], reviews: dict[str, dict[str, Any]], locale: str):
        self.locale = normalize_locale(locale)
        self.locations = locations
        self.entities = entity_db(entities, reviews)
        self.events = enrich_rows([dict(row) for row in rows], locations)
        self.links = apply_graph_entity_links(self.events, self.entities, self.locations)
        self.entity_layers = build_entity_layers(self.events, self.entities, self.locations, self.links)
        self.location_layers = build_location_layers(self.events, self.entity_layers, self.locations)
        for event in self.events:
            entity = self.entity_layers.get(event.get("entity_id") or "", {})
            event["entity_name"] = entity.get("canonical_name") or event.get("entity_id") or ""


# --------------------------------------------------------------------------------------
# Entity and location summaries
# --------------------------------------------------------------------------------------
ENTITY_PROFILE_FIELDS = (
    "description", "image_url", "identity_status", "given_name", "family_name", "gender",
    "age_years", "date_of_birth", "role", "occupation", "affiliations",
    "nationality", "ethnicity", "languages", "residence", "place_of_birth",
    "previous_residences", "connections", "military_service", "associated_entity_ids",
    "identifiers", "telecom", "biographical_notes",
)

PRESENCE_CLAIM_TERMS = (
    "נוכחות", "תנועה", "פעילות", "היערכות", "פריסה", "תגבור",
    "presence", "movement", "activity", "deployment", "operating", "reinforcement",
)


def event_supports_presence(event: dict[str, Any]) -> bool:
    summary = str(event.get("event_summary") or "").casefold()
    return bool(event.get("location_id")) and any(term in summary for term in PRESENCE_CLAIM_TERMS)


def build_entity_layers(events, entities, locations, links) -> dict[str, dict[str, Any]]:
    presentations: dict[str, dict[str, Any]] = {}
    for entity_id, base in sorted(entities.items()):
        entity_events = [e for e in events if e.get("entity_id") == entity_id or entity_id in (e.get("related_entity_ids") or [])]
        top_locations = []
        for location_id, count in Counter(e.get("location_id") for e in entity_events if e.get("location_id")).most_common(12):
            location = locations.get(location_id, {})
            location_events = [e for e in entity_events if e.get("location_id") == location_id]
            presence = [e for e in location_events if event_supports_presence(e)]
            high = any(
                str(e.get("certainty_level") or "").casefold() in {"גבוהה", "high"}
                or str(e.get("source_reliability_label") or "").casefold() == "confirmed"
                for e in presence
            )
            top_locations.append({
                "location_id": location_id, "location_name": location.get("name", location_id),
                "municipality": location.get("municipality"), "latitude": location.get("latitude"),
                "longitude": location.get("longitude"), "count": count,
                "presence_claim": bool(presence), "presence_evidence_count": len(presence),
                "assessment_status": "assessed" if high or len(presence) > 1 else "reported",
                "confidence": "high" if high else ("medium" if len(presence) > 1 else "low"),
                "latest_timestamp_utc": max((str(e.get("timestamp_utc") or "") for e in presence), default=""),
                "evidence_record_ids": [e.get("record_id") or e.get("event_id") for e in presence[:25]],
            })
        presentation = {
            "entity_id": entity_id,
            "canonical_name": base.get("canonical_name") or entity_id,
            "entity_type": base.get("entity_type") or "גורם מדווח",
            "confidence": base.get("confidence") or "entity_id גלוי ברשומה",
            "basis": base.get("basis") or "ישות i360",
            "aliases": list(dict.fromkeys([base.get("canonical_name") or entity_id, *(base.get("aliases") or [])])),
            "event_count": len(entity_events),
            "top_locations": top_locations,
            "top_sources": [{"source_type": k, "count": c} for k, c in Counter(e.get("source_type") or "לא ידוע" for e in entity_events).most_common(10)],
            "certainty_breakdown": dict(Counter(e.get("certainty_level") or "לא ידוע" for e in entity_events)),
            "reliability_breakdown": dict(Counter(e.get("source_reliability_label") or e.get("source_reliability") or "לא ידוע" for e in entity_events)),
        }
        presentation.update({f: base[f] for f in ENTITY_PROFILE_FIELDS if base.get(f) not in (None, "", [], {})})
        derivation = derive_subscriber_identity(events, links, entity_id)
        if derivation and not (presentation.get("telecom") or {}).get("approved_subscriber_identity"):
            presentation["telecom"] = {**(presentation.get("telecom") or {}), "subscriber_identity_derivation": derivation}
        presentations[entity_id] = presentation
    return presentations


def build_location_layers(events, entity_presentations, locations) -> dict[str, dict[str, Any]]:
    presentations: dict[str, dict[str, Any]] = {}
    by_location: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        if event.get("location_id"):
            by_location[event["location_id"]].append(event)
    for location_id, location in locations.items():
        location_events = by_location.get(location_id, [])
        presentations[location_id] = {
            "location_id": location_id,
            "location_name": location.get("name", location_id),
            "name": location.get("name", location_id),
            **{k: location.get(k) for k in ("type", "country", "region", "municipality", "locality", "precision", "latitude", "longitude")},
            "event_count": len(location_events),
            "top_entities": [
                {"entity_id": eid, "name": entity_presentations.get(eid, {}).get("canonical_name", eid), "count": c}
                for eid, c in Counter(e.get("entity_id") for e in location_events if e.get("entity_id")).most_common(10)
            ],
            "top_sources": [{"source_type": k, "count": c} for k, c in Counter(e.get("source_type") or "לא ידוע" for e in location_events).most_common(10)],
            "certainty_breakdown": dict(Counter(e.get("certainty_level") or "לא ידוע" for e in location_events)),
            "reliability_breakdown": dict(Counter(e.get("source_reliability_label") or e.get("source_reliability") or "לא ידוע" for e in location_events)),
        }
    return presentations


# --------------------------------------------------------------------------------------
# Layer catalog
# --------------------------------------------------------------------------------------
def list_layers(data: Dataset, known_sources: list[str] | None = None) -> list[dict[str, Any]]:
    en = data.locale == "en"
    unknown_source = "Unknown source" if en else "מקור לא ידוע"
    layers = [
        {"id": "entity-metadata:all", "label": "Entity layer" if en else "שכבת ישויות", "family": "entities",
         "kind": "entity_metadata", "count": len(data.entity_layers),
         "capabilities": {"table": True, "map": True, "timeline": False}},
        {"id": "location-metadata:all", "label": "Location layer" if en else "שכבת מיקומים", "family": "locations",
         "kind": "location_metadata", "count": len(data.location_layers),
         "capabilities": {"table": True, "map": True, "timeline": False}},
    ]
    counts = Counter(e.get("source_type") or unknown_source for e in data.events)
    for source in known_sources or []:
        counts.setdefault(source, 0)
    for source_type, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        rows = [e for e in data.events if (e.get("source_type") or unknown_source) == source_type]
        layers.append({
            "id": f"events:{source_type}", "label": source_type, "family": "events", "kind": "events",
            "source_type": source_type, "count": count,
            "capabilities": {"table": True, "timeline": True,
                             "map": not count or any(e.get("location_id") in data.locations or e.get("latitude") for e in rows)},
        })
    return layers


def layer_rows(data: Dataset, layer_id: str, filters=None, known_sources: list[str] | None = None):
    layers = {layer["id"]: layer for layer in list_layers(data, known_sources)}
    layer = layers.get(layer_id)
    if not layer:
        return None
    if layer_id == "entity-metadata:all":
        rows = sorted(data.entity_layers.values(), key=lambda i: (-int(i.get("event_count") or 0), str(i.get("canonical_name") or "")))
    elif layer_id == "location-metadata:all":
        rows = sorted(data.location_layers.values(), key=lambda i: (-int(i.get("event_count") or 0), str(i.get("location_name") or "")))
    else:
        unknown_source = "Unknown source" if data.locale == "en" else "מקור לא ידוע"
        source_type = layer.get("source_type")
        rows = [e for e in data.events if (e.get("source_type") or unknown_source) == source_type]
    scope = validate_filters(filters)
    if scope:
        if layer.get("kind") != "events":
            raise ValueError("catalog filters are supported only for raw event layers")
        rows = filter_rows(rows, scope)
        layer = {**layer, "count": len(rows), "catalog_filters": scope}
    return layer, rows


# --------------------------------------------------------------------------------------
# Saved-item payloads (validation carried over unchanged)
# --------------------------------------------------------------------------------------
def require_investigation_id(value: Any) -> str:
    investigation_id = str(value or "").strip()
    if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id):
        raise ValueError("Invalid investigation id")
    return investigation_id


def normalize_memory_comment(value: Any) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) > 1200:
        raise ValueError("Memory comment exceeds 1200 characters")
    return text


def _list(value: Any) -> list[dict]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def normalize_memory_filters(value: Any) -> list[dict]:
    filters = []
    for item in _list(value):
        field = compact_text(item.get("field"), 160)
        operator = compact_text(item.get("operator") or "contains", 40)
        filter_value = compact_text(item.get("value"), 320)
        if field and filter_value:
            filters.append({"field": field, "operator": operator, "value": filter_value})
    return filters[:20]


def normalize_memory_ids(value: Any, limit: int = 80) -> list[str]:
    if not isinstance(value, list):
        return []
    ids, seen = [], set()
    for item in value:
        text = compact_text(item, 120)
        if text and text not in seen:
            ids.append(text)
            seen.add(text)
            if len(ids) >= limit:
                break
    return ids


def normalize_memory_reconstruction(value: Any) -> dict | None:
    if not isinstance(value, dict):
        return None
    reconstruction_type = compact_text(value.get("type"), 40)
    layer_kind = compact_text(value.get("layer_kind"), 80)
    record_ids = normalize_memory_ids(value.get("record_ids"), limit=5000)
    if reconstruction_type != "typed_ids" or not layer_kind or not record_ids:
        return None
    return {"type": reconstruction_type, "layer_kind": layer_kind, "record_ids": record_ids,
            "dataset_version": compact_text(value.get("dataset_version"), 40),
            "locale": compact_text(value.get("locale"), 12) or "he"}


def _count(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def layer_memory_item(request: dict) -> dict:
    layer = request.get("layer")
    if not isinstance(layer, dict):
        raise ValueError("Missing layer")
    label = compact_text(layer.get("label"), 240)
    kind = compact_text(layer.get("kind"), 80)
    if not label or not kind:
        raise ValueError("Missing layer label or kind")
    view = compact_text(layer.get("presentation_view"), 20)
    return {
        "id": new_item_id("layer"), "kind": "layer_filter_state", "saved_at_utc": utc_now_iso(),
        "source": "manual_user_action", "layer_id": compact_text(layer.get("id"), 240), "label": label,
        "layer_kind": kind,
        "catalog_layer_id": compact_text(layer.get("catalog_layer_id") or layer.get("catalogLayerId"), 240),
        "catalog_filters": validate_filters(layer.get("catalog_filters")),
        "data_id": compact_text(layer.get("data_id") or layer.get("dataId"), 240),
        "source_id": compact_text(layer.get("source_id") or layer.get("sourceId"), 240),
        "source_label": compact_text(layer.get("source_label") or layer.get("sourceLabel"), 240),
        "source_type": compact_text(layer.get("source_type"), 160),
        "presentation_view": view if view in {"map", "timeline", "table"} else "",
        "original_count": _count(layer.get("original_count")),
        "filtered_count": _count(layer.get("filtered_count")),
        "applied_filters": normalize_memory_filters(layer.get("applied_filters")),
        "sample_ids": normalize_memory_ids(layer.get("sample_ids")),
        "reconstruction": normalize_memory_reconstruction(layer.get("reconstruction")),
        "analyst_comment": normalize_memory_comment(request.get("comment")),
    }


def _ring(geometry: Any, what: str) -> list[list[float]]:
    coordinates = geometry.get("coordinates") if isinstance(geometry, dict) and geometry.get("type") == "Polygon" else None
    if not isinstance(coordinates, list) or len(coordinates) != 1 or not isinstance(coordinates[0], list):
        raise ValueError(f"{what} polygon requires one ring")
    ring = coordinates[0]
    if len(ring) < 4 or len(ring) > 200 or ring[0] != ring[-1]:
        raise ValueError(f"{what} polygon must be closed with 4 to 200 positions")
    normalized = []
    for position in ring:
        if not isinstance(position, list) or len(position) != 2:
            raise ValueError(f"Invalid {what.lower()} polygon position")
        lon, lat = position
        if (not isinstance(lon, (int, float)) or not isinstance(lat, (int, float)) or not math.isfinite(lon)
                or not math.isfinite(lat) or not -180 <= lon <= 180 or not -90 <= lat <= 90):
            raise ValueError(f"Invalid {what.lower()} polygon coordinates")
        normalized.append([float(lon), float(lat)])
    return normalized


def artifact_memory_item(request: dict) -> dict:
    artifact = request.get("artifact")
    if not isinstance(artifact, dict):
        raise ValueError("Missing memory artifact")
    kind = compact_text(artifact.get("kind"), 32)
    if kind == "object":
        object_kind = compact_text(artifact.get("object_kind"), 40)
        object_id = compact_text(artifact.get("object_id"), 240)
        label = compact_text(artifact.get("label"), 240)
        if not object_kind or not object_id or not label:
            raise ValueError("Memory object requires kind, id and label")
        item = {"kind": "object", "object_kind": object_kind, "object_id": object_id, "label": label,
                "summary": compact_text(artifact.get("summary"), 1800), "source_type": compact_text(artifact.get("source_type"), 160)}
    elif kind == "polygon":
        item = {"kind": "polygon", "label": compact_text(artifact.get("label") or "Saved area", 240),
                "geometry": {"type": "Polygon", "coordinates": [_ring(artifact.get("geometry"), "Memory")]}}
    else:
        raise ValueError("Unsupported memory artifact")
    item.update({"id": new_item_id("artifact"), "saved_at_utc": utc_now_iso(), "source": "manual_user_action",
                 "analyst_comment": normalize_memory_comment(request.get("comment"))})
    return item


COLLECTION_REQUEST_TYPES = {"adint", "cellular_geolocations", "cellular_calls", "satellite", "cctv"}
COLLECTION_REQUEST_TYPES_BY_ROLE = {
    "general": COLLECTION_REQUEST_TYPES,
    "sigint": {"cellular_geolocations", "cellular_calls"},
    "visint": {"satellite", "cctv"},
}
COLLECTION_EXTRACTION_OBJECTS = {"convoy", "vehicles", "personnel", "equipment", "infrastructure"}


def collection_request_item(request: dict, requested_by: str) -> dict:
    # The role decides which collection types the form offers. It is a workspace choice in the
    # UI, not an authorization: the record is attributed to the signed-in i360 user.
    role = compact_text(request.get("role") or "general", 20).lower()
    if role not in COLLECTION_REQUEST_TYPES_BY_ROLE:
        raise ValueError("Invalid collection role")
    collection_type = compact_text(request.get("collection_type"), 40).lower()
    if collection_type not in COLLECTION_REQUEST_TYPES_BY_ROLE[role]:
        raise ValueError("Collection type is not available for this role")
    target = request.get("target") if isinstance(request.get("target"), dict) else {}
    target_type = compact_text(target.get("type"), 20)
    if target_type == "imei":
        imei = compact_text(target.get("imei"), 32)
        if not re.fullmatch(r"[0-9A-Za-z._:-]{6,32}", imei):
            raise ValueError("Invalid IMEI collection target")
        normalized_target = {"type": "imei", "imei": imei}
    elif target_type == "polygon":
        normalized_target = {"type": "polygon", "geometry": {"type": "Polygon", "coordinates": [_ring(target.get("geometry"), "Collection")]}}
    else:
        raise ValueError("Unsupported collection target")
    extraction_objects = []
    for value in request.get("extraction_objects") if isinstance(request.get("extraction_objects"), list) else []:
        item = compact_text(value, 40).lower()
        if item in COLLECTION_EXTRACTION_OBJECTS and item not in extraction_objects:
            extraction_objects.append(item)
    if role == "visint" and not extraction_objects:
        raise ValueError("Choose at least one object to extract for a VISINT request")
    return {
        "id": new_item_id("collection"), "kind": "collection_request", "saved_at_utc": utc_now_iso(),
        "source": "user_action", "status": "requested", "role": role, "requested_by": requested_by,
        "collection_type": collection_type, "target": normalized_target,
        "extraction_objects": extraction_objects[:12],
        "instructions": normalize_memory_comment(request.get("instructions")),
        "label": f"{collection_type.replace('_', ' ')} · {normalized_target.get('imei') or 'marked area'}",
    }


def memory_layer_presentation(memory_payload: dict, memory_layer_id: str, data: Dataset) -> dict | None:
    memory = memory_payload.get("memory") if isinstance(memory_payload.get("memory"), dict) else {}
    saved_layer = next((item for item in _list(memory.get("layers")) if item.get("id") == memory_layer_id), None)
    if saved_layer is None:
        return None

    def unavailable(reason: str) -> dict:
        return {"memory_layer_id": memory_layer_id, "label": saved_layer.get("label"),
                "restore_status": "unavailable", "reason": reason, "requested_result_layers": []}

    reconstruction = normalize_memory_reconstruction(saved_layer.get("reconstruction"))
    if reconstruction is None:
        return unavailable("missing_reconstruction_definition")
    if reconstruction["locale"] != data.locale:
        return unavailable("locale_mismatch")
    layer_kind = reconstruction["layer_kind"]
    requested_ids = reconstruction["record_ids"]
    capabilities = {"table": True, "map": False, "timeline": False}
    if layer_kind == "events":
        rows_by_id = {str(r.get("record_id") or r.get("event_id") or ""): r for r in data.events}
        capabilities = {"table": True, "map": True, "timeline": True}
    elif layer_kind in {"locations", "location_metadata"}:
        rows_by_id = data.location_layers
        capabilities = {"table": True, "map": True, "timeline": False}
    elif layer_kind in {"entities", "entity_metadata"}:
        rows_by_id = data.entity_layers
    else:
        return unavailable("unsupported_layer_kind")
    rows = [rows_by_id[i] for i in requested_ids if i in rows_by_id]
    if layer_kind == "events":
        capabilities["map"] = any(r.get("location_id") in data.locations or r.get("latitude") for r in rows)
    missing = [i for i in requested_ids if i not in rows_by_id]
    status = "fully_restored" if not missing else ("partially_restored" if rows else "unavailable")
    kind = {"locations": "location_metadata", "entities": "entity_metadata"}.get(layer_kind, layer_kind)
    return {
        "memory_layer_id": memory_layer_id, "label": saved_layer.get("label"),
        "applied_filters": normalize_memory_filters(saved_layer.get("applied_filters")),
        "restore_status": status, "requested_count": len(requested_ids), "restored_count": len(rows),
        "missing_ids": missing,
        "requested_result_layers": ([{
            "id": f"memory:{memory_layer_id}", "label": saved_layer.get("label") or "Saved investigation layer",
            "kind": kind, "rows": rows, "capabilities": capabilities,
            "recommended_view": "timeline" if rows and all(r.get("call_id") for r in rows) else ("map" if capabilities["map"] else "table"),
        }] if rows else []),
    }


def subscriber_identity_review(data: Dataset, entity_id: str, action: str, previous: dict | None, reviewer: str) -> dict:
    if entity_id not in data.entities:
        raise ValueError("Person entity was not found")
    if action not in {"approve", "reject"}:
        raise ValueError("Derivation review action must be approve or reject")
    derivation = derive_subscriber_identity(data.events, data.links, entity_id)
    if derivation is None:
        raise ValueError("No cellular-geolocation records corroborate subscriber identifiers for this IMEI")
    return {
        **derivation,
        "review_state": "approved" if action == "approve" else "rejected",
        "reviewed_at_utc": (previous or {}).get("reviewed_at_utc") or utc_now_iso(),
        "reviewed_by": reviewer,
    }
