#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

DATASET_VARIANTS = [
    {
        "name": "v1",
        "events": ROOT / "data" / "serbia_kosovo_events_projection.csv",
        "events_en": ROOT / "data" / "serbia_kosovo_events_projection.en.csv",
        "locations": ROOT / "data" / "serbia_kosovo_locations.json",
        "locations_en": ROOT / "data" / "serbia_kosovo_locations.en.json",
        "entities": ROOT / "data" / "serbia_kosovo_entities.json",
        "entities_en": ROOT / "data" / "serbia_kosovo_entities.en.json",
    },
    {
        "name": "v2",
        "events": ROOT / "data" / "serbian_intelligence_v2" / "serbia_kosovo_events_projection_v2.csv",
        "events_en": ROOT / "data" / "serbian_intelligence_v2" / "serbia_kosovo_events_projection_v2.en.csv",
        "locations": ROOT / "data" / "serbian_intelligence_v2" / "serbia_kosovo_locations_v2.json",
        "locations_en": ROOT / "data" / "serbian_intelligence_v2" / "serbia_kosovo_locations_v2.en.json",
        "entities": ROOT / "data" / "serbian_intelligence_v2" / "serbia_kosovo_entities_v2.json",
        "entities_en": ROOT / "data" / "serbian_intelligence_v2" / "serbia_kosovo_entities_v2.en.json",
    },
    {
        "name": "v2.1",
        "events": ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_events_projection_v2_1.csv",
        "events_en": ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_events_projection_v2_1.en.csv",
        "locations": ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_locations_v2_1.json",
        "locations_en": ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_locations_v2_1.en.json",
        "entities": ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_entities_v2_1.json",
        "entities_en": ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_entities_v2_1.en.json",
    },
]

RECORDED_RUNS_VARIANTS = [
    (ROOT / "recorded_runs", ROOT / "recorded_runs_en"),
    (ROOT / "recorded_runs" / "v2", ROOT / "recorded_runs_en" / "v2"),
    (ROOT / "recorded_runs" / "v2.1", ROOT / "recorded_runs_en" / "v2.1"),
]


