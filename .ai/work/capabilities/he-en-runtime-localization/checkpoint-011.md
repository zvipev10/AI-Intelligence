# Checkpoint 011 — Deployment consistency fix for locale toggle and status indicators

## Date
2026-08-08

## Scope
Fix the deployed UI regression around English/Hebrew switching and system status indicators.

## Finding
The VM had status-indicator HTML from the newer header/status UI but did not have the matching frontend status-rendering implementation and styles from merged `main`.

That left the deployed frontend inconsistent:

- the header status markup used `datasetStatusIndicator` / `agentStatusIndicator`;
- the older deployed JavaScript still expected the previous `.status-dot` structure in part of boot/status handling;
- the matching status indicator CSS was not deployed with the new markup.

This could break boot-time status updates and make the locale/status header state appear regressed even though the backend locale APIs were healthy.

## Fix
Deployed the matching merged `main` frontend assets to `/opt/serbia-poc-ui`:

- `app.js`
- `index.html`
- `styles.css`

No backend code or data files were changed in this checkpoint.

## Production deployment

Host:

- `151.145.93.180`

Rollback backup:

- `/opt/serbia-poc-ui-backups/status-locale-fix-20260808T204607Z`

Production checks:

- `serbia-poc-ui.service` is active.
- `GET http://127.0.0.1:8769/api/status` returned build `serbia-poc-v2.1`, locale `he`, 14,800 dataset rows.
- Deployed `app.js` contains `renderSystemStatuses` and dataset `updateSystemStatus(...)` calls.
- Deployed `index.html` contains `datasetStatusIndicator` and references `app.js?v=141`.
- Deployed `styles.css` contains `status-indicator`.
- Deployed language slider markup contains the compact `E` / `ע` labels.

## Local validation before this fix

The merged `main` branch had already passed:

- `python -m py_compile server.py scenario_playback.py workstream_artifacts.py`
- `python -m unittest test_scenario_playback.py test_workstream_ui.py -q`
- `cd mcp_server && python -m unittest test_playback_visibility.py test_workstream_indication_tools.py -q`

## Remaining risks

- This checkpoint fixes deployment drift, not a source-code bug. If future deployments copy only part of the frontend bundle, the same class of mismatch can recur.
- Manual browser acceptance is still recommended for the header in both `?lang=he` and `?lang=en`.
