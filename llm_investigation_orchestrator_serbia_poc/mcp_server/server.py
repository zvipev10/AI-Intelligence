#!/usr/bin/env python3
"""Constrained MCP server for synthetic intelligence evidence and target candidates."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    from fusion_tools import discover_corroborating_evidence, find_duplicate_candidates, prepare_candidate
    from semantic_index import SemanticEventIndex
    from target_bank import TargetBank
except ImportError:  # pragma: no cover - package-style execution fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from fusion_tools import discover_corroborating_evidence, find_duplicate_candidates, prepare_candidate
    from semantic_index import SemanticEventIndex
    from target_bank import TargetBank


PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "serbia-events-poc"
SERVER_VERSION = "0.3.0"
DEFAULT_LIMIT = 2000
MAX_LIMIT = 2000
MIN_COVERAGE_LIMIT = 2000
MAX_SEMANTIC_LIMIT = 200

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_VERSION = os.environ.get("INTELLIGENCE_POC_DATASET_VERSION", "v2").strip().lower()
if DATASET_VERSION in {"v2.1", "v2_1", "v21"}:
    DATASET_VERSION = "v2.1"
    DEFAULT_DATASET_DIR = BASE_DIR / "data" / "serbian_intelligence_v2_1"
    DEFAULT_DATA_PATH = DEFAULT_DATASET_DIR / "serbia_kosovo_events_projection_v2_1.csv"
    DEFAULT_LOCATIONS_PATH = DEFAULT_DATASET_DIR / "serbia_kosovo_locations_v2_1.json"
    DEFAULT_ENTITIES_PATH = DEFAULT_DATASET_DIR / "serbia_kosovo_entities_v2_1.json"
elif DATASET_VERSION == "v2":
    DEFAULT_DATASET_DIR = BASE_DIR / "data" / "serbian_intelligence_v2"
    DEFAULT_DATA_PATH = DEFAULT_DATASET_DIR / "serbia_kosovo_events_projection_v2.csv"
    DEFAULT_LOCATIONS_PATH = DEFAULT_DATASET_DIR / "serbia_kosovo_locations_v2.json"
    DEFAULT_ENTITIES_PATH = DEFAULT_DATASET_DIR / "serbia_kosovo_entities_v2.json"
elif DATASET_VERSION == "v1":
    DEFAULT_DATASET_DIR = BASE_DIR / "data"
    DEFAULT_DATA_PATH = DEFAULT_DATASET_DIR / "serbia_kosovo_events_projection.csv"
    DEFAULT_LOCATIONS_PATH = DEFAULT_DATASET_DIR / "serbia_kosovo_locations.json"
    DEFAULT_ENTITIES_PATH = DEFAULT_DATASET_DIR / "serbia_kosovo_entities.json"
else:
    raise ValueError(f"Unsupported INTELLIGENCE_POC_DATASET_VERSION: {DATASET_VERSION}")
DATA_PATH = Path(os.environ.get("INTELLIGENCE_POC_DATA", DEFAULT_DATA_PATH))
LOCATIONS_PATH = Path(os.environ.get("INTELLIGENCE_POC_LOCATIONS", DEFAULT_LOCATIONS_PATH))
ENTITIES_PATH = Path(os.environ.get("INTELLIGENCE_POC_ENTITIES", DEFAULT_ENTITIES_PATH))
SEMANTIC_INDEX_DIR = Path(os.environ.get("INTELLIGENCE_POC_SEMANTIC_INDEX", BASE_DIR / "data" / "semantic_index" / DATASET_VERSION))
SEMANTIC_BACKEND = os.environ.get("INTELLIGENCE_POC_SEMANTIC_BACKEND", "hybrid_embedding")
AUDIT_PATH = Path(os.environ.get("INTELLIGENCE_POC_AUDIT", BASE_DIR / "mcp_audit.jsonl"))
PLAYBACK_VISIBILITY_PATH = Path(os.environ.get(
    "INTELLIGENCE_POC_PLAYBACK_VISIBILITY",
    BASE_DIR / "scenario_runs" / ("" if DATASET_VERSION == "v1" else DATASET_VERSION) / "active_visibility.json",
))
CLIENT_SUPPORTS_SAMPLING = False
NEXT_SERVER_REQUEST_ID = 100000

LOCATIONS = json.loads(LOCATIONS_PATH.read_text(encoding="utf-8")) if LOCATIONS_PATH.exists() else {}

AREA_ALIASES = {
    "צפון קוסובו": [location_id for location_id, item in LOCATIONS.items() if item.get("region") == "צפון קוסובו"],
    "צפון מיטרוביצה": [location_id for location_id, item in LOCATIONS.items() if item.get("municipality") == "צפון מיטרוביצה"],
    "זבצ׳אן": [location_id for location_id, item in LOCATIONS.items() if item.get("municipality") == "זבצ׳אן"],
    "זובין פוטוק": [location_id for location_id, item in LOCATIONS.items() if item.get("municipality") == "זובין פוטוק"],
    "לפוסאביץ׳": [location_id for location_id, item in LOCATIONS.items() if item.get("municipality") == "לפוסאביץ׳"],
    "סרביה": [location_id for location_id, item in LOCATIONS.items() if item.get("country") == "סרביה"],
    "דרום סרביה": [location_id for location_id, item in LOCATIONS.items() if item.get("region") == "דרום סרביה"],
    "בלגרד": [location_id for location_id, item in LOCATIONS.items() if item.get("municipality") == "בלגרד"],
    "פרישטינה": [location_id for location_id, item in LOCATIONS.items() if item.get("municipality") == "פרישטינה"],
    "ראשקה": [location_id for location_id, item in LOCATIONS.items() if item.get("municipality") == "ראשקה"],
    "נובי פאזאר": [location_id for location_id, item in LOCATIONS.items() if item.get("municipality") == "נובי פאזאר"],
}

EVENT_REFERENCES = {}

IDENTIFIER_PATTERNS = {
    "record": re.compile(r"\bREC-(?:V2-)?\d{6}\b", re.IGNORECASE),
    "location": re.compile(r"\bLOC-(?:V2-)?\d{3}\b", re.IGNORECASE),
}

BENIGN_MARKERS = (
    "תקלה רגילה", "רעש", "אין אישור", "לא ברור", "שגרה", "אזרחי", "לא מאומת",
    "לא ידוע", "שמועה", "מכחיש",
)

NEGATION_MARKERS = (
    "אין אישור", "מכחיש", "לא ברור", "לא מאומת", "אין לכך אימות",
)

DIRECT_OBSERVATION_MARKERS = (
    "דיווח", "זוהה", "נמסר", "תועד", "נטען", "אישר", "הכחיש", "הופיע", "נסגר", "נחסם",
)

NON_INFORMATIVE_ACTORS = {
    "", "לא ידוע", "לא מזוהה", "גורם לא ידוע", "גורם לא מזוהה", "לא ברור",
}

SEMANTIC_CLUE_TERMS = (
    "KFOR", "EULEX", "משטרת קוסובו", "צבא סרביה", "מפגינים", "חסימה", "מחסום",
    "ירי", "פיצוץ", "רחפן", "מסוק", "כוננות", "חציית גבול", "גבול", "עירייה",
    "פצועים", "אמבולנס", "בית חולים", "שמועה", "מקורות אחרים", "חשבונות",
    "סרטון", "תמונה", "הכחשה", "מכחישים", "הסלמה", "מחאה",
)

def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def load_events() -> list[dict[str, Any]]:
    with DATA_PATH.open(encoding="utf-8-sig", newline="") as handle:
        events = list(csv.DictReader(handle))
    for event in events:
        location = LOCATIONS.get(event["location_id"], {})
        event["location_name"] = location.get("name", event["location_id"])
        event["location_type"] = location.get("type", "")
        event["timestamp"] = parse_time(event["timestamp_utc"])
    events.sort(key=lambda item: item["timestamp"])
    return events


EVENTS = load_events()
EVENT_BY_ID = {event["event_id"]: event for event in EVENTS}
EVENTS_BY_ID = {event["event_id"]: event for event in EVENTS}
FUSION_EVENTS_BY_CONTEXT: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
for _fusion_event in EVENTS:
    FUSION_EVENTS_BY_CONTEXT[(_fusion_event.get("location_id") or "", _fusion_event.get("entity_id") or "")].append(_fusion_event)
ENTITY_PRESENTATIONS: dict[str, dict[str, Any]] = {}
LOCATION_PRESENTATIONS: dict[str, dict[str, Any]] = {}
ENTITIES: dict[str, dict[str, Any]] = {}
SEMANTIC_INDEX: SemanticEventIndex | None = None


def active_playback_policy() -> dict[str, Any] | None:
    """Load and strictly validate the current server-owned playback boundary."""
    if not PLAYBACK_VISIBILITY_PATH.exists():
        return None
    try:
        policy = json.loads(PLAYBACK_VISIBILITY_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("Playback visibility policy is unreadable") from exc
    if not isinstance(policy, dict) or policy.get("schema_version") != 1:
        raise ValueError("Playback visibility policy is invalid")
    if not policy.get("active"):
        return None
    if policy.get("dataset") != DATASET_VERSION:
        raise ValueError("Active playback dataset does not match the evidence server")
    timeframe = policy.get("visible_timeframe")
    if not isinstance(timeframe, dict):
        raise ValueError("Active playback timeframe is invalid")
    start = parse_time(timeframe.get("from"))
    end = parse_time(timeframe.get("to"))
    if start is None or end is None or start >= end:
        raise ValueError("Active playback timeframe is invalid")
    layers = policy.get("layers") or []
    if not isinstance(layers, list) or any(not isinstance(item, str) for item in layers):
        raise ValueError("Active playback layers are invalid")
    return {**policy, "_from": start, "_to": end, "layers": layers}


def event_visible(event: dict[str, Any], policy: dict[str, Any] | None = None) -> bool:
    policy = active_playback_policy() if policy is None else policy
    if policy is None:
        return True
    if not (policy["_from"] <= event["timestamp"] < policy["_to"]):
        return False
    layers = set(policy["layers"])
    return not layers or f"events:{event.get('source_type', '')}" in layers


def visible_events() -> list[dict[str, Any]]:
    policy = active_playback_policy()
    return list(EVENTS) if policy is None else [event for event in EVENTS if event_visible(event, policy)]


def visible_event(event_id: str) -> dict[str, Any] | None:
    event = EVENTS_BY_ID.get(event_id)
    return event if event is not None and event_visible(event) else None


def visible_event_ids() -> set[str]:
    return {event["event_id"] for event in visible_events()}


def scoped_entity_presentation(entity_id: str) -> dict[str, Any] | None:
    base = ENTITY_PRESENTATIONS.get(entity_id)
    if base is None:
        return None
    if active_playback_policy() is None:
        return base
    events = [event for event in visible_events() if event.get("entity_id") == entity_id]
    if not events:
        return None
    return {
        **base,
        "event_count": len(events),
        "top_locations": [
            {"location_id": key, "location_name": LOCATIONS.get(key, {}).get("name", key), "count": count}
            for key, count in Counter(event["location_id"] for event in events).most_common(12)
        ],
        "top_sources": [
            {"source_type": key, "count": count}
            for key, count in Counter(event["source_type"] for event in events).most_common(10)
        ],
        "certainty_breakdown": dict(Counter(event.get("certainty_level") or "unknown" for event in events)),
        "reliability_breakdown": dict(Counter(
            event.get("source_reliability_label") or event.get("source_reliability") or "unknown"
            for event in events
        )),
    }


def scoped_location_presentation(location_id: str) -> dict[str, Any] | None:
    base = LOCATION_PRESENTATIONS.get(location_id)
    if base is None:
        return None
    if active_playback_policy() is None:
        return base
    events = [event for event in visible_events() if event["location_id"] == location_id]
    if not events:
        return None
    return {
        **base,
        "event_count": len(events),
        "top_entities": [
            {"entity_id": key, "name": ENTITY_PRESENTATIONS.get(key, {}).get("canonical_name", key), "count": count}
            for key, count in Counter(
                event.get("entity_id") for event in events if event.get("entity_id")
            ).most_common(10)
        ],
        "top_sources": [
            {"source_type": key, "count": count}
            for key, count in Counter(event["source_type"] for event in events).most_common(10)
        ],
        "certainty_breakdown": dict(Counter(event.get("certainty_level") or "unknown" for event in events)),
        "reliability_breakdown": dict(Counter(
            event.get("source_reliability_label") or event.get("source_reliability") or "unknown"
            for event in events
        )),
    }


def _fold(value: str | None) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


def split_location_query(query: str) -> list[str]:
    """Split natural analyst geography into separately resolvable terms."""
    normalized = re.sub(r"\s+", " ", query.strip())
    if not normalized:
        return []
    parts = re.split(r"[,;،]+|\s+ו(?=\S)|\s+ו(?=\s)", normalized)
    cleaned: list[str] = []
    for part in parts:
        term = part.strip(" .:-–—")
        if term and term not in cleaned:
            cleaned.append(term)
    if len(cleaned) <= 1 and normalized not in cleaned:
        cleaned.insert(0, normalized)
    return cleaned


def match_location_term(term: str) -> list[str]:
    folded = _fold(term)
    if not folded:
        return []
    exact_alias = AREA_ALIASES.get(term)
    if exact_alias:
        return list(exact_alias)
    for alias, location_ids in AREA_ALIASES.items():
        alias_folded = _fold(alias)
        if folded == alias_folded or folded in alias_folded or alias_folded in folded:
            return list(location_ids)

    matched: list[str] = []
    for location_id, location in LOCATIONS.items():
        fields = [
            location.get("name"),
            location.get("type"),
            location.get("municipality"),
            location.get("region"),
            location.get("country"),
            location.get("locality"),
        ]
        haystack = " ".join(_fold(value) for value in fields if value)
        if folded in haystack:
            matched.append(location_id)
    return matched


def load_entity_db() -> dict[str, dict[str, Any]]:
    loaded = json.loads(ENTITIES_PATH.read_text(encoding="utf-8")) if ENTITIES_PATH.exists() else []
    return {item["entity_id"]: item for item in loaded if item.get("entity_id")}


def build_entity_layers() -> dict[str, dict[str, Any]]:
    entity_db = load_entity_db()
    entity_ids = sorted({event.get("entity_id", "") for event in EVENTS if event.get("entity_id")})
    presentations: dict[str, dict[str, Any]] = {}
    for entity_id in entity_ids:
        base = entity_db.get(entity_id)
        if not base:
            raise ValueError(f"Missing entity_id in entities DB: {entity_id}")
        events = [event for event in EVENTS if event.get("entity_id") == entity_id]
        top_locations = []
        for location_id, count in Counter(event["location_id"] for event in events).most_common(12):
            location = LOCATIONS.get(location_id, {})
            top_locations.append({
                "location_id": location_id,
                "location_name": location.get("name", location_id),
                "municipality": location.get("municipality"),
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
                "count": count,
            })
        presentations[entity_id] = {
            "entity_id": entity_id,
            "canonical_name": base.get("canonical_name") or entity_id,
            "entity_type": base.get("entity_type") or "גורם מדווח",
            "confidence": base.get("confidence") or "entity_id גלוי ברשומה",
            "basis": base.get("basis") or "ישות מתוך serbia_kosovo_entities.json לפי entity_id ברשומה",
            "aliases": list(dict.fromkeys(base.get("aliases") or [base.get("canonical_name") or entity_id])),
            "event_count": len(events),
            "top_locations": top_locations,
            "top_sources": [{"source_type": key, "count": count} for key, count in Counter(event["source_type"] for event in events).most_common(10)],
            "certainty_breakdown": dict(Counter(event.get("certainty_level") or "לא ידוע" for event in events)),
            "reliability_breakdown": dict(Counter(event.get("source_reliability_label") or event.get("source_reliability") or "לא ידוע" for event in events)),
        }
    return presentations


def build_location_layers() -> dict[str, dict[str, Any]]:
    presentations: dict[str, dict[str, Any]] = {}
    events_by_location: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in EVENTS:
        events_by_location[event["location_id"]].append(event)
    for location_id, location in LOCATIONS.items():
        events = events_by_location.get(location_id, [])
        presentations[location_id] = {
            "location_id": location_id,
            "location_name": location.get("name", location_id),
            "name": location.get("name", location_id),
            "type": location.get("type"),
            "country": location.get("country"),
            "region": location.get("region"),
            "municipality": location.get("municipality"),
            "locality": location.get("locality"),
            "precision": location.get("precision"),
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "event_count": len(events),
            "top_entities": [
                {
                    "entity_id": entity_id,
                    "name": ENTITY_PRESENTATIONS.get(entity_id, {}).get("canonical_name", entity_id),
                    "count": count,
                }
                for entity_id, count in Counter(event.get("entity_id") for event in events if event.get("entity_id")).most_common(10)
            ],
            "top_sources": [{"source_type": key, "count": count} for key, count in Counter(event["source_type"] for event in events).most_common(10)],
            "certainty_breakdown": dict(Counter(event.get("certainty_level") or "לא ידוע" for event in events)),
            "reliability_breakdown": dict(Counter(event.get("source_reliability_label") or event.get("source_reliability") or "לא ידוע" for event in events)),
        }
    return presentations


ENTITY_PRESENTATIONS = build_entity_layers()
LOCATION_PRESENTATIONS = build_location_layers()


def event_entity_id(event: dict[str, Any]) -> str | None:
    return event.get("entity_id")


def event_entity_name(event: dict[str, Any]) -> str:
    entity = ENTITY_PRESENTATIONS.get(event_entity_id(event) or "", {})
    return entity.get("canonical_name") or event_entity_id(event) or "לא ידוע"


def public_event(event: dict[str, Any]) -> dict[str, Any]:
    entity_id = event_entity_id(event)
    entity = ENTITY_PRESENTATIONS.get(entity_id or "", {})
    return {
        "event_id": event["event_id"],
        "timestamp_utc": event["timestamp_utc"],
        "source_type": event["source_type"],
        "source_reliability": event["source_reliability"],
        "certainty_level": event.get("certainty_level", ""),
        "source_reliability_label": event.get("source_reliability_label", ""),
        "entity_id": entity_id,
        "entity_name": entity.get("canonical_name") or entity_id,
        "location_id": event["location_id"],
        "location_name": event["location_name"],
        "location_type": event["location_type"],
        "event_summary": event["event_summary"],
        "collection_family": event.get("collection_family", ""),
        "observation_id": event.get("observation_id", ""),
        "mission_id": event.get("mission_id", ""),
        "object_class": event.get("object_class", ""),
        "estimated_object_count": event.get("estimated_object_count", ""),
        "movement_status": event.get("movement_status", ""),
        "movement_direction": event.get("movement_direction", ""),
        "geolocation_confidence": event.get("geolocation_confidence", ""),
        "identification_confidence": event.get("identification_confidence", ""),
    }


def semantic_index_signature() -> dict[str, Any]:
    signature = {}
    for label, path in [("events", DATA_PATH), ("locations", LOCATIONS_PATH), ("entities", ENTITIES_PATH)]:
        try:
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            signature[f"{label}_sha256"] = digest.hexdigest()
            signature[f"{label}_size"] = path.stat().st_size
        except OSError:
            signature[f"{label}_missing"] = True
    return signature


def get_semantic_index() -> SemanticEventIndex:
    global SEMANTIC_INDEX
    if SEMANTIC_INDEX is None:
        SEMANTIC_INDEX = SemanticEventIndex(
            [public_event(event) for event in EVENTS],
            cache_dir=SEMANTIC_INDEX_DIR,
            signature=semantic_index_signature(),
            backend=SEMANTIC_BACKEND,
        )
    return SEMANTIC_INDEX


def text_result(payload: Any, is_error: bool = False) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
        "structuredContent": payload,
        "isError": is_error,
    }


def write_audit(tool: str, arguments: dict[str, Any], result: Any, is_error: bool = False, duration_ms: float | None = None) -> None:
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "tool": tool,
        "arguments": arguments,
        "result": result,
        "is_error": is_error,
    }
    try:
        policy = active_playback_policy()
        record["playback_visibility"] = (
            {
                "run_id": policy.get("run_id"),
                "revision": policy.get("revision"),
                "visible_timeframe": policy.get("visible_timeframe"),
            }
            if policy is not None else None
        )
    except ValueError:
        record["playback_visibility"] = {"invalid": True}
    if duration_ms is not None:
        record["duration_ms"] = round(duration_ms, 3)
    try:
        AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with AUDIT_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    except OSError:
        pass


def bounded_limit(value: Any) -> int:
    try:
        return max(1, min(int(value or DEFAULT_LIMIT), MAX_LIMIT))
    except (TypeError, ValueError):
        return DEFAULT_LIMIT


def coverage_limit(value: Any) -> int:
    """Use maximum bounded coverage for investigative retrieval, even if the model asks for a small sample."""
    return max(MIN_COVERAGE_LIMIT, bounded_limit(value))


def semantic_filters_from_arguments(arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        "start_time": arguments.get("start_time"),
        "end_time": arguments.get("end_time"),
        "location_ids": arguments.get("location_ids") or [],
        "entity_ids": arguments.get("entity_ids") or [],
        "source_types": arguments.get("source_types") or [],
        "reliabilities": arguments.get("reliabilities") or [],
        "certainty_levels": arguments.get("certainty_levels") or [],
        "keywords": arguments.get("keywords") or [],
        "match_all_keywords": bool(arguments.get("match_all_keywords", False)),
    }


def semantic_candidates(query: str, arguments: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    query = str(query or "").strip()
    if not query:
        return []
    try:
        candidate_limit = max(1, min(int(limit or DEFAULT_LIMIT), MAX_LIMIT))
    except (TypeError, ValueError):
        candidate_limit = DEFAULT_LIMIT
    matches = get_semantic_index().search(
        query,
        filters=semantic_filters_from_arguments(arguments),
        limit=candidate_limit,
    )
    allowed = visible_event_ids()
    return [match for match in matches if match.get("event_id") in allowed]


def sort_order_desc(arguments: dict[str, Any]) -> bool:
    return str(arguments.get("sort_order") or "asc").casefold() == "desc"


def normalize_text(value: str) -> str:
    return " ".join(value.casefold().split())


def next_server_request_id() -> int:
    global NEXT_SERVER_REQUEST_ID
    NEXT_SERVER_REQUEST_ID += 1
    return NEXT_SERVER_REQUEST_ID


def extract_json_object(text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {}
    try:
        parsed = json.loads(match.group(0))
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def sample_json_task(
    task_name: str,
    system_prompt: str,
    payload: dict[str, Any],
    max_tokens: int = 700,
) -> dict[str, Any] | None:
    if not CLIENT_SUPPORTS_SAMPLING:
        return None
    request_id = next_server_request_id()
    sampling_payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "sampling/createMessage",
        "params": {
            "systemPrompt": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": json.dumps({"task": task_name, **payload}, ensure_ascii=False),
                    },
                }
            ],
            "maxTokens": max_tokens,
            "temperature": 0,
        },
    }
    print(json.dumps(sampling_payload, ensure_ascii=False, separators=(",", ":")), flush=True)
    deadline = time.time() + 20
    while time.time() < deadline:
        line = sys.stdin.readline()
        if not line:
            return None
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if message.get("id") != request_id:
            continue
        if "error" in message:
            return None
        result = message.get("result") or {}
        content = result.get("content")
        text = ""
        if isinstance(content, dict):
            text = str(content.get("text") or "")
        elif isinstance(content, list):
            text = "\n".join(str(item.get("text") or "") for item in content if isinstance(item, dict))
        if not text:
            text = str(result.get("text") or "")
        return extract_json_object(text) or None
    return None


def string_list(value: Any, limit: int = 20) -> list[str]:
    if not isinstance(value, list):
        return []
    cleaned = []
    seen = set()
    for item in value:
        text = str(item).strip()
        folded = normalize_text(text)
        if not text or folded in seen:
            continue
        seen.add(folded)
        cleaned.append(text[:80])
        if len(cleaned) >= limit:
            break
    return cleaned


def is_informative_actor(actor: str | None) -> bool:
    return normalize_text(actor or "") not in {normalize_text(item) for item in NON_INFORMATIVE_ACTORS}


def event_has_negation(event: dict[str, Any]) -> bool:
    return any(marker in event["event_summary"] for marker in NEGATION_MARKERS)


def term_variants(term: str) -> set[str]:
    folded = normalize_text(term)
    variants = {folded}
    words = folded.split()
    if not words:
        return variants
    first_prefixes = ["", "ה", "ב", "ל", "כ", "מ"]
    word_options = []
    for index, word in enumerate(words):
        if index == 0:
            word_options.append([f"{prefix}{word}" for prefix in first_prefixes])
        else:
            word_options.append([word, f"ה{word}"])
    for first in word_options[0]:
        if len(word_options) == 1:
            variants.add(first)
        else:
            for second in word_options[1]:
                tail = word_options[2:] if len(word_options) > 2 else []
                if not tail:
                    variants.add(" ".join([first, second]))
                else:
                    variants.add(" ".join([first, second, *[options[0] for options in tail]]))
    return variants


def term_in_text(term: str, text: str) -> bool:
    folded_text = normalize_text(text)
    return any(variant and variant in folded_text for variant in term_variants(term))


def semantic_clues_from_text(text: str) -> list[str]:
    clues = []
    for term in SEMANTIC_CLUE_TERMS:
        if term_in_text(term, text):
            clues.append(term)
    return clues


def semantic_overlap(first_text: str, second_text: str) -> list[str]:
    first = set(semantic_clues_from_text(first_text))
    second = set(semantic_clues_from_text(second_text))
    return sorted(first & second)


def investigative_seed_score(event: dict[str, Any], matched_clues: list[str] | None = None) -> tuple[int, list[str]]:
    summary = event["event_summary"]
    score = 0
    reasons = []
    source = event["source_type"]
    source_weights = {
        "הודעת דובר": 8,
        "טלגרם": 7,
        "חדשות מקומיות": 7,
        "X": 7,
        "טיקטוק": 6,
        "פייסבוק": 6,
        "קבוצת וואטסאפ": 6,
        "ערוץ חדשות בינלאומי": 6,
        "בלוג פוליטי": 5,
        "שמועה מקומית": 4,
    }
    if source in source_weights:
        score += source_weights[source]
        reasons.append(f"סוג מקור חקירתי: {source}")
    markers = [
        ("חציית גבול", 8, "רמז לטענת חציית גבול"),
        ("מקורות אחרים", 8, "רמז לסתירה בין מקורות"),
        ("מכחישים", 7, "רמז להכחשה או סתירה"),
        ("חשבונות", 7, "רמז להפצה ברשתות"),
        ("KFOR", 7, "רמז לנוכחות KFOR"),
        ("EULEX", 7, "רמז לנוכחות EULEX"),
        ("משטרת קוסובו", 7, "רמז לפעילות משטרתית"),
        ("חסימה", 6, "רמז למחסום או חסימת ציר"),
        ("ירי", 6, "רמז לטענת ירי"),
        ("פיצוץ", 6, "רמז לטענת פיצוץ"),
        ("שמועה", 5, "רמז לדיווח לא מאומת"),
        ("סרטון", 5, "רמז למדיה גלויה או טענה ויזואלית"),
    ]
    for term, weight, reason in markers:
        if term_in_text(term, summary):
            score += weight
            reasons.append(reason)
    if matched_clues:
        score += min(len(matched_clues), 3) * 3
        reasons.append("התאמה לרמזים שנבדקו")
    if event_has_negation(event):
        score -= 12
        reasons.append("רשומה שוללת או חלופית")
    if any(marker in summary for marker in BENIGN_MARKERS):
        score -= 10
        reasons.append("מסומן כשגרתי או תמים")
    return score, reasons[:5]


def entity_matches(query: str) -> list[dict[str, Any]]:
    folded = normalize_text(query)
    matches = []
    for entity_id, entity in ENTITY_PRESENTATIONS.items():
        entity = scoped_entity_presentation(entity_id)
        if entity is None:
            continue
        aliases = entity.get("aliases", [])
        exact = [alias for alias in aliases if normalize_text(alias) == folded]
        partial = [alias for alias in aliases if folded and folded in normalize_text(alias)]
        id_match = folded and folded == normalize_text(entity_id)
        if exact or partial:
            matches.append({"entity_id": entity_id, **entity, "match_type": "exact" if exact else "partial"})
        elif id_match:
            matches.append({"entity_id": entity_id, **entity, "match_type": "entity_id"})
    return matches


def canonical_entity_ids(actor: str) -> set[str]:
    return {match["entity_id"] for match in entity_matches(actor)}


def extract_identifiers(text: str) -> list[dict[str, str]]:
    found = []
    seen = set()
    for identifier_type, pattern in IDENTIFIER_PATTERNS.items():
        for match in pattern.finditer(text):
            value = " ".join(match.group(0).upper().split()) if identifier_type == "container" else " ".join(match.group(0).split())
            key = (identifier_type, value.casefold())
            if key not in seen:
                seen.add(key)
                found.append({"identifier_type": identifier_type, "value": value})
    return found


def haversine_km(first_location_id: str, second_location_id: str) -> float | None:
    first = LOCATIONS.get(first_location_id)
    second = LOCATIONS.get(second_location_id)
    if not first or not second:
        return None
    lat1, lon1 = math.radians(first["latitude"]), math.radians(first["longitude"])
    lat2, lon2 = math.radians(second["latitude"]), math.radians(second["longitude"])
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    value = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    return 6371.0 * 2 * math.atan2(math.sqrt(value), math.sqrt(1 - value))


def resolve_entity(arguments: dict[str, Any]) -> dict[str, Any]:
    query = str(arguments.get("query") or "").strip()
    matches = entity_matches(query)
    actor_counts = Counter(event_entity_name(event) for event in visible_events())
    for match in matches:
        match["event_counts_by_alias"] = {
            alias: actor_counts[alias] for alias in match["aliases"] if actor_counts[alias]
        }
        for relationship in match.get("relationships", []):
            related = ENTITY_PRESENTATIONS.get(relationship["entity_id"], {})
            relationship["canonical_name"] = related.get("canonical_name")
    return {"query": query, "matches": matches, "entity_layers": matches, "match_count": len(matches)}


def intent_defaults(intent: str, has_geo: bool = False, has_timeline: bool = False) -> dict[str, Any]:
    if intent == "investigation":
        intent = "investigation"
        recommended_mode = "investigation"
        confidence = "גבוהה"
        tool_budget = 30
        allowed = [
            "resolve", "search", "semantic_search", "aggregate", "get", "trace_identifier", "trace_semantic_clues",
            "related_expansion", "linkage", "hypothesis_challenge", "sequence",
        ]
        blocked = []
        view_hint = "timeline" if has_timeline else "map" if has_geo else "evidence"
        reason = "השאלה מבקשת דפוס, קשר, תרחיש, חלופות או הסבר חקירתי."
    elif intent == "geographic_aggregation":
        intent = "geographic_aggregation"
        recommended_mode = "retrieval"
        confidence = "גבוהה"
        tool_budget = 3
        allowed = ["resolve", "search", "semantic_search", "aggregate", "get"]
        blocked = ["related_expansion", "hypothesis_challenge", "linkage"]
        view_hint = "map"
        reason = "השאלה מבקשת הצגה או ספירה לפי מיקום, ללא בקשת קשרים נסתרים."
    elif intent == "timeline_retrieval":
        intent = "timeline_retrieval"
        recommended_mode = "retrieval"
        confidence = "בינונית-גבוהה"
        tool_budget = 4
        allowed = ["resolve", "search", "semantic_search", "get", "sequence"]
        blocked = ["related_expansion", "hypothesis_challenge", "linkage"]
        view_hint = "timeline"
        reason = "השאלה מבקשת סדר או עיתוי של אירועים קיימים."
    elif intent == "retrieval":
        intent = "retrieval"
        recommended_mode = "retrieval"
        confidence = "גבוהה"
        tool_budget = 3
        allowed = ["resolve", "search", "semantic_search", "aggregate", "get"]
        blocked = ["related_expansion", "hypothesis_challenge", "linkage"]
        view_hint = "evidence"
        reason = "השאלה מבקשת שליפה, סינון, צמצום או ספירה של רשומות קיימות."
    else:
        intent = "retrieval"
        recommended_mode = "retrieval"
        confidence = "בינונית"
        tool_budget = 3
        allowed = ["resolve", "search", "semantic_search", "aggregate", "get"]
        blocked = ["related_expansion", "hypothesis_challenge", "linkage"]
        view_hint = "evidence"
        reason = "לא נמצאה בקשה מפורשת לחקירה עמוקה; ברירת המחדל היא שליפה זהירה."
    return {
        "intent": intent,
        "recommended_mode": recommended_mode,
        "confidence": confidence,
        "reason": reason,
        "tool_budget": tool_budget,
        "allowed_tool_families": allowed,
        "blocked_tool_families": blocked,
        "recommended_view_hint": view_hint,
    }


def deterministic_intent_fallback(question: str, context: str = "") -> dict[str, Any]:
    text = normalize_text(f"{question} {context}")

    investigation_terms = [
        "דפוס", "קשרים נסתרים", "קשר נסתר", "חשוד", "חשודה", "חשד", "חקור", "חקירה",
        "הסברים חלופיים", "חלופות", "גורמים משותפים", "אירועים מקדימים", "תחילת",
        "מקור התרחיש", "תרחיש", "רכיב מרכזי", "האם הוא חלק",
        "למה", "הסבר", "סיבתי", "גורם", "חוליה", "שרשרת",
        "רעש מידע", "אמיתי", "אמיתיים", "אמיתית", "אמינות", "ודאות",
        "מאומת", "מאומתים", "לא מאומת", "לא מאומתים",
    ]
    retrieval_terms = [
        "תראה", "הצג", "הראה", "רשימה", "כל האירועים", "אירועים סביב", "תצמצם",
        "סנן", "כמה", "כמות", "top", "טופ", "מיקומים", "לפי", "רשומות", "אירועים של",
        "סביב", "הגעת", "מטענים", "מקורות", "טבלה",
    ]
    geographic_terms = ["מפה", "איפה", "מיקומים", "מוקדים", "מקבצים", "אזורים", "top 3", "טופ 3"]
    timeline_terms = [
        "ציר זמן", "סדר זמן", "סדר לפי זמן", "סדר כרונולוגי", "כרונולוג",
        "לפי זמן", "מיין לפי זמן", "תמיין לפי זמן", "מיון לפי זמן",
        "רצף לפי זמן", "רצף זמן", "עיתוי", "לפני", "אחרי", "מתי", "שעה",
    ]

    has_investigation = any(term in text for term in investigation_terms)
    has_retrieval = any(term in text for term in retrieval_terms)
    has_geo = any(term in text for term in geographic_terms)
    has_timeline = any(term in text for term in timeline_terms)

    if has_investigation:
        return intent_defaults("investigation", has_geo=has_geo, has_timeline=has_timeline)
    if has_geo:
        return intent_defaults("geographic_aggregation")
    if has_timeline:
        return intent_defaults("timeline_retrieval")
    if has_retrieval:
        return intent_defaults("retrieval")
    return intent_defaults("default")


def classify_with_sampling(question: str, context: str = "") -> dict[str, Any] | None:
    if not CLIENT_SUPPORTS_SAMPLING:
        return None
    request_id = next_server_request_id()
    user_text = f"שאלת האנליסט: {question}"
    if context:
        user_text += f"\nהקשר שיחה קצר: {context}"
    system_prompt = (
        "אתה מסווג כוונת שאלת אנליסט עבור מערכת חקירה מודיעינית. "
        "החזר JSON תקין בלבד, ללא טקסט נוסף. "
        "שדות חובה: intent, recommended_mode, recommended_view_hint, confidence, reason. "
        "intent חייב להיות אחד מ: retrieval, geographic_aggregation, timeline_retrieval, investigation. "
        "recommended_mode חייב להיות retrieval או investigation. "
        "recommended_view_hint חייב להיות map, timeline או evidence. "
        "כללים: אם האנליסט מבקש למיין, לסדר, לשחזר התרחשות או לקבל תמונה לפי זמן, בחר timeline_retrieval ו-timeline. "
        "אם הוא מבקש מוקדים, איפה, אזורים, מקבצים או TOP מיקומים, בחר geographic_aggregation ו-map. "
        "אם הוא מבקש רשימה, סינון, הצגה או צמצום של רשומות, בחר retrieval. "
        "אם הוא מבקש הסבר, מה באמת קרה, דפוס, קשרים, חלופות, אמינות, רעש מידע או תרחיש מתגלגל, בחר investigation. "
        "אם זו חקירה אך הליבה היא שחזור סדר ההתרחשות, השאר intent=investigation אבל בחר recommended_view_hint=timeline. "
        "reason יהיה משפט עברי קצר אחד."
    )
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "sampling/createMessage",
        "params": {
            "systemPrompt": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": {"type": "text", "text": user_text},
                }
            ],
            "maxTokens": 220,
            "temperature": 0,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), flush=True)
    deadline = time.time() + 20
    while time.time() < deadline:
        line = sys.stdin.readline()
        if not line:
            return None
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if message.get("id") != request_id:
            continue
        if "error" in message:
            return None
        result = message.get("result") or {}
        content = result.get("content")
        text = ""
        if isinstance(content, dict):
            text = str(content.get("text") or "")
        elif isinstance(content, list):
            text = "\n".join(str(item.get("text") or "") for item in content if isinstance(item, dict))
        if not text:
            text = str(result.get("text") or "")
        parsed = extract_json_object(text)
        return parsed or None
    return None


def classify_question_intent(arguments: dict[str, Any]) -> dict[str, Any]:
    question = str(arguments.get("question") or "").strip()
    context = str(arguments.get("conversation_context") or "").strip()
    valid_intents = {"retrieval", "geographic_aggregation", "timeline_retrieval", "investigation"}
    valid_modes = {"retrieval", "investigation"}
    valid_views = {"map", "timeline", "evidence"}
    sampled = classify_with_sampling(question, context)
    model_intent = str((sampled or {}).get("intent") or arguments.get("model_intent") or "").strip()
    model_mode = str((sampled or {}).get("recommended_mode") or arguments.get("model_recommended_mode") or "").strip()
    model_view = str((sampled or {}).get("recommended_view_hint") or arguments.get("model_recommended_view_hint") or "").strip()
    model_confidence = str((sampled or {}).get("confidence") or arguments.get("model_confidence") or "").strip()
    model_reason = str((sampled or {}).get("reason") or arguments.get("model_reason") or "").strip()
    source = "mcp_sampling" if sampled else "model_override"

    if model_intent in valid_intents:
        defaults = intent_defaults(model_intent)
        intent = model_intent
        recommended_mode = model_mode if model_mode in valid_modes else defaults["recommended_mode"]
        confidence = model_confidence or defaults["confidence"]
        reason = model_reason or defaults["reason"]
        tool_budget = defaults["tool_budget"]
        allowed = defaults["allowed_tool_families"]
        blocked = defaults["blocked_tool_families"]
        view_hint = model_view if model_view in valid_views else defaults["recommended_view_hint"]
        if recommended_mode == "investigation" and tool_budget < 30:
            tool_budget = 30
        if recommended_mode == "retrieval" and intent == "timeline_retrieval":
            tool_budget = 4
    else:
        fallback = deterministic_intent_fallback(question, context)
        intent = fallback["intent"]
        recommended_mode = fallback["recommended_mode"]
        confidence = fallback["confidence"]
        reason = fallback["reason"]
        tool_budget = fallback["tool_budget"]
        allowed = fallback["allowed_tool_families"]
        blocked = fallback["blocked_tool_families"]
        view_hint = fallback["recommended_view_hint"]
        source = "deterministic_fallback"

    return {
        "question": question,
        "intent": intent,
        "recommended_mode": recommended_mode,
        "confidence": confidence,
        "reason": reason,
        "tool_budget": tool_budget,
        "allowed_tool_families": allowed,
        "blocked_tool_families": blocked,
        "recommended_view_hint": view_hint,
        "classification_source": source,
        "counts_as_data_query": False,
    }


def plan_next_investigation_step(arguments: dict[str, Any]) -> dict[str, Any]:
    objective = str(arguments.get("objective") or "").strip()
    candidate_chain = [str(item) for item in arguments.get("candidate_chain_event_ids") or [] if str(item)]
    pending_seeds = [str(item) for item in arguments.get("pending_recommended_seeds") or [] if str(item)]
    expanded_seeds = {str(item) for item in arguments.get("expanded_seed_event_ids") or [] if str(item)}
    new_clues = [str(item) for item in arguments.get("new_clues_to_trace") or [] if str(item)]
    linkage_checks = {
        tuple(item)
        for item in arguments.get("linkage_checks_done") or []
        if isinstance(item, list) and len(item) == 2
    }
    semantic_calls_used = int(arguments.get("semantic_calls_used") or 0)
    related_calls_used = int(arguments.get("related_calls_used") or 0)
    tool_budget_remaining = int(arguments.get("tool_budget_remaining") or 0)

    unexpanded_seeds = [event_id for event_id in pending_seeds if event_id not in expanded_seeds][:3]
    unchecked_pairs = []
    for first, second in zip(candidate_chain, candidate_chain[1:]):
        if (first, second) not in linkage_checks and (second, first) not in linkage_checks:
            unchecked_pairs.append([first, second])

    if unexpanded_seeds:
        decision = "continue"
        next_step_constraint = "expand_pending_recommended_seeds"
        required_event_ids = unexpanded_seeds
        allowed = ["get_objects", "find_related_events", "trace_semantic_clues", "semantic_search_events", "explain_linkage"]
        blocked = ["challenge_hypothesis", "final_summary"]
        reason = "קיימים seeds מומלצים שעדיין לא הורחבו; אין לסכם או לאתגר השערה לפני טיפול בהם."
    elif new_clues and semantic_calls_used < 2:
        decision = "continue"
        next_step_constraint = "trace_new_clues"
        required_event_ids = []
        allowed = ["trace_semantic_clues", "semantic_search_events", "search_events"]
        blocked = ["challenge_hypothesis", "final_summary"]
        reason = "קיימים רמזים סמנטיים חדשים שעדיין לא נבדקו, ועדיין יש תקציב קריאות סמנטיות."
    elif unchecked_pairs:
        decision = "continue"
        next_step_constraint = "check_adjacent_linkage"
        required_event_ids = [event_id for pair in unchecked_pairs[:3] for event_id in pair]
        allowed = ["explain_linkage"]
        blocked = ["final_summary"]
        reason = "קיימות חוליות סמוכות בשרשרת המועמדת ללא בדיקת גשר ראייתי."
    elif len(candidate_chain) < 5 and tool_budget_remaining > 3 and related_calls_used < 4:
        decision = "continue"
        next_step_constraint = "continue_bounded_expansion"
        required_event_ids = candidate_chain[-3:] if candidate_chain else []
        allowed = ["find_related_events", "trace_semantic_clues", "semantic_search_events", "search_events"]
        blocked = ["challenge_hypothesis", "final_summary"]
        reason = "השרשרת עדיין קצרה ויש תקציב להרחבה מוגבלת לפני מסקנה."
    elif len(candidate_chain) >= 5:
        decision = "continue"
        next_step_constraint = "challenge_or_summarize_with_gaps"
        required_event_ids = candidate_chain[:20]
        allowed = ["challenge_hypothesis", "build_event_sequence", "get_objects"]
        blocked = []
        reason = "קיימת שרשרת מועמדת מספקת או שה-frontier מוצה; מותר לבצע ביקורת השערה או סיכום עם פערים."
    else:
        decision = "stop"
        next_step_constraint = "summarize_with_gaps"
        required_event_ids = candidate_chain[:20]
        allowed = ["build_event_sequence", "get_objects"]
        blocked = []
        reason = "אין frontier מחייב נוסף או תקציב הרחבה משמעותי; יש לסכם את הפערים בלי להציג קשר לא מוכח."

    return {
        "objective": objective,
        "decision": decision,
        "next_step_constraint": next_step_constraint,
        "required_event_ids": required_event_ids,
        "required_clues": new_clues[:8] if next_step_constraint == "trace_new_clues" else [],
        "allowed_tool_families": allowed,
        "blocked_tool_families": blocked,
        "final_summary_allowed": "final_summary" not in blocked,
        "challenge_hypothesis_allowed": "challenge_hypothesis" not in blocked,
        "reason": reason,
        "state_summary": {
            "candidate_chain_length": len(candidate_chain),
            "pending_recommended_seed_count": len(pending_seeds),
            "unexpanded_recommended_seed_count": len(unexpanded_seeds),
            "new_clue_count": len(new_clues),
            "unchecked_adjacent_pair_count": len(unchecked_pairs),
            "tool_budget_remaining": tool_budget_remaining,
        },
    }


def trace_identifier(arguments: dict[str, Any]) -> dict[str, Any]:
    identifier = str(arguments.get("identifier") or "").strip()
    identifier_type = arguments.get("identifier_type")
    include_negated = bool(arguments.get("include_negated", False))
    start = parse_time(arguments.get("start_time"))
    end = parse_time(arguments.get("end_time"))
    location_ids = set(arguments.get("location_ids") or [])
    source_types = set(arguments.get("source_types") or [])
    folded = normalize_text(identifier)
    mentions = []
    for event in visible_events():
        if start and event["timestamp"] < start:
            continue
        if end and event["timestamp"] > end:
            continue
        if location_ids and event["location_id"] not in location_ids:
            continue
        if source_types and event["source_type"] not in source_types:
            continue
        if normalize_text(event["event_id"]) == folded and (not identifier_type or identifier_type == "record"):
            mentions.append({
                "event": event,
                "mention_type": "direct",
                "matched_identifiers": [{"identifier_type": "record", "value": event["event_id"]}],
            })
            continue
        extracted = extract_identifiers(event["event_summary"])
        matching = [
            item for item in extracted
            if normalize_text(item["value"]) == folded and (not identifier_type or item["identifier_type"] == identifier_type)
        ]
        if matching:
            negated = any(marker in event["event_summary"] for marker in NEGATION_MARKERS)
            mentions.append({
                "event": event,
                "mention_type": "negated" if negated else "direct",
                "matched_identifiers": matching,
            })
    selected = [mention for mention in mentions if include_negated or mention["mention_type"] != "negated"]
    return {
        "identifier": identifier,
        "identifier_type": identifier_type,
        "include_negated": include_negated,
        "start_time": arguments.get("start_time"),
        "end_time": arguments.get("end_time"),
        "location_ids": sorted(location_ids),
        "source_types": sorted(source_types),
        "event_ids": [mention["event"]["event_id"] for mention in selected],
        "events": [
            {**public_event(mention["event"]), "mention_type": mention["mention_type"]}
            for mention in selected
        ],
        "total_mentions": len(mentions),
        "returned": len(selected),
        "excluded_negated_mentions": sum(mention["mention_type"] == "negated" for mention in mentions) if not include_negated else 0,
    }


def trace_semantic_clues(arguments: dict[str, Any]) -> dict[str, Any]:
    clues = [str(value).strip() for value in arguments.get("clues") or [] if str(value).strip()]
    seed_ids = arguments.get("seed_event_ids") or []
    seed_events = [event for event_id in seed_ids if (event := visible_event(event_id)) is not None]
    for event in seed_events:
        for clue in semantic_clues_from_text(event["event_summary"]):
            if clue not in clues:
                clues.append(clue)
    llm_expansion = sample_json_task(
        "trace_semantic_clues_expand",
        (
            "אתה עוזר לכלי חיפוש סמנטי במאגר מודיעיני. "
            "החזר JSON תקין בלבד עם השדות expanded_clues ו-rationale. "
            "expanded_clues תהיה רשימה של עד 10 ביטויי חיפוש קצרים בעברית/שם מקור, "
            "רק ביטויים שנובעים במפורש מהרמזים או מתקצירי ה-seeds. "
            "אל תמציא ישויות או אירועים ספציפיים שלא הופיעו בקלט."
        ),
        {
            "input_clues": clues[:20],
            "seed_events": [public_event(event) for event in seed_events[:5]],
        },
        max_tokens=500,
    )
    llm_expanded_clues = string_list((llm_expansion or {}).get("expanded_clues"), limit=10)
    start = parse_time(arguments.get("start_time"))
    end = parse_time(arguments.get("end_time"))
    location_ids = set(arguments.get("location_ids") or [])
    source_types = set(arguments.get("source_types") or [])
    include_negated = bool(arguments.get("include_negated", False))
    requested_limit = arguments.get("limit", MAX_LIMIT)
    limit = coverage_limit(requested_limit)
    active_clues = list(dict.fromkeys(clues + llm_expanded_clues))
    normalized_clues = [(clue, normalize_text(clue)) for clue in active_clues]
    semantic_query_parts = active_clues[:30] + [event["event_summary"] for event in seed_events[:5]]
    semantic_query = "\n".join(part for part in semantic_query_parts if part)
    semantic_matches = semantic_candidates(semantic_query, arguments, limit)
    semantic_by_id = {match["event_id"]: match for match in semantic_matches if match.get("event_id")}
    matches_by_id: dict[str, dict[str, Any]] = {}
    for event in visible_events():
        if start and event["timestamp"] < start:
            continue
        if end and event["timestamp"] > end:
            continue
        if location_ids and event["location_id"] not in location_ids:
            continue
        if source_types and event["source_type"] not in source_types:
            continue
        haystack = normalize_text(" ".join([event["event_summary"], event_entity_name(event), event["location_name"]]))
        matched_clues = [clue for clue, folded in normalized_clues if folded and term_in_text(folded, haystack)]
        if not matched_clues:
            continue
        negated = event_has_negation(event)
        if negated and not include_negated:
            continue
        score = len(matched_clues) * 4
        semantic_match = semantic_by_id.get(event["event_id"])
        if semantic_match:
            score += min(4, max(1, int(float(semantic_match.get("semantic_score") or 0) * 10)))
        if any(marker in event["event_summary"] for marker in DIRECT_OBSERVATION_MARKERS):
            score += 1
        if negated:
            score -= 4
        if any(marker in event["event_summary"] for marker in BENIGN_MARKERS):
            score -= 2
        matches_by_id[event["event_id"]] = {
            "score": score,
            "matched_clues": matched_clues,
            "mention_type": "negated" if negated else "direct",
            "semantic_score": round(float(semantic_match.get("semantic_score") or 0), 6) if semantic_match else 0,
            "semantic_rationale": semantic_match.get("rationale") if semantic_match else "",
            "match_source": "direct_and_semantic" if semantic_match else "direct_clue",
            "event": public_event(event),
        }
    for match in semantic_matches:
        event_id = match.get("event_id")
        if not event_id or event_id in matches_by_id:
            continue
        event = visible_event(event_id)
        if not event:
            continue
        negated = event_has_negation(event)
        if negated and not include_negated:
            continue
        event_clues = semantic_clues_from_text(event["event_summary"])
        matched_clues = [clue for clue in event_clues if clue in active_clues] or ["semantic_similarity"]
        score = min(6, max(2, int(float(match.get("semantic_score") or 0) * 12)))
        if any(marker in event["event_summary"] for marker in DIRECT_OBSERVATION_MARKERS):
            score += 1
        if negated:
            score -= 4
        if any(marker in event["event_summary"] for marker in BENIGN_MARKERS):
            score -= 2
        if score < 2:
            continue
        matches_by_id[event_id] = {
            "score": score,
            "matched_clues": matched_clues,
            "mention_type": "negated" if negated else "semantic",
            "semantic_score": round(float(match.get("semantic_score") or 0), 6),
            "semantic_rationale": match.get("rationale") or "",
            "match_source": "semantic_candidate",
            "event": public_event(event),
        }
    matches = list(matches_by_id.values())
    matches.sort(key=lambda item: (-item["score"], item["event"]["timestamp_utc"], item["event"]["event_id"]))
    selected = matches[:limit]
    seed_id_set = {event["event_id"] for event in seed_events}
    ranked_seeds = []
    for item in selected:
        event_id = item["event"]["event_id"]
        if event_id in seed_id_set:
            continue
        event = visible_event(event_id)
        if not event:
            continue
        seed_score, reasons = investigative_seed_score(event, item.get("matched_clues") or [])
        if seed_score < 12:
            continue
        ranked_seeds.append({
            "event_id": event_id,
            "score": seed_score,
            "reasons": reasons,
            "matched_clues": item.get("matched_clues") or [],
            "event": item["event"],
        })
    ranked_seeds.sort(key=lambda item: (-item["score"], item["event"]["timestamp_utc"], item["event_id"]))
    recommended_next_seeds = ranked_seeds[:3]
    new_clues = []
    for seed in recommended_next_seeds:
        event = visible_event(seed["event_id"])
        if not event:
            continue
        for clue in semantic_clues_from_text(event["event_summary"]):
            if clue not in clues and clue not in new_clues:
                new_clues.append(clue)
    return {
        "clues": clues,
        "seed_event_ids": [event["event_id"] for event in seed_events],
        "missing_seed_event_ids": [event_id for event_id in seed_ids if visible_event(event_id) is None],
        "include_negated": include_negated,
        "start_time": arguments.get("start_time"),
        "end_time": arguments.get("end_time"),
        "location_ids": sorted(location_ids),
        "source_types": sorted(source_types),
        "event_ids": [item["event"]["event_id"] for item in selected],
        "matches": selected,
        "total_matches": len(matches),
        "semantic_candidate_count": len(semantic_matches),
        "semantic_backend": get_semantic_index().backend if semantic_matches else None,
        "returned": len(selected),
        "truncated": len(matches) > len(selected),
        "requested_limit": requested_limit,
        "effective_limit": limit,
        "coverage_policy": "max_coverage_default",
        "recommended_next_seeds": recommended_next_seeds,
        "new_clues_to_trace": list(dict.fromkeys(new_clues + llm_expanded_clues))[:8],
        "llm_expanded_clues": llm_expanded_clues,
        "llm_expansion_rationale": str((llm_expansion or {}).get("rationale") or "")[:500],
        "llm_assist_source": "mcp_sampling" if llm_expansion else "not_available",
    }


def find_related_events(arguments: dict[str, Any]) -> dict[str, Any]:
    seed_ids = arguments.get("seed_event_ids") or []
    seeds = [event for event_id in seed_ids if (event := visible_event(event_id)) is not None]
    if not seeds:
        return {"seed_event_ids": seed_ids, "missing_seed_event_ids": seed_ids, "related_events": [], "event_ids": []}
    dimensions = set(arguments.get("dimensions") or ["entity", "identifier", "semantic", "time", "location"])
    before_hours = max(0, min(float(arguments.get("before_hours", 24)), 168))
    after_hours = max(0, min(float(arguments.get("after_hours", 12)), 168))
    distance_km = max(0, min(float(arguments.get("distance_km", 25)), 500))
    source_types = set(arguments.get("source_types") or [])
    requested_limit = arguments.get("limit", MAX_LIMIT)
    limit = coverage_limit(requested_limit)
    informative_seed_actors = [event_entity_name(seed) for seed in seeds if is_informative_actor(event_entity_name(seed))]
    seed_entities = set().union(*(canonical_entity_ids(actor) for actor in informative_seed_actors))
    seed_identifiers = {
        (item["identifier_type"], normalize_text(item["value"]))
        for seed in seeds for item in extract_identifiers(seed["event_summary"])
    }
    seed_semantic_clues = set().union(*(set(semantic_clues_from_text(seed["event_summary"])) for seed in seeds))
    earliest = min(seed["timestamp"] for seed in seeds) - timedelta(hours=before_hours)
    latest = max(seed["timestamp"] for seed in seeds) + timedelta(hours=after_hours)
    semantic_related_matches: list[dict[str, Any]] = []
    if "semantic" in dimensions:
        semantic_query = "\n".join(
            list(sorted(seed_semantic_clues))[:20] + [seed["event_summary"] for seed in seeds[:5]]
        )
        semantic_related_matches = semantic_candidates(
            semantic_query,
            {
                **arguments,
                "start_time": earliest.isoformat().replace("+00:00", "Z"),
                "end_time": latest.isoformat().replace("+00:00", "Z"),
                "source_types": list(source_types),
            },
            limit,
        )
    semantic_related_by_id = {
        match["event_id"]: match
        for match in semantic_related_matches
        if match.get("event_id") and match.get("event_id") not in seed_ids
    }
    ranked = []
    for event in visible_events():
        if event["event_id"] in seed_ids or event["timestamp"] < earliest or event["timestamp"] > latest:
            continue
        if source_types and event["source_type"] not in source_types:
            continue
        score = 0.0
        reasons = []
        if "identifier" in dimensions:
            identifiers = {
                (item["identifier_type"], normalize_text(item["value"]))
                for item in extract_identifiers(event["event_summary"])
            }
            shared = seed_identifiers & identifiers
            if shared:
                score += 8
                reasons.append({"dimension": "identifier", "detail": ", ".join(value for _, value in sorted(shared)), "weight": 8})
        if "entity" in dimensions and is_informative_actor(event_entity_name(event)):
            event_entities = canonical_entity_ids(event_entity_name(event))
            if seed_entities & event_entities:
                shared_entity_ids = sorted(seed_entities & event_entities)
                score += 6
                reasons.append({
                    "dimension": "entity",
                    "detail": ", ".join(
                        f"{entity_id} ({ENTITY_PRESENTATIONS.get(entity_id, {}).get('canonical_name') or entity_id})"
                        for entity_id in shared_entity_ids
                    ),
                    "weight": 6,
                })
            elif any(is_informative_actor(event_entity_name(seed)) and event_entity_name(event) == event_entity_name(seed) for seed in seeds):
                score += 4
                reasons.append({"dimension": "entity", "detail": "שם גורם זהה", "weight": 4})
        event_semantic_clues = set(semantic_clues_from_text(event["event_summary"]))
        shared_semantic = seed_semantic_clues & event_semantic_clues
        if "semantic" in dimensions and shared_semantic:
            semantic_weight = 4 if len(shared_semantic) >= 2 else 2
            score += semantic_weight
            reasons.append({
                "dimension": "semantic",
                "detail": ", ".join(sorted(shared_semantic)),
                "weight": semantic_weight,
            })
        semantic_match = semantic_related_by_id.get(event["event_id"])
        if "semantic" in dimensions and semantic_match:
            semantic_score = float(semantic_match.get("semantic_score") or 0)
            semantic_weight = 3 if semantic_score >= 0.12 else 2 if semantic_score >= 0.06 else 1
            score += semantic_weight
            reasons.append({
                "dimension": "semantic_embedding",
                "detail": semantic_match.get("rationale") or "hybrid semantic similarity to seed events",
                "weight": semantic_weight,
                "semantic_score": round(semantic_score, 6),
            })
        nearest_hours = min(abs((event["timestamp"] - seed["timestamp"]).total_seconds()) / 3600 for seed in seeds)
        if "time" in dimensions:
            time_weight = 3 if nearest_hours <= 2 else 2 if nearest_hours <= 6 else 1 if nearest_hours <= 24 else 0
            if time_weight:
                score += time_weight
                reasons.append({"dimension": "time", "detail": f"מרחק זמן מינימלי {nearest_hours:.1f} שעות", "weight": time_weight})
        if "location" in dimensions:
            distances = [haversine_km(event["location_id"], seed["location_id"]) for seed in seeds]
            valid_distances = [distance for distance in distances if distance is not None]
            nearest_distance = min(valid_distances) if valid_distances else None
            if nearest_distance is not None and nearest_distance <= distance_km:
                location_weight = 3 if nearest_distance < 1 else 2 if nearest_distance <= 10 else 1
                score += location_weight
                reasons.append({"dimension": "location", "detail": f"מרחק מינימלי {nearest_distance:.1f} קמ", "weight": location_weight})
        if any(marker in event["event_summary"] for marker in BENIGN_MARKERS):
            score -= 3
            reasons.append({"dimension": "specificity", "detail": "הרשומה מסומנת כהסבר שגרתי או תמים", "weight": -3})
        elif any(marker in event["event_summary"] for marker in DIRECT_OBSERVATION_MARKERS):
            score += 1
            reasons.append({"dimension": "specificity", "detail": "תיאור של פעולה או תצפית קונקרטית", "weight": 1})
        if score >= 3:
            ranked.append({"score": score, "reasons": reasons, "event": public_event(event)})
    ranked.sort(key=lambda item: (-item["score"], item["event"]["timestamp_utc"]))
    selected = ranked[:limit]
    llm_rerank = None
    if selected:
        llm_rerank = sample_json_task(
            "find_related_events_rerank",
            (
                "אתה מדרג מועמדים להרחבת חקירה מודיעינית. "
                "החזר JSON תקין בלבד עם top_event_ids ו-rationale. "
                "top_event_ids תהיה רשימה של עד 12 event_id מתוך candidate_events בלבד. "
                "דרג לפי חוזק גשר ראייתי, המשכיות תפעולית, מקור/אמינות, והימנעות מרעש או הסבר תמים. "
                "אסור להוסיף מזהים שאינם בקלט."
            ),
            {
                "seed_events": [public_event(seed) for seed in seeds[:5]],
                "candidate_events": [
                    {
                        "event_id": item["event"]["event_id"],
                        "timestamp_utc": item["event"]["timestamp_utc"],
                        "source_type": item["event"]["source_type"],
                        "certainty_level": item["event"].get("certainty_level", ""),
                        "source_reliability_label": item["event"].get("source_reliability_label", ""),
                        "entity_id": item["event"].get("entity_id"),
                        "entity_name": item["event"].get("entity_name"),
                        "location_name": item["event"]["location_name"],
                        "event_summary": item["event"]["event_summary"],
                        "deterministic_score": item["score"],
                        "reasons": item["reasons"][:5],
                    }
                    for item in selected[:40]
                ],
            },
            max_tokens=700,
        )
        top_ids = [
            event_id
            for event_id in string_list((llm_rerank or {}).get("top_event_ids"), limit=12)
            if event_id in {item["event"]["event_id"] for item in selected}
        ]
        if top_ids:
            rank = {event_id: index for index, event_id in enumerate(top_ids)}
            selected.sort(
                key=lambda item: (
                    0 if item["event"]["event_id"] in rank else 1,
                    rank.get(item["event"]["event_id"], 999),
                    -item["score"],
                    item["event"]["timestamp_utc"],
                )
            )
    ranked_seeds = []
    for item in selected:
        event_id = item["event"]["event_id"]
        event = visible_event(event_id)
        if not event:
            continue
        seed_score, seed_reasons = investigative_seed_score(event)
        linkage_reasons = item.get("reasons") or []
        strong_link_count = sum(1 for reason in linkage_reasons if reason.get("weight", 0) >= 3)
        seed_score += min(strong_link_count, 3) * 2
        if seed_score < 12:
            continue
        ranked_seeds.append({
            "event_id": event_id,
            "score": seed_score,
            "reasons": seed_reasons[:4] + [f"נמצא בהרחבה עם {len(linkage_reasons)} נימוקי קשר"],
            "linkage_reasons": linkage_reasons[:4],
            "event": item["event"],
        })
    ranked_seeds.sort(key=lambda item: (-item["score"], item["event"]["timestamp_utc"], item["event_id"]))
    recommended_next_seeds = ranked_seeds[:3]
    new_clues = []
    for seed in recommended_next_seeds:
        event = visible_event(seed["event_id"])
        if not event:
            continue
        for clue in semantic_clues_from_text(event["event_summary"]):
            if clue not in new_clues:
                new_clues.append(clue)
    return {
        "seed_event_ids": [seed["event_id"] for seed in seeds],
        "missing_seed_event_ids": [event_id for event_id in seed_ids if visible_event(event_id) is None],
        "dimensions": sorted(dimensions),
        "source_types": sorted(source_types),
        "related_events": selected,
        "event_ids": [item["event"]["event_id"] for item in selected],
        "total_candidates": len(ranked),
        "semantic_candidate_count": len(semantic_related_matches),
        "semantic_backend": get_semantic_index().backend if semantic_related_matches else None,
        "returned": len(selected),
        "truncated": len(ranked) > len(selected),
        "requested_limit": requested_limit,
        "effective_limit": limit,
        "coverage_policy": "max_coverage_default",
        "recommended_next_seeds": recommended_next_seeds,
        "new_clues_to_trace": new_clues[:8],
        "llm_rerank": {
            "top_event_ids": string_list((llm_rerank or {}).get("top_event_ids"), limit=12),
            "rationale": str((llm_rerank or {}).get("rationale") or "")[:700],
            "source": "mcp_sampling" if llm_rerank else "not_available",
        },
    }


GEO_CONFLICT_MARKERS = (
    "סרטון", "תמונה", "צולם", "מוצג כאילו", "לא נראה מהיום", "ישן",
    "אינו קשור", "מקורות אחרים", "מכחישים", "אין לכך אימות", "אין מקור רשמי",
    "לא אומת", "מתייחס לאירוע קודם", "ניסוח דומה", "חשבונות בוט",
)


def location_claim_template(event: dict[str, Any]) -> str:
    text = event["event_summary"]
    location_names = sorted(
        {
            str(location.get("name") or "")
            for location in LOCATIONS.values()
            if len(str(location.get("name") or "")) >= 4
        }
        | {
            str(location.get("municipality") or "")
            for location in LOCATIONS.values()
            if len(str(location.get("municipality") or "")) >= 4
        },
        key=len,
        reverse=True,
    )
    normalized = text
    for name in location_names:
        normalized = normalized.replace(name, "<מיקום>")
    normalized = re.sub(r"\d+", "<מספר>", normalized)
    return normalize_text(normalized)


def compare_location_claims(arguments: dict[str, Any]) -> dict[str, Any]:
    seed_ids = arguments.get("seed_event_ids") or []
    seed_events = [event for event_id in seed_ids if (event := visible_event(event_id)) is not None]
    keywords = [str(value).strip() for value in arguments.get("keywords") or [] if str(value).strip()]
    start = parse_time(arguments.get("start_time"))
    end = parse_time(arguments.get("end_time"))
    location_ids = set(arguments.get("location_ids") or [])
    source_types = set(arguments.get("source_types") or [])
    requested_limit = arguments.get("limit", 100)
    limit = coverage_limit(requested_limit)
    if seed_events:
        window_hours = max(1, min(float(arguments.get("time_window_hours", 24)), 168))
        if not start:
            start = min(event["timestamp"] for event in seed_events) - timedelta(hours=window_hours)
        if not end:
            end = max(event["timestamp"] for event in seed_events) + timedelta(hours=window_hours)
        for event in seed_events:
            for clue in semantic_clues_from_text(event["event_summary"]):
                if clue not in keywords:
                    keywords.append(clue)

    normalized_keywords = [normalize_text(keyword) for keyword in keywords]
    candidates = []
    for event in visible_events():
        if start and event["timestamp"] < start:
            continue
        if end and event["timestamp"] > end:
            continue
        if location_ids and event["location_id"] not in location_ids:
            continue
        if source_types and event["source_type"] not in source_types:
            continue
        haystack = normalize_text(" ".join([event["event_summary"], event_entity_name(event), event["location_name"], event["source_type"]]))
        matched_keywords = [keyword for keyword, folded in zip(keywords, normalized_keywords) if folded and term_in_text(folded, haystack)]
        markers = [marker for marker in GEO_CONFLICT_MARKERS if marker in event["event_summary"]]
        if keywords and not matched_keywords:
            continue
        if not keywords and not markers:
            continue
        candidates.append({
            "event": event,
            "template": location_claim_template(event),
            "matched_keywords": matched_keywords,
            "markers": markers,
        })

    groups_by_template: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        groups_by_template[candidate["template"]].append(candidate)

    conflict_groups = []
    for template, group in groups_by_template.items():
        if len(group) < 2:
            continue
        locations = {item["event"]["location_id"] for item in group}
        municipalities = {
            LOCATIONS.get(item["event"]["location_id"], {}).get("municipality", "")
            for item in group
        }
        if len(locations) < 2 and len(municipalities) < 2:
            continue
        low_certainty = sum(1 for item in group if item["event"].get("certainty_level") == "נמוכה")
        weak_reliability = sum(
            1 for item in group
            if item["event"].get("source_reliability_label") in {"unverified", "disputed", "false", "propaganda/disinformation"}
        )
        marker_count = sum(len(set(item["markers"])) for item in group)
        source_diversity = len({item["event"]["source_type"] for item in group})
        score = (
            len(locations) * 1.5
            + len(municipalities) * 2.0
            + min(len(group), 20) * 0.25
            + min(low_certainty, 10) * 0.4
            + min(weak_reliability, 10) * 0.35
            + min(marker_count, 12) * 0.5
            + min(source_diversity, 6) * 0.5
        )
        sample = sorted(group, key=lambda item: (item["event"]["timestamp"], item["event"]["event_id"]))[:limit]
        all_markers = sorted({marker for item in group for marker in item["markers"]})
        all_keywords = sorted({keyword for item in group for keyword in item["matched_keywords"]})
        conflict_groups.append({
            "conflict_score": round(score, 3),
            "claim_template": template,
            "event_count": len(group),
            "location_count": len(locations),
            "municipality_count": len(municipalities),
            "source_type_count": source_diversity,
            "low_certainty_count": low_certainty,
            "weak_reliability_count": weak_reliability,
            "markers": all_markers[:12],
            "matched_keywords": all_keywords[:12],
            "locations": [
                {
                    "location_id": location_id,
                    "location_name": LOCATIONS.get(location_id, {}).get("name", location_id),
                    "municipality": LOCATIONS.get(location_id, {}).get("municipality", ""),
                    "count": sum(1 for item in group if item["event"]["location_id"] == location_id),
                }
                for location_id in sorted(locations)
            ][:20],
            "event_ids": [item["event"]["event_id"] for item in sample],
            "events": [public_event(item["event"]) for item in sample],
            "assessment": "חשד לסתירה או הפצה גאוגרפית של אותה טענה; הכלי אינו יודע מה המיקום הנכון ואינו משתמש באמת קרקע.",
        })

    conflict_groups.sort(key=lambda item: (-item["conflict_score"], -item["event_count"], item["claim_template"]))
    selected_groups = conflict_groups[:limit]
    llm_assessment = None
    if selected_groups:
        llm_assessment = sample_json_task(
            "compare_location_claims_assess",
            (
                "אתה מנתח קבוצות של דיווחים עם אפשרות להטעיה או סתירה גאוגרפית. "
                "החזר JSON תקין בלבד עם fields: assessment, strongest_group_indexes, caution. "
                "assessment יהיה עד שלושה משפטים בעברית. strongest_group_indexes תהיה רשימת אינדקסים קיימים בלבד. "
                "הסבר אם הדפוס נראה כמו אותה טענה שמופצת בכמה מקומות, דיווחים לא מאומתים, או פעילות אמיתית מרובת מוקדים. "
                "אין לך אמת קרקע; אסור לקבוע מיקום נכון בוודאות."
            ),
            {
                "groups": [
                    {
                        "index": index,
                        "conflict_score": group["conflict_score"],
                        "event_count": group["event_count"],
                        "location_count": group["location_count"],
                        "municipality_count": group["municipality_count"],
                        "low_certainty_count": group["low_certainty_count"],
                        "weak_reliability_count": group["weak_reliability_count"],
                        "markers": group["markers"],
                        "matched_keywords": group["matched_keywords"],
                        "locations": group["locations"][:8],
                        "sample_events": group["events"][:5],
                    }
                    for index, group in enumerate(selected_groups[:8])
                ]
            },
            max_tokens=700,
        )
    return {
        "seed_event_ids": [event["event_id"] for event in seed_events],
        "missing_seed_event_ids": [event_id for event_id in seed_ids if visible_event(event_id) is None],
        "keywords": keywords,
        "start_time": start.isoformat().replace("+00:00", "Z") if start else None,
        "end_time": end.isoformat().replace("+00:00", "Z") if end else None,
        "location_ids": sorted(location_ids),
        "source_types": sorted(source_types),
        "candidate_event_count": len(candidates),
        "conflict_group_count": len(conflict_groups),
        "returned": len(selected_groups),
        "truncated": len(conflict_groups) > len(selected_groups),
        "requested_limit": requested_limit,
        "effective_limit": limit,
        "coverage_policy": "max_coverage_default",
        "conflict_groups": selected_groups,
        "llm_assessment": {
            "assessment": str((llm_assessment or {}).get("assessment") or "")[:900],
            "strongest_group_indexes": [
                index for index in (llm_assessment or {}).get("strongest_group_indexes", [])
                if isinstance(index, int) and 0 <= index < min(len(selected_groups), 8)
            ],
            "caution": str((llm_assessment or {}).get("caution") or "")[:500],
            "source": "mcp_sampling" if llm_assessment else "not_available",
        },
    }


def challenge_hypothesis(arguments: dict[str, Any]) -> dict[str, Any]:
    hypothesis = str(arguments.get("hypothesis") or "").strip()
    evidence_ids = arguments.get("supporting_event_ids") or []
    evidence = [event for event_id in evidence_ids if (event := visible_event(event_id)) is not None]
    source_types = sorted({event["source_type"] for event in evidence})
    reliabilities = Counter(event["source_reliability"] for event in evidence)
    identifiers = []
    seen_identifiers = set()
    for event in evidence:
        for item in extract_identifiers(event["event_summary"]):
            key = (item["identifier_type"], normalize_text(item["value"]))
            if key not in seen_identifiers:
                seen_identifiers.add(key)
                identifiers.append(item)
    if evidence:
        start = min(event["timestamp"] for event in evidence) - timedelta(hours=12)
        end = max(event["timestamp"] for event in evidence) + timedelta(hours=12)
        locations = {event["location_id"] for event in evidence}
        alternatives = [
            event for event in visible_events()
            if start <= event["timestamp"] <= end
            and event["location_id"] in locations
            and event["event_id"] not in evidence_ids
            and any(marker in event["event_summary"] for marker in BENIGN_MARKERS)
        ][:30]
    else:
        alternatives = []
    direct_count = sum(any(marker in event["event_summary"] for marker in DIRECT_OBSERVATION_MARKERS) for event in evidence)
    gaps = []
    if len(source_types) < 3:
        gaps.append("פחות משלושה סוגי מקור עצמאיים")
    if not identifiers:
        gaps.append("אין מזהה תפעולי משותף שניתן לעקוב אחריו")
    if direct_count == 0:
        gaps.append("אין תצפית ישירה בין הראיות שסופקו")
    if not alternatives:
        gaps.append("לא נמצאו בחלון המצומצם רשומות עם הסבר תמים; יש להרחיב חיפוש")
    llm_challenge = sample_json_task(
        "challenge_hypothesis_reasoning",
        (
            "אתה עוזר לאתגר השערת חקירה מודיעינית בלי להכריע אמת. "
            "החזר JSON תקין בלבד עם competing_hypotheses, disproof_tests, synthesis. "
            "competing_hypotheses תהיה רשימה של עד 4 חלופות קצרות. "
            "disproof_tests תהיה רשימה של עד 5 בדיקות המשך קונקרטיות. "
            "synthesis יהיה עד שלושה משפטים בעברית ויתבסס רק על הראיות, החלופות והפערים שבקלט."
        ),
        {
            "hypothesis": hypothesis,
            "evidence_events": [public_event(event) for event in evidence[:30]],
            "alternative_events": [public_event(event) for event in alternatives[:15]],
            "deterministic_gaps": gaps,
            "evidence_profile": {
                "event_count": len(evidence),
                "source_types": source_types,
                "reliability_counts": dict(reliabilities),
                "direct_observation_count": direct_count,
                "traceable_identifiers": identifiers[:20],
            },
        },
        max_tokens=800,
    )
    return {
        "hypothesis": hypothesis,
        "supporting_event_ids": [event["event_id"] for event in evidence],
        "missing_event_ids": [event_id for event_id in evidence_ids if visible_event(event_id) is None],
        "evidence_profile": {
            "event_count": len(evidence),
            "source_types": source_types,
            "source_type_count": len(source_types),
            "reliability_counts": dict(reliabilities),
            "direct_observation_count": direct_count,
            "traceable_identifiers": identifiers,
        },
        "alternative_event_ids": [event["event_id"] for event in alternatives],
        "alternative_events": [public_event(event) for event in alternatives],
        "gaps": gaps,
        "llm_challenge": {
            "competing_hypotheses": string_list((llm_challenge or {}).get("competing_hypotheses"), limit=4),
            "disproof_tests": string_list((llm_challenge or {}).get("disproof_tests"), limit=5),
            "synthesis": str((llm_challenge or {}).get("synthesis") or "")[:900],
            "source": "mcp_sampling" if llm_challenge else "not_available",
        },
        "assessment_note": "הכלי מתאר חוזק, חלופות ופערים באופן דטרמיניסטי; הסוכן חייב להעריך את ההשערה בעצמו.",
    }


def sort_event_matches(matches: list[tuple[int, dict[str, Any]]], arguments: dict[str, Any]) -> list[tuple[int, dict[str, Any]]]:
    sort_by = str(arguments.get("sort_by") or "").casefold()
    reverse = sort_order_desc(arguments)
    if sort_by in {"timestamp", "time", "event_time"}:
        matches.sort(key=lambda item: (item[1]["timestamp"], item[1]["event_id"]), reverse=reverse)
    elif sort_by in {"score", "match_score", "relevance"}:
        matches.sort(key=lambda item: (item[0], item[1]["timestamp"], item[1]["event_id"]), reverse=reverse)
    elif sort_by in {"event_id", "id"}:
        matches.sort(key=lambda item: item[1]["event_id"], reverse=reverse)
    elif arguments.get("keywords"):
        matches.sort(key=lambda item: (-item[0], item[1]["timestamp"], item[1]["event_id"]))
    else:
        matches.sort(key=lambda item: (item[1]["timestamp"], item[1]["event_id"]))
    return matches


def filter_event_matches(arguments: dict[str, Any]) -> list[tuple[int, dict[str, Any]]]:
    start = parse_time(arguments.get("start_time"))
    end = parse_time(arguments.get("end_time"))
    location_ids = set(arguments.get("location_ids") or [])
    entity_ids = set(arguments.get("entity_ids") or [])
    actors = {value.casefold() for value in arguments.get("actors") or []}
    source_types = set(arguments.get("source_types") or [])
    reliabilities = set(arguments.get("reliabilities") or [])
    keywords = [normalize_text(value) for value in arguments.get("keywords") or [] if value]
    event_ids = set(arguments.get("event_ids") or [])
    night_only = bool(arguments.get("night_only"))
    match_all_keywords = bool(arguments.get("match_all_keywords"))

    matches = []
    for event in visible_events():
        if start and event["timestamp"] < start:
            continue
        if end and event["timestamp"] > end:
            continue
        if location_ids and event["location_id"] not in location_ids:
            continue
        if entity_ids and event_entity_id(event) not in entity_ids:
            continue
        if actors and event_entity_name(event).casefold() not in actors:
            continue
        if source_types and event["source_type"] not in source_types:
            continue
        if reliabilities and event["source_reliability"] not in reliabilities:
            continue
        if event_ids and event["event_id"] not in event_ids:
            continue
        hour = event["timestamp"].hour
        if night_only and not (hour >= 20 or hour < 6):
            continue
        haystack = normalize_text(
            " ".join([event["event_summary"], event_entity_name(event), event["location_name"], event["source_type"]])
        )
        if keywords:
            keyword_matches = [term_in_text(keyword, haystack) for keyword in keywords]
            if match_all_keywords and not all(keyword_matches):
                continue
            if not match_all_keywords and not any(keyword_matches):
                continue
        score = 0
        summary_folded = normalize_text(event["event_summary"])
        actor_folded = normalize_text(event_entity_name(event))
        for keyword in keywords:
            if keyword == summary_folded or keyword == actor_folded:
                score += 6
            elif term_in_text(keyword, summary_folded):
                score += 4
            elif term_in_text(keyword, actor_folded):
                score += 3
            elif term_in_text(keyword, haystack):
                score += 1
        if any(marker in event["event_summary"] for marker in DIRECT_OBSERVATION_MARKERS):
            score += 1
        if event_has_negation(event):
            score -= 4
        if any(marker in event["event_summary"] for marker in BENIGN_MARKERS):
            score -= 2
        matches.append((score, event))

    return sort_event_matches(matches, arguments)


def search_events(arguments: dict[str, Any]) -> dict[str, Any]:
    matches = filter_event_matches(arguments)
    total = len(matches)
    requested_limit = arguments.get("limit")
    limit = coverage_limit(requested_limit)
    selected = matches[:limit]
    return {
        "total": total,
        "returned": len(selected),
        "truncated": total > len(selected),
        "requested_limit": requested_limit,
        "effective_limit": limit,
        "coverage_policy": "max_coverage_default",
        "sort_by": arguments.get("sort_by") or ("score" if arguments.get("keywords") else "timestamp"),
        "sort_order": arguments.get("sort_order") or ("desc" if str(arguments.get("sort_by") or "").casefold() in {"score", "match_score", "relevance"} else "asc"),
        "event_ids": [event["event_id"] for _, event in selected],
        "events": [{**public_event(event), "match_score": score} for score, event in selected],
    }


def semantic_search_events(arguments: dict[str, Any]) -> dict[str, Any]:
    query = str(arguments.get("query") or "").strip()
    seed_ids = arguments.get("seed_event_ids") or []
    seed_events = [event for event_id in seed_ids if (event := visible_event(event_id)) is not None]
    query_parts = [query]
    query_parts.extend(event["event_summary"] for event in seed_events)
    query_text = "\n".join(part for part in query_parts if part)
    if not query_text.strip():
        raise ValueError("semantic_search_events requires query or seed_event_ids")

    requested_limit = arguments.get("limit", 50)
    limit = min(bounded_limit(requested_limit), MAX_SEMANTIC_LIMIT)
    filters = {
        "start_time": arguments.get("start_time"),
        "end_time": arguments.get("end_time"),
        "location_ids": arguments.get("location_ids") or [],
        "entity_ids": arguments.get("entity_ids") or [],
        "source_types": arguments.get("source_types") or [],
        "reliabilities": arguments.get("reliabilities") or [],
        "certainty_levels": arguments.get("certainty_levels") or [],
        "keywords": arguments.get("keywords") or [],
        "match_all_keywords": bool(arguments.get("match_all_keywords", False)),
    }
    index = get_semantic_index()
    matches = index.search(query_text, filters=filters, limit=limit)
    events = []
    event_ids = []
    for match in matches:
        event = visible_event(match["event_id"])
        if not event:
            continue
        event_ids.append(event["event_id"])
        events.append({
            **public_event(event),
            "semantic_score": match["semantic_score"],
            "semantic_rationale": match["rationale"],
        })
    return {
        "query": query,
        "seed_event_ids": [event["event_id"] for event in seed_events],
        "missing_seed_event_ids": [event_id for event_id in seed_ids if visible_event(event_id) is None],
        "backend": index.backend,
        "semantic_backend": index.backend,
        "index_manifest": index.manifest,
        "filters_applied": filters,
        "requested_limit": requested_limit,
        "effective_limit": limit,
        "event_ids": event_ids,
        "events": events,
        "matches": [
            {
                "event_id": item["event_id"],
                "semantic_score": item["semantic_score"],
                "rationale": item["rationale"],
            }
            for item in matches
        ],
        "returned": len(event_ids),
    }


def get_objects(arguments: dict[str, Any]) -> dict[str, Any]:
    object_type = str(arguments.get("object_type") or "event").casefold()
    if object_type == "events":
        object_type = "event"
    elif object_type == "locations":
        object_type = "location"
    elif object_type == "entities":
        object_type = "entity"

    event_ids = arguments.get("event_ids") or []
    location_ids = arguments.get("location_ids") or []
    entity_ids = arguments.get("entity_ids") or []
    names_or_aliases = arguments.get("names_or_aliases") or []

    found_events = [event for event_id in event_ids if (event := visible_event(event_id)) is not None]
    found_locations = [
        item for location_id in location_ids
        if (item := scoped_location_presentation(location_id)) is not None
    ]
    found_entities = [
        item for entity_id in entity_ids
        if (item := scoped_entity_presentation(entity_id)) is not None
    ]

    if object_type == "all":
        found_locations.extend(
            scoped_location_presentation(event["location_id"])
            for event in found_events
            if scoped_location_presentation(event["location_id"]) is not None
        )
        found_entities.extend(
            scoped_entity_presentation(event_entity_id(event))
            for event in found_events
            if scoped_entity_presentation(event_entity_id(event)) is not None
        )

    if object_type in {"location", "all"}:
        for name in names_or_aliases:
            for location_id in LOCATION_PRESENTATIONS:
                location = scoped_location_presentation(location_id)
                if location is None:
                    continue
                haystack = " ".join(str(location.get(key) or "") for key in ["location_id", "location_name", "name", "municipality", "locality", "region", "type"])
                if normalize_text(name) and normalize_text(name) in normalize_text(haystack):
                    found_locations.append(location)

    if object_type in {"entity", "all"}:
        for name in names_or_aliases:
            found_entities.extend(entity_matches(str(name)))

    deduped_locations = {item["location_id"]: item for item in found_locations}
    deduped_entities = {item["entity_id"]: item for item in found_entities}
    return {
        "object_type": object_type,
        "events": [public_event(event) for event in found_events] if object_type in {"event", "all"} else [],
        "location_layers": list(deduped_locations.values()) if object_type in {"location", "all"} else [],
        "entity_layers": list(deduped_entities.values()) if object_type in {"entity", "all"} else [],
        "missing_event_ids": [event_id for event_id in event_ids if visible_event(event_id) is None],
        "missing_location_ids": [location_id for location_id in location_ids if scoped_location_presentation(location_id) is None],
        "missing_entity_ids": [entity_id for entity_id in entity_ids if scoped_entity_presentation(entity_id) is None],
    }


def resolve_location(arguments: dict[str, Any]) -> dict[str, Any]:
    query = str(arguments.get("query") or "").strip()
    resolved_terms = []
    ids: list[str] = []
    seen: set[str] = set()
    for term in split_location_query(query):
        term_ids = match_location_term(term)
        if not term_ids:
            continue
        new_ids = [location_id for location_id in term_ids if location_id not in seen]
        for location_id in new_ids:
            seen.add(location_id)
            ids.append(location_id)
        resolved_terms.append({
            "term": term,
            "matched_location_count": len(term_ids),
            "new_location_count": len(new_ids),
            "sample_location_ids": term_ids[:10],
        })
    return {
        "query": query,
        "location_ids": ids,
        "match_count": len(ids),
        "locations": [{"location_id": location_id, **LOCATIONS[location_id]} for location_id in ids],
        "location_layers": [LOCATION_PRESENTATIONS[location_id] for location_id in ids if location_id in LOCATION_PRESENTATIONS],
        "resolved_terms": resolved_terms,
    }


def resolve_event_reference(arguments: dict[str, Any]) -> dict[str, Any]:
    query = str(arguments.get("query") or "").strip()
    direct_ids = EVENT_REFERENCES.get(query, [])
    llm_interpretation = None
    if direct_ids:
        events = [event for event_id in direct_ids if (event := visible_event(event_id)) is not None]
    else:
        llm_interpretation = sample_json_task(
            "resolve_event_reference_terms",
            (
                "אתה מפרש הפניה טבעית של אנליסט לאירוע במאגר מודיעיני. "
                "החזר JSON תקין בלבד עם search_phrases, location_terms, actor_terms, rationale. "
                "כל רשימה תכיל עד 8 ביטויים קצרים שניתן לחפש בשדות גלויים. "
                "אל תמציא מזהי אירועים או שמות שלא משתמעים מהשאילתה."
            ),
            {"query": query},
            max_tokens=450,
        )
        search_terms = [query]
        for key in ("search_phrases", "location_terms", "actor_terms"):
            for term in string_list((llm_interpretation or {}).get(key), limit=8):
                if normalize_text(term) not in {normalize_text(item) for item in search_terms}:
                    search_terms.append(term)
        resolved_location_ids: list[str] = []
        for term in string_list((llm_interpretation or {}).get("location_terms"), limit=8):
            for location_id in match_location_term(term):
                if location_id not in resolved_location_ids:
                    resolved_location_ids.append(location_id)
        resolved_entity_ids: list[str] = []
        for term in string_list((llm_interpretation or {}).get("actor_terms"), limit=8):
            for match in entity_matches(term):
                entity_id = match.get("entity_id")
                if entity_id and entity_id not in resolved_entity_ids:
                    resolved_entity_ids.append(entity_id)
        semantic_matches = semantic_candidates(
            "\n".join(search_terms),
            {
                "location_ids": resolved_location_ids,
                "entity_ids": resolved_entity_ids,
            },
            80,
        )
        semantic_by_id = {match["event_id"]: match for match in semantic_matches if match.get("event_id")}
        query_folded = query.casefold()
        scored_events_by_id: dict[str, dict[str, Any]] = {}
        for event in visible_events():
            haystack = normalize_text(
                " ".join([event["event_summary"], event["event_id"], event_entity_name(event), event["location_name"], event["source_type"]])
            )
            score = 0
            if query_folded in event["event_summary"].casefold() or query_folded in event["event_id"].casefold():
                score += 10
            matched_terms = []
            for term in search_terms[1:]:
                folded = normalize_text(term)
                if folded and term_in_text(folded, haystack):
                    score += 3
                    matched_terms.append(term)
            if score > 0 and any(marker in event["event_summary"] for marker in DIRECT_OBSERVATION_MARKERS):
                score += 1
            if score > 0:
                semantic_match = semantic_by_id.get(event["event_id"])
                if semantic_match:
                    score += min(6, max(1, int(float(semantic_match.get("semantic_score") or 0) * 14)))
                scored_events_by_id[event["event_id"]] = {
                    "score": score,
                    "matched_terms": matched_terms,
                    "semantic_score": round(float(semantic_match.get("semantic_score") or 0), 6) if semantic_match else 0,
                    "semantic_rationale": semantic_match.get("rationale") if semantic_match else "",
                    "event": event,
                }
        for semantic_match in semantic_matches:
            event_id = semantic_match.get("event_id")
            if not event_id or event_id in scored_events_by_id:
                continue
            event = visible_event(event_id)
            if not event:
                continue
            score = min(8, max(2, int(float(semantic_match.get("semantic_score") or 0) * 18)))
            if any(marker in event["event_summary"] for marker in DIRECT_OBSERVATION_MARKERS):
                score += 1
            scored_events_by_id[event_id] = {
                "score": score,
                "matched_terms": [],
                "semantic_score": round(float(semantic_match.get("semantic_score") or 0), 6),
                "semantic_rationale": semantic_match.get("rationale") or "",
                "event": event,
            }
        scored_events = sorted(
            scored_events_by_id.values(),
            key=lambda item: (-item["score"], item["event"]["timestamp"], item["event"]["event_id"]),
        )
        events = [item["event"] for item in scored_events[:20]]
    return {
        "query": query,
        "event_ids": [event["event_id"] for event in events],
        "events": [
            {
                **public_event(event),
                "reference_score": next((item["score"] for item in scored_events if item["event"]["event_id"] == event["event_id"]), None) if not direct_ids else None,
                "matched_terms": next((item["matched_terms"] for item in scored_events if item["event"]["event_id"] == event["event_id"]), []) if not direct_ids else [],
                "semantic_score": next((item["semantic_score"] for item in scored_events if item["event"]["event_id"] == event["event_id"]), 0) if not direct_ids else 0,
                "semantic_rationale": next((item["semantic_rationale"] for item in scored_events if item["event"]["event_id"] == event["event_id"]), "") if not direct_ids else "",
            }
            for event in events
        ],
        "semantic_candidate_count": len(semantic_matches) if not direct_ids else 0,
        "semantic_backend": get_semantic_index().backend if not direct_ids and semantic_matches else None,
        "resolved_location_ids": resolved_location_ids if not direct_ids else [],
        "resolved_entity_ids": resolved_entity_ids if not direct_ids else [],
        "llm_interpretation": {
            "search_phrases": string_list((llm_interpretation or {}).get("search_phrases"), limit=8),
            "location_terms": string_list((llm_interpretation or {}).get("location_terms"), limit=8),
            "actor_terms": string_list((llm_interpretation or {}).get("actor_terms"), limit=8),
            "rationale": str((llm_interpretation or {}).get("rationale") or "")[:500],
            "source": "mcp_sampling" if llm_interpretation else "not_available",
        },
    }


def find_actor_history(arguments: dict[str, Any]) -> dict[str, Any]:
    actors = arguments.get("actors") or []
    entity_ids = list(arguments.get("entity_ids") or [])
    seen_entities = set(entity_ids)
    for actor in actors:
        matches = entity_matches(actor)
        for match in matches:
            entity_id = match.get("entity_id")
            if entity_id and entity_id not in seen_entities:
                seen_entities.add(entity_id)
                entity_ids.append(entity_id)
    forwarded = {
        "entity_ids": entity_ids,
        "start_time": arguments.get("start_time"),
        "end_time": arguments.get("end_time"),
        "location_ids": arguments.get("location_ids") or [],
        "source_types": arguments.get("source_types") or [],
        "night_only": arguments.get("night_only", False),
        "limit": coverage_limit(arguments.get("limit", DEFAULT_LIMIT)),
    }
    result = search_events(forwarded)
    result["requested_actors"] = actors
    result["requested_entity_ids"] = entity_ids
    result["resolved_entity_ids"] = entity_ids
    result["entity_layers"] = [
        item for entity_id in entity_ids
        if (item := scoped_entity_presentation(entity_id)) is not None
    ]
    return result


def aggregate_events(arguments: dict[str, Any]) -> dict[str, Any]:
    group_by = arguments.get("group_by", "location")
    matches = filter_event_matches(arguments)
    events = [event for _, event in matches]
    include_first_last = bool(arguments.get("include_first_last"))
    aggregate_sort_by = str(arguments.get("sort_by") or "count").casefold()
    needs_first_last = include_first_last or aggregate_sort_by in {"first_event_time", "first_time", "last_event_time", "last_time"}
    aggregate_reverse = sort_order_desc({**arguments, "sort_order": arguments.get("sort_order") or ("asc" if aggregate_sort_by in {"first_event_time", "first_time"} else "desc")})
    top_n = arguments.get("top_n")
    top_n = bounded_limit(top_n) if top_n is not None else None
    key_functions = {
        "location": lambda event: (event["location_id"], event["location_name"]),
        "municipality": lambda event: LOCATIONS.get(event["location_id"], {}).get("municipality") or "לא ידוע",
        "actor": lambda event: event_entity_name(event),
        "entity": lambda event: event_entity_id(event) or event_entity_name(event),
        "source": lambda event: event["source_type"],
        "hour": lambda event: f"{event['timestamp'].hour:02d}:00",
        "date": lambda event: event["timestamp"].date().isoformat(),
    }
    if group_by not in key_functions:
        raise ValueError(f"Unsupported group_by: {group_by}")
    counts = Counter(key_functions[group_by](event) for event in events)
    grouped_events: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    if needs_first_last:
        for event in events:
            grouped_events[key_functions[group_by](event)].append(event)

    def apply_first_last(group: dict[str, Any], key: Any) -> dict[str, Any]:
        group_events = grouped_events.get(key) or []
        if not group_events:
            return group
        ordered = sorted(group_events, key=lambda event: (event["timestamp"], event["event_id"]))
        first = ordered[0]
        last = ordered[-1]
        group.update({
            "first_event_id": first["event_id"],
            "first_event_time": first["timestamp"].isoformat().replace("+00:00", "Z"),
            "first_location_id": first["location_id"],
            "first_location_name": first["location_name"],
            "last_event_id": last["event_id"],
            "last_event_time": last["timestamp"].isoformat().replace("+00:00", "Z"),
            "last_location_id": last["location_id"],
            "last_location_name": last["location_name"],
        })
        return group

    groups = []
    for key, count in counts.most_common():
        if group_by == "location":
            location_id, label = key
            location = LOCATIONS.get(location_id, {})
            group = {
                "key": location_id,
                "label": label,
                "count": count,
                "location_id": location_id,
                "location_name": label,
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
            }
            groups.append(apply_first_last(group, key) if needs_first_last else group)
        elif group_by == "municipality":
            municipality = str(key)
            matching_locations = [
                location
                for location in LOCATIONS.values()
                if (location.get("municipality") or "לא ידוע") == municipality
            ]
            coordinates = [
                (location.get("latitude"), location.get("longitude"))
                for location in matching_locations
                if location.get("latitude") is not None and location.get("longitude") is not None
            ]
            group = {
                "key": municipality,
                "label": municipality,
                "count": count,
                "municipality": municipality,
                "latitude": sum(lat for lat, _ in coordinates) / len(coordinates) if coordinates else None,
                "longitude": sum(lon for _, lon in coordinates) / len(coordinates) if coordinates else None,
            }
            groups.append(apply_first_last(group, key) if needs_first_last else group)
        elif group_by == "entity":
            entity_id = str(key)
            entity = ENTITY_PRESENTATIONS.get(entity_id, {})
            group = {
                "key": entity_id,
                "label": entity.get("canonical_name") or entity_id,
                "count": count,
                "entity_id": entity_id,
                "entity_name": entity.get("canonical_name") or entity_id,
                "entity_type": entity.get("entity_type"),
            }
            groups.append(apply_first_last(group, key) if needs_first_last else group)
        else:
            group = {"key": str(key), "label": str(key), "count": count}
            groups.append(apply_first_last(group, key) if needs_first_last else group)
    if aggregate_sort_by in {"first_event_time", "first_time"}:
        groups.sort(key=lambda group: (group.get("first_event_time") or "", str(group.get("key") or "")), reverse=aggregate_reverse)
    elif aggregate_sort_by in {"last_event_time", "last_time"}:
        groups.sort(key=lambda group: (group.get("last_event_time") or "", str(group.get("key") or "")), reverse=aggregate_reverse)
    elif aggregate_sort_by in {"label", "key"}:
        groups.sort(key=lambda group: str(group.get("label") or group.get("key") or ""), reverse=aggregate_reverse)
    else:
        groups.sort(key=lambda group: (int(group.get("count") or 0), str(group.get("key") or "")), reverse=aggregate_reverse)
    if top_n is not None:
        groups = groups[:top_n]
    result = {
        "group_by": group_by,
        "total_events": len(events),
        "groups_returned": len(groups),
        "top_n": top_n,
        "sort_by": aggregate_sort_by or "count",
        "sort_order": "desc" if aggregate_reverse else "asc",
        "include_first_last": needs_first_last,
        "aggregation_scope": "complete_filtered_population",
        "ignored_raw_event_limit": arguments.get("limit") if arguments.get("limit") is not None else None,
        "groups": groups,
    }
    if group_by in {"location", "municipality"}:
        result["map_locations"] = groups
        if group_by == "location":
            result["location_layers"] = [LOCATION_PRESENTATIONS[group["location_id"]] for group in groups if group.get("location_id") in LOCATION_PRESENTATIONS]
    if group_by == "entity":
        result["entity_layers"] = [ENTITY_PRESENTATIONS[group["entity_id"]] for group in groups if group.get("entity_id") in ENTITY_PRESENTATIONS]
    return result


def explain_linkage(arguments: dict[str, Any]) -> dict[str, Any]:
    first_id = arguments.get("first_event_id")
    second_id = arguments.get("second_event_id")
    first = visible_event(first_id)
    second = visible_event(second_id)
    if not first or not second:
        return {
            "first_event_id": first_id,
            "second_event_id": second_id,
            "missing_event_ids": [event_id for event_id, event in [(first_id, first), (second_id, second)] if not event],
            "bridges": [],
            "bridge_count": 0,
            "strongest_bridge": None,
            "assessment": "לא ניתן לבדוק קשר כי אחד האירועים לא נמצא.",
        }

    bridges = []
    first_identifiers = {
        (item["identifier_type"], normalize_text(item["value"]), item["value"])
        for item in extract_identifiers(first["event_summary"])
    }
    second_identifiers = {
        (item["identifier_type"], normalize_text(item["value"]), item["value"])
        for item in extract_identifiers(second["event_summary"])
    }
    shared_identifiers = first_identifiers & second_identifiers
    if shared_identifiers:
        bridges.append({
            "bridge_type": "shared_identifier",
            "confidence": "גבוהה",
            "weight": 8,
            "detail": ", ".join(value for _, _, value in sorted(shared_identifiers)),
        })

    if is_informative_actor(event_entity_name(first)) and is_informative_actor(event_entity_name(second)):
        first_entities = canonical_entity_ids(event_entity_name(first))
        second_entities = canonical_entity_ids(event_entity_name(second))
        if first_entities & second_entities:
            shared_entity_ids = sorted(first_entities & second_entities)
            entity_names = [
                ENTITY_PRESENTATIONS.get(entity_id, {}).get("canonical_name") or entity_id
                for entity_id in shared_entity_ids
            ]
            bridges.append({
                "bridge_type": "shared_entity_id",
                "confidence": "גבוהה",
                "weight": 6,
                "detail": ", ".join(f"{entity_id} ({name})" for entity_id, name in zip(shared_entity_ids, entity_names)),
            })
        elif normalize_text(event_entity_name(first)) == normalize_text(event_entity_name(second)):
            bridges.append({
                "bridge_type": "same_actor_text",
                "confidence": "בינונית",
                "weight": 4,
                "detail": event_entity_name(first),
            })

    hours_delta = abs((second["timestamp"] - first["timestamp"]).total_seconds()) / 3600
    if hours_delta <= 24:
        bridges.append({
            "bridge_type": "temporal_proximity",
            "confidence": "נמוכה" if hours_delta > 6 else "בינונית",
            "weight": 3 if hours_delta <= 2 else 2 if hours_delta <= 6 else 1,
            "detail": f"פער זמן {hours_delta:.1f} שעות",
        })

    distance = haversine_km(first["location_id"], second["location_id"])
    if distance is not None and distance <= 25:
        bridges.append({
            "bridge_type": "geographic_proximity",
            "confidence": "נמוכה" if distance > 10 else "בינונית",
            "weight": 3 if distance < 1 else 2 if distance <= 10 else 1,
            "detail": f"מרחק {distance:.1f} קמ",
        })

    shared_terms = semantic_overlap(first["event_summary"], second["event_summary"])
    if shared_terms:
        bridges.append({
            "bridge_type": "semantic_overlap",
            "confidence": "בינונית" if len(shared_terms) >= 2 else "נמוכה",
            "weight": 3 if len(shared_terms) >= 2 else 2,
            "detail": ", ".join(shared_terms[:8]),
        })

    bridges.sort(key=lambda item: -item["weight"])
    strongest = bridges[0] if bridges else None
    total_weight = sum(item["weight"] for item in bridges)
    if any(item["bridge_type"] in {"shared_identifier", "shared_entity_id", "shared_entity_or_alias"} for item in bridges):
        assessment = "קיים גשר ראייתי ישיר יחסית בין האירועים."
    elif total_weight >= 4:
        assessment = "קיים קשר נסיבתי המבוסס על זמן, מקום או תוכן, אך לא מזהה ישיר."
    else:
        assessment = "לא נמצא גשר ראייתי מספיק; יש להציג את המעבר כהשערה או פער."
    return {
        "first_event_id": first["event_id"],
        "second_event_id": second["event_id"],
        "bridges": bridges,
        "bridge_count": len(bridges),
        "strongest_bridge": strongest,
        "total_weight": total_weight,
        "assessment": assessment,
        "events": [public_event(first), public_event(second)],
    }


def build_event_sequence(arguments: dict[str, Any]) -> dict[str, Any]:
    ids = arguments.get("event_ids") or []
    events = [event for event_id in ids if (event := visible_event(event_id)) is not None]
    events.sort(key=lambda event: event["timestamp"])
    by_location: dict[str, list[str]] = defaultdict(list)
    for event in events:
        by_location[event["location_id"]].append(event["event_id"])
    route = []
    seen = set()
    for event in events:
        if event["location_id"] not in seen:
            seen.add(event["location_id"])
            location = LOCATIONS.get(event["location_id"], {})
            route.append(
                {
                    "step": len(route) + 1,
                    "location_id": event["location_id"],
                    "location_name": event["location_name"],
                    "latitude": location.get("latitude"),
                    "longitude": location.get("longitude"),
                    "event_ids": by_location[event["location_id"]],
                }
            )
    return {
        "event_count": len(events),
        "start_time": events[0]["timestamp_utc"] if events else None,
        "end_time": events[-1]["timestamp_utc"] if events else None,
        "ordered_event_ids": [event["event_id"] for event in events],
        "route": route,
        "events": [public_event(event) for event in events],
    }


STEP_BRIDGE_PROPERTY = {
    "type": "string",
    "description": (
        "Optional model-authored Hebrew sentence explaining the previous-step conclusion "
        "and why this tool call is the next step. Metadata only; ignored by tool logic."
    ),
}


def with_step_bridge(schema: dict[str, Any]) -> dict[str, Any]:
    properties = dict(schema.get("properties") or {})
    properties.setdefault("step_bridge", STEP_BRIDGE_PROPERTY)
    return {**schema, "properties": properties}


TARGET_BANK = TargetBank()


def _prior_successful_audit_records() -> list[dict[str, Any]]:
    if not AUDIT_PATH.exists():
        return []
    records = []
    policy = active_playback_policy()
    expected_visibility = (
        {
            "run_id": policy.get("run_id"),
            "revision": policy.get("revision"),
            "visible_timeframe": policy.get("visible_timeframe"),
        }
        if policy is not None else None
    )
    for line in AUDIT_PATH.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (
            isinstance(record, dict)
            and not record.get("is_error")
            and record.get("playback_visibility") == expected_visibility
        ):
            records.append(record)
    return records


def _selected_aggregate_rows(group_by: str, row_ids: list[str]) -> list[dict[str, Any]]:
    available: dict[str, dict[str, Any]] = {}
    for record in _prior_successful_audit_records():
        if record.get("tool") != "aggregate_events":
            continue
        result = record.get("result") or {}
        if result.get("group_by") != group_by:
            continue
        for row in result.get("groups") or []:
            if not isinstance(row, dict):
                continue
            key = str(row.get("key") or row.get("label") or "").strip()
            label = str(row.get("label") or row.get("key") or "").strip()
            if key:
                available[key] = row
            if label:
                available[label] = row
    missing = [row_id for row_id in row_ids if row_id not in available]
    if missing:
        raise ValueError(f"aggregate result IDs were not returned by an earlier aggregate_events call: {', '.join(missing)}")
    return [{**available[row_id], "group_by": group_by} for row_id in row_ids]


def _materialize_presentation_layers(
    selections: list[dict[str, Any]],
    *,
    id_prefix: str,
    evidence_references: bool = False,
) -> list[dict[str, Any]]:
    requested_layers = []
    for index, selection in enumerate(selections, start=1):
        kind = str(selection.get("kind") or "").strip()
        row_ids = list(dict.fromkeys(
            str(value or "").strip()
            for value in selection.get("ids") or []
            if str(value or "").strip()
        ))
        if not row_ids:
            raise ValueError(f"layer {index} requires at least one ID")
        label = str(selection.get("label") or "").strip()
        if not label:
            raise ValueError(f"layer {index} requires a user-facing label")
        view = str(selection.get("view") or "").strip()
        if kind == "events":
            missing = [row_id for row_id in row_ids if visible_event(row_id) is None]
            if missing:
                raise ValueError(f"unknown event IDs: {', '.join(missing)}")
            rows = [public_event(visible_event(row_id)) for row_id in row_ids]
            result_kind = "events"
            capabilities = {"table": True, "map": True, "timeline": True}
        elif kind == "locations":
            missing = [row_id for row_id in row_ids if scoped_location_presentation(row_id) is None]
            if missing:
                raise ValueError(f"unknown location IDs: {', '.join(missing)}")
            rows = [scoped_location_presentation(row_id) for row_id in row_ids]
            result_kind = "location_metadata"
            capabilities = {"table": True, "map": True, "timeline": False}
        elif kind == "entities":
            missing = [row_id for row_id in row_ids if scoped_entity_presentation(row_id) is None]
            if missing:
                raise ValueError(f"unknown entity IDs: {', '.join(missing)}")
            rows = [scoped_entity_presentation(row_id) for row_id in row_ids]
            result_kind = "entity_metadata"
            capabilities = {"table": True, "map": True, "timeline": False}
        elif kind == "attack_targets":
            TARGET_BANK.initialize()
            rows = [TARGET_BANK.get_candidate(row_id) for row_id in row_ids]
            result_kind = "attack_targets"
            capabilities = {"table": True, "map": True, "timeline": False}
        elif kind == "aggregate_groups":
            group_by = str(selection.get("group_by") or "").strip()
            if not group_by:
                raise ValueError(f"aggregate layer {index} requires group_by")
            rows = _selected_aggregate_rows(group_by, row_ids)
            is_time = group_by in {"date", "hour"}
            is_location = group_by == "location"
            if is_location:
                result_kind = "locations"
                capabilities = {"table": True, "map": True, "timeline": False}
            elif is_time:
                result_kind = "time_aggregation"
                capabilities = {"table": True, "map": False, "timeline": True}
                rows = [{
                    **row,
                    "timeLabel": row.get("label") or row.get("key"),
                    "sortKey": row.get("key") or row.get("label"),
                    "summary": f'{row.get("count", 0)} events',
                } for row in rows]
            else:
                result_kind = "group_aggregation"
                capabilities = {"table": True, "map": False, "timeline": False}
        else:
            raise ValueError(f"unsupported requested-result kind: {kind}")
        view_capability = {"map": "map", "timeline": "timeline", "evidence": "table"}.get(view)
        if view_capability is None:
            raise ValueError(f"unsupported requested view: {view}")
        if evidence_references and view not in {"map", "timeline"}:
            raise ValueError("evidence-reference layers support map or timeline views only")
        if not capabilities.get(view_capability):
            raise ValueError(f"requested view {view} is incompatible with {result_kind}")
        requested_layers.append({
            "id": f"{id_prefix}:{index}",
            "label": label,
            "kind": result_kind,
            "rows": rows,
            "capabilities": capabilities,
            "recommended_view": view,
        })
    return requested_layers


def present_requested_results(arguments: dict[str, Any]) -> dict[str, Any]:
    selections = arguments.get("layers") or []
    evidence_selections = arguments.get("evidence_layers") or []
    if not selections and not evidence_selections:
        raise ValueError("at least one requested-result or evidence-reference layer is required")
    requested_layers = _materialize_presentation_layers(
        selections, id_prefix="requested-result"
    )
    evidence_layers = _materialize_presentation_layers(
        evidence_selections, id_prefix="evidence-reference", evidence_references=True
    )
    return {
        "requested_result_layers": requested_layers,
        "evidence_reference_layers": evidence_layers,
        "returned_layers": len(requested_layers),
        "returned_evidence_layers": len(evidence_layers),
    }


def validate_target_references(candidate: dict[str, Any], evidence: list[dict[str, Any]] | None = None) -> None:
    location_id = str(candidate.get("location_id") or "").strip()
    if location_id not in LOCATIONS:
        raise ValueError(f"unknown canonical location_id: {location_id}")
    entity_id = str(candidate.get("entity_id") or "").strip()
    if entity_id and entity_id not in ENTITY_PRESENTATIONS:
        raise ValueError(f"unknown canonical entity_id: {entity_id}")
    for item in evidence or []:
        record_id = str(item.get("record_id") or "").strip()
        evidence_location_id = str(item.get("location_id") or "").strip()
        if visible_event(record_id) is None:
            raise ValueError(f"unknown evidence record_id: {record_id}")
        if evidence_location_id not in LOCATIONS:
            raise ValueError(f"unknown evidence location_id: {evidence_location_id}")


def search_target_candidates(arguments: dict[str, Any]) -> dict[str, Any]:
    TARGET_BANK.initialize()
    candidates = TARGET_BANK.search_candidates(arguments)
    return {"candidates": candidates, "returned": len(candidates)}


def get_target_candidate(arguments: dict[str, Any]) -> dict[str, Any]:
    TARGET_BANK.initialize()
    return {"candidate": TARGET_BANK.get_candidate(arguments.get("target_id"))}


def create_target_candidate(arguments: dict[str, Any]) -> dict[str, Any]:
    TARGET_BANK.initialize()
    candidate = {**(arguments.get("candidate") or {}), "created_by": "moshe"}
    supplied_evidence = arguments.get("evidence") or []
    event_ids = [str(item.get("record_id") or "").strip() for item in supplied_evidence]
    fusion = prepare_candidate(_fusion_events(event_ids), candidate.get("confidence") or "")
    if not fusion["persistence_eligible"]:
        raise ValueError("candidate is not persistence eligible: " + "; ".join(fusion["persistence_block_reasons"]))
    evidence = fusion["evidence"]
    candidate.update(fusion["quantity"])
    validate_target_references(candidate, evidence)
    return {"candidate": TARGET_BANK.create_candidate(candidate, evidence)}


def update_target_candidate(arguments: dict[str, Any]) -> dict[str, Any]:
    TARGET_BANK.initialize()
    target_id = arguments.get("target_id")
    changes = arguments.get("changes") or {}
    current = TARGET_BANK.get_candidate(target_id)
    validate_target_references({**current, **changes})
    return {"candidate": TARGET_BANK.update_candidate(target_id, changes)}


def reconcile_attached_evidence_groups(
    current_evidence: list[dict[str, Any]], fused_evidence: list[dict[str, Any]], new_ids: set[str],
) -> list[dict[str, Any]]:
    """Preserve stored group identities while rejecting real regrouping of existing evidence."""
    stored_by_id = {item["record_id"]: item["source_group"] for item in current_evidence}
    fused_by_id = {item["record_id"]: item for item in fused_evidence}
    missing = [record_id for record_id in stored_by_id if record_id not in fused_by_id]
    if missing:
        raise ValueError(f"fusion omitted existing evidence: {missing[0]}")

    stored_groups_by_fused_group: dict[str, set[str]] = defaultdict(set)
    fused_groups_by_stored_group: dict[str, set[str]] = defaultdict(set)
    for record_id, stored_group in stored_by_id.items():
        fused_group = fused_by_id[record_id]["source_group"]
        stored_groups_by_fused_group[fused_group].add(stored_group)
        fused_groups_by_stored_group[stored_group].add(fused_group)

    if any(len(groups) > 1 for groups in stored_groups_by_fused_group.values()):
        raise ValueError("new evidence would merge existing immutable source groups")
    if any(len(groups) > 1 for groups in fused_groups_by_stored_group.values()):
        raise ValueError("new evidence would split an existing immutable source group")

    assigned_by_fused_group = {
        fused_group: next(iter(stored_groups))
        for fused_group, stored_groups in stored_groups_by_fused_group.items()
        if stored_groups
    }
    occupied_groups = set(stored_by_id.values())
    members_by_fused_group: dict[str, list[str]] = defaultdict(list)
    for item in fused_evidence:
        members_by_fused_group[item["source_group"]].append(item["record_id"])

    for fused_group, members in members_by_fused_group.items():
        if fused_group in assigned_by_fused_group:
            continue
        assigned_group = fused_group
        if fused_group.startswith("visible-report:") or assigned_group in occupied_groups:
            fingerprint = hashlib.sha256("\n".join(sorted(members)).encode("utf-8")).hexdigest()[:12]
            assigned_group = f"visible-report:{fingerprint}"
        assigned_by_fused_group[fused_group] = assigned_group
        occupied_groups.add(assigned_group)

    return [
        {**item, "source_group": assigned_by_fused_group[item["source_group"]]}
        for item in fused_evidence
        if item["record_id"] in new_ids
    ]


def attach_target_evidence(arguments: dict[str, Any]) -> dict[str, Any]:
    TARGET_BANK.initialize()
    target_id = arguments.get("target_id")
    supplied_evidence = arguments.get("evidence") or []
    current = TARGET_BANK.get_candidate(target_id)
    all_ids = [item["record_id"] for item in current["evidence"]] + [str(item.get("record_id") or "").strip() for item in supplied_evidence]
    fusion = prepare_candidate(_fusion_events(all_ids), current["confidence"])
    new_ids = {str(item.get("record_id") or "").strip() for item in supplied_evidence}
    evidence = reconcile_attached_evidence_groups(current["evidence"], fusion["evidence"], new_ids)
    validate_target_references(current, evidence)
    return {"candidate": TARGET_BANK.attach_evidence(target_id, evidence)}


def _fusion_events(event_ids: list[str]) -> list[dict[str, Any]]:
    if not event_ids:
        raise ValueError("at least one event_id is required")
    if len(set(event_ids)) != len(event_ids):
        raise ValueError("event_id values must be unique")
    unknown = [event_id for event_id in event_ids if visible_event(event_id) is None]
    if unknown:
        raise ValueError(f"unknown event_id: {unknown[0]}")
    return [public_event(visible_event(event_id)) for event_id in event_ids]


def prepare_target_candidate(arguments: dict[str, Any]) -> dict[str, Any]:
    """Discover corroboration and build a deterministic save-ready assessment without persisting it."""
    seeds = _fusion_events(arguments.get("event_ids") or [])
    if arguments.get("discover_corroboration", True):
        anchor = next((item for item in seeds if item.get("collection_family") == "airborne_isr_video_exploitation"), seeds[0])
        corpus = [
            public_event(item)
            for item in FUSION_EVENTS_BY_CONTEXT.get((anchor.get("location_id") or "", anchor.get("entity_id") or ""), [])
            if event_visible(item)
        ]
        discovery = discover_corroborating_evidence(seeds, corpus)
        selected = _fusion_events(discovery["selected_event_ids"])
        assessment = prepare_candidate(selected, arguments.get("confidence") or "")
        if discovery["ambiguous"]:
            assessment["persistence_eligible"] = False
            assessment["persistence_block_reasons"].append("corroborating evidence pair is ambiguous; report only")
        return {**assessment, "discovery": discovery}
    return prepare_candidate(seeds, arguments.get("confidence") or "")


WORKSTREAM_ACTIONS = {
    "create", "add_indication", "remove_indication", "update_annotation",
    "update_lead_statement", "request_completion", "send_to_assessment", "reject",
}


def prepare_workstream_creation(arguments: dict[str, Any]) -> dict[str, Any]:
    """Return a bounded workstream creation handoff; persistence stays in the app server."""
    title = str(arguments.get("title") or "").strip()
    objective = str(arguments.get("objective") or "").strip()
    responsibility = str(arguments.get("responsibility") or "").strip()
    if not title:
        raise ValueError("title is required")
    if not objective:
        raise ValueError("objective is required")
    if not responsibility:
        raise ValueError("responsibility is required")
    return {
        "workstream_creation": {
            "title": title,
            "objective": objective,
            "responsibility": responsibility,
        },
        "persisted": False,
    }


def prepare_workstream_indication_proposal(arguments: dict[str, Any]) -> dict[str, Any]:
    """Resolve references and prepare an uncommitted workstream change."""
    action = str(arguments.get("action") or "create").strip()
    if action not in WORKSTREAM_ACTIONS:
        raise ValueError("unsupported workstream action")
    record_ids = [str(value).strip() for value in arguments.get("record_ids") or []]
    events = _fusion_events(record_ids) if record_ids else []
    if action in {"create", "add_indication"} and not events:
        raise ValueError("at least one REC record_id is required for this action")
    target_id = str(arguments.get("target_id") or "").strip()
    target = None
    if target_id:
        TARGET_BANK.initialize()
        target = TARGET_BANK.get_candidate(target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {target_id}")
    indications = []
    supplied = arguments.get("indications") or []
    supplied_by_id = {
        str(item.get("record_id") or "").strip(): item
        for item in supplied if isinstance(item, dict)
    }
    for event in events:
        record_id = event["event_id"]
        detail = supplied_by_id.get(record_id, {})
        indications.append({
            "record_id": record_id,
            "role": str(detail.get("role") or "context").strip(),
            "relevance": str(detail.get("relevance") or "").strip(),
            "annotation": str(detail.get("annotation") or "").strip(),
            "observed_claim": event.get("event_summary") or record_id,
        })
    proposal = {
        "proposal_type": "target_assessment_lead",
        "action": action,
        "proposed_turn_message_id": str(arguments.get("proposed_turn_message_id") or "").strip(),
        "expected_revision": arguments.get("expected_revision"),
        "artifact_id": str(arguments.get("artifact_id") or "").strip() or None,
        "target_id": target_id or None,
        "target_label": (target or {}).get("title") if target else None,
        "lead_statement": str(arguments.get("lead_statement") or "").strip(),
        "indications": indications,
        "payload": arguments.get("payload") if isinstance(arguments.get("payload"), dict) else {},
        "supporting_signals": arguments.get("supporting_signals") or [],
        "contradictions": arguments.get("contradictions") or [],
        "assessment_questions": arguments.get("assessment_questions") or [],
        "gaps": arguments.get("gaps") or [],
        "assigned_to": str(arguments.get("assigned_to") or "").strip(),
        "annotation": str(arguments.get("annotation") or "").strip(),
    }
    if action == "create" and not proposal["lead_statement"]:
        raise ValueError("lead_statement is required for create")
    return {"workstream_proposal": proposal, "persisted": False}


def decide_workstream_indication_proposal(arguments: dict[str, Any]) -> dict[str, Any]:
    """Interpret a later user turn without persisting any workstream state."""
    proposal = arguments.get("proposal")
    if not isinstance(proposal, dict) or proposal.get("proposal_type") != "target_assessment_lead":
        raise ValueError("invalid proposal")
    decision = str(arguments.get("decision") or "").strip()
    if decision not in {"confirm", "reject", "correct", "clarify", "send_to_assessment"}:
        raise ValueError("unsupported proposal decision")
    proposed_turn = str(proposal.get("proposed_turn_message_id") or "").strip()
    current_turn = str(arguments.get("current_turn_message_id") or "").strip()
    if decision in {"confirm", "send_to_assessment"}:
        if not proposed_turn or not current_turn or proposed_turn == current_turn:
            raise ValueError("confirmation requires a distinct later user turn")
    corrected = arguments.get("corrected_proposal")
    return {
        "workstream_action": {
            "decision": decision,
            "proposal": corrected if decision == "correct" and isinstance(corrected, dict) else proposal,
            "current_turn_message_id": current_turn,
            "confirmation_text": str(arguments.get("confirmation_text") or "").strip(),
        },
        "persisted": False,
    }


def find_duplicate_target_candidates(arguments: dict[str, Any]) -> dict[str, Any]:
    """Find existing candidates that share the assessed target or selected evidence."""
    TARGET_BANK.initialize()
    filters = {
        "object_class": arguments.get("object_class"),
        "location_id": arguments.get("location_id"),
        "entity_id": arguments.get("entity_id"),
        "limit": arguments.get("limit", 100),
    }
    summaries = TARGET_BANK.search_candidates(filters)
    candidates = [TARGET_BANK.get_candidate(item["target_id"]) for item in summaries]
    return find_duplicate_candidates(
        candidates,
        arguments.get("event_ids") or [],
        object_class=str(arguments.get("object_class") or "").strip(),
        location_id=str(arguments.get("location_id") or "").strip(),
        entity_id=str(arguments.get("entity_id") or "").strip() or None,
    )


TARGET_CANDIDATE_PROPERTIES = {
    "target_id": {"type": "string"},
    "title": {"type": "string", "minLength": 1},
    "summary": {"type": "string", "minLength": 1},
    "object_class": {"type": "string", "minLength": 1},
    "entity_id": {"type": ["string", "null"]},
    "location_id": {"type": "string", "minLength": 1},
    "confidence": {"type": "string", "enum": ["medium", "high"]},
    "count_min": {"type": ["integer", "null"], "minimum": 0},
    "count_max": {"type": ["integer", "null"], "minimum": 0},
    "count_estimate": {"type": ["integer", "null"], "minimum": 0},
    "count_assessment": {"type": "string", "enum": ["exact", "approximate", "range", "unresolved"]},
    "fusion_explanation": {"type": "string", "minLength": 1},
    "mission_run_id": {"type": "string", "minLength": 1},
}
TARGET_CREATE_REQUIRED = [
    "title", "summary", "object_class", "location_id", "confidence", "count_assessment",
    "fusion_explanation", "mission_run_id",
]
TARGET_EVIDENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "record_id": {"type": "string", "minLength": 1},
        "source_group": {"type": "string", "minLength": 1},
        "source_type": {"type": "string", "minLength": 1},
        "observed_at": {"type": "string", "minLength": 1},
        "location_id": {"type": "string", "minLength": 1},
        "reported_object": {"type": "string", "minLength": 1},
        "reported_count": {"type": ["integer", "null"], "minimum": 0},
        "relevant_text": {"type": "string", "minLength": 1},
        "evidence_role": {"type": "string", "minLength": 1},
    },
    "required": ["record_id", "source_group", "source_type", "observed_at", "location_id", "reported_object", "relevant_text", "evidence_role"],
    "additionalProperties": False,
}


TOOLS = [
    {
        "name": "prepare_workstream_creation",
        "title": "Prepare a workstream for creation",
        "description": "Use only in the dedicated workstream-creation conversation after resolving every supplied TGT/REC identifier and deriving title, objective, and Moshe's responsibility from verified target/evidence context. Do not ask the user for fields that can be inferred. Ask at most one focused question only after lookup when a blocking ambiguity remains. The app server persists the returned handoff immediately; there is no separate approval step.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "minLength": 1, "maxLength": 240},
                "objective": {"type": "string", "minLength": 1, "maxLength": 4000},
                "responsibility": {"type": "string", "minLength": 1, "maxLength": 2000},
            },
            "required": ["title", "objective", "responsibility"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
    },
    {
        "name": "prepare_workstream_indication_proposal",
        "title": "Prepare a workstream indication proposal",
        "description": "Resolve REC evidence and an optional read-only TGT subject, then return a bounded proposal for the user to review in chat. Never persists an artifact or changes a target.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": sorted(WORKSTREAM_ACTIONS)},
                "proposed_turn_message_id": {"type": "string", "minLength": 1},
                "record_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 100},
                "target_id": {"type": "string"},
                "artifact_id": {"type": "string"},
                "expected_revision": {"type": "integer", "minimum": 1},
                "lead_statement": {"type": "string"},
                "indications": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "record_id": {"type": "string"},
                            "role": {"type": "string", "enum": ["supports", "contradicts", "context"]},
                            "relevance": {"type": "string"},
                            "annotation": {"type": "string"},
                        },
                        "required": ["record_id"],
                        "additionalProperties": False,
                    },
                    "maxItems": 100,
                },
                "payload": {"type": "object"},
                "supporting_signals": {"type": "array", "items": {"type": "string"}, "maxItems": 50},
                "contradictions": {"type": "array", "items": {"type": "string"}, "maxItems": 50},
                "assessment_questions": {"type": "array", "items": {"type": "string"}, "maxItems": 50},
                "gaps": {"type": "array", "items": {"type": "string"}, "maxItems": 50},
                "assigned_to": {"type": "string"},
                "annotation": {"type": "string"},
            },
            "required": ["action", "proposed_turn_message_id"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "decide_workstream_indication_proposal",
        "title": "Interpret a workstream proposal decision",
        "description": "Return a structured confirm, reject, correction, clarification, or assessment-handoff decision for an existing staged proposal. Never persists state.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "proposal": {"type": "object"},
                "decision": {"type": "string", "enum": ["confirm", "reject", "correct", "clarify", "send_to_assessment"]},
                "current_turn_message_id": {"type": "string", "minLength": 1},
                "confirmation_text": {"type": "string"},
                "corrected_proposal": {"type": "object"},
            },
            "required": ["proposal", "decision", "current_turn_message_id"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "present_requested_results",
        "title": "Present only the requested results",
        "description": "Final presentation-selection tool. Call once after analysis when requested results or materially relevant evidence references exist. Put only data directly requested by the user in layers. Put only canonical records that materially support the final conclusion in evidence_layers, grouped into meaningful map/timeline layers. Never include intermediate searches, rejected candidates, duplicate checks, or unrelated tool output. Canonical IDs are validated, and aggregate IDs must come from an earlier aggregate_events result in this run.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "layers": {
                    "type": "array",
                    "maxItems": 5,
                    "items": {
                        "type": "object",
                        "properties": {
                            "kind": {"type": "string", "enum": ["events", "locations", "entities", "attack_targets", "aggregate_groups"]},
                            "ids": {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 1, "maxItems": MAX_LIMIT},
                            "label": {"type": "string", "minLength": 1, "maxLength": 120},
                            "view": {"type": "string", "enum": ["map", "timeline", "evidence"]},
                            "group_by": {"type": "string", "description": "Required only for aggregate_groups and must match an earlier aggregate_events call."},
                        },
                        "required": ["kind", "ids", "label", "view"],
                        "additionalProperties": False,
                    },
                },
                "evidence_layers": {
                    "type": "array",
                    "maxItems": 5,
                    "items": {
                        "type": "object",
                        "properties": {
                            "kind": {"type": "string", "enum": ["events", "locations", "entities", "attack_targets", "aggregate_groups"]},
                            "ids": {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 1, "maxItems": MAX_LIMIT},
                            "label": {"type": "string", "minLength": 1, "maxLength": 120},
                            "view": {"type": "string", "enum": ["map", "timeline"]},
                            "group_by": {"type": "string", "description": "Required only for aggregate_groups and must match an earlier aggregate_events call."},
                        },
                        "required": ["kind", "ids", "label", "view"],
                        "additionalProperties": False,
                    },
                },
            },
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "prepare_target_candidate",
        "title": "Prepare a fused target candidate",
        "description": "Starting from visible seed evidence, retrieves and ranks nearby independent public corroboration, selects the strongest evidence pair, groups sources, reconciles quantity, builds compact evidence snapshots, and reports whether medium/high-confidence persistence is allowed. Returns pair scores, reasons, alternatives, and an ambiguity margin. It does not save anything.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "event_ids": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": MAX_LIMIT},
                "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
                "discover_corroboration": {"type": "boolean", "description": "Defaults to true. Set false only to validate an already selected evidence set without retrieval."},
            },
            "required": ["event_ids", "confidence"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "find_duplicate_target_candidates",
        "title": "Find duplicate target candidates",
        "description": "Checks the candidate bank for the same assessed object, canonical location/entity, or overlapping evidence before creation.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "object_class": {"type": "string", "minLength": 1},
                "location_id": {"type": "string", "minLength": 1},
                "entity_id": {"type": "string"},
                "event_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_LIMIT},
                "limit": {"type": "integer", "minimum": 1, "maximum": 500},
            },
            "required": ["object_class", "location_id", "event_ids"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "search_target_candidates",
        "title": "Search attack-target candidates",
        "description": "Search final-state candidate targets by exact assessed object class, canonical entity/location, mission run, or raw record ID. A record_id lookup returns every target containing that raw record while preserving each target's full summary. Returns summaries only; use get_target_candidate for evidence.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "object_class": {"type": "string"}, "entity_id": {"type": "string"},
                "location_id": {"type": "string"}, "mission_run_id": {"type": "string"},
                "record_id": {"type": "string", "description": "Exact raw-data record ID, for example REC-V2-009058."},
                "limit": {"type": "integer", "minimum": 1, "maximum": 500},
            },
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "get_target_candidate",
        "title": "Get attack-target candidate",
        "description": "Read one candidate target and its compact evidence snapshots by target ID.",
        "inputSchema": with_step_bridge({"type": "object", "properties": {"target_id": {"type": "string"}}, "required": ["target_id"], "additionalProperties": False}),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "create_target_candidate",
        "title": "Create attack-target candidate",
        "description": "Create one medium/high-confidence final-state candidate and its evidence atomically. Requires at least two independent source groups and canonical record/location/entity IDs.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "candidate": {"type": "object", "properties": TARGET_CANDIDATE_PROPERTIES, "required": TARGET_CREATE_REQUIRED, "additionalProperties": False},
                "evidence": {"type": "array", "items": TARGET_EVIDENCE_SCHEMA, "minItems": 2},
            },
            "required": ["candidate", "evidence"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
    },
    {
        "name": "update_target_candidate",
        "title": "Update attack-target candidate",
        "description": "Update assessed fields on an existing candidate. Status, creator, timestamps, review fields, raw SQL, and deletion are not accepted.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "target_id": {"type": "string"},
                "changes": {"type": "object", "properties": {key: value for key, value in TARGET_CANDIDATE_PROPERTIES.items() if key not in {"target_id", "created_by"}}, "minProperties": 1, "additionalProperties": False},
            },
            "required": ["target_id", "changes"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "attach_target_evidence",
        "title": "Attach evidence to attack-target candidate",
        "description": "Atomically attach new compact evidence snapshots to an existing candidate. Existing evidence cannot be edited or deleted.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {"target_id": {"type": "string"}, "evidence": {"type": "array", "items": TARGET_EVIDENCE_SCHEMA, "minItems": 1}},
            "required": ["target_id", "evidence"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
    },
    {
        "name": "classify_question_intent",
        "title": "Classify analyst question intent",
        "description": "Classify the analyst question using MCP sampling when available. The tool asks the host model to infer intent from natural language, then returns normalized recommended_mode, tool_budget, allowed tool families, blocked tool families, and recommended_view_hint. If sampling is unavailable or fails, it falls back to a deterministic classifier.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "conversation_context": {"type": "string"},
            },
            "required": ["question"],
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "plan_next_investigation_step",
        "title": "Plan next investigation step",
        "description": "Process-control checkpoint for investigations. It does not search data or decide truth. It checks candidate chain state, pending recommended seeds, untraced clues, linkage checks, and remaining budget, then returns procedural constraints for the next step. Use after tools return recommended_next_seeds/new_clues_to_trace and before challenge_hypothesis or final summary.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "objective": {"type": "string"},
                "candidate_chain_event_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_LIMIT},
                "pending_recommended_seeds": {"type": "array", "items": {"type": "string"}, "maxItems": 30},
                "expanded_seed_event_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_LIMIT},
                "new_clues_to_trace": {"type": "array", "items": {"type": "string"}, "maxItems": 30},
                "linkage_checks_done": {
                    "type": "array",
                    "items": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 2},
                    "maxItems": 50,
                },
                "semantic_calls_used": {"type": "integer", "minimum": 0},
                "related_calls_used": {"type": "integer", "minimum": 0},
                "tool_budget_remaining": {"type": "integer", "minimum": 0},
            },
            "required": ["objective"],
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "search_events",
        "title": "Search intelligence events",
        "description": "Search the synthetic event dataset using deterministic filters. Use location IDs from resolve_location and ISO-8601 UTC timestamps. Returns explicit event IDs and evidence rows. Supports explicit sorting by timestamp, relevance score, or event_id. Coverage is mandatory by default: broad searches are normalized to the maximum bounded coverage limit of 2000 even if a smaller limit is supplied. If truncated=true, do not treat returned rows as exhaustive; narrow filters or report the coverage gap.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "start_time": {"type": "string", "description": "Inclusive ISO-8601 UTC start time."},
                "end_time": {"type": "string", "description": "Inclusive ISO-8601 UTC end time."},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "entity_ids": {"type": "array", "items": {"type": "string"}},
                "actors": {"type": "array", "items": {"type": "string"}, "description": "Compatibility only. Prefer entity_ids from resolve_entity/get_objects."},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "reliabilities": {"type": "array", "items": {"type": "string"}},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "event_ids": {"type": "array", "items": {"type": "string"}},
                "night_only": {"type": "boolean", "description": "Keep events between 20:00 and 06:00 UTC."},
                "match_all_keywords": {"type": "boolean"},
                "sort_by": {"type": "string", "enum": ["timestamp", "score", "event_id"], "description": "Sort returned raw rows. Use timestamp asc for earliest events; use score desc for relevance-ranked keyword searches."},
                "sort_order": {"type": "string", "enum": ["asc", "desc"]},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Requested maximum returned rows. Broad retrieval is normalized to 2000 by coverage policy; smaller values are not proof of absence."},
            },
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "semantic_search_events",
        "title": "Semantic event search",
        "description": "Retrieve events by corpus-level semantic similarity over enriched event text. Use when the analyst's wording may not match exact keywords, when tracing paraphrased claims, or when broad fuzzy recall is needed. This does not replace exact filters, IDs, aggregation, or identifier tracing. Results are auditable event rows with REC IDs and semantic scores.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural-language retrieval query in Hebrew or English."},
                "seed_event_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 50, "description": "Optional seed events; their summaries are appended to the semantic query."},
                "start_time": {"type": "string", "description": "Optional inclusive ISO-8601 UTC start time."},
                "end_time": {"type": "string", "description": "Optional inclusive ISO-8601 UTC end time."},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "entity_ids": {"type": "array", "items": {"type": "string"}},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "reliabilities": {"type": "array", "items": {"type": "string"}},
                "certainty_levels": {"type": "array", "items": {"type": "string"}},
                "keywords": {"type": "array", "items": {"type": "string"}, "description": "Optional exact terms that must also appear in enriched event text."},
                "match_all_keywords": {"type": "boolean", "description": "If true, all keywords must match; otherwise any keyword may match."},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_SEMANTIC_LIMIT, "description": "Maximum semantic candidates returned. Use deterministic search and aggregation for exhaustive coverage."},
            },
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "get_objects",
        "title": "Get layer objects",
        "description": "Retrieve exact objects from the event, location, and entity layers. Use object_type=event before citing raw evidence; use location/entity/all when the answer should present those layers.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "object_type": {"type": "string", "enum": ["event", "location", "entity", "all"], "description": "Layer object type to retrieve."},
                "event_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_LIMIT},
                "location_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_LIMIT},
                "entity_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_LIMIT},
                "names_or_aliases": {"type": "array", "items": {"type": "string"}, "maxItems": 100, "description": "Optional names or aliases to resolve within location/entity layers."},
            },
            "required": ["object_type"],
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "resolve_location",
        "title": "Resolve geographic reference",
        "description": "Resolve a Hebrew place or area phrase to known location IDs and coordinates.",
        "inputSchema": with_step_bridge({"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"], "additionalProperties": False}),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "resolve_event_reference",
        "title": "Resolve event reference",
        "description": "Resolve a natural-language event reference to anchor events. When MCP sampling is available, the tool asks the host model for bounded visible search phrases, location terms, and actor terms, then uses direct DB matching plus hybrid semantic retrieval to generate candidate anchors. It never uses hidden scenario labels.",
        "inputSchema": with_step_bridge({"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"], "additionalProperties": False}),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "find_actor_history",
        "title": "Find actor history",
        "description": "Find prior or subsequent appearances of entities with optional time, location, source, and night filters. Prefer entity_ids. Natural-language actor names are accepted only as compatibility input and resolved through the entity DB.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "actors": {"type": "array", "items": {"type": "string"}, "description": "Compatibility only: natural-language entity names or aliases. Prefer entity_ids."},
                "entity_ids": {"type": "array", "items": {"type": "string"}, "description": "Canonical entity IDs from resolve_entity or get_objects."},
                "start_time": {"type": "string"}, "end_time": {"type": "string"},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "night_only": {"type": "boolean"},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Requested maximum returned rows. Broad actor history is normalized to 2000 by coverage policy."},
            },
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "aggregate_events",
        "title": "Aggregate event results",
        "description": "Count all matching events by location, municipality, actor, source, hour, or date using the same filters as search_events. Aggregation is exhaustive over the filtered population; use top_n to limit only the number of groups returned. For grouped timelines, set include_first_last=true and sort_by=first_event_time. Use this before broad investigative sampling to understand the distribution and choose narrowing filters.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "group_by": {"type": "string", "enum": ["location", "municipality", "actor", "entity", "source", "hour", "date"]},
                "start_time": {"type": "string"}, "end_time": {"type": "string"},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "entity_ids": {"type": "array", "items": {"type": "string"}},
                "actors": {"type": "array", "items": {"type": "string"}, "description": "Compatibility only. Prefer entity_ids."},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "night_only": {"type": "boolean"},
                "top_n": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT},
                "include_first_last": {"type": "boolean", "description": "When true, each group includes first_event_id/time/location and last_event_id/time/location from the complete filtered population."},
                "sort_by": {"type": "string", "enum": ["count", "first_event_time", "last_event_time", "label"], "description": "Sort groups by count, first event time, last event time, or label."},
                "sort_order": {"type": "string", "enum": ["asc", "desc"]},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Compatibility only: aggregation counts the complete filtered population. Use top_n to limit displayed groups; use search_events when raw rows are needed."},
            },
            "required": ["group_by"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "explain_linkage",
        "title": "Explain evidence linkage",
        "description": "Deterministically explain whether two events are connected by a shared identifier, entity/alias, time, location, or semantic overlap. Use this before presenting a transition in an investigative chain.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "first_event_id": {"type": "string"},
                "second_event_id": {"type": "string"},
            },
            "required": ["first_event_id", "second_event_id"],
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "build_event_sequence",
        "title": "Build chronological event sequence",
        "description": "Order selected evidence by time and derive a first-appearance geographic route for map and timeline presentation.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {"event_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_LIMIT}},
            "required": ["event_ids"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "resolve_entity",
        "title": "Resolve entity and aliases",
        "description": "Resolve an actor name to a canonical synthetic entity, aliases, cautious relationship links, confidence, and provenance. Use before exact actor searches when names may vary.",
        "inputSchema": with_step_bridge({
            "type": "object", "properties": {"query": {"type": "string"}},
            "required": ["query"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "trace_identifier",
        "title": "Trace an operational identifier",
        "description": "Find every event that contains an exact operational identifier such as a container number, warehouse reference, or monetary amount.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "identifier": {"type": "string"},
                "identifier_type": {"type": "string", "enum": ["container", "warehouse", "amount"]},
                "start_time": {"type": "string", "description": "Optional inclusive ISO-8601 UTC start time."},
                "end_time": {"type": "string", "description": "Optional inclusive ISO-8601 UTC end time."},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "include_negated": {
                    "type": "boolean",
                    "description": (
                        "Defaults to false and should stay false for normal identifier tracing or main-chain construction. "
                        "Set true only for explicit contradiction, negation, or alternative-explanation checks; do not mix negated matches into the primary evidence chain."
                    ),
                },
            },
            "required": ["identifier"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "trace_semantic_clues",
        "title": "Trace operational semantic clues",
        "description": "Find events that mention or semantically match operational clue terms such as border-crossing claims, roadblocks, KFOR/EULEX presence, police activity, shooting or explosion claims, media reports, rumors, contradiction language, or other semantic hints extracted from seed events. With MCP sampling, the tool expands clue phrases, then uses hybrid semantic retrieval plus clue-specific scoring to retrieve current matches. Use when the chain changes from a formal REC/LOC identifier to descriptive language. Negated benign records are excluded by default. Returns up to 3 recommended_next_seeds and new_clues_to_trace; use these before judging the chain or challenging the hypothesis.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "clues": {"type": "array", "items": {"type": "string"}},
                "seed_event_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 50},
                "start_time": {"type": "string", "description": "Optional inclusive ISO-8601 UTC start time."},
                "end_time": {"type": "string", "description": "Optional inclusive ISO-8601 UTC end time."},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "include_negated": {
                    "type": "boolean",
                    "description": "Defaults to false. Set true only for contradiction or alternative checks, not for main-chain discovery.",
                },
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Requested maximum returned clue matches. Broad clue tracing is normalized to 2000 by coverage policy."},
            },
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "find_related_events",
        "title": "Expand from seed evidence",
        "description": "Rank events related to seed evidence through explicit entity IDs/aliases, shared identifiers, operational semantic clues, hybrid semantic similarity, temporal proximity, geographic proximity, and optional source-type filtering. Unknown or non-informative entity names are not treated as evidence bridges. Semantic similarity is a supporting signal, not a replacement for concrete bridges. Every candidate includes linkage reasons and weights. With MCP sampling, the tool may rerank only the deterministic top candidates; it cannot introduce outside event IDs. Returns up to 3 recommended_next_seeds and new_clues_to_trace for bounded frontier expansion. Coverage is mandatory by default: broad expansion is normalized to 2000 even if a smaller limit is supplied; if total_candidates is larger than returned, treat results as incomplete and narrow or report the gap.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "seed_event_ids": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 50},
                "dimensions": {"type": "array", "items": {"type": "string", "enum": ["entity", "identifier", "time", "location", "semantic"]}},
                "source_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional event/source channel filter for candidate events. Use only source_type values that exist in the dataset, for example טלגרם, טיקטוק, X, פייסבוק, חדשות מקומיות, הודעת דובר, קבוצת וואטסאפ, שמועה מקומית, בלוג פוליטי, or ערוץ חדשות בינלאומי.",
                },
                "before_hours": {"type": "number", "minimum": 0, "maximum": 168},
                "after_hours": {"type": "number", "minimum": 0, "maximum": 168},
                "distance_km": {"type": "number", "minimum": 0, "maximum": 500},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Requested maximum returned candidates. Broad expansion is normalized to 2000 by coverage policy."},
            },
            "required": ["seed_event_ids"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "compare_location_claims",
        "title": "Compare geographic claims",
        "description": "Detect visible geographic-conflict signals by grouping similar reports, media claims, rumors, or repeated narratives across different locations. Uses only visible fields, including certainty_level and source_reliability_label; it does not know ground truth and must not be treated as proof of the correct location. With MCP sampling, the tool adds a cautious textual assessment of the returned groups only. Use for questions about wrong location claims, old videos, repeated rumors across places, or geographic deception.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "seed_event_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 50},
                "keywords": {"type": "array", "items": {"type": "string"}, "description": "Visible claim terms to compare, such as סרטון, תמונה, חציית גבול, שיירה, KFOR, מחסום."},
                "start_time": {"type": "string", "description": "Optional inclusive ISO-8601 UTC start time."},
                "end_time": {"type": "string", "description": "Optional inclusive ISO-8601 UTC end time."},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "time_window_hours": {"type": "number", "minimum": 1, "maximum": 168, "description": "Used around seed events when start/end are not supplied."},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Requested maximum conflict groups. Broad comparison is normalized to 2000 by coverage policy."},
            },
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "challenge_hypothesis",
        "title": "Challenge an investigative hypothesis",
        "description": "Profile supplied evidence, surface nearby benign or contradictory alternatives, and identify evidentiary gaps. With MCP sampling, the tool adds competing hypotheses and concrete disproof tests based only on the supplied evidence and deterministic alternatives. This tool does not decide whether the hypothesis is true. In chain/identifier investigations, use only after related expansion and linkage checks have produced a candidate chain with at least 3-5 supporting events, or after at least two explicit targeted searches failed. Do not use it early based only on one or two seed records.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "hypothesis": {"type": "string"},
                "supporting_event_ids": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": MAX_LIMIT},
            },
            "required": ["hypothesis", "supporting_event_ids"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
]

TOOL_HANDLERS = {
    "prepare_workstream_creation": prepare_workstream_creation,
    "prepare_workstream_indication_proposal": prepare_workstream_indication_proposal,
    "decide_workstream_indication_proposal": decide_workstream_indication_proposal,
    "present_requested_results": present_requested_results,
    "prepare_target_candidate": prepare_target_candidate,
    "find_duplicate_target_candidates": find_duplicate_target_candidates,
    "search_target_candidates": search_target_candidates,
    "get_target_candidate": get_target_candidate,
    "create_target_candidate": create_target_candidate,
    "update_target_candidate": update_target_candidate,
    "attach_target_evidence": attach_target_evidence,
    "classify_question_intent": classify_question_intent,
    "plan_next_investigation_step": plan_next_investigation_step,
    "search_events": search_events,
    "semantic_search_events": semantic_search_events,
    "get_objects": get_objects,
    "resolve_location": resolve_location,
    "resolve_event_reference": resolve_event_reference,
    "find_actor_history": find_actor_history,
    "aggregate_events": aggregate_events,
    "explain_linkage": explain_linkage,
    "build_event_sequence": build_event_sequence,
    "resolve_entity": resolve_entity,
    "trace_identifier": trace_identifier,
    "trace_semantic_clues": trace_semantic_clues,
    "find_related_events": find_related_events,
    "compare_location_claims": compare_location_claims,
    "challenge_hypothesis": challenge_hypothesis,
}


def response(request_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error_response(request_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    error = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": error}


def handle_message(message: dict[str, Any]) -> dict[str, Any] | None:
    global CLIENT_SUPPORTS_SAMPLING
    request_id = message.get("id")
    method = message.get("method")
    params = message.get("params") or {}

    if request_id is None:
        return None
    if method == "initialize":
        capabilities = params.get("capabilities") or {}
        CLIENT_SUPPORTS_SAMPLING = "sampling" in capabilities
        requested_version = params.get("protocolVersion", PROTOCOL_VERSION)
        negotiated = requested_version if requested_version in {PROTOCOL_VERSION, "2024-11-05"} else PROTOCOL_VERSION
        return response(
            request_id,
            {
                "protocolVersion": negotiated,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "title": "Serbia Events POC", "version": SERVER_VERSION},
                "instructions": (
                    "Read-only synthetic intelligence data. Cite only event IDs returned by tools. "
                    "Resolve geographic, event, and entity references before broad searches. "
                    "Trace concrete identifiers, use semantic_search_events for fuzzy or paraphrased retrieval, trace semantic clues when a chain shifts from IDs to descriptive claims, location, actor, media, disinformation, or movement language, use plan_next_investigation_step as a process-control checkpoint after recommended seeds or before challenge/final summary, expand iteratively from strong seed evidence, and use aggregate_events before broad sampling. "
                    "Keep result sets bounded but do not use low limits as proof of absence: if total/truncated or total_candidates/returned show sampling, narrow filters or raise limits before selecting investigative seeds. "
                    "Challenge hypotheses only after a candidate chain has enough supporting evidence or after explicit failed searches."
                ),
            },
        )
    if method == "ping":
        return response(request_id, {})
    if method == "tools/list":
        return response(request_id, {"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        handler = TOOL_HANDLERS.get(name)
        if handler is None:
            return error_response(request_id, -32602, f"Unknown tool: {name}")
        started = time.perf_counter()
        try:
            result = handler(arguments)
            write_audit(name, arguments, result, duration_ms=(time.perf_counter() - started) * 1000)
            return response(request_id, text_result(result))
        except (ValueError, TypeError, KeyError) as exc:
            result = {"error": str(exc)}
            write_audit(name, arguments, result, is_error=True, duration_ms=(time.perf_counter() - started) * 1000)
            return response(request_id, text_result(result, is_error=True))
        except Exception as exc:  # pragma: no cover - boundary safety
            return response(request_id, text_result({"error": "Internal tool failure", "detail": str(exc)}, is_error=True))
    return error_response(request_id, -32601, f"Method not found: {method}")


def main() -> int:
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    if not DATA_PATH.exists():
        print(f"Dataset not found: {DATA_PATH}", file=sys.stderr, flush=True)
        return 1
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            output = handle_message(message)
        except json.JSONDecodeError as exc:
            output = error_response(None, -32700, "Parse error", str(exc))
        if output is not None:
            print(json.dumps(output, ensure_ascii=False, separators=(",", ":")), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

