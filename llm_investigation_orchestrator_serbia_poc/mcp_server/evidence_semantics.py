"""Canonical evidence classification backed by the shared semantic vocabulary."""

from __future__ import annotations

from typing import Any

try:
    from semantic_index import concept_weights
except ImportError:  # pragma: no cover - package-style execution fallback
    from .semantic_index import concept_weights


OBJECT_CLASS_CONCEPTS = {
    "שיירת כלי רכב": "concept:convoy_or_vehicle_column",
    "רכב משוריין": "concept:armored_vehicle",
    "מחסום דרכים": "concept:roadblock_position",
    "עמדת תצפית": "concept:observation_post",
    "מסוק": "concept:helicopter",
    "משאית לוגיסטית": "concept:logistics_vehicle",
    "עבודות הנדסיות": "concept:engineering_activity",
}


def normalize_evidence_event(event: dict[str, Any]) -> dict[str, Any]:
    """Resolve a missing object class with the existing semantic concept model.

    Structured source data remains authoritative. Semantic resolution is only
    applied when the source projection omitted an object class, and only when
    exactly one canonical object concept is present.
    """
    normalized = dict(event)
    existing = str(event.get("object_class") or "").strip()
    if existing:
        normalized["object_class"] = existing
        normalized["object_class_resolution"] = {
            "method": "structured_source",
            "semantic_concept": OBJECT_CLASS_CONCEPTS.get(existing),
            "score": 1.0,
        }
        return normalized

    summary = str(event.get("event_summary") or event.get("text") or "").strip()
    concepts = concept_weights(summary)
    matches = [
        (object_class, concept, float(concepts[concept]))
        for object_class, concept in OBJECT_CLASS_CONCEPTS.items()
        if concept in concepts
    ]
    if len(matches) != 1:
        normalized["object_class_resolution"] = {
            "method": "unresolved" if not matches else "multiple_semantic_concepts",
            "semantic_concepts": [concept for _, concept, _ in matches],
            "score": 0.0,
        }
        return normalized

    object_class, concept, weight = matches[0]
    normalized["object_class"] = object_class
    normalized["object_class_resolution"] = {
        "method": "shared_semantic_concept",
        "semantic_concept": concept,
        "score": round(min(weight / 5.0, 1.0), 6),
    }
    return normalized
