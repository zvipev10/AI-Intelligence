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
- Allow users to find/select a layer.
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

To be confirmed by developer review:
- Whether filtering should be implemented entirely client-side for the visible layer items or routed through backend/MCP query calls.
- Whether field discovery should inspect the current layer's item objects dynamically or use explicit field definitions.
- Whether contains matching should normalize Hebrew/English text the same way as existing backend search helpers.
- How to represent draft filters vs applied filters in `state.layers`.

## UX notes
- The filter controls should be presented beside the existing results table.
- Each layer should own its own filter state and Apply action.
- Editing filters and closing a layer must feel like distinct actions.
- The X close action should remain the way users close/remove a selected layer.
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
- Should filtering run client-side on already-loaded layer items for MVP, or should Apply execute a backend/MCP query?
- Should contains matching be case-insensitive and normalized for Hebrew final letters/diacritics, matching existing backend behavior where possible?
- Should duplicate filters on the same field/value be blocked or allowed?
- When a layer is closed with X, should draft/applied filters be discarded immediately with no confirmation?
- Should the existing eye visibility control remain available as-is, or should it be hidden/de-emphasized for this capability?
- Should filter fields display raw field names or translated/user-friendly labels?
- Should each layer have its own Apply button, or should Apply appear in the selected layer's filter panel only?

## Missing inputs
- Preferred UI placement for the layer filter panel beside the results table.
- Exact copy/labels for Add filter, Apply, Edit, Remove, and empty-value validation.
- Whether filter field names need translation.
- Final decision on duplicate filters.
- Final decision on client-side vs backend filtering.
- Expected performance target for filtering large event-source layers.

## Required reviewers
- Product
- Development
- UX
- QA

Potentially also:
- Architecture, if filtering requires backend/MCP API changes.

## Proposed execution checkpoints
1. Product/UX checkpoint: confirm per-layer filter interaction, Apply behavior, and panel placement.
2. Developer checkpoint: confirm client-side vs backend filtering and the state model for draft/applied filters.
3. Execution checkpoint 1: layer filter panel skeleton beside the results table, no filtering logic yet.
4. Execution checkpoint 2: per-layer add/edit/remove filter state with validation.
5. Execution checkpoint 3: Apply filters to one layer using contains + AND.
6. Execution checkpoint 4: support Entities, Locations, and event-source layers consistently.
7. QA checkpoint: validate edge cases, no-results behavior, Hebrew/English contains matching, and existing table/layer regressions.

## Handoff to developer

Questions for developer:
- Should MVP filtering be client-side against `layer.items`, or should Apply call backend/MCP search endpoints?
- What is the safest state shape for per-layer `draftFilters` and `appliedFilters` inside `state.layers`?
- Which fields should be shown to users when "all fields" are filterable: raw object keys, translated labels, or a generated field list?
- Can the existing `renderEvidence()` table rendering be extended cleanly, or should filtering introduce a small layer/filter model helper first?
- Should the existing query modal be reused or kept separate from this layer-filter workflow?
- How should contains matching normalize Hebrew/English strings?
- What is the smallest first implementation slice that can be reviewed safely?

Expected developer output:
- feasibility notes
- likely affected files/services
- implementation options
- recommended approach
- technical risks
- test strategy
- proposed execution slices
