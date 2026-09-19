# Checkpoint Summary

## Checkpoint

001 — production recovery

## Checkpoint status

Complete.

## What changed

- The deployer now copies into the existing UI root rather than deleting it, creates a timestamped backup, excludes mutable state from its payload, ships `scenario_manifests`, and pins the regenerated systemd unit to v2.1.
- The canonical manifest now uses the validated dataset-start baseline.
- Playback-loading errors are visible in the header.
- Production restored the validated manifest from `/opt/serbia-poc-ui-backups/staged-playback-20260808T203509Z` and installed the updated UI asset.

## Production evidence

- Backup created: `/opt/serbia-poc-ui-backups/playback-recovery-20260919T163354Z`
- Service: active
- Status: `serbia-poc-v2.1`, dataset v2.1
- Playback: `next_stage.sequence: 1`, from `2026-09-17T02:00:00Z` to `2026-09-17T06:00:00Z`

## Tests/checks run

- Python compilation of the deployer, server, and playback module.
- `test_scenario_playback.py`: 19 passed.
- `node --check app.js`.
- Production API and service-log smoke checks.

## Risk

The initial health request happened before the restarted service was accepting connections; a subsequent probe passed. Existing historical runtime state was not restored because the inspected staged-playback backup contained only the manifest.
