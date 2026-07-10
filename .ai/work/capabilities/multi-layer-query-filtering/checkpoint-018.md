# Checkpoint 018 - Hide prompt layer pill until selected

## Date
2026-07-10

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Checkpoint status
Follow-up correction complete on draft PR #18.

## Trigger
Product reported that the selected-layers mention still appeared in the query composer before the user selected layers, and requested a small `x` so the user can remove the option after regret.

## What changed
- The selected-layers pill is hidden by default.
- The pill appears only after the user opens the `+` menu, selects layers in the layer-selection window, and submits the selection.
- Added a small `×` control inside the selected-layers pill.
- Clicking or keyboard-activating `×` clears the prompt-layer selection and hides the pill.
- Clearing the prompt-layer selection does not hide or close currently visible map/table layers.
- Bumped cache versions:
  - `styles.css?v=75`
  - `app.js?v=98`

## Files changed
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `.ai/work/capabilities/multi-layer-query-filtering/checkpoint-018.md`
- `.ai/work/capabilities/multi-layer-query-filtering/status.md`

## Validation
- JavaScript syntax:
  - bundled Node: `node.exe --check llm_investigation_orchestrator_serbia_poc/app.js`
- Local browser validation at `http://127.0.0.1:8768/`:
  - initial composer served `styles.css?v=75` and `app.js?v=98`
  - selected-layers pill was hidden on initial load
  - opening `טלגרם` as a visible layer kept the pill hidden
  - opening the layers window through `+` showed the checkbox unchecked
  - selecting `טלגרם` and submitting showed `שכבה אחת נבחרה טלגרם ×`
  - clicking `×` hid the pill again while leaving the visible layer tab open
  - browser console reported no warnings or errors

## Risk
- The only entry point for adding prompt-layer selection when none is selected is now the `+` menu, by design.

## Recommendation
Deploy this correction to the VM and have Product re-check the composer empty state and clear-selection behavior.
