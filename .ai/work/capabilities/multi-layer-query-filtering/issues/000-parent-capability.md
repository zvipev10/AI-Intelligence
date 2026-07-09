# [Capability] Multi-Layer Query Filtering

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

GitHub issue: #3

## Current phase
Final handoff and merge.

## Overall status
Slice 5 cross-layer validation passed and Product approved `checkpoint-013.md`; final handoff is complete and the branch is ready to merge to `main`.

## Operational status
See `.ai/work/capabilities/multi-layer-query-filtering/status.md`.

## User problem
Users need a faster way to query and inspect application data by selecting relevant layers and narrowing each layer with field/value filters.

## MVP scope
- Standalone compact layer search/autocomplete.
- Entities, Locations, and event-source layers by `source_type`.
- API-backed row loading for selected layers.
- Independent opened layer tabs.
- Per-layer draft and applied filters.
- Client-side contains matching with AND logic.
- Filtered presentations for table, map, and timeline where supported.

## Acceptance criteria
See `.ai/work/capabilities/multi-layer-query-filtering/capability-brief.md`.

## Child tasks
- [ ] Product brief review: #4 / `010-product-brief-review.md`
- [x] Developer review: #5 / `020-developer-review.md`
- [x] UX review: #6 / `030-ux-review.md`
- [x] QA planning: #7 / `040-qa-planning.md`
- [x] Execution plan review: #8 / `050-execution-plan-review.md`
- [x] Slice 1 implementation: #9 / `060-slice-1-implementation.md`
- [x] Slice 1 selector correction: #10 / `061-slice-1-selector-correction.md`
- [x] Slice 1 review: #11 / `070-slice-1-review.md`
- [x] Slice 2 implementation: #12 / `080-slice-2-presentation-filter-model.md`
- [x] Slice 3 implementation: #13 / `090-slice-3-filter-panel.md`
- [x] Slice 3 mobile filter-panel correction: #17 / `130-slice-3-mobile-filter-panel-correction.md`
- [x] Slice 4 implementation: #14 / `100-slice-4-filter-behavior.md`
- [x] Slice 5 validation: #15 / `110-slice-5-validation.md`
- [x] Final handoff: #16 / `120-final-handoff.md`

## Artifacts
- Capability brief: `.ai/work/capabilities/multi-layer-query-filtering/capability-brief.md`
- Status: `.ai/work/capabilities/multi-layer-query-filtering/status.md`
- Decisions: `.ai/work/capabilities/multi-layer-query-filtering/decisions.md`
- Developer review: `.ai/work/capabilities/multi-layer-query-filtering/developer-review.md`
- UX review: `.ai/work/capabilities/multi-layer-query-filtering/ux-review.md`
- QA review: `.ai/work/capabilities/multi-layer-query-filtering/qa-review.md`
- Execution plan: `.ai/work/capabilities/multi-layer-query-filtering/execution-plan.md`
- Latest checkpoint: `.ai/work/capabilities/multi-layer-query-filtering/checkpoint-013.md`
- Handoff: `.ai/work/capabilities/multi-layer-query-filtering/handoff-summary.md`

## Closure rule
Keep this parent issue open until all required child tasks are closed, acceptance criteria are satisfied, final QA is complete, and final handoff is published.

## Closure checklist
- [x] Child tasks complete locally.
- [x] Acceptance criteria satisfied.
- [x] Final QA validation passed.
- [x] Final handoff published in `handoff-summary.md`.
- [ ] Merge to `main` confirmed.
