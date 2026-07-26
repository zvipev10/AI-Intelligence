# UX Review — Indications in the Workstream

## Status

AI-authored recommendation — pending human UX approval.

## UX principle

Do not expose an artifact name, management panel, or new navigation concept. The user sees indications, what they may mean, and the next available action through chat. The minimal active-workstream indicator remains unchanged.

## Manual MVP flow

1. The user presses the active-workstream indicator.
2. The agent-style message summarizes how many indications are saved, their support/contradiction balance, gaps, and current responsibility.
3. If no indications exist, the message says so and offers `הוסף אינדיקציות מהשכבה`.
4. The action asks the user to type one or more `REC-...` identifiers in chat.
5. The user sends a message such as `REC-V2-000142, REC-V2-000207`.
6. The system validates the identifiers against the explicitly attached event layer.
7. Chat shows a preview listing the resolved records and asks `לשמור את האינדיקציות במעקב?`.
8. On confirmation, the references persist and chat reports the updated count and unresolved gaps.
9. The user may later remove an indication, add an annotation, request completion, or choose `שלח להערכה`.
10. `שלח להערכה` requires a second confirmation and only changes the artifact status in this slice.

There is no selection mode, checkbox, layer-view mutation, separate artifact screen, or drawer in the MVP.

## Agent-style message states

### Empty

“עדיין לא נשמרו אינדיקציות במעקב הזה.”

Actions: `הוסף מזהי רשומות`.

### Proposed

“מצאתי 3 רשומות בשכבה המצורפת. לשמור אותן במעקב כאינדיקציות לבדיקה?”

Actions: `שמור במעקב`, `חזור לבחירה`, `ביטול`.

### Active

“במעקב שמורות 4 אינדיקציות: 2 תומכות באפשרות, 1 סותרת ו־1 מספקת הקשר. זיהוי המקור עדיין דורש בדיקה.”

Actions: `הצג אינדיקציות`, `הוסף`, `בקש השלמה`, `שלח להערכה`.

### Conflict

“המעקב השתנה מאז שפתחת אותו. הצגתי את הגרסה העדכנית; בחר שוב את הפעולה הרצויה.”

### Ready for assessment

“האינדיקציות סומנו כמוכנות להערכה. עדיין לא נוצרה הערכה או מטרה.”

## Record-level presentation

Each indication is shown as a compact chat row containing:

- source label and stable item identifier;
- observed claim;
- role label: `תומכת`, `סותרת`, or `הקשר`;
- optional user annotation;
- `פתח במקור` action;
- `הסר מהמעקב` action with confirmation.

Do not use color alone to distinguish roles. Include text and an icon or shape.

## Disabled and error states

- No attached event layer: explain that this workstream has no event layer against which the identifiers can be validated.
- Layer unavailable: retain saved references and show them as temporarily unavailable.
- Invalid or unknown `REC-...`: list unresolved identifiers and do not include them in the confirmation.
- Archived workstream: read-only message; no mutation actions.
- Network/save failure: preserve the pending selection locally and offer retry.
- Stale revision: reload the latest state and require renewed confirmation.
- No valid identifiers: do not show a persistence confirmation.
- `שלח להערכה`: disabled until at least one active indication exists.

## Accessibility

- The prompt explicitly states the required `REC-...` format and supports pasted comma-, space-, or line-separated identifiers.
- Focus remains in chat throughout the flow.
- Mixed RTL/LTR record IDs remain readable.
- Dynamic chat updates use the existing accessible message pattern and do not steal focus unexpectedly.

## UX risks

- Manual identifiers may be mistyped or inconvenient to discover.
- Long record lists can overwhelm chat; default to a compact count and reveal details on request.
- “Send to assessment” may imply that assessment already ran; confirmation copy must state that it only queues the next step.

## Recommendation

Approve manual `REC-...` entry plus chat resolution and confirmation. Do not change the layer UI or build a separate artifact management surface for the MVP.