EXACT_TEXT_MAP = {
    "לא מסווגה": "Unrated",
    "נמוכה": "Low",
    "בינונית": "Medium",
    "גבוהה": "High",
    "חדשות מקומיות": "Local news",
    "טלגרם": "Telegram",
    "טיקטוק": "TikTok",
    "שמועה מקומית": "Local rumor",
    "קבוצת וואטסאפ": "WhatsApp group",
    "הודעת דובר": "Spokesperson statement",
    "בלוג פוליטי": "Political blog",
    "פייסבוק": "Facebook",
    "ערוץ חדשות בינלאומי": "International news channel",
    "גורם מדווח": "Reporting actor",
    "מוקד ליבה": "Core hotspot",
    "ציר": "Route",
    "מוקד ביטחוני": "Security hotspot",
    "כפר/יישוב": "Village/locality",
    "אזרחי/חירום": "Civil/emergency",
    "אזרחי/ציבורי": "Civil/public",
    "מדיני": "Governmental",
    "שטח": "Terrain",
    "מוסד מדיני": "State institution",
    "צד סרבי": "Serbian side",
    "רעש/רקע": "Noise/background",
    "כפר/ציר": "Village/route",
    "כפר/שטח": "Village/terrain",
    "אזרחי": "Civilian",
    "קוסובו": "Kosovo",
    "צפון קוסובו": "North Kosovo",
    "צפון מיטרוביצה": "North Mitrovica",
    "זבצ׳אן": "Zvečan",
    "לפוסאביץ׳": "Leposavić",
    "זובין פוטוק": "Zubin Potok",
    "פרישטינה": "Pristina",
    "ראסקה": "Raška",
    "נובי פאזאר": "Novi Pazar",
    "בלגרד": "Belgrade",
    "טירנה": "Tirana",
    "זגרב": "Zagreb",
    "בריסל": "Brussels",
    "פק": "Peć",
    "פריזרן": "Prizren",
    "משטרת קוסובו": "Kosovo Police",
    "יחידה מיוחדת של משטרת קוסובו": "Kosovo Police Special Unit",
    "צבא סרביה": "Serbian Army",
    "מפגינים סרבים מקומיים": "Local Serbian protesters",
    "תושבים מקומיים": "Local residents",
    "כתבים מקומיים": "Local journalists",
    "ממשלת קוסובו": "Government of Kosovo",
    "משרד ההגנה של סרביה": "Serbian Ministry of Defence",
    "נאט״ו": "NATO",
    "לא סווגה": "Unrated",
    "נמוכה": "Low",
    "בינונית": "Medium",
    "גבוהה": "High",
    "חדשות מקומיות": "Local news",
    "טלגרם": "Telegram",
    "טיקטוק": "TikTok",
    "שמועה מקומית": "Local rumor",
    "קבוצת וואטסאפ": "WhatsApp group",
    "הודעת דובר": "Spokesperson statement",
    "בלוג פוליטי": "Political blog",
    "פייסבוק": "Facebook",
    "ערוץ חדשות בינלאומי": "International news channel",
    "גורם מדווח": "Reporting actor",
    "מוקד ליבה": "Core hotspot",
    "ציר": "Route",
    "מוקד ביטחוני": "Security hotspot",
    "כפר/יישוב": "Village/locality",
    "אזרחי/חירום": "Civil/emergency",
    "אזרחי/ציבורי": "Civil/public",
    "מדיני": "Governmental",
    "שטח": "Terrain",
    "מוסד מדיני": "State institution",
    "צד סרבי": "Serbian side",
    "רעש/רקע": "Noise/background",
    "כפר/ציר": "Village/route",
    "כפר/שטח": "Village/terrain",
    "אזרחי": "Civilian",
    "קוסובו": "Kosovo",
    "צפון קוסובו": "North Kosovo",
    "צפון מיטרוביצה": "North Mitrovica",
    "זבצ׳אן": "Zvečan",
    "לפוסאביץ׳": "Leposavić",
    "זובין פוטוק": "Zubin Potok",
    "פרישטינה": "Pristina",
    "ראשקה": "Raška",
    "נובי פאזאר": "Novi Pazar",
    "בלגרד": "Belgrade",
    "טירנה": "Tirana",
    "זגרב": "Zagreb",
    "בריסל": "Brussels",
    "פק": "Peć",
    "פריזרן": "Prizren",
    "משטרת קוסובו": "Kosovo Police",
    "יחידה מיוחדת של משטרת קוסובו": "Kosovo Police Special Unit",
    "צבא סרביה": "Serbian Army",
    "מפגינים סרבים מקומיים": "Local Serbian protesters",
    "תושבים מקומיים": "Local residents",
    "כתבים מקומיים": "Local journalists",
    "ממשלת קוסובו": "Government of Kosovo",
    "משרד ההגנה של סרביה": "Serbian Ministry of Defence",
    "נאט״ו": "NATO",
}

