# Capability Status

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Current phase
Slice 3 mobile correction requested.

## Overall status
Slice 2 is fully approved by Product, Development, and UX. Slice 3 filter-panel skeleton is implemented and deployed, but Product requested a Development fix for the phone-width mobile filter-panel visibility issue before Slice 4 behavior wiring.

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Complete | Approved the Slice 2 VM build for unchanged visible behavior and readiness for Slice 3 filter-panel work. | Done |
| Development | Complete | Approved `checkpoint-006.md` and confirmed the shared presentation/filter helper approach for Slice 3. | Done |
| UX | Complete | Approved `checkpoint-006.md` and allowed Slice 3 to begin. | Done |
| Development | Action needed | Fix GitHub issue #17 / `issues/130-slice-3-mobile-filter-panel-correction.md` so the filter panel is visible immediately on phone widths. | Slice 4 starts |
| Product/UX/Development | Waiting | Review the corrected Slice 3 mobile behavior after Development publishes the fix. | Before Slice 4 starts |
| QA | Waiting | Confirm canonical manual test fixture and review QA checklist before core filter behavior is wired. | Slice 4 completion |
| Architecture/Security | Not blocking | Review API endpoint shape and authorization assumptions if this pattern will continue beyond the local POC. | Before productionizing |

## Latest change since previous review
Product opened Development request #17:
- Fix phone-width Slice 3 mobile filter-panel visibility before Slice 4 behavior wiring.
- Local request artifact: `issues/130-slice-3-mobile-filter-panel-correction.md`.

Mobile audit `mobile-audit-2026-07-08/report.md`:
- Tablet portrait review is acceptable for Slice 3.
- Phone-width review needs a fix: the filter panel opens below the visible overlay area, so users may not see the result of tapping the filter button.

Deployment checkpoint `checkpoint-010.md`:
- Deployed Slice 3 `app.js`, `index.html`, and `styles.css` to the review VM on 2026-07-08.
- Restarted `serbia-poc-ui.service`; service reported `active`.
- Verified the served page returns HTTP 200 and references `app.js?v=82` and `styles.css?v=64`.

UX approved Slice 2 on 2026-07-08.
Development implemented Slice 3 in `checkpoint-009.md`:
- Added a distinct filter action on each layer tab.
- Added a beside-table filter-panel skeleton with active layer name, raw fields, draft filter summary, active filter summary, and disabled placeholder actions.
- Kept Add/Apply mutation behavior deferred to Slice 4.

Development approved the Slice 2 shared presentation/filter helper approach on 2026-07-08.
Product approved the Slice 2 VM build on 2026-07-08.
UX approved Slice 1 on 2026-07-08.
Product approved Slice 1 on 2026-07-08.

Development implemented Slice 2 in `checkpoint-006.md`:
- Opened layers now initialize draft/applied filter model state.
- Field discovery, value stringification, text normalization, contains matching, AND filtering, and shared presentation item helpers were added.
- Table, map, timeline, and result counts now consume `itemsForLayerPresentation(layer)`.

Deployment checkpoint `checkpoint-007.md`:
- Deployed `app.js`, `index.html`, and `styles.css` to the review VM on 2026-07-08.
- Restarted `serbia-poc-ui.service`; service reported `active`.
- Verified the served page returns HTTP 200 and references `app.js?v=81` and `styles.css?v=63`.

Development approval checkpoint `checkpoint-008.md`:
- Development approved the Slice 2 implementation and shared presentation/filter helper approach on 2026-07-08.

## Current blockers
- Slice 4 should not start until Development fixes issue #17 or Product explicitly waives phone-width mobile approval.
- Product/UX/Development should review the corrected Slice 3 mobile behavior before Slice 4 behavior wiring.

## Current risks
- MVP row loading has no limit, which may create browser performance risk on larger datasets.
- UX and QA were previously captured indirectly; separate UX and QA artifacts have now been backfilled but still require human approval.
- QA still needs to confirm the canonical manual test fixture before Slice 4 acceptance.

## Next expected artifact
Development checkpoint for issue #17 mobile filter-panel correction.

## Parent issue
GitHub issue: #3. Local issue body: `issues/000-parent-capability.md`.

## Child issues

| Local issue body | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| #4 / `issues/010-product-brief-review.md` | Product | Approve initial capability brief. | Backfilled as complete from existing brief decisions | No |
| #5 / `issues/020-developer-review.md` | Development | Review technical approach and implementation slices. | Complete after Slice 1 correction | No |
| #6 / `issues/030-ux-review.md` | UX | Review selector and filter-panel UX decisions. | Complete; UX approved corrected selector | No |
| #7 / `issues/040-qa-planning.md` | QA | Confirm test fixture and manual coverage. | Pending human QA input | Before Slice 4 acceptance |
| #8 / `issues/050-execution-plan-review.md` | Product/Development | Approve execution plan gates and slices. | Complete; plan reconciled after Slice 1 correction | No |
| #9 / `issues/060-slice-1-implementation.md` | Development | Implement API layer catalog and selector. | Complete with correction checkpoint | No |
| #10 / `issues/061-slice-1-selector-correction.md` | Development | Remove selector wrapper/header/count. | Implemented in `checkpoint-002.md`; follow-up UX comments implemented in `checkpoint-003.md` | No |
| #11 / `issues/070-slice-1-review.md` | Product/UX/Development | Review corrected Slice 1. | Complete; Product and UX approved `checkpoint-005.md` | No |
| #12 / `issues/080-slice-2-presentation-filter-model.md` | Development | Add presentation reuse and filterable model helpers. | Complete; Product, Development, and UX approved | No |
| #13 / `issues/090-slice-3-filter-panel.md` | UX/Development | Add filter panel skeleton. | Implemented in `checkpoint-009.md`; pending Product/UX/Development review | Yes |
| #17 / `issues/130-slice-3-mobile-filter-panel-correction.md` | Development | Fix phone-width filter panel visibility. | Product requested; Development action needed | Yes |
| #14 / `issues/100-slice-4-filter-behavior.md` | Product/UX/Development/QA | Wire draft/edit/remove/apply behavior. | Not ready | Blocked by Slice 3 |
| #15 / `issues/110-slice-5-validation.md` | QA/Product/Development | Validate cross-layer behavior and regressions. | Not ready | Blocked by Slice 4 |
| #16 / `issues/120-final-handoff.md` | Product/Development/QA | Publish final handoff and closure status. | Not ready | Blocked by final QA |

## Artifact links

- Capability brief: `capability-brief.md`
- Decisions: `decisions.md`
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-010.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue bodies are present locally.
- [x] Remote GitHub issues are created and linked.
