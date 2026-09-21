# Checkpoint 003 — Dual-endpoint map presentation

## Outcome

Cellular call records now preserve their two-location meaning on the map. Each call renders a neutral Side A marker, a distinct Side B marker, and a dashed connection line. Either endpoint or the line opens the same raw `REC-*` viewer; the table and timeline still contain one record per call.

## Verification

- 17 focused cellular-call and object-viewer tests pass.
- JavaScript syntax and `git diff --check` pass.
- Live browser verification against dataset V2.1 showed 18 endpoints for the nine calls in the active 02:00–09:00 slice, their connecting lines, and the shared call viewer opening from Side B.
- Full suite: 195 tests pass. Four PyYAML import errors and one existing production-manifest checksum failure are unchanged baseline failures reproduced before this map change.

## Release state

Merged to remote `main` at `47692c3df80ecb3652ac5cd2664caf0bd9573cb6` and deployed to `/opt/serbia-poc-ui` and `/opt/serbia-poc`.

Production verification:

- `serbia-poc-ui.service` and `hermes-gateway.service` are active.
- Public assets are `app.js?v=197` and `styles.css?v=152`.
- `/api/status` reports V2.1 with 14,833 source rows.
- The English catalog exposes `Cellular Calls` with 24 records.
- A deployed map opened all 48 endpoint controls; Side B of `REC-V2-014816` opened the shared two-party viewer and simulated recording.
- The legacy comprehensive MCP smoke client hung and was terminated; targeted gateway/UI health checks passed and the UI reports Hermes + MCP connected.
