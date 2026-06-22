from __future__ import annotations

import csv
import html
import json
from collections import Counter
from pathlib import Path


BASE = Path(__file__).resolve().parent
OUT = BASE / "raw_data_visual_presentation.html"
MAPPING = BASE / "event_id_mapping_private.json"

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

STORIES = [
    {
        "id": "pumps",
        "kind": "חשוד",
        "severity": "גבוה יחסית",
        "title": "התרחשות 1: משאבות השקיה",
        "short": "מכולה חקלאית לכאורה הופכת לרצף לוגיסטי לילי מחיפה לבית שאן.",
        "hypothesis": "ייתכן שמכולה שהוצהרה כמשאבות השקיה שימשה ככיסוי להעברת מטען רגיש דרך מחסן 11 ומזרחה לכיוון בית שאן / מעבר נהר הירדן.",
        "search_keywords": ["משאבות", "מחסן 11", "בית שאן", "קישון", "מעבר נהר הירדן", "שעון חול", "אופק"],
        "why": [
            "פער בין הכיסוי התמים לבין ההתנהגות: שחרור מזורז, תשלום קשור, מטען מכוסה ותנועה לילית.",
            "אותה שפה חוזרת: “משאבות” במסמכי המכולה וגם ביירוט.",
            "התכנסות בזמן ובמרחב: נמל חיפה → קישון → צומת גולני → בית שאן.",
            "קשר לדפוס עבר: ציוד חקלאי ככיסוי וחוליית שעון חול כתא לוגיסטי.",
        ],
        "route": ["L-201", "L-208", "L-202", "L-204", "L-206", "L-207", "L-203"],
        "old_ids": [
            "HX-001", "HX-002", "HX-003", "HX-004", "HX-005", "HX-006",
            "HX-007", "HX-008", "HX-009", "HX-010", "HX-011", "HX-013", "HX-015",
        ],
    },
    {
        "id": "filters",
        "kind": "חשוד",
        "severity": "בינוני",
        "title": "התרחשות 2: מסנני מים",
        "short": "משלוח מסננים לכאורה כולל קירור לא מוסבר, אריזה מפוצלת ותנועה לכיוון צמח.",
        "hypothesis": "ייתכן שמכולת מסנני מים שימשה ככיסוי להעברת פריטים רגישים באריזות קטנות דרך קישון לכיוון צמח.",
        "search_keywords": ["מסננים", "קירור", "צמח", "קישון", "סהר כחול"],
        "why": [
            "הצהרת מטען יבשה מול משאית קירור והוראה “המסננים נשארים קרים”.",
            "סהר כחול, כינוי שמקושר לקבוצת הסהר הצפוני, מופיע בתשלום מפוצל.",
            "העברה לרכב לא מסומן ועצירה ליד צמח יוצרים רצף הסתרה אפשרי.",
            "ההתרחשות חלשה יותר כי אין המשך גבול/רחפן ברור כמו בהתרחשות 1.",
        ],
        "route": ["L-201", "L-202", "L-204", "L-206", "L-209"],
        "old_ids": ["SX-001", "SX-002", "SX-003", "SX-004", "SX-005", "SX-006", "SX-007", "SX-008", "SX-009", "SX-010"],
    },
    {
        "id": "agriculture",
        "kind": "תמים",
        "severity": "תמים",
        "title": "התרחשות 3: משלוח חקלאי רגיל",
        "short": "דוגמה לרצף לוגיסטי דומה מבחוץ, אבל עם בדיקה, מסירה וחשבונית.",
        "hypothesis": "נראה כמשלוח חקלאי לגיטימי של צינורות השקיה.",
        "search_keywords": ["צינורות השקיה", "ציוד חקלאי", "צמח", "כרמל ציוד חקלאי"],
        "why": [
            "בדיקה פיזית בנמל.",
            "שחרור במסלול רגיל.",
            "מסירה בשעות היום עם חתימה.",
            "תשלום עם חשבונית מלאה.",
        ],
        "route": ["L-201", "L-204", "L-209"],
        "old_ids": ["BN-AGR-001", "BN-AGR-002", "BN-AGR-003", "BN-AGR-004", "BN-AGR-005"],
    },
    {
        "id": "fuel",
        "kind": "תמים",
        "severity": "תמים",
        "title": "התרחשות 4: שיירת דלק חוקית",
        "short": "שיירת דלק לילית שמסבירה חלק מהרעש, אבל לא את כל הרצף החשוד.",
        "hypothesis": "נראה כרצף דלק לגיטימי, אבל הוא גם משמש כהסבר חלופי לחלק מהתנועה.",
        "search_keywords": ["דלק", "מכליות", "צמח", "מעבר נהר הירדן", "קואופרטיב דלק העמק"],
        "why": [
            "יציאה לפי תוכנית אספקה שבועית.",
            "מסמכי מעבר תואמים.",
            "חיישן מאמת ארבע מכליות בלבד.",
            "אין כלי רכב נלווים לפי החיישן.",
        ],
        "route": ["L-209", "L-203"],
        "old_ids": ["BN-FUEL-001", "BN-FUEL-002", "BN-FUEL-003", "BN-FUEL-004", "HX-012"],
    },
    {
        "id": "maintenance",
        "kind": "תמים",
        "severity": "תמים",
        "title": "התרחשות 5: תחזוקת גנרטור בבית שאן",
        "short": "פעילות תעשייתית לילית עם פתיחה, ביצוע וסגירת קריאה.",
        "hypothesis": "נראה כהסבר תמים לחלק מהרעש באזור התעשייה בית שאן.",
        "search_keywords": ["תחזוקה", "גנרטור", "בית שאן", "מפעלי עמק הירדן"],
        "why": [
            "קריאת תחזוקה נפתחה מראש.",
            "רעש המנוע תואם בדיקת גנרטור.",
            "הפעילות מתועדת ביומן תחזוקה.",
            "הקריאה נסגרה עם חתימת טכנאי.",
        ],
        "route": ["L-207"],
        "old_ids": ["BN-MAINT-001", "BN-MAINT-002", "BN-MAINT-003", "BN-MAINT-004", "HX-014"],
    },
    {
        "id": "medical",
        "kind": "תמים",
        "severity": "תמים",
        "title": "התרחשות 6: משלוח סיוע רפואי",
        "short": "משלוח רפואי שנבדק, שוחרר וחולק בפומבי.",
        "hypothesis": "נראה כפעילות סיוע לגיטימית ונפרדת מהתרחשות 1.",
        "search_keywords": ["ציוד רפואי", "סיוע", "תרומה", "נצרת", "משרד סיוע מרחב"],
        "why": [
            "מספר מכולה נפרד.",
            "בדיקה ושחרור תקינים.",
            "חלוקה פומבית בנצרת.",
            "אימות עקיף דרך פוסטים מקומיים.",
        ],
        "route": ["L-201", "L-205"],
        "old_ids": ["BN-MED-001", "BN-MED-002", "BN-MED-003", "BN-MED-004", "HX-016"],
    },
]


