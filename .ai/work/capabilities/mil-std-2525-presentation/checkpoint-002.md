# Checkpoint 002 — Remove map legend

## Outcome
Removed the collapsible MIL-STD map legend at the user's explicit direction.

## Scope
- Removed the legend markup from `index.html`.
- Removed the dedicated, now-unused legend CSS.
- Advanced the stylesheet asset reference to `styles.css?v=144`.
- Updated regression tests to require the legend to remain absent.

## Preserved behavior
MIL-STD symbol selection and rendering, accessible marker labels, confidence and evidence details, popups, and object-viewer navigation are unchanged.

## Validation
- `test_mil_std_presentation.py`
- `test_production_v162_contract.py`
- `test_welcome_page.py`
- JavaScript syntax check

## Publication
- Branch: `codex/remove-map-legend`
- Implementation commit: `fa6e4f9`
- Merge commit: `1122051`

## Deployment
- Target: `/opt/serbia-poc-ui` on `151.145.93.180`
- Production asset: `styles.css?v=144`
- Rollback: `/home/ubuntu/deploy-backups/remove-map-legend-1122051`
- Disk hashes match `deployment/SHA256SUMS-v175.txt` for `index.html` and `styles.css`.
- UI service is active and local `/api/status` reports the 14,800-row v2.1 dataset.
- Public HTTPS serves `styles.css?v=144` and `app.js?v=172` with no legend markup or legend CSS.

## Remaining work
None.
