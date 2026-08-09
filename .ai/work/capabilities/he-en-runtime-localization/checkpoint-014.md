# Checkpoint 014 — Restore collapsed steps and automatic final-result presentation

## Date
2026-08-09

## Scope
Restore two previously implemented UI behaviors that were absent from deployed `main`:

- step details in the conversation are collapsed by default;
- final agent results are automatically presented on the map or timeline when the answer arrives.

## Finding
The missing behavior came from branch integration drift. The features existed in separate feature branches but were not present in the current `main` line:

- `74a8d37` — `feat: collapse agent research steps`
- `9c463e7` — `feat: auto-present agent final results`

Current deployed `app.js` lacked:

- `activity-disclosure`;
- `activity-card-summary`;
- `resolveFinalResultView(...)`;
- `presentFinalAgentResult(...)`;
- the call to present final result layers immediately after `finalizeAssistantMessage(...)`.

## Fix

- Restored closed native disclosure rendering for each investigation step.
- Restored readable fallback titles for unknown tool names.
- Restored the shared final result presenter.
- Normal and restored final answers now use the same layer presentation path.
- Final result presentation chooses map/timeline from requested layer preferences, result recommendation, or layer capabilities.
- Bumped asset cache keys:
  - `styles.css?v=132`
  - `app.js?v=144`
- Restored regression tests:
  - `test_agent_step_collapse.py`
  - `test_final_result_auto_visualization.py`
- Updated existing cache-buster assertions.

## Local validation

- `python -m py_compile server.py scenario_playback.py workstream_artifacts.py`
- `python -m unittest test_agent_step_collapse.py test_final_result_auto_visualization.py test_workstream_ui.py test_chat_autoscroll.py -q`
- `python -m unittest test_workstreams.py test_workstream_artifacts.py test_scenario_playback.py test_workstream_ui.py test_agent_step_collapse.py test_final_result_auto_visualization.py test_chat_autoscroll.py -q`

## Production deployment

Host:

- `151.145.93.180`

Backup:

- `/opt/serbia-poc-ui-backups/restore-result-ui-20260809T081047Z`

Deployed files:

- `/opt/serbia-poc-ui/app.js`
- `/opt/serbia-poc-ui/index.html`
- `/opt/serbia-poc-ui/styles.css`

Production checks:

- `serbia-poc-ui.service` is active.
- `/api/status` reports build `serbia-poc-v2.1`, 14,800 rows.
- Deployed `app.js` contains `activity-disclosure` and `activity-card-summary`.
- Deployed `styles.css` contains `activity-disclosure` and focus-visible disclosure styling.
- Deployed `app.js` contains `presentFinalAgentResult` and `resolveFinalResultView`.
- Public HTML references `app.js?v=144` and `styles.css?v=132`.

## Remaining note

This checkpoint restores the code and static production checks. A manual browser smoke with a real agent answer is still useful to visually confirm the map/timeline auto-selection in the exact analyst flow.
