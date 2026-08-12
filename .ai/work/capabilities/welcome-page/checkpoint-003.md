# Checkpoint 003 — Draft exploration composer

## Status

Implemented and locally validated; pending product/UX review and deployment approval.

## What changed

- Added the existing chat-composer visual treatment between the welcome message and “My investigations.”
- Preserved both existing composer actions: send starts the draft exploration, while add opens the existing attachment/options menu inside the draft workspace and carries over any typed text.
- Added localized prompt copy: `התחל אקספלורציה בחקירת טיוטה...` / `Start exploring in a draft investigation...`.
- Enter without Shift and the send arrow both submit; Shift+Enter remains available for a newline.
- Empty submission keeps focus in the welcome composer.
- A valid submission creates or reuses a localized draft investigation through the existing registry, opens the workspace on the same page, and immediately runs the prompt.
- Advanced candidate assets to `app.js?v=164` and `styles.css?v=137`.

## Validation

- `node --check app.js`
- `python -m unittest discover -p 'test_*.py'` — 129 tests passed.
- `git diff --check`
- Browser: verified Hebrew RTL placement and copy, English LTR copy, matching composer background, no horizontal overflow, draft investigation selection, workspace reveal, and submitted prompt visibility.

## Data and API impact

No new API or model. The feature uses the existing investigation registry and prompt execution path.

## Deployment

Not deployed. Production remains on v163/v136 pending explicit approval.
