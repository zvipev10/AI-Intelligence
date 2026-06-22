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
SERVER_NAME = "intelligence-events-poc"
SERVER_VERSION = "0.2.0"
DEFAULT_LIMIT = 100
MAX_LIMIT = 500

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = Path(os.environ.get("INTELLIGENCE_POC_DATA", BASE_DIR / "data" / "events_he_large.csv"))
AUDIT_PATH = Path(os.environ.get("INTELLIGENCE_POC_AUDIT", BASE_DIR / "mcp_audit.jsonl"))

LOCATIONS = {
    "L-201": {"name": "נמל חיפה", "type": "נמל", "latitude": 32.820, "longitude": 35.000},
    "L-202": {"name": "מתחם מחסנים קישון", "type": "אזור תעשייה", "latitude": 32.790, "longitude": 35.040},
    "L-203": {"name": "מעבר נהר הירדן", "type": "מעבר גבול", "latitude": 32.503, "longitude": 35.570},
    "L-204": {"name": "צומת גולני", "type": "צומת דרכים", "latitude": 32.782, "longitude": 35.409},
    "L-205": {"name": "שוק נצרת", "type": "מרכז עירוני", "latitude": 32.699, "longitude": 35.303},
    "L-206": {"name": "כביש גישה צדדי ליד בית שאן", "type": "דרך צדדית", "latitude": 32.505, "longitude": 35.500},
    "L-207": {"name": "אזור התעשייה בית שאן", "type": "אזור תעשייה", "latitude": 32.500, "longitude": 35.500},
    "L-208": {"name": "משרד סיוע מרחב בחיפה", "type": "משרד", "latitude": 32.815, "longitude": 34.995},
    "L-209": {"name": "מסוף דלק צמח", "type": "מסוף דלק", "latitude": 32.703, "longitude": 35.586},
}

AREA_ALIASES = {
    "בית שאן": ["L-206", "L-207", "L-203"],
    "אזור בית שאן": ["L-206", "L-207", "L-203"],
    "חיפה": ["L-201", "L-208", "L-202"],
    "קישון": ["L-202"],
    "צמח": ["L-209"],
    "גולני": ["L-204"],
    "נצרת": ["L-205"],
    "מעבר הגבול": ["L-203"],
    "מעבר נהר הירדן": ["L-203"],
}

EVENT_REFERENCES = {
    "אירוע הגבול": ["BORD-0001"],
    "מקבץ כלי הרכב ליד הגבול": ["BORD-0001"],
    "המכולה של משאבות ההשקיה": ["PORT-0090"],
    "יציאת המשאיות ממחסן 11": ["OBS-0002"],
    "היירוט ליד בית שאן": ["SIG-0002"],
}

ENTITY_REGISTRY = {
    "ENT-OFK": {
        "canonical_name": "אופק לוגיסטיקה",
        "aliases": ["אופק לוגיסטיקה", "אופק מטענים"],
        "entity_type": "משפחת חברות לוגיסטיקה",
        "confidence": "גבוהה",
        "basis": "שמות מסחריים מקושרים ברישומי הישות הסינתטיים",
        "relationships": [],
    },
    "ENT-LEVY": {
        "canonical_name": "אורי לוי",
        "aliases": ["אורי לוי", "א. לוי"],
        "entity_type": "אדם",
        "confidence": "בינונית",
        "basis": "קיצור שם ומזהי קשר היסטוריים; הזהות אינה ודאית",
        "relationships": [
            {
                "entity_id": "ENT-LEVY-MARINE",
                "relationship": "קשר היסטורי משותף",
                "confidence": "בינונית",
                "basis": "מספר קשר היסטורי משותף ברישומי הישות",
            }
        ],
    },
    "ENT-LEVY-MARINE": {
        "canonical_name": "לוי ימי",
        "aliases": ["לוי ימי"],
        "entity_type": "חברה מסחרית",
        "confidence": "גבוהה",
        "basis": "שם חברה רשום",
        "relationships": [
            {
                "entity_id": "ENT-LEVY",
                "relationship": "קשר היסטורי משותף",
                "confidence": "בינונית",
                "basis": "מספר קשר היסטורי משותף ברישומי הישות",
            }
        ],
    },
    "ENT-SANDGLASS": {
        "canonical_name": "חוליית שעון חול",
        "aliases": ["חוליית שעון חול", "שעון חול"],
        "entity_type": "חוליית לוגיסטיקה חשודה",
        "confidence": "בינונית",
        "basis": "שני דיווחים היסטוריים סינתטיים",
        "relationships": [
            {
                "entity_id": "ENT-BLUE-CRESCENT",
                "relationship": "קשר לוגיסטי שדווח בעבר",
                "confidence": "בינונית",
                "basis": "דפוס רכש ותנועה מתיק קודם",
            }
        ],
    },
    "ENT-BLUE-CRESCENT": {
        "canonical_name": "סהר כחול",
        "aliases": ["סהר כחול"],
        "entity_type": "רשת רכש חשודה",
        "confidence": "בינונית",
        "basis": "כינוי שהופיע בהפניות תשלום היסטוריות",
        "relationships": [
            {
                "entity_id": "ENT-SANDGLASS",
                "relationship": "קשר לוגיסטי שדווח בעבר",
                "confidence": "בינונית",
                "basis": "דפוס רכש ותנועה מתיק קודם",
            }
        ],
    },
}

