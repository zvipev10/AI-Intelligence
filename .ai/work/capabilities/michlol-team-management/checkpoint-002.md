# Checkpoint 002 - VM Deployment

## Date

2026-07-17

## Scope

Deploy Slice 1 of `מכלול` to the shared review VM for Product/UX/QA review.

## VM target

- Public URL: `http://151.145.93.180/`
- Active directory: `/opt/serbia-poc-ui`
- Service: `serbia-poc-ui.service`
- Port: `8769`

## What changed

- Updated the deploy script to upload the project `assets/` directory.
- Deployed current branch `codex/michlol-team-management` to the VM.
- Restarted `serbia-poc-ui.service`.

## Served versions

- `styles.css?v=82`
- `app.js?v=103`

## VM verification

- Deploy script reported service `active`.
- Deploy script verified local VM `/api/status`.
- Public `http://151.145.93.180/api/status` returned `200 OK`.
- Public index contains:
  - `styles.css?v=82`
  - `michlol-team` markup
  - five `assets/michlol/*.png` avatar references
  - `app.js?v=103`
- Public avatar URLs returned HTTP 200:
  - `assets/michlol/moshe.png`
  - `assets/michlol/talia.png`
  - `assets/michlol/naama.png`
  - `assets/michlol/gadi.png`
  - `assets/michlol/yahli.png`
- Public `styles.css?v=82` contains the expected `michlol-*` rules.

## Review needed

Product/UX/QA should review Slice 1 on the shared VM:

`http://151.145.93.180/`

## Notes

No server API or persistence behavior changed. The only deployment-code change was adding `assets/` to the UI deploy directory list so local image assets are included in VM deployments.
