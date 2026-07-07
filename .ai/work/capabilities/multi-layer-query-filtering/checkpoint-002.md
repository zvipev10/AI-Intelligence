# Checkpoint Summary

## Checkpoint
Checkpoint 002 - Slice 1 selector correction

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Related issue
GitHub issue: #10 / `issues/061-slice-1-selector-correction.md`.

## Checkpoint status
Pending Product/UX/Development review.

## Handoff

Next role: Product, UX, and Development.
Required action: review the corrected compact selector and decide whether Slice 2 may start.
Expected output: approval or requested changes on issue #11.
Do not proceed to: Slice 2.
Until: Product/UX approve the corrected selector and Development confirms no API/catalog regression.

## What changed since previous review
The separate visible selector section/header/count was removed. The layer selector is now a compact search/autocomplete line over the presentation surface.

## Slice goal
Apply Product/UX feedback from Slice 1 by removing the visible "Data layers / Layer selection / available layers" selector section while preserving API-backed layer search and opening.

## What changed
- Removed the standalone selector section wrapper from `index.html`.
- Removed visible selector eyebrow/header/status/count copy.
- Moved the compact layer search/autocomplete control into the presentation stack as an overlay.
- Kept `layerSelectorStatus` as a visually hidden live region for loading/error accessibility.
- Removed the successful available-layer count text from the live region.
- Removed the old "layer selection" wording from catalog-opened layer tab titles and load messages.
- Preserved catalog search, autocomplete results, and API-backed layer opening.

## Files changed
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `.ai/work/capabilities/multi-layer-query-filtering/checkpoint-002.md`
- `.ai/work/capabilities/multi-layer-query-filtering/status.md`
- `.ai/work/capabilities/multi-layer-query-filtering/issues/061-slice-1-selector-correction.md`
- `.ai/work/capabilities/multi-layer-query-filtering/issues/070-slice-1-review.md`

## Decisions made
- Keep the selector as a compact overlayed search line rather than a separate full-width section.
- Keep a hidden live region for loading/error state, but do not announce or render a successful available-layer count.
- Use the opened layer label as the tab title for catalog-opened layers.

## Tests/checks run
- Python syntax check:
  - `C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m py_compile llm_investigation_orchestrator_serbia_poc/server.py`
- Local API smoke against existing server on port `8777`:
  - `GET /api/layers` returned 12 layers, including Entities, Locations, and 10 event-source layers.
  - `GET /api/layers/entity-metadata%3Aall/rows` returned 16 entity rows.
- HTML smoke:
  - Served HTML no longer contains visible rejected labels: `שכבות נתונים`, `בחירת שכבות`, or `שכבות זמינות`.
- Browser verification with the in-app browser:
  - No `section.layer-selector` wrapper exists.
  - No `.layer-selector-header` exists.
  - Compact selector input is visible with a 360px by 32px bounding box.
  - Rejected selector text is not visible and not present in opened-layer tab titles.
  - Autocomplete search for `טלגרם` returns one `events:טלגרם` option.
  - Selecting `טלגרם` opens an existing-style layer tab and renders 1,280 rows.

## Not completed yet
- Product/UX/Development review of the corrected selector.
- Slice 2 presentation reuse and filterable layer model.
- Filter panel UI.
- Draft/applied filter behavior.
- Full QA validation.

## Blockers
- Slice 2 remains blocked until issue #11 review approves this correction.

## Risks
- Browser validation used an already-running local server on port `8777`.
- `node` is not available on the PowerShell PATH, so `node --check` could not be run.
- `styles.css` had unrelated pre-existing local changes before this task; only selector-related hunks should be staged for this checkpoint.

## Open questions
- Should the compact selector stay as an overlay on both map and timeline, or should UX request map-only placement later?
- Which API-loaded dataset state should QA treat as the canonical manual fixture?

## Review requested from
- Product
- UX
- Development

## Continue / pause recommendation
Pause for issue #11 review. If Product/UX/Development approve this correction, update `status.md` and proceed to Slice 2.

## Next planned slice
Slice 2: Presentation Reuse And Filterable Layer Model.
