# Checkpoint Summary

## Status
Implementation complete; deployment pending.

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
