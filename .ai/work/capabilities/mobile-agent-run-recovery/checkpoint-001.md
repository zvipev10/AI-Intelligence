# Checkpoint 001 — mobile agent-run recovery

## Problem

Mobile browsers can suspend or discard the long-lived `/api/investigate` response while Hermes continues server-side. Returning to the tab therefore displayed a false “real agent run” failure.

## Correction

- Each submission carries a stable `client_request_id`.
- The server retains running, completed, or failed results for 30 minutes.
- `GET /api/investigate-result?id=...` recovers the original run without duplicating it.
- A hidden client waits for visibility and then reconnects for up to three minutes.
- Broken response pipes no longer turn a completed server run into another response error.

## Validation

- Recovery state, expiry, invalid IDs, and frontend wiring have automated tests.
- JavaScript and Python syntax checks pass.
- Existing welcome, scroll, and canonical-source contracts remain covered.
