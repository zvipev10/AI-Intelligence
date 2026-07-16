# Checkpoint Summary

## Checkpoint
Checkpoint 002 - Slice 2

## Capability
Investigation Memory (`investigation-memory`)

## Checkpoint Status
Complete - ready for developer/product/UX review.

## Slice Goal
Add an explicit user action to save an interesting chat/result into server-side investigation memory.

## What Changed
- Added a server append endpoint for manual chat/result memory saves.
- Added deterministic server-side summary shaping for saved chat results.
- Added a final-answer button to save the current answer to investigation memory.
- Kept saved questions separate from investigation memory.

## Files Changed
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `.ai/work/capabilities/investigation-memory/status.md`
- `.ai/work/capabilities/investigation-memory/checkpoint-002.md`

## User Flow
1. User asks a question and receives a final answer.
2. User explicitly clicks `שמור לזיכרון`.
3. Browser posts the current investigation id/name, prompt, and result to `/api/investigation-memory/chat-summary`.
4. Server appends a compact `chat_result_summary` item to that investigation memory.
5. Button changes to `נשמר בזיכרון`.

## Stored Chat Summary Shape
Each saved item includes:
- `id`
- `kind`
- `saved_at_utc`
- `source`
- `prompt`
- `answer_summary`
- `answer_preview`
- `source_run_id`
- `recommended_view`
- `step_count`
- `evidence_ids`

## Decisions Made
- Memory save remains manual only.
- Slice 2 uses a compact deterministic summary, not automatic LLM summarization.
- The existing saved-question feature is not reused because investigation memory is a separate capability.
- The browser does not perform a read-modify-write of the whole memory; the server owns append behavior.

## Tests / Checks
- Python syntax check:
  - `C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m py_compile llm_investigation_orchestrator_serbia_poc\server.py`
- Whitespace check:
  - `git diff --check`
- Local API smoke on `http://127.0.0.1:8781`:
  - `POST /api/investigation-memory/chat-summary` saved a compact chat summary.
  - `GET /api/investigation-memory?id=investigation-slice2-smoke` loaded the appended summary.
  - Evidence IDs were extracted from both `event_ids` and answer text.
  - Invalid investigation ID returned `400`.
  - Removed the generated smoke-test memory file after validation.
- JavaScript syntax check was attempted with `node --check`, but Node is not installed in this environment.
- Browser load check on `http://127.0.0.1:8781/`:
  - Core app controls rendered.
  - Browser console had no error logs on load.

## Not Completed Yet
- Manual layer memory save.
- Load memory on investigation selection.
- Reopen memory-saved layers with filters.
- Agent prompt memory integration.

## Risks / Open Questions
- UX/product should confirm the Hebrew button copy and action placement.
- Product should confirm deterministic answer compaction is sufficient for MVP memory.
- Production authorization is not addressed in this POC slice.

## Review Requested From
- Development
- Product
- UX

## Continue / Pause Recommendation
Pause after validation for review before Slice 3.

## Next Planned Slice
Slice 3: Manual layer memory save.
