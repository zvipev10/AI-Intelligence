# UX Review — Indications in the Workstream

## Status

AI-authored recommendation — pending human UX approval.

## UX principle

Do not expose an artifact name, management panel, or new navigation concept. The user sees indications, what they may mean, and the next available action through chat. The minimal active-workstream indicator remains unchanged.

## MVP chat flow

1. The user writes naturally to Moshe in the existing general chat, for example: “@משה, בדוק אם REC-V2-000142 ו־REC-V2-000207 מצדיקים המשך הערכה לגבי TGT-D4DC7A7EBE02.”
2. Moshe interprets the request from his instructions; there is no required command wording.
3. Tools resolve the `REC-...` indications and optional `TGT-...` assessment subject.
4. Moshe explains what resolved, what failed, the possible relationship, contradictions, and gaps.
5. Moshe asks in natural language whether to persist the proposed workstream change.
6. The user replies naturally in a later turn.
7. Moshe interprets that turn and confirms or rejects the staged proposal through a bounded tool.
8. Later additions, removals, annotations, completion requests, and assessment handoff follow the same conversational pattern.

There are no command buttons, saved expressions, dedicated composer, selection mode, checkbox, layer-view mutation, separate artifact screen, or drawer in the MVP.

## Agent-style message states

### Empty

“עדיין לא נשמרו אינדיקציות במעקב הזה.”

Moshe asks what the user wants to investigate or which `REC-...` / `TGT-...` references are relevant.

### Proposed

“מצאתי 3 רשומות בשכבה המצורפת. לשמור אותן במעקב כאינדיקציות לבדיקה?”

Moshe asks for confirmation in natural language; the user is not constrained to specific response wording.

### Active

“במעקב שמורות 4 אינדיקציות: 2 תומכות באפשרות, 1 סותרת ו־1 מספקת הקשר. זיהוי המקור עדיין דורש בדיקה.”

Moshe describes possible next actions in prose; the user responds naturally.

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
- Invalid or unavailable `TGT-...`: distinguish a missing subject from invalid evidence.
- Archived workstream: read-only message; no mutation actions.
- Network/save failure: preserve the pending selection locally and offer retry.
- Stale revision: reload the latest state and require renewed confirmation.
- No valid identifiers: do not show a persistence confirmation.
- `שלח להערכה`: disabled until at least one active indication exists.

## Accessibility

- Mixed free text, `REC-...`, and `TGT-...` references remain readable.
- Focus remains in chat throughout the flow.
- Mixed RTL/LTR record IDs remain readable.
- Dynamic chat updates use the existing accessible message pattern and do not steal focus unexpectedly.

## UX risks

- Manual identifiers may be mistyped or inconvenient to discover.
- Long record lists can overwhelm chat; default to a compact count and reveal details on request.
- “Send to assessment” may imply that assessment already ran; confirmation copy must state that it only queues the next step.

## Recommendation

Approve ordinary general-chat interaction interpreted by Moshe, with bounded reference-resolution and staged artifact tools. Do not add phrase-based commands, new chat modes, layer UI, or a separate artifact surface.
