# Checkpoint 004 - Three-dot Outside-tap Dismissal

## Date

2026-07-17

## Request

When the three-dot teammate control is expanded, tapping or clicking elsewhere on the screen should return the control to its unpressed/closed state.

## What changed

- Added one document-level `pointerdown` listener.
- The listener finds an open `details.michlol-more` control and removes its `open` attribute when the pointer target is outside that control.
- Pointer interactions inside the expanded teammate list do not close it, so its contents remain usable.
- Bumped the application script cache key from `app.js?v=103` to `app.js?v=104`.
- No Graphify tools, output, or context were used.

## Validation

- `node --check llm_investigation_orchestrator_serbia_poc/app.js` passed.
- `git diff --check` passed.
- Automated browser interaction smoke could not run because the available local Playwright installations were incomplete (`playwright` missing in the project and `playwright-core` missing in the bundled runtime).

## Manual acceptance case

1. Tap the three-dot control and confirm the additional teammates appear.
2. Tap anywhere outside the control and confirm the list closes and the three-dot control is no longer pressed/open.
3. Reopen it and tap within the expanded teammate list; confirm the list remains usable.

## Deployment

Not deployed as part of this checkpoint.

## Review needed

Product/UX/QA should validate the outside-tap behavior after deployment.
