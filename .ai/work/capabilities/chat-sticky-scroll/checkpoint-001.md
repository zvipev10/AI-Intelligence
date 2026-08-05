# Checkpoint Summary

## Status
Complete and deployed.

## Changes
- Added a 96-pixel near-bottom threshold.
- User messages always force the conversation to the bottom.
- Assistant messages, live steps, and final answers follow conditionally.
- Bulk live-step replacement preserves its pre-update scroll decision.
- Browser asset version advanced to `app.js?v=134`.

## Files
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/test_chat_autoscroll.py`

## Checks
- `node --check app.js`
- Focused UI tests: 55 passed.
- Full POC suite: 118 passed.
- All three VM services reported `active` after deployment.
- Public HTTPS serves `app.js?v=134`.
- Public JavaScript contains the 96-pixel threshold, forced user-message following, and bulk-step scroll preservation.
- Public `app.js` SHA-256: `cb4700752e69237f2e4891ed6b45a1a5ece611517f89baee1ecb940113363391`.

## Rollback Files
- `/opt/serbia-poc-ui/app.js.backup-20260804-2252-chat-scroll`
- `/opt/serbia-poc-ui/index.html.backup-20260804-2252-chat-scroll`
