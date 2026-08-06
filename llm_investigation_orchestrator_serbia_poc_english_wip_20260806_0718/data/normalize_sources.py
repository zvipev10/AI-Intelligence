#!/usr/bin/env python3
"""Normalize source channels and generic information types for the Serbia POC data."""

from __future__ import annotations

import csv
import io
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "north_kosovo_attachment_inspect" / "north_kosovo_synthetic_dataset_he_10k_subset.csv"
RAW_JSONL_PATH = ROOT / "north_kosovo_attachment_inspect" / "north_kosovo_synthetic_dataset_he_10k_subset.jsonl"
PROJECTION_PATH = ROOT / "serbia_kosovo_events_projection.csv"
LABELS_PATH = ROOT / "serbia_kosovo_evaluator_labels.csv"
REPORT_PATH = ROOT / "source_normalization_report.json"

APPROVED_SOURCE_TYPES = {
    "פייסבוק",
    "חדשות מקומיות",
    "X",
    "בלוג פוליטי",
    "טלגרם",
    "הודעת דובר",
    "טיקטוק",
    "ערוץ חדשות בינלאומי",
    "שמועה מקומית",
    "קבוצת וואטסאפ",
}

REMOVED_SOURCE_TYPES = {"דיווח אזרחי", "דיווח חירום"}
REMOVED_SOURCE_CATEGORIES = {"דיסאינפורמציה/מידע מטעה", "רעש לא קשור", "דיווח אזרחי", "דיווח חירום"}
NORMALIZED_INFORMATION_TYPES = {"דיווח אזרחי", "רעש לא קשור"}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def read_head_csv(repo_path: str) -> list[dict[str, str]]:
    try:
        completed = subprocess.run(
            ["git", "show", f"HEAD:{repo_path}"],
            cwd=ROOT.parents[1],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return list(csv.DictReader(io.StringIO(completed.stdout.lstrip("\ufeff"))))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fieldnames} for row in rows])


def text_has(text: str, *needles: str) -> bool:
    return any(needle in text for needle in needles)


def normalize_information_type(row: dict[str, str]) -> str:
    value = row.get("information_type", "")
    text = row.get("text", "")
    actor = row.get("actor_mentioned", "")

    if value == "רעש לא קשור":
        if text_has(text, "עבודות בכביש", "חסימה ביטחונית", "כביש"):
            return "תחבורה/לוגיסטיקה אזרחית"
        if text_has(text, "תמונות ישנות", "משתפים", "רשתות", "פוסט"):
            return "רשתות חברתיות"
        if text_has(text, "זיקוקים", "רעש ממפעל", "פיצוץ"):
            return "דיווח פיצוץ"
        if text_has(text, "דיון פוליטי"):
            return "מדיני/דיפלומטי"
        if text_has(text, "מחירי דלק", "חנות", "כדורגל", "מזג האוויר", "מבצע בחנות"):
            return "כלכלי/חברתי"
        return "כלכלי/חברתי"

    if value == "דיווח אזרחי":
        if text_has(text, "אמבולנס"):
            return "רפואי/חירום"
        if text_has(text, "משפחות עזבו", "פינוי", "עברו לקרובי משפחה"):
            return "פינוי/חילוץ"
        if text_has(text, "אוטובוס", "מונית", "עומס", "דרך", "כביש", "חסימה חלקית"):
            return "תחבורה/לוגיסטיקה אזרחית"
        if text_has(text, "משטרת קוסובו", "משטרה") or text_has(actor, "משטרת קוסובו"):
            return "פעילות משטרתית"
        if text_has(text, "KFOR") or actor == "KFOR":
            return "נוכחות KFOR"
        if text_has(text, "רכבים", "סיורים", "מחסום זמני"):
            return "ציוד/רכבים"
        if text_has(text, "הפסקת חשמל", "חנות", "בית ספר", "לימודים", "עירייה", "התקהלויות", "קבוצת הורים"):
            return "כלכלי/חברתי"
        return "כלכלי/חברתי"

    return value


def infer_social_source(text: str) -> str | None:
    if text_has(text, "קבוצת וואטסאפ", "קבוצות מקומיות", "קבוצות"):
        return "קבוצת וואטסאפ"
    if text_has(text, "סרטון", "תמונה", "תיעוד חזותי"):
        return "טיקטוק"
    if text_has(text, "פוסט", "חשבון", "גולשים", "משתמשים"):
        return "X"
    if text_has(text, "שמועה"):
        return "שמועה מקומית"
    return None


def normalize_source_type(row: dict[str, str]) -> str:
    current = row.get("source_type", "")
    if current in APPROVED_SOURCE_TYPES:
        return current

    text = row.get("text", "")
    category = row.get("source_category", "")
    info = row.get("information_type", "")

    social = infer_social_source(text)
    if social:
        return social
    if text_has(text, "דובר רשמי", "נציגים בינלאומיים", "העירייה המקומית מבקשת"):
        return "הודעת דובר"
    if text_has(text, "דיווח תקשורתי", "חדשות", "ערוץ", "עיתונאים"):
        return "חדשות מקומיות"
    if text_has(text, "מקור מפלגתי", "דיון פוליטי"):
        return "בלוג פוליטי"

    if category == "חדשות/תקשורת" or info == "חדשות/תקשורת":
        return "חדשות מקומיות"
    if category == "מדיני/דיפלומטי" or info == "מדיני/דיפלומטי":
        return "הודעת דובר"
    if category == "תחבורה/לוגיסטיקה אזרחית" or info == "תחבורה/לוגיסטיקה אזרחית":
        return "חדשות מקומיות"
    if category in {"רשתות חברתיות", "דיסאינפורמציה/מידע מטעה"} or info == "רשתות חברתיות":
        return "טלגרם"
    if category == "רעש לא קשור":
        return "שמועה מקומית"
    if category in {"דיווח אזרחי", "רפואי/חירום", "כלכלי/חברתי"}:
        return "שמועה מקומית"
    if category == "צבאי־ביטחוני גולמי":
        return "חדשות מקומיות"

    return "שמועה מקומית"


