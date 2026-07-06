# Execution Plan

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Goal
Allow users to select independent result layers and add, edit, remove, and apply per-layer free-text filters without changing other selected layers.

## Context used
- `.ai/work/capabilities/multi-layer-query-filtering/capability-brief.md`
- `.ai/work/capabilities/multi-layer-query-filtering/developer-review.md`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- Relevant selectors in `llm_investigation_orchestrator_serbia_poc/styles.css`

## Approved scope
- Client-side MVP filtering over already-loaded `layer.items`.
- Entities, Locations, and event-source layers.
- Dynamic field discovery from layer rows.
- Free-text contains matching.
- AND logic across filters in one layer.
- Separate draft and applied filters per layer.
- Empty-value validation before Apply.
- Existing X close behavior remains the layer close/removal action.

## Non-goals
- Backend/MCP filtering.
- OR logic.
- Nested filter groups.
- Saved filters or templates.
- Dropdown/autocomplete values.
- Type-specific operators.
- Admin-configured fields.
- Redesign of the whole result workspace.

## Proposed approach
Add small filter model helpers in `app.js` before extending the UI:
- Ensure each layer has `draftFilters`, `appliedFilters`, `filterError`, and `filterDirty`.
- Discover filter fields by inspecting row object keys on the active layer.
- Normalize text by stringifying values, lowercasing, trimming, and removing combining marks/diacritics.
- Render a filter panel in the raw results overlay for the active table layer.
- Apply filters only when the active layer's Apply button is clicked.
- Use `filteredItemsForLayer(activeLayer)` inside existing table rendering branches.

Keep existing table branches by replacing direct `activeLayer.items` reads with the derived visible item list where appropriate. Keep close, visibility, minimize, and raw overlay close behavior unchanged except that closing a layer naturally removes its filter state with the layer object.

## Files/services likely affected
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`

## Data/API changes
None for MVP.

## UX changes
- Add a per-active-layer filter panel beside the raw results table.
- Show draft filter rows with field select, free-text input, remove control, Add filter, Apply, and Cancel/Revert controls.
- Show inline validation when Apply is attempted with an empty filter value.
- Indicate unapplied filter changes.
- Show active filters/count near the current active layer context.

## Test plan
- Manual browser smoke test through the static/server UI.
- Verify existing investigation result rendering still works.
- Verify layer tabs, active layer selection, visibility toggle, close action, raw overlay minimize, and raw overlay close still work.
- Verify filter behavior against event-source, entity metadata, and location metadata layers.
- Verify empty value validation, no-results rendering, Hebrew/English contains, AND logic, draft-vs-applied behavior, and filter removal.

## Execution slices

### Slice 1
Goal: Add filter state/model helpers without visible behavior changes.
Expected changes:
- Add helper functions for filter state, field discovery, text normalization, value formatting, matching, and derived filtered rows.
- Ensure new layers receive empty filter state in `addResultLayers()`.
Risk: Low.
Reviewer: Development.
Stop after slice? No.

### Slice 2
Goal: Add filter panel skeleton beside the existing table.
Expected changes:
- Add filter panel container in `index.html`.
- Update raw overlay layout CSS.
- Render active layer name, available fields empty state, Add filter, Apply, and validation placeholders.
Risk: Medium because it affects the raw results workspace layout.
Reviewer: UX/Product.
Stop after slice? Yes.

### Slice 3
Goal: Implement draft filter editing.
Expected changes:
- Add delegated handlers for add, field change, value input, remove, and cancel/revert.
- Track dirty state per active layer.
- Preserve applied results until Apply.
Risk: Medium.
Reviewer: Development/QA.
Stop after slice? No.

### Slice 4
Goal: Apply filters to table rendering.
Expected changes:
- Validate non-empty filter values on Apply.
- Copy draft filters to applied filters.
- Use contains + AND matching to derive table rows.
- Update no-results messages and count display.
Risk: Medium because it changes visible table behavior.
Reviewer: Product/QA.
Stop after slice? Yes.

### Slice 5
Goal: Cross-layer and regression cleanup.
Expected changes:
- Validate independence across selected layers.
- Verify Entities, Locations, and event-source layers consistently support filters.
- Polish dirty/active-filter indicators and edge cases.
- Create checkpoint summary.
Risk: Medium.
Reviewer: QA/Product.
Stop after slice? Yes.

## Stop conditions
Stop before implementation if Product/UX rejects the beside-table filter panel placement, requires translated field labels for MVP, or requires backend filtering.

Stop during implementation if the existing raw overlay layout cannot fit the filter panel without breaking table readability on normal desktop widths.

Stop before merging if layer filtering changes map/timeline semantics unexpectedly. The MVP should apply to displayed table results first; map/timeline filtering should be explicitly decided before changing those views.

## Rollback/fallback notes
- The feature can be rolled back by removing filter state helpers, filter panel markup/styles, and filter event handlers.
- Because MVP filtering is client-side only, rollback does not require data migration or backend deployment.
- If performance is poor on large layers, fallback to hiding the filter panel behind a disabled state for oversized layers while preserving current table behavior.

## Required approval before implementation
- Product/UX confirmation of panel placement beside the existing results table.
- Product decision on tab count display: filtered count, total count, or both.
- Product decision on raw field names vs translated labels.
- Architecture/development confirmation that client-side filtering is acceptable for MVP layer sizes.
