# Capability Brief

## Capability name
Multi-Layer Query Filtering

## Capability slug
multi-layer-query-filtering

## User problem
Users need a faster way to query and inspect application data by selecting relevant layers and narrowing each layer with field/value filters. Today the application can display result layers and a results table, but users do not yet have a guided workflow for finding a layer, adding filters to that layer, applying those filters, and later reopening the filter for editing.

## Business goal
Improve investigation and data-discovery workflows by letting users progressively narrow visible results per layer while keeping the existing results-table experience.

## Target users
- Analysts using the investigation workspace.
- Users who inspect event, entity, and location results in the existing table/map/timeline workflow.

## Proposed behavior
The user can find and select query layers.

Supported layer families for MVP:
- Entities
- Locations
- Event-source layers, where each available `source_type` is represented as a selectable event layer.

When the user selects a layer:
- the layer is added to the query workspace
- the layer is displayed as selected
- the layer's results are shown in the existing results table area
- the layer remains available when the user selects another layer
- each selected layer is handled separately from other selected layers
- each selected layer can be closed using the existing X close action

Filtering behavior:
- filters belong to a specific layer
- all fields on the selected layer are available for filtering
- a filter consists of a selected field and a free-text value entered by the user
- free-text matching uses contains logic
- empty filter values are blocked
- multiple filters on the same layer are combined using AND logic
- filter changes do not affect the displayed layer results until the user applies them
- applying filters updates only that layer's displayed results
- the user can reopen an existing filter and edit it later
- editing filters and closing the layer are separate actions

## MVP scope
- Support the existing entity layer.
- Support the existing location layer.
- Support event-source layers derived from available `source_type` values.
- Add a new standalone layer selection component for choosing layers.
- The layer selection component must include Entities, Locations, and Events grouped by type/source type.
- Allow users to find/select a layer from the new layer selection component.
- Add each selected layer to the existing layer/table workspace.
- Keep selected layers independent from each other.
- Keep previously selected layers and their filters when another layer is selected.
- Allow each selected layer to be closed with an X action.
- Allow all fields on each layer to be filterable.
- Allow users to add multiple filters per layer.
- Use free-text values for MVP filters.
- Use contains matching for free-text values.
- Combine filters within the same layer using AND logic.
- Block empty filter values before Apply.
- Apply filter changes per layer.
- Display layer filters beside the existing results table.
- Allow filters to be reopened and edited later.

## Non-goals
- OR logic between filters.
- Nested filter groups.
- Cross-layer relationship filtering.
- Hidden or restricted filter fields.
- Dropdown/autocomplete filter values.
- Type-specific operators for dates, numbers, booleans, or enums.
- Saved query templates.
- Sharing query configurations between users.
- Admin configuration of filterable fields.
- Replacing or redesigning the existing results table beyond the needed layer/filter integration.

## Acceptance criteria
- [ ] The user can select the Entities layer.
- [ ] The user can select the Locations layer.
- [ ] The user can select event-source layers derived from available `source_type` values.
- [ ] Selecting a layer displays it as selected in the query workspace.
- [ ] Selecting a new layer does not remove or modify previously selected layers.
- [ ] Each selected layer is handled separately.
- [ ] Each selected layer can be closed using an X action.
- [ ] Closing a layer does not act as filter editing.
- [ ] The user can add filters to a specific selected layer.
- [ ] All fields on the selected layer are available for filtering.
- [ ] A filter consists of a field and a free-text value.
- [ ] Empty filter values are blocked before Apply.
- [ ] Free-text filters use contains matching.
- [ ] Multiple filters on the same layer are combined using AND logic.
- [ ] The user can apply filters for one layer without modifying filters on another layer.
- [ ] Applying filters updates that layer's displayed results.
- [ ] The user can reopen and edit an existing filter.
- [ ] Edited filters do not affect the displayed layer results until Apply.
- [ ] The user can remove an existing filter from a layer.
- [ ] Active filters are displayed beside the existing results table.

## Edge cases
- No layers are available.
- No event-source layers are available.
- Layer search returns no results.
- A selected layer has no rows/items.
- A selected layer has no discoverable fields.
- User tries to apply a filter with an empty value.
- User creates duplicate filters for the same field/value.
- User edits a filter and cancels before applying.
- User closes a layer that has draft or applied filters.
- Applying filters returns no matching rows.
- Applying filters fails.
- A field exists on some rows but not others.
- Contains matching is used on non-string values.
- Hebrew/English text matching and casing/normalization affect contains behavior.

## Technical constraints
Observed code context:
- The current UI layer state lives in `llm_investigation_orchestrator_serbia_poc/app.js` under `state.layers` and `state.activeLayerId`.
- Event layers are already built in `buildEventLayers(events)` by grouping events on `event.source_type`.
- Location and entity layers are already represented by `buildLocationMetadataLayer(items)` and `buildEntityMetadataLayer(items)`.
- The existing raw results overlay is rendered by `renderEvidence()`.
- The existing layer tab close action uses `[data-layer-close]` and removes the layer from `state.layers`.
- The current UI also has layer visibility behavior through `[data-layer-visibility]`; this capability does not require adding another toggle.
- The MCP/backend data currently exposes event `source_type`, entity metadata, and location metadata.
- Current event data fields include at least: `event_id`, `timestamp_utc`, `source_type`, `source_reliability`, `source_reliability_label`, `certainty_level`, `entity_id`, `location_id`, and `event_summary`.
- The source normalization report lists approved source types such as `X`, `בלוג פוליטי`, `הודעת דובר`, `חדשות מקומיות`, `טיקטוק`, `טלגרם`, `ערוץ חדשות בינלאומי`, `פייסבוק`, `קבוצת וואטסאפ`, and `שמועה מקומית`.