IDENTIFIER_PATTERNS = {
    "container": re.compile(r"\b[A-Z]{2}-\d{4}\b", re.IGNORECASE),
    "warehouse": re.compile(r"מחסן\s*\d+"),
    "amount": re.compile(r"\b\d{1,3}(?:,\d{3})+\s*(?:ש[״\"]ח|שקל(?:ים)?)"),
}

BENIGN_MARKERS = (
    "אין קשר ידוע", "תנועה מסחרית רגילה", "פעילות אזרחית", "עומס מקומי",
    "ללא חריגה", "תחזוקה", "דלק", "אספקה חקלאית", "רעש סביבתי",
)

NEGATION_MARKERS = (
    "אין קשר ידוע", "אין מספרי מכולה משותפים", "ללא קשר", "לא קשור",
)

DIRECT_OBSERVATION_MARKERS = (
    "זוהה", "מציגה", "נכנסו", "יצאו", "עברו", "שוחררה", "הגיעה", "תשלום",
)

NON_INFORMATIVE_ACTORS = {
    "", "לא ידוע", "לא מזוהה", "גורם לא ידוע", "גורם לא מזוהה", "לא ברור",
}

SEMANTIC_CLUE_TERMS = (
    "משאבות", "משאבת", "אטמים", "מכולה", "מטען", "מטען מכוסה", "מכוסות",
    "משאיות", "משאית", "ארגז", "מחסן", "דרך צדדית", "הדרך הצדדית",
    "אחרי החשכה", "לאחר החשכה", "שקיעת הירח", "לחכות", "דלק", "כלי רכב כבדים",
    "לוחיות", "מוסתרות", "מסלול מזורז", "בדיקה פיזית", "תמונה תרמית",
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


def normalize_text(value: str) -> str:
    return " ".join(value.casefold().split())


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
        "התראה פיננסית": 8,
        "מטא-דאטה טלפוני": 8,
        "יירוט אות": 8,
        "חיישן תנועה": 7,
        "תצפית מקור": 7,
        "מצלמת דרך": 7,
        "תצפית רחפן": 7,
        "חיישן אקוסטי": 6,
        "חיישן גבול": 6,
        "רשומת מכס": 5,
        "רשומת נמל": 5,
    }
    if source in source_weights:
        score += source_weights[source]
        reasons.append(f"סוג מקור חקירתי: {source}")
    markers = [
        ("מחסן", 8, "רמז מחסן או נקודת מעבר"),
        ("משאיות", 7, "רמז תנועה של משאיות"),
        ("משאית", 7, "רמז תנועה של משאית"),
        ("מטען מכוסה", 7, "רמז מטען מכוסה"),
        ("מכוסות", 6, "רמז הסתרה או כיסוי"),
        ("דרך צדדית", 7, "רמז מסלול צדדי"),
        ("הדרך הצדדית", 7, "רמז מסלול צדדי"),
        ("משאבות", 5, "רמז תוכן מטען"),
        ("אטמים", 5, "רמז תוכן מטען"),
        ("דלק", 4, "רמז תזמון או הסחה"),
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


def classify_question_intent(arguments: dict[str, Any]) -> dict[str, Any]:
    question = str(arguments.get("question") or "").strip()
    context = str(arguments.get("conversation_context") or "").strip()
    text = normalize_text(f"{question} {context}")

    investigation_terms = [
        "דפוס", "קשרים נסתרים", "קשר נסתר", "חשוד", "חשודה", "חשד", "חקור", "חקירה",
        "הסברים חלופיים", "חלופות", "גורמים משותפים", "אירועים מקדימים", "תחילת",
        "מקור התרחיש", "תרחיש", "אובייקט", "רכיב מרכזי", "מטען עצמו", "האם הוא חלק",
        "למה", "הסבר", "סיבתי", "גורם", "חוליה", "שרשרת",
    ]
    retrieval_terms = [
        "תראה", "הצג", "הראה", "רשימה", "כל האירועים", "אירועים סביב", "תצמצם",
        "סנן", "כמה", "כמות", "top", "טופ", "מיקומים", "לפי", "רשומות", "אירועים של",
        "סביב", "הגעת", "מטענים", "מקורות", "טבלה",
    ]
    geographic_terms = ["מפה", "איפה", "מיקומים", "מוקדים", "מקבצים", "אזורים", "top 3", "טופ 3"]
    timeline_terms = ["ציר זמן", "סדר", "כרונולוג", "לפני", "אחרי", "מתי", "שעה", "רצף לפי זמן"]

    has_investigation = any(term in text for term in investigation_terms)
    has_retrieval = any(term in text for term in retrieval_terms)
    has_geo = any(term in text for term in geographic_terms)
    has_timeline = any(term in text for term in timeline_terms)

    if has_investigation:
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
    elif has_geo:
        intent = "geographic_aggregation"
        recommended_mode = "retrieval"
        confidence = "גבוהה"
        tool_budget = 3
        allowed = ["resolve", "search", "aggregate", "get"]
        blocked = ["related_expansion", "hypothesis_challenge", "linkage"]
        view_hint = "map"
        reason = "השאלה מבקשת הצגה או ספירה לפי מיקום, ללא בקשת קשרים נסתרים."
    elif has_timeline:
        intent = "timeline_retrieval"
        recommended_mode = "retrieval"
        confidence = "בינונית-גבוהה"
        tool_budget = 4
        allowed = ["resolve", "search", "get", "sequence"]
        blocked = ["related_expansion", "hypothesis_challenge", "linkage"]
        view_hint = "timeline"
        reason = "השאלה מבקשת סדר או עיתוי של אירועים קיימים."
    elif has_retrieval:
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
        "question": question,
        "intent": intent,
        "recommended_mode": recommended_mode,
        "confidence": confidence,
        "reason": reason,
        "tool_budget": tool_budget,
        "allowed_tool_families": allowed,
        "blocked_tool_families": blocked,
        "recommended_view_hint": view_hint,
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
    start = parse_time(arguments.get("start_time"))
    end = parse_time(arguments.get("end_time"))
    location_ids = set(arguments.get("location_ids") or [])
    source_types = set(arguments.get("source_types") or [])
    include_negated = bool(arguments.get("include_negated", False))
    limit = bounded_limit(arguments.get("limit", 500))
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
        "new_clues_to_trace": new_clues[:8],
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
    limit = bounded_limit(arguments.get("limit", 500))
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
        "assessment_note": "הכלי מתאר חוזק, חלופות ופערים באופן דטרמיניסטי; הסוכן חייב להעריך את ההשערה בעצמו.",
    }


