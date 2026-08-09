# Capability Status

## Capability

Evidence-first workstream creation

## Current phase

Phase 5 — corrective design after failed product validation

## Overall status

Changes requested: supplied targets are not persisted in created workstreams; merge blocked

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Decision required | Choose durable seed-target representation | Corrective implementation |
| Development | Blocked on product decision | Preserve rollback path and prepare correction | Corrective implementation |
| UX | Review required | Review how attached targets appear in the workstream | Corrective implementation |
| QA/Security | Complete | Live target and raw-record smoke passed | Merge approval |
| Architecture/Security | Not independently triggered | Join developer/QA review if a new orchestration guard or permission is proposed | Implementation |

## Latest change since previous review

Product validation found that both Hebrew and English target-backed workstreams omit the supplied
target from their saved data.

## Current blockers

- Merge is blocked because supplied targets are used for inference but not persisted in workstreams.
- Corrective implementation is blocked on choosing root-level target references versus an initial
  target-assessment artifact.

## Current risks

- Existing tools may not expose enough context for reliable field inference.
- Raw-record expansion may be slow or broad without an explicit budget.
- "Create new targets" remains ambiguous between preparing candidate context and persisting a target.

## Next expected artifact

Corrective design decision and execution-plan update.

## Parent issue

Pending remote creation; local draft: `issues/parent-capability.md`.

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| Pending | Product | Approve capability semantics | Draft | Yes |
| Pending | Development | Validate tool and orchestration approach | Not started | Yes |
| Pending | UX | Review inferred-fields and clarification experience | Not started | Yes |
| Pending | QA/Security | Review tests and protected-write boundary | Not started | Yes |
| Pending | Planning | Produce execution plan after reviews | Blocked | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Decisions: pending
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-003-target-reference-gap.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue drafts are identified.
