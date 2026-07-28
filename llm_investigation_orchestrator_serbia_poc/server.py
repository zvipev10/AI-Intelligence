#!/usr/bin/env python3
from __future__ import annotations

import http.client
import csv
import json
import mimetypes
import os
import re
import sys
import time
import secrets
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from agent_result_pipeline import (
    build_agent_result,
    evidence_reference_layers_from_audit,
    normalize_aggregate_groups,
    normalize_entity_layers,
    normalize_location_layers,
    normalize_map_locations,
    normalize_attack_targets,
    normalize_workstream_collaboration,
    requested_result_layers_from_audit,
)
from agent_routing import AgentRouteRegistry, MOSHE_AGENT_ID
from scenario_playback import (
    PlaybackConflictError,
    claim_reevaluation,
    find_investigation_run,
    find_workstream_run,
    finish_reevaluation,
    get_manifest,
    list_scenarios,
    load_run as load_scenario_run,
    load_playback_visibility,
    public_run,
    scenario_details,
    start_run as start_scenario_run,
    transition_run as transition_scenario_run,
    run_with_next_stage,
    write_historical_visibility,
    write_playback_visibility,
)
from workstream_artifacts import (
    ArtifactConflictError,
    create_artifact,
    get_artifact,
    list_artifacts,
    revise_artifact,
)

try:
    import paramiko
except ImportError:
    paramiko = None


ROOT = Path(__file__).resolve().parent
ATTACK_TARGET_CATALOG_LAYER_ID = "attack-targets:all"
TARGET_CATALOG_READER = Path(os.environ.get(
    "INTELLIGENCE_POC_TARGET_CATALOG_READER",
    "/opt/serbia-poc/mcp_server/target_catalog_reader.py",
))
TARGET_BANK_PATH = Path(os.environ.get(
    "INTELLIGENCE_POC_TARGET_BANK",
    "/opt/serbia-poc/data/attack_targets/attack_targets.db",
))
CONFIG_PATH = ROOT / ".hermes-api.json"
RECORDED_RUNS_PATH = ROOT / "test_runs" / "compact_demo_after_general_instructions_20260620T151848Z.json"
DATASET_VERSION = os.environ.get("INTELLIGENCE_POC_DATASET_VERSION", "v2").strip().lower()
if DATASET_VERSION in {"v2.1", "v2_1", "v21"}:
    DATASET_VERSION = "v2.1"
    DATASET_DIR = ROOT / "data" / "serbian_intelligence_v2_1"
    LOCATIONS_PATH = DATASET_DIR / "serbia_kosovo_locations_v2_1.json"
    EVENTS_PATH = DATASET_DIR / "serbia_kosovo_events_projection_v2_1.csv"
    ENTITIES_PATH = DATASET_DIR / "serbia_kosovo_entities_v2_1.json"
    DATASET_URL = "./data/serbian_intelligence_v2_1/serbia_kosovo_events_projection_v2_1.csv"
    LOCATIONS_URL = "./data/serbian_intelligence_v2_1/serbia_kosovo_locations_v2_1.json"
elif DATASET_VERSION == "v2":
    DATASET_DIR = ROOT / "data" / "serbian_intelligence_v2"
    LOCATIONS_PATH = DATASET_DIR / "serbia_kosovo_locations_v2.json"
    EVENTS_PATH = DATASET_DIR / "serbia_kosovo_events_projection_v2.csv"
    ENTITIES_PATH = DATASET_DIR / "serbia_kosovo_entities_v2.json"
    DATASET_URL = "./data/serbian_intelligence_v2/serbia_kosovo_events_projection_v2.csv"
    LOCATIONS_URL = "./data/serbian_intelligence_v2/serbia_kosovo_locations_v2.json"
elif DATASET_VERSION == "v1":
    DATASET_DIR = ROOT / "data"
    LOCATIONS_PATH = DATASET_DIR / "serbia_kosovo_locations.json"
    EVENTS_PATH = DATASET_DIR / "serbia_kosovo_events_projection.csv"
    ENTITIES_PATH = DATASET_DIR / "serbia_kosovo_entities.json"
    DATASET_URL = "./data/serbia_kosovo_events_projection.csv"
    LOCATIONS_URL = "./data/serbia_kosovo_locations.json"
else:
    raise ValueError(f"Unsupported INTELLIGENCE_POC_DATASET_VERSION: {DATASET_VERSION}")

# Keep replacement-scenario state separate from legacy V1 event identifiers.
# Selecting V1 preserves the existing on-disk layout for rollback compatibility.
STATE_SUFFIX = Path(DATASET_VERSION) if DATASET_VERSION != "v1" else Path()
PERFORMANCE_DIR = ROOT / "performance_logs" / STATE_SUFFIX
RECORDED_RUNS_DIR = ROOT / "recorded_runs" / STATE_SUFFIX
SAVED_QUESTIONS_DIR = ROOT / "saved_questions" / STATE_SUFFIX
INVESTIGATIONS_DIR = ROOT / "investigations" / STATE_SUFFIX
WORKSTREAMS_DIR = ROOT / "workstreams" / STATE_SUFFIX
SCENARIO_MANIFESTS_DIR = ROOT / "scenario_manifests"
SCENARIO_RUNS_DIR = ROOT / "scenario_runs" / STATE_SUFFIX
TERMINAL_STATUSES = {"completed", "failed", "cancelled"}
EVENT_ID_PATTERN = re.compile(r"\b(?:REC-(?:V2-)?\d{6}|LOC-(?:V2-)?\d{3})\b")
SAVED_QUESTION_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")
INVESTIGATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")
WORKSTREAM_ID_PATTERN = re.compile(r"^ws_[A-Za-z0-9_.-]+$")
WORKSTREAM_STATUSES = {"active", "paused", "completed", "archived"}
PARTICIPANT_KINDS = {"human", "agent"}
ACTIVE_RUN_STARTED_AT = None
ACTIVE_RUN_STARTED_AT_BY_AUDIT: dict[str, datetime] = {}
APP_BUILD = f"serbia-poc-{DATASET_VERSION}"
REMOTE_AUDIT_PATH = "/opt/serbia-poc/mcp_audit.jsonl"
HERMES_TOOL_PREFIX = "mcp_serbia_events_poc_"
AGENT_ROUTES = AgentRouteRegistry()
try:
    LOCATIONS = json.loads(LOCATIONS_PATH.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    LOCATIONS = {}


def load_ui_events() -> list[dict[str, Any]]:
    if not EVENTS_PATH.exists():
        return []
    with EVENTS_PATH.open(encoding="utf-8-sig", newline="") as handle:
        events = list(csv.DictReader(handle))
    for event in events:
        location = LOCATIONS.get(event.get("location_id") or "", {})
        event["location_name"] = location.get("name", event.get("location_id") or "")
        event["location_type"] = location.get("type", "")
    return sorted(events, key=lambda item: str(item.get("timestamp_utc") or ""))


def load_ui_entity_db() -> dict[str, dict[str, Any]]:
    if not ENTITIES_PATH.exists():
        return {}
    try:
        loaded = json.loads(ENTITIES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {item["entity_id"]: item for item in loaded if item.get("entity_id")}


def build_ui_entity_layers(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    entity_db = load_ui_entity_db()
    entity_ids = sorted({event.get("entity_id", "") for event in events if event.get("entity_id")})
    presentations: dict[str, dict[str, Any]] = {}
    for entity_id in entity_ids:
        base = entity_db.get(entity_id, {})
        entity_events = [event for event in events if event.get("entity_id") == entity_id]
        top_locations = []
        for location_id, count in Counter(event.get("location_id") for event in entity_events if event.get("location_id")).most_common(12):
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
            "event_count": len(entity_events),
            "top_locations": top_locations,
            "top_sources": [{"source_type": key, "count": count} for key, count in Counter(event.get("source_type") or "לא ידוע" for event in entity_events).most_common(10)],
            "certainty_breakdown": dict(Counter(event.get("certainty_level") or "לא ידוע" for event in entity_events)),
            "reliability_breakdown": dict(Counter(event.get("source_reliability_label") or event.get("source_reliability") or "לא ידוע" for event in entity_events)),
        }
    return presentations


def build_ui_location_layers(events: list[dict[str, Any]], entity_presentations: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    presentations: dict[str, dict[str, Any]] = {}
    events_by_location: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        if event.get("location_id"):
            events_by_location[event["location_id"]].append(event)
    for location_id, location in LOCATIONS.items():
        location_events = events_by_location.get(location_id, [])
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
            "event_count": len(location_events),
            "top_entities": [
                {
                    "entity_id": entity_id,
                    "name": entity_presentations.get(entity_id, {}).get("canonical_name", entity_id),
                    "count": count,
                }
                for entity_id, count in Counter(event.get("entity_id") for event in location_events if event.get("entity_id")).most_common(10)
            ],
            "top_sources": [{"source_type": key, "count": count} for key, count in Counter(event.get("source_type") or "לא ידוע" for event in location_events).most_common(10)],
            "certainty_breakdown": dict(Counter(event.get("certainty_level") or "לא ידוע" for event in location_events)),
            "reliability_breakdown": dict(Counter(event.get("source_reliability_label") or event.get("source_reliability") or "לא ידוע" for event in location_events)),
        }
    return presentations


def ui_layer_data() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    events = load_ui_events()
    entities = build_ui_entity_layers(events)
    locations = build_ui_location_layers(events, entities)
    for event in events:
        entity = entities.get(event.get("entity_id") or "", {})
        event["entity_name"] = entity.get("canonical_name") or event.get("entity_id") or ""
    return events, entities, locations


def load_persisted_attack_targets(
    entities: dict[str, dict[str, Any]], locations: dict[str, dict[str, Any]], limit: int = 500,
) -> list[dict[str, Any]]:
    if not TARGET_CATALOG_READER.is_file() or not TARGET_BANK_PATH.is_file():
        return []
    try:
        completed = subprocess.run(
            [sys.executable, str(TARGET_CATALOG_READER), "--db", str(TARGET_BANK_PATH), "--limit", str(limit)],
            capture_output=True, text=True, encoding="utf-8", timeout=8, check=True, shell=False,
        )
        rows = json.loads(completed.stdout).get("rows", [])
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        return []
    for row in rows:
        entity = entities.get(row.get("entity_id") or "", {})
        location = locations.get(row.get("location_id") or "", {})
        row["entity_name"] = entity.get("canonical_name") or row.get("entity_id") or ""
        row["location_name"] = location.get("location_name") or location.get("name") or row.get("location_id") or ""
    return rows


def list_ui_layers() -> list[dict[str, Any]]:
    events, entities, locations = ui_layer_data()
    targets = load_persisted_attack_targets(entities, locations)
    layers = [
        {
            "id": "entity-metadata:all",
            "label": "שכבת ישויות",
            "family": "entities",
            "kind": "entity_metadata",
            "count": len(entities),
            "capabilities": {"table": True, "map": True, "timeline": False},
        },
        {
            "id": "location-metadata:all",
            "label": "שכבת מיקומים",
            "family": "locations",
            "kind": "location_metadata",
            "count": len(locations),
            "capabilities": {"table": True, "map": True, "timeline": False},
        },
    ]
    layers.append({
        "id": ATTACK_TARGET_CATALOG_LAYER_ID,
        "label": "מועמדי מטרות",
        "family": "targets",
        "kind": "attack_targets",
        "count": len(targets),
        "capabilities": {"table": True, "map": True, "timeline": False},
    })
    source_counts = Counter(event.get("source_type") or "מקור לא ידוע" for event in events)
    for source_type, count in sorted(source_counts.items(), key=lambda item: (-item[1], item[0])):
        layers.append({
            "id": f"events:{source_type}",
            "label": source_type,
            "family": "events",
            "kind": "events",
            "source_type": source_type,
            "count": count,
            "capabilities": {"table": True, "map": True, "timeline": True},
        })
    return layers


def get_ui_layer_rows(layer_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]] | None:
    events, entities, locations = ui_layer_data()
    layers = {layer["id"]: layer for layer in list_ui_layers()}
    layer = layers.get(layer_id)
    if not layer:
        return None
    if layer_id == "entity-metadata:all":
        rows = sorted(entities.values(), key=lambda item: (-int(item.get("event_count") or 0), str(item.get("canonical_name") or "")))
    elif layer_id == "location-metadata:all":
        rows = sorted(locations.values(), key=lambda item: (-int(item.get("event_count") or 0), str(item.get("location_name") or "")))
    elif layer_id == ATTACK_TARGET_CATALOG_LAYER_ID:
        rows = load_persisted_attack_targets(entities, locations)
    elif layer_id.startswith("events:"):
        source_type = layer.get("source_type") or layer_id.split(":", 1)[1]
        rows = [event for event in events if (event.get("source_type") or "מקור לא ידוע") == source_type]
    else:
        return None
    return layer, rows


def load_hermes_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))


def load_agent_hermes_config(agent_id: str) -> dict:
    """Merge a non-secret per-agent endpoint override into the shared transport config."""
    config = dict(load_hermes_config())
    agents = config.pop("agents", {}) or {}
    override = agents.get(agent_id, {}) if isinstance(agents, dict) else {}
    if not isinstance(override, dict):
        raise ValueError(f"Invalid Hermes configuration for agent: {agent_id}")
    merged = {**config, **override}
    merged["agent_id"] = agent_id
    merged.setdefault("audit_path", REMOTE_AUDIT_PATH)
    return merged


def route_agent_request(request: dict[str, Any]):
    """Route from the unmodified current user message, never enriched prompt/history text."""
    routing_prompt = str(request.get("routing_prompt") or request.get("prompt") or "").strip()
    conversation_id = str(request.get("investigation_id") or "").strip()
    route = AGENT_ROUTES.route(conversation_id, routing_prompt)
    if route.responding_agent == MOSHE_AGENT_ID and route.hermes_session_id is None:
        AGENT_ROUTES.bind_hermes_session(conversation_id, route.mission_run_id, route.mission_run_id)
    return route

RECORDED_TOOL_TEXT = {
    "classify_question_intent": (
        "סיווג כוונת השאלה",
        "הסוכן מזהה אם זו שליפה, מפה, ציר זמן או חקירה עמוקה.",
        "נקבע מסלול עבודה והמלצת תצוגה לריצה המוקלטת.",
    ),
    "resolve_location": (
        "פתרון מיקום",
        "הסוכן מתרגם אזור או מקום למזהי LOC שניתן להציג ולסנן לפיהם.",
        "נמצאו מיקומים רלוונטיים לשאלה.",
    ),
    "resolve_entity": (
        "פתרון ישות",
        "הסוכן מאחד שמות וכינויים של גורם כדי לא לפספס רשומות רלוונטיות.",
        "הישות והכינויים שימשו לחיפוש המשך.",
    ),
    "aggregate_events": (
        "אגרגציה",
        "הסוכן סופר אירועים לפי מיקום, זמן, מקור או גורם כדי לראות איפה יש ריכוז חריג.",
        "התקבלה התפלגות שמבליטה מוקדים או חלונות זמן.",
    ),
    "search_events": (
        "חיפוש אירועים",
        "הסוכן מחפש במאגר לפי מילות מפתח, זמן, מקור או מיקום כדי לאסוף ראיות.",
        "נמצאו רשומות שתומכות בתשובה המוקלטת.",
    ),
    "semantic_search_events": (
        "חיפוש סמנטי במאגר",
        "הסוכן מחפש אירועים דומים במשמעות גם כאשר הניסוח אינו זהה למילות הרשומה.",
        "נמצאו מועמדים סמנטיים עם מזהי אירועים וציון התאמה.",
    ),
    "find_actor_history": (
        "היסטוריית גורם",
        "הסוכן בודק הופעות של אותו גורם לאורך זמן ומרחב.",
        "נמצאו הופעות נוספות שמחזקות או מסייגות את הדפוס.",
    ),
    "get_objects": (
        "שליפת אובייקטים",
        "הסוכן שולף אובייקטים מלאים משכבות האירועים, המיקומים או הישויות לפני הצגה או ציטוט.",
        "האובייקטים אומתו מול המזהים המרכזיים.",
    ),
    "trace_semantic_clues": (
        "מעקב רמזים סמנטיים",
        "הסוכן מחפש ניסוחים חוזרים כמו ירי, חסימה, חציית גבול, שמועה או הכחשה.",
        "נמצאו רמזים שמסבירים את ההמשך או את רעש המידע.",
    ),
    "find_related_events": (
        "הרחבת ראיות",
        "הסוכן מרחיב מאירועי עוגן לפי זמן, מקום, ישות ותוכן סמנטי.",
        "נמצאו מועמדים קשורים להמשך בדיקה.",
    ),
    "explain_linkage": (
        "בדיקת גשר ראייתי",
        "הסוכן בודק האם המעבר בין שתי רשומות נשען על זמן, מקום, ישות או תוכן משותף.",
        "הגשר סווג כחזק, נסיבתי או חסר.",
    ),
    "challenge_hypothesis": (
        "בדיקת חלופות",
        "הסוכן מחפש הסברים חלופיים ופערים לפני מסקנה חזקה.",
        "נמצאו חלופות ופערים שצריך לציין בתשובה.",
    ),
    "plan_next_investigation_step": (
        "בקרת כיוון",
        "הסוכן בודק אם יש עוד רמזים פתוחים לפני סיכום.",
        "נקבע האם להמשיך להרחיב או לסכם בזהירות.",
    ),
    "build_event_sequence": (
        "בניית רצף",
        "הסוכן מסדר את הראיות לפי זמן כדי לראות את מהלך ההתרחשות.",
        "נבנה רצף כרונולוגי לתצוגה.",
    ),
}


def elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 3)


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def safe_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.:-]+", "-", str(value or "")).strip("-")
    return cleaned[:120] or "run"


