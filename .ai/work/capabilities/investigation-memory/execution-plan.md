# Execution Plan

## Capability
Investigation Memory (`investigation-memory`)

## Plan Status
Accepted for Slice 1 implementation by explicit user request.

## Goal
Add server-side, user-explicit investigation memory. Memory is loaded when selecting an investigation; later slices will reopen memory-saved layers with their saved filters and provide memory to agent prompts.

## Approved Scope
- Manual-only memory updates.
- Server-side persistence.
- Chat/result memory saved only by explicit user action.
- Layer/filter memory saved only by explicit user action.
- Saved memory loaded on investigation selection.
- Saved memory layers reopened with filters in a later slice.

## Non-Goals
- Automatic summarization.
- Automatic layer capture.
- Memory edit/review UI.
- Full chat history or DOM restore.

## Execution Slices

### Slice 1: Server Memory Store Foundation
Expected changes:
- Add server-side `investigations/` JSON storage.
- Add `GET /api/investigations`.
- Add `GET /api/investigation-memory?id=...`.
- Add `PUT /api/investigation-memory`.
- Validate investigation IDs and write memory atomically.

### Slice 2: Manual Chat/Result Memory Save
Expected changes:
- Add explicit save action from an interesting chat/result.
- Add server summary component triggered only by that user action.
- Append structured chat summary memory.

### Slice 3: Manual Layer Memory Save
Expected changes:
- Add explicit layer action to save the opened layer with current applied filters.
- Store layer identity, catalog ID, kind, label, applied filters, counts, and sample IDs.

### Slice 4: Load Memory And Reopen Saved Layers
Expected changes:
- Load memory on investigation selection.
- Reopen memory-saved layers by refetching rows.
- Reapply saved filters as both draft and applied filters.

### Slice 5: Agent Prompt Memory Context
Expected changes:
- Include loaded saved memory in `investigation_state`.
- Render memory into Hermes prompt context as user-saved investigation memory.

### Slice 6: Reconstruct And Present Saved Result Layers
Expected changes:
- Persist typed reconstruction IDs, dataset version, and locale for newly saved layers.
- Add a server presentation endpoint that resolves saved IDs into the standard typed-layer contract.
- Reuse the normal map/table/timeline layer pipeline for automatic restore and explicit presentation.
- Add a read-only agent tool that returns structured present/clarify actions for saved memory-layer IDs.
- Report fully restored, partially restored, unavailable, and ambiguous states.

Explicit exclusions:
- No migration of existing context-only memory records.
- No new automated tests in this slice, per Product instruction.

## Stop Conditions
- Any need for automatic memory capture.
- Any need to store full layer row payloads.
- Any production authorization or multi-user requirement.

## Test Plan
- Python compile check for `server.py`.
- API smoke for save/list/load memory.
- Invalid ID rejection.
- Verify unrelated saved-question endpoints still compile and route.
