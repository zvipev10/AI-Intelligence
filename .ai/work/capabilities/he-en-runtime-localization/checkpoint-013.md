# Checkpoint 013 — Remove staged playback header title

## Date
2026-08-09

## Scope
Remove the visible staged playback title from the header while preserving the timeframe and Next button.

## Fix

- Removed the `intelligenceModeSelect` title element from `index.html`.
- Removed the remaining JavaScript dependency and text assignment for `Staged playback` / `ניגון מדורג`.
- Kept `intelligencePeriod`, `playbackAgentStatus`, and `playbackNextButton`.
- Bumped `app.js` cache-buster from `v=142` to `v=143`.

## Validation

Local:

- `python -m unittest test_workstream_ui.py -q`

Production deployment:

- Host: `151.145.93.180`
- Backup: `/opt/serbia-poc-ui-backups/remove-playback-title-20260808T211229Z`
- Deployed files:
  - `/opt/serbia-poc-ui/app.js`
  - `/opt/serbia-poc-ui/index.html`

Production checks:

- `serbia-poc-ui.service` is active.
- `/api/status` reports build `serbia-poc-v2.1`, 14,800 rows.
- Deployed `index.html` and `app.js` do not contain `Staged playback`, `ניגון מדורג`, or `intelligenceModeSelect`.
- Public `index.html` references `app.js?v=143`.
- Next button markup and visibility logic remain deployed.
