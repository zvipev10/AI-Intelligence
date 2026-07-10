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
- Added a layer-selection modal that uses the same floating checkbox-window UX as step ingestion and shows only currently open table-capable layers.
- Bumped cache versions to `app.js?v=95` and `styles.css?v=73`.

## Validation
- `git diff --check` passed.
- `app.js` parsed successfully with Node `vm.Script`.
- Deployed VM smoke with Playwright + system Edge passed:
  - `+` menu opens.
  - `הקלטות` and `שכבות` options render.
  - `שכבות` opens the same `step-inject-window` floating shell used by step ingestion.
  - With no open layers, the modal shows `אין שכבות פתוחות לבחירה.` and no options.
  - With no open layers, the submit button is disabled.
  - After opening `טלגרם` through the existing catalog selector, `שכבות` shows exactly one `step-inject-layer-item` row.
  - The row includes the same checkbox, color dot, layer name, and count structure as step ingestion.
  - The open layer checkbox is checked by default.
  - Submitting closes the modal, focuses the result overlay, and keeps the existing layer tab without creating a duplicate.
  - Browser console reported zero warnings/errors.

## Follow-up
Phase 2 query-builder work can later decide whether selected open layers should become structured query context for a new agent run.
