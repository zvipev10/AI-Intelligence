# Checkpoint 017 - VM deployment for PR 18

## Date
2026-07-10

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Checkpoint status
PR #18 UI build deployed to the review VM.

## Trigger
Product requested deployment to the VM after the explicit prompt-layer selection correction.

## Deployed source
- Branch: `codex/fix-results-composer-layer-selection`
- Commit: `1c01c24 Require explicit prompt layer selection`
- PR: https://github.com/zvipev10/AI-Intelligence/pull/18

## Deployment target
- Public URL: `https://151.145.93.180/`
- Active VM directory: `/opt/serbia-poc-ui`
- Service: `serbia-poc-ui.service`

## What changed on VM
- Overlaid the committed UI package onto `/opt/serbia-poc-ui`.
- Preserved runtime configuration and existing VM storage by not deleting the active directory.
- Restarted `serbia-poc-ui.service`.

## Verification
- VM service:
  - `serbia-poc-ui.service`: `active`
  - `hermes-gateway.service`: `active`
- Public served assets:
  - `styles.css?v=74`
  - `app.js?v=97`
- Public API status:
  - `{"mode": "hermes", "configured": true, "build": "serbia-poc-1"}`
- Local VM API check:
  - `http://127.0.0.1:8769/api/live-steps` returned `{"investigation_steps": []}`

## Notes
- The public `https://151.145.93.180/` endpoint redirects once to `http://151.145.93.180/`; verification followed redirects and confirmed the active served HTML.
- No Hermes or MCP code changes were required for this deployment.
