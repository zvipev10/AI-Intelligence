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

## Production deployment

Deployed to VM `151.145.93.180` on 2026-08-08.

Changed runtime files installed under `/opt/serbia-poc-ui`:

- `server.py`
- `app.js`
- `index.html`
- `scenario_manifests/brnjak-engineering-assessment-v1.json`

Rollback backup:

- `/opt/serbia-poc-ui-backups/staged-playback-20260808T203509Z`

Production deployment checks:

- `serbia-poc-ui.service` is active.
- `GET http://127.0.0.1:8769/api/status` returned build `serbia-poc-v2.1` with 14,800 rows.
- Deployed `index.html` contains `Staged playback`.
- Deployed `server.py` contains `visible_ui_events`.
- Deployed `app.js` contains `initializeStagedPlayback`.
- Deployed scenario manifest starts at `2026-09-12T04:25:50.096250Z`.

Production smoke:

- Temporarily wrote a baseline active `active_visibility.json`, queried English TikTok layer rows, and restored the previous inactive historical policy afterward.
- English TikTok rows returned under the baseline policy: 1,073.
- First returned timestamp: `2026-09-12T04:42:16.063015Z`.
- Last returned timestamp: `2026-09-17T05:55:41.342520Z`.
- No sampled row fell outside `2026-09-12T04:25:50.096250Z` to `2026-09-17T06:00:00Z`.
- `GET /api/playback?investigation_id=smoke-read-only&locale=en` reported `mode: real_time` and the first staged timeframe from dataset start through `2026-09-17T06:00:00Z`.
- After smoke, `/opt/serbia-poc-ui/scenario_runs/v2.1/active_visibility.json` was restored to the previous inactive historical policy and the UI service remained active.

## Product behavior after this checkpoint

The user sees one staged playback control. The first loaded state behaves like the previous historical/default state for the initial scenario window because all records from dataset beginning through the first slice boundary are visible. Pressing Next advances the cumulative visible window. Moshe is not asked to reevaluate at baseline creation; he reevaluates only after new data is released and only if active workstreams exist.

## Risks and follow-ups

- The active playback visibility policy remains global for the current deployed UI/MCP process. Production smoke restored the previous `active_visibility.json` after test calls.
- Explicit scenario-run IDs are still directly addressable by ID, although investigation-level playback lookup is locale-filtered.
- Manual UX acceptance is still needed for final wording and layout of the simplified staged control.