PHRASE_REPLACEMENTS = [
    ("KFOR", "KFOR"),
    ("EULEX", "EULEX"),
    ("KSF", "KSF"),
    ("דיווח ממקור גלוי מתאר פעילות של ", "A public-source report describes activity by "),
    ("תושבים דיווחו על נוכחות ", "Residents reported the presence of "),
    ("מספר פרסומים מצביעים על תנועה של ", "Several publications point to movement by "),
    ("במרחב ", "in the area "),
    ("ליד ", "near "),
    ("במסגרת '", "as part of '"),
    ("נדרש אימות נוסף.", "Additional verification is required."),
    ("חלק מהחשבונות משתמשים באותו ניסוח.", "Some accounts use the same wording."),
    ("קיימת אי-ודאות לגבי הכמות והיעד.", "There is uncertainty regarding the quantity and destination."),
    ("משרד הפנים של קוסובו", "Kosovo Interior Ministry"),
    ("היחידה הרב-לאומית המיוחדת של KFOR", "KFOR Multinational Specialized Unit"),
    ("כוח סרבי", "Serbian force"),
    ("כוחות גדולים", "large forces"),
    ("חצו את הגבול", "crossed the border"),
    ("הלילה", "overnight"),
    ("מקור מפלגתי טוען שהאירוע הוא מתקפה מתוכננת מראש", "A partisan source claims the incident is a pre-planned attack"),
    ("העירייה המקומית מבקשת מהתושבים להימנע מהתקהלויות גדולות", "The local municipality asks residents to avoid large gatherings"),
    ("קבוצת הורים מקומית מדווחת על ביטול לימודים זמני בבית ספר סמוך", "A local parents' group reports a temporary suspension of classes at a nearby school"),
    ("תושבים מדווחים על ירידה בתנועת אוטובוסים באזור", "Residents report reduced bus traffic in the area"),
    ("חברת הסעות מקומית הודיעה על ביטול חלק מהקווים באזור הצפון", "A local transport company announced the cancellation of some routes in the northern area"),
    ("כתבים מקומיים מדווחים על סתירות בין גרסאות הצדדים לגבי מקור הירי", "Local reporters describe contradictions between the sides' accounts regarding the source of the gunfire"),
    ("נהגים מתבקשים לא להסתמך על דיווחי רשת לא מאומתים לגבי סגירת כבישים", "Drivers are asked not to rely on unverified online reports about road closures"),
    ("ערוץ סרבי מדגיש את מצוקת התושבים הסרבים באזור, בעוד ערוץ קוסוברי מדגיש את הצורך באכיפת חוק", "A Serbian channel emphasizes the distress of Serbian residents in the area, while a Kosovar channel emphasizes the need for law enforcement"),
    ("ציר הכניסה לעיירה פתוח, אך תושבים מדווחים על בדיקות ממושכות", "The access route into the town is open, but residents report lengthy inspections"),
    ("דובר רשמי מסר כי הפעילות נועדה לשמור על הסדר הציבורי ולא לפגוע באוכלוסייה אזרחית", "An official spokesperson said the activity is intended to maintain public order and not harm the civilian population"),
    ("מקור חדשותי מתקן דיווח קודם ומבהיר שלא הייתה חציית גבול מאומתת", "A news source corrects an earlier report and clarifies that there was no verified border crossing"),
    ("מקורות בינלאומיים קוראים לכל הצדדים להימנע מהסלמה ולשתף פעולה עם KFOR", "International sources call on all sides to avoid escalation and cooperate with KFOR"),
    ("דיווח תקשורתי טוען כי KFOR הגביר את הנוכחות כדי למנוע חיכוך ישיר", "A media report claims that KFOR increased its presence to prevent direct friction"),
    ("פרשנים מזהירים שהפצת סרטונים חלקיים עלולה להחריף את המצב", "Commentators warn that the spread of partial videos may worsen the situation"),
    ("צוות רפואי התבקש להישאר בכוננות עד להודעה חדשה", "A medical team was asked to remain on standby until further notice"),
    ("הופצו שמועות על מספר גבוה של נפגעים, אך בית החולים אישר רק מספר מצומצם", "Rumors circulated about a high number of casualties, but the hospital confirmed only a limited number"),
    ("מקור מקומי טוען שהפצועים מאירוע הלילה אינם במצב קשה", "A local source claims that those injured in the overnight incident are not in serious condition"),
    ("בית החולים האזורי קיבל מספר פצועים קל מאירועי דחיפות והפרות סדר", "The regional hospital received several lightly injured people from scuffles and public-order disturbances"),
    ("תושבים מתלוננים שהמצב הביטחוני פוגע בשגרה יותר מהאירוע עצמו", "Residents complain that the security situation is disrupting daily routine more than the incident itself"),
    ("דיון חירום מתקיים בעקבות דיווחים על עימותים בצפון", "An emergency discussion is taking place בעקבות reports of clashes in the north"),
    ("נציגים בינלאומיים קוראים להפחתת מתיחות ולחזרה לדיאלוג", "International representatives call for reducing tensions and returning to dialogue"),
    ("גורם אירופי מזהיר מפני צעדים חד־צדדיים שיחמירו את המצב", "A European official warns against unilateral steps that could worsen the situation"),
    ("מוקד חירום מקומי מבקש מהתושבים לא לדווח שוב ושוב על אותו אירוע", "A local emergency center asks residents not to report the same incident repeatedly"),
    ("שוק מקומי פעל חלקית בלבד בגלל היעדר ספקים", "A local market operated only partially because suppliers were absent"),
    ("הודעה אזרחית מזכירה לתושבים שהשימוש במטבע ובשירותים פיננסיים נמצא במוקד מחלוקת", "A civic notice reminds residents that the use of currency and financial services remains disputed"),
    ("בעלי חנויות חוששים מנזק אם המחאות יתקרבו למרכז המסחרי", "Shop owners fear damage if protests move closer to the commercial center"),
    ("הודעה רשמית מדגישה שאין שינוי במנדט KFOR באזור", "An official notice emphasizes that there is no change in KFOR's mandate in the area"),
    ("ממשלת קוסובו טוענת שהפעולות מתבצעות במסגרת אכיפת חוק וריבונות", "The Government of Kosovo says the actions are being carried out under law enforcement and sovereignty authorities"),
    ("משפחות מקומיות מנסות למשוך מזומן בגלל שמועות על סגירת בנקים", "Local families are trying to withdraw cash because of rumors about bank closures"),
    ("משרד ממשלתי בסרביה דוחה טענות על מעורבות ישירה באירועים", "A Serbian government ministry rejects claims of direct involvement in the events"),
    ("פוסט ויראלי מייחס ירי לממשלת סרביה, אך סרטונים אחרים מאותו אזור מצביעים על רעש אזרחי בלבד", "A viral post attributes gunfire to the Serbian government, but other videos from the same area point only to civilian noise"),
    ("גורמים בבלגרד קוראים ל־KFOR להבטיח את ביטחון התושבים הסרבים", "Officials in Belgrade call on KFOR to guarantee the security of Serbian residents"),
    ("בפרישטינה אומרים שהמשבר נובע מהתנגדות מאורגנת לאכיפת חוק", "Officials in Pristina say the crisis stems from organized resistance to law enforcement"),
    ("מספר עובדים לא הגיעו לעבודה בגלל חסימות וחשש מנסיעה", "Several workers did not report to work because of blockages and concern about travel"),
    ("תושבים מדווחים על עלייה זמנית במחירי מוצרי יסוד בחנויות קטנות", "Residents report a temporary rise in basic-goods prices in small shops"),
    ("הסרטון שמופץ עכשיו לא נראה מהיום", "The video being circulated now does not appear to be from today"),
    ("המשפחה שלי החליטה לא לשלוח את הילדים לבית הספר מחר בגלל המצב", "My family decided not to send the children to school tomorrow because of the situation"),
    ("תמונה של שיירה מוצגת ככוח סרבי, אך משתמשים אחרים טוענים שמדובר ב־KFOR או במשטרה", "A photo of a convoy is presented as a Serbian force, but other users claim it is KFOR or the police"),
    ("שמועה בקבוצות מקומיות טוענת שיש רשימת מעצרים חדשה", "A rumor in local groups claims there is a new arrest list"),
    ("דיווח דרמטי טוען שכוחות גדולים חצו את הגבול הלילה", "A dramatic report claims that large forces crossed the border overnight"),
    ("יש דיווחים על הפסקת חשמל קצרה באזור", "There are reports of a brief power outage in the area"),
    ("לא ברור אם מדובר בתקלה רגילה", "It is unclear whether this was a routine malfunction"),
    ("דיווח על כלי טיס בלתי מזוהה מעל אזור", "Report of an unidentified aircraft above the area of"),
    ("אין אישור אם מדובר ברחפן, מסוק או רעש אזרחי", "There is no confirmation whether it was a drone, a helicopter, or civilian noise"),
    ("דובר רשמי מסר כי הפעילות נועדה לשמור על הסדר הציבורי ולא לפגוע באוכלוסייה אזרחית", "An official spokesperson said the activity is intended to preserve public order and not harm civilians"),
    ("להימנע מהסלמה", "avoid escalation"),
    ("ולשתף פעולה עם", "and cooperate with"),
    ("לא מאומתים", "unverified"),
    ("לא מאומתת", "unverified"),
    ("לא ברור", "it is unclear"),
    ("מדובר", "this concerns"),
    ("בית הספר", "the school"),
    ("בגלל המצב", "because of the situation"),
    ("באזור", "in the area"),
    ("הצפון", "the north"),
    ("ירי", "gunfire"),
    ("חסימות", "blockages"),
]

