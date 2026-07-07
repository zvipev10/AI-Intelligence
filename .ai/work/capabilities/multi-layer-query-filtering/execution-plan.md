# Execution Plan

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Related issues
- Parent issue: #3 / `issues/000-parent-capability.md`
- Execution plan review issue: #8 / `issues/050-execution-plan-review.md`
- Active blocker issue: #10 / `issues/061-slice-1-selector-correction.md`

## Plan status
Reopened.

## Role actions

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Action needed | Correct the Slice 1 selector UI and publish `checkpoint-002.md`. | Slice 2 starts |
| Product | Waiting | Review corrected selector after Development publishes `checkpoint-002.md`. | Slice 2 starts |
| UX | Waiting | Review corrected selector placement after Development publishes `checkpoint-002.md`. | Slice 2 starts |
| QA | Waiting | Confirm QA fixture and validation plan before Slice 4 acceptance. | Slice 4 completion |

## What changed since previous review
The plan is reopened because Product rejected the visible selector section/header/count from Slice 1. The next action is a Slice 1 correction, not Slice 2 implementation.

Prepared on 2026-07-07 from the approved capability brief and developer review. Do not start implementation until Product and Development accept this plan or explicitly accept any changes as execution assumptions.
Updated on 2026-07-07 after Product reviewed Slice 1 and requested removal of the separate visible "Data layers / Layer selection / available layers" selector section.

## Prerequisite review gate
- Product brief: `.ai/work/capabilities/multi-layer-query-filtering/capability-brief.md` updated with Product/UX decisions.
- Developer review: `.ai/work/capabilities/multi-layer-query-filtering/developer-review.md` reopened for Slice 1 correction.
- UX review: `.ai/work/capabilities/multi-layer-query-filtering/ux-review.md` backfilled and marked Changes requested for Slice 1.
- QA review: `.ai/work/capabilities/multi-layer-query-filtering/qa-review.md` backfilled and pending human QA review.
- Architecture/Security review: not blocking for local MVP, but API shape and authorization assumptions should be reviewed if this pattern is expected to survive beyond the POC.
- Blocking questions resolved or accepted as assumptions: yes. Developer approved standalone API-backed layer loading, no row limit for MVP, client-side MVP filtering, raw field names, duplicate filters allowed, draft-only remove until Apply, and filter panel opened from the layer tab.

## Goal
Deliver a standalone layer-selection and per-layer filtering workflow that is separate from chat/agent results, reuses the existing layer presentation components, and applies filters across all supported presentations for each opened layer.

