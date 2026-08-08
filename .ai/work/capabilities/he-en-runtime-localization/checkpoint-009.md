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

## Remaining notes
- Explicit scenario-run IDs remain addressable by ID for transition routes; locale is persisted on the run and investigation-level playback lookup is locale-filtered.
- Production deployment and smoke validation are the next step.