def write_performance_log(run_id: str, performance: dict, prompt: str | None = None) -> Path:
    PERFORMANCE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = PERFORMANCE_DIR / f"{timestamp}-{safe_filename(run_id)}.json"
    payload = {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "performance": performance,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def update_performance_client(run_id: str, client_performance: dict) -> Path | None:
    if not run_id:
        return None
    files = sorted(PERFORMANCE_DIR.glob(f"*-{safe_filename(run_id)}.json"))
    if not files:
        return None
    path = files[-1]
    payload = json.loads(path.read_text(encoding="utf-8"))
    performance = payload.setdefault("performance", {})
    performance["client"] = client_performance
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_full_recorded_runs() -> list[dict]:
    if not RECORDED_RUNS_DIR.exists():
        return []
    runs: list[dict] = []
    for path in sorted(RECORDED_RUNS_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        result = payload.get("result") or {}
        if not payload.get("id") or not payload.get("question") or not result.get("answer"):
            continue
        payload["_path"] = path.name
        runs.append(payload)
    return runs


def load_recorded_results() -> list[dict]:
    if not RECORDED_RUNS_PATH.exists():
        return []
    try:
        payload = json.loads(RECORDED_RUNS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return [item for item in payload.get("results") or [] if item.get("status") == 200 and item.get("answer")]


def recorded_questions() -> list[dict]:
    demo_order = {
        "q1_hotspots": 1,
        "real_hotspots_20260621": 1,
        "q2_movement": 2,
        "q3_stabilizer": 3,
        "q4_violence_noise": 4,
        "q5_assessment": 5,
    }
    questions = []
    seen_questions: set[str] = set()
    seen_ids: set[str] = set()
    for item in load_full_recorded_runs():
        recorded_id = item.get("id")
        question = item.get("question")
        result = item.get("result") or {}
        questions.append({
            "id": recorded_id,
            "question": question,
            "view": result.get("recommended_view") or "evidence",
            "step_count": len(result.get("investigation_steps") or []),
            "elapsed_ms": item.get("elapsed_ms"),
            "source": item.get("source") or "live_hermes_run",
        })
        if recorded_id:
            seen_ids.add(str(recorded_id).strip())
        if question:
            seen_questions.add(str(question).strip())
    for item in load_recorded_results():
        recorded_id = item.get("id")
        if recorded_id and str(recorded_id).strip() in seen_ids:
            continue
        question = item.get("prompt")
        if question and str(question).strip() in seen_questions:
            continue
        questions.append({
            "id": recorded_id,
            "question": question,
            "view": item.get("recommended_view") or "evidence",
            "step_count": item.get("step_count") or len(item.get("tool_sequence") or []),
            "elapsed_ms": item.get("elapsed_ms"),
        })
    return sorted(questions, key=lambda item: (demo_order.get(str(item.get("id") or ""), 100), str(item.get("question") or "")))


def recorded_map_locations(ids: list[str]) -> list[dict]:
    locations = []
    for event_id in ids:
        if not str(event_id).startswith("LOC-"):
            continue
        location = LOCATIONS.get(event_id)
        if not location:
            continue
        locations.append({
            "location_id": event_id,
            "location_name": location.get("name", event_id),
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "count": 1,
        })
    return locations


def synthesize_recorded_steps(item: dict) -> list[dict]:
    sequence = item.get("tool_sequence") or []
    ids = [str(value) for value in item.get("ids") or []]
    map_locations = recorded_map_locations(ids)
    steps = []
    for index, tool in enumerate(sequence, start=1):
        action, bridge, result = RECORDED_TOOL_TEXT.get(tool, ("פעולת חקירה", "הסוכן התקדם לפי ההקשר שנאסף.", "התקבל פלט ששימש את התשובה."))
        if index == 1:
            bridge = "הסוכן מתחיל מסיווג השאלה כדי לבחור האם זו שליפה, מפה, ציר זמן או חקירה עמוקה."
        elif index == len(sequence):
            bridge = "בשלב הסיום הסוכן מחבר את הממצאים המרכזיים לתשובה שניתן להציג לאנליסט."
        step = {
            "tool": tool,
            "bridge_summary": bridge,
            "observed_clue": "ריצה מוקלטת מתוך תוצר אמיתי של הסוכן.",
            "decision": bridge,
            "expected_value": "לקדם את החקירה בלי להמתין להרצת מודל חיה.",
            "rationale": bridge,
            "action": action,
            "result": result,
            "technical": {
                "tool": tool,
                "arguments": {"recorded_replay": True, "source_run_id": item.get("run_id")},
                "is_error": False,
            },
        }
        if tool == "aggregate_events" and map_locations:
            step["map_locations"] = map_locations
        steps.append(step)
    if not steps:
        steps.append({
            "tool": "recorded_replay",
            "bridge_summary": "המערכת מציגה תשובה מוקלטת מריצה אמיתית.",
            "observed_clue": "נבחרה שאלה מוקלטת.",
            "decision": "להציג תוצאה שאושרה מראש לצורכי דמו.",
            "expected_value": "תשובה מהירה ועקבית.",
            "rationale": "תשובה מהירה ועקבית לדמו.",
            "action": "טעינת תשובה מוקלטת",
            "result": "התשובה נטענה מהמאגר המקומי של הריצות המוקלטות.",
            "technical": {"tool": "recorded_replay", "arguments": {"recorded_replay": True}, "is_error": False},
        })
    return steps


def recorded_result(recorded_id: str) -> dict | None:
    for item in load_full_recorded_runs():
        if item.get("id") != recorded_id:
            continue
        result = dict(item.get("result") or {})
        original_usage = result.get("usage") if isinstance(result.get("usage"), dict) else {}
        result.update({
            "demo_replay": True,
            "replay_delay_ms": 2000,
            "recorded_id": item.get("id"),
            "question": item.get("question"),
            "source_run_id": result.get("run_id") or item.get("source_run_id"),
            "run_id": f"recorded-{item.get('id')}",
            "usage": {**original_usage, "recorded_replay": True, "recorded_source": item.get("source") or "live_hermes_run"},
            "recorded_at_utc": item.get("recorded_at_utc"),
            "recorded_elapsed_ms": item.get("elapsed_ms"),
        })
        return result
    for item in load_recorded_results():
        if item.get("id") != recorded_id:
            continue
        ids = [str(value) for value in item.get("ids") or []]
        event_ids = [value for value in ids if value.startswith("REC-")]
        loc_ids = [value for value in ids if value.startswith("LOC-")]
        return {
            "demo_replay": True,
            "replay_delay_ms": 2000,
            "recorded_id": item.get("id"),
            "question": item.get("prompt"),
            "run_id": f"recorded-{item.get('id')}",
            "source_run_id": item.get("run_id"),
            "answer": item.get("answer") or "",
            "event_ids": event_ids + loc_ids,
            "recommended_view": item.get("recommended_view") or "evidence",
            "view_reason": item.get("view_reason") or "ריצה מוקלטת לדמו",
            "investigation_steps": synthesize_recorded_steps(item),
            "events": [],
            "usage": {"recorded_replay": True},
            "performance_log": item.get("performance_log"),
        }
    return None


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def saved_question_path(saved_id: str) -> Path:
    if not SAVED_QUESTION_ID_PATTERN.fullmatch(saved_id or ""):
        raise ValueError("Invalid saved question id")
    path = (SAVED_QUESTIONS_DIR / f"{saved_id}.json").resolve()
    if SAVED_QUESTIONS_DIR.resolve() not in path.parents:
        raise ValueError("Invalid saved question path")
    return path


def investigation_memory_path(investigation_id: str) -> Path:
    if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id or ""):
        raise ValueError("Invalid investigation id")
    path = (INVESTIGATIONS_DIR / f"{investigation_id}.json").resolve()
    if INVESTIGATIONS_DIR.resolve() not in path.parents:
        raise ValueError("Invalid investigation memory path")
    return path


def empty_investigation_memory(investigation_id: str, name: str = "") -> dict:
    now = utc_now_iso()
    return {
        "schema_version": 1,
        "investigation_id": investigation_id,
        "name": name or investigation_id,
        "created_at_utc": now,
        "updated_at_utc": now,
        "memory": {
            "chat_summaries": [],
            "layers": []
        }
    }


def investigation_memory_metadata(payload: dict) -> dict:
    memory = payload.get("memory") if isinstance(payload.get("memory"), dict) else {}
    return {
        "investigation_id": payload.get("investigation_id"),
        "name": payload.get("name") or payload.get("investigation_id") or "Investigation",
        "created_at_utc": payload.get("created_at_utc"),
        "updated_at_utc": payload.get("updated_at_utc"),
        "chat_summary_count": len(memory.get("chat_summaries") or []),
        "layer_count": len(memory.get("layers") or []),
    }


def normalize_memory_list(value: Any) -> list[dict]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def compact_text(value: Any, limit: int) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def extract_result_ids(result: dict) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for value in result.get("event_ids") or []:
        text = str(value or "").strip()
        if text and text not in seen:
            ids.append(text)
            seen.add(text)
    for match in EVENT_ID_PATTERN.findall(str(result.get("answer") or "")):
        if match not in seen:
            ids.append(match)
            seen.add(match)
    return ids[:80]


def create_chat_summary_memory(request: dict) -> dict:
    investigation_id = str(request.get("investigation_id") or "").strip()
    if not investigation_id:
        raise ValueError("Missing investigation_id")
    if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id):
        raise ValueError("Invalid investigation id")

    prompt = str(request.get("prompt") or "").strip()
    result = request.get("result")
    if not prompt:
        raise ValueError("Missing prompt")
    if not isinstance(result, dict):
        raise ValueError("Missing result")
    answer = str(result.get("answer") or "").strip()
    if not answer:
        raise ValueError("Missing result answer")

    now = utc_now_iso()
    run_id = str(result.get("run_id") or result.get("source_run_id") or "").strip()
    item = {
        "id": f"chat_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{secrets.token_hex(3)}",
        "kind": "chat_result_summary",
        "saved_at_utc": now,
        "source": "manual_user_action",
        "prompt": compact_text(prompt, 1200),
        "answer_summary": compact_text(answer, 1800),
        "answer_preview": compact_text(answer, 320),
        "source_run_id": run_id,
        "recommended_view": result.get("recommended_view") or "",
        "step_count": len(result.get("investigation_steps") or []),
        "evidence_ids": extract_result_ids(result),
    }

    existing = load_investigation_memory(investigation_id)
    memory = existing.get("memory") if isinstance(existing.get("memory"), dict) else {}
    chat_summaries = normalize_memory_list(memory.get("chat_summaries"))
    chat_summaries.append(item)
    saved = save_investigation_memory({
        "investigation_id": investigation_id,
        "name": request.get("name") or existing.get("name") or investigation_id,
        "memory": {
            "chat_summaries": chat_summaries,
            "layers": normalize_memory_list(memory.get("layers")),
        }
    })
    return {"saved": item, "memory": saved}


def normalize_memory_filters(value: Any) -> list[dict]:
    filters: list[dict] = []
    for item in normalize_memory_list(value):
        field = compact_text(item.get("field"), 160)
        operator = compact_text(item.get("operator") or "contains", 40)
        filter_value = compact_text(item.get("value"), 320)
        if not field or not filter_value:
            continue
        filters.append({
            "field": field,
            "operator": operator,
            "value": filter_value,
        })
    return filters[:20]


def normalize_memory_ids(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    ids: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = compact_text(item, 120)
        if not text or text in seen:
            continue
        ids.append(text)
        seen.add(text)
        if len(ids) >= 80:
            break
    return ids


def memory_count(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def create_layer_memory(request: dict) -> dict:
    investigation_id = str(request.get("investigation_id") or "").strip()
    if not investigation_id:
        raise ValueError("Missing investigation_id")
    if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id):
        raise ValueError("Invalid investigation id")

    layer = request.get("layer")
    if not isinstance(layer, dict):
        raise ValueError("Missing layer")
    label = compact_text(layer.get("label"), 240)
    kind = compact_text(layer.get("kind"), 80)
    if not label or not kind:
        raise ValueError("Missing layer label or kind")

    now = utc_now_iso()
    item = {
        "id": f"layer_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{secrets.token_hex(3)}",
        "kind": "layer_filter_state",
        "saved_at_utc": now,
        "source": "manual_user_action",
        "layer_id": compact_text(layer.get("id"), 240),
        "label": label,
        "layer_kind": kind,
        "catalog_layer_id": compact_text(layer.get("catalog_layer_id") or layer.get("catalogLayerId"), 240),
        "data_id": compact_text(layer.get("data_id") or layer.get("dataId"), 240),
        "source_id": compact_text(layer.get("source_id") or layer.get("sourceId"), 240),
        "source_label": compact_text(layer.get("source_label") or layer.get("sourceLabel"), 240),
        "source_type": compact_text(layer.get("source_type"), 160),
        "original_count": memory_count(layer.get("original_count")),
        "filtered_count": memory_count(layer.get("filtered_count")),
        "applied_filters": normalize_memory_filters(layer.get("applied_filters")),
        "sample_ids": normalize_memory_ids(layer.get("sample_ids")),
    }

    existing = load_investigation_memory(investigation_id)
    memory = existing.get("memory") if isinstance(existing.get("memory"), dict) else {}
    layers = normalize_memory_list(memory.get("layers"))
    layers.append(item)
    saved = save_investigation_memory({
        "investigation_id": investigation_id,
        "name": request.get("name") or existing.get("name") or investigation_id,
        "memory": {
            "chat_summaries": normalize_memory_list(memory.get("chat_summaries")),
            "layers": layers,
        }
    })
    return {"saved": item, "memory": saved}


def normalize_investigation_memory(request: dict) -> dict:
    investigation_id = str(request.get("investigation_id") or "").strip()
    if not investigation_id:
        raise ValueError("Missing investigation_id")
    if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id):
        raise ValueError("Invalid investigation id")

    existing = load_investigation_memory(investigation_id)
    now = utc_now_iso()
    name = str(request.get("name") or existing.get("name") or investigation_id).strip() or investigation_id
    memory = request.get("memory") if isinstance(request.get("memory"), dict) else {}
    existing_memory = existing.get("memory") if isinstance(existing.get("memory"), dict) else {}
    return {
        "schema_version": 1,
        "investigation_id": investigation_id,
        "name": name,
        "created_at_utc": existing.get("created_at_utc") or now,
        "updated_at_utc": now,
        "memory": {
            "chat_summaries": normalize_memory_list(memory.get("chat_summaries", existing_memory.get("chat_summaries"))),
            "layers": normalize_memory_list(memory.get("layers", existing_memory.get("layers"))),
        }
    }


def load_investigation_memory(investigation_id: str) -> dict:
    try:
        path = investigation_memory_path(investigation_id)
    except ValueError:
        raise
    if not path.exists():
        return empty_investigation_memory(investigation_id)
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return empty_investigation_memory(investigation_id)
    if not isinstance(payload, dict):
        return empty_investigation_memory(investigation_id)
    memory = payload.get("memory") if isinstance(payload.get("memory"), dict) else {}
    return {
        "schema_version": 1,
        "investigation_id": str(payload.get("investigation_id") or investigation_id),
        "name": str(payload.get("name") or investigation_id),
        "created_at_utc": payload.get("created_at_utc") or utc_now_iso(),
        "updated_at_utc": payload.get("updated_at_utc") or payload.get("created_at_utc") or utc_now_iso(),
        "memory": {
            "chat_summaries": normalize_memory_list(memory.get("chat_summaries")),
            "layers": normalize_memory_list(memory.get("layers")),
        }
    }


def save_investigation_memory(request: dict) -> dict:
    payload = normalize_investigation_memory(request)
    INVESTIGATIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = investigation_memory_path(payload["investigation_id"])
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)
    return payload


def list_investigation_memory_metadata() -> list[dict]:
    if not INVESTIGATIONS_DIR.exists():
        return []
    items: list[dict] = []
    for path in sorted(INVESTIGATIONS_DIR.glob("*.json")):
        investigation_id = path.stem
        try:
            payload = load_investigation_memory(investigation_id)
        except ValueError:
            continue
        items.append(investigation_memory_metadata(payload))
    return sorted(items, key=lambda item: str(item.get("updated_at_utc") or ""), reverse=True)


def workstream_path(workstream_id: str) -> Path:
    if not WORKSTREAM_ID_PATTERN.fullmatch(workstream_id or ""):
        raise ValueError("Invalid workstream id")
    path = (WORKSTREAMS_DIR / f"{workstream_id}.json").resolve()
    if WORKSTREAMS_DIR.resolve() not in path.parents:
        raise ValueError("Invalid workstream path")
    return path


def normalize_workstream_text(value: Any, field: str, limit: int, required: bool = False) -> str:
    text = compact_text(value, limit)
    if required and not text:
        raise ValueError(f"Missing {field}")
    return text


def normalize_participants(value: Any) -> list[dict]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("Invalid participants")
    participants: list[dict] = []
    seen: set[str] = set()
    for raw in value[:20]:
        if not isinstance(raw, dict):
            raise ValueError("Invalid participant")
        participant_id = normalize_workstream_text(raw.get("participant_id"), "participant_id", 120, required=True)
        if participant_id in seen:
            raise ValueError("Duplicate participant_id")
        kind = normalize_workstream_text(raw.get("kind"), "participant kind", 20, required=True)
        if kind not in PARTICIPANT_KINDS:
            raise ValueError("Invalid participant kind")
        participants.append({
            "participant_id": participant_id,
            "kind": kind,
            "display_name": normalize_workstream_text(raw.get("display_name"), "participant display_name", 160),
            "role": normalize_workstream_text(raw.get("role"), "participant role", 160),
        })
        seen.add(participant_id)
    return participants


def normalize_assignments(value: Any, participant_ids: set[str]) -> list[dict]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("Invalid assignments")
    assignments: list[dict] = []
    seen: set[str] = set()
    for index, raw in enumerate(value[:30], start=1):
        if not isinstance(raw, dict):
            raise ValueError("Invalid assignment")
        assignment_id = normalize_workstream_text(
            raw.get("assignment_id") or f"assignment-{index}", "assignment_id", 120, required=True
        )
        if assignment_id in seen:
            raise ValueError("Duplicate assignment_id")
        owner_id = normalize_workstream_text(raw.get("owner_id"), "assignment owner_id", 120, required=True)
        if owner_id not in participant_ids:
            raise ValueError("Assignment owner is not a participant")
        assignments.append({
            "assignment_id": assignment_id,
            "owner_id": owner_id,
            "responsibility": normalize_workstream_text(
                raw.get("responsibility"), "assignment responsibility", 1200, required=True
            ),
            "status": "active",
        })
        seen.add(assignment_id)
    return assignments


def normalize_workstream_request(request: dict, existing: dict | None = None) -> dict:
    existing = existing or {}
    investigation_id = str(request.get("investigation_id", existing.get("investigation_id") or "")).strip()
    if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id):
        raise ValueError("Invalid investigation id")
    title = normalize_workstream_text(request.get("title", existing.get("title")), "title", 240, required=True)
    objective = normalize_workstream_text(
        request.get("objective", existing.get("objective")), "objective", 4000, required=True
    )
    status = normalize_workstream_text(request.get("status", existing.get("status") or "active"), "status", 30)
    if status not in WORKSTREAM_STATUSES or status == "archived" and existing.get("status") != "archived":
        raise ValueError("Invalid workstream status")
    participants = normalize_participants(request.get("participants", existing.get("participants") or []))
    assignments = normalize_assignments(
        request.get("assignments", existing.get("assignments") or []),
        {item["participant_id"] for item in participants},
    )
    return {
        "investigation_id": investigation_id,
        "title": title,
        "objective": objective,
        "status": status,
        "participants": participants,
        "assignments": assignments,
    }


def write_workstream(payload: dict) -> dict:
    WORKSTREAMS_DIR.mkdir(parents=True, exist_ok=True)
    path = workstream_path(payload["workstream_id"])
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)
    return payload


def create_workstream(request: dict) -> dict:
    normalized = normalize_workstream_request(request)
    now = utc_now_iso()
    workstream_id = f"ws_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{secrets.token_hex(4)}"
    return write_workstream({
        "schema_version": 1,
        "workstream_id": workstream_id,
        **normalized,
        "artifacts": [],
        "activity": [],
        "attention_requests": [],
        "created_at_utc": now,
        "updated_at_utc": now,
        "archived_at_utc": None,
    })


def apply_workstream_creation(investigation_id: str, creation: Any) -> dict | None:
    """Persist a Moshe creation handoff after the dedicated chat mode authorized this turn."""
    if not isinstance(creation, dict):
        return None
    title = normalize_workstream_text(creation.get("title"), "title", 240, required=True)
    objective = normalize_workstream_text(creation.get("objective"), "objective", 4000, required=True)
    responsibility = normalize_workstream_text(
        creation.get("responsibility"), "responsibility", 2000, required=True
    )
    return create_workstream({
        "investigation_id": investigation_id,
        "title": title,
        "objective": objective,
        "participants": [
            {
                "participant_id": "current-analyst",
                "kind": "human",
                "display_name": "אנליסט",
                "role": "owner",
            },
            {
                "participant_id": "moshe-targets-officer",
                "kind": "agent",
                "display_name": "משה",
                "role": "קצין מטרות",
            },
        ],
        "assignments": [{
            "assignment_id": "initial-responsibility",
            "owner_id": "moshe-targets-officer",
            "responsibility": responsibility,
        }],
    })


def load_workstream(workstream_id: str) -> dict | None:
    path = workstream_path(workstream_id)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or payload.get("workstream_id") != workstream_id:
        return None
    return payload


def workstream_metadata(payload: dict) -> dict:
    return {
        "workstream_id": payload.get("workstream_id"),
        "investigation_id": payload.get("investigation_id"),
        "title": payload.get("title"),
        "objective": payload.get("objective"),
        "status": payload.get("status"),
        "participant_count": len(payload.get("participants") or []),
        "assignment_count": len(payload.get("assignments") or []),
        "created_at_utc": payload.get("created_at_utc"),
        "updated_at_utc": payload.get("updated_at_utc"),
        "archived_at_utc": payload.get("archived_at_utc"),
    }


def list_workstreams(investigation_id: str) -> list[dict]:
    if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id or ""):
        raise ValueError("Invalid investigation id")
    if not WORKSTREAMS_DIR.exists():
        return []
    items: list[dict] = []
    for path in WORKSTREAMS_DIR.glob("ws_*.json"):
        payload = load_workstream(path.stem)
        if payload and payload.get("investigation_id") == investigation_id:
            items.append(workstream_metadata(payload))
    return sorted(items, key=lambda item: str(item.get("updated_at_utc") or ""), reverse=True)


def list_workstreams_with_latest_fallback(investigation_id: str) -> dict:
    exact = list_workstreams(investigation_id)
    if exact:
        return {
            "workstreams": exact,
            "canonical_investigation_id": investigation_id,
            "fallback_used": False,
        }
    if not WORKSTREAMS_DIR.exists():
        return {
            "workstreams": [],
            "canonical_investigation_id": investigation_id,
            "fallback_used": False,
        }
    groups: dict[str, list[dict]] = {}
    for path in WORKSTREAMS_DIR.glob("ws_*.json"):
        payload = load_workstream(path.stem)
        canonical_id = str(payload.get("investigation_id") or "") if payload else ""
        if payload and INVESTIGATION_ID_PATTERN.fullmatch(canonical_id):
            groups.setdefault(canonical_id, []).append(workstream_metadata(payload))
    if not groups:
        return {
            "workstreams": [],
            "canonical_investigation_id": investigation_id,
            "fallback_used": False,
        }
    canonical_id, items = max(
        groups.items(),
        key=lambda group: max(str(item.get("updated_at_utc") or "") for item in group[1]),
    )
    return {
        "workstreams": sorted(
            items, key=lambda item: str(item.get("updated_at_utc") or ""), reverse=True
        ),
        "canonical_investigation_id": canonical_id,
        "fallback_used": True,
    }


def update_workstream(workstream_id: str, request: dict) -> dict | None:
    existing = load_workstream(workstream_id)
    if existing is None:
        return None
    if existing.get("status") == "archived":
        raise ValueError("Archived workstream cannot be updated")
    requested_investigation_id = request.get("investigation_id")
    if requested_investigation_id is not None and str(requested_investigation_id).strip() != existing.get("investigation_id"):
        raise ValueError("Workstream investigation cannot be changed")
    normalized = normalize_workstream_request(request, existing)
    payload = {
        **existing,
        **normalized,
        "schema_version": 1,
        "workstream_id": workstream_id,
        "artifacts": normalize_memory_list(existing.get("artifacts")),
        "activity": normalize_memory_list(existing.get("activity")),
        "attention_requests": normalize_memory_list(existing.get("attention_requests")),
        "updated_at_utc": utc_now_iso(),
    }
    return write_workstream(payload)


def archive_workstream(workstream_id: str) -> dict | None:
    existing = load_workstream(workstream_id)
    if existing is None:
        return None
    if existing.get("status") == "archived":
        return existing
    now = utc_now_iso()
    return write_workstream({
        **existing,
        "status": "archived",
        "updated_at_utc": now,
        "archived_at_utc": now,
    })