def load_events() -> list[dict[str, str]]:
    with (BASE / "events_he_large.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda row: row["timestamp_utc"])
    return rows


def load_mapping() -> tuple[dict[str, str], dict[str, str]]:
    if not MAPPING.exists():
        return {}, {}
    payload = json.loads(MAPPING.read_text(encoding="utf-8"))
    return payload.get("old_to_new", {}), payload.get("new_to_old", {})


def enrich_events(rows: list[dict[str, str]], new_to_old: dict[str, str]) -> list[dict[str, str]]:
    enriched = []
    for row in rows:
        item = dict(row)
        item["location_name"] = LOCATIONS.get(row["location_id"], {}).get("name", row["location_id"])
        item["location_type"] = LOCATIONS.get(row["location_id"], {}).get("type", "")
        enriched.append(item)
    return enriched


def story_payload(old_to_new: dict[str, str], events_by_id: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    output = []
    all_events = list(events_by_id.values())
    for story in STORIES:
        event_ids = [old_to_new.get(old_id, old_id) for old_id in story["old_ids"]]
        event_ids = [event_id for event_id in event_ids if event_id in events_by_id]
        event_rows = [events_by_id[event_id] for event_id in event_ids]
        public_story = {key: value for key, value in story.items() if key != "old_ids"}
        keyword_hits = sum(
            1
            for row in all_events
            if any(
                keyword in " ".join([row["event_summary"], row["entity_or_actor"], row["location_name"]])
                for keyword in story["search_keywords"]
            )
        )
        output.append(
            {
                **public_story,
                "event_ids": event_ids,
                "event_count": len(event_ids),
                "keyword_hits": keyword_hits,
                "sources": sorted({row["source_type"] for row in event_rows}),
                "locations": [LOCATIONS[loc]["name"] for loc in story["route"] if loc in LOCATIONS],
            }
        )
    return output


def make_rows_preview(rows: list[dict[str, str]]) -> str:
    return "\n".join(
        "<tr>"
        f"<td>{html.escape(row['event_id'])}</td>"
        f"<td>{html.escape(row['timestamp_utc'])}</td>"
        f"<td>{html.escape(row['source_type'])}</td>"
        f"<td>{html.escape(row['source_reliability'])}</td>"
        f"<td>{html.escape(row['entity_or_actor'])}</td>"
        f"<td>{html.escape(row['location_name'])}</td>"
        f"<td>{html.escape(row['event_summary'])}</td>"
        "</tr>"
        for row in rows[:220]
    )


def main() -> None:
    old_to_new, new_to_old = load_mapping()
    events = enrich_events(load_events(), new_to_old)
    events_by_id = {row["event_id"]: row for row in events}
    stories = story_payload(old_to_new, events_by_id)
    suspicious_ids = {event_id for story in stories if story["kind"] == "חשוד" for event_id in story["event_ids"]}
    benign_ids = {event_id for story in stories if story["kind"] == "תמים" for event_id in story["event_ids"]}

    source_counts = Counter(row["source_type"] for row in events)
    payload = {
        "events": events,
        "stories": stories,
        "locations": LOCATIONS,
        "suspiciousIds": sorted(suspicious_ids),
        "benignIds": sorted(benign_ids),
        "sourceCounts": source_counts,
        "summary": {
            "total": len(events),
            "suspicious_events": len(suspicious_ids),
            "benign_story_events": len(benign_ids),
            "suspicious_percent": round(len(suspicious_ids) / len(events) * 100, 2),
        },
    }

    rows_preview = make_rows_preview(events)
    data_json = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")

    html_text = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>תצוגת התרחשויות מודיעיניות</title>
  <link rel="stylesheet" href="./maplibre-gl.css">
  <style>
    :root {{
      --bg: #f5f6f1;
      --panel: #ffffff;
      --ink: #20231f;
      --muted: #646b61;
      --line: #d9dfd4;
      --soft: #edf2e8;
      --danger: #b42318;
      --danger-soft: #fff0ed;
      --ok: #16725f;
      --ok-soft: #eaf5f0;
      --blue: #2f5d9b;
      --amber: #9a5b00;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: Arial, "Noto Sans Hebrew", sans-serif; line-height: 1.45; }}
    header {{ background: #fff; border-bottom: 1px solid var(--line); padding: 22px 32px 16px; position: sticky; top: 0; z-index: 10; }}
    h1 {{ margin: 0 0 6px; font-size: 28px; }}
    h2 {{ margin: 0 0 12px; font-size: 21px; }}
    h3 {{ margin: 0 0 8px; font-size: 16px; }}
    p {{ margin: 0 0 10px; color: var(--muted); }}
    button {{ font: inherit; }}
    main {{ max-width: 1560px; margin: 0 auto; padding: 22px 32px 54px; }}
    .topline {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }}
    .chip {{ border: 1px solid var(--line); background: var(--soft); border-radius: 999px; padding: 6px 10px; font-size: 13px; color: var(--muted); }}
    .kpis {{ display: grid; grid-template-columns: repeat(4, minmax(130px, 1fr)); gap: 10px; margin-bottom: 18px; }}
    .kpi {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 12px; }}
    .kpi strong {{ display: block; font-size: 24px; margin-bottom: 2px; }}
    .kpi span {{ color: var(--muted); font-size: 12px; }}
    .layout {{ display: grid; grid-template-columns: minmax(320px, 420px) 1fr; gap: 16px; align-items: start; }}
    .panel {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px; }}
    .empty-detail {{ min-height: 220px; display: grid; place-items: center; text-align: center; padding: 28px; }}
    .empty-detail h2 {{ margin-bottom: 6px; }}
    .story-list {{ display: grid; gap: 8px; }}
    .story-button {{ width: 100%; text-align: right; border: 1px solid var(--line); background: #fff; border-radius: 8px; padding: 12px; cursor: pointer; display: grid; gap: 5px; }}
    .story-button:hover, .story-button.active {{ border-color: var(--blue); box-shadow: 0 0 0 2px rgba(47,93,155,.12); }}
    .story-title {{ display: flex; align-items: center; justify-content: space-between; gap: 8px; font-weight: 700; }}
    .badge {{ border-radius: 999px; padding: 3px 8px; font-size: 12px; white-space: nowrap; }}
    .badge.suspicious {{ color: var(--danger); background: var(--danger-soft); border: 1px solid #ffc9c0; }}
    .badge.benign {{ color: var(--ok); background: var(--ok-soft); border: 1px solid #b9e2d5; }}
    .story-meta {{ color: var(--muted); font-size: 12px; }}
    .detail-grid {{ display: grid; grid-template-columns: 1fr 360px; gap: 14px; }}
    .summary-box {{ border-right: 4px solid var(--danger); background: #fffaf8; border-radius: 8px; padding: 12px; margin-bottom: 12px; }}
    .summary-box.benign {{ border-right-color: var(--ok); background: #f6fffb; }}
    .search-impact {{ margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--line); }}
    .search-impact strong {{ color: var(--ink); }}
    .search-terms {{ margin-top: 6px; color: var(--muted); font-size: 12px; }}
    .why-list {{ margin: 0; padding: 0 18px 0 0; color: var(--ink); }}
    .why-list li {{ margin-bottom: 7px; }}
    .route {{ display: grid; gap: 8px; margin-top: 8px; }}
    .route-step {{ display: grid; grid-template-columns: 28px 1fr; gap: 8px; align-items: start; }}
    .route-num {{ width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; background: var(--blue); color: #fff; font-size: 12px; direction: ltr; }}
    .route-name {{ font-weight: 700; }}
    .route-type {{ color: var(--muted); font-size: 12px; }}
    .evidence-list {{ display: grid; gap: 8px; margin-top: 12px; }}
    .evidence {{ border: 1px solid var(--line); border-radius: 8px; padding: 10px; background: #fff; }}
    .evidence.suspicious {{ background: var(--danger-soft); }}
    .evidence.benign {{ background: var(--ok-soft); }}
    .event-id {{ font-family: Consolas, monospace; direction: ltr; unicode-bidi: embed; font-weight: 700; }}
    .event-line {{ color: var(--muted); font-size: 12px; margin: 2px 0 6px; }}
    .jump {{ border: 1px solid var(--line); background: var(--soft); border-radius: 6px; padding: 5px 8px; cursor: pointer; font-size: 12px; }}
    .table-toolbar {{ display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin: 20px 0 10px; }}
    .table-toolbar input {{ flex: 1; min-width: 260px; border: 1px solid var(--line); border-radius: 6px; padding: 9px 10px; }}
    .table-toolbar button {{ border: 1px solid var(--line); background: var(--soft); border-radius: 6px; padding: 9px 10px; cursor: pointer; }}
    .table-toolbar button:disabled {{ cursor: not-allowed; opacity: .45; }}
    .table-wrap {{ max-height: 480px; overflow: auto; border: 1px solid var(--line); background: #fff; border-radius: 8px; }}
    .map-panel {{ margin-top: 16px; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fbfcf8; }}
    .map-head {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; padding: 12px 14px; border-bottom: 1px solid var(--line); background: #fff; }}
    .map-head h3 {{ margin: 0 0 4px; }}
    .map-head p {{ margin: 0; font-size: 13px; }}
    .map-status {{ color: var(--muted); font-size: 13px; white-space: nowrap; }}
    .map-canvas {{ height: 540px; min-height: 430px; position: relative; }}
    .maplibregl-map {{ font-family: Arial, "Noto Sans Hebrew", sans-serif; }}
    .maplibregl-ctrl-attrib {{ direction: ltr; font-size: 10px; }}
    .map-count-marker {{ min-width: 116px; padding: 7px 10px; border: 1px solid #9bb4d8; border-radius: 7px; background: rgba(255,255,255,.94); box-shadow: 0 2px 8px rgba(32,35,31,.18); text-align: center; color: var(--ink); direction: rtl; }}
    .map-count-marker strong {{ display: block; font-size: 13px; }}
    .map-count-marker span {{ display: block; margin-top: 1px; color: var(--muted); font-size: 11px; white-space: nowrap; }}
    .map-count-marker.route {{ border-color: #ee9b91; background: rgba(255,240,237,.96); }}
    .map-count-marker.route.benign {{ border-color: #8ccab7; background: rgba(234,245,240,.96); }}
    .map-count-marker.dim {{ opacity: .35; }}
    .map-count-marker.focus {{ box-shadow: 0 0 0 3px rgba(47,93,155,.32), 0 2px 8px rgba(32,35,31,.18); }}
    .map-route-step {{ width: 32px; height: 32px; display: grid; place-items: center; border: 4px solid var(--danger); border-radius: 50%; background: #fff; color: var(--ink); font-weight: 800; direction: ltr; box-shadow: 0 2px 7px rgba(32,35,31,.22); }}
    .map-route-step.benign {{ border-color: var(--ok); }}
    .map-error {{ position: absolute; inset: 0; display: grid; place-items: center; padding: 24px; background: #f4f6f1; color: var(--muted); text-align: center; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    th, td {{ border-bottom: 1px solid #e8ece3; padding: 7px 8px; vertical-align: top; }}
    th {{ position: sticky; top: 0; background: #f0f4eb; text-align: right; z-index: 1; }}
    tr.mark-suspicious td {{ background: #fff3f0; }}
    tr.mark-benign td {{ background: #f0fbf6; }}
    tr.flash td {{ outline: 2px solid var(--blue); outline-offset: -2px; }}
    .source-grid {{ display: grid; gap: 7px; }}
    .source-row {{ display: grid; grid-template-columns: 105px 1fr 34px; gap: 7px; align-items: center; font-size: 12px; }}
    .source-bar {{ height: 10px; background: var(--soft); border-radius: 3px; overflow: hidden; }}
    .source-fill {{ height: 100%; background: var(--ok); }}
    @media (max-width: 1050px) {{
      header, main {{ padding-left: 16px; padding-right: 16px; }}
      .layout, .detail-grid {{ grid-template-columns: 1fr; }}
      .kpis {{ grid-template-columns: 1fr 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>תצוגת התרחשויות מתוך נתוני גלם</h1>
    <p>במקום להתחיל מטבלת 2,044 אירועים, המסך מציג התרחשויות אפשריות: מה חשוד, מה תמים, ואילו אירועים גולמיים תומכים בכל התרחשות.</p>
    <div class="topline">
      <span class="chip">מזהי אירועים לפי מקור בלבד: PORT / CUST / FIN / TEL / MOVE / SIG</span>
      <span class="chip">אין במזהה רמז אם האירוע חשוד או תמים</span>
      <span class="chip">לחיצה על התרחשות מציגה את הראיות הגולמיות שלה</span>
    </div>
  </header>
  <main>
    <section class="kpis">
      <div class="kpi"><strong id="totalEvents"></strong><span>אירועים גולמיים</span></div>
      <div class="kpi"><strong id="suspiciousEvents"></strong><span>אירועים בשתי התרחשויות חשודות</span></div>
      <div class="kpi"><strong id="benignEvents"></strong><span>אירועים בהתרחשויות תמימות</span></div>
      <div class="kpi"><strong id="signalPercent"></strong><span>אחוז אירועים חשודים</span></div>
    </section>

    <section class="layout">
      <aside class="panel">
        <h2>התרחשויות אפשריות</h2>
        <p>בחר התרחשות כדי לראות את ההשערה, המסלול והאירועים הגולמיים שמרכיבים אותה.</p>
        <div id="storyList" class="story-list"></div>
      </aside>
      <section id="storyDetail" class="panel"></section>
    </section>

    <section class="panel" style="margin-top:16px">
      <h2>חיפוש בטבלת האירועים הגולמית</h2>
      <p>החיפוש מדגים למה סינון מילולי לבד לא מספיק: הוא מחזיר גם אירועים קשורים, גם מסיחים, וגם התרחשויות תמימות.</p>
      <div class="table-toolbar">
        <input id="eventSearch" value="" aria-label="חיפוש אירועים">
        <button id="clearStoryFilter">הצג את כל התוצאות</button>
        <button id="showSelectedStory">הצג רק את ההתרחשות הנבחרת</button>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>מזהה</th><th>זמן</th><th>מקור</th><th>אמינות</th><th>גורם</th><th>מיקום</th><th>תקציר</th></tr></thead>
          <tbody id="eventRows">{rows_preview}</tbody>
        </table>
      </div>
      <div class="map-panel">
        <div class="map-head">
          <div>
            <h3>מפת האירועים המסוננים</h3>
            <p>כל מלבן מציג מיקום וכמות אירועים בסינון הנוכחי; בבחירת התרחשות נוסף מסלול, והמספרים בתוך העיגולים מציינים את סדר התנועה.</p>
          </div>
          <div id="mapStatus" class="map-status"></div>
        </div>
        <div id="eventMap" class="map-canvas"></div>
      </div>
    </section>
  </main>

  <script src="./maplibre-gl.js"></script>
  <script id="data" type="application/json">{data_json}</script>
  <script>
    const data = JSON.parse(document.getElementById('data').textContent);
    const fmt = new Intl.NumberFormat('he-IL');
    const eventsById = Object.fromEntries(data.events.map(e => [e.event_id, e]));
    const suspiciousSet = new Set(data.suspiciousIds);
    const benignSet = new Set(data.benignIds);
    let selectedStory = null;
    let tableMode = 'search';
    const eventSearch = document.getElementById('eventSearch');
    let intelligenceMap = null;
    let mapLoaded = false;
    let pendingMapState = null;
    let countMarkers = [];
    let routeStepMarkers = [];
    const locationMarkerOffsets = {{
      "L-201": [-78, -34],
      "L-208": [76, -38],
      "L-202": [34, 48],
      "L-204": [0, -48],
      "L-205": [-12, 44],
      "L-206": [-82, -38],
      "L-207": [78, -104],
      "L-209": [0, 52],
      "L-203": [82, -34]
    }};

    document.getElementById('totalEvents').textContent = fmt.format(data.summary.total);
    document.getElementById('suspiciousEvents').textContent = fmt.format(data.summary.suspicious_events);
    document.getElementById('benignEvents').textContent = fmt.format(data.summary.benign_story_events);
    document.getElementById('signalPercent').textContent = data.summary.suspicious_percent + '%';

    function storyClass(story) {{
      return story.kind === 'חשוד' ? 'suspicious' : 'benign';
    }}

    function storySearchValue(story) {{
      return [
        story.title.replace(':', ' '),
        story.event_ids.join(' '),
        story.locations.join(' '),
        story.sources.join(' ')
      ].filter(Boolean).join(' ');
    }}

    function showStorySearchValue() {{
      if (!selectedStory) return;
      eventSearch.value = storySearchValue(selectedStory);
    }}

    function showDefaultSearchValue() {{
      eventSearch.value = '';
    }}

    function renderStoryList() {{
      document.getElementById('storyList').innerHTML = data.stories.map(story => `
        <button class="story-button ${{selectedStory && story.id === selectedStory.id ? 'active' : ''}}" data-story="${{story.id}}">
          <div class="story-title">
            <span>${{story.title}}</span>
            <span class="badge ${{storyClass(story)}}">${{story.kind}}</span>
          </div>
          <div>${{story.short}}</div>
          <div class="story-meta">${{story.event_count}} אירועים · ${{story.severity}}</div>
        </button>
      `).join('');
      document.querySelectorAll('[data-story]').forEach(button => {{
        button.addEventListener('click', () => {{
          selectedStory = data.stories.find(story => story.id === button.dataset.story);
          tableMode = 'story';
          showStorySearchValue();
          renderAll();
        }});
      }});
    }}

    function renderRoute(story) {{
      return `<div class="route">${{story.route.map((locId, index) => {{
        const loc = data.locations[locId] || {{ name: locId, type: '' }};
        return `<div class="route-step">
          <div class="route-num">${{index + 1}}</div>
          <div><div class="route-name">${{loc.name}}</div><div class="route-type">${{loc.type}}</div></div>
        </div>`;
      }}).join('')}}</div>`;
    }}

    function renderEvidence(story) {{
      return `<div class="evidence-list">${{story.event_ids.map(id => {{
        const e = eventsById[id];
        if (!e) return '';
        const mark = suspiciousSet.has(id) ? 'suspicious' : benignSet.has(id) ? 'benign' : '';
        return `<div class="evidence ${{mark}}">
          <div><span class="event-id">${{e.event_id}}</span> · ${{e.source_type}} · ${{e.source_reliability}}</div>
          <div class="event-line">${{e.timestamp_utc}} · ${{e.location_name}} · ${{e.entity_or_actor}}</div>
          <div>${{e.event_summary}}</div>
          <button class="jump" data-jump="${{e.event_id}}">הצג בטבלה</button>
        </div>`;
      }}).join('')}}</div>`;
    }}

    function renderStoryDetail() {{
      const selectedButton = document.getElementById('showSelectedStory');
      selectedButton.disabled = !selectedStory;
      if (!selectedStory) {{
        document.getElementById('storyDetail').innerHTML = `
          <div class="empty-detail">
            <div>
              <h2>לא נבחרה התרחשות</h2>
              <p>בחר התרחשות מהרשימה כדי להציג את ההשערה, המסלול והאירועים הגולמיים המקושרים אליה.</p>
            </div>
          </div>
        `;
        return;
      }}
      const cls = storyClass(selectedStory);
      document.getElementById('storyDetail').innerHTML = `
        <div class="detail-grid">
          <div>
            <div class="summary-box ${{cls === 'benign' ? 'benign' : ''}}">
              <h2>${{selectedStory.title}}</h2>
              <p><strong>השערה:</strong> ${{selectedStory.hypothesis}}</p>
              <p><strong>רמת עניין:</strong> ${{selectedStory.severity}} · <strong>אירועים:</strong> ${{selectedStory.event_count}}</p>
              <div class="search-impact">
                <strong>${{fmt.format(selectedStory.keyword_hits)}} אירועים היו מתקבלים בחיפוש מילולי רחב</strong>
                <div class="search-terms">מילות החיפוש: ${{selectedStory.search_keywords.join(' · ')}}</div>
              </div>
            </div>
            <h3>${{selectedStory.kind === 'חשוד' ? 'למה זה חשוד?' : 'למה זה כנראה תמים?'}}</h3>
            <ul class="why-list">${{selectedStory.why.map(item => `<li>${{item}}</li>`).join('')}}</ul>
            <h3 style="margin-top:14px">אירועים גולמיים שמרכיבים את ההתרחשות</h3>
            ${{renderEvidence(selectedStory)}}
          </div>
          <aside>
            <h3>מסלול ההתרחשות</h3>
            ${{renderRoute(selectedStory)}}
            <h3 style="margin-top:16px">מקורות מידע</h3>
            <div class="topline">${{selectedStory.sources.map(source => `<span class="chip">${{source}}</span>`).join('')}}</div>
          </aside>
        </div>
      `;
      document.querySelectorAll('[data-jump]').forEach(button => {{
        button.addEventListener('click', () => {{
          tableMode = 'story';
          showStorySearchValue();
          renderTable(button.dataset.jump);
        }});
      }});
    }}

    function rowClass(e) {{
      if (suspiciousSet.has(e.event_id)) return 'mark-suspicious';
      if (benignSet.has(e.event_id)) return 'mark-benign';
      return '';
    }}

    function tableRow(e, flashId) {{
      const flash = e.event_id === flashId ? ' flash' : '';
      return `<tr id="row-${{e.event_id}}" class="${{rowClass(e)}}${{flash}}">
        <td><span class="event-id">${{e.event_id}}</span></td>
        <td>${{e.timestamp_utc}}</td>
        <td>${{e.source_type}}</td>
        <td>${{e.source_reliability}}</td>
        <td>${{e.entity_or_actor}}</td>
        <td>${{e.location_name}}</td>
        <td>${{e.event_summary}}</td>
      </tr>`;
    }}

    function clearMapMarkers() {{
      countMarkers.forEach(marker => marker.remove());
      routeStepMarkers.forEach(marker => marker.remove());
      countMarkers = [];
      routeStepMarkers = [];
    }}

    function initMap() {{
      if (intelligenceMap || typeof maplibregl === 'undefined') {{
        if (typeof maplibregl === 'undefined') {{
          document.getElementById('eventMap').innerHTML = '<div class="map-error">רכיב המפה לא נטען. ודא שהקבצים maplibre-gl.js ו-maplibre-gl.css נמצאים לצד קובץ ה-HTML.</div>';
        }}
        return;
      }}
      intelligenceMap = new maplibregl.Map({{
        container: 'eventMap',
        style: {{
          version: 8,
          sources: {{
            osm: {{
              type: 'raster',
              tiles: ['https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png'],
              tileSize: 256,
              attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors'
            }}
          }},
          layers: [{{ id: 'osm', type: 'raster', source: 'osm' }}]
        }},
        center: [35.30, 32.68],
        zoom: 8.4,
        minZoom: 7.2,
        maxZoom: 15,
        maxBounds: [[34.72, 32.30], [35.86, 33.08]],
        attributionControl: true
      }});
      intelligenceMap.addControl(new maplibregl.NavigationControl({{ showCompass: false }}), 'top-left');
      intelligenceMap.on('load', () => {{
        mapLoaded = true;
        intelligenceMap.addSource('occurrence-route', {{
          type: 'geojson',
          data: {{ type: 'FeatureCollection', features: [] }}
        }});
        intelligenceMap.addLayer({{
          id: 'occurrence-route-line',
          type: 'line',
          source: 'occurrence-route',
          paint: {{
            'line-color': '#b42318',
            'line-width': 5,
            'line-opacity': 0.86
          }},
          layout: {{
            'line-cap': 'round',
            'line-join': 'round'
          }}
        }});
        if (pendingMapState) applyMapState(pendingMapState.rows, pendingMapState.flashId);
      }});
    }}

    function applyMapState(rows, flashId = null) {{
      if (!mapLoaded) {{
        pendingMapState = {{ rows, flashId }};
        return;
      }}
      const counts = {{}};
      rows.forEach(event => {{
        counts[event.location_id] = (counts[event.location_id] || 0) + 1;
      }});
      const flashLocation = flashId && eventsById[flashId] ? eventsById[flashId].location_id : null;
      const routeIds = tableMode === 'story' && selectedStory ? selectedStory.route : [];
      const routeSet = new Set(routeIds);
      const visibleIds = new Set([
        ...Object.keys(counts).filter(id => counts[id] > 0),
        ...routeIds
      ]);
      clearMapMarkers();
      const bounds = new maplibregl.LngLatBounds();

      visibleIds.forEach(locationId => {{
        const location = data.locations[locationId];
        if (!location) return;
        const count = counts[locationId] || 0;
        const isRoute = routeSet.has(locationId);
        const markerElement = document.createElement('div');
        markerElement.className = `map-count-marker${{isRoute ? ' route' : ''}}${{isRoute && selectedStory.kind === 'תמים' ? ' benign' : ''}}${{tableMode === 'story' && !isRoute ? ' dim' : ''}}${{flashLocation === locationId ? ' focus' : ''}}`;
        markerElement.innerHTML = `<strong>${{count}} אירועים</strong><span>${{location.name}}</span>`;
        countMarkers.push(
          new maplibregl.Marker({{ element: markerElement, anchor: 'center', offset: locationMarkerOffsets[locationId] || [0, -42] }})
            .setLngLat([location.longitude, location.latitude])
            .addTo(intelligenceMap)
        );
        bounds.extend([location.longitude, location.latitude]);
      }});

      const routeCoordinates = routeIds
        .map(locationId => data.locations[locationId])
        .filter(Boolean)
        .map(location => [location.longitude, location.latitude]);
      const routeSource = intelligenceMap.getSource('occurrence-route');
      routeSource.setData({{
        type: 'FeatureCollection',
        features: routeCoordinates.length > 1 ? [{{
          type: 'Feature',
          properties: {{}},
          geometry: {{ type: 'LineString', coordinates: routeCoordinates }}
        }}] : []
      }});
      intelligenceMap.setPaintProperty('occurrence-route-line', 'line-color', selectedStory?.kind === 'תמים' ? '#16725f' : '#b42318');

      routeIds.forEach((locationId, index) => {{
        const location = data.locations[locationId];
        if (!location) return;
        const stepElement = document.createElement('div');
        stepElement.className = `map-route-step${{selectedStory.kind === 'תמים' ? ' benign' : ''}}`;
        stepElement.textContent = String(index + 1);
        routeStepMarkers.push(
          new maplibregl.Marker({{ element: stepElement, anchor: 'center' }})
            .setLngLat([location.longitude, location.latitude])
            .addTo(intelligenceMap)
        );
      }});

      if (!bounds.isEmpty()) {{
        intelligenceMap.fitBounds(bounds, {{
          padding: {{ top: 190, right: 155, bottom: 180, left: 155 }},
          maxZoom: 9.8,
          duration: 500
        }});
      }}
    }}

    function renderMap(rows, flashId = null) {{
      document.getElementById('mapStatus').textContent = tableMode === 'story'
        ? `${{selectedStory.title}} · ${{rows.length}} אירועים`
        : `${{rows.length}} אירועים בסינון הנוכחי`;
      pendingMapState = {{ rows, flashId }};
      initMap();
      applyMapState(rows, flashId);
    }}

    function renderTable(flashId = null) {{
      let rows;
      if (tableMode === 'story' && selectedStory) {{
        const ids = new Set(selectedStory.event_ids);
        rows = data.events.filter(e => ids.has(e.event_id));
      }} else {{
        const terms = eventSearch.value.split(/\\s+/).filter(Boolean);
        rows = data.events.filter(e => terms.length === 0 || terms.some(t => (e.event_summary + ' ' + e.entity_or_actor + ' ' + e.event_id).includes(t)));
      }}
      document.getElementById('eventRows').innerHTML = rows.map(e => tableRow(e, flashId)).join('');
      renderMap(rows, flashId);
      if (flashId) {{
        const row = document.getElementById(`row-${{flashId}}`);
        row?.scrollIntoView({{ block: 'center', behavior: 'smooth' }});
      }}
    }}

    function renderSources() {{
      const entries = Object.entries(data.sourceCounts).sort((a,b) => b[1] - a[1]).slice(0, 12);
      const max = Math.max(...entries.map(x => x[1]));
      return `<div class="source-grid">${{entries.map(([name, value]) => `
        <div class="source-row">
          <span>${{name}}</span>
          <span class="source-bar"><span class="source-fill" style="display:block;width:${{value / max * 100}}%"></span></span>
          <span>${{value}}</span>
        </div>`).join('')}}</div>`;
    }}

    eventSearch.addEventListener('input', () => {{ tableMode = 'search'; renderTable(); }});
    document.getElementById('clearStoryFilter').addEventListener('click', () => {{ tableMode = 'search'; showDefaultSearchValue(); renderTable(); }});
    document.getElementById('showSelectedStory').addEventListener('click', () => {{
      if (!selectedStory) return;
      tableMode = 'story';
      showStorySearchValue();
      renderTable();
    }});

    function renderAll() {{
      renderStoryList();
      renderStoryDetail();
      renderTable();
    }}
    renderAll();
  </script>
</body>
</html>
"""
    OUT.write_text(html_text, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
