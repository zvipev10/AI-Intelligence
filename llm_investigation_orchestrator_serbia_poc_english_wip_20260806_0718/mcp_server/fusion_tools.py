"""Deterministic, evaluator-isolated fusion helpers for Moshe target candidates."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from itertools import combinations
from statistics import median
from typing import Any, Iterable


UAV_FAMILY = "airborne_isr_video_exploitation"
PERSISTABLE_CONFIDENCE = frozenset({"medium", "high"})
MAX_CORROBORATION_HOURS = 8.0
MIN_ANCHOR_COMPETITION_MARGIN = 0.5
CONTRADICTION_MARKERS = (
    "אין סימן המקשר", "לא אותו", "אינו אותו", "סותר", "הכחיש", "מכחיש",
    "אין לכך אימות", "לא מאומת", "שמועה",
)
OBJECT_ALIASES = {
    "שיירת כלי רכב": ("שיירה", "טור כלי רכב", "מספר כלי רכב שנעו יחד", "שיירה ממונעת"),
    "רכב משוריין": ("משוריין", "ממוגן", "כלים משוריינים", "רכב כבד ממוגן", "כלי רכב בעלי מיגון"),
    "מחסום דרכים": ("מחסום", "חסימה", "נקודת חסימה", "חסימה מאוישת", "עמדת בידוק"),
    "עמדת תצפית": ("תצפית", "נקודת תצפית", "עמדה שולטת", "צוות תצפית"),
    "מסוק": ("מסוק", "כלי טיס סובב כנף", "רוטור"),
    "משאית לוגיסטית": ("משאית", "לוגיסט", "רכב תובלה", "משאית אספקה"),
    "עבודות הנדסיות": ("הנדסי", "הנדסית", "הכשרת שטח", "עבודות עפר", "חפירה", "דחפור"),
}


def _text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def _tokens(value: Any) -> set[str]:
    return set(re.findall(r"[\w\u0590-\u05ff]+", _text(value).casefold(), re.UNICODE))


def _time(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
    normalized = _text(value).replace("Z", "+00:00")
    if not normalized:
        return None
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    return parsed.astimezone(timezone.utc) if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _object_score(event: dict[str, Any], object_class: str) -> tuple[float, list[str]]:
    reported = _text(event.get("object_class"))
    if reported:
        return (1.0, ["exact structured object class"]) if reported == object_class else (-1.0, ["incompatible structured object class"])
    text = _text(event.get("event_summary")).casefold()
    matches = [alias for alias in OBJECT_ALIASES.get(object_class, (object_class,)) if alias.casefold() in text]
    return (1.0, [f"object alias: {matches[0]}"]) if matches else (0.0, ["no compatible object cue"])


def _reported_count_range(event: dict[str, Any]) -> tuple[int | None, int | None]:
    value = event.get("estimated_object_count")
    if str(value or "").isdigit():
        count = int(value)
        return count, count
    text = _text(event.get("event_summary"))
    range_match = re.search(r"בין\s+(\d+)\s+ל[-־]?(\d+)", text)
    if range_match:
        return int(range_match.group(1)), int(range_match.group(2))
    approximate = re.search(r"כ[-־]?\s*(\d+)", text)
    if approximate:
        count = int(approximate.group(1))
        return max(0, count - 1), count + 1
    return None, None


def _count_score(anchor: dict[str, Any], event: dict[str, Any]) -> tuple[float, str]:
    anchor_value = anchor.get("estimated_object_count")
    if not str(anchor_value or "").isdigit():
        return 0.5, "anchor quantity unresolved"
    low, high = _reported_count_range(event)
    if low is None or high is None:
        return 0.5, "public quantity unresolved"
    count = int(anchor_value)
    if low <= count <= high:
        return 1.0, "quantity compatible"
    distance = min(abs(count - low), abs(count - high))
    return (-1.0 if distance > 2 else 0.0), "quantity incompatible" if distance > 2 else "quantity close"


def discover_corroborating_evidence(
    seed_events: Iterable[dict[str, Any]], corpus: Iterable[dict[str, Any]], *,
    max_hours: float = MAX_CORROBORATION_HOURS, max_results: int = 24,
) -> dict[str, Any]:
    """Retrieve and rank visible, independent corroboration for one target seed."""
    seeds = list(seed_events)
    corpus_rows = list(corpus)
    if not seeds:
        raise ValueError("at least one seed event is required")
    anchor = next((item for item in seeds if _text(item.get("collection_family")) == UAV_FAMILY), seeds[0])
    anchor_time = _time(anchor.get("timestamp_utc") or anchor.get("timestamp"))
    object_class = _text(anchor.get("object_class"))
    seed_ids = {_text(item.get("event_id")) for item in seeds}

    def fit_score(candidate_anchor: dict[str, Any], event: dict[str, Any]) -> float | None:
        candidate_time = _time(candidate_anchor.get("timestamp_utc") or candidate_anchor.get("timestamp"))
        event_time = _time(event.get("timestamp_utc") or event.get("timestamp"))
        if not candidate_time or not event_time:
            return None
        delta = abs((event_time - candidate_time).total_seconds()) / 3600
        if delta > max_hours:
            return None
        object_fit, _ = _object_score(event, _text(candidate_anchor.get("object_class")))
        count_fit, _ = _count_score(candidate_anchor, event)
        if object_fit <= 0 or count_fit < 0:
            return None
        return 5.0 * object_fit + 3.0 * count_fit + 2.0 * max(0.0, 1.0 - delta / max_hours)

    ranked = []
    for event in corpus_rows:
        if _text(event.get("event_id")) in seed_ids:
            continue
        if _text(event.get("collection_family")) != "public_source":
            continue
        if _text(event.get("location_id")) != _text(anchor.get("location_id")):
            continue
        if _text(event.get("entity_id")) != _text(anchor.get("entity_id")):
            continue
        event_time = _time(event.get("timestamp_utc") or event.get("timestamp"))
        if not anchor_time or not event_time:
            continue
        delta_hours = abs((event_time - anchor_time).total_seconds()) / 3600
        if delta_hours > max_hours:
            continue
        text = _text(event.get("event_summary")).casefold()
        contradiction = next((marker for marker in CONTRADICTION_MARKERS if marker.casefold() in text), None)
        object_score, reasons = _object_score(event, object_class)
        if object_score <= 0 or contradiction:
            continue
        count_score, count_reason = _count_score(anchor, event)
        if count_score < 0:
            continue
        time_score = max(0.0, 1.0 - delta_hours / max_hours)
        total = 5.0 * object_score + 3.0 * count_score + 2.0 * time_score
        ranked.append({
            "event": event,
            "record_id": _text(event.get("event_id")),
            "score": round(total, 6),
            "delta_hours": round(delta_hours, 6),
            "reasons": [*reasons, count_reason, f"time distance {delta_hours:.2f}h", "same canonical location and entity"],
        })
    ranked.sort(key=lambda item: (-item["score"], item["delta_hours"], item["record_id"]))
    ranked = ranked[:max_results]

    pairs = []
    competing_anchors = [
        item for item in corpus_rows
        if _text(item.get("collection_family")) == UAV_FAMILY
        and _text(item.get("event_id")) != _text(anchor.get("event_id"))
        and _text(item.get("object_class")) == object_class
    ]
    for first, second in combinations(ranked, 2):
        first_event, second_event = first["event"], second["event"]
        if _text(first_event.get("source_type")) == _text(second_event.get("source_type")):
            continue
        grouping = group_independent_sources([anchor, first_event, second_event])
        if not grouping["independence_requirement_met"]:
            continue
        public_similarity = _similarity(first_event, second_event)
        pair_score = first["score"] + second["score"] + min(1.0, public_similarity)
        competing_scores = []
        for competitor in competing_anchors:
            first_fit = fit_score(competitor, first_event)
            second_fit = fit_score(competitor, second_event)
            if first_fit is not None and second_fit is not None:
                competing_scores.append(first_fit + second_fit + min(1.0, public_similarity))
        competing_score = max(competing_scores) if competing_scores else None
        anchor_margin = pair_score - competing_score if competing_score is not None else None
        if anchor_margin is not None and anchor_margin < MIN_ANCHOR_COMPETITION_MARGIN:
            continue
        pairs.append({
            "event_ids": [_text(anchor.get("event_id")), first["record_id"], second["record_id"]],
            "score": round(pair_score, 6),
            "source_group_count": grouping["independent_source_group_count"],
            "anchor_competition_margin": round(anchor_margin, 6) if anchor_margin is not None else None,
            "reasons": ["different public source types", "independent source groups", f"public semantic overlap {public_similarity:.3f}", f"current seed leads competing visible anchors by at least {MIN_ANCHOR_COMPETITION_MARGIN:.1f}"],
        })
    pairs.sort(key=lambda item: (-item["score"], item["event_ids"]))
    best = pairs[0] if pairs else None
    second = pairs[1] if len(pairs) > 1 else None
    margin = round(best["score"] - second["score"], 6) if best and second else None
    return {
        "anchor_record_id": _text(anchor.get("event_id")),
        "retrieved": [{key: value for key, value in item.items() if key != "event"} for item in ranked],
        "ranked_pairs": pairs[:10],
        "selected_event_ids": best["event_ids"] if best else [_text(item.get("event_id")) for item in seeds],
        "selected_pair_score": best["score"] if best else None,
        "ambiguity_margin": margin,
        "ambiguous": bool(best and second and margin is not None and margin < MIN_ANCHOR_COMPETITION_MARGIN),
    }


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
