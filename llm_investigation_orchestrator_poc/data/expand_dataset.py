#!/usr/bin/env python3
"""Create an expanded, non-overwriting POC dataset with more benign chains."""

from __future__ import annotations

import csv
import random
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INPUT = BASE_DIR / "events_he_large.csv"
OUTPUT = BASE_DIR / "events_he_expanded_5000.csv"
SUMMARY = BASE_DIR / "events_he_expanded_5000.summary.txt"
TARGET_ROWS = 5000
BENIGN_CHAIN_COUNT = 60
RANDOM_SEED = 4482

FIELDNAMES = [
    "event_id",
    "timestamp_utc",
    "source_type",
    "source_reliability",
    "entity_or_actor",
    "location_id",
    "event_summary",
]

PREFIX_TO_SOURCE = {
    "PORT": "רשומת נמל",
    "CUST": "רשומת מכס",
    "FIN": "התראה פיננסית",
    "TEL": "מטא-דאטה טלפוני",
    "MOVE": "חיישן תנועה",
    "CAM": "מצלמת דרך",
    "SOC": "רשתות חברתיות",
    "MAINT": "יומן תחזוקה",
    "ACOU": "חיישן אקוסטי",
}

SOURCE_TO_PREFIX = {value: key for key, value in PREFIX_TO_SOURCE.items()}

LOCATION_NAMES = {
    "L-201": "נמל חיפה",
    "L-202": "מתחם מחסנים קישון",
    "L-203": "מעבר נהר הירדן",
    "L-204": "צומת גולני",
    "L-205": "שוק נצרת",
    "L-206": "כביש גישה צדדי ליד בית שאן",
    "L-207": "אזור התעשייה בית שאן",
    "L-208": "משרד סיוע מרחב בחיפה",
    "L-209": "מסוף דלק צמח",
}

ACTORS = [
    "גליל הובלות",
    "כרמל ציוד חקלאי",
    "עמק שירותי קירור",
    "צפון משלוחים",
    "חברת אורנים",
    "מפעלי עמק הירדן",
    "קואופרטיב דלק העמק",
    "משרד סיוע מרחב",
    "יחידת תיאום מכס חיפה",
]

CARGO_TYPES = [
    "צינורות השקיה",
    "מסנני מים",
    "ציוד קירור",
    "חלקי חממות",
    "ציוד רפואי",
    "חומרי אריזה",
    "חלפים למשאבות מים",
    "מכלי דשן ריקים",
]

ROUTES = [
    ["L-201", "L-202", "L-204", "L-207"],
    ["L-201", "L-208", "L-202", "L-205"],
    ["L-209", "L-204", "L-203", "L-207"],
    ["L-201", "L-202", "L-206", "L-207"],
    ["L-205", "L-204", "L-209", "L-203"],
]


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_rows() -> list[dict[str, str]]:
    with INPUT.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def initial_counters(rows: list[dict[str, str]]) -> Counter[str]:
    counters: Counter[str] = Counter()
    for row in rows:
        match = re.match(r"([A-Z]+)-(\d+)", row["event_id"])
        if match:
            prefix, value = match.groups()
            counters[prefix] = max(counters[prefix], int(value))
    return counters


def next_id(counters: Counter[str], prefix: str) -> str:
    counters[prefix] += 1
    return f"{prefix}-{counters[prefix]:04d}"


def new_row(
    counters: Counter[str],
    prefix: str,
    timestamp: datetime,
    actor: str,
    location_id: str,
    summary: str,
    reliability: str = "גבוהה",
) -> dict[str, str]:
    return {
        "event_id": next_id(counters, prefix),
        "timestamp_utc": format_time(timestamp),
        "source_type": PREFIX_TO_SOURCE[prefix],
        "source_reliability": reliability,
        "entity_or_actor": actor,
        "location_id": location_id,
        "event_summary": summary,
    }


def make_container(index: int) -> str:
    prefixes = ["BN", "AG", "CL", "MD", "FR", "GL", "KR", "NZ", "QP", "RV"]
    return f"{prefixes[index % len(prefixes)]}-{5000 + index:04d}"


