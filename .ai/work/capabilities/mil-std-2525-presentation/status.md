# Capability Status

## Current phase
Corrective checkpoint 004 — complete.

## Overall status
The UAV-layer affiliation propagation bug is fixed, merged, deployed, and production-verified.

## Who acts now
No role action required.

## Blockers
None.

## Corrective checkpoint 004
Supported UAV observations inherit affiliation from the existing organization registry through `event.entity_id`. Unmapped entity IDs continue to render as unknown, preserving the fail-safe fallback.

## Corrective checkpoint 003
The four KFOR organization entities and the NATO reserve entity now use hostile affiliation. The presentation uses a red diamond frame; Serbian Armed Forces remain friendly and UAV observations remain unknown.

## Corrective checkpoint 003 publication
- Implementation commit on `main`: `803b212`
- Production assets: `app.js?v=173`, `styles.css?v=145`
- Production backup: `/home/ubuntu/deploy-backups/kfor-nato-hostile-803b212`
- Manifest: `deployment/SHA256SUMS-v176.txt`

## Next artifact
None.

## Corrective checkpoint 004 publication
- Implementation commit on `main`: `a5038a7`
- Production assets: `app.js?v=174`, `styles.css?v=145`
- Production backup: `/home/ubuntu/deploy-backups/uav-affiliation-a5038a7`
- Manifest: `deployment/SHA256SUMS-v177.txt`

## Issues
- Parent: https://github.com/zvipev10/AI-Intelligence/issues/51
- Implementation: https://github.com/zvipev10/AI-Intelligence/issues/52
- Draft PR: https://github.com/zvipev10/AI-Intelligence/pull/53

## Latest change
PR #53 merged to `main` as `9e5b17e6995b40340919523bb05b87b281ff2d60`. v174 is deployed to `/opt/serbia-poc-ui`; public HTTP, asset, API, and service checks passed. Rollback is `/home/ubuntu/deploy-backups/mil-std-2525-20260910T230410Z`. See `handoff-summary.md`.

## Corrective change
At the user's direction, the collapsible map legend and its dedicated CSS were removed. The stylesheet asset version advances to `styles.css?v=144`; symbol rendering and traceability remain in scope and unchanged.

## Corrective publication
- Branch: `codex/remove-map-legend`
- Commit: `fa6e4f9`
- Merge commit on `main`: `1122051`
- Production asset: `styles.css?v=144`
- Production backup: `/home/ubuntu/deploy-backups/remove-map-legend-1122051`
