# Checkpoint 010 - Slice 3 VM Deployment

## Date
2026-07-08

## Purpose
Deploy the Slice 3 filter-panel skeleton build to the VM so Product, UX, and Development can review the visible placement and action clarity in the shared review environment.

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
  - `./styles.css?v=64`
  - `./app.js?v=82`
- Verified HTTP response from the VM returned `200 OK`.

## Review request
Product, UX, and Development should review the Slice 3 VM build before Slice 4 begins.

Review focus:
- Filter button is distinct from visibility and close actions.
- Filter panel placement beside the table is understandable.
- Disabled Add/Apply controls clearly communicate that behavior wiring is not part of Slice 3.
- Existing table transparency and readability remain acceptable.
