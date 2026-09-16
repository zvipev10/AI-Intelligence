# Checkpoint 002 — Rendering correction

## User findings addressed
1. Opening the 4,165-row evidence layer could overload per-item DOM marker rendering and appear to refresh the application.
2. Raw event layers still used MIL-STD symbology despite raw records being provenance rather than normalized evidence.

## Changes
- Raw event layers now aggregate into neutral location dots.
- Focusing an individual raw record also uses a neutral marker.
- MIL-STD rendering remains for normalized evidence and entity presence layers.
- Equivalent evidence descriptors are coalesced by location, symbol, icon, and affiliation.
- Evidence map rendering is capped at 400 groups; table, timeline, viewer, and provenance retain every row.

## QA
- Focused evidence/MIL-STD/viewer/catalog suite: 32 passed.
- JavaScript syntax and diff checks passed.

## Production follow-up — 2026-09-16
- Fixed the remaining `undefined is not an object (evaluating 'value.replace')` failure by making the shared HTML escaping boundary tolerate null and undefined optional fields.
- Added focused regression coverage and advanced the UI asset to `app.js?v=186`.
- Twenty-five focused evidence, MIL-STD, and catalog tests pass; JavaScript syntax and catalog behavioral checks pass.
- Deployed commit `a630c67` with rollback backup `/home/ubuntu/deploy-backups/null-safe-render-a630c67`.
- UI and Hermes services are active; deployed `app.js` and `index.html` hashes match the commit exactly.