def normalize_raw_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, dict[str, str]], dict[str, Counter]]:
    source_type_changes: Counter[str] = Counter()
    information_type_changes: Counter[str] = Counter()
    source_category_removed: Counter[str] = Counter()
    by_record: dict[str, dict[str, str]] = {}
    normalized = []

    for row in rows:
        updated = dict(row)
        original_source_type = updated.get("source_type", "")
        original_information_type = updated.get("information_type", "")
        original_source_category = updated.get("source_category", "")

        updated["source_type"] = normalize_source_type(updated)
        updated["information_type"] = normalize_information_type(updated)

        if original_source_type != updated["source_type"]:
            source_type_changes[f"{original_source_type} -> {updated['source_type']}"] += 1
        if original_information_type != updated["information_type"]:
            information_type_changes[f"{original_information_type} -> {updated['information_type']}"] += 1
        if original_source_category:
            source_category_removed[original_source_category] += 1
        updated.pop("source_category", None)

        by_record[updated["record_id"]] = {
            "source_type": updated["source_type"],
            "information_type": updated["information_type"],
        }
        normalized.append(updated)

    return normalized, by_record, {
        "source_type_changes": source_type_changes,
        "information_type_changes": information_type_changes,
        "source_category_removed": source_category_removed,
    }


def update_projection(rows: list[dict[str, str]], by_record: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    updated = []
    for row in rows:
        next_row = dict(row)
        mapping = by_record.get(next_row.get("event_id", ""))
        if mapping:
            next_row["source_type"] = mapping["source_type"]
        updated.append(next_row)
    return updated


def update_labels(rows: list[dict[str, str]], by_record: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    updated = []
    for row in rows:
        next_row = dict(row)
        mapping = by_record.get(next_row.get("event_id", ""))
        if mapping:
            next_row["source_type"] = mapping["source_type"]
            next_row["information_type"] = mapping["information_type"]
        next_row.pop("source_category", None)
        updated.append(next_row)
    return updated


def update_jsonl(path: Path, by_record: dict[str, dict[str, str]]) -> int:
    if not path.exists():
        return 0
    updated_lines = []
    count = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            item = json.loads(line)
            mapping = by_record.get(item.get("record_id", ""))
            if mapping:
                item["source_type"] = mapping["source_type"]
                item["information_type"] = mapping["information_type"]
            item.pop("source_category", None)
            updated_lines.append(json.dumps(item, ensure_ascii=False, separators=(",", ":")))
            count += 1
    path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
    return count


def main() -> int:
    raw_fields, raw_rows = read_csv(RAW_PATH)
    projection_fields, projection_rows = read_csv(PROJECTION_PATH)
    labels_fields, label_rows = read_csv(LABELS_PATH)

    normalized_raw, by_record, counters = normalize_raw_rows(raw_rows)
    normalized_projection = update_projection(projection_rows, by_record)
    normalized_labels = update_labels(label_rows, by_record)
    jsonl_rows = update_jsonl(RAW_JSONL_PATH, by_record)
    original_raw_rows = read_head_csv(
        "llm_investigation_orchestrator_serbia_poc/data/north_kosovo_attachment_inspect/north_kosovo_synthetic_dataset_he_10k_subset.csv"
    )

    raw_fields = [field for field in raw_fields if field != "source_category"]
    labels_fields = [field for field in labels_fields if field != "source_category"]
    if "source_type" not in labels_fields:
        labels_fields.insert(2, "source_type")

    write_csv(RAW_PATH, raw_fields, normalized_raw)
    write_csv(PROJECTION_PATH, projection_fields, normalized_projection)
    write_csv(LABELS_PATH, labels_fields, normalized_labels)

    transition_source_type: Counter[str] = Counter()
    transition_information_type: Counter[str] = Counter()
    removed_source_categories: Counter[str] = Counter()
    if original_raw_rows:
        current_by_record = {row["record_id"]: row for row in normalized_raw}
        for original in original_raw_rows:
            current = current_by_record.get(original.get("record_id", ""))
            if not current:
                continue
            if original.get("source_type", "") != current.get("source_type", ""):
                transition_source_type[f"{original.get('source_type', '')} -> {current.get('source_type', '')}"] += 1
            if original.get("information_type", "") != current.get("information_type", ""):
                transition_information_type[f"{original.get('information_type', '')} -> {current.get('information_type', '')}"] += 1
            if original.get("source_category"):
                removed_source_categories[original["source_category"]] += 1

    report = {
        "rows": {
            "raw": len(normalized_raw),
            "raw_jsonl": jsonl_rows,
            "projection": len(normalized_projection),
            "labels": len(normalized_labels),
        },
        "approved_source_types": sorted(APPROVED_SOURCE_TYPES),
        "removed_source_types": sorted(REMOVED_SOURCE_TYPES),
        "removed_source_categories": sorted(REMOVED_SOURCE_CATEGORIES),
        "normalized_information_types": sorted(NORMALIZED_INFORMATION_TYPES),
        "source_type_counts": dict(Counter(row["source_type"] for row in normalized_raw).most_common()),
        "information_type_counts": dict(Counter(row["information_type"] for row in normalized_raw).most_common()),
        "source_type_changes": dict((transition_source_type or counters["source_type_changes"]).most_common()),
        "information_type_changes": dict((transition_information_type or counters["information_type_changes"]).most_common()),
        "source_category_removed_counts": dict((removed_source_categories or counters["source_category_removed"]).most_common()),
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
