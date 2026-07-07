# Developer Review

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Review status
Ready for execution planning.

Prepared on 2026-07-06 as AI-authored draft notes during developer-stage review. Approved by the human developer on 2026-07-07 with the MVP decision that API row loading should have no limit.
Product UX decisions added on 2026-07-07: the filter panel opens from the layer tab, and MVP uses raw field names.

## Reviewer / input source
AI-prepared draft from Codex repository inspection, approved by the human developer.

## Developer-stage outcome
Updated after human developer/product clarification on 2026-07-06 and human developer approval on 2026-07-07.

Approved developer decision:
- Build this as a standalone layer-selection capability, separate from chat, agent runs, and chat-step result loading.
- Add or use an API endpoint to fetch rows for selected layers.
- Reuse the existing presentation components for opened layer tabs and expand them to support layer-selection results.
- Filtering must be available for any opened layer tab, regardless of whether the tab was opened by the standalone layer selector or by a later/legacy result path.
- For MVP, do not add a row limit to layer row loading.
- Product-owned UX decision: open the filter panel from the layer tab.
- Product-owned UX decision: use raw field names for MVP filter fields.
- Product-owned UX decision: add a new standalone layer selection component for Entities, Locations, and Events grouped by `source_type`. Existing layer tabs are for already opened layers, not for discovering/selecting new layers.
- Product-owned UX decision: the standalone layer selection component should be a compact search/autocomplete input, potentially on the map surface, not a full list of all layers above the map. Selecting an autocomplete result opens the layer in the results panel/opened-layer tabs.

This artifact is approved for execution planning.

