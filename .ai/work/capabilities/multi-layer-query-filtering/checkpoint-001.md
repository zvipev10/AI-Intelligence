# Checkpoint Summary

## Checkpoint
Checkpoint 001 - Slice 1

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Related issue
GitHub issue: #9 / `issues/060-slice-1-implementation.md`. Follow-up correction issue: #10 / `issues/061-slice-1-selector-correction.md`.

## Checkpoint status
Changes requested.

## Handoff

Next role: Development.
Required action: remove the selector section/header/count and keep only the compact autocomplete line.
Expected output: `checkpoint-002.md`.
Do not proceed to: Slice 2.
Until: Product/UX/Development review the corrected selector.

## What changed since previous review
Product rejected the separate visible selector block after Slice 1.

## Slice goal
Create the standalone compact layer search/autocomplete component and API-backed data path for selectable layers.

## What changed
- Added API-backed layer catalog support in the Serbia POC UI server.
- Added row-loading support for selected layers.
- Added a standalone compact layer search/autocomplete component above the map/timeline workspace.
- Added frontend catalog loading and layer-opening behavior independent from chat/agent results.
- Opened selected API-loaded layers through the existing layer tab/table/map model.
- Kept event layers grouped strictly by `source_type`.
- Updated the selector UX after Product clarification so available layers are not shown as a full always-visible list above the map.

## Files changed
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `.ai/work/capabilities/multi-layer-query-filtering/checkpoint-001.md`

## Decisions made
- API layer IDs for the MVP:
  - `entity-metadata:all`
  - `location-metadata:all`
  - `events:<source_type>`
- `GET /api/layers` returns selectable layer definitions.
- `GET /api/layers/:layerId/rows` returns all rows for the selected layer with no MVP limit.
- Catalog-opened layers use `catalog:<layer-id>` source IDs so each selected catalog layer stays independent.
- The selector is compact and always available above the presentation area.
- The selector shows matching autocomplete results only while focused/searching, and selecting a result opens it as an existing-style layer tab.

## Tests/checks run
- Python syntax check:
  - `C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m py_compile llm_investigation_orchestrator_serbia_poc/server.py`
- Local server API smoke:
  - Started `llm_investigation_orchestrator_serbia_poc/server.py` on port `8777`.
  - `GET /api/layers` returned Entities, Locations, and event-source layers.
  - `GET /api/layers/events:<encoded source_type>/rows` returned rows for Hebrew `source_type` value `חדשות מקומיות`.
  - `GET /api/layers/events:<encoded source_type>/rows` returned `1280` rows for Hebrew `source_type` value `טלגרם`.
  - `GET /api/layers/entity-metadata:all/rows` returned `16` entity rows.
  - `GET /api/layers/location-metadata:all/rows` returned `155` location rows.
- JavaScript parser check:
  - Parsed `llm_investigation_orchestrator_serbia_poc/app.js` successfully with Acorn through the Node REPL tool.
- Browser automation was attempted through Playwright, but no bundled Chromium is installed, Chrome is not installed at the expected path, and Edge launch is blocked by local permissions.

## Not completed yet
- Filter panel UI.
- Draft/applied filter state.
- Cross-presentation filtering helper.
- Filter Apply behavior.
- Full browser interaction QA.

## Blockers
- Product reviewed the selector layout and rejected the separate "Data layers / Layer selection / available layers" section shown in the Slice 1 UI. Development must remove that visible section/header/count and keep only a compact search/autocomplete line.

## Risks
- MVP no-limit row loading can still become a performance issue on larger datasets.
- Existing unrelated local changes in `styles.css` predated this slice; this slice preserved and worked with them rather than reverting.

## Open questions
- Which API-loaded dataset state should be used as the canonical manual QA fixture?

## Review requested from
- Product
- UX
- Development

## Continue / pause recommendation
Pause for Developer review before implementing Slice 2. Product requested a Slice 1 UX correction: remove the separate selector section/header/count and keep only the compact search/autocomplete affordance.

## Next planned slice
Slice 2: Presentation Reuse And Filterable Layer Model.