def add_benign_chain(rows: list[dict[str, str]], counters: Counter[str], index: int) -> None:
    actor = ACTORS[index % len(ACTORS)]
    receiver = ACTORS[(index + 3) % len(ACTORS)]
    cargo = CARGO_TYPES[index % len(CARGO_TYPES)]
    container = make_container(index)
    route = ROUTES[index % len(ROUTES)]
    base = datetime(2026, 5, 14, 6, 0, tzinfo=timezone.utc) + timedelta(hours=index * 2, minutes=(index * 7) % 50)
    chain_tag = f"שרשרת תמימה BN-{index + 1:03d}"
    rows.extend([
        new_row(counters, "PORT", base, actor, route[0], f"{chain_tag}: מכולה {container} של {cargo} הגיעה לנקודת קליטה עם מסמכי משלוח תקינים; אין קשר ידוע ל-OF-4482."),
        new_row(counters, "CUST", base + timedelta(minutes=42), "יחידת תיאום מכס חיפה", route[0], f"{chain_tag}: {container} שוחררה לאחר בדיקת מסמכים רגילה; אין מספרי מכולה משותפים עם OF-4482."),
        new_row(counters, "FIN", base + timedelta(hours=1, minutes=10), receiver, route[0], f"{chain_tag}: תשלום רגיל עבור הובלת {container} עם חשבונית מלאה וללא חריגה."),
        new_row(counters, "TEL", base + timedelta(hours=1, minutes=35), actor, route[1], f"{chain_tag}: שיחת תיאום קצרה על חלון פריקה של {container}; פעילות לוגיסטית רגילה."),
        new_row(counters, "MOVE", base + timedelta(hours=2, minutes=20), actor, route[1], f"{chain_tag}: משאית מורשית יצאה עם {container} לכיוון {LOCATION_NAMES[route[2]]}; תנועה מסחרית רגילה."),
        new_row(counters, "CAM", base + timedelta(hours=3, minutes=5), actor, route[2], f"{chain_tag}: מצלמת דרך תיעדה את המשאית של {container} במסלול המתוכנן; ללא חריגה."),
        new_row(counters, "SOC", base + timedelta(hours=3, minutes=50), receiver, route[3], f"{chain_tag}: דיווח מקומי על הגעת {cargo} לאתר היעד; פעילות אזרחית."),
        new_row(counters, "MAINT", base + timedelta(hours=4, minutes=25), receiver, route[3], f"{chain_tag}: נרשם סיום פריקה של {container} ובדיקת ציוד תקינה; אין קשר ידוע לאירוע הגבול."),
    ])


def add_background(rows: list[dict[str, str]], counters: Counter[str], rng: random.Random, amount: int) -> None:
    prefixes = ["FIN", "ACOU", "CAM", "CUST", "TEL", "MOVE", "PORT", "MAINT", "SOC"]
    summaries = [
        "פעילות אזרחית רגילה באזור {location}; אין חריגה תפעולית.",
        "עומס מקומי באזור {location}; אין קשר ידוע לאירוע הגבול.",
        "רישום מנהלי שגרתי עבור {actor}; ללא דפוס המשך ברור.",
        "תנועה מסחרית רגילה באזור {location}; אין קשר ידוע ל-OF-4482.",
        "בדיקת שירות שגרתית עבור {actor}; לא נמצא מזהה משותף עם תרחישים אחרים.",
        "דיווח רקע על פעילות יומית באזור {location}; ללא חריגה.",
        "עדכון תפעולי רגיל של {actor}; המסמכים תואמים.",
    ]
    start = datetime(2026, 5, 14, 0, 0, tzinfo=timezone.utc)
    for _ in range(amount):
        prefix = rng.choice(prefixes)
        actor = rng.choice(ACTORS + ["לא ידוע", "נועה ברק", "אורי לוי", "א. לוי"])
        location_id = rng.choice(list(LOCATION_NAMES))
        timestamp = start + timedelta(minutes=rng.randrange(0, 8 * 24 * 60))
        summary_template = rng.choice(summaries)
        summary = summary_template.format(actor=actor, location=LOCATION_NAMES[location_id])
        rows.append(new_row(
            counters,
            prefix,
            timestamp,
            actor,
            location_id,
            summary,
            reliability=rng.choice(["גבוהה", "בינונית", "נמוכה"]),
        ))


def write_rows(rows: list[dict[str, str]]) -> None:
    rows.sort(key=lambda row: (parse_time(row["timestamp_utc"]), row["event_id"]))
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(rows: list[dict[str, str]], original_count: int) -> None:
    sources = Counter(row["source_type"] for row in rows)
    locations = Counter(row["location_id"] for row in rows)
    chain_rows = sum("שרשרת תמימה BN-" in row["event_summary"] for row in rows)
    lines = [
        f"input: {INPUT.name}",
        f"output: {OUTPUT.name}",
        f"original_rows: {original_count}",
        f"expanded_rows: {len(rows)}",
        f"new_rows: {len(rows) - original_count}",
        f"benign_chains_added: {BENIGN_CHAIN_COUNT}",
        f"benign_chain_rows_added: {chain_rows}",
        f"target_rows: {TARGET_ROWS}",
        "hidden_suspicious_chain: unchanged original rows retained",
        f"sources: {dict(sources)}",
        f"locations: {dict(locations)}",
    ]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rng = random.Random(RANDOM_SEED)
    rows = load_rows()
    original_count = len(rows)
    counters = initial_counters(rows)
    for index in range(BENIGN_CHAIN_COUNT):
        add_benign_chain(rows, counters, index)
    remaining = TARGET_ROWS - len(rows)
    if remaining < 0:
        raise RuntimeError("Target row count is smaller than original rows plus benign chains")
    add_background(rows, counters, rng, remaining)
    if len(rows) != TARGET_ROWS:
        raise RuntimeError(f"Expected {TARGET_ROWS} rows, got {len(rows)}")
    write_rows(rows)
    write_summary(rows, original_count)
    print(SUMMARY.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
