# Semantic Tool Gold Reference V1

Purpose: judge whether current lexical/TF-IDF semantic retrieval is good enough before implementing real embeddings.

This reference uses visible fields only, not hidden evaluator labels.

## Score Against Current Tool Run

| Probe | Recall must-find | High-value top10/top20 | Bad priority | Assessment |
|---|---:|---:|---|---|
| `tp_01_semantic_zvecan_shooting_paraphrase` | 16/16 (1.0) | 2/3 | REC-039674, REC-034783, REC-090709 | Mixed: good recall, weak ranking; generic road-closure items outrank direct shooting/noise evidence. |
| `tp_02_semantic_kfor_role` | 18/18 (1.0) | 5/6 | - | Adequate recall but ranking drops quickly into generic/noisy KFOR mentions. |
| `tp_03_semantic_geographic_deception` | 24/24 (1.0) | 7/8 | - | Strong: good recall and high-value evidence ranks well. |
| `tp_04_compare_location_claims` | 4/4 templates | ranks {'הסרטון שמופץ עכשיו לא נראה מהיום. שימו לב לפני שמשתפים.': 1, 'תמונה של שיירה מוצגת ככוח סרבי, אך משתמשים אחרים טוענים שמדובר ב־kfor או במשטרה.': 2, 'סרטון שמופץ ברשת מוצג כאילו צולם באזור <מיקום>, אך יש טענות שהוא ישן ואינו קשור לאירועים הנוכחיים.': 3, 'דיווח דרמטי טוען שכוחות גדולים חצו את הגבול הלילה. נכון לעכשיו אין לכך אימות, ומקורות אחרים מכחישים.': 4} | - | Strong: required conflict groups are present and highly ranked. |

## Decision Signal

- Current semantic retrieval is good enough for geographic-deception style evidence (`tp_03`) and the dedicated comparison tool (`tp_04`).
- Current semantic retrieval is not clearly good enough for nuanced tactical/noise and KFOR-role ranking (`tp_01`, `tp_02`): recall exists, but top ranking includes generic/noisy items above more direct evidence.
- This supports implementing real embeddings as an A/B backend for `semantic_search_events`, while keeping lexical fallback and reusing this gold set for scoring.

## Required Re-Test After Embeddings

Run the same probes and compare top10/top20/top50 recall and bad-priority hits against this file. Success means improved high-value top10/top20 without losing current recall.
