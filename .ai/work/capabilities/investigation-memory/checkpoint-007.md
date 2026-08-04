# Checkpoint Summary

## Checkpoint
Checkpoint 007 - Remove old investigations

## Status
Implementation complete; production reset pending.

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

## Rollback
Restore the deployed UI files and investigation-memory directory from timestamped VM backups.
