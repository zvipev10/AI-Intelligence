# UX Review — Indications in the Workstream

## Status

AI-authored recommendation — pending human UX approval.

## UX principle

Do not expose an artifact name, management panel, or new navigation concept. The user sees indications, what they may mean, and the next available action through chat. The minimal active-workstream indicator remains unchanged.

## Manual MVP flow

1. The user presses the active-workstream indicator.
2. The agent-style message summarizes how many indications are saved, their support/contradiction balance, gaps, and current responsibility.
3. If no indications exist, the message says so and offers `הוסף אינדיקציות מהשכבה`.
4. Pressing that action places the already attached layer into a temporary record-selection mode.
5. The user selects one or more records/items in the existing layer view and confirms.
6. Chat shows a preview listing the selected references and asks `לשמור את האינדיקציות במעקב?`.
7. On confirmation, the references persist and chat reports the updated count and unresolved gaps.
8. The user may later remove an indication, add an annotation, request completion, or choose `שלח להערכה`.
9. `שלח להערכה` requires a second confirmation and only changes the artifact status in this slice.

Record selection uses the existing layer view as a temporary selection state. It does not introduce a separate artifact screen or drawer. The resulting description, confirmation, success, conflict, and next actions always return to chat.

## Agent-style message states

### Empty

“עדיין לא נשמרו אינדיקציות במעקב הזה.”

Actions: `הוסף אינדיקציות מהשכבה`.

### Proposed

“בחרת 3 פריטים שעשויים להיות רלוונטיים. לשמור אותם במעקב כאינדיקציות לבדיקה?”

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

- No attached layer: explain that this workstream has no available source layer; do not offer selection.
- Layer unavailable: retain saved references and show them as temporarily unavailable.
- No stable record IDs: disable confirmation for those items and explain why.
- Archived workstream: read-only message; no mutation actions.
- Network/save failure: preserve the pending selection locally and offer retry.
- Stale revision: reload the latest state and require renewed confirmation.
- Empty selection: confirmation disabled.
- `שלח להערכה`: disabled until at least one active indication exists.

## Accessibility

- Selection state is announced and visibly distinguished from ordinary browsing.
- Keyboard selection and confirmation are supported.
- Focus returns to the originating chat action after cancel and to the confirmation message after selection.
- Mixed RTL/LTR record IDs remain readable.
- Dynamic chat updates use the existing accessible message pattern and do not steal focus unexpectedly.

## UX risks

- Temporary selection mode may be confused with normal layer filtering.
- Long record lists can overwhelm chat; default to a compact count and reveal details on request.
- “Send to assessment” may imply that assessment already ran; confirmation copy must state that it only queues the next step.

## Recommendation

Approve the temporary layer-selection mode plus chat confirmation. Do not build a separate artifact management surface for the MVP.
