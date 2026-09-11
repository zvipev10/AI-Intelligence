# Checkpoint 004 — Propagate explicit affiliation to UAV observations

## Root cause
`milStdObservationDescriptor()` hard-coded every supported UAV observation to `unknown`, ignoring the record's `entity_id`. The preceding hostile registry correction therefore affected organization layers only.

## Fix
- Resolve UAV affiliation from `MIL_STD_ORGANIZATIONS[event.entity_id]`.
- Fall back to `unknown` when the entity has no explicit registry mapping.
- Advance the script to `app.js?v=174`.
- Update regression and production-manifest contracts.

## Expected data effect
The current v2.1 projection contains 1,509 supported UAV observations. Of these, 508 reference the five explicitly hostile KFOR/NATO entities and will render hostile; observations tied to unmapped entities remain unknown.

## Preserved behavior
Object class, confidence, claim state, location, evidence traceability, and viewer navigation are unchanged.

## Release plan
Validate, push directly to remote `main` under the user's explicit instruction, back up current production assets, deploy v177, and verify the public script and service.

## Release outcome
- Pushed to remote `main` at `a5038a7`.
- Deployed `app.js` and `index.html` to `/opt/serbia-poc-ui`.
- Rollback backup: `/home/ubuntu/deploy-backups/uav-affiliation-a5038a7`.
- Deployed hashes match `deployment/SHA256SUMS-v177.txt`.
- Production serves `app.js?v=174` and `styles.css?v=145`.
- The public script contains explicit entity-affiliation propagation, unknown fallback, and all five hostile mappings.
- `serbia-poc-ui.service` is active; `/api/status` reports the 14,800-row v2.1 dataset.

## Remaining work
None.
