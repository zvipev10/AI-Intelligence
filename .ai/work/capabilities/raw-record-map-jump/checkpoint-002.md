# Checkpoint 002 — Shared map row selection

## Summary

Resolved the post-deployment gaps reported during user acceptance.

## Changes

- Refresh restored memory-layer rows after the runtime location catalog loads, preventing stale disabled map actions.
- Added the map action to target, location, and location-metadata rows.
- Generalized coordinate resolution to canonical IDs, direct coordinates, and matching location names.
- Added toggle semantics with `aria-pressed`, an active pin state, selected-row highlighting, and repeat-click unselection.
- Added target- and location-specific map popups.
- Bumped static asset cache keys.

## Checks

- `node --check app.js`
- 41 focused regression tests passed.
- `git diff --check`
- Deployed browser smoke confirmed 170 location actions, one selected row/pressed action/popup after selection, and zero of each after unselection.

## Deployment

- Assets: `app.js?v=154`, `styles.css?v=135`.
- VM service active; status endpoint reports the V2.1 dataset.
- Rollback backup: `/opt/serbia-poc-ui.backup-map-selection-20260811T154856Z`.

## Review recommendation

Ready for user acceptance of restored raw layers, targets, and locations.
