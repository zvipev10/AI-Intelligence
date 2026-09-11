# Capability Status

## Current phase
Corrective checkpoint 003 — implementation in progress.

## Overall status
KFOR- and NATO-related organization entities are being corrected from neutral to hostile symbology at the user's direction.

## Who acts now
Development is implementing, validating, merging, and deploying the correction under the user's explicit authorization.

## Blockers
Complete validation, merge to remote `main`, deploy v176, and record production verification.

## Corrective checkpoint 003
The four KFOR organization entities and the NATO reserve entity now use hostile affiliation. The presentation uses a red diamond frame; Serbian Armed Forces remain friendly and UAV observations remain unknown.

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
