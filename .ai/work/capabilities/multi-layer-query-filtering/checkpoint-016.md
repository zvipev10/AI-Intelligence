# Checkpoint 016 - Explicit prompt layer selection

## Date
2026-07-10

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Checkpoint status
Follow-up correction complete on draft PR #18.

## Trigger
Product clarified that:
- the wording `נבחרו שכבות` should appear only after the user intentionally selects layers from the selection window
- layers should be attached to the agent prompt only after that explicit selection, not merely because they are visible on the map or in the results table

## What changed
- Added explicit prompt-layer selection state separate from layer visibility.
- `selectedLayerContextForAgent()` now reads only explicitly selected prompt layers.
- Opening or displaying a layer no longer attaches it to the agent prompt.
- The selected-layers pill now starts with `בחר שכבות` instead of `לא נבחרו שכבות`.
- The selection modal opens with currently open table layers unchecked until the user selects them.
- Submitting the modal records prompt-layer selection without hiding/showing map or table layers.
- Closing/resetting layers clears their prompt-selection state.

## Files changed
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `.ai/work/capabilities/multi-layer-query-filtering/checkpoint-016.md`
- `.ai/work/capabilities/multi-layer-query-filtering/status.md`

## Validation
- JavaScript syntax:
  - bundled Node: `node.exe --check llm_investigation_orchestrator_serbia_poc/app.js`
- Local browser validation at `http://127.0.0.1:8768/`:
  - initial selected-layers pill text was `בחר שכבות בחר שכבות לשאילתה`
  - the initial pill did not include `נבחרו שכבות`
  - opening `טלגרם` as a visible table layer did not change the pill and did not show `נבחרו שכבות`
  - opening the selection modal after adding `טלגרם` showed one unchecked checkbox
  - checking that layer and submitting changed the pill to `שכבה אחת נבחרה טלגרם`

## Risk
- Prompt-layer selection is now independent from layer visibility. This matches the product clarification, but users must explicitly select layers for prompt context even if layers are already visible.

## Recommendation
Product/UX should review the selected-layer pill copy and confirm whether `שכבה אחת נבחרה` is preferred for one layer or whether the plural phrase should be used consistently after selection.
