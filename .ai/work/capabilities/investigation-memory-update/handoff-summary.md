# Handoff summary

## Outcome

Implemented an independent, memory-grounded general-agent update for newly released playback slices. Empty investigation memory remains silent. The result is chat-only and cannot read or mutate workstream/Moshe state.

## Runtime changes

- `scenario_playback.py` persists revision-scoped memory-update job state.
- `server.py` claims, runs, resumes, and completes the background general-agent job.
- `app.js` renders and polls the update independently in chat.
- Public browser asset version advances to `app.js?v=167`.

## Validation

All 131 package tests pass. Focused tests cover empty-memory silence, triggering without active workstreams, and exclusion of workstreams from general-agent context.

## Release

Deployed the reviewed runtime files to production with runtime data, configuration, and secrets preserved. The service is healthy, serves `app.js?v=167`, and all deployed hashes match commit `5ebdfb8`. The commit is merged into remote `main`.

## Remaining risk

The live agent response depends on the configured general Hermes provider. Provider failures are isolated and reported in chat without affecting Moshe processing or playback advancement.

## Corrective release v172

Fixed a cross-investigation isolation defect reported from KFOR and NATO screenshots.
The playback clock remains global, but memory-update claims, serialization, worker
resumption, browser rendering, and deduplication are now scoped to the update's owning
investigation. Legacy revision-only records are read only when their stored owner
matches the requested investigation.

All 125 locally runnable package tests pass. Production serves `app.js?v=170`, the UI
service is healthy, and live API comparison confirms KFOR and NATO share the global
run while only NATO receives the NATO-owned stored update. Rollback backup:
`/opt/serbia-poc-ui-backups/v172-isolation-20260908T1915Z`.

The corrective implementation and deployment record are merged into remote `main` at
`fa7c596`.