def scenario_workstream_exists(workstream_id: str, investigation_id: str) -> bool:
    workstream = load_workstream(workstream_id)
    return bool(
        workstream
        and workstream.get("investigation_id") == investigation_id
        and workstream.get("status") != "archived"
    )


def parse_scenario_run_action(path: str) -> tuple[str, str] | None:
    prefix = "/api/scenario-runs/"
    if not path.startswith(prefix):
        return None
    remainder = path[len(prefix):].strip("/")
    parts = remainder.split("/")
    if len(parts) != 2 or parts[1] not in {"advance", "complete", "reset"}:
        return None
    return unquote(parts[0]), parts[1]


def prepared_playback_manifest() -> dict | None:
    scenarios = [
        item for item in list_scenarios(SCENARIO_MANIFESTS_DIR)
        if (item.get("scope") or {}).get("dataset") == DATASET_VERSION
    ]
    if not scenarios:
        return None
    selected = scenarios[0]
    return get_manifest(
        SCENARIO_MANIFESTS_DIR, selected["scenario_id"], selected["version"]
    )


def workstream_playback_status(workstream_id: str) -> dict | None:
    workstream = load_workstream(workstream_id)
    if workstream is None or workstream.get("status") == "archived":
        return None
    run = find_workstream_run(SCENARIO_RUNS_DIR, workstream_id)
    if run is not None:
        return {
            "workstream_id": workstream_id,
            "run": run_with_next_stage(SCENARIO_MANIFESTS_DIR, run),
        }
    manifest = prepared_playback_manifest()
    if manifest is None:
        return {"workstream_id": workstream_id, "run": None, "next_stage": None}
    first = manifest["stages"][0]
    return {
        "workstream_id": workstream_id,
        "run": None,
        "next_stage": {
            "sequence": first["sequence"],
            "timeframe": {
                "from": first["from"],
                "to": first["to"],
                "from_inclusive": True,
                "to_exclusive": True,
            },
        },
    }


def investigation_playback_status(investigation_id: str) -> dict:
    if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id or ""):
        raise ValueError("Invalid investigation id")
    policy = load_playback_visibility(SCENARIO_RUNS_DIR) or {}
    mode = policy.get("mode") if policy.get("mode") in {"historical", "real_time"} else "historical"
    event_times = sorted(
        str(item.get("timestamp_utc") or "")
        for item in load_ui_events()
        if item.get("timestamp_utc")
    )
    full_timeframe = {
        "from": event_times[0] if event_times else None,
        "to": event_times[-1] if event_times else None,
        "from_inclusive": True,
        "to_inclusive": True,
    }
    run = find_investigation_run(SCENARIO_RUNS_DIR, investigation_id)
    if run is not None:
        return {
            "investigation_id": investigation_id,
            "mode": mode,
            "full_timeframe": full_timeframe,
            "run": run_with_next_stage(SCENARIO_MANIFESTS_DIR, run),
        }
    manifest = prepared_playback_manifest()
    if manifest is None:
        return {
            "investigation_id": investigation_id,
            "mode": mode,
            "full_timeframe": full_timeframe,
            "run": None,
            "next_stage": None,
        }
    first = manifest["stages"][0]
    return {
        "investigation_id": investigation_id,
        "mode": mode,
        "full_timeframe": full_timeframe,
        "run": None,
        "next_stage": {
            "sequence": first["sequence"],
            "timeframe": {
                "from": first["from"],
                "to": first["to"],
                "from_inclusive": True,
                "to_exclusive": True,
            },
        },
    }


def artifact_id(prefix: str) -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{secrets.token_hex(4)}"


def resolve_workstream_event(layer_id: str, record_id: str) -> dict | None:
    event = next(
        (
            row for row in load_ui_events()
            if (row.get("record_id") or row.get("event_id")) == record_id
        ),
        None,
    )
    if event is None:
        return None
    canonical = dict(event)
    canonical["record_id"] = event.get("record_id") or event.get("event_id")
    canonical["summary"] = event.get("summary") or event.get("event_summary") or ""
    canonical["_canonical_layer_id"] = f"events:{event.get('source_type') or 'מקור לא ידוע'}"
    return canonical


def resolve_workstream_target(target_id: str) -> dict | None:
    result = get_ui_layer_rows(ATTACK_TARGET_CATALOG_LAYER_ID)
    if result is None:
        return None
    _, rows = result
    return next((row for row in rows if row.get("target_id") == target_id), None)


def bounded_workstream_context(value: Any, investigation_id: str) -> dict | None:
    """Load server-owned context; never trust browser-supplied artifact or participant data."""
    if not isinstance(value, dict):
        return None
    workstream_id = str(value.get("workstream_id") or "").strip()
    workstream = load_workstream(workstream_id) if workstream_id else None
    if not workstream or workstream.get("investigation_id") != investigation_id or workstream.get("status") == "archived":
        return None
    artifacts = list_artifacts(workstream)
    active_artifact = next(
        (item for item in artifacts if item.get("artifact_type") == "target_assessment_lead"
         and item.get("status") not in {"closed", "rejected"}),
        None,
    )
    pending = value.get("pending_proposal")
    if not isinstance(pending, dict) or pending.get("proposal_type") != "target_assessment_lead":
        pending = None
    return {
        "workstream_id": workstream_id,
        "title": workstream.get("title"),
        "objective": workstream.get("objective"),
        "active_artifact": active_artifact,
        "pending_proposal": pending,
        "current_turn_message_id": str(value.get("current_turn_message_id") or "").strip()[:160],
    }


def apply_workstream_action(context: dict | None, action: Any) -> tuple[dict | None, dict | None]:
    """Independently validate and apply a confirmed MCP handoff through the local service."""
    if not context or not isinstance(action, dict):
        return None, None
    decision = action.get("decision")
    if decision not in {"confirm", "send_to_assessment"}:
        return None, None
    proposal = action.get("proposal")
    if not isinstance(proposal, dict) or proposal.get("proposal_type") != "target_assessment_lead":
        raise ValueError("Invalid confirmed workstream proposal")
    current_turn = str(action.get("current_turn_message_id") or "").strip()
    proposed_turn = str(proposal.get("proposed_turn_message_id") or "").strip()
    if not current_turn or not proposed_turn or current_turn == proposed_turn:
        raise ValueError("Confirmation requires a distinct later user turn")
    if current_turn != context.get("current_turn_message_id"):
        raise ValueError("Confirmation turn does not match the current request")
    workstream = load_workstream(context["workstream_id"])
    if not workstream:
        raise ValueError("Workstream no longer exists")
    human = next((item for item in workstream.get("participants") or [] if item.get("kind") == "human"), None)
    if not human:
        raise ValueError("Workstream has no human participant")
    confirmation = {
        "message_id": current_turn,
        "text": str(action.get("confirmation_text") or "").strip() or "Confirmed in chat",
    }
    actor = {"participant_id": human["participant_id"], "kind": "human"}
    now = utc_now_iso()
    proposal_action = "send_to_assessment" if decision == "send_to_assessment" else proposal.get("action")
    if proposal_action == "create":
        content = {
            "subject_reference": (
                {"kind": "target", "target_id": proposal["target_id"]}
                if proposal.get("target_id") else None
            ),
            "lead_statement": proposal.get("lead_statement"),
            "indications": [
                {
                    "source_reference": {
                        "kind": "event_record",
                        "record_id": item.get("record_id"),
                    },
                    "role": item.get("role"),
                    "relevance": item.get("relevance"),
                    "annotation": item.get("annotation"),
                }
                for item in proposal.get("indications") or []
            ],
            "supporting_signals": proposal.get("supporting_signals") or [],
            "contradictions": proposal.get("contradictions") or [],
            "assessment_questions": proposal.get("assessment_questions") or [],
            "gaps": proposal.get("gaps") or [],
            "assigned_to": proposal.get("assigned_to"),
            "annotation": proposal.get("annotation"),
        }
        artifact = create_artifact(
            workstream, {
                "artifact_type": "target_assessment_lead",
                "actor": actor, "confirmation_turn": confirmation, "content": content,
            },
            resolve_event=resolve_workstream_event, resolve_target=resolve_workstream_target,
            now=now, id_factory=artifact_id,
        )
    else:
        artifact_value = context.get("active_artifact") or {}
        artifact_id_value = proposal.get("artifact_id") or artifact_value.get("artifact_id")
        revision = proposal.get("expected_revision") or artifact_value.get("revision")
        payload = proposal.get("payload") if isinstance(proposal.get("payload"), dict) else {}
        if proposal_action == "add_indication":
            indications = proposal.get("indications") or []
            if len(indications) != 1:
                raise ValueError("add_indication requires exactly one indication")
            item = indications[0]
            payload = {"indication": {
                "source_reference": {"kind": "event_record", "record_id": item.get("record_id")},
                "role": item.get("role"), "relevance": item.get("relevance"), "annotation": item.get("annotation"),
            }}
        artifact = revise_artifact(
            workstream, str(artifact_id_value or ""), {
                "expected_revision": revision, "action": proposal_action, "payload": payload,
                "actor": actor, "confirmation_turn": confirmation,
            },
            resolve_event=resolve_workstream_event, now=now, id_factory=artifact_id,
        )
    write_workstream(workstream)
    return artifact, None


def parse_artifact_api_path(path: str) -> tuple[str, str | None, bool] | None:
    prefix = "/api/workstreams/"
    if not path.startswith(prefix):
        return None
    parts = [unquote(part) for part in path[len(prefix):].split("/") if part]
    if len(parts) == 2 and parts[1] == "artifacts":
        return parts[0], None, False
    if len(parts) == 3 and parts[1] == "artifacts":
        return parts[0], parts[2], False
    if len(parts) == 4 and parts[1] == "artifacts" and parts[3] == "revisions":
        return parts[0], parts[2], True
    return None


def saved_question_metadata(payload: dict) -> dict:
    result = payload.get("result") if isinstance(payload.get("result"), dict) else {}
    return {
        "id": payload.get("id"),
        "title": payload.get("title") or payload.get("question") or "שאלה שמורה",
        "question": payload.get("question") or "",
        "saved_at_utc": payload.get("saved_at_utc"),
        "source_run_id": payload.get("source_run_id") or result.get("run_id"),
        "recommended_view": result.get("recommended_view") or "evidence",
        "step_count": len(result.get("investigation_steps") or []),
    }


def load_saved_questions() -> list[dict]:
    if not SAVED_QUESTIONS_DIR.exists():
        return []
    saved: list[dict] = []
    for path in sorted(SAVED_QUESTIONS_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        result = payload.get("result")
        if not payload.get("id") or not payload.get("question") or not isinstance(result, dict) or not result.get("answer"):
            continue
        saved.append(payload)
    return sorted(saved, key=lambda item: str(item.get("saved_at_utc") or ""), reverse=True)


def list_saved_question_metadata() -> list[dict]:
    return [saved_question_metadata(item) for item in load_saved_questions()]


def load_saved_question(saved_id: str) -> dict | None:
    try:
        path = saved_question_path(saved_id)
    except ValueError:
        return None
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    result = payload.get("result")
    if not payload.get("question") or not isinstance(result, dict) or not result.get("answer"):
        return None
    return payload


def create_saved_question(request: dict) -> dict:
    question = str(request.get("question") or "").strip()
    result = request.get("result")
    if not question:
        raise ValueError("Missing question")
    if not isinstance(result, dict):
        raise ValueError("Missing result")
    if not str(result.get("answer") or "").strip():
        raise ValueError("Missing result answer")
    if not isinstance(result.get("investigation_steps"), list):
        result = {**result, "investigation_steps": []}
    now = utc_now_iso()
    saved_id = f"saved_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{secrets.token_hex(3)}"
    raw_title = str(request.get("title") or "").strip()
    title = raw_title or question[:60]
    payload = {
        "id": saved_id,
        "schema_version": 1,
        "title": title,
        "question": question,
        "saved_at_utc": now,
        "source_run_id": result.get("run_id"),
        "result": result,
    }
    SAVED_QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = saved_question_path(saved_id)
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)
    return payload


def delete_saved_question(saved_id: str) -> bool:
    path = saved_question_path(saved_id)
    if not path.exists():
        return False
    path.unlink()
    return True


class SSHHTTPConnection(http.client.HTTPConnection):
    def __init__(self, ssh_client, remote_host, remote_port, timeout=30):
        super().__init__(remote_host, remote_port, timeout=timeout)
        self.ssh_client = ssh_client

    def connect(self):
        transport = self.ssh_client.get_transport()
        if transport is None:
            raise ConnectionError("SSH transport is unavailable")
        self.sock = transport.open_channel(
            "direct-tcpip",
            (self.host, self.port),
            ("127.0.0.1", 0),
            timeout=self.timeout,
        )


class HermesSession:
    def __init__(self, config):
        self.config = config
        self.direct = config.get("transport") == "direct"
        if not self.direct and paramiko is None:
            raise RuntimeError("paramiko is required for SSH Hermes transport")
        self.ssh = None if self.direct else paramiko.SSHClient()
        if self.ssh:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self):
        if self.ssh:
            self.ssh.connect(
                self.config["host"],
                username=self.config["user"],
                key_filename=self.config["key_path"],
                look_for_keys=False,
                allow_agent=False,
                timeout=15,
            )
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.ssh:
            self.ssh.close()

    def request(self, method, path, body=None, timeout=60, parse_json=True):
        if self.direct:
            connection = http.client.HTTPConnection(
                self.config["remote_host"],
                int(self.config["remote_port"]),
                timeout=timeout,
            )
        else:
            connection = SSHHTTPConnection(
                self.ssh,
                self.config["remote_host"],
                int(self.config["remote_port"]),
                timeout=timeout,
            )
        encoded = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Accept": "application/json" if parse_json else "text/event-stream",
        }
        if encoded is not None:
            headers["Content-Type"] = "application/json; charset=utf-8"
        try:
            connection.request(method, path, body=encoded, headers=headers)
            response = connection.getresponse()
            raw = response.read().decode("utf-8", errors="replace")
            if response.status >= 400:
                raise RuntimeError(f"Hermes API {response.status}: {raw}")
            return (json.loads(raw) if raw else {}) if parse_json else raw
        finally:
            connection.close()

    def ssh_command(self, command, timeout=30):
        if self.direct:
            import subprocess
            completed = subprocess.run(
                command,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
            )
            if completed.returncode:
                raise RuntimeError(completed.stderr or completed.stdout or f"Command failed: {completed.returncode}")
            return completed.stdout
        _, stdout, stderr = self.ssh.exec_command(command, timeout=timeout)
        code = stdout.channel.recv_exit_status()
        output = stdout.read().decode("utf-8", errors="replace")
        error = stderr.read().decode("utf-8", errors="replace")
        if code:
            raise RuntimeError(error or output or f"SSH command failed: {code}")
        return output


