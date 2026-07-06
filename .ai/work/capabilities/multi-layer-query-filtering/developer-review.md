# Developer Review

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Context reviewed
- `.ai/work/capabilities/multi-layer-query-filtering/capability-brief.md`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- Relevant existing style selectors in `llm_investigation_orchestrator_serbia_poc/styles.css`

## Feasibility
Feasible as a client-side MVP within the existing Serbia investigation POC.

The app already builds independent table-capable layers in `state.layers`, assigns `state.activeLayerId`, renders tabs in `renderEvidence()`, and supports per-layer close and visibility actions. Event-source layers, location metadata, and entity metadata already exist as layer objects with `kind`, `items`, `capabilities`, `label`, and stable generated IDs.

The lowest-risk implementation is to add per-layer draft/applied filter state and have `renderEvidence()` derive the active table rows from `layer.items` plus applied filters. This avoids backend/MCP changes for MVP and keeps Apply local to the selected layer.

## Likely affected files/services
- `llm_investigation_orchestrator_serbia_poc/app.js`
  - Add filter state helpers.
  - Initialize filter fields on layer creation.
  - Extend `renderEvidence()` to render filter controls and filtered rows.
  - Add event handlers for add/edit/remove/apply/cancel filter actions.
- `llm_investigation_orchestrator_serbia_poc/index.html`
  - Add a filter panel/container beside the raw results table.
  - Keep existing raw table, layer tabs, minimize, and close controls.
- `llm_investigation_orchestrator_serbia_poc/styles.css`
  - Add layout and control styling for the filter panel, filter rows, validation, dirty state, and no-results state.
- No backend or MCP service changes are recommended for MVP.

## Existing patterns to follow
- Layer model: `state.layers[]` with `id`, `dataId`, `sourceId`, `sourceLabel`, `kind`, `items`, `capabilities`, `visible`, and `color`.
- Layer construction: `buildEventLayers()`, `buildLocationMetadataLayer()`, and `buildEntityMetadataLayer()`.
- Layer lifecycle: `addResultLayers()`, `ensureActiveLayer()`, `[data-layer-close]`, `[data-layer-visibility]`, and `[data-layer-id]` event delegation.
- Table rendering: `renderEvidence()` switches on `activeLayer.kind`.
- UI behavior: single delegated document click handler and direct DOM rendering with escaped HTML.

## Implementation options

### Option 1
Client-side filtering over `layer.items`.

Pros:
- Smallest change.
- No MCP/backend API contract changes.
- Matches MVP requirement that applying filters updates only a selected already-loaded layer.
- Easy to preserve draft vs applied state per layer.

Cons:
- Large layers may become slow if many rows and many filters are active.
- Contains semantics may diverge from backend search if later backend filtering is introduced.

### Option 2
Backend/MCP filtering on Apply.

Pros:
- Better long-term fit for large datasets.
- Can align filtering with server-side search/index semantics.

Cons:
- Requires API design, query contracts, loading/error states, and failure handling.
- Harder to keep event-source, entity metadata, and location metadata behavior consistent without additional backend work.
- Higher risk than the MVP requires.

## Recommended approach
Use Option 1 for MVP: client-side filtering against the active layer's existing `items`.

Recommended per-layer state:

```js
{
  draftFilters: [{ id, field, value }],
  appliedFilters: [{ id, field, value }],
  filterError: "",
  filterDirty: false
}
```

`draftFilters` are edited by the UI. `appliedFilters` are used to derive displayed rows. Apply validates non-empty values, copies normalized draft filters to applied filters, clears the error, and re-renders only the active layer table. Cancel/reopen should reset drafts from applied filters.

Recommended helper functions:
- `createFilterId()`
- `ensureLayerFilterState(layer)`
- `filterableFieldsForLayer(layer)`
- `normalizeFilterText(value)`
- `layerItemMatchesFilters(item, filters)`
- `filteredItemsForLayer(layer)`
- `formatFieldValue(value)`
- `renderLayerFilterPanel(activeLayer, visibleItems)`

Field discovery should dynamically inspect the current layer's `items`, with stable sorting and a fallback empty state when no fields are available. For arrays and nested objects, filtering should stringify values for MVP.

Contains matching should be case-insensitive, trim surrounding whitespace, and remove Hebrew niqqud/combining marks. Hebrew final-letter normalization is optional for MVP unless Product requires stricter Hebrew equivalence.