LOCATION_PATTERNS = [
    (re.compile(r"^כפר סמוך (\d+)$"), lambda m: f"Nearby village {m.group(1)}"),
    (re.compile(r"^תחנת דלק (\d+)$"), lambda m: f"Gas station {m.group(1)}"),
    (re.compile(r"^נקודת בידוק כללית (\d+)$"), lambda m: f"General checkpoint {m.group(1)}"),
    (re.compile(r"^אזור תעשייה קטן (\d+)$"), lambda m: f"Small industrial area {m.group(1)}"),
    (re.compile(r"^ציר גישה (\d+)$"), lambda m: f"Access route {m.group(1)}"),
    (re.compile(r"^בית ספר (\d+)$"), lambda m: f"School {m.group(1)}"),
    (re.compile(r"^כיכר מרכזית (\d+)$"), lambda m: f"Central square {m.group(1)}"),
    (re.compile(r"^צומת מקומי (\d+)$"), lambda m: f"Local junction {m.group(1)}"),
    (re.compile(r"^מרכז בריאות (\d+)$"), lambda m: f"Health center {m.group(1)}"),
    (re.compile(r"^אזור מיוער (\d+)$"), lambda m: f"Wooded area {m.group(1)}"),
]


def translate_plain(text: str) -> str:
    value = str(text or "").strip()
    if not value:
        return value
    if value in EXACT_TEXT_MAP:
        return EXACT_TEXT_MAP[value]
    for pattern, repl in LOCATION_PATTERNS:
        match = pattern.fullmatch(value)
        if match:
            return repl(match)
    translated = value
    for he, en in sorted(PHRASE_REPLACEMENTS, key=lambda item: len(item[0]), reverse=True):
        translated = translated.replace(he, en)
    translated = translated.replace("־", "-").replace("״", "\"").replace("׳", "'")
    translated = re.sub(r"\s+", " ", translated).strip()
    return translated


