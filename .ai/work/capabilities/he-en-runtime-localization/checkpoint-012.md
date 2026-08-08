# Checkpoint 012 — Next button visibility fix

## Date
2026-08-09

## Scope
Fix the deployed regression where the staged playback Next button did not appear.

## Finding
The playback API correctly returned `next_stage` when there was no scenario run yet, but the frontend immediately tried to create the baseline run during page-load playback fetch:

```js
if (!payload?.run && payload?.next_stage) {
  return initializeStagedPlayback();
}
```

If baseline initialization failed, the UI never kept the API payload with `next_stage`, so `renderInvestigationPlayback()` had no next timeframe and hid the button.

This was also inconsistent with the intended behavior: baseline creation should happen only when the user presses Next, not automatically during page load.

## Fix

- Removed automatic `initializeStagedPlayback()` from `fetchInvestigationPlayback()`.
- The UI now stores and renders the playback status payload directly, including top-level `next_stage`.
- Bumped the `app.js` browser cache-buster from `v=141` to `v=142`.
- Added UI regression checks to ensure:
  - no `return initializeStagedPlayback();` remains in the page-load fetch path;
  - Next can be rendered from `playback?.run?.next_stage || playback?.next_stage`;
  - deployed HTML references `app.js?v=142`.

## Validation

Local:

- `python -m py_compile server.py scenario_playback.py workstream_artifacts.py`
- `python -m unittest test_workstream_ui.py test_scenario_playback.py -q`

Production deployment:

- Host: `151.145.93.180`
- Backup: `/opt/serbia-poc-ui-backups/next-button-fix-20260808T210948Z`
- Deployed files:
  - `/opt/serbia-poc-ui/app.js`
  - `/opt/serbia-poc-ui/index.html`

Production checks:

- `serbia-poc-ui.service` is active.
- `/api/status` reports build `serbia-poc-v2.1`, 14,800 rows.
- Deployed `app.js` no longer contains `return initializeStagedPlayback();`.
- Deployed `app.js` contains `playback?.run?.next_stage || playback?.next_stage`.
- Deployed and public `index.html` reference `app.js?v=142`.
- Public `/api/playback` for both `locale=he` and `locale=en` returns a top-level `next_stage` with timeframe `2026-09-12T04:25:50.096250Z` to `2026-09-17T06:00:00Z`, so the Next button should render in both locales.

## Remaining note

This checkpoint fixes visibility of the Next button. If pressing Next exposes an older production scenario-run conflict, handle that as a separate state cleanup or server-side stale-run recovery decision.
