# Checkpoint 011 - Slice 3 floating filter window correction

## Date
2026-07-08

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Related issue
GitHub issue: #17 / `issues/130-slice-3-mobile-filter-panel-correction.md`.

## Checkpoint status
Development correction complete; waiting for Product/UX/Development review before Slice 4.

## Handoff

Next role: Product, UX, and Development.
Required action: review the corrected floating filter window on phone, tablet, and desktop widths.
Expected output: approval to continue to Slice 4 or requested changes.
Do not proceed to: Slice 4.
Until: Product/UX/Development approve the corrected Slice 3 filter-window behavior.

## What changed
- Moved `#layerFilterPanel` out of the raw results table layout so it is a sibling of `#rawEventsOverlay` under `.view-stack`.
- Changed the filter panel from a beside-table/stacked panel to an absolute floating window above the results tabs/table.
- Kept the filter window on top of the active map or timeline surface.
- Kept the table in a single-column results overlay so it remains horizontally scrollable.
- Added view-stack raw-overlay height tracking so the floating window stays above the results overlay when the overlay is resized.
- Fixed mobile timeline layout growth by giving the mobile result panel a fixed working height.
- Added an inline empty favicon to avoid the browser console 404 from the implicit favicon request.
- Bumped cache versions:
  - `styles.css?v=65`
  - `app.js?v=83`

## Files changed
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `.ai/work/capabilities/multi-layer-query-filtering/checkpoint-011.md`
- `.ai/work/capabilities/multi-layer-query-filtering/status.md`
- `.ai/work/capabilities/multi-layer-query-filtering/issues/130-slice-3-mobile-filter-panel-correction.md`

## Tests/checks run
- JavaScript syntax check:
  - `C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe --check llm_investigation_orchestrator_serbia_poc/app.js`
- Git whitespace check:
  - `git diff --check`
- Local HTTP check:
  - `GET http://127.0.0.1:8768/` returned HTTP 200.
- Local browser validation with Microsoft Edge through Playwright:
  - `360x800` map view: opened `טלגרם`, filter window visible immediately, parent is `.view-stack`, position is `absolute`, above results tabs/overlay, does not overlap selector, close action visible, table overflow-x remains `auto`, 1,280 rows remain rendered, no console errors or warnings.
  - `390x844` map view: same checks passed.
  - `390x844` timeline view: same checks passed.
  - `768x1024` map view: same checks passed.
- VM deployment:
  - Copied `app.js`, `index.html`, and `styles.css` to `/opt/serbia-poc-ui`.
  - Restarted `serbia-poc-ui.service`.
  - `systemctl is-active serbia-poc-ui.service` returned `active`.
  - `GET http://151.145.93.180/` returned HTTP 200.
  - Deployed `index.html` references `styles.css?v=65` and `app.js?v=83`.

## Validation notes
- Slice 3 still intentionally provides only the filter-panel skeleton. Add/edit/remove/apply behavior remains deferred to Slice 4.
- The floating window remains a single active-layer panel; opening another layer's filter button closes the previous panel through the existing state behavior.

## Risks
- Product/UX should still confirm whether the floating window location is preferred on desktop, because it now overlays map/timeline content rather than occupying table-side space.
- QA still needs to confirm the canonical manual test fixture before Slice 4 acceptance.

## Continue / pause recommendation
Pause for Product/UX/Development review. If approved, proceed to Slice 4: Draft/Edit/Remove/Apply Behavior.
