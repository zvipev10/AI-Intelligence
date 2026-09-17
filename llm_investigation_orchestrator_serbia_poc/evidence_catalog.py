"""Build and load the deterministic deployment-time evidence catalog."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from generate_english_projection import translate_plain
from mcp_server.evidence_store import prepare_fused_object, project_event
from mcp_server.evidence_semantics import normalize_evidence_event
from mcp_server.fusion_tools import build_evidence_snapshots, group_independent_sources, reconcile_quantity


CATALOG_SCHEMA_VERSION = "evidence-catalog-v2"
FUSION_WINDOW_HOURS = 8


def _time(value: str) -> datetime:
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def _rolling_groups(rows: list[dict[str, Any]], hours: int = FUSION_WINDOW_HOURS) -> list[list[dict[str, Any]]]:
    """Partition compatible rows without fixed wall-clock bucket boundaries."""
    ordered = sorted(rows, key=lambda row: (_time(row["timestamp_utc"]), str(row.get("event_id") or "")))
    groups: list[list[dict[str, Any]]] = []
    for row in ordered:
        if not groups or (_time(row["timestamp_utc"]) - _time(groups[-1][0]["timestamp_utc"])).total_seconds() > hours * 3600:
            groups.append([row])
        else:
            groups[-1].append(row)
    return groups


def _localized_evidence(row: dict[str, Any], locale: str) -> dict[str, Any]:
    if locale != "en":
        return row
    localized = dict(row)
    localized["summary"] = translate_plain(str(row.get("summary") or ""))
    movement = row.get("movement")
    if isinstance(movement, dict):
        localized["movement"] = {key: translate_plain(str(value)) if value else value for key, value in movement.items()}
    return localized


def _batch_fusion(rows: list[dict[str, Any]]) -> dict[str, Any]:
    public_rows = [row for row in rows if row.get("collection_family") != "airborne_isr_video_exploitation"]
    public_assignments = group_independent_sources(public_rows)["assignments"] if public_rows else []
    assignments = list(public_assignments)
    for row in rows:
        if row.get("collection_family") != "airborne_isr_video_exploitation":
            continue
        record_id = str(row.get("event_id") or "")
        mission_id = str(row.get("mission_id") or "").strip()
        observation_id = str(row.get("observation_id") or "").strip()
        group = f"uav-mission:{mission_id}" if mission_id else f"uav-observation:{observation_id or record_id}"
        assignments.append({"record_id": record_id, "source_group": group, "grouping_reason": "deployment catalog UAV collection identity"})
    source_count = len({item["source_group"] for item in assignments})
    reasons = [] if source_count >= 2 else ["fewer than two independent source groups"]
    return {
        "assignments": assignments,
        "independent_source_group_count": source_count,
        "independence_requirement_met": source_count >= 2,
        "confidence": "medium",
        "persistence_eligible": not reasons,
        "persistence_block_reasons": reasons,
        "quantity": reconcile_quantity(rows),
        "evidence": build_evidence_snapshots(rows, assignments),
    }


def build_catalog(events: list[dict[str, Any]], *, dataset_version: str, locale: str = "he") -> dict[str, Any]:
    structured = [normalize_evidence_event(row) for row in events]
    projected = [project_event(row) for row in structured]
    catalog_projected = [
        evidence for evidence, source in zip(projected, structured)
        if source.get("collection_family") == "airborne_isr_video_exploitation"
        or (source.get("object_class_resolution") or {}).get("method") == "shared_semantic_concept"
    ]
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in structured:
        location = str(row.get("location_id") or "").strip()
        entity = str(row.get("entity_id") or "").strip()
        object_class = str(row.get("object_class") or "").strip()
        timestamp = str(row.get("timestamp_utc") or "").strip()
        if location and entity and object_class and timestamp:
            groups[(location, entity, object_class)].append(row)

    fused, rejected = [], 0
    for key in sorted(groups):
        for rows in _rolling_groups(groups[key]):
            if len(rows) < 2:
                continue
            fusion = _batch_fusion(rows)
            candidate = prepare_fused_object(rows, fusion)
            if candidate["persistence_eligible"]:
                candidate["cataloged"] = True
                fused.append(candidate)
            else:
                rejected += 1

    rows = [_localized_evidence(row, locale) for row in catalog_projected + fused]
    source_ids = sorted(str(row.get("event_id") or row.get("record_id") or "") for row in events)
    return {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "dataset_version": dataset_version,
        "locale": locale,
        "source_fingerprint": hashlib.sha256("\n".join(source_ids).encode("utf-8")).hexdigest(),
        "build_parameters": {"fusion_window_hours": FUSION_WINDOW_HOURS, "object_class_resolution": "shared-semantic-concepts", "temporal_grouping": "rolling-window"},
        "counts": {
            "source_records": len(events),
            "projected": len(projected),
            "cataloged_observations_and_structured_reports": len(catalog_projected),
            "fused": len(fused),
            "rejected_fusion_groups": rejected,
            "total": len(rows),
        },
        "rows": rows,
    }


def load_events(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_catalog(path: Path, catalog: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--dataset-version", required=True)
    args = parser.parse_args()
    events = load_events(args.events)
    counts = {}
    for locale in ("he", "en"):
        catalog = build_catalog(events, dataset_version=args.dataset_version, locale=locale)
        counts[locale] = catalog["counts"]
        write_catalog(args.output_dir / f"{locale}.json", catalog)
    write_catalog(args.output_dir / "manifest.json", {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "dataset_version": args.dataset_version,
        "counts": counts,
    })
    print(json.dumps(counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
