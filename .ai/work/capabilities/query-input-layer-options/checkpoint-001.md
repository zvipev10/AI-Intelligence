# Checkpoint 001

## Date
2026-07-10

## Scope
Add prompt-area `+` options for saved runs and layer selection.

## Files changed
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `PROJECT_HANDOFF.md`

## Implementation
- Converted the old direct saved-run `+` button into a menu trigger.
- Added menu actions for `הקלטות` and `שכבות`.
- Added a layer-selection modal that shows only currently open table-capable layers, matching the step-ingestion layer selector.
- Bumped cache versions to `app.js?v=94` and `styles.css?v=72`.

## Validation
- `git diff --check` passed.
- `app.js` parsed successfully with Node `vm.Script`.
- Deployed VM smoke with Playwright + system Edge passed:
  - `+` menu opens.
  - `הקלטות` and `שכבות` options render.
  - `שכבות` opens the layer-selection modal.
  - Searching `טלגרם` returns one matching open layer after the layer is already open.
  - Selecting that layer closes the modal, focuses the result overlay, and keeps the existing layer tab.
  - Browser console reported zero warnings/errors.

## Follow-up
Phase 2 query-builder work can later decide whether selected open layers should become structured query context for a new agent run.
