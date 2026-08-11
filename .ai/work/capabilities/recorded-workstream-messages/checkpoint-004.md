# Checkpoint 004 — Recorded result visibility toggle

## Summary

Recorded workstream detail cards now include the same Show/Hide results control
as live workstream cards.

## Behavior

- The button operates only on the recorded presentation layers.
- Replay remains read-only and never mutates the live workstream.
- The label and accessible state switch between `הצג תוצאות` and
  `הסתר תוצאות` according to layer visibility.
- If an older recording cannot restore a presentation, the unavailable button
  is removed instead of leaving a broken action.

## Deployment

Validation passed:

- JavaScript syntax check passed.
- Focused recorded-workstream/UI suite: 37 tests passed.
- Full Python discovery: 142 tests passed.

Localized VM deployment is pending.
