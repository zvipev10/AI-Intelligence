# Execution Plan

## Status
Accepted through the user's explicit behavior specification and implemented as one low-risk UI slice.

## Slice
- Add a near-bottom calculation and shared follow helper.
- Force following for user-authored messages.
- Apply conditional following to assistant message creation, progress updates, and finalization.
- Preserve the original decision during bulk live-step rerenders.
- Add focused regression tests and bump the browser asset version.

## Validation
- JavaScript syntax check.
- Focused chat-scroll tests.
- Full POC unit-test discovery.

## Rollback
Restore the preceding `app.js` and `index.html` versions.
