# Checkpoint 003 — Draft exploration composer

## Status

Implemented, deployed, and verified in production.

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

Deployed through the targeted three-asset procedure. Production serves `app.js?v=164` and `styles.css?v=137`, and deployed hashes match `deployment/SHA256SUMS-v164.txt`.

Backup: `/opt/serbia-poc-ui-backups/welcome-draft-composer-20260812T101820Z`.

Production verification covered Hebrew RTL copy and placement, visible add/send controls, no horizontal overflow, the existing switch to English LTR with the English placeholder, HTTP 200 for both locale URLs, and HTTP 200 for `/api/investigations`. The live submit action was not invoked during smoke testing to avoid creating test production data; its end-to-end behavior was verified locally before deployment.

## Follow-up participant-count update

The first two mocked similar-investigation participant counts were changed from 8 and 12 to 2 and 3. The candidate advances to `app.js?v=165`; production deployment evidence will be recorded after verification.
