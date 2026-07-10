# Checkpoint 014 - Selected layer context in agent prompt

## Date
2026-07-10

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Checkpoint status
Post-merge bugfix complete; selected visible layers are now included in the agent request context.

## Trigger
Product reported that selected layers did not appear to be part of the query/prompt received by the agent.

## What changed
- Added frontend selected-layer context construction for normal prompt submissions.
- The UI now sends selected visible table layers with:
  - layer label
  - layer kind
  - catalog layer ID
  - source type when available
  - original and filtered counts
  - applied filters
  - sample event/location/entity IDs
- The hidden agent prompt now appends a compact "selected layers" context block.
- The request also sends the same context as structured `investigation_state.selected_layers`.
- The server now renders `selected_layers` inside the Hermes instruction state block.
- User-visible chat text remains unchanged; the selected-layer context is only for the agent request.
- Bumped `app.js` cache version from `v=95` to `v=96`.

## Files changed
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `.ai/work/capabilities/multi-layer-query-filtering/checkpoint-014.md`
- `.ai/work/capabilities/multi-layer-query-filtering/status.md`
- `.ai/work/capabilities/multi-layer-query-filtering/handoff-summary.md`

## Validation
- JavaScript syntax:
  - `node --check llm_investigation_orchestrator_serbia_poc/app.js`
- Python syntax:
  - `python -m py_compile llm_investigation_orchestrator_serbia_poc/server.py`
- Server render check:
  - verified `HermesClient.render_investigation_state(...)` includes selected layer label, kind, catalog ID, source type, filtered/original count, applied filter, sample IDs, and the instruction to treat selected layers as narrowing context.

## Not completed
- VM deployment was not performed in this checkpoint yet.
- End-to-end Hermes run was not executed; this change was validated at request/context construction and server rendering level.

## Risk
- The selected-layer context is appended to the hidden agent prompt. This is intentional so the agent receives the context with the analyst question, but the UI keeps the visible user message clean.
- Sample IDs are capped to keep prompt size bounded; large filtered layers are summarized with `sample_ids_are_partial=true`.

## Recommendation
Review the next agent run with selected layers open and verify the tool calls honor the selected layer source/filter context.
