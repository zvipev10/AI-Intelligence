#!/usr/bin/env python3
"""Read-only MCP server for the synthetic Hebrew intelligence event dataset."""

from __future__ import annotations

import csv
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


PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "serbia-events-poc"
SERVER_VERSION = "0.2.0"
DEFAULT_LIMIT = 2000
MAX_LIMIT = 2000

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = Path(os.environ.get("INTELLIGENCE_POC_DATA", BASE_DIR / "data" / "serbia_kosovo_events_projection.csv"))
LOCATIONS_PATH = Path(os.environ.get("INTELLIGENCE_POC_LOCATIONS", BASE_DIR / "data" / "serbia_kosovo_locations.json"))
AUDIT_PATH = Path(os.environ.get("INTELLIGENCE_POC_AUDIT", BASE_DIR / "mcp_audit.jsonl"))
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

ENTITY_REGISTRY = {
    "ENT-KFOR": {
        "canonical_name": "KFOR",
        "aliases": ["KFOR", "כוח קפור", "קפור"],
        "entity_type": "כוח בינלאומי",
        "confidence": "גבוהה",
        "basis": "שם ארגון מוכר ברשומות הסינתטיות",
        "relationships": [],
    },
    "ENT-EULEX": {
        "canonical_name": "EULEX",
        "aliases": ["EULEX", "יולקס"],
        "entity_type": "משימה אירופית",
        "confidence": "גבוהה",
        "basis": "שם ארגון מוכר ברשומות הסינתטיות",
        "relationships": [],
    },
    "ENT-KOSOVO-POLICE": {
        "canonical_name": "משטרת קוסובו",
        "aliases": ["משטרת קוסובו", "כוחות קוסובו", "כוח קוסוברי", "סיור קוסוברי"],
        "entity_type": "כוח ביטחוני",
        "confidence": "בינונית",
        "basis": "וריאציות שמיות בדיווחים",
        "relationships": [],
    },
    "ENT-SERBIAN-ACTORS": {
        "canonical_name": "מפגינים סרבים מקומיים",
        "aliases": ["מפגינים סרבים מקומיים", "תושבים סרבים", "קבוצות סרביות", "צבא סרביה"],
        "entity_type": "שחקן אזרחי/מדיני",
        "confidence": "בינונית",
        "basis": "קבוצת שמות סמנטית לצורכי סימולציה",
        "relationships": [],
    },
}