def translate_location_name(name: str) -> str:
    direct = {
        "אזור גשר איבר": "Ibar Bridge area",
        "מבנה העירייה": "Municipal building",
        "אזור מבנה העירייה": "Municipal building area",
        "הכביש לצפון מיטרוביצה": "Road to North Mitrovica",
        "מרכז העיירה": "Town center",
        "הציר לכיוון סרביה": "Route toward Serbia",
        "אזור כפרי מערבי": "Western rural area",
        "הדרך לאגם גזיבודה": "Road to Lake Gazivoda",
        "תחנת משטרה אזורית": "Regional police station",
        "צומת כניסה לעיירה": "Town entrance junction",
        "כביש כפרי צפוני": "Northern rural road",
        "אזור מיוער סמוך לכפר": "Wooded area near the village",
        "משרד הפנים": "Interior Ministry",
        "מטה ממשלת קוסובו": "Government of Kosovo headquarters",
        "אזור כללי סמוך לגבול": "General area near the border",
        "מרכז עירוני": "Urban center",
        "משרד ממשלתי": "Government office",
        "בית חולים אזורי": "Regional hospital",
        "תחנת דלק מרכזית": "Central gas station",
        "בית ספר סרבי מקומי": "Local Serbian school",
        "משרד ההגנה האלבני": "Albanian Ministry of Defence",
        "מטה נאט״ו": "NATO headquarters",
    }
    return direct.get(name) or translate_plain(name)


