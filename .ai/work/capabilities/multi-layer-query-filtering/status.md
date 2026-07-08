# Capability Status

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Current phase
Slice 1 UX styling checkpoint review.

## Overall status
Development implementation complete; waiting for Product/UX review.

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Action needed | Review `checkpoint-003.md` and approve or request changes to the selector/control/table transparency treatment. | Slice 2 starts |
| Development | Waiting | Support review questions; implementation is complete and API/catalog behavior was smoke-tested. | Product/UX review |
| UX | Action needed | Validate the updated selector/control/table transparency in `checkpoint-003.md`. | Slice 2 starts |
| QA | Waiting | Confirm canonical manual test fixture and review QA checklist before core filter behavior is wired. | Slice 4 completion |
| Architecture/Security | Not blocking | Review API endpoint shape and authorization assumptions if this pattern will continue beyond the local POC. | Before productionizing |

## Latest change since previous review
Development implemented Product's three UX comments in `checkpoint-003.md`:
- The selector is reduced from 360px to 190px on desktop.
- The selector and MapLibre top-left controls now share the same translucent surface.
- The raw events overlay/table now uses the same translucent surface while preserving readable text.

## Current blockers
- Slice 2 should not start until Product/UX approve `checkpoint-003.md` and issue #11 review is complete.

## Current risks
- MVP row loading has no limit, which may create browser performance risk on larger datasets.
- UX and QA were previously captured indirectly; separate UX and QA artifacts have now been backfilled but still require human approval.
- Selector/control/table transparency needs Product/UX visual review after implementation.

## Next expected artifact
Product/UX review of `checkpoint-003.md`.

## Parent issue
GitHub issue: #3. Local issue body: `issues/000-parent-capability.md`.

## Child issues

| Local issue body | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| #4 / `issues/010-product-brief-review.md` | Product | Approve initial capability brief. | Backfilled as complete from existing brief decisions | No |
| #5 / `issues/020-developer-review.md` | Development | Review technical approach and implementation slices. | Pending review of corrected Slice 1 | Yes |
| #6 / `issues/030-ux-review.md` | UX | Review selector and filter-panel UX decisions. | Pending review of corrected selector | Yes |
| #7 / `issues/040-qa-planning.md` | QA | Confirm test fixture and manual coverage. | Pending human QA input | Before Slice 4 acceptance |
| #8 / `issues/050-execution-plan-review.md` | Product/Development | Approve execution plan gates and slices. | Pending review after Slice 1 correction | Yes |
| #9 / `issues/060-slice-1-implementation.md` | Development | Implement API layer catalog and selector. | Complete with correction checkpoint | No |
| #10 / `issues/061-slice-1-selector-correction.md` | Development | Remove selector wrapper/header/count. | Implemented in `checkpoint-002.md`; follow-up UX comments implemented in `checkpoint-003.md` | No |
| #11 / `issues/070-slice-1-review.md` | Product/UX/Development | Review corrected Slice 1. | Waiting Product/UX review of `checkpoint-003.md` | Yes |
| #12 / `issues/080-slice-2-presentation-filter-model.md` | Development | Add presentation reuse and filterable model helpers. | Not ready | Blocked by Slice 1 |
| #13 / `issues/090-slice-3-filter-panel.md` | UX/Development | Add filter panel skeleton. | Not ready | Blocked by Slice 2 |
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
- Latest checkpoint: `checkpoint-003.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue bodies are present locally.
- [x] Remote GitHub issues are created and linked.
