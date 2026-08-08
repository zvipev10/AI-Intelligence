# Checkpoint 009 — locale-isolated workstream stores and flows

## Scope
Implement Section 4 workstream localization for Hebrew/English runtime separation.

## Implementation result
- Workstreams now persist under physical locale roots:
  - Hebrew: `workstreams/v2_1/he/`
  - English: `workstreams/v2_1/en/`
- Existing legacy/shared workstream files are treated as Hebrew-owned fallback data only.
- English workstream creation, updates, action mutations, and artifacts reject Hebrew characters in user-visible fields before writing.
- Workstream list, get, update, archive, artifacts, presentations, chat actions, and playback reevaluation now route with explicit locale.
- The browser UI sends the current locale with workstream and playback API calls.
- Scenario playback runs persist locale and investigation lookups filter by locale.

## Validation
- `python -m py_compile server.py workstream_artifacts.py scenario_playback.py`
- `python -m unittest test_workstreams.py test_workstream_artifacts.py test_scenario_playback.py test_workstream_ui.py -q`
- `cd mcp_server; python -m unittest test_workstream_indication_tools.py -q`

All checks passed locally on 2026-08-08.

## Acceptance coverage
- English and Hebrew workstreams are physically separated.
- English list/get cannot see Hebrew workstream IDs.
- English Hebrew-text payloads fail closed without partial writes.
- Artifact creation and revision enforce English text validation.
- UI request paths include locale, preventing silent cross-language reads.

## Production deployment
Deployed to VM `151.145.93.180` on 2026-08-08.

Changed runtime files installed under `/opt/serbia-poc-ui`:
- `server.py`
- `app.js`
- `workstream_artifacts.py`
- `scenario_playback.py`

Backup retained at:
- `/opt/serbia-poc-ui-backups/workstream-locale-20260808T200045Z`

Service result:
- `serbia-poc-ui.service`: active
- `GET /api/status?locale=en`: returned v2.1 English dataset with 14,800 rows.

## Production smoke validation
- Created an English workstream and verified its physical file at `workstreams/v2_1/en/`.
- Confirmed Hebrew `GET` could not fetch the English workstream ID.
- Confirmed an English workstream payload containing Hebrew was rejected with HTTP 400 before persistence.
- Created a Hebrew workstream and verified its physical file at `workstreams/v2_1/he/`.
- Confirmed English `GET` could not fetch the Hebrew workstream ID.
- Removed the exact temporary smoke files after validation.
- Confirmed both English and Hebrew workstream lists for the smoke investigation were empty after cleanup.

## Remaining notes
- Explicit scenario-run IDs remain addressable by ID for transition routes; locale is persisted on the run and investigation-level playback lookup is locale-filtered.
