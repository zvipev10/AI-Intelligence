# Checkpoint Summary

## Checkpoint
Checkpoint 006 - Investigation isolation

## Capability
Investigation Memory (`investigation-memory`)

## Checkpoint Status
Complete and deployed.

## Goal
Keep the browser-selected investigation authoritative and prevent stale server-side state from changing or resetting its environment during startup.

## What Changed
- Removed startup use of the latest-workstream fallback.
- Removed canonical investigation-ID adoption from workstream responses.
- Removed automatic historical-playback initialization and reset during application boot.
- Retained explicit historical/real-time playback controls.
- Bumped the browser application asset version to `v132`.

## Scope
- No workstream records or statuses are changed.
- No scenario records are deleted or migrated.
- No investigation-memory records are deleted.

## Files Changed
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/test_workstream_ui.py`
- `.ai/work/capabilities/investigation-memory/status.md`
- `.ai/work/capabilities/investigation-memory/checkpoint-006.md`

## Checks
- `node --check app.js`
- `python -m unittest discover -p 'test*.py'`: 113 tests passed.
- All three VM services reported `active` after deployment.
- Public HTTPS served `app.js?v=132`.
- Public `app.js` SHA-256: `27e7414a30f80bde1cef92f8b88b199fd53190c286c836346c2e5680d948bc95`.
- Public JavaScript contains no latest-workstream fallback, canonical-ID adoption, or automatic historical-playback initializer.

## Risk
The investigation registry remains browser-local metadata. This checkpoint isolates selection correctly but does not introduce a multi-user, server-owned investigation registry.

## Deployment
- VM path: `/opt/serbia-poc-ui`
- Rollback copies:
  - `/opt/serbia-poc-ui/app.js.backup-20260804-2115-investigation-isolation`
  - `/opt/serbia-poc-ui/index.html.backup-20260804-2115-investigation-isolation`

## Next Step
User acceptance: switch among investigations and confirm each retains its own selected identity and environment.
