# Parent Capability Issue — Playback deployment recovery

## Purpose

Restore staged playback and prevent deployments from deleting investigation-owned runtime state.

## Owner

Development and QA, explicitly delegated by the user on 2026-09-19.

## Completion criteria

- The remediation is committed and pushed on a reviewable branch.
- Production runs v2.1 and returns a playback next stage.
- Production state is backed up before the deployment.
