# Checkpoint 007 - Slice 2 VM Deployment

## Date
2026-07-08

## Purpose
Deploy the current Slice 2 build to the VM so Product can review the implemented presentation/filter model plumbing in the real review environment.

## Files deployed
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`

## VM target
- Host: `151.145.93.180`
- App directory: `/opt/serbia-poc-ui`
- Service: `serbia-poc-ui.service`
- Public review URL: `http://151.145.93.180/`

## Verification
- Uploaded the three UI assets to the VM.
- Copied the assets into `/opt/serbia-poc-ui`.
- Restarted `serbia-poc-ui.service`.
- Verified `systemctl is-active serbia-poc-ui.service` returned `active`.
- Verified deployed `index.html` references:
  - `./styles.css?v=63`
  - `./app.js?v=81`
- Verified HTTP response from the VM returned `200 OK`.

## Review request
Product approved the VM build for unchanged visible behavior and overall readiness to proceed to Slice 3 on 2026-07-08.

Development and UX should still review `checkpoint-006.md` before Slice 3 begins, because Slice 2 introduced the shared filter/presentation plumbing that future visible controls will use.
