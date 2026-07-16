# Capability Brief

## Capability Name
Investigation Memory

## Capability Slug
investigation-memory

## Current Status
See `status.md` for operational owner, blockers, and next action.

## User Problem
Analysts can create and switch investigations, but selecting an existing investigation currently restores only its identity. The system does not preserve user-curated investigation context, selected meaningful results, or memory-saved layers with their filters.

## Business Goal
Let analysts intentionally preserve important investigation context so future agent prompts and reopened investigations start from the analyst-approved memory rather than an empty workspace or full raw chat replay.

## Target Users
- Analysts using the Serbia / North Kosovo investigation workspace.
- Users who build evidence context through chat results, opened layers, and applied filters.

## Proposed Behavior
- Investigation memory is server-side, not only browser-local.
- Memory is updated only by explicit user action.
- Chat/result memory is saved only when the user decides the current result is important.
- Layer memory is saved only when the user explicitly saves a specific opened layer.
- When selecting an existing investigation, saved memory is loaded.
- Memory-saved layers are reopened automatically and restored with their saved applied filters.
- Future agent prompts receive the loaded investigation memory as context.

## MVP Scope
- Add server-side memory storage foundation.
- Store one JSON memory document per investigation.
- Support listing investigations with memory metadata.
- Support loading memory by `investigation_id`.
- Support replacing/saving an investigation memory payload.
- Define memory sections for manually saved chat summaries and manually saved layers.

## Non-Goals
- Automatic chat summarization.
- Automatic layer capture.
- Memory review/edit UI.
- Full chat transcript restoration.
- Full workspace DOM/state restoration.
- Multi-user authorization model.

## Acceptance Criteria
- Server can persist an investigation memory document by `investigation_id`.
- Server can return an empty memory document for a valid investigation with no saved memory yet.
- Server can list persisted investigation memories.
- Memory document includes `chat_summaries` and `layers` arrays.
- Invalid investigation IDs are rejected.
- Memory writes are atomic.

## Risks
- Future layer restore must refetch rows instead of storing full layer rows to avoid stale data and oversized memory files.
- Server-side persistence will need ownership/authorization review before production use.
- Future summarization quality depends on a strict schema and explicit user-triggered save action.

## Proposed Execution Checkpoints
1. Server-side memory store foundation.
2. Manual save chat/result to memory.
3. Manual save layer with filters to memory.
4. Load memory on investigation selection and reopen saved layers.
5. Include loaded memory in future agent prompts.