IDENTIFIER_PATTERNS = {
    "record": re.compile(r"\bREC-\d{6}\b", re.IGNORECASE),
    "location": re.compile(r"\bLOC-\d{3}\b", re.IGNORECASE),
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
EVENTS_BY_ID = {event["event_id"]: event for event in EVENTS}


def public_event(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": event["event_id"],
        "timestamp_utc": event["timestamp_utc"],
        "source_type": event["source_type"],
        "source_reliability": event["source_reliability"],
        "certainty_level": event.get("certainty_level", ""),
        "source_reliability_label": event.get("source_reliability_label", ""),
        "entity_or_actor": event["entity_or_actor"],
        "location_id": event["location_id"],
        "location_name": event["location_name"],
        "location_type": event["location_type"],
        "event_summary": event["event_summary"],
    }


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
        "דיווח אזרחי": 7,
        "טלגרם": 7,
        "טיקטוק": 6,
        "פייסבוק": 6,
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
    for entity_id, entity in ENTITY_REGISTRY.items():
        aliases = entity["aliases"]
        exact = [alias for alias in aliases if normalize_text(alias) == folded]
        partial = [alias for alias in aliases if folded and folded in normalize_text(alias)]
        if exact or partial:
            matches.append({"entity_id": entity_id, **entity, "match_type": "exact" if exact else "partial"})
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
    actor_counts = Counter(event["entity_or_actor"] for event in EVENTS)
    for match in matches:
        match["event_counts_by_alias"] = {
            alias: actor_counts[alias] for alias in match["aliases"] if actor_counts[alias]
        }
        for relationship in match["relationships"]:
            related = ENTITY_REGISTRY.get(relationship["entity_id"], {})
            relationship["canonical_name"] = related.get("canonical_name")
    return {"query": query, "matches": matches, "match_count": len(matches)}


def intent_defaults(intent: str, has_geo: bool = False, has_timeline: bool = False) -> dict[str, Any]:
    if intent == "investigation":
        intent = "investigation"
        recommended_mode = "investigation"
        confidence = "גבוהה"
        tool_budget = 30
        allowed = [
            "resolve", "search", "aggregate", "get", "trace_identifier", "trace_semantic_clues",
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
        allowed = ["resolve", "search", "aggregate", "get"]
        blocked = ["related_expansion", "hypothesis_challenge", "linkage"]
        view_hint = "map"
        reason = "השאלה מבקשת הצגה או ספירה לפי מיקום, ללא בקשת קשרים נסתרים."
    elif intent == "timeline_retrieval":
        intent = "timeline_retrieval"
        recommended_mode = "retrieval"
        confidence = "בינונית-גבוהה"
        tool_budget = 4
        allowed = ["resolve", "search", "get", "sequence"]
        blocked = ["related_expansion", "hypothesis_challenge", "linkage"]
        view_hint = "timeline"
        reason = "השאלה מבקשת סדר או עיתוי של אירועים קיימים."
    elif intent == "retrieval":
        intent = "retrieval"
        recommended_mode = "retrieval"
        confidence = "גבוהה"
        tool_budget = 3
        allowed = ["resolve", "search", "aggregate", "get"]
        blocked = ["related_expansion", "hypothesis_challenge", "linkage"]
        view_hint = "evidence"
        reason = "השאלה מבקשת שליפה, סינון, צמצום או ספירה של רשומות קיימות."
    else:
        intent = "retrieval"
        recommended_mode = "retrieval"
        confidence = "בינונית"
        tool_budget = 3
        allowed = ["resolve", "search", "aggregate", "get"]
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
        allowed = ["get_events", "find_related_events", "trace_semantic_clues", "explain_linkage"]
        blocked = ["challenge_hypothesis", "final_summary"]
        reason = "קיימים seeds מומלצים שעדיין לא הורחבו; אין לסכם או לאתגר השערה לפני טיפול בהם."
    elif new_clues and semantic_calls_used < 2:
        decision = "continue"
        next_step_constraint = "trace_new_clues"
        required_event_ids = []
        allowed = ["trace_semantic_clues", "search_events"]
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
        allowed = ["find_related_events", "trace_semantic_clues", "search_events"]
        blocked = ["challenge_hypothesis", "final_summary"]
        reason = "השרשרת עדיין קצרה ויש תקציב להרחבה מוגבלת לפני מסקנה."
    elif len(candidate_chain) >= 5:
        decision = "continue"
        next_step_constraint = "challenge_or_summarize_with_gaps"
        required_event_ids = candidate_chain[:20]
        allowed = ["challenge_hypothesis", "build_event_sequence", "get_events"]
        blocked = []
        reason = "קיימת שרשרת מועמדת מספקת או שה-frontier מוצה; מותר לבצע ביקורת השערה או סיכום עם פערים."
    else:
        decision = "stop"
        next_step_constraint = "summarize_with_gaps"
        required_event_ids = candidate_chain[:20]
        allowed = ["build_event_sequence", "get_events"]
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
    for event in EVENTS:
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
    seed_events = [EVENTS_BY_ID[event_id] for event_id in seed_ids if event_id in EVENTS_BY_ID]
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
    limit = bounded_limit(arguments.get("limit", MAX_LIMIT))
    normalized_clues = [(clue, normalize_text(clue)) for clue in clues]
    matches = []
    for event in EVENTS:
        if start and event["timestamp"] < start:
            continue
        if end and event["timestamp"] > end:
            continue
        if location_ids and event["location_id"] not in location_ids:
            continue
        if source_types and event["source_type"] not in source_types:
            continue
        haystack = normalize_text(" ".join([event["event_summary"], event["entity_or_actor"], event["location_name"]]))
        matched_clues = [clue for clue, folded in normalized_clues if folded and term_in_text(folded, haystack)]
        if not matched_clues:
            continue
        negated = event_has_negation(event)
        if negated and not include_negated:
            continue
        score = len(matched_clues) * 4
        if any(marker in event["event_summary"] for marker in DIRECT_OBSERVATION_MARKERS):
            score += 1
        if negated:
            score -= 4
        if any(marker in event["event_summary"] for marker in BENIGN_MARKERS):
            score -= 2
        matches.append({
            "score": score,
            "matched_clues": matched_clues,
            "mention_type": "negated" if negated else "direct",
            "event": public_event(event),
        })
    matches.sort(key=lambda item: (-item["score"], item["event"]["timestamp_utc"], item["event"]["event_id"]))
    selected = matches[:limit]
    seed_id_set = {event["event_id"] for event in seed_events}
    ranked_seeds = []
    for item in selected:
        event_id = item["event"]["event_id"]
        if event_id in seed_id_set:
            continue
        event = EVENTS_BY_ID.get(event_id)
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
        event = EVENTS_BY_ID.get(seed["event_id"])
        if not event:
            continue
        for clue in semantic_clues_from_text(event["event_summary"]):
            if clue not in clues and clue not in new_clues:
                new_clues.append(clue)
    return {
        "clues": clues,
        "seed_event_ids": [event["event_id"] for event in seed_events],
        "missing_seed_event_ids": [event_id for event_id in seed_ids if event_id not in EVENTS_BY_ID],
        "include_negated": include_negated,
        "start_time": arguments.get("start_time"),
        "end_time": arguments.get("end_time"),
        "location_ids": sorted(location_ids),
        "source_types": sorted(source_types),
        "event_ids": [item["event"]["event_id"] for item in selected],
        "matches": selected,
        "total_matches": len(matches),
        "returned": len(selected),
        "truncated": len(matches) > len(selected),
        "recommended_next_seeds": recommended_next_seeds,
        "new_clues_to_trace": list(dict.fromkeys(new_clues + llm_expanded_clues))[:8],
        "llm_expanded_clues": llm_expanded_clues,
        "llm_expansion_rationale": str((llm_expansion or {}).get("rationale") or "")[:500],
        "llm_assist_source": "mcp_sampling" if llm_expansion else "not_available",
    }


def find_related_events(arguments: dict[str, Any]) -> dict[str, Any]:
    seed_ids = arguments.get("seed_event_ids") or []
    seeds = [EVENTS_BY_ID[event_id] for event_id in seed_ids if event_id in EVENTS_BY_ID]
    if not seeds:
        return {"seed_event_ids": seed_ids, "missing_seed_event_ids": seed_ids, "related_events": [], "event_ids": []}
    dimensions = set(arguments.get("dimensions") or ["entity", "identifier", "semantic", "time", "location"])
    before_hours = max(0, min(float(arguments.get("before_hours", 24)), 168))
    after_hours = max(0, min(float(arguments.get("after_hours", 12)), 168))
    distance_km = max(0, min(float(arguments.get("distance_km", 25)), 500))
    source_types = set(arguments.get("source_types") or [])
    limit = bounded_limit(arguments.get("limit", MAX_LIMIT))
    informative_seed_actors = [seed["entity_or_actor"] for seed in seeds if is_informative_actor(seed["entity_or_actor"])]
    seed_entities = set().union(*(canonical_entity_ids(actor) for actor in informative_seed_actors))
    seed_identifiers = {
        (item["identifier_type"], normalize_text(item["value"]))
        for seed in seeds for item in extract_identifiers(seed["event_summary"])
    }
    seed_semantic_clues = set().union(*(set(semantic_clues_from_text(seed["event_summary"])) for seed in seeds))
    earliest = min(seed["timestamp"] for seed in seeds) - timedelta(hours=before_hours)
    latest = max(seed["timestamp"] for seed in seeds) + timedelta(hours=after_hours)
    ranked = []
    for event in EVENTS:
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
        if "entity" in dimensions and is_informative_actor(event["entity_or_actor"]):
            event_entities = canonical_entity_ids(event["entity_or_actor"])
            if seed_entities & event_entities:
                score += 5
                reasons.append({"dimension": "entity", "detail": "ישות קנונית או כינוי משותף", "weight": 5})
            elif any(is_informative_actor(seed["entity_or_actor"]) and event["entity_or_actor"] == seed["entity_or_actor"] for seed in seeds):
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
                        "entity_or_actor": item["event"]["entity_or_actor"],
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
        event = EVENTS_BY_ID.get(event_id)
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
        event = EVENTS_BY_ID.get(seed["event_id"])
        if not event:
            continue
        for clue in semantic_clues_from_text(event["event_summary"]):
            if clue not in new_clues:
                new_clues.append(clue)
    return {
        "seed_event_ids": [seed["event_id"] for seed in seeds],
        "missing_seed_event_ids": [event_id for event_id in seed_ids if event_id not in EVENTS_BY_ID],
        "dimensions": sorted(dimensions),
        "source_types": sorted(source_types),
        "related_events": selected,
        "event_ids": [item["event"]["event_id"] for item in selected],
        "total_candidates": len(ranked),
        "returned": len(selected),
        "truncated": len(ranked) > len(selected),
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
    seed_events = [EVENTS_BY_ID[event_id] for event_id in seed_ids if event_id in EVENTS_BY_ID]
    keywords = [str(value).strip() for value in arguments.get("keywords") or [] if str(value).strip()]
    start = parse_time(arguments.get("start_time"))
    end = parse_time(arguments.get("end_time"))
    location_ids = set(arguments.get("location_ids") or [])
    source_types = set(arguments.get("source_types") or [])
    limit = bounded_limit(arguments.get("limit", 100))
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
    for event in EVENTS:
        if start and event["timestamp"] < start:
            continue
        if end and event["timestamp"] > end:
            continue
        if location_ids and event["location_id"] not in location_ids:
            continue
        if source_types and event["source_type"] not in source_types:
            continue
        haystack = normalize_text(" ".join([event["event_summary"], event["entity_or_actor"], event["location_name"], event["source_type"]]))
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
        "missing_seed_event_ids": [event_id for event_id in seed_ids if event_id not in EVENTS_BY_ID],
        "keywords": keywords,
        "start_time": start.isoformat().replace("+00:00", "Z") if start else None,
        "end_time": end.isoformat().replace("+00:00", "Z") if end else None,
        "location_ids": sorted(location_ids),
        "source_types": sorted(source_types),
        "candidate_event_count": len(candidates),
        "conflict_group_count": len(conflict_groups),
        "returned": len(selected_groups),
        "truncated": len(conflict_groups) > len(selected_groups),
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
    evidence = [EVENTS_BY_ID[event_id] for event_id in evidence_ids if event_id in EVENTS_BY_ID]
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
            event for event in EVENTS
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
        "missing_event_ids": [event_id for event_id in evidence_ids if event_id not in EVENTS_BY_ID],
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
    actors = {value.casefold() for value in arguments.get("actors") or []}
    source_types = set(arguments.get("source_types") or [])
    reliabilities = set(arguments.get("reliabilities") or [])
    keywords = [normalize_text(value) for value in arguments.get("keywords") or [] if value]
    event_ids = set(arguments.get("event_ids") or [])
    night_only = bool(arguments.get("night_only"))
    match_all_keywords = bool(arguments.get("match_all_keywords"))

    matches = []
    for event in EVENTS:
        if start and event["timestamp"] < start:
            continue
        if end and event["timestamp"] > end:
            continue
        if location_ids and event["location_id"] not in location_ids:
            continue
        if actors and event["entity_or_actor"].casefold() not in actors:
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
            " ".join([event["event_summary"], event["entity_or_actor"], event["location_name"], event["source_type"]])
        )
        if keywords:
            keyword_matches = [term_in_text(keyword, haystack) for keyword in keywords]
            if match_all_keywords and not all(keyword_matches):
                continue
            if not match_all_keywords and not any(keyword_matches):
                continue
        score = 0
        summary_folded = normalize_text(event["event_summary"])
        actor_folded = normalize_text(event["entity_or_actor"])
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
    limit = bounded_limit(arguments.get("limit"))
    selected = matches[:limit]
    return {
        "total": total,
        "returned": len(selected),
        "truncated": total > len(selected),
        "sort_by": arguments.get("sort_by") or ("score" if arguments.get("keywords") else "timestamp"),
        "sort_order": arguments.get("sort_order") or ("desc" if str(arguments.get("sort_by") or "").casefold() in {"score", "match_score", "relevance"} else "asc"),
        "event_ids": [event["event_id"] for _, event in selected],
        "events": [{**public_event(event), "match_score": score} for score, event in selected],
    }


def get_events(arguments: dict[str, Any]) -> dict[str, Any]:
    ids = arguments.get("event_ids") or []
    found = [EVENTS_BY_ID[event_id] for event_id in ids if event_id in EVENTS_BY_ID]
    missing = [event_id for event_id in ids if event_id not in EVENTS_BY_ID]
    return {
        "events": [public_event(event) for event in found],
        "missing_event_ids": missing,
    }


def resolve_location(arguments: dict[str, Any]) -> dict[str, Any]:
    query = str(arguments.get("query") or "").strip()
    exact_ids = AREA_ALIASES.get(query)
    if exact_ids:
        ids = exact_ids
    else:
        query_folded = query.casefold()
        ids = [
            location_id
            for location_id, location in LOCATIONS.items()
            if query_folded in location["name"].casefold() or query_folded in location["type"].casefold()
        ]
    return {
        "query": query,
        "location_ids": ids,
        "locations": [{"location_id": location_id, **LOCATIONS[location_id]} for location_id in ids],
    }


def resolve_event_reference(arguments: dict[str, Any]) -> dict[str, Any]:
    query = str(arguments.get("query") or "").strip()
    direct_ids = EVENT_REFERENCES.get(query, [])
    llm_interpretation = None
    if direct_ids:
        events = [EVENTS_BY_ID[event_id] for event_id in direct_ids if event_id in EVENTS_BY_ID]
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
        query_folded = query.casefold()
        scored_events = []
        for event in EVENTS:
            haystack = normalize_text(
                " ".join([event["event_summary"], event["event_id"], event["entity_or_actor"], event["location_name"], event["source_type"]])
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
                scored_events.append((score, matched_terms, event))
        scored_events.sort(key=lambda item: (-item[0], item[2]["timestamp"], item[2]["event_id"]))
        events = [event for _, _, event in scored_events[:20]]
    return {
        "query": query,
        "event_ids": [event["event_id"] for event in events],
        "events": [public_event(event) for event in events],
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
    expanded_actors = []
    seen = set()
    for actor in actors:
        matches = entity_matches(actor)
        candidates = [alias for match in matches for alias in match["aliases"]] or [actor]
        for candidate in candidates:
            folded = normalize_text(candidate)
            if folded not in seen:
                seen.add(folded)
                expanded_actors.append(candidate)
    forwarded = {
        "actors": expanded_actors,
        "start_time": arguments.get("start_time"),
        "end_time": arguments.get("end_time"),
        "location_ids": arguments.get("location_ids") or [],
        "source_types": arguments.get("source_types") or [],
        "night_only": arguments.get("night_only", False),
        "limit": arguments.get("limit", DEFAULT_LIMIT),
    }
    result = search_events(forwarded)
    result["requested_actors"] = actors
    result["expanded_actors"] = expanded_actors
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
        "actor": lambda event: event["entity_or_actor"],
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
    return result


def explain_linkage(arguments: dict[str, Any]) -> dict[str, Any]:
    first_id = arguments.get("first_event_id")
    second_id = arguments.get("second_event_id")
    first = EVENTS_BY_ID.get(first_id)
    second = EVENTS_BY_ID.get(second_id)
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

    if is_informative_actor(first["entity_or_actor"]) and is_informative_actor(second["entity_or_actor"]):
        first_entities = canonical_entity_ids(first["entity_or_actor"])
        second_entities = canonical_entity_ids(second["entity_or_actor"])
        if first_entities & second_entities:
            bridges.append({
                "bridge_type": "shared_entity_or_alias",
                "confidence": "בינונית-גבוהה",
                "weight": 5,
                "detail": "ישות קנונית או כינוי משותף",
            })
        elif normalize_text(first["entity_or_actor"]) == normalize_text(second["entity_or_actor"]):
            bridges.append({
                "bridge_type": "same_actor_text",
                "confidence": "בינונית",
                "weight": 4,
                "detail": first["entity_or_actor"],
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
    if any(item["bridge_type"] in {"shared_identifier", "shared_entity_or_alias"} for item in bridges):
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
    events = [EVENTS_BY_ID[event_id] for event_id in ids if event_id in EVENTS_BY_ID]
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


TOOLS = [
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
        "description": "Search the synthetic event dataset using deterministic filters. Use location IDs from resolve_location and ISO-8601 UTC timestamps. Returns explicit event IDs and evidence rows. Supports explicit sorting by timestamp, relevance score, or event_id. For broad investigative or high-coverage searches, use limit=2000 unless the user explicitly asked for a small sample/TOP-N or the call is only validating selected records. If truncated=true, do not treat returned rows as exhaustive.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "start_time": {"type": "string", "description": "Inclusive ISO-8601 UTC start time."},
                "end_time": {"type": "string", "description": "Inclusive ISO-8601 UTC end time."},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "actors": {"type": "array", "items": {"type": "string"}},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "reliabilities": {"type": "array", "items": {"type": "string"}},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "event_ids": {"type": "array", "items": {"type": "string"}},
                "night_only": {"type": "boolean", "description": "Keep events between 20:00 and 06:00 UTC."},
                "match_all_keywords": {"type": "boolean"},
                "sort_by": {"type": "string", "enum": ["timestamp", "score", "event_id"], "description": "Sort returned raw rows. Use timestamp asc for earliest events; use score desc for relevance-ranked keyword searches."},
                "sort_order": {"type": "string", "enum": ["asc", "desc"]},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Maximum returned rows. For broad discovery use 2000. Use values below 500 only for explicit small samples, TOP-N, or focused validation."},
            },
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "get_events",
        "title": "Get raw events",
        "description": "Retrieve exact raw evidence records by event ID. Use this before citing or presenting evidence.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {"event_ids": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_LIMIT}},
            "required": ["event_ids"],
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
        "description": "Resolve a natural-language event reference to anchor events. When MCP sampling is available, the tool first asks the host model for bounded visible search phrases, then performs deterministic DB matching. It never uses hidden scenario labels.",
        "inputSchema": with_step_bridge({"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"], "additionalProperties": False}),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "find_actor_history",
        "title": "Find actor history",
        "description": "Find prior or subsequent appearances of actors with optional time, location, source, and night filters. Known entity aliases are expanded automatically and returned explicitly. For investigative seed selection, avoid low limits on broad actor searches; narrow with time/location/source filters or use limit=2000.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "actors": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                "start_time": {"type": "string"}, "end_time": {"type": "string"},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "night_only": {"type": "boolean"},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Maximum returned rows. For broad actor history use 2000; low values are samples when total is higher."},
            },
            "required": ["actors"], "additionalProperties": False,
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
                "group_by": {"type": "string", "enum": ["location", "municipality", "actor", "source", "hour", "date"]},
                "start_time": {"type": "string"}, "end_time": {"type": "string"},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "actors": {"type": "array", "items": {"type": "string"}},
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
        "description": "Find events that mention operational clue terms such as border-crossing claims, roadblocks, KFOR/EULEX presence, police activity, shooting or explosion claims, media reports, rumors, contradiction language, or other semantic hints extracted from seed events. With MCP sampling, the tool may suggest additional follow-up clues, but it does not silently add those broad clues to the current retrieval. Use when the chain changes from a formal REC/LOC identifier to descriptive language. Negated benign records are excluded by default. Returns up to 3 recommended_next_seeds and new_clues_to_trace; use these before judging the chain or challenging the hypothesis.",
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
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Maximum returned clue matches. For broad clue tracing use 2000; use low values only for explicit samples or focused validation."},
            },
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "find_related_events",
        "title": "Expand from seed evidence",
        "description": "Rank events related to seed evidence through explicit entity aliases, shared identifiers, operational semantic clues, temporal proximity, geographic proximity, and optional source-type filtering. Unknown actors such as 'לא ידוע' are not treated as evidence bridges. Every candidate includes linkage reasons and weights. With MCP sampling, the tool may rerank only the deterministic top candidates; it cannot introduce outside event IDs. Returns up to 3 recommended_next_seeds and new_clues_to_trace for bounded frontier expansion. Default and broad-investigation limit is 2000. In investigation mode, do not use low limits such as 20, 150, or 500 for broad expansion; if total_candidates is much larger than returned, treat results as a sample and either narrow by source/time/location or run follow-up expansions before drawing conclusions.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "seed_event_ids": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 50},
                "dimensions": {"type": "array", "items": {"type": "string", "enum": ["entity", "identifier", "time", "location", "semantic"]}},
                "source_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional event/source type filter for candidate events, for example telephone metadata, signal intercepts, financial alerts, movement sensors, or port/customs records.",
                },
                "before_hours": {"type": "number", "minimum": 0, "maximum": 168},
                "after_hours": {"type": "number", "minimum": 0, "maximum": 168},
                "distance_km": {"type": "number", "minimum": 0, "maximum": 500},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Maximum returned candidates. Default is 2000. Use 2000 for broad investigative expansion; low values are samples."},
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
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Maximum conflict groups and per-group sample rows returned."},
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
    "classify_question_intent": classify_question_intent,
    "plan_next_investigation_step": plan_next_investigation_step,
    "search_events": search_events,
    "get_events": get_events,
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
                    "Trace concrete identifiers, trace semantic clues when a chain shifts from IDs to descriptive claims, location, actor, media, disinformation, or movement language, use plan_next_investigation_step as a process-control checkpoint after recommended seeds or before challenge/final summary, expand iteratively from strong seed evidence, and use aggregate_events before broad sampling. "
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