class HermesClient:
    def __init__(self, config):
        self.config = config

    def request(self, method, path, body=None, timeout=60, parse_json=True):
        if self.config.get("transport") == "direct":
            connection = http.client.HTTPConnection(
                self.config["remote_host"],
                int(self.config["remote_port"]),
                timeout=timeout,
            )
            ssh = None
        else:
            if paramiko is None:
                raise RuntimeError("paramiko is required for SSH Hermes transport")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                self.config["host"],
                username=self.config["user"],
                key_filename=self.config["key_path"],
                look_for_keys=False,
                allow_agent=False,
                timeout=15,
            )
            connection = SSHHTTPConnection(
                ssh,
                self.config["remote_host"],
                int(self.config["remote_port"]),
                timeout=timeout,
            )
        try:
            encoded = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
            headers = {
                "Authorization": f"Bearer {self.config['api_key']}",
                "Accept": "application/json" if parse_json else "text/event-stream",
            }
            if encoded is not None:
                headers["Content-Type"] = "application/json; charset=utf-8"
            connection.request(method, path, body=encoded, headers=headers)
            response = connection.getresponse()
            raw = response.read().decode("utf-8", errors="replace")
            if response.status >= 400:
                raise RuntimeError(f"Hermes API {response.status}: {raw}")
            return (json.loads(raw) if raw else {}) if parse_json else raw
        finally:
            connection.close()
            if ssh:
                ssh.close()

    def ssh_command(self, command, timeout=30):
        if self.config.get("transport") == "direct":
            import subprocess
            completed = subprocess.run(
                command,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
            )
            if completed.returncode:
                raise RuntimeError(completed.stderr or completed.stdout or f"Command failed: {completed.returncode}")
            return completed.stdout
        if paramiko is None:
            raise RuntimeError("paramiko is required for SSH Hermes transport")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            self.config["host"], username=self.config["user"],
            key_filename=self.config["key_path"], look_for_keys=False,
            allow_agent=False, timeout=15,
        )
        try:
            _, stdout, stderr = ssh.exec_command(command, timeout=timeout)
            code = stdout.channel.recv_exit_status()
            output = stdout.read().decode("utf-8", errors="replace")
            error = stderr.read().decode("utf-8", errors="replace")
            if code:
                raise RuntimeError(error or output or f"SSH command failed: {code}")
            return output
        finally:
            ssh.close()

    @staticmethod
    def summarize_audit(records):
        def format_ids(ids, limit=14):
            values = [str(value) for value in ids if value]
            if len(values) <= limit:
                return ", ".join(values) if values else "אין"
            return f'{", ".join(values[:limit])}, ועוד {len(values) - limit} מזהים'

        def compact_json(value):
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

        def public_args(args):
            return {key: value for key, value in args.items() if key != "step_bridge"}

        def extract_identifiers(value, depth=0):
            if depth > 6:
                return []
            identifiers = []
            if isinstance(value, dict):
                for key, item in value.items():
                    if key.endswith("_id") and isinstance(item, (str, int)) and item:
                        identifiers.append(item)
                    elif key.endswith("_ids") and isinstance(item, list):
                        identifiers.extend(entry for entry in item if isinstance(entry, (str, int)) and entry)
                    else:
                        identifiers.extend(extract_identifiers(item, depth + 1))
            elif isinstance(value, list):
                for item in value:
                    identifiers.extend(extract_identifiers(item, depth + 1))
            return list(dict.fromkeys(str(identifier) for identifier in identifiers if identifier))

        def identifiers_text(*values):
            identifiers = []
            for value in values:
                identifiers.extend(extract_identifiers(value))
            identifiers = list(dict.fromkeys(identifiers))
            return f' מזהים: {format_ids(identifiers)}.' if identifiers else ""

        def target_candidate(result):
            candidate = result.get("candidate")
            return candidate if isinstance(candidate, dict) else {}

        def arg_clue(tool, args):
            if tool == "classify_question_intent":
                return f'השאלה "{args.get("question", "")}"'
            if tool in {"resolve_location", "resolve_event_reference", "resolve_entity"}:
                return f'"{args.get("query", "")}"'
            if tool == "trace_identifier":
                return f'המזהה "{args.get("identifier", "")}"'
            if tool == "trace_semantic_clues":
                clues = args.get("clues") or []
                seeds = args.get("seed_event_ids") or []
                if clues:
                    return f'הרמזים {format_ids(clues)}'
                return f'רמזים מתוך אירועי העוגן {format_ids(seeds)}'
            if tool == "semantic_search_events":
                seeds = args.get("seed_event_ids") or []
                query = args.get("query") or ""
                if seeds:
                    return f'השאלה הסמנטית "{query}" מתוך עוגנים {format_ids(seeds)}'
                return f'השאלה הסמנטית "{query}"'
            if tool == "plan_next_investigation_step":
                return f'מצב החקירה: {args.get("objective") or "יעד לא צוין"}'
            if tool == "get_objects":
                ids = (args.get("event_ids") or []) + (args.get("location_ids") or []) + (args.get("entity_ids") or [])
                return f'מזהי האובייקטים {format_ids(ids)}'
            if tool == "prepare_target_candidate":
                return f'רשומות העוגן {format_ids(args.get("event_ids") or [])}'
            if tool in {"get_target_candidate", "update_target_candidate", "attach_target_evidence"}:
                return f'מועמד המטרה {args.get("target_id") or "לא צוין"}'
            if tool == "find_duplicate_target_candidates":
                return f'מועמד במיקום {args.get("location_id") or "לא צוין"} ובסוג {args.get("object_class") or "לא צוין"}'
            if tool == "search_target_candidates":
                return "מאגר מועמדי המטרות"
            if tool == "create_target_candidate":
                return f'המועמד {((args.get("candidate") or {}).get("target_id")) or "החדש"}'
            if tool == "find_related_events":
                return f'אירועי העוגן {format_ids(args.get("seed_event_ids") or [])}'
            if tool == "explain_linkage":
                return f'המעבר בין {args.get("first_event_id") or "אירוע ראשון"} לבין {args.get("second_event_id") or "אירוע שני"}'
            if tool == "build_event_sequence":
                return f'קבוצת האירועים {format_ids(args.get("event_ids") or [])}'
            if tool == "challenge_hypothesis":
                return f'ההשערה על בסיס {format_ids(args.get("supporting_event_ids") or [])}'
            if tool == "find_actor_history":
                actors = args.get("actors") or []
                return f'הגורם "{actors[0]}"' if len(actors) == 1 else f'הגורמים {format_ids(actors)}'
            if tool == "aggregate_events":
                return f'ממד הקיבוץ {args.get("group_by") or "לא צוין"}'
            filters = {key: value for key, value in public_args(args).items() if value not in (None, "", [], False)}
            return f'מסנני החיפוש {compact_json(filters)}' if filters else "חיפוש פתוח ללא מסננים"

        def result_clue(result):
            ids = result.get("event_ids") or [item.get("event_id") for item in result.get("events") or []]
            ids = [item for item in ids if item]
            if ids:
                return f'מזהים שעלו: {format_ids(ids)}'
            matches = result.get("matches") or []
            if matches:
                labels = [item.get("canonical_name") or item.get("entity_id") for item in matches]
                return f'ישויות שעלו: {format_ids(labels)}'
            locations = result.get("locations") or []
            if locations:
                labels = [item.get("name") or item.get("location_id") for item in locations]
                return f'מיקומים שעלו: {format_ids(labels)}'
            location_layers = result.get("location_layers") or []
            if location_layers:
                labels = [item.get("location_name") or item.get("location_id") for item in location_layers]
                return f'מיקומים שעלו: {format_ids(labels)}'
            entity_layers = result.get("entity_layers") or []
            if entity_layers:
                labels = [item.get("canonical_name") or item.get("entity_id") for item in entity_layers]
                return f'ישויות שעלו: {format_ids(labels)}'
            alternatives = result.get("alternative_event_ids") or []
            if alternatives:
                return f'חלופות שעלו: {format_ids(alternatives)}'
            return "השלב הקודם צמצם את מרחב החיפוש"

        def derived_bridge(tool, args, index, previous_result):
            clue = arg_clue(tool, args)
            if index == 0:
                observed = f'נקודת הפתיחה של החקירה היא {clue}.'
            else:
                observed = f'{result_clue(previous_result or {})}; מזה הסוכן עבר לבדוק את {clue}.'

            if tool == "classify_question_intent":
                decision = "לפני בחירת כלי נתונים, הסוכן מסווג את סוג הבקשה כדי לבחור מסלול עבודה ותקציב מתאים."
                expected = "לקבל מצב עבודה, תקציב כלים, משפחות כלים מותרות וחסומות, ורמז לתצוגה."
            elif tool == "resolve_location":
                decision = f'צריך להפוך את הביטוי {clue} למיקום מוכר כדי שכל חיפוש המשך יהיה ממוקד.'
                expected = "לקבל מזהי מיקום קנוניים או להבין שאין התאמה גאוגרפית ברורה."
            elif tool == "resolve_event_reference":
                decision = f'צריך להפוך את ההפניה {clue} לאירוע עוגן מדויק לפני הרחבת החקירה.'
                expected = "לקבל מזהה אירוע, זמן ומיקום שישמשו בסיס לצעדים הבאים."
            elif tool == "search_events":
                decision = f'הסוכן משתמש ב-{clue} כדי למצוא רשומות שעומדות בתנאי החיפוש ולאסוף מועמדים ראשונים.'
                expected = "לקבל רשימת אירועים מצומצמת שאפשר לאמת או להרחיב ממנה."
            elif tool == "semantic_search_events":
                decision = f'הסוכן משתמש ב-{clue} כאשר הרמזים או ניסוח השאלה עשויים להופיע במאגר במילים אחרות.'
                expected = "לקבל מועמדי אירועים דומים סמנטית עם מזהי REC, ציון התאמה ורציונל קצר."
            elif tool == "get_objects":
                decision = f'הסוכן קורא את הרשומות המלאות של {clue} כדי לא להסתמך רק על מזהים או תקצירים.'
                expected = "לאמת את תוכן האירועים, המיקומים או הישויות לפני הסקת קשר או הצגה."
            elif tool == "find_actor_history":
                decision = f'{clue} עשוי לקשור בין אירועים, לכן הסוכן בודק היסטוריה וכינויים.'
                expected = "למצוא הופעות נוספות של אותו גורם או להבין שהוא אינו יוצר רצף."
            elif tool == "aggregate_events":
                decision = f'הסוכן מקבץ לפי {clue} כדי לזהות ריכוזים או חריגות שלא בולטים באירוע יחיד.'
                expected = "לקבל תמונת התפלגות שתכוון לחיפוש ממוקד יותר."
            elif tool == "explain_linkage":
                decision = f'לפני הצגת מעבר בשרשרת, הסוכן בודק אם {clue} נתמך בגשר ראייתי ולא רק בסיפור רציף.'
                expected = "לקבל את סוג הגשר, חוזקו, או אזהרה שהמעבר הוא פער."
            elif tool == "build_event_sequence":
                decision = f'לאחר שנאספו כמה אירועים, הסוכן מסדר את {clue} כדי לבדוק אם יש רצף ולא רק סמיכות.'
                expected = "לראות סדר זמנים ומסלול, ולזהות קפיצות או חוליות חסרות."
            elif tool == "resolve_entity":
                decision = f'השם {clue} עלול להיות כינוי או שם חלקי, לכן הסוכן בודק אם הוא שייך לישות מוכרת.'
                expected = "לקבל שם קנוני וכינויים שישמשו לחיפושים הבאים."
            elif tool == "trace_identifier":
                negated = " כולל אזכורים שוללים" if args.get("include_negated") else ""
                decision = f'הערך {clue} נראה כמו מזהה חוזר, ולכן הסוכן עוקב אחר הופעותיו במקורות נוספים{negated}.'
                expected = "למצוא אירועים שמחוברים באותו מזהה, או לשלול שהמזהה חוזר בשרשרת."
            elif tool == "trace_semantic_clues":
                negated = " כולל אזכורים שוללים" if args.get("include_negated") else ""
                decision = f'הערך {clue} הוא רמז תפעולי ולא מזהה פורמלי, לכן הסוכן מחפש הופעות סמנטיות שלו במקורות נוספים{negated}.'
                expected = "למצוא חוליות שבהן אותו חפץ, מסלול, מחסן, כלי רכב או ניסוח תפעולי מחבר בין אירועים."
            elif tool == "plan_next_investigation_step":
                decision = "הסוכן עוצר לבקרת תהליך כדי לוודא שלא נשארו seeds מומלצים, רמזים סמנטיים או גשרים סמוכים שלא נבדקו לפני סיכום."
                expected = "לקבל אילוץ לצעד הבא, מזהים או רמזים שחובה לטפל בהם, וכלים שחסומים עד להשלמת הבדיקה."
            elif tool == "find_related_events":
                decision = f'במקום להישאר סביב אירוע יחיד, הסוכן מרחיב מ-{clue} לפי קשרי זמן, מקום, ישות ומזהים.'
                expected = "לאתר חוליות סמוכות או מוקדמות שמקבלות ניקוד קשר גבוה."
            elif tool == "challenge_hypothesis":
                decision = f'לפני חיזוק ההשערה, הסוכן בודק את {clue} מול חלופות ופערים.'
                expected = "לגלות הסברים תמימים, סתירות או חסרים שמחלישים את הרצף."
            elif tool == "prepare_target_candidate":
                decision = f'משה בודק את {clue}, מאתר חיזוקים ומעריך אם ניתן ליצור מועמד מטרה.'
                expected = "לקבל החלטת כשירות, ביטחון, כמות ורשומות תומכות בלי לשמור עדיין."
            elif tool == "find_duplicate_target_candidates":
                decision = f'לפני יצירה, משה בודק אם {clue} כבר קיים במאגר.'
                expected = "למנוע יצירת מטרה כפולה ולהחזיר מזהי מועמדים דומים אם קיימים."
            elif tool in {"search_target_candidates", "get_target_candidate"}:
                decision = f'משה קורא את {clue} כדי להציג או להמשיך לעבוד על מטרה קיימת.'
                expected = "לקבל תקציר מטרה ומזהים רלוונטיים מתוך המאגר."
            elif tool in {"create_target_candidate", "update_target_candidate", "attach_target_evidence"}:
                decision = f'משה מעדכן את {clue} לאחר בדיקות הכשירות והכפילויות.'
                expected = "לקבל אישור קצר, מצב מעודכן ומזהים רלוונטיים."
            elif tool == "present_requested_results":
                decision = "הסוכן בוחר רק את הנתונים שעונים ישירות לבקשת המשתמש עבור כפתור הצג תוצאות."
                expected = "לקבל בנפרד שכבות תוצאה מבוקשות ושכבות ראיות תומכות מאומתות."
            else:
                decision = f'הסוכן משתמש ב-{clue} כדי לצמצם אי-ודאות ולהחליט על המשך החקירה.'
                expected = "לקבל פלט שיאשר, ישלול או ימקד את כיוון החקירה."
            return observed, decision, expected

        def extract_event_ids(value, depth=0):
            if depth > 5:
                return []
            ids = []
            if isinstance(value, dict):
                for key, item in value.items():
                    if any(marker in key for marker in ("missing", "excluded", "blocked")):
                        continue
                    if key == "event_id" and item:
                        ids.append(item)
                    elif key.endswith("event_id") and item:
                        ids.append(item)
                    elif key.endswith("event_ids") and isinstance(item, list):
                        ids.extend(entry for entry in item if entry)
                    else:
                        ids.extend(extract_event_ids(item, depth + 1))
            elif isinstance(value, list):
                for item in value:
                    ids.extend(extract_event_ids(item, depth + 1))
            return ids

        steps = []
        previous_result = None
        for index, record in enumerate(records):
            tool = record.get("tool", "MCP")
            args = record.get("arguments") or {}
            result = record.get("result") or {}
            observed_clue, decision, expected_value = derived_bridge(tool, args, index, previous_result)
            model_bridge = str(args.get("step_bridge") or "").strip()
            bridge_summary = model_bridge or decision
            if tool == "classify_question_intent":
                action = f'סיווג כוונת השאלה "{args.get("question", "")}".'
                outcome = (
                    f'הכוונה סווגה כ-{result.get("intent")}; מצב עבודה {result.get("recommended_mode")}; '
                    f'תקציב כלים {result.get("tool_budget")}; תצוגה מומלצת {result.get("recommended_view_hint")}; '
                    f'סיבה: {result.get("reason")}.'
                )
            elif tool == "resolve_location":
                action = f'פתרון הביטוי הגאוגרפי "{args.get("query", "")}" למזהי מיקום.'
                locations = result.get("locations") or []
                labels = [f'{item.get("location_id")} ({item.get("name")})' for item in locations]
                outcome = f'נמצאו {len(labels)} מיקומים: {", ".join(labels) if labels else "אין התאמות"}.'
            elif tool == "resolve_event_reference":
                action = f'פתרון ההפניה "{args.get("query", "")}" לאירוע עוגן.'
                ids = result.get("event_ids") or []
                times = [item.get("timestamp_utc") for item in result.get("events") or [] if item.get("timestamp_utc")]
                outcome = f'נמצאו {len(ids)} אירועים: {format_ids(ids)}' + (f'; זמנים: {", ".join(times)}.' if times else ".")
            elif tool in {"search_events", "find_actor_history"}:
                filters = []
                for key in ["start_time", "end_time", "location_ids", "actors", "source_types", "keywords", "night_only", "limit"]:
                    value = args.get(key)
                    if value not in (None, "", [], False):
                        filters.append(f"{key}={json.dumps(value, ensure_ascii=False)}")
                action = f'חיפוש במאגר עם המסננים: {"; ".join(filters) if filters else "ללא מסננים"}.'
                ids = result.get("event_ids") or []
                total = result.get("total", len(ids))
                returned = result.get("returned", len(ids))
                truncated = bool(result.get("truncated") or (isinstance(total, int) and isinstance(returned, int) and total > returned))
                warning = " זוהי תוצאה מקוצצת; אין לבחור ממנה עוגן חקירתי בלי צמצום נוסף או הגדלת limit." if truncated else ""
                outcome = f'נמצאו {total} רשומות; הוחזרו {returned}; מזהים: {format_ids(ids)}.{warning}'
            elif tool == "semantic_search_events":
                filters = []
                for key in ["query", "seed_event_ids", "start_time", "end_time", "location_ids", "entity_ids", "source_types", "reliabilities", "certainty_levels", "keywords", "match_all_keywords", "limit"]:
                    value = args.get(key)
                    if value not in (None, "", [], False):
                        filters.append(f"{key}={json.dumps(value, ensure_ascii=False)}")
                action = f'חיפוש סמנטי במאגר עם המסננים: {"; ".join(filters) if filters else "ללא מסננים"}.'
                ids = result.get("event_ids") or []
                returned = result.get("returned", len(ids))
                backend = result.get("semantic_backend") or result.get("backend") or "לא צוין"
                top_scores = [
                    f'{item.get("event_id")}={round(float(item.get("semantic_score") or 0), 3)}'
                    for item in (result.get("matches") or [])[:5]
                    if item.get("event_id")
                ]
                score_text = f'; ציונים מובילים: {", ".join(top_scores)}' if top_scores else ""
                outcome = f'הוחזרו {returned} מועמדים סמנטיים באמצעות {backend}: {format_ids(ids)}{score_text}.'
            elif tool == "get_objects":
                object_type = args.get("object_type") or result.get("object_type") or "event"
                event_ids = [item.get("event_id") for item in result.get("events") or [] if item.get("event_id")]
                location_ids = [item.get("location_id") for item in result.get("location_layers") or [] if item.get("location_id")]
                entity_ids = [item.get("entity_id") for item in result.get("entity_layers") or [] if item.get("entity_id")]
                requested = (args.get("event_ids") or []) + (args.get("location_ids") or []) + (args.get("entity_ids") or []) + (args.get("names_or_aliases") or [])
                action = f'שליפת אובייקטים מסוג {object_type}: {format_ids(requested)}.'
                outcome = (
                    f'הוחזרו {len(event_ids)} אירועים, {len(location_ids)} מיקומים ו-{len(entity_ids)} ישויות; '
                    f'אירועים: {format_ids(event_ids)}; מיקומים: {format_ids(location_ids)}; ישויות: {format_ids(entity_ids)}.'
                )
            elif tool == "aggregate_events":
                group_by = args.get("group_by")
                filters = {key: value for key, value in public_args(args).items() if key != "group_by" and value not in (None, "", [], False)}
                action = f'קיבוץ אירועים לפי {group_by} עם מסננים {json.dumps(filters, ensure_ascii=False)}.'
                groups = result.get("groups") or []
                group_text = ", ".join(f'{item.get("label")}={item.get("count")}' for item in groups[:12])
                outcome = f'נכללו {result.get("total_events", 0)} אירועים; קבוצות: {group_text if group_text else "אין"}.'
            elif tool == "explain_linkage":
                action = f'בדיקת גשר ראייתי בין {args.get("first_event_id")} לבין {args.get("second_event_id")}.'
                bridges = result.get("bridges") or []
                bridge_text = ", ".join(f'{item.get("bridge_type")} ({item.get("detail")})' for item in bridges[:4])
                outcome = f'נמצאו {result.get("bridge_count", 0)} גשרים; {bridge_text if bridge_text else "לא נמצא גשר"}; הערכה: {result.get("assessment") or "אין"}.'
            elif tool == "build_event_sequence":
                requested = args.get("event_ids") or []
                route = result.get("route") or []
                route_text = " -> ".join(f'{item.get("location_name")} [{", ".join(item.get("event_ids") or [])}]' for item in route)
                action = f'מיון כרונולוגי של {len(requested)} אירועים: {format_ids(requested)}.'
                outcome = f'נבנה רצף של {result.get("event_count", 0)} אירועים בין {result.get("start_time")} ל-{result.get("end_time")}; מסלול: {route_text or "לא נבנה"}.'
            elif tool == "resolve_entity":
                action = f'פתרון שם הגורם "{args.get("query", "")}" לישות קנונית ולכינויים.'
                matches = result.get("matches") or []
                labels = [f'{item.get("entity_id")} ({item.get("canonical_name")})' for item in matches]
                outcome = f'נמצאו {len(matches)} התאמות: {", ".join(labels) if labels else "אין"}.'
            elif tool == "trace_identifier":
                action = f'מעקב אחר המזהה "{args.get("identifier", "")}" מסוג {args.get("identifier_type") or "אוטומטי"}.'
                ids = result.get("event_ids") or []
                excluded = result.get("excluded_negated_mentions", 0)
                outcome = f'נמצאו {result.get("total_mentions", len(ids))} אזכורים והוחזרו {len(ids)} אירועים: {format_ids(ids)}; הושמטו {excluded} אזכורים שוללים.'
            elif tool == "trace_semantic_clues":
                clues = args.get("clues") or result.get("clues") or []
                seeds = args.get("seed_event_ids") or []
                action = f'מעקב אחר רמזים סמנטיים {format_ids(clues)} מתוך עוגנים {format_ids(seeds)}.'
                ids = result.get("event_ids") or []
                total = result.get("total_matches", len(ids))
                returned = result.get("returned", len(ids))
                truncated = bool(result.get("truncated") or (isinstance(total, int) and isinstance(returned, int) and total > returned))
                warning = " זוהי תוצאה מקוצצת; יש לצמצם או להמשיך הרחבה לפני שלילת קשר." if truncated else ""
                recommended = [item.get("event_id") for item in result.get("recommended_next_seeds") or [] if item.get("event_id")]
                new_clues = result.get("new_clues_to_trace") or []
                recommendation = ""
                if recommended:
                    recommendation = f' seeds מומלצים להמשך: {format_ids(recommended)}.'
                if new_clues:
                    recommendation += f' רמזים חדשים: {format_ids(new_clues)}.'
                outcome = f'נמצאו {total} התאמות סמנטיות והוחזרו {returned}: {format_ids(ids)}.{recommendation}{warning}'
            elif tool == "plan_next_investigation_step":
                action = "בדיקת בקרה תהליכית למצב החקירה לפני בחירת הצעד הבא."
                required_ids = result.get("required_event_ids") or []
                required_clues = result.get("required_clues") or []
                blocked = result.get("blocked_tool_families") or []
                allowed = result.get("allowed_tool_families") or []
                state_summary = result.get("state_summary") or {}
                parts = [
                    f'אילוץ הצעד הבא: {result.get("next_step_constraint") or "לא צוין"}',
                    f'החלטה: {result.get("decision") or "לא צוין"}',
                    f'סיבה: {result.get("reason") or "לא צוינה"}',
                ]
                if required_ids:
                    parts.append(f'מזהים שחובה לטפל בהם: {format_ids(required_ids)}')
                if required_clues:
                    parts.append(f'רמזים שחובה לבדוק: {format_ids(required_clues)}')
                if allowed:
                    parts.append(f'כלים מותרים: {format_ids(allowed)}')
                if blocked:
                    parts.append(f'כלים חסומים זמנית: {format_ids(blocked)}')
                if state_summary:
                    parts.append(
                        "מצב קצר: "
                        f'שרשרת={state_summary.get("candidate_chain_length", 0)}, '
                        f'seeds פתוחים={state_summary.get("unexpanded_recommended_seed_count", 0)}, '
                        f'רמזים חדשים={state_summary.get("new_clue_count", 0)}, '
                        f'תקציב נותר={state_summary.get("tool_budget_remaining", 0)}'
                    )
                outcome = "; ".join(parts) + "."
            elif tool == "find_related_events":
                seeds = args.get("seed_event_ids") or []
                source_filter = args.get("source_types") or []
                source_text = f' וסוגי מקור {format_ids(source_filter)}' if source_filter else ""
                action = f'הרחבת ראיות העוגן {format_ids(seeds)} לפי {", ".join(args.get("dimensions") or ["entity", "identifier", "semantic", "time", "location"])}{source_text}.'
                ids = result.get("event_ids") or []
                total = result.get("total_candidates", len(ids))
                returned = result.get("returned", len(ids))
                truncated = bool(result.get("truncated") or (isinstance(total, int) and isinstance(returned, int) and total > returned))
                warning = " זוהי הרחבה מקוצצת; אין להסיק שאין המשך שרשרת בלי הגדלת limit, צמצום ממוקד או הרחבה נוספת." if truncated else ""
                recommended = [item.get("event_id") for item in result.get("recommended_next_seeds") or [] if item.get("event_id")]
                new_clues = result.get("new_clues_to_trace") or []
                recommendation = ""
                if recommended:
                    recommendation = f' seeds מומלצים להמשך: {format_ids(recommended)}.'
                if new_clues:
                    recommendation += f' רמזים חדשים: {format_ids(new_clues)}.'
                outcome = f'דורגו {total} מועמדים והוחזרו {returned}: {format_ids(ids)}.{recommendation}{warning}'
            elif tool == "compare_location_claims":
                keywords = args.get("keywords") or result.get("keywords") or []
                seeds = args.get("seed_event_ids") or []
                action = f'השוואת דיווחים דומים בהקשרי מיקום לפי רמזים {format_ids(keywords)} ועוגנים {format_ids(seeds)}.'
                groups = result.get("conflict_groups") or []
                top = groups[0] if groups else {}
                top_ids = top.get("event_ids") or []
                outcome = (
                    f'נמצאו {result.get("conflict_group_count", 0)} קבוצות חשד מתוך '
                    f'{result.get("candidate_event_count", 0)} דיווחים; '
                    f'הקבוצה המובילה כוללת {top.get("event_count", 0)} אירועים, '
                    f'{top.get("location_count", 0)} מיקומים ו-{top.get("municipality_count", 0)} רשויות; '
                    f'מזהים לדוגמה: {format_ids(top_ids)}.'
                )
            elif tool == "challenge_hypothesis":
                evidence = args.get("supporting_event_ids") or []
                action = f'בדיקת חלופות ופערים להשערה על בסיס {len(evidence)} אירועים: {format_ids(evidence)}.'
                alternatives = result.get("alternative_event_ids") or []
                gaps = result.get("gaps") or []
                outcome = f'נמצאו {len(alternatives)} אירועי חלופה ו-{len(gaps)} פערים; חלופות: {format_ids(alternatives)}.'
            elif tool == "prepare_target_candidate":
                requested = args.get("event_ids") or []
                action = f'בדיקת {len(requested)} רשומות עוגן והשלמת חיזוקים למועמד מטרה: {format_ids(requested)}.'
                evidence = result.get("evidence") or []
                eligible = bool(result.get("persistence_eligible"))
                blocks = result.get("persistence_block_reasons") or []
                outcome = (
                    f'נבדקו {len(evidence)} רשומות ב-{result.get("independent_source_group_count", 0)} קבוצות מקור; '
                    f'ביטחון {result.get("confidence") or "לא נקבע"}; '
                    f'המועמד {"כשיר לשמירה" if eligible else "אינו כשיר לשמירה"}.'
                )
                if blocks:
                    outcome += f' סיבות: {"; ".join(str(item) for item in blocks[:3])}.'
                outcome += identifiers_text(result)
            elif tool == "find_duplicate_target_candidates":
                action = (
                    f'בדיקת מועמדים כפולים עבור סוג {args.get("object_class") or "לא צוין"}, '
                    f'מיקום {args.get("location_id") or "לא צוין"} וישות {args.get("entity_id") or "לא צוינה"}.'
                )
                matches = result.get("matches") or []
                outcome = f'{"נמצאו" if matches else "לא נמצאו"} {len(matches)} מועמדים דומים.' + identifiers_text(result)
            elif tool == "search_target_candidates":
                filters = {key: value for key, value in public_args(args).items() if value not in (None, "", [], False)}
                action = f'חיפוש מועמדי מטרות לפי {", ".join(filters) if filters else "ללא מסננים"}.'
                candidates = result.get("candidates") or []
                outcome = f'הוחזרו {result.get("returned", len(candidates))} מועמדי מטרות.' + identifiers_text(result)
            elif tool == "get_target_candidate":
                action = f'שליפת מועמד המטרה {args.get("target_id") or "לא צוין"}.'
                candidate = target_candidate(result)
                outcome = (
                    f'הוחזרה המטרה {candidate.get("title") or candidate.get("target_id") or "ללא כותרת"}; '
                    f'ביטחון {candidate.get("confidence") or "לא נקבע"}; '
                    f'{candidate.get("evidence_count", len(candidate.get("evidence") or []))} רשומות.'
                    + identifiers_text(result)
                )
            elif tool == "create_target_candidate":
                candidate_input = args.get("candidate") or {}
                action = f'יצירת מועמד המטרה {candidate_input.get("target_id") or "חדש"} לאחר בדיקות הכשירות.'
                candidate = target_candidate(result)
                outcome = (
                    f'נוצרה המטרה {candidate.get("title") or candidate.get("target_id") or "ללא כותרת"}; '
                    f'ביטחון {candidate.get("confidence") or "לא נקבע"}; '
                    f'{candidate.get("evidence_count", len(candidate.get("evidence") or []))} רשומות.'
                    + identifiers_text(result)
                )
            elif tool == "update_target_candidate":
                changed_fields = list((args.get("changes") or {}).keys())
                action = f'עדכון המטרה {args.get("target_id") or "לא צוינה"}; שדות: {", ".join(changed_fields) if changed_fields else "אין"}.'
                candidate = target_candidate(result)
                outcome = f'המטרה {candidate.get("title") or candidate.get("target_id") or "לא צוינה"} עודכנה.' + identifiers_text(result)
            elif tool == "attach_target_evidence":
                supplied = args.get("evidence") or []
                action = f'צירוף {len(supplied)} רשומות למטרה {args.get("target_id") or "לא צוינה"}.'
                candidate = target_candidate(result)
                if record.get("is_error") or result.get("error"):
                    outcome = f'הצירוף נכשל: {result.get("error") or "שגיאה לא מפורטת"}.' + identifiers_text(args, result)
                else:
                    outcome = f'הרשומות צורפו; למטרה משויכות כעת {candidate.get("evidence_count", len(candidate.get("evidence") or []))} רשומות.' + identifiers_text(result)
            elif tool == "present_requested_results":
                layers = result.get("requested_result_layers") or []
                evidence_layers = result.get("evidence_reference_layers") or []
                action = (
                    f'בחירת {len(args.get("layers") or [])} שכבות שעונות ישירות לבקשת המשתמש '
                    f'ו-{len(args.get("evidence_layers") or [])} שכבות ראיות תומכות.'
                )
                outcome = f'אומתו {len(layers)} שכבות תוצאה ו-{len(evidence_layers)} שכבות ראיות.'
            else:
                action = f'קלט: {json.dumps(public_args(args), ensure_ascii=False)}.'
                outcome = f'פלט: {json.dumps(result, ensure_ascii=False)}.'
            # Collect event_ids for per-step visualization
            step_event_ids = []
            if tool in {"search_events", "semantic_search_events", "find_actor_history", "trace_identifier", "trace_semantic_clues", "find_related_events"}:
                step_event_ids = result.get("event_ids") or []
            elif tool in {"resolve_event_reference"}:
                step_event_ids = result.get("event_ids") or []
            elif tool == "get_objects":
                step_event_ids = [item.get("event_id") for item in result.get("events") or [] if item.get("event_id")]
            elif tool == "build_event_sequence":
                for route_item in (result.get("route") or []):
                    step_event_ids.extend(route_item.get("event_ids") or [])
            elif tool == "compare_location_claims":
                for group in (result.get("conflict_groups") or []):
                    step_event_ids.extend(group.get("event_ids") or [])
            elif tool == "challenge_hypothesis":
                step_event_ids = (result.get("alternative_event_ids") or []) + (args.get("supporting_event_ids") or [])
            if not step_event_ids:
                step_event_ids = extract_event_ids(result)

            step_dict = {
                "tool": tool,
                "bridge_summary": bridge_summary,
                "observed_clue": observed_clue,
                "decision": decision,
                "expected_value": expected_value,
                "rationale": decision,
                "action": action,
                "result": outcome,
                "technical": {
                    "tool": tool,
                    "arguments": args,
                    "is_error": bool(record.get("is_error")),
                    "timestamp_utc": record.get("timestamp_utc"),
                },
            }
            if step_event_ids:
                step_dict["event_ids"] = list(dict.fromkeys(step_event_ids))  # deduplicate, preserve order

            map_locations = normalize_map_locations(tool, result)
            if map_locations:
                step_dict["map_locations"] = map_locations

            aggregate_groups = normalize_aggregate_groups(result)
            if aggregate_groups:
                step_dict["aggregate_groups"] = aggregate_groups

            location_layers = normalize_location_layers(result)
            if location_layers:
                step_dict["location_layers"] = location_layers

            entity_layers = normalize_entity_layers(result)
            if entity_layers:
                step_dict["entity_layers"] = entity_layers

            steps.append(step_dict)
            previous_result = result
        return steps

    @staticmethod
    def render_investigation_state(inv_state):
        """Render the structured investigation state as a Hebrew instruction block."""
        if not inv_state:
            return ""
        lines = ["--- מצב חקירה נוכחי (אל תחזור על עבודה שכבר בוצעה) ---"]
        turn = inv_state.get("turn", 0)
        lines.append(f"תור מספר: {turn}")

        confirmed = inv_state.get("confirmed_event_ids") or []
        if confirmed:
            ids_str = ", ".join(confirmed[:40])
            suffix = f" ועוד {len(confirmed) - 40}" if len(confirmed) > 40 else ""
            lines.append(f"אירועים שאושרו עד כה ({len(confirmed)}): {ids_str}{suffix}")

        actors = inv_state.get("confirmed_actors") or []
        if actors:
            lines.append(f"גורמים שזוהו: {', '.join(actors)}")

        entities = inv_state.get("entities_resolved") or {}
        if entities:
            entity_strs = [f"{eid}: {', '.join(aliases)}" for eid, aliases in entities.items()]
            lines.append(f"ישויות שפוענחו: {'; '.join(entity_strs)}")

        hypothesis = inv_state.get("current_hypothesis")
        if hypothesis:
            confidence = inv_state.get("confidence") or "לא הוגדרה"
            lines.append(f"השערה פעילה: {hypothesis}")
            lines.append(f"רמת ביטחון נוכחית: {confidence}")

        gaps = inv_state.get("gaps") or []
        if gaps:
            lines.append(f"פערים ידועים: {'; '.join(gaps)}")

        leads = inv_state.get("open_leads") or []
        if leads:
            lines.append(f"כיווני המשך פתוחים: {'; '.join(leads)}")

        workstream = inv_state.get("active_workstream")
        if isinstance(workstream, dict):
            lines.append("הקשר מעקב פעיל לשיתוף פעולה עם המשתמש:")
            lines.append(json.dumps(workstream, ensure_ascii=False))
            lines.append(
                "הקשר זה אינו הרשאה לכתיבה. הצעה חדשה מחייבת prepare_workstream_indication_proposal; "
                "הכרעה על הצעה ממתינה מחייבת decide_workstream_indication_proposal."
            )

        selected_layers = inv_state.get("selected_layers") or []
        if selected_layers:
            lines.append("שכבות שנבחרו בממשק לפני שליחת השאלה:")
            for layer in selected_layers[:8]:
                if not isinstance(layer, dict):
                    continue
                label = str(layer.get("label") or layer.get("id") or "שכבה ללא שם")
                kind = str(layer.get("kind") or "unknown")
                catalog_id = str(layer.get("catalog_layer_id") or "")
                filtered_count = layer.get("filtered_count")
                original_count = layer.get("original_count")
                count_text = ""
                if isinstance(filtered_count, int) and isinstance(original_count, int):
                    count_text = f"{filtered_count}/{original_count}" if filtered_count != original_count else str(original_count)
                source_type = str(layer.get("source_type") or "").strip()
                filters = layer.get("applied_filters") or []
                filter_parts = []
                if isinstance(filters, list):
                    for item in filters[:8]:
                        if not isinstance(item, dict):
                            continue
                        field = str(item.get("field") or "").strip()
                        value = str(item.get("value") or "").strip()
                        if field and value:
                            filter_parts.append(f"{field} contains {value}")
                sample_ids = layer.get("sample_ids") or []
                ids_text = ", ".join(str(item) for item in sample_ids[:80] if item)
                parts = [f"- {label}", f"kind={kind}"]
                if catalog_id:
                    parts.append(f"catalog_layer_id={catalog_id}")
                if source_type:
                    parts.append(f"source_type={source_type}")
                if count_text:
                    parts.append(f"count={count_text}")
                if filter_parts:
                    parts.append(f"filters={'; '.join(filter_parts)}")
                if ids_text:
                    parts.append(f"sample_ids={ids_text}")
                    if isinstance(filtered_count, int) and filtered_count > len(sample_ids):
                        parts.append("sample_ids_are_partial=true")
                lines.append(" | ".join(parts))
            lines.append("כאשר שאלת האנליסט מתייחסת לשכבות, לתוצאות שנבחרו, או להקשר הנוכחי בממשק, השתמש בשכבות האלה כמסגרת צמצום ולא כנתון רק לתצוגה.")

        saved_memory = inv_state.get("saved_memory") or {}
        if isinstance(saved_memory, dict):
            chat_summaries = saved_memory.get("chat_summaries") or []
            if chat_summaries:
                lines.append("זיכרון חקירה שנשמר ידנית על ידי האנליסט - ממצאי שיחה:")
                for item in chat_summaries[:8]:
                    if not isinstance(item, dict):
                        continue
                    prompt = str(item.get("prompt") or "").strip()
                    summary = str(item.get("answer_summary") or item.get("answer_preview") or "").strip()
                    evidence_ids = item.get("evidence_ids") or []
                    ids_text = ", ".join(str(eid) for eid in evidence_ids[:60] if eid)
                    parts = ["- ממצא שמור"]
                    if prompt:
                        parts.append(f"שאלה={prompt[:500]}")
                    if summary:
                        parts.append(f"סיכום={summary[:800]}")
                    if ids_text:
                        parts.append(f"evidence_ids={ids_text}")
                    lines.append(" | ".join(parts))

            memory_layers = saved_memory.get("layers") or []
            if memory_layers:
                lines.append("זיכרון חקירה שנשמר ידנית על ידי האנליסט - שכבות ומסננים:")
                for layer in memory_layers[:12]:
                    if not isinstance(layer, dict):
                        continue
                    label = str(layer.get("label") or layer.get("layer_id") or "שכבה שמורה")
                    kind = str(layer.get("layer_kind") or layer.get("kind") or "unknown")
                    catalog_id = str(layer.get("catalog_layer_id") or "")
                    source_type = str(layer.get("source_type") or "").strip()
                    filtered_count = layer.get("filtered_count")
                    original_count = layer.get("original_count")
                    count_text = ""
                    if isinstance(filtered_count, int) and isinstance(original_count, int):
                        count_text = f"{filtered_count}/{original_count}" if filtered_count != original_count else str(original_count)
                    filters = layer.get("applied_filters") or []
                    filter_parts = []
                    if isinstance(filters, list):
                        for item in filters[:8]:
                            if not isinstance(item, dict):
                                continue
                            field = str(item.get("field") or "").strip()
                            value = str(item.get("value") or "").strip()
                            if field and value:
                                filter_parts.append(f"{field} contains {value}")
                    sample_ids = layer.get("sample_ids") or []
                    ids_text = ", ".join(str(item) for item in sample_ids[:80] if item)
                    restore_status = str(layer.get("restore_status") or "").strip()
                    parts = [f"- {label}", f"kind={kind}"]
                    if catalog_id:
                        parts.append(f"catalog_layer_id={catalog_id}")
                    if source_type:
                        parts.append(f"source_type={source_type}")
                    if count_text:
                        parts.append(f"count={count_text}")
                    if filter_parts:
                        parts.append(f"filters={'; '.join(filter_parts)}")
                    if ids_text:
                        parts.append(f"sample_ids={ids_text}")
                        if isinstance(filtered_count, int) and filtered_count > len(sample_ids):
                            parts.append("sample_ids_are_partial=true")
                    if restore_status:
                        parts.append(f"restore_status={restore_status}")
                    lines.append(" | ".join(parts))
                lines.append("זיכרון זה נשמר ידנית; כאשר השאלה מתייחסת לחקירה הקודמת, המשך ממנו במקום להתחיל מאפס.")

        lines.append("--- המשך החקירה משאלת האנליסט הנוכחית ---")
        return "\n".join(lines)

    def read_live_steps(self):
        audit_path = self.config.get("audit_path") or REMOTE_AUDIT_PATH
        started_at = ACTIVE_RUN_STARTED_AT_BY_AUDIT.get(audit_path)
        if started_at is None:
            return []
        audit_text = self.ssh_command(f"cat {audit_path} 2>/dev/null || true", timeout=20)
        audit_records = []
        for line in audit_text.splitlines():
            try:
                record = json.loads(line)
                timestamp = record.get("timestamp_utc")
                if timestamp:
                    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    if parsed < started_at:
                        continue
                audit_records.append(record)
            except json.JSONDecodeError:
                continue
        return self.summarize_audit(audit_records)

    def investigate(self, prompt, history, investigation_state=None, investigation_id=None, is_continuation=False, continuation_context=None, responding_agent="general", mission_run_id=None):
        global ACTIVE_RUN_STARTED_AT
        overall_started = time.perf_counter()
        performance = {
            "gateway": {},
            "hermes": {"poll_count": 0, "status_request_total_ms": 0},
            "tools": {},
        }
        audit_path = self.config.get("audit_path") or REMOTE_AUDIT_PATH
        original_classification = {}
        if isinstance(continuation_context, dict):
            original_classification = continuation_context.get("original_classification") or {}
        original_classification_summary = ""
        if isinstance(original_classification, dict):
            original_classification_summary = str(original_classification.get("summary") or "").strip()
        if is_continuation:
            preserved_context = (
                f" מסגרת הסיווג המקורית לשימור: {original_classification_summary}"
                if original_classification_summary else ""
            )
            classify_instruction = (
                "זהו המשך של חקירה פעילה — אל תפעיל classify_question_intent ואל תתחיל חקירה חדשה."
                " הקשר המלא של החקירה נמצא בהיסטוריית השיחה שסופקה, כולל תוצאת classify_question_intent"
                " המקורית שקבעה את recommended_mode ו-tool_budget. המשך לפעול לפי אותם mode ו-budget"
                " שנקבעו בסיווג המקורי. המשך ישירות מהנקודה שבה הסתיימה החקירה הקודמת בהתבסס על"
                " ההוראה החדשה שסופקה ב-prompt."
                f"{preserved_context}\n"
            )
        else:
            classify_instruction = (
                "בכל שאלה חדשה, הפעל תחילה את classify_question_intent עם נוסח שאלת האנליסט והקשר קצר אם דרוש."
                " הכלי משתמש ב-MCP sampling כדי לסווג את הכוונה בעזרת מודל, ומחזיר מסגרת עבודה מנורמלת."
                " אל תשלח לכלי שדות סיווג ידניים כמו model_intent; תן לכלי לבצע את הסיווג."
                " התייחס לפלט הכלי כמסגרת העבודה: recommended_mode, tool_budget, allowed_tool_families, blocked_tool_families ו-recommended_view_hint.\n"
            )
        instructions = (
            "אתה סוכן חקירה למערכת מודיעינית ניסיונית על תרחיש הסלמה בצפון קוסובו/סרביה. השב בעברית בלבד.\n"
            "נקודת המבט היא של אנליסט מודיעין בצבא סרביה. המאגר מבוסס בעיקר על מקורות גלויים ועל תצפיות וידאו מכטב״ם סרביות סינתטיות כלפי כוחות היריב והסביבה. "
            "הכיסוי חלקי ומוטה לאיסוף על היריב; היעדר דיווח על כוח סרבי אינו ראיה להיעדר פעילות סרבית. "
            "הפרד תמיד בין תצפית, זיהוי והסקה, והתייחס לספירת עצמים בווידאו כהערכה הדורשת הצלבה.\n"
            f"השתמש אך ורק בכלי MCP ששמם מתחיל ב-{HERMES_TOOL_PREFIX} ובנתונים שהם מחזירים.\n"
            + classify_instruction +
            "עקרון כיסוי מחייב: ברירת המחדל בכל שאלת מודיעין היא Coverage / exhaustive mode."
            " אל תסתפק בדוגמאות מייצגות כאשר הכלים יכולים להחזיר את כלל התוצאות בתחום המוגדר."
            " השתמש באגרגציה כדי להבין את מרחב התוצאות, ואז בשליפה רחבה עם limit=2000 או במסננים מצמצמים כדי להביא את כל הרשומות הרלוונטיות האפשריות."
            " אם כלי מחזיר truncated=true או total/total_candidates גדול מ-returned, אסור להציג זאת כתוצאה מלאה; חובה להמשיך לצמצם או לציין במפורש כמה הוחזר וכמה נשאר מחוץ לכיסוי."
            " גם כאשר התשובה המילולית קצרה, שמור על כיסוי ראייתי מלא בפלט הכלים: אל תבחר רק 3-5 דוגמאות אם קיימות רשומות רלוונטיות נוספות."
            " עם זאת, מזהי הראיות שמופיעים בסוף התשובה הם החוזה המחייב מול הממשק: רק מזהים שהחלטת שהם תומכים בתשובה צריכים להופיע שם.\n"
            "בכל קריאת כלי, כולל classify_question_intent, כלול בפרמטרים step_bridge."
            " step_bridge חייב להיות משפט אחד או שניים בעברית שמסבירים את עבודת הסוכן בין תוצאת הכלי הקודם לבין בחירת הצעד הנוכחי:"
            " מה זוהה או הובן מהמידע שחזר, איזה פרט בתוצאה גרם לזיהוי הזה, מה הצעד הבא שנבחר, ומדוע הצעד הזה מתאים."
            " בצעד הראשון, כאשר אין עדיין תוצאת כלי קודמת, כתוב שזה צעד פתיחה לסיווג שאלת האנליסט ובחירת מסלול עבודה."
            " אל תחשוף מחשבות פנימיות או chain-of-thought; כתוב רציונל אנליטי קצר שניתן להציג לאנליסט.\n"
            "אם recommended_mode הוא retrieval: הישאר בתוך tool_budget ככל האפשר, השתמש רק במשפחות הכלים המותרות,"
            " ואל תפעיל challenge_hypothesis, find_related_events או explain_linkage אלא אם המשתמש ביקש במפורש קשר נסתר, דפוס, חשד, הסבר או חלופות.\n"
            "אם recommended_mode הוא investigation: בצע חקירה, אך נסה להישאר בתוך tool_budget. עבור חקירות שרשרת, מזהה ספציפי, גבול או רכיב מרכזי, tool_budget עשוי להיות 30 והוא נועד לאפשר השלמת בדיקה אמיתית."
            " אל תעצור אחרי מציאת שתי רשומות ישירות בלבד; המשך להרחבה, צמצום, בדיקת גשרים, ובניית רצף עד שיש בסיס למסקנה או עד שמוצגים פערים מפורשים.\n"
            "בחקירה על מזהה רשומה, מיקום או טענה ספציפית לכיוון תרחיש הסלמה, בצע סדר עבודה מחייב:"
            " 1) trace_identifier למזהה עצמו אם יש מזהה רשומה גלוי מסוג REC; עבור מיקום LOC השתמש ב-resolve_location או search_events; אחרת resolve_event_reference או search_events לפי הטענה;"
            " 2) אם נמצאו רשומות ישירות, find_related_events מהן עם limit=2000 לפני כל challenge_hypothesis;"
            " 3) אחרי כלי שמחזיר recommended_next_seeds או new_clues_to_trace, הפעל plan_next_investigation_step לפני בחירת צעד אחר;"
            " 4) אם המזהה הישיר מפסיק להופיע, הפעל trace_semantic_clues על מונחי טענה, מיקום, שחקן, חסימה, ירי, KFOR, מדיה, שמועה, דיסאינפורמציה או ניסוח תקשורתי שעלו ברשומות;"
            " 5) אם יש הרבה מועמדים, צמצם לפי source_types, זמן, מיקום או ממד קשר והרחב שוב;"
            " 6) בדוק גשרים עם explain_linkage בין מועמדי שרשרת מרכזיים;"
            " 7) בנה רצף עם build_event_sequence;"
            " 8) רק לאחר מכן בדוק חלופות עם challenge_hypothesis."
            " אם המזהה לא מופיע ישירות ביעד, זה פער ולא סיום חקירה; המשך לבדוק המשך תפעולי דרך ישות, זמן, מיקום, תנועה/חסימה, תצפית, תקשורת או ניסוח סמנטי.\n"
            "פרוטוקול הרחבת שרשרת מוגבל: בחקירת שרשרת, אל תבדוק קשר ישיר בין העוגן הראשוני לעוגן הסופי כמבחן מסכם לפני שבנית חוליות ביניים."
            " נהל רשימת frontier של אירועים מבטיחים: לאחר trace_identifier, trace_semantic_clues, search_events או find_related_events,"
            " בחר לכל היותר 3 אירועים חדשים בעלי ערך חקירתי גבוה שאינם כבר בשרשרת, והפוך אותם ל-seeds להרחבה נוספת."
            " ערך חקירתי גבוה כולל: מזהה גלוי, רמז סמנטי, מיקום, שחקן, מקור רשמי, מקור חברתי, מדיה לא מאומתת, שמועה, הכחשה, חסימה, ירי, KFOR, תנועה או קרבה ברורה לעוגן היעד."
            " הרחב עד עומק 3 לכל היותר מהעוגן המקורי, ועד 9 seeds חדשים לכל היותר בכל החקירה."
            " אל תבצע יותר מ-2 קריאות trace_semantic_clues, יותר מ-4 קריאות find_related_events, או יותר מ-6 בדיקות explain_linkage באותה חקירה, אלא אם המשתמש ביקש במפורש להמשיך."
            " בכל סבב הרחבה, העדף הרחבה ממועמד שנמצא כבר כגשר ביניים ולא מחיפוש רחב מקוצץ."
            " אם trace_semantic_clues מחזיר אירועים כמו מקור רשמי, רשת חברתית, מדיה, שמועה, טענה לא מאומתת, חסימה, ירי, תנועה, KFOR או דיווח מקומי,"
            " חובה לבצע לפחות סבב הרחבה אחד מאחד מהם לפני בדיקת challenge_hypothesis או לפני מסקנה שהקשר חלש."
            " אם trace_semantic_clues מחזיר recommended_next_seeds, השתמש בהם כ-frontier המחייב הבא: הרחב עד 3 seeds בלבד, לפי הסדר שהכלי החזיר."
            " אם הוא מחזיר new_clues_to_trace, השתמש בהם בקריאת trace_semantic_clues הבאה, אלא אם כבר הגעת למגבלת 2 קריאות סמנטיות."
            " אל תבחר seeds אחרים מתוך תוצאה רחבה לפני שניסית את recommended_next_seeds או הסברת מדוע הם לא רלוונטיים."
            " אותו כלל חל גם על find_related_events: אם הוא מחזיר recommended_next_seeds, השתמש בהם כ-frontier המחייב הבא לפני מעבר ל-challenge_hypothesis או לסיכום."
            " אל תבנה רצף סופי רק מהעוגנים המקוריים אם find_related_events החזיר seeds מומלצים מסוג מקור רשמי, רשת חברתית, מדיה, שמועה, חסימה, ירי, KFOR, תנועה או מיקום שלא הורחבו."
            " כלל מחייב: כאשר כלי מחזיר recommended_next_seeds, הקריאה הבאה שאינה explain_linkage חייבת להיות get_objects עם object_type=event או find_related_events על אותם event_id בדיוק, עד 3 seeds, לפי הסדר שהוחזר."
            " אל תחליף אותם בזרעים אחרים מתוך הרשימה הרחבה, אל תבחר חלופות, ואל תפעיל challenge_hypothesis לפני שבוצעה לפחות קריאת הרחבה אחת על seed מומלץ אחד או יותר."
            " אם seed מומלץ נראה לא רלוונטי, חובה לציין זאת ב-step_bridge ולשלוף אותו עם get_objects object_type=event לפני דחייה."
            " כאשר seeds מומלצים כוללים חוליית ביניים כמו מקור רשמי, מקור חברתי, מדיה, מיקום, חסימה, ירי, KFOR או תנועה, כלול אותם ברצף המועמד עד שבדיקת explain_linkage מראה שאין גשר מספיק."
            " השתמש ב-plan_next_investigation_step כנקודת ביקורת תהליכית: שלח לו objective, candidate_chain_event_ids, pending_recommended_seeds, expanded_seed_event_ids, new_clues_to_trace, linkage_checks_done, semantic_calls_used, related_calls_used ו-tool_budget_remaining."
            " אם הוא מחזיר blocked_tool_families הכוללים challenge_hypothesis או final_summary, אסור להפעיל אותם עד שבוצעה הפעולה שהוא דרש."
            " אם הוא מחזיר required_event_ids, הצעד הבא חייב להשתמש במזהים האלה בדיוק, אלא אם step_bridge מסביר מדוע הם נדחו לאחר get_objects object_type=event."
            " בדוק גשרים עם explain_linkage בין חוליות סמוכות בשרשרת המועמדת, לא רק בין התחלה לסוף."
            " הפעל challenge_hypothesis רק לאחר שנמצא רצף מועמד של לפחות 5 אירועים, או לאחר שני סבבי הרחבה שלא מצאו שום חוליה חדשה."
            " אם הגעת למגבלות העומק או הקריאות, עצור והצג אילו חוליות נמצאו ואילו seeds לא הורחבו.\n"
            "בחקירה עמוקה או בשליפה מודיעינית, אל תשתמש ב-limit קטן כמו 20, 50, 80, 120 או 500 לחיפוש רחב לפי מיקום בלבד, אזור כללי, שחקן רחב, רמז סמנטי או הרחבת קשרים."
            " אם החיפוש נועד לבחור עוגני שרשרת מתוך מרחב גדול, השתמש קודם ב-aggregate_events או במסננים מצמצמים כגון זמן, סוג מקור, מילות מפתח, ישות או מזהה."
            " אם בכל זאת נדרש חיפוש רחב, השתמש ב-limit=2000 והבהר ב-step_bridge שזה עדיין לא כיסוי מלא אם התוצאה מקוצצת."
            " השתמש ב-limit קטן רק כאשר הצעד הוא אימות ממוקד של מזהים/רשומות שכבר נבחרו, לא לצורך חיפוש או שלילה."
            " כאשר כלי מחזיר truncated=true או total גדול מ-returned, אל תבחר עוגן חקירתי כאילו נבדקו כל הרשומות; בצע צמצום נוסף, אגרגציה, או חיפוש ממוקד לפני בחירת seeds."
            " אל תציג שרשרת כמבוססת אם העוגנים נבחרו רק מתוך תוצאה מקוצצת ללא הצדקה.\n"
            "השתמש ב-semantic_search_events כאשר השאלה, הטענה או הרמזים מתארים משמעות כללית, פרפרזה, ניסוח תקשורתי, שמועה או תיאור שאולי לא מופיע במילים המדויקות ברשומות."
            " אל תשתמש בו במקום trace_identifier למזהה גלוי, במקום search_events למסננים מפורשים, במקום aggregate_events לספירות, או במקום get_objects לשליפת אובייקטים ידועים."
            " התייחס לתוצאת semantic_search_events כמועמדי ראיות בלבד: לאחר מכן אמת מועמדים מרכזיים בעזרת get_objects, find_related_events, explain_linkage או build_event_sequence לפי הצורך."
            " כאשר קיימים entity_id או location_id ידועים, העבר אותם כמסננים ל-semantic_search_events כדי לצמצם רעש.\n"
            "ב-find_related_events בחקירה עמוקה, אל תשתמש ב-limit=20, limit=150 או limit=500 להרחבה רחבה. השתמש בדרך כלל ב-limit=2000, או צמצם מראש לפי source_types, חלון זמן, מיקום או ממדי קשר."
            " אם total_candidates גדול בהרבה מ-returned, התייחס לתוצאה כמדגם מדורג ולא כבדיקה מלאה; המשך בסינון או בהרחבה נוספת.\n"
            "אם המשתמש מבקש להציג, לשלוף, לסנן, לצמצם, למנות או להראות אירועים/רשומות/תוצאות,"
            " התייחס לכך כבקשת שליפה וסינון. במצב זה החזר את התוצאות הרלוונטיות וסיכום קצר של דרך הסינון,"
            " בלי לבנות תרחיש, בלי לחפש קשרים נסתרים, בלי להציג שרשרת או דפוס, ובלי להפעיל challenge_hypothesis,"
            " אלא אם המשתמש ביקש במפורש דפוס, קשרים, הסבר, חשד, חלופות, מקור התרחיש או רכיב מרכזי.\n"
            "בבקשת שליפה וסינון, השתמש בכלים הדרושים לזיהוי מיקום, חיפוש ושליפת רשומות בלבד,"
            " והעדף תצוגת evidence כאשר מטרת המשתמש היא לראות את האירועים עצמם.\n"
            "כאשר השאלה גאוגרפית או מבקשת מקבצים, ריכוזים, TOP מיקומים, אזורים, מוקדים או 'איפה',"
            " התייחס לכך כתוצאה מרחבית. השתמש ב-aggregate_events עם group_by=location כאשר מתאים,"
            " והשתמש ב-aggregate_events עם group_by=municipality כאשר נדרשת תמונת אזור רחבה."
            " כאשר התשובה צריכה להציג מיקומים מלאים, השתמש ב-get_objects עם object_type=location או all כדי להחזיר location_layers להצגה."
            " החזר גם רמת אזור/רשות וגם מוקדים מדויקים כאשר המשתמש מבקש מוקדים עיקריים."
            " החזר לכל מיקום את location_id, שם המיקום ומספר האירועים, ולכל רשות את שם הרשות והספירה."
            " בחר תצוגה מומלצת map גם אם אין מזהי אירועים בודדים, והסבר שזו תוצאה אגרגטיבית לפי מיקום."
            " אל תציג היעדר מזהי אירועים ככשל כאשר המשתמש ביקש ריכוזים או מיקומים.\n"
            "כאשר המשתמש מבקש לסדר מוקדים, אזורים או רשויות על ציר זמן לפי האירוע הראשון או האחרון בכל מוקד,"
            " השתמש ב-aggregate_events עם include_first_last=true ו-sort_by=first_event_time או last_event_time לפי השאלה,"
            " במקום להריץ חיפוש limit=1 נפרד לכל מוקד. השתמש ב-search_events עם sort_by=timestamp רק כאשר נדרש ציר זמן של רשומות גולמיות.\n"
            "כאשר השאלה עוסקת בגורמים, שחקנים, ארגונים או כוחות, השתמש ב-resolve_entity או aggregate_events group_by=entity כדי לעבוד עם entity_id קנוני."
            " כאשר צריך להציג או לאמת גורמים כ-layer, השתמש ב-get_objects עם object_type=entity או all כדי להחזיר entity_layers."
            " search_events ו-find_actor_history יכולים לקבל entity_ids כאשר השאלה כבר הובנה ברמת ישות ולא רק ברמת actor טקסטואלי.\n"
            "כאשר המשתמש שואל על מיקום שגוי, הטעיה גאוגרפית, סרטון ישן, תמונה/שיירה שמיוחסת למקום, או טענה שמופצת בכמה מקומות,"
            " השתמש ב-compare_location_claims לפני מסקנה. הכלי מזהה רק סימני סתירה גלויים בין דיווחים דומים,"
            " ואינו יודע מה המיקום הנכון; לכן הצג את התוצאה כחשד לפיזור/הטעיה גאוגרפית ולא כהוכחת אמת קרקע."
            " התחשב ב-certainty_level וב-source_reliability_label שחוזרים מהכלים כאשר אתה מדרג את חוזק החשד.\n"
            "כאשר שאלת המשתמש קצרה אך אנליטית, אל תדרוש מהמשתמש לפרט את תתי-הבדיקות."
            " פרק בעצמך את השאלה לפי מטרתה: מוקדי חיכוך מחייבים גם אגרגציה מרחבית רחבה וגם מוקדים מדויקים;"
            " תנועה או נוכחות מחייבות חתך זמן, חתך מקום, שחקנים ודוגמאות ראיה;"
            " שאלות על גורם מייצב, חיץ או מגביל פעולה מחייבות הבחנה בין נוכחות, תנועה, חסימה, תיאום, וזיהוי שגוי;"
            " שאלות על ירי, פיצוץ או אירוע אלים מחייבות בדיקת אמינות, ודאות, חיזוקים, הכחשות והסברים אזרחיים חלופיים;"
            " ושאלה מסכמת על אירוע נקודתי מול דפוס רחב מחייבת לחבר את ממצאי המפה, הזמן, השחקנים ואיכות המידע."
            " הכללים האלה הם כלליים ואינם מניחים מראש שחקן, מקום או תרחיש מסוים.\n"
            "כאשר המשתמש מבקש להבחין בין אירוע אלים אמיתי לבין רעש מידע, אל תסתפק בחיפוש טקסט יחיד."
            " בצע לפחות: חיפוש אירועי האלימות הרלוונטיים; אגרגציה לפי זמן ומיקום; בדיקת source_reliability_label ו-certainty_level;"
            " חיפוש חיזוקים כגון נפגעים, פינוי, חסימות או נוכחות כוחות; חיפוש חלופות כמו תקלה, תאונה, אירוע אזרחי, שמועה, מדיה ישנה או דיווח מוגזם;"
            " ואם יש טענות מדיה או טענות חוזרות במקומות שונים, השתמש ב-compare_location_claims לפני מסקנה."
            " השתמש ב-challenge_hypothesis כאשר יש מספיק ראיות או חלופות כדי לבדוק האם מדובר באירוע ממשי או ברעש מידע.\n"
            "אם המשתמש מבקש לחקור דפוס, קשר נסתר, גורמים משותפים, אירועים מקדימים, הסברים חלופיים,"
            " תחילת תרחיש או רכיב מרכזי, התייחס לכך כבקשת חקירה והפעל את תהליך ההרחבה, ההצלבה והביקורת המלא.\n"
            "אל תניח שמזהה מקום או תיאור יחסי ברורים: פתור קודם מיקומים והפניות לאירועים בעזרת הכלים המתאימים.\n"
            "בצע הצלבה בין זמן, מקום, גורם וסוג מקור. הפרד בין עובדות, הסקה וחוסר ודאות.\n"
            "כאשר שם גורם עשוי להיות כינוי או שם מקוצר, השתמש ב-resolve_entity לפני חיפוש היסטוריה."
            " find_actor_history מרחיב אוטומטית את כל הכינויים של ישות מוכרת; בדוק בפלט אילו שמות הורחבו.\n"
            "כאשר מופיע ערך מובחן שעשוי לשמש מזהה חוזר, השתמש ב-trace_identifier כדי לבדוק אם הוא מופיע במקורות נוספים."
            " אל תניח מראש את סוג המזהה או את משמעותו.\n"
            "כאשר trace_identifier משמש לבדיקת אזור, חלון זמן או משפחת מקורות מסוימת, השתמש במסנני start_time, end_time, location_ids ו-source_types"
            " כדי למנוע ערבוב אזכורים רחוקים או לא רלוונטיים.\n"
            "ב-trace_identifier, השאר include_negated=false בכל מעקב רגיל אחר מזהה ובכל ניסיון לבנות את השרשרת הראשית."
            " השתמש ב-include_negated=true רק בבדיקת סתירות, שלילות או חלופות, ורק כאשר אתה מציין שזו מטרת הבדיקה."
            " אל תערבב תוצאות שוללות עם ראיות השרשרת המרכזית.\n"
            "כאשר נמצאה ראיית עוגן משמעותית, השתמש ב-find_related_events להרחבה איטרטיבית."
            " העדף מועמדים עם כמה ממדי קשר והמשך להרחיב מהם עד שהקשרים נחלשים או שאין תוספת מהותית.\n"
            "כאשר אתה בודק משפחת ראיות מסוימת סביב עוגנים שכבר נמצאו, השתמש ב-source_types של find_related_events"
            " כדי לצמצם את ההרחבה לערוצי מקור שקיימים במאגר, למשל טלגרם, טיקטוק, X, פייסבוק, חדשות מקומיות, הודעת דובר, קבוצת וואטסאפ, שמועה מקומית, בלוג פוליטי או ערוץ חדשות בינלאומי."
            " אל תשתמש במסנן זה אם מטרת הצעד היא גילוי רחב; השתמש בו כאשר השאלה או פערי השלמות מצביעים על מקור ראייתי חסר.\n"
            "אל תפעיל challenge_hypothesis מוקדם מדי. בחקירת שרשרת או מזהה, אל תפעיל אותו לפני שבוצע find_related_events אחד לפחות על רשומות העוגן ונבדק לפחות גשר אחד עם explain_linkage, אלא אם היו לפחות שני חיפושים ממוקדים שנכשלו."
            " השתמש בו רק אחרי שנבנתה שרשרת מועמדת עם לפחות 3 עד 5 אירועים תומכים, או אחרי חיפוש מפורש שנכשל ומטרתו לבדוק חלופות."
            " אל תאתגר השערה על בסיס אירוע אחד או שתי רשומות מאותו ערוץ מקור בלבד אם עדיין לא נבדק המשך תפעולי. הכלי אינו קובע אם ההשערה נכונה.\n"
            "אל תסתפק בתשובה מקומית אם השאלה מבקשת דפוס, קשר נסתר, מקור מוקדם או הסבר. חפש לאחור וקדימה סביב ראיות העוגן.\n"
            "כאשר המשתמש מבקש את תחילת התרחיש, הבחן בין האירוע המוקדם ביותר שכבר נמצא לבין המקור הסיבתי או התפעולי של הרצף."
            " אל תכריז על התחלה לפני שהרחבת לאחור מכל חוליית ביניים משמעותית שנמצאה, לרבות פעולות, קשרים, העברות, נקודות מעבר או שינויים במצב.\n"
            "כאשר המשתמש מבקש לזהות את הטענה, הישות או הרכיב המרכזי בתרחיש, אל תבחר את המועמד המפורש הראשון בתוצאות."
            " דרוש חיבור רב-שלבי בינו לבין רצף הפעילות באמצעות מזהה גלוי, ישות, זמן, מקום, סוג מקור או קשר נרטיבי; ציין אם החיבור ישיר או נסיבתי.\n"
            "כאשר רשומה מכילה תוכן סמנטי כגון חפץ, כינוי, מסלול, פעולה או תנאי תזמון,"
            " השתמש ב-trace_semantic_clues עם המונחים שבה כדי לחפש אחורה וקדימה ולעקוב אחר מזהים, ישויות או נקודות תפעוליות שנרמזו בה."
            " השתמש בכלי הזה במיוחד כאשר המעבר בשרשרת אינו מבוסס על מזהה פורמלי אלא על שפת טענה כמו חסימה, ירי, חציית גבול, KFOR, סרטון, שמועה, הכחשה, תזמון או כינוי.\n"
            "אם קיימת תנועה חוקית או שגרתית באותו חלון זמן, אל תניח שהיא התרחיש המרכזי."
            " בדוק האם היא מחוברת לשרשרת או משמשת חלופה, רקע, הסחה או נקודת תזמון שהפעילות האחרת מתרחשת לפניה או אחריה.\n"
            "לפני תשובה על מקור התרחיש או הרכיב המרכזי בו, נסה לבנות שרשרת סיבתית ותפעולית מלאה ככל האפשר:"
            " תנאי מקדים, הכנה, קשר או העברה, שינוי מצב, תנועה או פעולה, ותוצאה."
            " אם חסרה חוליה, הצג אותה כפער והמשך לחפש במקום להשלים אותה בהשערה.\n"
            "לפני הצגת תרחיש רב-מקורי, בצע בדיקת שלמות של סוגי הראיות שעשויים להיות רלוונטיים לשאלה:"
            " תנועה ותצפית, תקשורת ותוכן סמנטי, קשרי ישויות וכינויים, העברות או פעולות מנהליות, ומזהים חוזרים."
            " אין חובה למצוא ראיה מכל סוג, אך חובה לבדוק סוגים סבירים ולציין במפורש אילו נבדקו, אילו נמצאו ואילו חסרים.\n"
            "אל תסתפק בקרבת זמן ומקום כאשר קיימת רשומה בעלת תוכן סמנטי שעשוי להסביר את הרצף."
            " חלץ ממנה מונחים, פעולות, מסלולים ותנאי תזמון, חפש אותם במקורות נוספים, והרחב גם מהאירוע הסמנטי עצמו.\n"
            "לכל מעבר בין שני שלבים בשרשרת, קבע את סוג הגשר הראייתי: מזהה משותף, ישות או כינוי, תוכן סמנטי,"
            " רציפות זמן-מקום, או קשר תפעולי מפורש. אם אין גשר כזה, אל תציג את המעבר כעובדה; סמן אותו כהשערה או כפער.\n"
            "כאשר אתה עומד להציג מעבר חשוב בין שני אירועים בשרשרת, השתמש ב-explain_linkage כדי לבדוק את הגשר הראייתי."
            " אם הכלי מחזיר שאין גשר מספיק, אל תציג את המעבר כעובדה גם אם הוא נראה סביר כרונולוגית.\n"
            "הפרד בין חברי השרשרת לבין אירועי חלופה, רקע או תזמון. אירוע חוקי, שגרתי או מאומת אינו הופך לחלק מהשרשרת"
            " רק משום שהוא סמוך בזמן או במקום; בדוק אם הוא מחובר בגשר ראייתי או דווקא מסביר, סותר או מתזמן את הפעילות האחרת.\n"
            "לאחר זיהוי מועמד לרכיב מרכזי, אל תעצור מיד. בצע סבב הרחבה נוסף משני צדי המועמד ומנקודות המעבר הסמוכות לו,"
            " ובדוק אם קיימות ראיות תקשורתיות, קשרי גורמים, פעולות קודמות או תצפיות מאוחרות שמחזקות או מחלישות את הזיהוי.\n"
            "כל טענה עובדתית מרכזית חייבת לכלול מזהי רשומות או מיקומים גלויים בסוגריים, לדוגמה (REC-025790) או (LOC-001).\n"
            "מבנה תשובת הצ'אט לאנליסט תלוי בפלט classify_question_intent.\n"
            "אם recommended_mode הוא retrieval: כתוב תשובת תוצאה קצרה מאוד, 1 עד 3 משפטים בלבד."
            " ענה ישירות על מה שהתבקש, ציין ספירות, מיקומים או סינון שבוצע, ואל תוסיף ניתוח חקירתי, השערות, חלופות, גשר ראייתי או דפוס נסתר."
            " אם מדובר באגרגציה לפי מיקום, ציין location_id, שם מיקום וספירה. אם מדובר ברשומות, ציין את מספר הרשומות שהוחזרו ואת מצב הכיסוי."
            " אל תכתוב מהלך חקירה, אל תפרט כלים ופרמטרים, ואל תשתמש במבנה עובדה/הסקה/חוסר ודאות.\n"
            "אם recommended_mode הוא investigation: כתוב תשובה קצרה אך חקירתית, 3 עד 6 משפטים."
            " סכם מה נבדק, מה נמצא, מהו הגשר הראייתי או הפער המרכזי, ומה נשאר לא ודאי."
            " אם יש רצף או דפוס, תאר אותו במשפט אחד או שניים בלבד."
            " אל תפרט את כל הצעדים הטכניים, הכלים והפרמטרים; יומן הפעילות בממשק מציג אותם בנפרד.\n"
            "אל תכתוב שורת טקסט חופשי שמתחילה 'מזהי ראיות:'. הממשק בונה את אזור מזהי הראיות רק מהשדה evidence_layers"
            " בקריאה הסופית ל-present_requested_results. מזהים קנוניים יכולים להישאר בגוף התשובה כאשר הם נחוצים להבנת טענה מסוימת.\n"
            "אם באחד מצעדי החקירה התקבלה תוצאה מקוצצת או מדגם מדורג, אל תנסח היעדר ראיה כמסקנה מוחלטת."
            " כתוב במפורש שהבדיקה אינה ממצה ושנדרש צמצום נוסף או הרחבת limit כדי לשלול המשך שרשרת בביטחון גבוה.\n"
            "הוסף שורה אחרונה בפורמט המדויק 'תצוגה מומלצת: VIEW | REASON'.\n"
            "VIEW חייב להתבסס קודם על recommended_view_hint מ-classify_question_intent, אלא אם תוצאות הכלים מצדיקות שינוי ברור."
            " הערכים האפשריים: map כאשר הממצא הגאוגרפי או מסלול התנועה הוא העיקר;"
            " timeline כאשר סדר האירועים והעיתוי הם העיקר; evidence כאשר בדיקת המקורות והרשומות הגולמיות היא העיקר.\n"
            "REASON הוא הסבר קצר בעברית, עד שמונה מילים, לבחירת התצוגה.\n"
            "אין להשתמש בכלי מערכת, קבצים, רשת או shell, ואין לבקש אישור לכלים."
            " מאגר המטרות תומך באיתור ישיר לפי מזהה רשומה גולמית באמצעות search_target_candidates עם record_id."
            " הכלי זמין למשה בלבד; הסוכן הכללי אינו טוען שביצע חיפוש כזה ואינו מנתב למשה ללא אזכור מפורש של @משה."
            " לפני התשובה הסופית, כאשר קיימים נתונים מבוקשים להצגה או ראיות מהותיות לניווט, חובה לקרוא פעם אחת ל-present_requested_results."
            " בשדה layers בחר רק את הרשומות שעונות ישירות למה שהמשתמש ביקש; שכבה אחת כברירת מחדל וכמה רק אם התבקשו כמה סוגי תוצאה."
            " בשדה evidence_layers בחר מספר קטן של שכבות בעלות שמות משמעותיים, ורק רשומות קנוניות שתומכות מהותית במסקנה הסופית."
            " קבץ ראיות לפי הסיבה שהן חשובות ולא לפי הכלי שהחזיר אותן, ובחר עבורן map או timeline."
            " לעולם אל תכלול תוצאות ביניים, בדיקות כפילות, מועמדים שנדחו או פלט כלי שאינו רלוונטי ישירות לתוצאה או למסקנה."
            " אם אין אובייקט נתונים להצגה ואין ראיות מהותיות לניווט, אל תקרא לכלי."
            " כפתור הצג תוצאות מבוסס רק על layers; אזור מזהי ראיות מבוסס רק על evidence_layers."
        )
        if responding_agent == MOSHE_AGENT_ID:
            instructions += (
                "\n\nאתה משה, קצין המטרות. המשתמש פנה אליך במפורש באמצעות @משה. "
                "אתה אחראי לשאלות הבהרה, איתור ראיות, סיווג, מיזוג, בדיקת עצמאות מקורות, "
                "בדיקת כפילויות, ויצירת מועמד מטרה רק כאשר כלי prepare_target_candidate מאשר persistence_eligible=true. "
                "כאשר המשתמש מספק מזהה REC, השתמש ב-search_target_candidates עם record_id כדי למצוא כל מטרה קיימת שמכילה את הרשומה. "
                "ממצא בביטחון נמוך מדווח למשתמש ואינו נשמר. אל תמציא source_group ואל תעקוף את כלי המיזוג. "
                "בבקשה הנוגעת למעקב, פרש שפה טבעית ללא ביטויי פקודה שמורים. REC הוא אינדיקציה; TGT הוא נושא אפשרי בלבד ולעולם אינו ראיה. "
                "פתור את המזהים והשתמש ב-prepare_workstream_indication_proposal כדי להציג הצעה לפני שמירה. "
                "אל תאשר הצעה בעצמך: רק בתור משתמש מאוחר ונפרד השתמש ב-decide_workstream_indication_proposal. "
                "אם התגובה עמומה בקש הבהרה; ready_for_assessment הוא מסירה להערכה ולא הערכה או יצירת מטרה. "
                "בזרימת המעקב אל תפעיל כלי יצירה או עדכון של בנק המטרות. "
                "אין לך הרשאה לכלי מערכת, filesystem, shell, SQL, מחיקה, reset, evaluator או שינוי סטטוס."
            )
        state_block = self.render_investigation_state(investigation_state)
        full_instructions = f"{instructions}\n\n{state_block}" if state_block else instructions
        safe_investigation_id = re.sub(r"[^A-Za-z0-9_.:-]+", "-", str(investigation_id or "")).strip("-")
        session_id = safe_investigation_id or f"intelligence-orchestrator-{int(time.time() * 1000)}"
        session_started = time.perf_counter()
        with HermesSession(self.config) as session:
            performance["gateway"]["ssh_session_open_ms"] = elapsed_ms(session_started)
            stage_started = time.perf_counter()
            session.ssh_command(f"truncate -s 0 {audit_path}")
            performance["gateway"]["audit_truncate_ms"] = elapsed_ms(stage_started)
            ACTIVE_RUN_STARTED_AT = datetime.now(timezone.utc)
            ACTIVE_RUN_STARTED_AT_BY_AUDIT[audit_path] = ACTIVE_RUN_STARTED_AT
            create_started = time.perf_counter()
            created = session.request("POST", "/v1/runs", {
                "input": prompt,
                "instructions": full_instructions,
                "conversation_history": history[-10:],
                "session_id": session_id,
            })
            created_at = datetime.now(timezone.utc)
            performance["hermes"]["run_create_ms"] = elapsed_ms(create_started)
            run_id = created["run_id"]
            run_wait_started = time.perf_counter()
            deadline = time.time() + 480
            while time.time() < deadline:
                poll_started = time.perf_counter()
                status = session.request("GET", f"/v1/runs/{run_id}")
                performance["hermes"]["poll_count"] += 1
                performance["hermes"]["status_request_total_ms"] += elapsed_ms(poll_started)
                if status.get("status") in TERMINAL_STATUSES:
                    terminal_at = datetime.now(timezone.utc)
                    performance["hermes"]["run_wait_ms"] = elapsed_ms(run_wait_started)
                    if status.get("status") != "completed":
                        raise RuntimeError(status.get("error") or f"Hermes run {status.get('status')}")
                    postprocess_started = time.perf_counter()
                    output = status.get("output", "")
                else:
                    time.sleep(1)
                    continue
                step_pattern = re.compile(
                    r"(?im)^\s*שלב חקירה\s*:\s*([^|\r\n]+?)\s*\|\s*([^|\r\n]+?)\s*\|\s*([^|\r\n]+?)\s*\|\s*([^|\r\n]+?)\s*\|\s*([^|\r\n]+?)\s*\|\s*(.+?)\s*$"
                )
                any_step_line_pattern = re.compile(r"(?im)^\s*שלב חקירה\s*:.*(?:\r?\n|$)")
                investigation_steps = [
                    {
                        "tool": match.group(1).strip(),
                        "observed_clue": match.group(2).strip(),
                        "decision": match.group(3).strip(),
                        "expected_value": match.group(4).strip(),
                        "action": match.group(5).strip(),
                        "result": match.group(6).strip(),
                    }
                    for match in step_pattern.finditer(output)
                ]
                output_without_steps = any_step_line_pattern.sub("", output)
                view_match = re.search(
                    r"(?im)^\s*תצוגה מומלצת\s*:\s*(map|timeline|evidence)(?:\s*\|\s*(.+?))?\s*$",
                    output_without_steps,
                )
                recommended_view = view_match.group(1).lower() if view_match else None
                view_reason = view_match.group(2).strip() if view_match and view_match.group(2) else ""
                clean_output = (
                    (output_without_steps[:view_match.start()] + output_without_steps[view_match.end():]).strip()
                    if view_match else output_without_steps.strip()
                )
                if recommended_view is None:
                    combined = f"{prompt}\n{clean_output}"
                    if re.search(r"רשומ|מקור|ראי|אימות|בדוק|ציטוט", combined):
                        recommended_view, view_reason = "evidence", "בדיקה ישירה של הרשומות המצוטטות"
                    elif re.search(r"רצף|סדר|ציר זמן|לפי זמן|מיין|תמיין|כרונולוג|לפני|אחרי|עיתוי|שעה", combined):
                        recommended_view, view_reason = "timeline", "העיתוי ורצף האירועים הם העיקר"
                    else:
                        recommended_view, view_reason = "map", "המיקומות והתנועה הם מוקד הממצא"
                event_fetch_started = time.perf_counter()
                event_stream = session.request(
                    "GET",
                    f"/v1/runs/{run_id}/events",
                    timeout=30,
                    parse_json=False,
                )
                performance["gateway"]["event_fetch_ms"] = elapsed_ms(event_fetch_started)
                events = []
                for line in event_stream.splitlines():
                    if not line.startswith("data:"):
                        continue
                    try:
                        event = json.loads(line[5:].strip())
                    except json.JSONDecodeError:
                        continue
                    if event.get("event") in {"tool.started", "tool.completed"}:
                        events.append(event)
                audit_fetch_started = time.perf_counter()
                audit_text = session.ssh_command(f"cat {audit_path} 2>/dev/null || true")
                performance["gateway"]["audit_fetch_ms"] = elapsed_ms(audit_fetch_started)
                audit_records = []
                for line in audit_text.splitlines():
                    try:
                        audit_records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
                exact_steps = self.summarize_audit(audit_records)
                answer_event_ids = list(dict.fromkeys(
                    event_id for event_id in EVENT_ID_PATTERN.findall(clean_output)
                    if event_id.startswith("REC-")
                ))
                tool_durations = [
                    float(record.get("duration_ms"))
                    for record in audit_records
                    if isinstance(record.get("duration_ms"), (int, float))
                ]
                slowest_record = max(
                    (record for record in audit_records if isinstance(record.get("duration_ms"), (int, float))),
                    key=lambda record: float(record.get("duration_ms")),
                    default=None,
                )
                first_tool_time = min(
                    (parsed for parsed in (parse_utc(record.get("timestamp_utc")) for record in audit_records) if parsed),
                    default=None,
                )
                tool_total_ms = round(sum(tool_durations), 3)
                performance["tools"] = {
                    "tool_call_count": len(audit_records),
                    "tool_execution_total_ms": tool_total_ms,
                    "tool_execution_max_ms": round(max(tool_durations), 3) if tool_durations else 0,
                    "slowest_tool": (
                        {
                            "name": slowest_record.get("tool"),
                            "duration_ms": round(float(slowest_record.get("duration_ms")), 3),
                        }
                        if slowest_record else None
                    ),
                }
                if first_tool_time:
                    performance["hermes"]["time_to_first_tool_ms"] = round((first_tool_time - created_at).total_seconds() * 1000, 3)
                hermes_run_ms = round((terminal_at - created_at).total_seconds() * 1000, 3)
                performance["hermes"]["run_total_ms"] = hermes_run_ms
                performance["hermes"]["model_orchestration_gap_ms"] = round(max(0, hermes_run_ms - tool_total_ms), 3)
                if exact_steps and investigation_steps:
                    for index, step in enumerate(exact_steps):
                        if index >= len(investigation_steps):
                            continue
                        model_step = investigation_steps[index]
                        if model_step.get("tool") != step.get("tool"):
                            continue
                        step["model_explanation"] = {
                            "observed_clue": model_step.get("observed_clue"),
                            "decision": model_step.get("decision"),
                            "expected_value": model_step.get("expected_value"),
                            "action": model_step.get("action"),
                            "result": model_step.get("result"),
                        }
                performance["gateway"]["postprocess_ms"] = elapsed_ms(postprocess_started)
                performance["gateway"]["total_ms"] = elapsed_ms(overall_started)
                performance["summary"] = {
                    "total_user_wait_server_ms": performance["gateway"]["total_ms"],
                    "hermes_run_total_ms": performance["hermes"].get("run_total_ms"),
                    "time_to_first_tool_ms": performance["hermes"].get("time_to_first_tool_ms"),
                    "tool_execution_total_ms": performance["tools"].get("tool_execution_total_ms"),
                    "model_orchestration_gap_ms": performance["hermes"].get("model_orchestration_gap_ms"),
                    "tool_call_count": performance["tools"].get("tool_call_count"),
                    "slowest_tool": performance["tools"].get("slowest_tool"),
                }
                performance_log_path = write_performance_log(run_id, performance, prompt)
                requested_layers = requested_result_layers_from_audit(
                    audit_records,
                    locations=LOCATIONS,
                    entities=load_ui_entity_db(),
                )
                evidence_reference_layers = evidence_reference_layers_from_audit(
                    audit_records,
                    locations=LOCATIONS,
                    entities=load_ui_entity_db(),
                )
                collaboration = normalize_workstream_collaboration(audit_records)
                return build_agent_result({
                    "run_id": run_id,
                    "answer": clean_output,
                    "event_ids": answer_event_ids,
                    "answer_event_ids": answer_event_ids,
                    "recommended_view": recommended_view,
                    "view_reason": view_reason,
                    "investigation_steps": exact_steps or investigation_steps,
                    "events": events,
                    "usage": status.get("usage", {}),
                    "performance_log": performance_log_path.name,
                    **collaboration,
                }, responding_agent=responding_agent, session_id=session_id, mission_run_id=mission_run_id,
                    requested_result_layers=requested_layers,
                    evidence_reference_layers=evidence_reference_layers)
            time.sleep(1)
        raise TimeoutError("Hermes investigation exceeded 480 seconds")