Duplicate filters should be allowed for MVP unless Product decides otherwise. Duplicate field/value filters are redundant but not harmful, and blocking them adds extra product rules not yet decided.

Closing a layer with X should discard its draft/applied filters with no confirmation, matching the existing close behavior.

## Technical risks
- `renderEvidence()` is already a large function. Adding filtering directly can make it harder to maintain unless small helpers are introduced first.
- `layer.items.length` currently appears in tabs. Product/UX should decide whether this remains total rows, filtered rows, or `filtered / total`. Recommended: show filtered count when filters are applied, with total in a secondary label if space allows.
- Filtering hidden layers needs a clear rule. Recommended: hidden active layers keep filters but render the existing hidden/empty message.
- Dynamic field discovery can surface technical fields that are not useful but is consistent with the MVP requirement that all fields are filterable.

## Data/API considerations
- No data model or API changes for MVP.
- Event-source layers are already derived from `source_type` in `buildEventLayers()`.
- Entity and location metadata layers are already present when result steps include `entity_layers` and `location_layers`.
- If future backend filtering is required, this client model can be mapped to a backend payload of `{ layerId, filters: [{ field, value, operator: "contains" }] }`.

## Security/permissions considerations
- No new permissions are introduced.
- Because all filtering is against already-rendered client-side data, this does not expose data beyond what the current UI already loads.
- Continue escaping rendered values with `escapeHtml()`.

## Performance considerations
- Client-side filtering is acceptable for MVP-sized result layers.
- Filtering should run only on Apply and render, not on every keystroke.
- For large event-source layers, `filteredItemsForLayer()` should avoid deep cloning and only return matching references.
- If layers exceed several thousand rows, add a future checkpoint for indexing, pagination, or backend filtering.

## Test strategy
- Manual browser validation for layer selection, layer close, visibility, and table rendering.
- Focused automated or scripted checks for pure helper behavior if the project has a lightweight JS test path; otherwise isolate helpers enough for future tests.
- Regression smoke via existing server/static UI path.

Test cases:
- Select Entities layer and apply a filter on an entity field.
- Select Locations layer and apply a filter on a location field.
- Select an event-source layer and apply a filter on `event_summary`, `entity_id`, or `location_id`.
- Add two filters to one layer and verify AND behavior.
- Apply filters on one layer and verify another layer is unchanged.
- Edit draft filters without Apply and verify displayed rows do not change.
- Remove a filter and Apply.
- Attempt Apply with an empty value and verify inline validation.
- Verify Hebrew and English contains matching.
- Close a layer with filters and verify no stale state remains.
- Verify no-results after Apply.

## Acceptance criteria improvements
- Define whether tab counts show total rows, filtered rows, or both.
- Define whether duplicate field/value filters should be allowed or blocked.
- Define exact Hebrew normalization expectations beyond case/diacritic handling.
- Define whether raw field names are acceptable for MVP or require display labels.
- Define whether hidden active layers should show filters, table hidden state, or both.

## Proposed execution slices

### Slice 1
Add per-layer filter state helpers and initialize filter state for new and existing layers without changing visible behavior.

### Slice 2
Add the filter panel layout beside the existing results table and render field/value draft controls for the active layer.

### Slice 3
Implement add/edit/remove/cancel/apply filter interactions with empty-value validation and dirty-state indication.

### Slice 4
Apply contains + AND filtering to the active layer table rows and tab count display.

### Slice 5
Regression pass across event-source, entity metadata, location metadata, layer close, visibility, minimize, and no-results behavior.

## Required review gates before coding
- Product/UX should confirm the filter panel placement and count display behavior.
- Product should confirm duplicate-filter behavior.
- Product/UX should confirm raw field names are acceptable for MVP.
- Development can proceed with client-side filtering unless Architecture requires backend filtering for the expected dataset size.

## Open questions for Product / UX / QA / Architecture / Security
- Product/UX: Should tab counts show filtered rows, total rows, or both?
- Product: Should duplicate filters be blocked or allowed?
- Product/UX: Are raw field names acceptable, or should the MVP ship with translated labels?
- QA: Is manual browser validation sufficient for this POC, or should helper-level automated tests be required before implementation?
- Architecture: Are expected result-layer sizes small enough for client-side Apply filtering in the MVP?
