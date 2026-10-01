"""Deterministic, provenance-preserving links between immutable data objects.

This module deliberately creates links only.  It never adds facts to entities
or turns a graph path into a claim; that is the responsibility of a derivation
rule in the caller.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from typing import Any


SCHEMA_VERSION = 1


def _text(value: Any) -> str:
    return str(value or "").strip()


def _link_id(rule_id: str, source_id: str, source_field: str, target_id: str, target_field: str, value: str) -> str:
    payload = "\x1f".join((rule_id, source_id, source_field, target_id, target_field, value))
    return f"LNK-v1-{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:20].upper()}"


def _link(
    rule_id: str,
    source_type: str,
    source_id: str,
    source_field: str,
    target_type: str,
    target_id: str,
    target_field: str,
    value: str,
) -> dict[str, Any]:
    return {
        "link_id": _link_id(rule_id, source_id, source_field, target_id, target_field, value),
        "schema_version": SCHEMA_VERSION,
        "rule_id": rule_id,
        "kind": "field_equality",
        "from": {"object_type": source_type, "object_id": source_id, "field": source_field},
        "to": {"object_type": target_type, "object_id": target_id, "field": target_field},
        "matched_value": value,
        "provenance_record_ids": [source_id] if source_type == "raw_record" else [],
        "status": "observed",
    }


def build_links(events: list[dict[str, Any]], entities: dict[str, dict[str, Any]], locations: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Build only approved field-pair link rules for the active dataset."""
    links: list[dict[str, Any]] = []
    entity_identifiers: dict[str, list[str]] = defaultdict(list)
    device_identifiers: dict[str, str] = {}
    for entity_id, entity in entities.items():
        telecom = entity.get("telecom") if isinstance(entity.get("telecom"), dict) else {}
        imei = _text(telecom.get("imei"))
        if imei:
            entity_identifiers[imei].append(entity_id)
        if _text(entity.get("entity_type")).lower() == "device":
            for identifier in [_text(entity.get("canonical_name")), *[_text(value) for value in entity.get("aliases") or []]]:
                if identifier:
                    device_identifiers[identifier] = entity_id

    for event in events:
        record_id = _text(event.get("event_id"))
        if not record_id:
            continue
        source_type = _text(event.get("source_type"))
        entity_id = _text(event.get("entity_id"))
        if entity_id in entities:
            links.append(_link("event_entity_id_v1", "raw_record", record_id, "entity_id", "entity", entity_id, "entity_id", entity_id))
        location_id = _text(event.get("location_id"))
        if location_id in locations:
            links.append(_link("event_location_id_v1", "raw_record", record_id, "location_id", "location", location_id, "location_id", location_id))
        if _text(event.get("source_type")).casefold() == "adint":
            device_id = _text(event.get("device_id"))
            device_entity_id = device_identifiers.get(device_id)
            if device_id and device_entity_id:
                links.append(_link("adint_device_entity_v1", "raw_record", record_id, "device_id", "entity", device_entity_id, "canonical_name", device_id))
        # Side B is intentionally omitted: current data has no asserted Side-B identity.
        for field, rule_id, allowed_sources in (
            ("imei", "entity_imei_to_ipdr_imei_v1", {"IPDR"}),
            ("target_imei", "entity_imei_to_cellular_target_imei_v1", {"Cellular Geolocations"}),
            ("side_a_imei", "entity_imei_to_call_party_v1", {"Cellular Calls", "שיחות סלולר"}),
            ("call_transcript_speaker_imei", "entity_imei_to_call_speaker_imei_v1", {"Cellular Calls", "שיחות סלולר"}),
        ):
            if source_type not in allowed_sources:
                continue
            value = _text(event.get(field))
            for matched_entity_id in entity_identifiers.get(value, []):
                links.append(_link(rule_id, "raw_record", record_id, field, "entity", matched_entity_id, "telecom.imei", value))
        package_id = _text(event.get("package_id"))
        if package_id:
            links.append(_link("ipdr_package_membership_v1", "raw_record", record_id, "package_id", "evidence", package_id, "package_id", package_id))
    return sorted(links, key=lambda item: item["link_id"])


def derive_subscriber_identity(events: list[dict[str, Any]], links: list[dict[str, Any]], entity_id: str, minimum_records: int = 2) -> dict[str, Any] | None:
    """Derive a candidate only from already-created target-IMEI links.

    The rule requires a unique most-supported non-empty MSISDN/IMSI pair.  A
    tie or insufficient support produces no claim rather than an arbitrary one.
    """
    by_id = {_text(event.get("event_id")): event for event in events if _text(event.get("event_id"))}
    pairs: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)
    for link in links:
        if link.get("rule_id") != "entity_imei_to_cellular_target_imei_v1" or link.get("to", {}).get("object_id") != entity_id:
            continue
        record_id = _text(link.get("from", {}).get("object_id"))
        event = by_id.get(record_id, {})
        msisdn, imsi = _text(event.get("target_msisdn")), _text(event.get("target_imsi"))
        if msisdn and imsi:
            pairs[(msisdn, imsi)].append((record_id, _text(link.get("link_id"))))
    eligible = [(pair, support) for pair, support in pairs.items() if len({record_id for record_id, _ in support}) >= minimum_records]
    if not eligible:
        return None
    best_count = max(len({record_id for record_id, _ in support}) for _, support in eligible)
    winners = [(pair, support) for pair, support in eligible if len({record_id for record_id, _ in support}) == best_count]
    if len(winners) != 1:
        return None
    (msisdn, imsi), support = winners[0]
    record_ids = sorted({record_id for record_id, _ in support})
    link_ids = sorted({link_id for _, link_id in support})
    fingerprint = hashlib.sha256(json.dumps([entity_id, msisdn, imsi, record_ids], separators=(",", ":")).encode("utf-8")).hexdigest()[:20].upper()
    return {
        "derivation_id": f"DRV-v1-{fingerprint}",
        "schema_version": SCHEMA_VERSION,
        "rule_id": "subscriber_identity_from_imei_linked_records_v1",
        "subject": {"object_type": "entity", "object_id": entity_id},
        "claim": {"property": "subscriber_identity", "value": {"msisdn": msisdn, "imsi": imsi}},
        "supporting_link_ids": link_ids,
        "supporting_record_ids": record_ids,
        "status": "candidate",
        "review_state": "pending",
    }
