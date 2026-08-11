# Checkpoint 019 — Server-backed investigation registry

## Outcome

The investigation selector no longer treats browser local storage as the source
of truth. The server registry is assembled by investigation ID from durable
investigation memory, workstreams, and scenario runs. On startup, the client
registers its locally known IDs and hydrates the selector from the server.

Distinct investigation IDs are preserved even when their display names match.
This corrects the prior name-based deduplication that could hide valid entries.

## Scope

- add `POST /api/investigations` for durable ID/name registration;
- expand `GET /api/investigations` to discover durable investigation activity;
- merge browser and server entries strictly by investigation ID;
- hydrate the selector during application boot;
- cover duplicate-name and workstream/scenario discovery regressions.

## Validation

- JavaScript syntax check passed.
- Python compilation passed.
- Focused investigation/UI suite: 32 tests passed.
- Full Python discovery: 135 tests passed.
- Production deployment and smoke evidence are recorded in the handoff summary.
- The live Hebrew registry returned 11 investigations and the public page served
  `app.js?v=156`; UI and both Hermes gateway services were active.

## Risk and rollback

Existing browser entries are uploaded on boot, so an obsolete local entry may
remain visible until an explicit archive/delete lifecycle exists. This is safer
than silently hiding an investigation. The deployment backup path is recorded
in `handoff-summary.md`.
