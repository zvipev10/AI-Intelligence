# Execution Plan — resume recovery and live-step disclosure state

## Review gate

The user explicitly requested implementation, deployment, push, and merge. Product and UX decisions are therefore treated as delegated for this focused regression fix.

## Acceptance criteria

1. Switching away from and back to the app during a run does not create a fake Hermes/reconnection research step.
2. A genuinely failed or stalled direct request can still recover by `client_request_id`.
3. A research step expanded by the analyst remains expanded when later live steps arrive.
4. Desktop and mobile use the same behavior.

## Implementation

- Add a short grace period after `visibilitychange`/`pageshow`; recover only if the direct request remains unsettled.
- Keep recovery operational status out of the numbered research-step list.
- Snapshot expanded step numbers before rebuilding live steps and restore them afterward.
- Bump the frontend asset version and update contract tests and canonical hashes.

## Risk and rollback

Low-risk, frontend-only behavior change. Roll back the single release commit if mobile recovery regresses.

