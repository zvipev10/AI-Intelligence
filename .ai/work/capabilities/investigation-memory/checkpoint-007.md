# Checkpoint Summary

## Checkpoint
Checkpoint 007 - Remove old investigations

## Status
Complete and deployed.

## Goal
Remove all old investigations without changing workstream records.

## Changes
- Replaced the browser investigation registry key with `serbia-poc-investigations-v2`.
- On application load, explicitly removes `serbia-poc-investigations-v1`.
- Browsers with only the legacy registry start with one fresh default investigation.
- Bumped the public application asset to `app.js?v=133`.

## Production Reset
- Back up `/opt/serbia-poc-ui/investigations/v2.1` if it contains files.
- Clear JSON investigation-memory records from the live directory.
- Do not modify `/opt/serbia-poc-ui/workstreams/v2.1`.

## Checks
- `node --check app.js`
- `python -m unittest test_workstream_ui.py`: 24 tests passed.
- `python -m unittest discover -p 'test*.py'`: 114 tests passed.
- Production `/api/investigations` returns an empty list.
- Public HTTPS serves `app.js?v=133`.
- Public JavaScript includes the `v2` registry and legacy-key removal.
- Public `app.js` SHA-256: `a49467786976d2c59ccd86eecaa0db46a93ad2264190d2287278aae6621469de`.
- All three VM services are active.
- Workstream count remained 13 before and after deployment.

## Production Result
- `/opt/serbia-poc-ui/investigations/v2.1` did not exist, so there were no server investigation files to remove or archive.
- Old visible investigations were browser-local and are removed when each browser loads `v133`.
- UI rollback files:
  - `/opt/serbia-poc-ui/app.js.backup-20260804-2120-investigation-reset`
  - `/opt/serbia-poc-ui/index.html.backup-20260804-2120-investigation-reset`

## Rollback
Restore the deployed UI files and investigation-memory directory from timestamped VM backups.
