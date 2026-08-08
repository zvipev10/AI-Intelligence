# Checkpoint 002 — VM deployment

## Status

Deployed and verified

## Publishing

- Branch: `codex/agent-step-collapse`
- Implementation commit: `74a8d37`

## Deployment

- Target: `/opt/serbia-poc-ui`
- Service: `serbia-poc-ui.service`
- Static rollback backup: `/opt/serbia-poc-ui.backup-agent-steps-20260808T142346Z`
- Deployed files: `index.html`, `styles.css`, `app.js`

## Verification

- Service active and listening on port 8769.
- `/api/status`: Hermes configured, dataset v2.1, 14,800 rows.
- Public assets: `styles.css?v=132`, `app.js?v=142`.
- Public page loads without console errors or horizontal overflow.
- Disclosure CSS and renderer are present in deployed assets.
- A pre-deployment live Hermes run validated six collapsed steps and full expansion using the identical committed assets.

## Rollback

Restore the three static files from `/opt/serbia-poc-ui.backup-agent-steps-20260808T142346Z`, then restart `serbia-poc-ui.service`.
