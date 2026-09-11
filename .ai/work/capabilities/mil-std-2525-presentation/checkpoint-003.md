# Checkpoint 003 — KFOR and NATO hostile symbology

## Decision
The user explicitly classified all KFOR- and NATO-related catalog entities as enemy/hostile for this scenario presentation.

## Scope
- Map `ENT-KFOR-RCE`, `ENT-KFOR-KTRBN`, `ENT-KFOR-MSU`, `ENT-KFOR-AVIATION`, and `ENT-NATO-RESERVE` to `hostile`.
- Present hostile organization symbols with a red diamond frame.
- Advance assets to `app.js?v=173` and `styles.css?v=145`.
- Add regression coverage for all five mappings and the hostile frame styling.

## Preserved behavior
- Serbian Armed Forces organization entities remain friendly.
- UAV observations remain unknown affiliation.
- Confidence, claim state, evidence traceability, and object-viewer behavior are unchanged.

## Release plan
Validate, merge directly to remote `main` under the user's explicit instruction, back up the current production assets, deploy v176, and verify the public site and service.

## Release outcome
- Merged and pushed to remote `main` at `803b212`.
- Deployed `app.js`, `index.html`, and `styles.css` to `/opt/serbia-poc-ui`.
- Rollback backup: `/home/ubuntu/deploy-backups/kfor-nato-hostile-803b212`.
- Deployed hashes match `deployment/SHA256SUMS-v176.txt`.
- Production serves `app.js?v=173` and `styles.css?v=145`.
- Public assets contain all five hostile mappings and the hostile red diamond-frame CSS.
- `serbia-poc-ui.service` is active; `/api/status` reports the 14,800-row v2.1 dataset.

## Remaining work
None.
