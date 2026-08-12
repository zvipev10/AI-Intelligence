# Checkpoint 001 — Welcome page implementation

## Status

Ready for product/UX/QA review.

## What changed

- Added a bilingual welcome page as the initial view.
- Reused the existing app name, `E / ע` switcher, and live health indicators.
- Rendered all real registry investigations as large ribbons using the existing team roster.
- Kept attention, participation, activity, progress, and milestone content inside each ribbon.
- Added same-document ribbon entry and app-name return navigation.
- Preserved workspace initialization and resized MapLibre after reveal.
- Added demo-only invite/add, join, and request-to-join feedback.
- Added three mocked similar investigations.
- Added desktop, tablet, and narrow responsive ribbon layouts.
- Advanced UI assets to `app.js?v=163` and `styles.css?v=136` with a source manifest.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/test_welcome_page.py`
- `llm_investigation_orchestrator_serbia_poc/test_chat_autoscroll.py`
- `llm_investigation_orchestrator_serbia_poc/test_production_v162_contract.py`
- `llm_investigation_orchestrator_serbia_poc/deployment/README.md`
- `llm_investigation_orchestrator_serbia_poc/deployment/SHA256SUMS-v163.txt`
- Capability artifacts under `.ai/work/capabilities/welcome-page/`

## Validation

- `node --check app.js`
- `python -m unittest discover -p 'test_*.py'` — 127 tests passed.
- `git diff --check`
- Browser smoke checks in Hebrew and English.
- Verified initial welcome state, demo action isolation, ribbon entry, app-name return, map dimensions after reveal, and no browser console errors.
- Verified 390×844 layout: no horizontal overflow and 44px action height.

## Decisions

- Refresh always starts at welcome.
- App name returns to welcome.
- Workspace investigation creation remains unchanged and is hidden only while welcome is active.
- New collaboration actions are explicitly non-persistent demos.

## Known limitations

- Attention, progress, recent activity, milestones, and recommendations are mocked.
- Invitation and participation actions do not persist.
- Existing investigation names are displayed exactly as stored, so a Hebrew name remains Hebrew in English mode.

## Review request

Product/UX should review content density, ribbon hierarchy, and mocked copy. QA should repeat the smoke flow against the review branch before deployment.