def search_events(arguments: dict[str, Any]) -> dict[str, Any]:
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

    total = len(matches)
    limit = bounded_limit(arguments.get("limit"))
    if keywords:
        matches.sort(key=lambda item: (-item[0], item[1]["timestamp"], item[1]["event_id"]))
    selected = matches[:limit]
    return {
        "total": total,
        "returned": len(selected),
        "truncated": total > len(selected),
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
    if direct_ids:
        events = [EVENTS_BY_ID[event_id] for event_id in direct_ids if event_id in EVENTS_BY_ID]
    else:
        query_folded = query.casefold()
        events = [
            event
            for event in EVENTS
            if query_folded in event["event_summary"].casefold() or query_folded in event["event_id"].casefold()
        ][:20]
    return {
        "query": query,
        "event_ids": [event["event_id"] for event in events],
        "events": [public_event(event) for event in events],
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
    filtered = search_events({**arguments, "limit": MAX_LIMIT})
    events = [EVENTS_BY_ID[event_id] for event_id in filtered["event_ids"]]
    top_n = arguments.get("top_n")
    top_n = bounded_limit(top_n) if top_n is not None else None
    key_functions = {
        "location": lambda event: (event["location_id"], event["location_name"]),
        "actor": lambda event: event["entity_or_actor"],
        "source": lambda event: event["source_type"],
        "hour": lambda event: f"{event['timestamp'].hour:02d}:00",
        "date": lambda event: event["timestamp"].date().isoformat(),
    }
    if group_by not in key_functions:
        raise ValueError(f"Unsupported group_by: {group_by}")
    counts = Counter(key_functions[group_by](event) for event in events)
    groups = []
    for key, count in counts.most_common():
        if group_by == "location":
            location_id, label = key
            location = LOCATIONS.get(location_id, {})
            groups.append({
                "key": location_id,
                "label": label,
                "count": count,
                "location_id": location_id,
                "location_name": label,
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
            })
        else:
            groups.append({"key": str(key), "label": str(key), "count": count})
    if top_n is not None:
        groups = groups[:top_n]
    result = {"group_by": group_by, "total_events": len(events), "groups": groups}
    if group_by == "location":
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
        "description": "Deterministically classify the analyst question as retrieval, geographic aggregation, timeline retrieval, or investigation. Call this first for every analyst question to choose tool budget and workflow.",
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
        "description": "Search the synthetic event dataset using deterministic filters. Use location IDs from resolve_location and ISO-8601 UTC timestamps. Returns explicit event IDs and evidence rows. For broad investigative searches, avoid small samples: narrow first with time/source/keyword/entity filters or use a high limit up to 500. If truncated=true, do not treat returned rows as exhaustive.",
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
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Maximum returned rows. A low value is only a sample when total is higher; use up to 500 for broad investigative discovery."},
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
        "description": "Resolve a natural-language reference such as 'אירוע הגבול' to one or more anchor events.",
        "inputSchema": with_step_bridge({"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"], "additionalProperties": False}),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "find_actor_history",
        "title": "Find actor history",
        "description": "Find prior or subsequent appearances of actors with optional time, location, source, and night filters. Known entity aliases are expanded automatically and returned explicitly. For investigative seed selection, avoid low limits on broad actor searches; narrow with time/location/source filters or use a high limit up to 500.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "actors": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                "start_time": {"type": "string"}, "end_time": {"type": "string"},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "night_only": {"type": "boolean"},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Maximum returned rows. Low values are samples when total is higher; use high limits for investigation."},
            },
            "required": ["actors"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "aggregate_events",
        "title": "Aggregate event results",
        "description": "Count matching events by location, actor, source, hour, or date using the same filters as search_events. Use this before broad investigative sampling to understand the distribution and choose narrowing filters.",
        "inputSchema": with_step_bridge({
            "type": "object",
            "properties": {
                "group_by": {"type": "string", "enum": ["location", "actor", "source", "hour", "date"]},
                "start_time": {"type": "string"}, "end_time": {"type": "string"},
                "location_ids": {"type": "array", "items": {"type": "string"}},
                "actors": {"type": "array", "items": {"type": "string"}},
                "source_types": {"type": "array", "items": {"type": "string"}},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "night_only": {"type": "boolean"},
                "top_n": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Maximum events considered before grouping. Use up to 500 for broad distributions."},
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
        "description": "Find events that mention operational clue terms such as cargo/object words, warehouse/route phrases, covered movement, side-road timing, or other semantic hints extracted from seed events. Use when the chain changes from a formal identifier to descriptive language, for example from a container to cargo, trucks, route, or SIGINT wording. Negated benign records are excluded by default. Returns up to 3 recommended_next_seeds and new_clues_to_trace; use these before judging the chain or challenging the hypothesis.",
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
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Maximum returned clue matches. Use high limits for broad clue tracing."},
            },
            "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "find_related_events",
        "title": "Expand from seed evidence",
        "description": "Rank events related to seed evidence through explicit entity aliases, shared identifiers, operational semantic clues, temporal proximity, geographic proximity, and optional source-type filtering. Unknown actors such as 'לא ידוע' are not treated as evidence bridges. Every candidate includes linkage reasons and weights. Returns up to 3 recommended_next_seeds and new_clues_to_trace for bounded frontier expansion. Default limit is 500. In investigation mode, do not use low limits such as 20 or 150 for broad expansion; if total_candidates is much larger than returned, treat results as a sample and either raise limit, narrow by source/time/location, or run follow-up expansions before drawing conclusions.",
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
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT, "description": "Maximum returned candidates. Default is 500. Use 500 for broad investigative expansion; low values are samples."},
            },
            "required": ["seed_event_ids"], "additionalProperties": False,
        }),
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "challenge_hypothesis",
        "title": "Challenge an investigative hypothesis",
        "description": "Profile supplied evidence, surface nearby benign or contradictory alternatives, and identify evidentiary gaps. This tool does not decide whether the hypothesis is true. In chain/identifier investigations, use only after related expansion and linkage checks have produced a candidate chain with at least 3-5 supporting events, or after at least two explicit targeted searches failed. Do not use it early based only on one or two seed records.",
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
    request_id = message.get("id")
    method = message.get("method")
    params = message.get("params") or {}

    if request_id is None:
        return None
    if method == "initialize":
        requested_version = params.get("protocolVersion", PROTOCOL_VERSION)
        negotiated = requested_version if requested_version in {PROTOCOL_VERSION, "2024-11-05"} else PROTOCOL_VERSION
        return response(
            request_id,
            {
                "protocolVersion": negotiated,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "title": "Intelligence Events POC", "version": SERVER_VERSION},
                "instructions": (
                    "Read-only synthetic intelligence data. Cite only event IDs returned by tools. "
                    "Resolve geographic, event, and entity references before broad searches. "
                    "Trace concrete identifiers, trace semantic clues when a chain shifts from IDs to descriptive cargo/route language, use plan_next_investigation_step as a process-control checkpoint after recommended seeds or before challenge/final summary, expand iteratively from strong seed evidence, and use aggregate_events before broad sampling. "
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
