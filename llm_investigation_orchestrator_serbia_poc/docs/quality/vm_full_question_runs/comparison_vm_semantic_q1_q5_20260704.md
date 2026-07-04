# VM Semantic Quality Comparison - Q1-Q5 Integrated

Date: 2026-07-04

| ID | Status | Time | View | Steps | First Tool | Semantic | Notes |
|---|---|---:|---|---:|---|---|---|
| `fq_01_hotspots` | completed | 79.5s | map | 12 | `classify_question_intent` | False | מוקדי החיכוך העיקריים בצפון קוסובו לפי ספירת אירועים הם: צפון מיטרוביצה 2,947; זבצ׳אן 2,518; לפוסאביץ׳ 2,420; זובין פוטוק 1,898.   המוקדים המדויקים הבולטים: בצפון מיטרוביצה — LOC-0... |
| `fq_02_force_movement` | completed | 303.7s | map | 25 | `classify_question_intent` | True | כן, יש אינדיקציה לדפוס בזמן ובמרחב, אבל הוא חזק יותר כדפוס של ריבוי דיווחים ונוכחות ביטחונית מאשר כשרשרת תפעולית אחת מוכחת: ספירת מונחי כוחות/נוכחות/שיירה/מחסום עולה בחדות מ-14 עד ... |
| `fq_03_international_actor_role` | completed | 174.7s | evidence | 21 | `classify_question_intent` | True | הגורם הבינלאומי הבולט הוא KFOR: הוא מופיע ב-637 דיווחים, והראיות התפעוליות מצביעות בעיקר על נוכחות מייצבת/חוצצת סביב צירים וצמתים, לא על פעולה התקפית. בפועל הדיווחים מתארים קריאות ... |
| `fq_04_tactical_event_zvecan` | completed | 222.4s | timeline | 15 | `classify_question_intent` | True | בבדיקה הממצה סביב מוקדי זבצ׳אן נמצאו 1078 רשומות רלוונטיות ללא קיטוע; בציר הליבה סביב אזור מבנה העירייה, הכביש לצפון מיטרוביצה וצומת הכניסה נמצאו 132 רשומות, ומהן הרצף נראה כך: תחי... |
| `fq_05_escalation_assessment` | completed | 252.1s | map | 17 | `classify_question_intent` | True | הממצא נוטה לדפוס רחב יותר מאכיפה נקודתית: נמצאו 69 דיווחים לא מקוצצים על צפון קוסובו במשך 14–19 בספטמבר, בארבע רשויות — לפוסאביץ׳, זבצ׳אן, צפון מיטרוביצה וזובין פוטוק — עם שיא ב-16... |
| `fq_06_violence_noise_general` | missing | - | - | - | - | - | Needs clean VM run |
| `fq_07_geographic_deception` | missing | - | - | - | - | - | Needs clean VM run |
| `fq_08_first_event_by_hotspot` | missing | - | - | - | - | - | Needs clean VM run |

## Current Coverage

- Cleanly integrated: `fq_01` through `fq_05`.
- `fq_05` is reconstructed from manual UI run `run_c6a8d4a8412b490caec13fd4d0bb8835` plus MCP audit and performance logs.
- Still pending clean VM runs: `fq_06_violence_noise_general`, `fq_07_geographic_deception`, `fq_08_first_event_by_hotspot`.

## Next Step

Run `fq_06_violence_noise_general` again as a clean one-by-one run. Accept it only if the first step is `classify_question_intent`; then continue to `fq_07` and `fq_08`.
