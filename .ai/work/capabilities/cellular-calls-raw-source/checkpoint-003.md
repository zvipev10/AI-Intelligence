# Checkpoint 003 — Dual-endpoint map presentation

## Outcome

Cellular call records now preserve their two-location meaning on the map. Each call renders a neutral Side A marker, a distinct Side B marker, and a dashed connection line. Either endpoint or the line opens the same raw `REC-*` viewer; the table and timeline still contain one record per call.

## Verification

- 17 focused cellular-call and object-viewer tests pass.
- JavaScript syntax and `git diff --check` pass.
- Live browser verification against dataset V2.1 showed 18 endpoints for the nine calls in the active 02:00–09:00 slice, their connecting lines, and the shared call viewer opening from Side B.
- Full suite: 195 tests pass. Four PyYAML import errors and one existing production-manifest checksum failure are unchanged baseline failures reproduced before this map change.

## Release state

Ready to merge and deploy.
