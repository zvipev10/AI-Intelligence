# QA Review

## Status

Ready for execution under the user's explicit end-to-end authorization.

## Required checks

- Verify the deployer no longer removes the UI root and excludes mutable paths from its payload.
- Verify the canonical manifest is staged.
- Verify the installed unit exposes v2.1.
- Verify `/api/status` and `/api/playback` on the VM.
- Confirm the UI's playback failure text becomes visible when the request rejects.

## Regression focus

Playback next/reset visibility, active workstream reevaluation, and existing investigation/workstream/saved-question persistence.
