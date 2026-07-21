# QA Review - מכלול Team Management

## Review status

Approved for Slice 1 implementation.

## Reviewer/source of input

AI QA review based on Product-approved scope, developer review, and UX review.

## Happy path

- Open the app.
- Confirm the header shows the active investigation combo.
- Confirm a compact `מכלול` list appears near the combo.
- Confirm all five predefined members render:
  - משה
  - טליה
  - נעמה
  - גדי
  - יהלי
- Confirm each member has a visible avatar.

## Edge cases

- Broken avatar image falls back to initials without layout break.
- Long role text is not always visible and does not overflow the compact row.
- Mobile header wraps cleanly.

## Regression areas

- Investigation combo input remains editable.
- Investigation dropdown still opens.
- Add-investigation button remains clickable.
- Header status remains readable.
- Chat, layer tabs, filters, map, timeline, table, and investigation memory are not affected.

## Suggested checks

- `git diff --check`
- Local server smoke at desktop viewport.
- Local server smoke at mobile viewport.
- Verify avatar assets return HTTP 200.
