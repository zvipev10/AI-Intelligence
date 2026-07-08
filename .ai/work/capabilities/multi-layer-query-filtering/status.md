# Capability Status

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Current phase
Slice 2 implementation review.

## Overall status
Slice 1 approved by Product and UX; Slice 2 development is implemented and waiting for Development/UX review.

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Complete | Approved the corrected selector/control/table transparency treatment in `checkpoint-005.md`. | Done |
| Development | Action needed | Review `checkpoint-006.md` and confirm shared presentation/filter helper approach before Slice 3. | Slice 3 starts |
| UX | Waiting | Review `checkpoint-006.md` for presentation/filter plumbing implications before visible filter controls are added. | Slice 3 starts |
| QA | Waiting | Confirm canonical manual test fixture and review QA checklist before core filter behavior is wired. | Slice 4 completion |
| Architecture/Security | Not blocking | Review API endpoint shape and authorization assumptions if this pattern will continue beyond the local POC. | Before productionizing |

## Latest change since previous review
UX approved Slice 1 on 2026-07-08.
Product approved Slice 1 on 2026-07-08.

Development implemented Slice 2 in `checkpoint-006.md`:
- Opened layers now initialize draft/applied filter model state.
- Field discovery, value stringification, text normalization, contains matching, AND filtering, and shared presentation item helpers were added.
- Table, map, timeline, and result counts now consume `itemsForLayerPresentation(layer)`.

## Current blockers
- Slice 3 should not start until Development/UX review `checkpoint-006.md`.

## Current risks
- MVP row loading has no limit, which may create browser performance risk on larger datasets.
- UX and QA were previously captured indirectly; separate UX and QA artifacts have now been backfilled but still require human approval.
- QA still needs to confirm the canonical manual test fixture before Slice 4 acceptance.

## Next expected artifact
Development/UX review of `checkpoint-006.md`.

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
| #12 / `issues/080-slice-2-presentation-filter-model.md` | Development | Add presentation reuse and filterable model helpers. | Implemented in `checkpoint-006.md`; pending review | Yes |
| #13 / `issues/090-slice-3-filter-panel.md` | UX/Development | Add filter panel skeleton. | Not ready | Blocked by Slice 2 review |
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
- Latest checkpoint: `checkpoint-006.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue bodies are present locally.
- [x] Remote GitHub issues are created and linked.
