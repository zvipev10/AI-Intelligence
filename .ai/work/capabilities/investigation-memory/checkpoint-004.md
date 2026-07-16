# Checkpoint Summary

## Checkpoint
Checkpoint 004 - Slice 4

## Capability
Investigation Memory (`investigation-memory`)

## Checkpoint Status
Complete - ready for developer/product/UX/QA review.

## Slice Goal
Load saved memory when an investigation is selected and reopen saved memory layers with their saved filters.

## What Changed
- Added frontend investigation memory loading state.
- Load memory on initial boot for the active investigation.
- Load memory whenever the user selects an investigation.
- Reopen saved catalog-backed layers by refetching rows through the existing catalog layer API.
- Reapply saved filters as both applied and draft filters.
- Preserve saved result-derived layers as context-only memory when they cannot be visually reconstructed from a catalog source.

## Files Changed
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `.ai/work/capabilities/investigation-memory/status.md`
- `.ai/work/capabilities/investigation-memory/checkpoint-004.md`

## User Flow
1. User selects an investigation from the investigation selector.
2. UI resets the current workspace.
3. UI loads `/api/investigation-memory?id=<investigation_id>`.
4. For saved layers with `catalog_layer_id`, UI refetches rows from `/api/layers/<id>/rows`.
5. UI opens those layers and reapplies saved filters.
6. Saved layers without a catalog source remain available to the agent as context but are not visually reconstructed.

## Decisions Made
- Restore refetches rows instead of storing/restoring full row payloads.
- Saved filters are restored as both `appliedFilters` and `draftFilters`.
- Restore is best-effort per saved layer; unavailable layers remain in memory context with a restore status.

## Tests / Checks
- Python syntax check:
  - `C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m py_compile llm_investigation_orchestrator_serbia_poc\server.py`
- Whitespace check:
  - `git diff --check`
- Browser restore smoke on `http://127.0.0.1:8781/`:
  - Created a real UI investigation.
  - Saved memory for that investigation with a catalog-backed layer.
  - Reloaded the app with that investigation active.
  - Confirmed one saved layer tab reopened.
  - Confirmed the saved-memory bookmark state appeared.
  - Confirmed restored evidence rows rendered.
  - Browser console had no error logs.
- Removed generated smoke-test memory files after validation.

## Not Completed Yet
- Full final QA acceptance.
- Production authorization/ownership model.

## Risks / Open Questions
- Product/UX should confirm context-only treatment is acceptable for result-derived saved layers.
- Restored layers use current catalog data, so counts may differ from the moment the layer was saved.

## Review Requested From
- Development
- Product
- UX
- QA

## Continue / Pause Recommendation
Review together with `checkpoint-005.md`.

## Next Planned Slice
Final QA/acceptance and handoff.
