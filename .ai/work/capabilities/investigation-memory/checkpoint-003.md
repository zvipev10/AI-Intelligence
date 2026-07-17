# Checkpoint Summary

## Checkpoint
Checkpoint 003 - Slice 3

## Capability
Investigation Memory (`investigation-memory`)

## Checkpoint Status
Complete - ready for developer/product/UX review.

## Slice Goal
Add an explicit user action to save an opened layer with its current applied filters into server-side investigation memory.

## Product Review Follow-Up Included
- Product comment from Slice 2: the `שמור לזיכרון` final-answer button should look exactly like the nearby final-answer buttons.
- Resolution: removed the special green styling; the memory button now shares the same visual treatment as the adjacent final-answer buttons.

## What Changed
- Added a server append endpoint for manual layer/filter memory saves.
- Added a compact bookmark action inside each table layer tab.
- Saved only lightweight layer metadata and filter state, not layer row payloads.
- Marked a layer as saved in-session after a successful save.

## Files Changed
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `.ai/work/capabilities/investigation-memory/status.md`
- `.ai/work/capabilities/investigation-memory/checkpoint-003.md`

## User Flow
1. User opens a layer in the evidence/table overlay.
2. User applies filters if needed.
3. User clicks the bookmark icon in the layer tab.
4. Browser posts the current investigation id/name and lightweight layer metadata to `/api/investigation-memory/layer`.
5. Server appends a `layer_filter_state` item to that investigation memory.
6. The bookmark action shows the saved state for that layer in the current session.

## Stored Layer Shape
Each saved layer item includes:
- `id`
- `kind`
- `saved_at_utc`
- `source`
- `layer_id`
- `label`
- `layer_kind`
- `catalog_layer_id`
- `data_id`
- `source_id`
- `source_label`
- `source_type`
- `original_count`
- `filtered_count`
- `applied_filters`
- `sample_ids`

## Decisions Made
- Layer memory save remains manual only.
- The UI sends metadata/filter state only; the server appends it to existing memory.
- Full layer rows are not stored in memory.
- Restore is deferred to Slice 4 and should refetch rows from source/catalog data.

## Tests / Checks
- Python syntax check:
  - `C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m py_compile llm_investigation_orchestrator_serbia_poc\server.py`
- Whitespace check:
  - `git diff --check`
- Local API smoke on `http://127.0.0.1:8781`:
  - `POST /api/investigation-memory/layer` saved layer/filter metadata.
  - `GET /api/investigation-memory?id=investigation-slice3-smoke` loaded the appended layer memory.
  - Confirmed saved shape includes catalog layer id, `source_type`, applied filters, counts, and sample IDs.
  - Invalid investigation ID returned `400`.
  - Removed the generated smoke-test memory file after validation.
- Browser load check on `http://127.0.0.1:8781/`:
  - Core app controls rendered.
  - New memory button CSS was present.
  - Browser console had no error logs on load.
- JavaScript syntax check with `node --check` was not run because Node is not installed in this environment.

## Not Completed Yet
- Load memory on investigation selection.
- Reopen memory-saved layers with filters.
- Agent prompt memory integration.

## Risks / Open Questions
- UX/product should confirm the bookmark icon is clear enough as the layer-save action.
- Restoring non-catalog/result-derived layers in Slice 4 may require a fallback if no catalog source exists.
- Production authorization is not addressed in this POC slice.

## Review Requested From
- Development
- Product
- UX

## Continue / Pause Recommendation
Pause after validation for review before Slice 4.

## Next Planned Slice
Slice 4: Load memory and reopen saved layers.
