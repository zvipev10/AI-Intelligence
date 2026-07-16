# Checkpoint Summary

## Checkpoint
Checkpoint 005 - Slice 5

## Capability
Investigation Memory (`investigation-memory`)

## Checkpoint Status
Complete - ready for developer/product/QA review.

## Slice Goal
Provide saved investigation memory to the agent as context when the user asks a new question.

## What Changed
- Normalize loaded saved memory into a compact agent-context shape.
- Include saved memory in `investigation_state.saved_memory`.
- Send saved memory for normal prompts and continuation prompts.
- Render saved chat summaries and saved layer/filter memory in the Hermes prompt state block.

## Files Changed
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `.ai/work/capabilities/investigation-memory/status.md`
- `.ai/work/capabilities/investigation-memory/checkpoint-005.md`

## Agent Context Shape
`investigation_state.saved_memory` includes:
- `chat_summaries`
  - prompt
  - answer summary / preview
  - source run id
  - recommended view
  - step count
  - evidence IDs
- `layers`
  - label/kind/source metadata
  - catalog/data/source IDs
  - counts
  - applied filters
  - sample IDs
  - restore status

## Decisions Made
- Saved memory is passed only after explicit user saves.
- Saved memory is compacted client-side before sending to `/api/investigate`.
- The server renders memory into the existing `investigation_state` prompt block rather than adding a separate API contract.

## Tests / Checks
- Python syntax check:
  - `C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m py_compile llm_investigation_orchestrator_serbia_poc\server.py`
- Whitespace check:
  - `git diff --check`
- Server prompt renderer smoke:
  - Called `HermesClient.render_investigation_state(...)` with `saved_memory`.
  - Confirmed saved-memory Hebrew prompt block renders.
  - Confirmed saved evidence IDs and saved layer catalog IDs render into the prompt state.
- Browser load/restore smoke also confirmed no console errors after memory-loading code paths ran.

## Not Completed Yet
- Full final QA acceptance.
- Production authorization/ownership model.

## Risks / Open Questions
- Product should validate whether the rendered memory context is detailed enough for expected analyst continuation behavior.
- Prompt size can grow with many saved memory items; current client limits are 8 chat summaries and 12 layers.

## Review Requested From
- Development
- Product
- QA

## Continue / Pause Recommendation
Pause for review and QA before merge.

## Next Planned Slice
Final QA/acceptance and handoff.
