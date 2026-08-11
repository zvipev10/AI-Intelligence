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

## Deployment and browser validation

- Deployed assets: `app.js?v=153`, `styles.css?v=134`.
- VM service: active; `/api/status` reports 14,800 V2.1 events.
- Browser smoke: opened the 3,745-row UAV video layer, activated `Show REC-V2-006948 on map`, confirmed map view active and exactly one event popup containing that record's ID, time, entity, location, and summary.
- Rollback backup: `/opt/serbia-poc-ui.backup-raw-map-jump-20260811T153527Z`.

## Review recommendation

Approve for user acceptance.
