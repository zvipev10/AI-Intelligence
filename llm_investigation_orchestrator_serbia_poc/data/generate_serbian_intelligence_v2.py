#!/usr/bin/env python3
"""Generate the immutable Serbian-intelligence-perspective V2 scenario corpus.

All operational events and movements produced here are synthetic. Publicly named
formations are used only as fictional scenario entities. Existing V1 files are
read-only inputs and are never rewritten.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "north_kosovo_attachment_inspect"
SOURCE_CSV = SOURCE_DIR / "north_kosovo_synthetic_dataset_he_10k_subset.csv"
SOURCE_ENTITIES = ROOT / "serbia_kosovo_entities.json"
SOURCE_LOCATIONS = ROOT / "serbia_kosovo_locations.json"
OUTPUT_DIR = ROOT / "serbian_intelligence_v2"
SEED = 20260717
TARGET_ROWS = 14_800
PRELUDE_ROWS = 4_500
UAV_ROWS = 3_800
MAX_FRIENDLY_SHARE = 0.10

RAW_FIELDS = [
    "record_id", "timestamp", "source_type", "language", "country", "region",
    "municipality", "locality", "place_name", "location_id", "location_precision",
    "location_confidence", "claimed_location", "ground_truth_location",
    "actor_mentioned", "observed_actor", "event_id", "event_name",
    "information_type", "military_signal_type", "text", "relevance_label",
    "reliability_label", "claim_strength", "certainty_level", "is_duplicate",
    "is_rumor", "is_disinformation", "is_civilian_related", "is_military_related",
    "media_claimed", "media_verified", "possible_misidentification",
    "misleading_type", "ground_truth_status", "same_event_cluster",
    "analyst_question", "collection_family", "collection_platform", "observation_id",
    "mission_id", "video_segment_id", "observed_object_class",
    "estimated_object_count", "movement_status", "movement_direction",
    "geolocation_confidence", "identification_confidence", "analyst_assessment",
]

PROJECTION_FIELDS = [
    "event_id", "timestamp_utc", "source_type", "source_reliability",
    "source_reliability_label", "certainty_level", "entity_id", "location_id",
    "event_summary",
]

LABEL_FIELDS = [
    "event_id", "record_id", "source_type", "scenario_event_id", "event_name",
    "same_event_cluster", "information_type", "military_signal_type",
    "relevance_label", "source_reliability_label", "claim_strength",
    "certainty_level", "is_duplicate", "is_rumor", "is_disinformation",
    "is_civilian_related", "is_military_related", "media_claimed", "media_verified",
    "possible_misidentification", "misleading_type", "ground_truth_status",
    "claimed_location", "ground_truth_location", "analyst_question", "country",
    "region", "municipality", "locality", "place_name", "location_precision",
    "location_confidence",
]

EVENTS = {
    "EVT-012": "אינדיקציות פומביות למעבר צבא סרביה לכוננות מבצעית",
    "EVT-013": "כניסת כוחות סרביים בצירי יאריניה וברניאק",
    "EVT-014": "נסיגת מוצבי משטרת קוסובו והקמת קווי עיכוב",
    "EVT-015": "התבססות סרבית בשטחי מפתח רדודים בצפון",
    "EVT-016": "תנועת כוח סרבי מוגבלת לעבר מרחב גזיבודה",
    "EVT-017": "מעבר KFOR לתמיכה פעילה בכוחות קוסובו בתרחיש",
    "EVT-018": "פריסת קווי חסימה של KFOR בצפון",
    "EVT-019": "התגברות סיורי אוויר ותצפית של נאטו",
    "EVT-020": "תגבור משטרת קוסובו ו-KSF בחסות KFOR",
    "EVT-021": "בלימת ההתקדמות הסרבית מול קווי החסימה",
    "EVT-022": "ניסיונות תמרון סרביים בצירים חלופיים",
    "EVT-023": "עימותי כלי רכב והצגת נשק ללא לחימה מתמשכת",
    "EVT-024": "התבססות בכיסי שליטה מוגבלים והתגברות דיסאינפורמציה",
    "EVT-025": "קיפאון מבצעי והסדר מניעת חיכוך זמני",
}

EVENT_HOURS = {
    event_id: (index * 5, index * 5 + 13)
    for index, event_id in enumerate(EVENTS)
}

NEW_ENTITIES = [
    ("ENT-SAF-2BRIGADE", "החטיבה השנייה של צבא סרביה", ["2nd Army Brigade", "החטיבה השנייה"], "כוח סרבי - מקור פומבי"),
    ("ENT-SAF-21-INF", "גדוד החי״ר ה-21", ["21st Infantry Battalion"], "כוח סרבי - מקור פומבי"),
    ("ENT-SAF-22-INF", "גדוד החי״ר ה-22", ["22nd Infantry Battalion"], "כוח סרבי - מקור פומבי"),
    ("ENT-SAF-27-MECH", "הגדוד הממוכן ה-27", ["27th Mechanized Battalion"], "כוח סרבי - מקור פומבי"),
    ("ENT-SAF-28-MECH", "הגדוד הממוכן ה-28", ["28th Mechanized Battalion"], "כוח סרבי - מקור פומבי"),
    ("ENT-SAF-210-ENG", "גדוד ההנדסה ה-210", ["210th Engineer Battalion"], "כוח סרבי - מקור פומבי"),
    ("ENT-SAF-3BRIGADE", "החטיבה השלישית של צבא סרביה", ["3rd Army Brigade", "החטיבה השלישית"], "כוח סרבי - מקור פומבי"),
    ("ENT-KFOR-RCE", "KFOR פיקוד אזורי מזרח", ["KFOR RC-East", "Regional Command East"], "כוח נאטו"),
    ("ENT-KFOR-KTRBN", "גדוד העתודה הטקטית של KFOR", ["KTRBN", "KFOR Tactical Reserve Battalion"], "כוח נאטו"),
    ("ENT-KFOR-MSU", "היחידה הרב-לאומית המיוחדת של KFOR", ["KFOR MSU", "Multinational Specialized Unit"], "כוח נאטו"),
    ("ENT-KFOR-AVIATION", "כוח התעופה של KFOR", ["KFOR Aviation", "Aviation Support Task Force"], "כוח נאטו"),
    ("ENT-NATO-RESERVE", "כוח עתודה אזורי של נאטו", ["NATO reserve", "כוח תגבור נאטו"], "כוח נאטו"),
]

NEW_LOCATIONS = {
    "LOC-V2-001": {"name": "מרחב מעבר יאריניה", "type": "מעבר גבול - אזור כללי", "latitude": 43.17, "longitude": 20.70, "country": "קוסובו", "region": "צפון קוסובו", "municipality": "לפוסאביץ׳", "locality": "יאריניה", "precision": "coarse_area"},
    "LOC-V2-002": {"name": "ציר יאריניה–לפוסאביץ׳", "type": "ציר תנועה כללי", "latitude": 43.14, "longitude": 20.75, "country": "קוסובו", "region": "צפון קוסובו", "municipality": "לפוסאביץ׳", "locality": "צפון לפוסאביץ׳", "precision": "coarse_area"},
    "LOC-V2-003": {"name": "מרחב מעבר ברניאק", "type": "מעבר גבול - אזור כללי", "latitude": 42.98, "longitude": 20.50, "country": "קוסובו", "region": "צפון קוסובו", "municipality": "זובין פוטוק", "locality": "ברניאק", "precision": "coarse_area"},
    "LOC-V2-004": {"name": "ציר ברניאק–זובין פוטוק", "type": "ציר תנועה כללי", "latitude": 42.94, "longitude": 20.60, "country": "קוסובו", "region": "צפון קוסובו", "municipality": "זובין פוטוק", "locality": "מערב זובין פוטוק", "precision": "coarse_area"},
    "LOC-V2-005": {"name": "מרחב גזיבודה הצפוני", "type": "מרחב שליטה כללי", "latitude": 42.96, "longitude": 20.57, "country": "קוסובו", "region": "צפון קוסובו", "municipality": "זובין פוטוק", "locality": "גזיבודה", "precision": "coarse_area"},
    "LOC-V2-006": {"name": "קו חסימה צפוני ללפוסאביץ׳", "type": "קו חסימה תרחישי", "latitude": 43.11, "longitude": 20.79, "country": "קוסובו", "region": "צפון קוסובו", "municipality": "לפוסאביץ׳", "locality": "לפוסאביץ׳", "precision": "coarse_area"},
    "LOC-V2-007": {"name": "קו חסימה מערבי לזובין פוטוק", "type": "קו חסימה תרחישי", "latitude": 42.91, "longitude": 20.67, "country": "קוסובו", "region": "צפון קוסובו", "municipality": "זובין פוטוק", "locality": "זובין פוטוק", "precision": "coarse_area"},
    "LOC-V2-008": {"name": "גישות צפוניות לזבצ׳אן", "type": "מרחב הגנה כללי", "latitude": 42.92, "longitude": 20.82, "country": "קוסובו", "region": "צפון קוסובו", "municipality": "זבצ׳אן", "locality": "זבצ׳אן", "precision": "coarse_area"},
    "LOC-V2-009": {"name": "גישות צפוניות לצפון מיטרוביצה", "type": "מרחב הגנה כללי", "latitude": 42.90, "longitude": 20.85, "country": "קוסובו", "region": "צפון קוסובו", "municipality": "צפון מיטרוביצה", "locality": "צפון מיטרוביצה", "precision": "coarse_area"},
    "LOC-V2-010": {"name": "מרחב גשר איבר", "type": "נקודת חסימה אסטרטגית", "latitude": 42.89, "longitude": 20.87, "country": "קוסובו", "region": "צפון קוסובו", "municipality": "צפון מיטרוביצה", "locality": "גשר איבר", "precision": "coarse_area"},
    "LOC-V2-011": {"name": "מחנה נובו סלו - אזור כללי", "type": "מרחב KFOR", "latitude": 42.72, "longitude": 21.08, "country": "קוסובו", "region": "מרכז קוסובו", "municipality": "ווצ׳יטרן", "locality": "נובו סלו", "precision": "coarse_area"},
    "LOC-V2-012": {"name": "מחנה בונדסטיל - אזור כללי", "type": "מרחב KFOR", "latitude": 42.36, "longitude": 21.25, "country": "קוסובו", "region": "דרום-מזרח קוסובו", "municipality": "פריזאי", "locality": "בונדסטיל", "precision": "coarse_area"},
    "LOC-V2-013": {"name": "ציר תגבור פרישטינה–מיטרוביצה", "type": "ציר תגבור כללי", "latitude": 42.76, "longitude": 21.02, "country": "קוסובו", "region": "מרכז קוסובו", "municipality": "ווצ׳יטרן", "locality": "ציר צפוני", "precision": "coarse_area"},
    "LOC-V2-014": {"name": "מרחב שדה התעופה פרישטינה", "type": "מרחב תעופה כללי", "latitude": 42.57, "longitude": 21.04, "country": "קוסובו", "region": "מרכז קוסובו", "municipality": "פרישטינה", "locality": "שדה התעופה", "precision": "coarse_area"},
    "LOC-V2-015": {"name": "מרחב מעבר מרדארה", "type": "ציר הדגמה כללי", "latitude": 42.94, "longitude": 21.27, "country": "קוסובו", "region": "מזרח קוסובו", "municipality": "פודויבו", "locality": "מרדארה", "precision": "coarse_area"},
}

FRIENDLY_ENTITY_IDS = {
    "ENT-SERBIA-GOV", "ENT-SERBIAN-ARMY", "ENT-SERBIAN-PROTESTERS",
    "ENT-LOCAL-SERBIAN-LEADERS", "ENT-LOCAL-ARMED-GROUP",
    *(item[0] for item in NEW_ENTITIES if item[0].startswith("ENT-SAF-")),
}

OPPOSITION_IDS = [
    "ENT-KFOR", "ENT-KFOR-RCE", "ENT-KFOR-KTRBN", "ENT-KFOR-MSU",
    "ENT-KFOR-AVIATION", "ENT-NATO-RESERVE", "ENT-KOSOVO-POLICE",
    "ENT-KOSOVO-SPECIAL-POLICE", "ENT-KOSOVO-MOI", "ENT-KOSOVO-GOV",
    "ENT-KSF", "ENT-EULEX",
]

FRIENDLY_IDS = [item[0] for item in NEW_ENTITIES if item[0].startswith("ENT-SAF-")] + [
    "ENT-SERBIAN-ARMY", "ENT-SERBIA-GOV"
]

PUBLIC_SOURCES = ["טלגרם", "X", "פייסבוק", "טיקטוק", "קבוצת וואטסאפ", "חדשות מקומיות", "ערוץ חדשות בינלאומי", "הודעת דובר", "בלוג פוליטי", "שמועה מקומית"]
UAV_SOURCE = "חיל האוויר הסרבי - ניצול וידאו מכטב״ם"
UAV_OBJECTS = ["שיירת כלי רכב", "רכב משוריין", "מחסום דרכים", "עמדת תצפית", "מסוק", "משאית לוגיסטית", "קבוצת אנשים", "רכב אזרחי חשוד", "עבודות הנדסיות", "שטח היערכות ריק"]
MOVEMENTS = ["בתנועה", "בעצירה", "בפריסה", "בנסיגה", "בהיערכות", "ללא שינוי נראה"]
DIRECTIONS = ["צפון", "דרום", "מזרח", "מערב", "צפון-מערב", "צפון-מזרח", "לא ניתן לקביעה"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def utc_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def load_inputs() -> tuple[list[dict], list[dict], dict]:
    with SOURCE_CSV.open("r", encoding="utf-8-sig", newline="") as stream:
        source_rows = list(csv.DictReader(stream))
    entities = json.loads(SOURCE_ENTITIES.read_text(encoding="utf-8-sig"))
    locations = json.loads(SOURCE_LOCATIONS.read_text(encoding="utf-8-sig"))
    return source_rows, entities, locations


def entity_maps(entities: list[dict]) -> tuple[dict[str, str], dict[str, str]]:
    name_to_id = {}
    id_to_name = {}
    for item in entities:
        id_to_name[item["entity_id"]] = item["canonical_name"]
        for name in [item["canonical_name"], *item.get("aliases", [])]:
            name_to_id[name] = item["entity_id"]
    return name_to_id, id_to_name


def public_text(entity_name: str, event_name: str, location_name: str, rng: random.Random, friendly: bool) -> str:
    if friendly:
        templates = [
            "פרסום פומבי מצביע על נוכחות אפשרית של {entity} במרחב {location}; אין אימות עצמאי להיקף הכוח.",
            "תיעוד ברשתות מציג כלי רכב שיוחסו ל{entity} סמוך ל{location}, אך מועד הצילום אינו ודאי.",
            "מקור גלוי טוען כי {entity} קשור להתפתחות '{event}' באזור {location}; הפרטים חלקיים.",
        ]
    else:
        templates = [
            "דיווח ממקור גלוי מתאר פעילות של {entity} באזור {location} במסגרת '{event}'. נדרש אימות נוסף.",
            "מספר פרסומים מצביעים על תנועה של {entity} ליד {location}; קיימת אי-ודאות לגבי הכמות והיעד.",
            "תושבים דיווחו על נוכחות {entity} במרחב {location}. חלק מהחשבונות משתמשים באותו ניסוח.",
            "הודעה פומבית מתייחסת ל{entity} ולשינוי היערכות באזור {location}, ללא פירוט מלא.",
        ]
    return rng.choice(templates).format(entity=entity_name, event=event_name, location=location_name)


def uav_text(entity_name: str, location_name: str, obj: str, count: int, movement: str, direction: str, confidence: str) -> str:
    return (
        f"בקטע וידאו מכטב״ם תרחישי זוהה {obj} המשויך בהסתברות {confidence} ל{entity_name} "
        f"במרחב {location_name}. הוערכו {count} פריטים, מצב {movement}, כיוון {direction}. "
        "הזיהוי מבוסס על ניצול חזותי בלבד ודורש הצלבה."
    )


def make_common_raw(record_id: str, timestamp: datetime, source_type: str, entity_name: str,
                    event_id: str, event_name: str, location_id: str, location: dict,
                    text: str, rng: random.Random) -> dict:
    certainty = rng.choices(["נמוכה", "בינונית", "גבוהה"], [0.34, 0.46, 0.20])[0]
    reliability = rng.choices(["unverified", "likely", "confirmed", "disputed", "false"], [0.34, 0.31, 0.13, 0.14, 0.08])[0]
    rumor = reliability in {"unverified", "disputed", "false"} and rng.random() < 0.45
    duplicate = rng.random() < 0.11
    return {
        "record_id": record_id,
        "timestamp": timestamp.isoformat(),
        "source_type": source_type,
        "language": "עברית",
        "country": location["country"],
        "region": location["region"],
        "municipality": location["municipality"],
        "locality": location["locality"],
        "place_name": location["name"],
        "location_id": location_id,
        "location_precision": location["precision"],
        "location_confidence": rng.choice(["נמוכה", "בינונית", "גבוהה"]),
        "claimed_location": f'{location["municipality"]}, {location["name"]}',
        "ground_truth_location": f'{location["municipality"]}, {location["name"]}',
        "actor_mentioned": entity_name,
        "observed_actor": entity_name if reliability in {"likely", "confirmed"} else "",
        "event_id": event_id,
        "event_name": event_name,
        "information_type": "תצפית על תנועת כוחות",
        "military_signal_type": "תצפית על תנועת כוחות",
        "text": text,
        "relevance_label": str(rng.randint(2, 5)),
        "reliability_label": reliability,
        "claim_strength": rng.choice(["חלשה", "בינונית", "חזקה"]),
        "certainty_level": certainty,
        "is_duplicate": bool_text(duplicate),
        "is_rumor": bool_text(rumor),
        "is_disinformation": bool_text(reliability == "false" and rng.random() < 0.55),
        "is_civilian_related": bool_text(rng.random() < 0.18),
        "is_military_related": "true",
        "media_claimed": bool_text(source_type in {"טלגרם", "X", "פייסבוק", "טיקטוק", UAV_SOURCE}),
        "media_verified": bool_text(source_type == UAV_SOURCE or reliability == "confirmed"),
        "possible_misidentification": bool_text(rng.random() < 0.16),
        "misleading_type": rng.choice(["", "זמן שגוי", "מיקום שגוי", "ייחוס שגוי", "הגזמת היקף"]),
        "ground_truth_status": rng.choice(["נכון", "נכון חלקית", "לא ידוע", "שגוי"]),
        "same_event_cluster": f"{event_id}-CL-{rng.randint(1, 18):02d}",
        "analyst_question": rng.choice([
            "מהו סדר הכוחות והאם התנועה נמשכת?",
            "האם מדובר בתגבור, חסימה או הונאה?",
            "מהי רמת הביטחון בזיהוי היחידה והמיקום?",
            "האם הכוח נערך לבלימה או לפעולה התקפית?",
        ]),
        "collection_family": "",
        "collection_platform": "",
        "observation_id": "",
        "mission_id": "",
        "video_segment_id": "",
        "observed_object_class": "",
        "estimated_object_count": "",
        "movement_status": "",
        "movement_direction": "",
        "geolocation_confidence": "",
        "identification_confidence": "",
        "analyst_assessment": "",
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(SEED)
    source_hashes_before = {path.name: sha256(path) for path in [SOURCE_CSV, SOURCE_ENTITIES, SOURCE_LOCATIONS]}
    source_rows, entities, locations = load_inputs()

    for entity_id, name, aliases, entity_type in NEW_ENTITIES:
        entities.append({"entity_id": entity_id, "canonical_name": name, "aliases": aliases, "entity_type": entity_type})
    locations.update(NEW_LOCATIONS)
    name_to_id, id_to_name = entity_maps(entities)

    prelude_pool = [row for row in source_rows if row.get("event_id") in {f"EVT-{i:03d}" for i in range(1, 12)}]
    if not prelude_pool:
        raise RuntimeError("No EVT-001 through EVT-011 source rows found")

    rows: list[dict] = []
    projections: list[dict] = []
    labels: list[dict] = []
    uav_observations: list[dict] = []
    friendly_count = 0
    start = datetime(2026, 9, 12, 4, 0, tzinfo=timezone.utc)

    def append_record(raw: dict, entity_id: str) -> None:
        nonlocal friendly_count
        rows.append(raw)
        if entity_id in FRIENDLY_ENTITY_IDS:
            friendly_count += 1
        projections.append({
            "event_id": raw["record_id"],
            "timestamp_utc": utc_text(datetime.fromisoformat(raw["timestamp"])),
            "source_type": raw["source_type"],
            "source_reliability": "מקור צבאי סרבי" if raw["source_type"] == UAV_SOURCE else "לא סווגה",
            "source_reliability_label": raw["reliability_label"],
            "certainty_level": raw["certainty_level"],
            "entity_id": entity_id,
            "location_id": raw["location_id"],
            "event_summary": raw["text"],
        })
        labels.append({
            "event_id": raw["record_id"], "record_id": raw["record_id"], "source_type": raw["source_type"],
            "scenario_event_id": raw["event_id"], **{field: raw.get(field, "") for field in LABEL_FIELDS if field not in {"event_id", "record_id", "source_type", "scenario_event_id"}},
        })

    # Perspective-adjusted buildup. Friendly references are aggressively downsampled
    # and remain public-source observations only.
    for index in range(PRELUDE_ROWS):
        base = rng.choice(prelude_pool)
        event_id = base["event_id"]
        event_index = int(event_id.split("-")[1])
        timestamp = start + timedelta(hours=(event_index - 1) * 4 + rng.random() * 10, minutes=rng.randint(0, 59))
        original_entity_id = name_to_id.get(base.get("actor_mentioned", ""), "ENT-UNIDENTIFIED-ACTORS")
        keep_friendly = original_entity_id in FRIENDLY_ENTITY_IDS and friendly_count < 250 and rng.random() < 0.22
        if original_entity_id in FRIENDLY_ENTITY_IDS and not keep_friendly:
            entity_id = rng.choice(OPPOSITION_IDS + ["ENT-LOCAL-RESIDENTS", "ENT-LOCAL-JOURNALISTS"])
        else:
            entity_id = original_entity_id
        entity_name = id_to_name.get(entity_id, "גורם לא מזוהה")
        location_id = base.get("location_id") if base.get("location_id") in locations else rng.choice(list(NEW_LOCATIONS))
        location = locations[location_id]
        event_name = base.get("event_name") or f"שלב מקדים {event_id}"
        text = public_text(entity_name, event_name, location["name"], rng, entity_id in FRIENDLY_ENTITY_IDS)
        record_id = f"REC-V2-{index + 1:06d}"
        raw = make_common_raw(record_id, timestamp, rng.choice(PUBLIC_SOURCES), entity_name, event_id, event_name, location_id, location, text, rng)
        raw["collection_family"] = "public_source"
        raw["collection_platform"] = raw["source_type"]
        append_record(raw, entity_id)

    escalation_start = datetime(2026, 9, 14, 6, 0, tzinfo=timezone.utc)
    escalation_rows = TARGET_ROWS - PRELUDE_ROWS
    new_location_ids = list(NEW_LOCATIONS)
    public_friendly_target = 950

    for offset in range(escalation_rows):
        global_index = PRELUDE_ROWS + offset
        record_id = f"REC-V2-{global_index + 1:06d}"
        event_id = rng.choice(list(EVENTS))
        low_hour, high_hour = EVENT_HOURS[event_id]
        timestamp = escalation_start + timedelta(hours=rng.uniform(low_hour, high_hour), minutes=rng.randint(0, 59))
        location_id = rng.choice(new_location_ids)
        location = locations[location_id]
        event_name = EVENTS[event_id]

        if offset < UAV_ROWS:
            entity_id = rng.choice(OPPOSITION_IDS + ["ENT-LOCAL-RESIDENTS", "ENT-AMBULANCES"])
            entity_name = id_to_name[entity_id]
            obj = rng.choice(UAV_OBJECTS)
            count = rng.randint(1, 24)
            movement = rng.choice(MOVEMENTS)
            direction = rng.choice(DIRECTIONS)
            identification = rng.choice(["נמוכה", "בינונית", "גבוהה"])
            observation_id = f"OBS-UAV-V2-{offset + 1:05d}"
            mission_id = f"UAV-MSN-{1 + offset // 95:03d}"
            video_segment = f"VID-V2-{offset + 1:05d}"
            text = uav_text(entity_name, location["name"], obj, count, movement, direction, identification)
            raw = make_common_raw(record_id, timestamp, UAV_SOURCE, entity_name, event_id, event_name, location_id, location, text, rng)
            raw.update({
                "collection_family": "airborne_isr_video_exploitation",
                "collection_platform": "synthetic_serbian_uav",
                "observation_id": observation_id,
                "mission_id": mission_id,
                "video_segment_id": video_segment,
                "observed_object_class": obj,
                "estimated_object_count": str(count),
                "movement_status": movement,
                "movement_direction": direction,
                "geolocation_confidence": rng.choice(["בינונית", "גבוהה"]),
                "identification_confidence": identification,
                "analyst_assessment": rng.choice(["דורש הצלבה", "תואם לדפוס תגבור", "עשוי להיות כוח חסימה", "ייתכן זיהוי שגוי", "אין שינוי מבצעי ברור"]),
                "reliability_label": rng.choice(["likely", "confirmed", "unverified"]),
                "media_claimed": "true",
                "media_verified": "true",
            })
            uav_observations.append({
                "observation_id": observation_id,
                "record_id": record_id,
                "scenario_event_id": event_id,
                "mission_id": mission_id,
                "video_segment_id": video_segment,
                "observed_at_utc": utc_text(timestamp),
                "processed_at_utc": utc_text(timestamp + timedelta(minutes=rng.randint(12, 150))),
                "source_type": UAV_SOURCE,
                "media_type": "synthetic_uav_video_exploitation",
                "location_id": location_id,
                "entity_id": entity_id,
                "object_class": obj,
                "estimated_object_count": count,
                "movement_status": movement,
                "movement_direction": direction,
                "geolocation_confidence": raw["geolocation_confidence"],
                "identification_confidence": identification,
                "observation_summary": text,
                "analyst_assessment": raw["analyst_assessment"],
                "synthetic": True,
            })
        else:
            can_add_friendly = friendly_count < public_friendly_target
            friendly = can_add_friendly and rng.random() < 0.13
            entity_id = rng.choice(FRIENDLY_IDS if friendly else OPPOSITION_IDS + ["ENT-LOCAL-RESIDENTS", "ENT-LOCAL-JOURNALISTS", "ENT-AMBULANCES"])
            entity_name = id_to_name[entity_id]
            source_type = rng.choice(PUBLIC_SOURCES)
            text = public_text(entity_name, event_name, location["name"], rng, friendly)
            raw = make_common_raw(record_id, timestamp, source_type, entity_name, event_id, event_name, location_id, location, text, rng)
            raw["collection_family"] = "public_source"
            raw["collection_platform"] = source_type

        append_record(raw, entity_id)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_csv = OUTPUT_DIR / "north_kosovo_serbian_intelligence_v2_14800.csv"
    raw_jsonl = OUTPUT_DIR / "north_kosovo_serbian_intelligence_v2_14800.jsonl"
    projection_csv = OUTPUT_DIR / "serbia_kosovo_events_projection_v2.csv"
    labels_csv = OUTPUT_DIR / "serbia_kosovo_evaluator_labels_v2.csv"
    entities_json = OUTPUT_DIR / "serbia_kosovo_entities_v2.json"
    locations_json = OUTPUT_DIR / "serbia_kosovo_locations_v2.json"
    uav_jsonl = OUTPUT_DIR / "serbian_uav_observations_v2.jsonl"

    write_csv(raw_csv, rows, RAW_FIELDS)
    write_jsonl(raw_jsonl, rows)
    write_csv(projection_csv, projections, PROJECTION_FIELDS)
    write_csv(labels_csv, labels, LABEL_FIELDS)
    entities_json.write_text(json.dumps(entities, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    locations_json.write_text(json.dumps(locations, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_jsonl(uav_jsonl, uav_observations)

    source_hashes_after = {path.name: sha256(path) for path in [SOURCE_CSV, SOURCE_ENTITIES, SOURCE_LOCATIONS]}
    if source_hashes_before != source_hashes_after:
        raise RuntimeError("A V1 source file changed during generation")

    entity_ids = {item["entity_id"] for item in entities}
    location_ids = set(locations)
    projection_columns_ok = list(projections[0]) == PROJECTION_FIELDS
    unique_records = len({row["record_id"] for row in rows})
    dangling_entities = sorted({row["entity_id"] for row in projections} - entity_ids)
    dangling_locations = sorted({row["location_id"] for row in projections} - location_ids)
    friendly_share = friendly_count / len(rows)
    friendly_non_public = [
        row["record_id"] for row, projection in zip(rows, projections)
        if projection["entity_id"] in FRIENDLY_ENTITY_IDS and row["collection_family"] != "public_source"
    ]
    event_counts = Counter(row["event_id"] for row in rows)
    collection_counts = Counter(row["collection_family"] for row in rows)
    source_counts = Counter(row["source_type"] for row in rows)
    checks = {
        "target_rows": len(rows) == TARGET_ROWS,
        "unique_record_ids": unique_records == TARGET_ROWS,
        "uav_minimum": len(uav_observations) >= UAV_ROWS,
        "friendly_share_at_or_below_10_percent": friendly_share <= MAX_FRIENDLY_SHARE,
        "friendly_records_public_only": not friendly_non_public,
        "projection_columns_exact": projection_columns_ok,
        "no_dangling_entities": not dangling_entities,
        "no_dangling_locations": not dangling_locations,
        "v1_hashes_unchanged": source_hashes_before == source_hashes_after,
        "v1_post_011_events_absent": not any(row.get("event_id") in EVENTS for row in prelude_pool),
    }
    if not all(checks.values()):
        raise RuntimeError(f"V2 validation failed: {checks}")

    output_files = [raw_csv, raw_jsonl, projection_csv, labels_csv, entities_json, locations_json, uav_jsonl]
    report = {
        "schema_version": 2,
        "synthetic": True,
        "seed": SEED,
        "rows": len(rows),
        "prelude_rows": PRELUDE_ROWS,
        "replacement_escalation_rows": escalation_rows,
        "uav_observations": len(uav_observations),
        "friendly_public_records": friendly_count,
        "friendly_share": round(friendly_share, 6),
        "collection_counts": dict(sorted(collection_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
        "event_counts": dict(sorted(event_counts.items())),
        "checks": checks,
        "dangling_entities": dangling_entities,
        "dangling_locations": dangling_locations,
        "v1_input_hashes": source_hashes_before,
        "output_hashes": {path.name: sha256(path) for path in output_files},
        "notes": [
            "All movements and operational events are fictional.",
            "Public formation names do not imply current or historical participation.",
            "No image or video media assets are included; UAV records are structured synthetic exploitation outputs.",
            "Existing V1 files are untouched and the application is not switched to V2.",
        ],
    }
    (OUTPUT_DIR / "generation_report_v2.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
