# Capability Status

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Current phase
Slice 3 floating filter-window correction review.

## Overall status
Slice 2 is fully approved by Product, Development, and UX. Product approved the Slice 3 floating filter-window correction; UX/Development review is still required before Slice 4 behavior wiring.

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Complete | Approved the Slice 2 VM build for unchanged visible behavior and readiness for Slice 3 filter-panel work. | Done |
| Development | Complete | Approved `checkpoint-006.md` and confirmed the shared presentation/filter helper approach for Slice 3. | Done |
| UX | Complete | Approved `checkpoint-006.md` and allowed Slice 3 to begin. | Done |
| Development | Complete | Implemented GitHub issue #17 / `issues/130-slice-3-mobile-filter-panel-correction.md` and deployed the corrected floating filter window. | Done |
| Product | Complete | Approved `checkpoint-011.md` and the VM build for corrected Slice 3 floating filter-window behavior. | Done |
| UX/Development | Action needed | Review `checkpoint-011.md` and approve or request changes before Slice 4 behavior wiring. | Before Slice 4 starts |
| QA | Waiting | Confirm canonical manual test fixture and review QA checklist before core filter behavior is wired. | Slice 4 completion |
| Architecture/Security | Not blocking | Review API endpoint shape and authorization assumptions if this pattern will continue beyond the local POC. | Before productionizing |

## Latest change since previous review
Product approved `checkpoint-011.md` on 2026-07-08 and confirmed the corrected mobile floating filter window looks good. Product noted that choosing fields on mobile belongs to the next slice; this matches Slice 4 scope.

Development implemented issue #17 in `checkpoint-011.md`:
- The filter section now opens as a floating window above the results tabs/table.
- The filter window is detached from the raw results table layout and renders over the active map/timeline surface.
- Local browser validation passed at 360x800, 390x844, 390x844 timeline view, and 768x1024.
- Deployed to the review VM with `app.js?v=83` and `styles.css?v=65`; VM returned HTTP 200.

Product changed Development request #17:
- Do not solve the mobile issue by stacking the filter section inside the raw results overlay.
- Open the filter section as a floating window above the results tabs, on top of the active map or timeline.

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
- Slice 4 should not start until UX/Development review and approve `checkpoint-011.md`, or Product explicitly waives this review.
- QA test-plan readiness is still required before Slice 4 acceptance.

## Current risks
- MVP row loading has no limit, which may create browser performance risk on larger datasets.
- UX and QA were previously captured indirectly; separate UX and QA artifacts have now been backfilled but still require human approval.
- QA still needs to confirm the canonical manual test fixture before Slice 4 acceptance.

## Next expected artifact
UX/Development review result for `checkpoint-011.md`.

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
| #13 / `issues/090-slice-3-filter-panel.md` | UX/Development | Add filter panel skeleton. | Implemented in `checkpoint-009.md`; Product approved issue #17 correction; pending UX/Development review | Yes |
| #17 / `issues/130-slice-3-mobile-filter-panel-correction.md` | Development | Change filter section to floating window above results tabs over map/timeline. | Product approved `checkpoint-011.md`; pending UX/Development review | Yes |
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
- Latest checkpoint: `checkpoint-011.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue bodies are present locally.
- [x] Remote GitHub issues are created and linked.