Confirmed by developer/product/UX review:
- The capability is standalone from chat and agent result loading.
- Layer rows are fetched through an API-backed path.
- MVP row loading has no row limit.
- MVP filtering runs client-side against API-loaded layer rows.
- Applied filters affect all supported presentations for the opened layer tab: table, map, and timeline.
- Field discovery should inspect the selected layer's loaded item objects dynamically.
- MVP contains matching should use simple string contains matching with case folding, aligned with current frontend helper constraints.
- Draft and applied filters should live on opened layer objects, using separate `draftFilters` and `appliedFilters` state.
- Duplicate filters are allowed for MVP.
- Removing a filter is a draft change until Apply.
- Closing a layer discards that layer's draft/applied filter state with no confirmation.

## UX notes
- Add a new standalone layer selection component. It is the place users choose/add layers.
- The layer selection component is separate from opened layer tabs, chat, agent result steps, and the query modal.
- The existing opened layer tabs remain the place users select, filter, hide/show, or close already opened layers.
- The filter controls should be presented beside the existing results table.
- The filter panel should be opened from the layer tab.
- Each layer should own its own filter state and Apply action.
- Editing filters and closing a layer must feel like distinct actions.
- The X close action should remain the way users close/remove a selected layer.
- MVP should display raw field names rather than translated or user-friendly field labels.
- The UI should clearly indicate which layer is selected/active for table display.
- The UI should make it clear when a layer has unapplied filter changes.
- Empty filter values should be blocked before Apply with an obvious inline state.
- Existing table visibility, minimization, and close behavior should not become confusing when filters are added.

## QA notes
- Test selecting Entities, Locations, and event-source layers.
- Test adding multiple filters to one layer.
- Test that filters on one layer do not affect another layer.
- Test AND behavior within a layer.
- Test contains matching with Hebrew and English values.
- Test empty filter blocking.
- Test editing an existing filter before and after Apply.
- Test removing an existing filter.
- Test closing a layer with filters.
- Test no-results behavior after Apply.
- Test existing results table, layer close, and layer selection regressions.

## Risks
- Dynamic "all fields are filterable" may expose fields that are technically present but not useful for users.
- Contains matching semantics may differ between client-side filtering and backend search unless explicitly aligned.
- Filtering large layer result sets client-side may have performance limits.
- Adding filter controls beside the current table may crowd the existing workspace.
- Current code has both layer visibility and close behaviors; product does not require additional toggling, so implementation needs to avoid adding another confusing control.
- Per-layer draft/applied state may complicate the current simple `state.layers` model.

## Open questions
No blocking product, UX, or developer questions remain before execution planning.

Implementation-detail questions to handle during planning/checkpoints:
- Whether the existing eye visibility control needs visual de-emphasis after the filter panel is added.
- Exact button and validation copy for Add filter, Apply, Edit, Remove, Cancel/Revert, and empty-value validation.
- Whether the first implementation should add a lightweight automated helper test harness or rely on manual browser validation.

## Missing inputs
None blocking execution planning.

Planning assumptions:
- MVP uses raw field names.
- MVP allows duplicate filters.
- MVP uses API row loading with no row limit.
- MVP uses client-side filtering over API-loaded rows.
- MVP keeps removal draft-only until Apply.
- MVP opens the filter panel from the layer tab.
- Product accepts the performance risk of unlimited row loading for MVP.

## Required reviewers
- Product
- Development
- UX
- QA

Potentially also:
- Architecture, if filtering requires backend/MCP API changes.

## Proposed execution checkpoints
1. Execution checkpoint 1: standalone API-backed layer catalog and row loading.
2. Execution checkpoint 2: presentation reuse for API-opened layers across table, map, and timeline.
3. Execution checkpoint 3: layer-tab-triggered filter panel skeleton beside the results table.
4. Execution checkpoint 4: per-layer add/edit/remove/apply filter state with validation.
5. Execution checkpoint 5: cross-layer validation for Entities, Locations, and event-source layers.
6. QA checkpoint: validate edge cases, no-results behavior, Hebrew/English contains matching, and existing table/layer regressions.

## Handoff to developer

Approved developer direction:
- Build standalone API-backed layer opening, separate from chat/agent results.
- Reuse existing presentation components after rows are loaded.
- Keep the existing query modal separate.
- Add helper functions before wiring heavy UI behavior.
- Use `draftFilters` and `appliedFilters` on opened layer objects.
- Use raw field names for MVP.
- Apply filters across all supported presentations for the opened layer.

Expected developer output:
- feasibility notes
- likely affected files/services
- implementation options
- recommended approach
- technical risks
- test strategy
- proposed execution slices
