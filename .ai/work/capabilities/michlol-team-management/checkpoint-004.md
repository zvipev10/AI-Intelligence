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

Deployed to the shared review VM on 2026-07-17.

- Updated `/opt/serbia-poc-ui/app.js` and `/opt/serbia-poc-ui/index.html` only; existing server configuration and data were preserved.
- Restarted `serbia-poc-ui.service`; it reported `active`.
- VM-local `/api/status` returned a configured Hermes response.
- Public `http://151.145.93.180/` returned HTTP 200 and served `app.js?v=104`.
- Public `app.js?v=104` contains the `details.michlol-more[open]` outside-tap handler.
- The first public request immediately after restart returned a transient HTTP 502; a health check seconds later confirmed the service and public endpoint were healthy.

## Review needed

Product/UX/QA should validate the outside-tap behavior after deployment.
