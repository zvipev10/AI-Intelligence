# Capability Status

## Capability

Evidence-first workstream creation

## Current phase

Phase 4 — corrective implementation planning

## Overall status

Rolled back after old-baseline deployment regression; current production restored

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Approved | Original simplified behavior remains approved | Corrected deployment |
| Development | Action required | Rebase onto current production and build narrow deploy path | Redeployment |
| UX | Waiting | Validate after corrected deployment | Final acceptance |
| QA/Security | Action required | Add current-feature regression checks | Redeployment |
| Architecture/Security | Not independently triggered | Join developer/QA review if a new orchestration guard or permission is proposed | Implementation |

## Latest change since previous review

Unsafe old-baseline deployment was diagnosed and rolled back byte-for-byte to the pre-deployment backup.

## Current blockers

- Corrected current-baseline implementation and narrow deployment mechanism are required.

## Current risks

- Existing tools may not expose enough context for reliable field inference.
- Raw-record expansion may be slow or broad without an explicit budget.
- "Create new targets" remains ambiguous between preparing candidate context and persisting a target.

## Next expected artifact

Corrective developer review and revised execution plan.

## Parent issue

Pending remote creation; local draft: `issues/parent-capability.md`.

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| Pending | Product | Approve capability semantics | Approved by user | No |
| Pending | Development | Validate tool and orchestration approach | Ready | No |
| Pending | UX | Review inferred-fields and clarification experience | Ready | No |
| Pending | QA/Security | Review tests and protected-write boundary | Ready | No |
| Pending | Planning | Produce execution plan after reviews | Complete | No |

## Artifact links

- Capability brief: `capability-brief.md`
- Decisions: pending
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-002-deployment-regression-rollback.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue drafts are identified.