## Context reviewed
- `.ai/work/capabilities/multi-layer-query-filtering/capability-brief.md`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`

## Code inspection notes
- `state.layers` and `state.activeLayerId` are already the right ownership boundary for selected layers.
- `buildEventLayers(events)` already creates one selectable event layer per `source_type`.
- `buildLocationMetadataLayer(items)` and `buildEntityMetadataLayer(items)` already create table-capable metadata layers for the MVP layer families.
- `addResultLayers(...)` already preserves existing layers and reactivates matching source layers instead of replacing all selected layers.
- `renderEvidence()` is the main integration point for layer tabs and table rows. It should delegate filtering to helpers rather than absorb all filter logic inline.
- `[data-layer-close]` already removes a layer from `state.layers`; this should remain the only close/remove-layer action.
- `[data-layer-visibility]` already controls visibility separately from close and filter editing.
- The raw overlay markup currently has only tabs/actions plus one table container; a side filter panel needs a small HTML/CSS layout addition.

## Product requirements understood
The product brief asks for a guided workflow where users can select independent query layers and apply per-layer field/value filters.

Product clarification from the human developer:
- This capability is totally separate from chat and agent behavior.
- It must not depend on layers/results loaded from chat answers or chat steps.
- It should reuse the same presentation components and expand them with the results of layer selection.
- Filtering should be allowed for any opened layer tab.
- Applied filters should affect all presentations for that opened layer tab, including table, map, and timeline where the layer supports those capabilities.
- Layer rows should be fetched through an API-based path.

MVP layer families:
- Entities
- Locations
- Event-source layers derived from available `source_type` values

MVP filtering behavior:
- Filters belong to a specific selected layer.
- All fields on the selected layer are available for filtering.
- A filter has a selected field and a free-text value.
- Empty values are blocked before Apply.
- Contains matching is used.
- Multiple filters on one layer use AND logic.
- Draft edits do not change displayed results until Apply.
- Applying filters affects only that layer.
- Existing filters can be reopened, edited, removed, and applied later.
- Active filters appear beside the existing results table.
- Layer close remains the existing X action and is separate from filter editing.

Important non-goals:
- OR logic, nested groups, cross-layer filtering, typed operators, saved templates, autocomplete values, admin field configuration, or replacing the existing results table.

## Feasibility
Feasible, but not as a purely client-side filtering feature over chat-loaded result data.

The current frontend already has useful presentation primitives:
- `buildEventLayers(events)` groups events by `source_type`.
- `buildLocationMetadataLayer(items)` creates the location metadata layer.
- `buildEntityMetadataLayer(items)` creates the entity metadata layer.
- `addResultLayers(...)` keeps previously selected layers and activates a preferred layer.
- `renderEvidence()` renders the active layer table and layer tabs.
- Click handling already supports layer visibility, close, active tab selection, minimizing, and clearing.

However, the new standalone layer-selection flow needs an API-backed layer catalog and row loading path. Filtering can still be applied to loaded rows in the presentation layer for MVP, but row acquisition must not depend on agent/chat results.

## Likely affected files/services
- `llm_investigation_orchestrator_serbia_poc/app.js`
  - Add standalone layer catalog/open-layer state and actions.
  - Add API-backed row loading for selected layers.
  - Add per-layer filter state defaults when layers are created.
  - Add helper functions for field discovery, filter matching, draft/applied filters, and filtered items.
  - Extend `renderEvidence()` to render filter controls beside the existing results table and to render filtered rows instead of raw `layer.items`.
  - Update map/timeline item selection helpers to use applied filtered items for opened layers where those presentations are supported.
  - Extend document click/input/change handlers for add/edit/remove/apply/cancel interactions.
- `llm_investigation_orchestrator_serbia_poc/server.py`
  - Add or expose API endpoint(s) for layer catalog and layer rows, depending on what existing data endpoints can already provide.
- `llm_investigation_orchestrator_serbia_poc/index.html`
  - Add a new compact search/autocomplete layer selection component for Entities, Locations, and Events grouped by `source_type`.
  - Add a container in `rawEventsOverlay` for the filter panel beside the table.
- `llm_investigation_orchestrator_serbia_poc/styles.css`
  - Add layout and control styles for the layer selector, filter panel, validation state, active filter indicators, and responsive behavior.

Backend/API changes are in scope because selected layer rows must come from an API path instead of chat/agent result state.

## Existing patterns to follow
- Keep state in the existing global `state` object and per-layer objects inside `state.layers`.
- Continue using `state.activeLayerId` as the selected table layer.
- Continue using `renderAllViews()` as the broad rerender path and `renderEvidence()` for table-only updates.
- Use data attributes for control actions, matching existing `[data-layer-close]`, `[data-layer-visibility]`, and `[data-layer-id]`.
- Preserve the X close behavior as layer removal only.
- Keep the existing query modal separate. It edits tool/query arguments and currently logs submission only; overloading it for layer filters would mix two concepts and create avoidable UX and state coupling.

## Implementation options

### Option 1: Standalone API-backed layer opening with client-side filtering over loaded rows
Add a standalone layer catalog and open-layer action. Fetch selected layer rows through API endpoint(s), store them on opened layer tabs, and apply `draftFilters`/`appliedFilters` to the loaded rows in the presentation layer.

Pros:
- Fits MVP scope.
- Separates the capability from chat and agent results.
- Keeps filters independent per opened layer tab.
- Makes Apply semantics straightforward.
- Reuses existing table/map/timeline presentation paths.

Cons:
- Requires API work for catalog/row loading.
- Filtering is limited to rows returned by the API request unless the API later supports server-side filter application.
- Large layers may require paging or backend filtering after MVP.

### Option 2: Standalone API-backed layer opening with server-side filtering on Apply
Add a layer catalog and row endpoint, then send draft filters to the backend on Apply so the API returns filtered rows.

Pros:
- Better for large datasets and not-yet-loaded rows.
- Establishes the longer-term filter contract earlier.

Cons:
- More API and state complexity in the first slice.
- Requires a generic field/value filter contract across event, entity, and location layers.
- Needs more QA around API errors, paging, stale results, and server/client matching parity.
- Needs architecture/product review before implementation.

## Recommended approach
Use Option 1 for MVP: standalone API-backed layer opening, with client-side filtering over rows returned for each opened tab.

This is not a chat-result filtering feature. The selected layer's rows must be fetched independently through an API path. The existing `state.layers`, `activeLayerId`, tab rendering, close behavior, and table rendering can still be reused as the presentation model after rows are loaded.

Recommended state shape per layer:

```js
{
  ...layer,
  draftFilters: [],
  appliedFilters: [],
  filterError: "",
  filterPanelOpen: false
}
```

Recommended filter object:

```js
{
  id: "filter-...",
  field: "source_type",
  value: ""
}
```

Implementation notes:
- Add a layer catalog model for selectable layers.
- Add a dedicated compact search/autocomplete layer selection component; do not treat the existing layer tabs as the layer picker.
- Avoid rendering all available layers as a large list above the map.
- Consider placing the search/autocomplete on the map surface, as long as it remains compact and does not obscure important map content.
- Add an open-layer function that fetches rows from the API and creates or updates an opened layer tab.
- Initialize filter state when a tab is opened from the layer selector and when any legacy path creates a tab.
- When an existing layer is re-shown, preserve its filter state.
- Use `layer.items` as immutable source rows and derive the opened layer's active presentation items through a helper such as `itemsForLayerPresentation(layer)`.
- Table, map, and timeline should consume the same applied-filter item set for a layer, while respecting each layer's existing `capabilities`.
- Apply should validate all draft filter values with `trim()`. Empty values should set an inline layer-local error and not modify `appliedFilters`.
- Cancel/reopen should reset `draftFilters` from `appliedFilters`.
- Remove should remove from `draftFilters`; results should only change after Apply, unless Product explicitly wants removing an already-applied filter to apply immediately.
- Display tab counts as filtered count plus optionally original count, for example `12/80`, to avoid hiding that a layer has more rows.
- Duplicate filters should be allowed for MVP unless Product decides otherwise. Duplicate same field/value filters are redundant but harmless under AND semantics.

Recommended matching:
- Convert candidate field values with `String(value ?? "")`.
- For arrays/objects, stringify in a stable user-facing way before matching.
- Use `casefold` equivalent in JS via `toLocaleLowerCase()` or `toLowerCase()` for MVP.
- Backend `normalize_text` currently performs case folding and whitespace compaction only. It does not normalize Hebrew final letters or diacritics, so exact parity does not require extra Hebrew normalization.

Recommended planning assumptions:
- The layer-selection workflow is independent from chat and agent result loading.
- Layer rows are fetched through an API-based path.
- Filters are available for any opened layer tab.
- Applied filters affect all presentations for the opened layer tab, including table, map, and timeline where supported.
- Filtering can run client-side over fetched rows for MVP, while the API contract should allow future server-side filtering/paging.
- For MVP, layer row loading has no row limit.
- A removed filter follows the same draft/apply contract as edited filters; presentations change only after Apply.
- Duplicate filters are allowed for MVP because they are redundant but do not change AND semantics.
- Raw field names are acceptable for the first implementation. Friendly labels/translations can be added after UX review.
- Closing a layer discards that layer's draft and applied filter state with no confirmation.

## Technical risks
- `renderEvidence()` is already a long function with per-kind table branches. Adding filters directly can make it harder to maintain unless helper functions are introduced first.
- Field discovery over raw object keys may expose technical fields that are not meaningful, but the brief explicitly says all fields are filterable for MVP.
- Objects/arrays in entity and location metadata need predictable display/match behavior.
- Map/timeline rendering currently uses visible layer items directly. This must be refactored so supported presentations use the same applied-filter item set as the table.
- The raw events overlay is constrained to 28% height by default. A side filter panel may crowd the table unless the layout is widened carefully or stacks on small heights/screens.

## Data/API considerations
- API-based row loading is required.
- Recommended API shape:
  - `GET /api/layers` returns selectable layer definitions, including `id`, `label`, `kind`, capabilities, and available metadata needed by the UI.
  - `GET /api/layers/:layerId/rows` returns rows for a selected layer tab.
  - Event-source layer ids should represent available `source_type` values.
  - Entities and Locations should return metadata rows compatible with the existing presentation components.
- Event rows already include fields such as `event_id`, `timestamp_utc`, `source_type`, `source_reliability`, `source_reliability_label`, `certainty_level`, `entity_id`, `entity_name`, `location_id`, `location_name`, `location_type`, and `event_summary`.
- Entity and location metadata include nested fields such as aliases, top locations, top sources, and breakdowns. These should be discoverable and matchable, but the table display can remain the existing curated columns.
- For MVP, row endpoints should return all rows for the selected layer with no row limit.
- If future requirements need better performance for large result sets or pagination, add server-side filter parameters to the row endpoint.

## Security/permissions considerations
The new API endpoint must not expose data beyond what the current application is allowed to show. No new permissions are expected for the local POC, but productionizing this pattern would require authorization on the layer catalog and row endpoints.

## Performance considerations
- Client-side contains matching is accepted for MVP even though row loading is unlimited.
- The no-limit MVP decision carries performance risk if selected layers are large.
- Add helpers that compute filtered items for visible/opened layers only when needed by table, map, timeline, or counts.
- If showing filtered counts for all tabs, count computation should be simple and based on existing `layer.items`.
- Server-side filtering should be considered if opened layers regularly contain many thousands of rows.

## Test strategy
Manual browser validation:
- Select/open Entities, Locations, and event-source layers.
- Verify selecting another layer preserves prior layers and filters.
- Add one filter and apply; confirm table, map, and timeline narrow only for that opened layer where those presentations are supported.
- Add multiple filters; confirm AND semantics.
- Edit a draft filter and confirm results do not change until Apply.
- Remove a draft/applied filter and confirm Apply controls when results change.
- Attempt Apply with an empty value and verify inline validation.
- Close a filtered layer with X and verify no filter-edit action occurs.
- Test no-results state after Apply.
- Test Hebrew and English contains matching, including case differences for English.
- Verify existing visibility eye, layer tab selection, minimize, resize, and raw overlay close behavior.

Automated/lightweight checks:
- Add focused JS helper tests if the repo gains a test harness.
- At minimum, run the app locally and perform a smoke flow in the browser.
- Run any existing quality/regression scripts only if they are relevant and practical for the frontend change.

## Acceptance criteria improvements
Recommended clarifications before execution planning:
- State that layer selection is a standalone workflow independent of chat/agent results.
- State which API endpoint(s) provide layer catalog and row data.
- State that MVP filtering affects all presentations for opened tabs, including table, map, and timeline where supported.
- Define duplicate filter behavior. Recommended: allow duplicates for MVP.
- Define whether removing an applied filter updates immediately or only after Apply. Recommended: only after Apply, to preserve the stated draft/apply contract.
- Define field labels. Recommended: raw field names for MVP, with user-friendly labels as a later UX enhancement.
- Define tab count display under filters. Recommended: filtered count with original count visible when filters are applied.

## Proposed execution slices

### Slice 1: Standalone layer catalog and API row loading
- Add or expose API endpoint(s) for layer catalog and selected layer rows.
- Add frontend layer selector state and open-layer action independent from chat/agent results.
- Open Entities, Locations, and event-source layers into existing layer tabs using fetched rows.
- Risk: medium because this introduces a new API-backed workflow.
- Review needed: Product, Development, QA.

### Slice 2: Presentation reuse and render plumbing
- Reuse existing layer tabs/table rendering for API-opened layers.
- Add per-layer filter state initialization for every opened tab.
- Add helper functions for field discovery, value normalization/stringification, contains matching, AND filtering, and filtered presentation item retrieval.
- Update table, map, and timeline rendering to use filtered items while preserving current output when no filters are applied.
- Risk: medium.
- Review needed: Development and UX.

### Slice 3: Filter panel skeleton beside the table
- Add HTML container and CSS layout for active-layer filter controls beside the raw results table.
- Render active layer name, filter rows, Add, Apply, Cancel/Revert, and active filter summary.
- No filtering state mutation beyond display wiring.
- Risk: medium because it touches overlay layout.
- Review needed: UX and Development.

### Slice 4: Draft/edit/remove/apply behavior
- Wire add/edit/remove/cancel/apply actions.
- Implement empty-value validation.
- Preserve draft vs applied behavior per layer.
- Keep layer close behavior unchanged.
- Risk: medium.
- Review needed: Product, UX, QA.

### Slice 5: Cross-layer and regression validation
- Validate Entities, Locations, and event-source layers.
- Validate independent filters per layer and close/minimize/visibility regressions.
- Add checkpoint summary with test results and remaining gaps.
- Risk: low to medium.
- Review needed: QA.

## Required review gates before coding
- Create `execution-plan.md` from this developer review and the product brief.
- Product should confirm the standalone layer-selection flow and API-backed row loading scope.
- UX should confirm layer selector placement, filter panel placement, and cross-presentation filtered states.
- Product should confirm duplicate filter and remove/apply behavior if not already accepted as assumptions.
- QA should confirm manual acceptance coverage before implementation starts.

## Blocking questions before execution planning
None. The human developer approved the following assumptions on 2026-07-07:
- The capability is standalone from chat/agent result loading.
- Layer rows are fetched by API.
- MVP layer row loading has no row limit.
- MVP filtering is client-side against API-loaded layer rows.
- Filters are available for every opened layer tab.
- Duplicate filters are allowed.
- Removing filters follows the same draft/apply contract and does not update displayed results until Apply.
- Raw field names are acceptable for MVP.

## Open questions for Product / UX / QA / Architecture / Security
- QA: Which API-loaded dataset state should be used as the canonical manual test fixture?
- Architecture: Confirm the API endpoint shape if this POC pattern is expected to survive beyond local/demo use.
- Security: Confirm no additional authorization is needed for the layer catalog and row endpoints in the current target environment.

Resolved product/UX questions:
- Filter panel opens from the layer tab.
- MVP filter fields use raw field names.
