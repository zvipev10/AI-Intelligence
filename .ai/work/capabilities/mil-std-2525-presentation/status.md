# Capability Status

## Current phase
Corrective checkpoint 002 — complete.

## Overall status
The map legend removal is merged, deployed, and production-verified. MIL-STD symbols, evidence details, and object-viewer behavior are unchanged.

## Who acts now
No role action required.

## Blockers
None.

## Next artifact
None.

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
