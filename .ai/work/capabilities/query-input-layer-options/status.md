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
- `שכבות` opens a new layer-selection modal backed by the existing layer catalog.
- Selecting a layer uses the existing `openCatalogLayer()` flow, so opened layers appear in the same additive layer/tab system.

## Current blockers
None.

## Current risks
- The layer modal opens layers directly; it does not yet attach selected layers as structured context to a new natural-language query.

## Next expected artifact
None unless this becomes part of the larger Phase 2 query-builder work.