## Context used
- `.ai/work/capabilities/multi-layer-query-filtering/capability-brief.md`
- `.ai/work/capabilities/multi-layer-query-filtering/developer-review.md`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/server.py`

## Approved scope
- Standalone layer catalog and layer-opening flow, independent of chat and agent results.
- New standalone compact search/autocomplete layer selection component for choosing/adding layers.
- MVP layer families:
  - Entities
  - Locations
  - Event-source layers derived from available `source_type` values
- API-backed row loading for selected layers.
- No row limit for MVP layer row loading.
- Reuse existing opened-layer tabs and presentation components.
- Per-opened-layer draft and applied filters.
- Raw field names for MVP filter fields.
- Free-text contains matching.
- Empty filter values blocked before Apply.
- Multiple filters on the same layer combined with AND logic.
- Duplicate filters allowed for MVP.
- Removing filters changes draft state only until Apply.
- Applied filters affect table, map, and timeline where the opened layer supports those presentations.
- Closing a layer with X discards that layer's filters without confirmation.

## Non-goals
- Backend/server-side filtering on Apply.
- Pagination or row limits for MVP.
- OR logic, nested filter groups, typed operators, autocomplete values, saved query templates, or shared query configurations.
- Friendly/translated filter field labels.
- Replacing the existing table, map, timeline, or chat workflows.
- Reusing the query modal for layer filters.

## Proposed approach
Build the capability in five reviewable slices.

First, expose a standalone layer catalog and layer row API in `server.py`, and add the new standalone compact search/autocomplete layer selection component. The frontend should fetch available layer definitions, let users search/autocomplete Entities, Locations, and Events grouped by `source_type`, then fetch all rows for a selected layer. The selected layer should open in the results panel through the existing opened-layer tab model rather than depending on agent/chat result data.

Second, introduce a shared presentation item helper so table, map, and timeline consume the same applied-filtered item set for each visible/opened layer. This avoids a common failure mode where the table looks filtered but the map and timeline still show unfiltered records.

Third, add the filter panel entry point from the layer tab and place filter controls beside the results table. Keep layer selection, opened layer tabs, close, visibility, and filter editing visually distinct.

Fourth, wire draft/edit/remove/apply behavior. Apply validates draft filters, copies valid draft filters to applied filters, and then rerenders the supported presentations.

Fifth, run cross-layer validation and capture checkpoint results before asking QA for acceptance.

## Files/services likely affected
- `llm_investigation_orchestrator_serbia_poc/server.py`
  - Add API endpoint(s) for layer catalog and layer row loading.
- `llm_investigation_orchestrator_serbia_poc/app.js`
  - Add standalone layer catalog loading and open-layer behavior.
  - Add per-layer filter state and helpers.
  - Refactor map/timeline/table item selection to use applied-filtered presentation items.
  - Add click/change/input handlers for layer filter controls.
- `llm_investigation_orchestrator_serbia_poc/index.html`
  - Add a new standalone layer selection component and filter panel container.
- `llm_investigation_orchestrator_serbia_poc/styles.css`
  - Add layer selection component and filter panel styles.
  - Preserve existing raw results overlay, layer tab, close, visibility, minimize, and resize behavior.

## Data/API changes
Recommended MVP API:
- `GET /api/layers`
  - Returns selectable layer definitions.
  - Each layer should include `id`, `label`, `kind`, `capabilities`, and any metadata needed by the UI.
- `GET /api/layers/:layerId/rows`
  - Returns all rows for the selected layer, with no MVP row limit.
  - Event-source layer IDs should map to existing `source_type` values.
  - Entity and Location layers should return metadata rows compatible with existing presentation/table rendering.

Server-side filtering, pagination, limits, and typed filter operators are deferred.

## UX changes
- Add a new standalone compact search/autocomplete layer selection component, separate from chat, agent result controls, existing opened-layer tabs, and the query modal.
- Do not display all available layers as a large list above the map.
- Do not display a separate selector section/header/count such as "Data layers", "Layer selection", or "12 available layers".
- Candidate placement: on the map surface, if compact and non-obstructive.
- The layer selection component should let users search/select Entities, Locations, and Events grouped by `source_type`.
- Selecting an autocomplete result should open that layer in the results panel as an existing-style opened layer tab.
- The existing opened-layer tabs should remain responsible for selecting an active opened layer, opening that layer's filter panel, visibility, and X close.
- Open selected layers as existing-style layer tabs.
- Open the filter panel from the layer tab.
- Show raw field names in field selectors.
- Place filter controls beside the existing results table.
- Clearly show unapplied filter changes.
- Keep X close as layer removal only.
- Keep the visibility eye separate from filtering.
- Empty filter values should show an inline validation state before Apply.

## Test plan
Manual validation:
- Load the app and confirm `/api/layers` returns Entities, Locations, and event-source layer definitions.
- Select Entities, Locations, and at least two event-source layers.
- Confirm opened layers appear as tabs and selecting a new layer does not remove existing layers.
- Confirm each opened layer can be closed with X.
- Confirm each opened layer preserves independent draft/applied filters.
- Add one filter and Apply; confirm table, map, and timeline update only for that layer where supported.
- Add multiple filters to one layer; confirm AND behavior.
- Edit draft filters and confirm presentations do not change until Apply.
- Remove a filter and confirm presentations do not change until Apply.
- Try Apply with an empty value and confirm inline validation.
- Test duplicate filters and confirm they do not break filtering.
- Test no-results state after Apply.
- Test Hebrew and English contains matching.
- Confirm existing chat/agent result loading still works.
- Confirm existing raw overlay minimize, resize, close, layer visibility, and layer tab selection still work.

Automation/lightweight checks:
- Add small helper-level tests only if a local JS test harness is already practical or can be added without distracting from MVP delivery.
- At minimum, run local app smoke validation before each implementation checkpoint.

## Execution slices

### Slice 1: Compact Layer Search/Autocomplete And API Row Loading
Goal:
Create the standalone compact layer search/autocomplete component and data path for selectable layers.

Expected changes:
- Add `GET /api/layers`.
- Add `GET /api/layers/:layerId/rows` or an equivalent route shape if the existing server routing makes query parameters safer.
- Return Entities, Locations, and event-source layer definitions.
- Return all rows for a selected layer with no MVP row limit.
- Add frontend fetch helpers for catalog and layer rows.
- Add a new standalone compact search/autocomplete layer selection component.
- The component searches/selects Entities, Locations, and Events grouped by `source_type`.
- Do not place a full list of all available layers above the map.
- Remove the separate visible selector section/header/count from the Slice 1 UI and keep the affordance as a small search/autocomplete line only.
- Prefer a small search line; it may sit on the map surface if it stays compact and does not obscure map use.
- Selecting an autocomplete result opens that layer in the results panel through the existing opened-layer tab model.
- The component remains available so users can add more layers later.

Risk:
Medium. This introduces a new API-backed workflow and becomes the foundation for the rest of the capability.

Reviewer:
Product, UX, and Development.

Stop after slice?
Yes. Development should first review and apply the Product correction to remove the selector section/header/count. Product/UX/Development should then verify that the new layer selection component is separate from opened-layer tabs, independent from chat/agent results, and that API shape is acceptable before filter UI work continues.

### Slice 2: Presentation Reuse And Filterable Layer Model
Goal:
Make API-opened layers render through the existing presentation model and prepare shared filtering helpers.

Expected changes:
- Open selected API-loaded layers into the existing layer tabs.
- Initialize `draftFilters`, `appliedFilters`, `filterError`, and filter-panel state on opened layers.
- Add helpers for field discovery, value stringification, text normalization, AND matching, and `itemsForLayerPresentation(layer)`.
- Refactor table, map, and timeline item selection so supported presentations use applied-filtered items.
- Preserve existing chat/agent result layers where practical.

Risk:
Medium. This touches shared presentation paths and can cause regressions if map/timeline/table diverge.

Reviewer:
Development and UX.

Stop after slice?
Yes. Development should verify the shared item helper before UI interaction code is added.

### Slice 3: Layer-Tab Filter Panel Skeleton
Goal:
Add the user-facing filter panel entry point and layout without full mutation behavior.

Expected changes:
- Add a layer-tab filter button/control distinct from X close and visibility.
- Add a filter panel beside the existing results table.
- Render active layer name, available fields, draft filter rows, active filter summary, and disabled/placeholder Apply controls.
- Style the panel so it does not confuse close, visibility, minimize, or resize controls.
- Use raw field names.

Risk:
Medium. The raw overlay is compact and existing tab behavior is already dense.

Reviewer:
Product, UX, and Development.

Stop after slice?
Yes. Product/UX should review placement and interaction clarity before behavior wiring.

### Slice 4: Draft/Edit/Remove/Apply Behavior
Goal:
Complete MVP filter interactions.

Expected changes:
- Wire Add filter, field selection, value editing, remove, cancel/revert, and Apply.
- Validate empty values before Apply.
- Preserve draft vs applied behavior.
- Keep duplicate filters allowed.
- Ensure Apply updates all supported presentations for the opened layer.
- Show filtered count versus original count when filters are applied.

Risk:
Medium. This is the core behavior and has several state edges.

Reviewer:
Product, UX, Development, and QA.

Stop after slice?
Yes. This changes product behavior and should get explicit review before final polish.

### Slice 5: Cross-Layer Validation And Regression Polish
Goal:
Validate the capability across layer families and protect existing workflows.

Expected changes:
- Validate Entities, Locations, and event-source layers.
- Verify independent filters across multiple opened layers.
- Verify close, visibility, minimize, resize, and tab selection regressions.
- Polish empty/no-results/error states discovered during validation.
- Create checkpoint summary with test results and remaining gaps.

Risk:
Low to medium.

Reviewer:
QA, Product, and Development.

Stop after slice?
Yes. Final QA acceptance should happen before merging/releasing.

## Stop conditions
Stop and request review if:
- API layer loading requires a meaningfully different route shape than planned.
- Selected layers cannot be loaded independently of chat/agent state.
- Map/timeline filtering cannot share the same applied-filtered item set as table filtering without a larger refactor.
- Unlimited row loading causes visible browser instability on the MVP dataset.
- Filter panel layout makes close, visibility, minimize, or resize actions ambiguous.
- Existing chat/agent result rendering regresses.

## Rollback/fallback notes
- Keep chat/agent result rendering paths intact while adding standalone layer selection.
- If the layer search/autocomplete component causes instability or obstructs the map/results experience, hide or disable it while preserving existing result tabs.
- If cross-presentation filtering is unstable, stop before release rather than shipping table-only filtering, because Product decided filters must affect all supported presentations.
- If unlimited row loading is too slow on the MVP dataset, return to Product/Development for a limit/paging decision before changing the approved scope.

## Required approval before implementation
Product and Development should review and approve this execution plan before coding begins.

QA should review the test plan before Slice 4 is considered complete.

Architecture/Security should review the endpoint shape and authorization assumptions if this API is intended to move beyond local/demo POC use.
