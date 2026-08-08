# Checkpoint 010 — Unified staged playback and visible-timeframe enforcement

## Date
2026-08-08

## Scope
Implement the approved playback simplification:

- one staged playback flow instead of separate historical and real-time UX modes;
- initial staged state exposes the cumulative data available from dataset start through the first slice end;
- Moshe reevaluation is skipped for initial baseline creation and can run only after a subsequent slice arrives;
- UI/data layer queries respect the active playback `visible_timeframe`;
- MCP queries continue to enforce active playback visibility through `active_visibility.json`.

## Implementation summary

- Updated the Brnjak engineering assessment scenario manifest so the first visible window starts at the beginning of the v2.1 dataset and ends at the first scenario slice boundary.
- Normalized `/api/playback` and `/api/playback/mode` to staged playback while keeping compatibility for clients that still send `mode: "historical"`.
- Changed `/api/playback/next` so a missing run creates the baseline visible window without Moshe reevaluation. Later advances trigger reevaluation only when active workstreams exist.
- Added server-side UI layer filtering against active `visible_timeframe`.
- Updated the browser flow to remove the historical/real-time selector distinction while keeping the timeframe display and Next button.
- Reloaded open catalog layers after playback timeframe changes so visible rows match the current slice.
- Added regression tests for initial-baseline Moshe skipping and UI layer timeframe filtering.
- Stabilized playback tests by joining background reevaluation workers during fixture cleanup.

## Files changed

- `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718/scenario_manifests/brnjak-engineering-assessment-v1.json`
- `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718/server.py`
- `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718/app.js`
- `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718/index.html`
- `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718/test_scenario_playback.py`
- `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718/test_workstream_ui.py`

## Local validation

- `python -m py_compile server.py scenario_playback.py workstream_artifacts.py`
- `python -m unittest test_scenario_playback.py test_workstream_ui.py -q`
- `python -m unittest test_workstreams.py test_workstream_artifacts.py test_scenario_playback.py test_workstream_ui.py test_moshe_profile.py -q`
- `cd mcp_server && python -m unittest test_playback_visibility.py test_workstream_indication_tools.py -q`

## Product behavior after this checkpoint

The user sees one staged playback control. The first loaded state behaves like the previous historical/default state for the initial scenario window because all records from dataset beginning through the first slice boundary are visible. Pressing Next advances the cumulative visible window. Moshe is not asked to reevaluate at baseline creation; he reevaluates only after new data is released and only if active workstreams exist.

## Risks and follow-ups

- The active playback visibility policy remains global for the current deployed UI/MCP process. Production smoke must restore the previous `active_visibility.json` after test calls.
- Explicit scenario-run IDs are still directly addressable by ID, although investigation-level playback lookup is locale-filtered.
- Manual UX acceptance is still needed for final wording and layout of the simplified staged control.
