# VM Semantic Quality Comparison - Q1-Q8

Date: 2026-07-04

| ID | Status | Assessment | Time | View | Steps | First Tool | Semantic | Evidence IDs | Notes |
|---|---|---|---:|---|---:|---|---|---:|---|
| `fq_01_hotspots` | completed | pass | 79.5s | map | 12 | `classify_question_intent` | False | 0 | מוקדי החיכוך העיקריים בצפון קוסובו לפי ספירת אירועים הם: צפון מיטרוביצה 2,947; זבצ׳אן 2,518; לפוסאביץ׳ 2,420; זובין פוטוק 1,898.   המוקדים המדויקים הבולטים: בצפון מיטרובי... |
| `fq_02_force_movement` | completed | pass_quality_slow | 303.7s | map | 25 | `classify_question_intent` | True | 8 | כן, יש אינדיקציה לדפוס בזמן ובמרחב, אבל הוא חזק יותר כדפוס של ריבוי דיווחים ונוכחות ביטחונית מאשר כשרשרת תפעולית אחת מוכחת: ספירת מונחי כוחות/נוכחות/שיירה/מחסום עולה בחדו... |
| `fq_03_international_actor_role` | completed | pass | 174.7s | evidence | 21 | `classify_question_intent` | True | 7 | הגורם הבינלאומי הבולט הוא KFOR: הוא מופיע ב-637 דיווחים, והראיות התפעוליות מצביעות בעיקר על נוכחות מייצבת/חוצצת סביב צירים וצמתים, לא על פעולה התקפית. בפועל הדיווחים מתאר... |
| `fq_04_tactical_event_zvecan` | completed | pass_strong | 222.4s | timeline | 15 | `classify_question_intent` | True | 21 | בבדיקה הממצה סביב מוקדי זבצ׳אן נמצאו 1078 רשומות רלוונטיות ללא קיטוע; בציר הליבה סביב אזור מבנה העירייה, הכביש לצפון מיטרוביצה וצומת הכניסה נמצאו 132 רשומות, ומהן הרצף נר... |
| `fq_05_escalation_assessment` | completed | pass_manual_reconstructed | 252.1s | map | 17 | `classify_question_intent` | True | 14 | הממצא נוטה לדפוס רחב יותר מאכיפה נקודתית: נמצאו 69 דיווחים לא מקוצצים על צפון קוסובו במשך 14–19 בספטמבר, בארבע רשויות — לפוסאביץ׳, זבצ׳אן, צפון מיטרוביצה וזובין פוטוק — ע... |
| `fq_06_violence_noise_general` | completed | pass_clean | 173.7s | evidence | 19 | `classify_question_intent` | False | 9 | נמצאו 1,387 דיווחי ירי/פיצוץ, אבל התמונה נוטה יותר לגל רעש מידע עם כמה אירועים נקודתיים אפשריים: יש מאות מופעים של הסברים אזרחיים כמו זיקוקים/תקלה 294 ושל סרטונים “לא מהי... |
| `fq_07_geographic_deception` | completed | pass_clean | 145.6s | map | 12 | `classify_question_intent` | False | 8 | כן — יש חשד משמעותי לפיזור/הטעיה גאוגרפית, אבל לא הוכחה שאותו קובץ וידאו ממש הועתק: נמצאה תבנית חוזרת “הסרטון שמופץ עכשיו לא נראה מהיום” ב-323 אירועים, 134 מיקומים ו-10 ס... |
| `fq_08_first_event_by_hotspot` | completed | pass_clean | 99.5s | timeline | 4 | `classify_question_intent` | False | 15 | מוקדי החיכוך העיקריים בצפון קוסובו נבחרו לפי ספירת אירועי חיכוך והם מסודרים כאן לפי זמן האירוע הראשון בכל מוקד: LOC-036 כיכר מרכזית 16 — 45, 2026-09-12 07:42; LOC-001 אזו... |

## Summary

- Completed all 8 full-investigation quality questions on the VM.
- All accepted artifacts start with `classify_question_intent`.
- `fq_05` is reconstructed from manual UI run `run_c6a8d4a8412b490caec13fd4d0bb8835` plus Hermes output, MCP audit, and performance logs.
- `fq_02` remains the slowest accepted run at about 304 seconds.
- New q6-q8 clean runs completed successfully: q6 about 174 seconds, q7 about 146 seconds, q8 about 99 seconds.

## Next Test Phase

Review the Q1-Q8 comparison against the ideal criteria and decide which quality gaps require code/prompt changes. The main candidates are performance reduction and any answer-quality gaps found by manual review.
