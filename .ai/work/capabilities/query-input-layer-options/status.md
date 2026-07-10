# Capability Status

## Capability
Query Input Layer Options (`query-input-layer-options`)

## Current phase
Implementation complete.

## Overall status
Implemented as a focused UI slice on 2026-07-10.

## What changed
- The prompt-area `+` control now opens an options menu.
- `הקלטות` opens the existing saved/replay investigation modal.
- `שכבות` opens the same floating checkbox-window UX as step ingestion, showing only currently open table-capable layers.
- Selecting a layer focuses that already-open layer in the existing additive layer/tab UI.

## Current blockers
None.

## Current risks
- The layer modal currently focuses an already-open layer; it does not yet attach selected layers as structured context to a new natural-language query.

## Next expected artifact
None unless this becomes part of the larger Phase 2 query-builder work.
