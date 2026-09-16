"""Conservative catalog resolution and lossless raw-record scope validation."""
from __future__ import annotations

import re
import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher


def normalized_name(value):
    value = unicodedata.normalize("NFKC", str(value)).casefold()
    value = value.translate(str.maketrans("ךםןףץ", "כמנפצ"))
    return " ".join(re.sub(r"[^\w\s]", "", value).split())


def resolve_layer(requested, catalog):
    """Return only catalog-owned IDs; never guess among close competitors."""
    requested = str(requested).strip()
    exact = next((layer for layer in catalog if layer["id"] == requested), None)
    if exact:
        return {"status": "resolved", "layer": exact, "match": "exact"}
    family, separator, name = requested.partition(":")
    name = name if separator else family
    needle = normalized_name(name)
    candidates = []
    for layer in catalog:
        if separator and layer["id"].split(":", 1)[0] != family:
            continue
        names = [layer["id"].split(":", 1)[-1], layer.get("label", ""), layer.get("source_type", "")]
        names += layer.get("aliases", [])
        score = max((SequenceMatcher(None, needle, normalized_name(n)).ratio() for n in names if n), default=0)
        if needle and score >= 0.70:
            candidates.append((score, layer))
    candidates.sort(key=lambda item: (-item[0], item[1]["id"]))
    if candidates:
        score, best = candidates[0]
        runner_up = candidates[1][0] if len(candidates) > 1 else 0
        if score >= 0.88 and score - runner_up >= 0.10:
            return {"status": "resolved", "layer": best, "match": "normalized" if score == 1 else "close"}
    return {
        "status": "ambiguous" if candidates else "not_found",
        "requested_id": requested,
        "candidates": [{"id": layer["id"], "label": layer.get("label", layer["id"])} for _, layer in candidates[:5]],
    }


FILTER_FIELDS = {"location_ids", "entity_ids", "event_ids", "start_time", "end_time"}


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed


def validate_filters(value):
    if value is None:
        return {}
    if not isinstance(value, dict) or set(value) - FILTER_FIELDS:
        raise ValueError("unsupported catalog filters; use location_ids, entity_ids, event_ids, start_time, end_time")
    result = {}
    for key, items in value.items():
        if key.endswith("_ids"):
            if not isinstance(items, list) or not items or len(items) > 2000 or any(not isinstance(i, str) or not i.strip() for i in items):
                raise ValueError(f"{key} must be a nonempty list of IDs")
            result[key] = sorted(set(i.strip() for i in items))
        else:
            if not isinstance(items, str) or not items.strip():
                raise ValueError(f"{key} must be an ISO timestamp")
            timestamp(items)
            result[key] = items
    if result.get("start_time") and result.get("end_time") and timestamp(result["start_time"]) > timestamp(result["end_time"]):
        raise ValueError("start_time must precede end_time")
    return result


def filter_rows(rows, filters):
    filters = validate_filters(filters)
    start = timestamp(filters["start_time"]) if filters.get("start_time") else None
    end = timestamp(filters["end_time"]) if filters.get("end_time") else None
    def matches(row):
        for field in ("location", "entity", "event"):
            if filters.get(field + "_ids") and row.get(field + "_id") not in filters[field + "_ids"]:
                return False
        if start or end:
            try:
                when = timestamp(row.get("timestamp_utc") or "")
            except (ValueError, TypeError):
                return False
            if (start and when < start) or (end and when > end):
                return False
        return True
    return [row for row in rows if matches(row)]
