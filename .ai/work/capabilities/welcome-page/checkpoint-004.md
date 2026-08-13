# Checkpoint 004 — Center welcome chat control

## Scope

Fix the welcome-page chat composer so its generic prompt-form margins cannot override its centered layout.

## Changes

- Increased the welcome composer selector specificity while preserving its existing width and vertical spacing.
- Advanced the stylesheet cache key to `styles.css?v=138`.
- Added a regression test for the selector and centered auto margins.

## Risk

Low. The selector targets only the welcome composer and does not change workspace composer behavior.

## Validation

- All 132 discovered POC tests pass.
- JavaScript syntax and Git diff checks pass.
- Local Edge geometry at 1440 px reports `left=360`, `right=1080`, and a center delta of `0`.
- Production serves `styles.css?v=138`; deployed `index.html` and `styles.css` hashes match `SHA256SUMS-v168.txt`.
- Production Edge geometry at 1440 px reports `left=360`, `right=1080`, and a center delta of `0`.
- `serbia-poc-ui.service` remains active.

## Deployment

- Scoped deployment: `index.html` and `styles.css` only.
- Rollback backup: `/opt/serbia-poc-ui-backups/welcome-chat-center-20260813T175451Z`.
