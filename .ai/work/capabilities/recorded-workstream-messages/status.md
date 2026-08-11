# Capability Status

## Capability

Recorded workstream messages

## Current phase

Final acceptance

## Overall status

Recorded result-toggle correction implemented, deployed, and approved for merge

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Approved | Duplicates and existing replay convention confirmed | Complete |
| Development | Ready | Review execution plan | Implementation |
| UX | Approved | Existing replay convention confirmed | Complete |
| QA | Ready | Review execution plan and required coverage | Implementation |
| Architecture/Security | Not triggered | Reassess if raw HTML persistence is proposed | Implementation |

## Latest change since previous review

Recorded workstream cards now expose a read-only Show/Hide results control for
their restored presentation layers.
Production serves the bilingual correction as `app.js?v=162`; public asset
verification passed and all UI/Hermes services are active.
Recorded workstream detail playback now saves and restores the typed result-layer
snapshot, matching normal workstream selection. Older recordings fall back to
the live presentation endpoint when the workstream is still available.

## Current blockers

No blockers.

## Current risks

Historical replay must never expose live workstream mutation actions or trust
stored HTML.

## Next expected artifact

Merge the verified implementation to `main`.

## Parent issue

Draft: `issues/parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/001-product-ux-review.md` | Product/UX | Confirm behavior and labels | Draft | Yes |
| `issues/002-developer-qa-review.md` | Development/QA | Confirm schema and tests | Draft | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Status: `status.md`
- Parent issue: `issues/parent-capability.md`
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
- [x] Draft issue links are current.
