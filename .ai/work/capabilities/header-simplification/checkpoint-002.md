# Checkpoint 002 — VM deployment

## Status

Deployed and verified

## Publishing

- Branch: `codex/header-simplification-latest`
- Implementation commit: `4af81c2`

## Deployment

- Target: `/opt/serbia-poc-ui`
- Service: `serbia-poc-ui.service`
- Backup: `/opt/serbia-poc-ui.backup-header-20260808T140508Z`
- Deployment method: focused static slice for `index.html`, `styles.css`, and `app.js`.

The full-package deployment stopped during local staging because Windows could not open one long historical-data path. It stopped before replacing the VM root. The focused slice was then used because this capability changes only three static files.

## VM verification

- Service: active
- Listener: `0.0.0.0:8769`
- `/api/status`: HTTP 200, Hermes configured, dataset v2.1, 14,800 rows
- Public endpoint: reachable after its existing HTTPS-to-HTTP redirect
- Public assets: `styles.css?v=131`, `app.js?v=141`
- Deployed browser: `E`/`ע` present, dataset ready, Hermes ready, localized accessible names, no console errors, no horizontal overflow

## Rollback

Restore the three static files or the complete UI directory from `/opt/serbia-poc-ui.backup-header-20260808T140508Z`, then restart `serbia-poc-ui.service`.
