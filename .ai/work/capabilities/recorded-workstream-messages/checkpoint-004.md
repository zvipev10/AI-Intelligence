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

## Production

- Deployed to VM `151.145.93.180`.
- Public asset: `app.js?v=162`.
- Hebrew and English recorded result-toggle paths were verified in the public
  cache-bypassed asset.
- `serbia-poc-ui.service`, `hermes-gateway.service`, and
  `hermes-moshe-gateway.service` are active.
- Rollback: `/home/ubuntu/deploy-backups/recorded-result-toggle-20260811T190123Z`.

## Recommendation

Approved for merge.
