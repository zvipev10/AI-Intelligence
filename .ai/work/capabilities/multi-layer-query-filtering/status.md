# Capability Status

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Current phase
Slice 1 review after Product feedback.

## Overall status
Changes requested.

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Waiting | Review corrected compact selector after Development publishes the next checkpoint. | Slice 2 starts |
| Development | Action needed | Remove the visible selector section/header/count from Slice 1 and keep only the compact search/autocomplete affordance. | Now |
| UX | Waiting | Validate compact selector placement after Development publishes the correction. | Slice 2 starts |
| QA | Waiting | Confirm canonical manual test fixture and review QA checklist before core filter behavior is wired. | Slice 4 completion |
| Architecture/Security | Not blocking | Review API endpoint shape and authorization assumptions if this pattern will continue beyond the local POC. | Before productionizing |

## Latest change since previous review
Product reviewed Slice 1 and requested removal of the separate visible "Data layers / Layer selection / available layers" selector section. The selector should remain a small search/autocomplete line only.

## Current blockers
- Slice 2 should not start until Development corrects the Slice 1 selector UI and publishes a new checkpoint.
- Product/UX review is needed after the selector correction.

## Current risks
- MVP row loading has no limit, which may create browser performance risk on larger datasets.
- UX and QA were previously captured indirectly; separate UX and QA artifacts have now been backfilled but still require human approval.
- GitHub issue creation is not yet confirmed from this local environment.

## Next expected artifact
`checkpoint-002.md` for the Slice 1 selector correction.

## Parent issue
GitHub issue: #3. Local issue body: `issues/000-parent-capability.md`.

## Child issues

| Local issue body | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| #4 / `issues/010-product-brief-review.md` | Product | Approve initial capability brief. | Backfilled as complete from existing brief decisions | No |
| #5 / `issues/020-developer-review.md` | Development | Review technical approach and implementation slices. | Reopened for Slice 1 correction | Yes |
| #6 / `issues/030-ux-review.md` | UX | Review selector and filter-panel UX decisions. | Changes requested for selector wrapper/header/count | Yes |
| #7 / `issues/040-qa-planning.md` | QA | Confirm test fixture and manual coverage. | Pending human QA input | Before Slice 4 acceptance |
| #8 / `issues/050-execution-plan-review.md` | Product/Development | Approve execution plan gates and slices. | Reopened after Slice 1 feedback | Yes |
| #9 / `issues/060-slice-1-implementation.md` | Development | Implement API layer catalog and selector. | Complete with changes requested | Superseded by correction |
| #10 / `issues/061-slice-1-selector-correction.md` | Development | Remove selector wrapper/header/count. | Action needed | Yes |
| #11 / `issues/070-slice-1-review.md` | Product/UX/Development | Review corrected Slice 1. | Pending correction | Yes |
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
- Latest checkpoint: `checkpoint-001.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue bodies are present locally.
- [x] Remote GitHub issues are created and linked.
