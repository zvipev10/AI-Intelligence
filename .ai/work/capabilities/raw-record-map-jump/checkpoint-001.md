# Checkpoint 001 — Raw record map jump

## Summary

Implemented the approved client-side interaction on top of the latest deployed memory/workstream branch.

## Changes

- Dedicated bilingual pin action on raw event rows.
- Canonical/event-coordinate resolution with disabled state when unavailable.
- Map activation, close-detail camera centering, and exact-record popup.
- Previous focused popup replacement and cleanup during map rerenders.
- Action column excluded from generic table sorting/filtering controls.
- Asset cache keys bumped for deployment.

## Checks

- `node --check app.js`
- 40 focused regression tests passed.
- `git diff --check`

## Incomplete

- VM deployment and browser smoke validation.

## Review recommendation

Continue to deployment and final QA.