def run_moshe_playback_reevaluation(run: dict, released_timeframe: dict) -> dict:
    """Run one playback-filtered Moshe assessment for a newly released window."""
    workstream_id = run.get("workstream_id")
    workstream_contexts = []
    if workstream_id:
        workstream_contexts.append(bounded_workstream_context(
            {
                "workstream_id": workstream_id,
                "current_turn_message_id": f"playback-revision-{run['revision']}",
            },
            run["investigation_id"],
        ))
    else:
        for workstream in list_workstreams(run["investigation_id"]):
            if workstream.get("status") == "archived":
                continue
            workstream_contexts.append(bounded_workstream_context(
                {
                    "workstream_id": workstream["workstream_id"],
                    "current_turn_message_id": f"playback-revision-{run['revision']}",
                },
                run["investigation_id"],
            ))
    investigation_state = {
        "active_workstreams": workstream_contexts,
        "scenario_playback": {
            "run_id": run["run_id"],
            "revision": run["revision"],
            "newly_released_timeframe": released_timeframe,
            "visible_timeframe": run["visible_timeframe"],
        },
    }
    if len(workstream_contexts) == 1:
        investigation_state["active_workstream"] = workstream_contexts[0]
    prompt = (
        "התקדם שלב אחד בתרחיש ההיסטורי. קלוט את פרוסת המידע החדשה, "
        "בדוק כיצד היא משנה כל אינדיקציה, יעד או מעקב פעיל ורלוונטי בחקירה, "
        "והצג את ההערכות המעודכנות. "
        "השתמש רק במידע הזמין כעת דרך כלי הראיות. "
        f"חלון המידע החדש: {released_timeframe.get('from')} עד {released_timeframe.get('to')}. "
        f"חלון מצטבר זמין: {run['visible_timeframe'].get('from')} עד {run['visible_timeframe'].get('to')}."
    )
    config = load_agent_hermes_config(MOSHE_AGENT_ID)
    return HermesClient(config).investigate(
        prompt,
        [],
        investigation_state=investigation_state,
        investigation_id=f"{run['run_id']}:revision:{run['revision']}",
        responding_agent=MOSHE_AGENT_ID,
        mission_run_id=f"{run['run_id']}:revision:{run['revision']}",
    )


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - %s\n" % (self.log_date_time_string(), fmt % args))

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def send_json(self, status, value):
        payload = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlparse(self.path)
        if path.path == "/api/status":
            self.send_json(200, {
                "mode": "hermes",
                "configured": CONFIG_PATH.exists(),
                "build": APP_BUILD,
                "dataset_version": DATASET_VERSION,
                "dataset_url": DATASET_URL,
                "locations_url": LOCATIONS_URL,
                "dataset_rows": len(load_ui_events()),
            })
            return
        if path.path == "/api/layers":
            self.send_json(200, {"layers": list_ui_layers()})
            return
        if path.path.startswith("/api/layers/") and path.path.endswith("/rows"):
            layer_id = unquote(path.path[len("/api/layers/"):-len("/rows")])
            result = get_ui_layer_rows(layer_id)
            if result is None:
                self.send_json(404, {"error": "Layer not found"})
            else:
                layer, rows = result
                self.send_json(200, {"layer": layer, "rows": rows})
            return
        if path.path == "/api/saved-questions":
            self.send_json(200, {"saved_questions": list_saved_question_metadata()})
            return
        if path.path == "/api/saved-question":
            query = parse_qs(path.query)
            saved_id = (query.get("id") or [""])[0]
            result = load_saved_question(saved_id)
            if result is None:
                self.send_json(404, {"error": "Saved question not found"})
            else:
                self.send_json(200, result)
            return
        if path.path == "/api/investigations":
            self.send_json(200, {"investigations": list_investigation_memory_metadata()})
            return
        if path.path == "/api/investigation-memory":
            query = parse_qs(path.query)
            investigation_id = (query.get("id") or [""])[0]
            try:
                result = load_investigation_memory(investigation_id)
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
                return
            self.send_json(200, result)
            return
        if path.path == "/api/scenarios":
            try:
                self.send_json(200, {"scenarios": list_scenarios(SCENARIO_MANIFESTS_DIR)})
            except ValueError as exc:
                self.send_json(500, {"error": str(exc)})
            return
        if path.path.startswith("/api/scenarios/"):
            scenario_id = unquote(path.path[len("/api/scenarios/"):])
            query = parse_qs(path.query)
            version_text = (query.get("version") or [""])[0]
            try:
                version = int(version_text) if version_text else None
                manifest = get_manifest(SCENARIO_MANIFESTS_DIR, scenario_id, version)
            except (TypeError, ValueError) as exc:
                self.send_json(400, {"error": str(exc)})
                return
            if manifest is None:
                self.send_json(404, {"error": "Scenario not found"})
            else:
                self.send_json(200, scenario_details(manifest))
            return
        if path.path.startswith("/api/scenario-runs/"):
            run_id = unquote(path.path[len("/api/scenario-runs/"):])
            try:
                result = load_scenario_run(SCENARIO_RUNS_DIR, run_id)
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
                return
            if result is None:
                self.send_json(404, {"error": "Scenario run not found"})
            else:
                self.send_json(200, public_run(result))
            return
        if path.path == "/api/playback":
            investigation_id = (parse_qs(path.query).get("investigation_id") or [""])[0]
            try:
                self.send_json(200, investigation_playback_status(investigation_id))
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            return
        if path.path == "/api/workstreams":
            query = parse_qs(path.query)
            investigation_id = (query.get("investigation_id") or [""])[0]
            try:
                if (query.get("fallback") or [""])[0] == "latest":
                    self.send_json(200, list_workstreams_with_latest_fallback(investigation_id))
                else:
                    self.send_json(200, {"workstreams": list_workstreams(investigation_id)})
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            return
        if path.path.startswith("/api/workstreams/") and path.path.endswith("/playback"):
            workstream_id = unquote(
                path.path[len("/api/workstreams/"):-len("/playback")].rstrip("/")
            )
            try:
                result = workstream_playback_status(workstream_id)
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
                return
            if result is None:
                self.send_json(404, {"error": "Workstream not found"})
            else:
                self.send_json(200, result)
            return
        artifact_route = parse_artifact_api_path(path.path)
        if artifact_route is not None:
            workstream_id, artifact_id_value, is_revisions = artifact_route
            if is_revisions:
                self.send_error(405)
                return
            try:
                workstream = load_workstream(workstream_id)
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
                return
            if workstream is None:
                self.send_json(404, {"error": "Workstream not found"})
                return
            if artifact_id_value is None:
                self.send_json(200, {"artifacts": list_artifacts(workstream)})
                return
            artifact = get_artifact(workstream, artifact_id_value)
            if artifact is None:
                self.send_json(404, {"error": "Artifact not found"})
            else:
                self.send_json(200, artifact)
            return
        if path.path.startswith("/api/workstreams/"):
            workstream_id = unquote(path.path[len("/api/workstreams/"):])
            try:
                result = load_workstream(workstream_id)
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
                return
            if result is None:
                self.send_json(404, {"error": "Workstream not found"})
            else:
                self.send_json(200, result)
            return
        if path.path == "/api/recorded-questions":
            self.send_json(200, {"questions": recorded_questions(), "replay_delay_ms": 2000})
            return
        if path.path == "/api/recorded-run":
            query = parse_qs(path.query)
            recorded_id = (query.get("id") or [""])[0]
            result = recorded_result(recorded_id)
            if result is None:
                self.send_json(404, {"error": "Recorded question not found"})
            else:
                self.send_json(200, result)
            return
        if path.path == "/api/live-steps":
            try:
                requested_agent = (parse_qs(path.query).get("agent") or ["general"])[0]
                agent_id = MOSHE_AGENT_ID if requested_agent == MOSHE_AGENT_ID else "general"
                config = load_agent_hermes_config(agent_id)
                steps = HermesClient(config).read_live_steps()
                self.send_json(200, {"investigation_steps": steps})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/playback/mode":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 1_000_000:
                    self.send_json(413, {"error": "Playback mode payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                if not isinstance(request, dict):
                    raise ValueError("Invalid playback mode payload")
                investigation_id = str(request.get("investigation_id") or "").strip()
                mode = str(request.get("mode") or "").strip()
                if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id):
                    raise ValueError("Invalid investigation id")
                if mode not in {"historical", "real_time"}:
                    raise ValueError("Invalid intelligence mode")
                if mode == "historical":
                    write_historical_visibility(SCENARIO_RUNS_DIR)
                else:
                    run = find_investigation_run(SCENARIO_RUNS_DIR, investigation_id)
                    if run is None:
                        manifest = prepared_playback_manifest()
                        if manifest is None:
                            raise LookupError("Prepared scenario not found")
                        run, _ = start_scenario_run(
                            SCENARIO_MANIFESTS_DIR,
                            SCENARIO_RUNS_DIR,
                            {
                                "scenario_id": manifest["scenario_id"],
                                "version": manifest["version"],
                                "investigation_id": investigation_id,
                                "idempotency_key": (
                                    f"mode-real-time-{investigation_id}-"
                                    f"{int(time.time() * 1000)}"
                                ),
                            },
                            scenario_workstream_exists,
                        )
                    current = load_scenario_run(SCENARIO_RUNS_DIR, run["run_id"])
                    if current is None:
                        raise LookupError("Scenario run not found")
                    write_playback_visibility(SCENARIO_RUNS_DIR, current)
                self.send_json(200, investigation_playback_status(investigation_id))
            except PlaybackConflictError as exc:
                self.send_json(409, {
                    "error": str(exc), "current_revision": exc.current_revision,
                })
            except LookupError as exc:
                self.send_json(409, {"error": str(exc)})
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path == "/api/playback/next":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 1_000_000:
                    self.send_json(413, {"error": "Playback payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                if not isinstance(request, dict):
                    raise ValueError("Invalid playback payload")
                investigation_id = str(request.get("investigation_id") or "").strip()
                if not INVESTIGATION_ID_PATTERN.fullmatch(investigation_id):
                    raise ValueError("Invalid investigation id")
                policy = load_playback_visibility(SCENARIO_RUNS_DIR) or {}
                if policy.get("mode") != "real_time" or not policy.get("active"):
                    raise ValueError("Real-time intelligence mode is not active")
                existing = find_investigation_run(SCENARIO_RUNS_DIR, investigation_id)
                claimed_revision = None
                if existing is None:
                    manifest = prepared_playback_manifest()
                    if manifest is None:
                        raise LookupError("Prepared scenario not found")
                    run, _ = start_scenario_run(
                        SCENARIO_MANIFESTS_DIR,
                        SCENARIO_RUNS_DIR,
                        {
                            "scenario_id": manifest["scenario_id"],
                            "version": manifest["version"],
                            "investigation_id": investigation_id,
                            "idempotency_key": request.get("idempotency_key"),
                        },
                        scenario_workstream_exists,
                    )
                    released_timeframe = {
                        "from": run["current_stage"]["from"],
                        "to": run["current_stage"]["to"],
                        "from_inclusive": True,
                        "to_exclusive": True,
                    }
                    claimed_revision = int(run["revision"])
                elif (
                    existing.get("transition_history")
                    and existing["transition_history"][0].get("idempotency_key")
                    == request.get("idempotency_key")
                ):
                    manifest = get_manifest(
                        SCENARIO_MANIFESTS_DIR,
                        existing["scenario_id"],
                        existing["scenario_version"],
                    )
                    if manifest is None:
                        raise LookupError("Scenario not found")
                    first = manifest["stages"][0]
                    run = existing
                    released_timeframe = {
                        "from": first["from"],
                        "to": first["to"],
                        "from_inclusive": True,
                        "to_exclusive": True,
                    }
                    claimed_revision = 1
                else:
                    run, _ = transition_scenario_run(
                        SCENARIO_MANIFESTS_DIR,
                        SCENARIO_RUNS_DIR,
                        existing["run_id"],
                        request,
                        "advance",
                    )
                    if run is None:
                        raise LookupError("Scenario run not found")
                    released_timeframe = {
                        "from": run["current_stage"]["from"],
                        "to": run["current_stage"]["to"],
                        "from_inclusive": True,
                        "to_exclusive": True,
                    }
                    claimed_revision = int(run["revision"])
                current = load_scenario_run(SCENARIO_RUNS_DIR, run["run_id"])
                if current is None:
                    raise LookupError("Scenario run not found")
                write_playback_visibility(SCENARIO_RUNS_DIR, current)
                _, claimed = claim_reevaluation(
                    SCENARIO_RUNS_DIR, run["run_id"], claimed_revision
                )
                moshe_result = None
                if claimed:
                    try:
                        moshe_result = run_moshe_playback_reevaluation(
                            run, released_timeframe
                        )
                        finish_reevaluation(
                            SCENARIO_RUNS_DIR, run["run_id"], claimed_revision, "completed"
                        )
                    except Exception as exc:
                        finish_reevaluation(
                            SCENARIO_RUNS_DIR,
                            run["run_id"],
                            claimed_revision,
                            "failed",
                            str(exc),
                        )
                        self.send_json(502, {
                            "error": str(exc),
                            "run": run_with_next_stage(SCENARIO_MANIFESTS_DIR, run),
                            "moshe_triggered": True,
                        })
                        return
                self.send_json(200, {
                    "run": run_with_next_stage(SCENARIO_MANIFESTS_DIR, run),
                    "released_timeframe": released_timeframe,
                    "moshe_triggered": claimed,
                    "moshe_result": moshe_result,
                })
            except PlaybackConflictError as exc:
                self.send_json(409, {
                    "error": str(exc), "current_revision": exc.current_revision,
                })
            except LookupError as exc:
                self.send_json(409, {"error": str(exc)})
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path == "/api/scenario-runs":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 1_000_000:
                    self.send_json(413, {"error": "Scenario run payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                result, created = start_scenario_run(
                    SCENARIO_MANIFESTS_DIR,
                    SCENARIO_RUNS_DIR,
                    request,
                    scenario_workstream_exists,
                )
                current_policy = load_playback_visibility(SCENARIO_RUNS_DIR)
                if (
                    result.get("status") == "active"
                    and current_policy
                    and current_policy.get("active")
                    and current_policy.get("run_id") != result.get("run_id")
                ):
                    raise PlaybackConflictError(
                        "Another scenario run is already active",
                        int(current_policy.get("revision") or 1),
                    )
                write_playback_visibility(SCENARIO_RUNS_DIR, result)
                self.send_json(201 if created else 200, result)
            except PlaybackConflictError as exc:
                self.send_json(409, {
                    "error": str(exc), "current_revision": exc.current_revision,
                })
            except LookupError as exc:
                self.send_json(404, {"error": str(exc)})
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        scenario_action = parse_scenario_run_action(path)
        if scenario_action is not None:
            run_id, action = scenario_action
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 1_000_000:
                    self.send_json(413, {"error": "Scenario transition payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                result, replayed = transition_scenario_run(
                    SCENARIO_MANIFESTS_DIR,
                    SCENARIO_RUNS_DIR,
                    run_id,
                    request,
                    action,
                )
                if result is None:
                    self.send_json(404, {"error": "Scenario run not found"})
                else:
                    current = load_scenario_run(SCENARIO_RUNS_DIR, run_id)
                    if current is not None:
                        write_playback_visibility(SCENARIO_RUNS_DIR, current)
                    self.send_json(200, {**result, "idempotent_replay": replayed})
            except PlaybackConflictError as exc:
                self.send_json(409, {
                    "error": str(exc), "current_revision": exc.current_revision,
                })
            except LookupError as exc:
                self.send_json(409, {"error": str(exc)})
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path == "/api/workstreams":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 1_000_000:
                    self.send_json(413, {"error": "Workstream payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                if not isinstance(request, dict):
                    raise ValueError("Invalid workstream payload")
                self.send_json(201, create_workstream(request))
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        artifact_route = parse_artifact_api_path(path)
        if artifact_route is not None:
            workstream_id, artifact_id_value, is_revisions = artifact_route
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 1_000_000:
                    self.send_json(413, {"error": "Artifact payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                if not isinstance(request, dict):
                    raise ValueError("Invalid artifact payload")
                workstream = load_workstream(workstream_id)
                if workstream is None:
                    self.send_json(404, {"error": "Workstream not found"})
                    return
                now = utc_now_iso()
                if artifact_id_value is None and not is_revisions:
                    artifact = create_artifact(
                        workstream,
                        request,
                        resolve_event=resolve_workstream_event,
                        resolve_target=resolve_workstream_target,
                        now=now,
                        id_factory=artifact_id,
                    )
                    write_workstream(workstream)
                    self.send_json(201, artifact)
                    return
                if artifact_id_value is not None and is_revisions:
                    artifact = revise_artifact(
                        workstream,
                        artifact_id_value,
                        request,
                        resolve_event=resolve_workstream_event,
                        now=now,
                        id_factory=artifact_id,
                    )
                    write_workstream(workstream)
                    self.send_json(200, artifact)
                    return
                self.send_error(405)
            except ArtifactConflictError as exc:
                self.send_json(409, {"error": str(exc), "current_revision": exc.current_revision})
            except LookupError as exc:
                self.send_json(404, {"error": str(exc)})
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path.startswith("/api/workstreams/") and path.endswith("/archive"):
            workstream_id = unquote(path[len("/api/workstreams/"):-len("/archive")].rstrip("/"))
            try:
                archived = archive_workstream(workstream_id)
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
                return
            if archived is None:
                self.send_json(404, {"error": "Workstream not found"})
            else:
                self.send_json(200, archived)
            return
        if path.startswith("/api/workstreams/") and path.endswith("/playback/next"):
            workstream_id = unquote(
                path[len("/api/workstreams/"):-len("/playback/next")].rstrip("/")
            )
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 1_000_000:
                    self.send_json(413, {"error": "Playback payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                if not isinstance(request, dict):
                    raise ValueError("Invalid playback payload")
                workstream = load_workstream(workstream_id)
                if workstream is None or workstream.get("status") == "archived":
                    self.send_json(404, {"error": "Workstream not found"})
                    return
                existing = find_workstream_run(SCENARIO_RUNS_DIR, workstream_id)
                claimed_revision = None
                if existing is None:
                    manifest = prepared_playback_manifest()
                    if manifest is None:
                        raise LookupError("Prepared scenario not found")
                    run, _ = start_scenario_run(
                        SCENARIO_MANIFESTS_DIR,
                        SCENARIO_RUNS_DIR,
                        {
                            "scenario_id": manifest["scenario_id"],
                            "version": manifest["version"],
                            "workstream_id": workstream_id,
                            "investigation_id": workstream["investigation_id"],
                            "idempotency_key": request.get("idempotency_key"),
                        },
                        scenario_workstream_exists,
                    )
                    released_timeframe = {
                        "from": run["current_stage"]["from"],
                        "to": run["current_stage"]["to"],
                        "from_inclusive": True,
                        "to_exclusive": True,
                    }
                    claimed_revision = int(run["revision"])
                elif (
                    existing.get("transition_history")
                    and existing["transition_history"][0].get("idempotency_key")
                    == request.get("idempotency_key")
                ):
                    manifest = get_manifest(
                        SCENARIO_MANIFESTS_DIR,
                        existing["scenario_id"],
                        existing["scenario_version"],
                    )
                    if manifest is None:
                        raise LookupError("Scenario not found")
                    first = manifest["stages"][0]
                    run = existing
                    released_timeframe = {
                        "from": first["from"],
                        "to": first["to"],
                        "from_inclusive": True,
                        "to_exclusive": True,
                    }
                    claimed_revision = 1
                else:
                    run, _ = transition_scenario_run(
                        SCENARIO_MANIFESTS_DIR,
                        SCENARIO_RUNS_DIR,
                        existing["run_id"],
                        request,
                        "advance",
                    )
                    if run is None:
                        raise LookupError("Scenario run not found")
                    released_timeframe = {
                        "from": run["current_stage"]["from"],
                        "to": run["current_stage"]["to"],
                        "from_inclusive": True,
                        "to_exclusive": True,
                    }
                    claimed_revision = int(run["revision"])
                current = load_scenario_run(SCENARIO_RUNS_DIR, run["run_id"])
                if current is None:
                    raise LookupError("Scenario run not found")
                write_playback_visibility(SCENARIO_RUNS_DIR, current)
                _, claimed = claim_reevaluation(
                    SCENARIO_RUNS_DIR, run["run_id"], claimed_revision
                )
                moshe_result = None
                if claimed:
                    try:
                        moshe_result = run_moshe_playback_reevaluation(
                            run, released_timeframe
                        )
                        finish_reevaluation(
                            SCENARIO_RUNS_DIR, run["run_id"], claimed_revision, "completed"
                        )
                    except Exception as exc:
                        finish_reevaluation(
                            SCENARIO_RUNS_DIR,
                            run["run_id"],
                            claimed_revision,
                            "failed",
                            str(exc),
                        )
                        self.send_json(502, {
                            "error": str(exc),
                            "run": run_with_next_stage(SCENARIO_MANIFESTS_DIR, run),
                            "moshe_triggered": True,
                        })
                        return
                self.send_json(200, {
                    "run": run_with_next_stage(SCENARIO_MANIFESTS_DIR, run),
                    "released_timeframe": released_timeframe,
                    "moshe_triggered": claimed,
                    "moshe_result": moshe_result,
                })
            except PlaybackConflictError as exc:
                self.send_json(409, {
                    "error": str(exc), "current_revision": exc.current_revision,
                })
            except LookupError as exc:
                self.send_json(409, {"error": str(exc)})
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path == "/api/saved-question":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 15_000_000:
                    self.send_json(413, {"error": "Saved question payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                saved = create_saved_question(request)
                self.send_json(201, saved_question_metadata(saved))
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path == "/api/investigation-memory/chat-summary":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 2_000_000:
                    self.send_json(413, {"error": "Investigation memory summary payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                if not isinstance(request, dict):
                    raise ValueError("Invalid investigation memory summary payload")
                saved = create_chat_summary_memory(request)
                self.send_json(201, saved)
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path == "/api/investigation-memory/layer":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 2_000_000:
                    self.send_json(413, {"error": "Investigation memory layer payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                if not isinstance(request, dict):
                    raise ValueError("Invalid investigation memory layer payload")
                saved = create_layer_memory(request)
                self.send_json(201, saved)
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path == "/api/performance-client":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                request = json.loads(self.rfile.read(length).decode("utf-8"))
                run_id = str(request.get("run_id") or "")
                client_performance = request.get("client") or {}
                updated = update_performance_client(run_id, client_performance)
                self.send_json(200, {"stored": bool(updated), "file": updated.name if updated else None})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path != "/api/investigate":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            request = json.loads(self.rfile.read(length).decode("utf-8"))
            prompt = str(request.get("prompt", "")).strip()
            if not prompt:
                self.send_json(400, {"error": "Missing prompt"})
                return
            conversation_id = str(request.get("investigation_id") or "").strip()
            route = route_agent_request(request)
            workstream_context = bounded_workstream_context(
                request.get("workstream_context"), conversation_id
            )
            investigation_state = request.get("investigation_state")
            if not isinstance(investigation_state, dict):
                investigation_state = {}
            if workstream_context:
                investigation_state = {**investigation_state, "active_workstream": workstream_context}
            config = load_agent_hermes_config(route.responding_agent)
            result = HermesClient(config).investigate(
                prompt,
                request.get("history") or [],
                investigation_state=investigation_state or None,
                investigation_id=route.mission_run_id if route.responding_agent == MOSHE_AGENT_ID else conversation_id,
                is_continuation=bool(request.get("is_continuation")) and not route.mission_started,
                continuation_context=request.get("continuation_context"),
                responding_agent=route.responding_agent,
                mission_run_id=route.mission_run_id,
            )
            if (
                request.get("workstream_creation_requested") is True
                and route.responding_agent == MOSHE_AGENT_ID
            ):
                try:
                    created = apply_workstream_creation(
                        conversation_id, result.get("workstream_creation")
                    )
                    if created:
                        result["workstream_created"] = created
                except ValueError as exc:
                    result["workstream_conflict"] = {"error": str(exc)}
            try:
                artifact, conflict = apply_workstream_action(
                    workstream_context, result.get("workstream_action")
                )
                if artifact:
                    result["workstream_artifact"] = artifact
                if conflict:
                    result["workstream_conflict"] = conflict
            except ArtifactConflictError as exc:
                result["workstream_conflict"] = {
                    "error": str(exc), "current_revision": exc.current_revision,
                }
            except (ValueError, LookupError) as exc:
                result["workstream_conflict"] = {"error": str(exc)}
            self.send_json(200, result)
        except Exception as exc:
            self.send_json(502, {"error": str(exc)})

    def do_PUT(self):
        path = urlparse(self.path).path
        if path.startswith("/api/workstreams/"):
            workstream_id = unquote(path[len("/api/workstreams/"):])
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 1_000_000:
                    self.send_json(413, {"error": "Workstream payload too large"})
                    return
                request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
                if not isinstance(request, dict):
                    raise ValueError("Invalid workstream payload")
                updated = update_workstream(workstream_id, request)
                if updated is None:
                    self.send_json(404, {"error": "Workstream not found"})
                else:
                    self.send_json(200, updated)
            except ValueError as exc:
                self.send_json(400, {"error": str(exc)})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path != "/api/investigation-memory":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 2_000_000:
                self.send_json(413, {"error": "Investigation memory payload too large"})
                return
            request = json.loads(self.rfile.read(length).decode("utf-8-sig"))
            if not isinstance(request, dict):
                raise ValueError("Invalid investigation memory payload")
            saved = save_investigation_memory(request)
            self.send_json(200, saved)
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except Exception as exc:
            self.send_json(502, {"error": str(exc)})

    def do_DELETE(self):
        path = urlparse(self.path)
        if path.path != "/api/saved-question":
            self.send_error(404)
            return
        query = parse_qs(path.query)
        saved_id = (query.get("id") or [""])[0]
        try:
            deleted = delete_saved_question(saved_id)
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
            return
        if not deleted:
            self.send_json(404, {"error": "Saved question not found"})
            return
        self.send_json(200, {"deleted": True, "id": saved_id})


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8767
    host = os.environ.get("POC_UI_HOST", "127.0.0.1")
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"POC server listening on http://{host}:{port}/", flush=True)
    server.serve_forever()