def translate_recorded_text(text: str) -> str:
    value = str(text or "")
    value = translate_plain(value)
    value = value.replace("מזהי ראיות", "Evidence IDs")
    value = value.replace("תוצאה אגרגטיבית ללא מזהי אירועים", "Aggregate result without event IDs")
    value = value.replace("אין התאמות", "No matches")
    value = value.replace("כן:", "Yes:")
    value = value.replace("לא:", "No:")
    return value


def project_locations(src: Path, dst: Path) -> None:
    data = json.loads(src.read_text(encoding="utf-8"))
    projected: dict[str, Any] = {}
    for location_id, item in data.items():
        projected[location_id] = {
            **item,
            "name": translate_location_name(item.get("name", "")),
            "type": translate_plain(item.get("type", "")),
            "country": translate_plain(item.get("country", "")),
            "region": translate_plain(item.get("region", "")),
            "municipality": translate_plain(item.get("municipality", "")),
            "locality": translate_plain(item.get("locality", "")),
        }
    dst.write_text(json.dumps(projected, ensure_ascii=False, indent=2), encoding="utf-8")


def project_entities(src: Path, dst: Path) -> None:
    data = json.loads(src.read_text(encoding="utf-8"))
    projected = []
    for item in data:
        projected.append({
            **item,
            "canonical_name": translate_plain(item.get("canonical_name", "")),
            "aliases": [translate_plain(alias) for alias in (item.get("aliases") or [])],
            "entity_type": translate_plain(item.get("entity_type", "")),
        })
    dst.write_text(json.dumps(projected, ensure_ascii=False, indent=2), encoding="utf-8")


def project_events(src: Path, dst: Path, locations_src: Path) -> None:
    locations = json.loads(locations_src.read_text(encoding="utf-8"))
    translated_location_names = {key: translate_location_name(value.get("name", "")) for key, value in locations.items()}
    with src.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys()) if rows else []
    for row in rows:
        row["source_type"] = translate_plain(row.get("source_type", ""))
        row["source_reliability"] = translate_plain(row.get("source_reliability", ""))
        row["certainty_level"] = translate_plain(row.get("certainty_level", ""))
        summary = translate_plain(row.get("event_summary", ""))
        location_id = row.get("location_id", "")
        if location_id in translated_location_names:
            summary = summary.replace(location_id, location_id)
            for original in {locations[location_id].get("name", ""), locations[location_id].get("locality", ""), locations[location_id].get("municipality", "")}:
                if original:
                    summary = summary.replace(original, translate_plain(original))
        row["event_summary"] = summary
    with dst.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def project_recorded_runs(src_dir: Path, dst_dir: Path) -> None:
    if not src_dir.exists():
        return
    dst_dir.mkdir(parents=True, exist_ok=True)
    for path in src_dir.glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        projected = json.loads(json.dumps(payload, ensure_ascii=False))
        if projected.get("question"):
            projected["question"] = translate_recorded_text(projected["question"])
        result = projected.get("result") or {}
        if result.get("answer"):
            result["answer"] = translate_recorded_text(result["answer"])
        if result.get("view_reason"):
            result["view_reason"] = translate_recorded_text(result["view_reason"])
        projected["result"] = result
        (dst_dir / path.name).write_text(json.dumps(projected, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    for variant in DATASET_VARIANTS:
        project_locations(variant["locations"], variant["locations_en"])
        project_entities(variant["entities"], variant["entities_en"])
        project_events(variant["events"], variant["events_en"], variant["locations"])
        print(f"Projected dataset: {variant['name']}")
    for src, dst in RECORDED_RUNS_VARIANTS:
        project_recorded_runs(src, dst)
        if src.exists():
            print(f"Projected recorded runs: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
