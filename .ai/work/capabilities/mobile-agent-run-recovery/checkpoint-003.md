# Checkpoint 003 — request-scoped mobile recovery

## Trigger

Production evidence showed that a newly submitted message could briefly render steps from an earlier Talia run, and an app-resume recovery could finalize an empty response card.

## Root cause

The live-step endpoint was scoped only by agent and read a shared audit window. A new browser request therefore had no ownership boundary for progress events. The direct and recovered completion paths also accepted an empty answer as a successful result.

## Resolution

- Add `client_request_id` to live-step polling.
- Preserve the routed agent and request start time in the server recovery registry.
- Filter live audit records from that request's start time.
- Reject blank direct and recovered completion payloads.
- Generate a localized server fallback when Hermes returns no answer and no audit records.

## Verification

- Focused recovery and UI suite: 27 tests passed.
- JavaScript syntax check passed.
- Python compilation passed.
- Source manifest contract passed.
