# Capability Brief

## Capability name

Playback deployment recovery

## Capability slug

`playback-deployment-recovery`

## Parent issue

Local draft; no remote issue created.

## Current status

User explicitly requested end-to-end remediation on 2026-09-19.

## User problem

The staged time-slice playback control disappeared, preventing investigators from releasing a new evidence window to agents and active workstreams.

## Proposed behavior

Deployments preserve mutable runtime state, ship the v2.1 playback manifest, run the UI under v2.1 explicitly, and display a visible error if playback state cannot load.

## MVP scope

- Preserve server-owned playback, investigation, workstream, and saved-question state.
- Deploy the canonical staged manifest.
- Pin the systemd UI service to dataset v2.1.
- Make playback fetch failures visible.
- Restore and verify the production service.

## Non-goals

- SSH-key rotation/history remediation.
- Redesign of the playback flow.

## Acceptance criteria

- A repeat deployment does not delete mutable state.
- `/api/status` reports `serbia-poc-v2.1`.
- `/api/playback` returns a next stage for a valid investigation.
- The UI exposes the Next control when a next stage exists and reports fetch failures.

## Risks

Production deployment can restart the UI service. Existing server state may already be missing and requires backup recovery.
