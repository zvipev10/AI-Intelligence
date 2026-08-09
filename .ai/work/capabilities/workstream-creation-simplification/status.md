# Capability Status

## Capability

Evidence-first workstream creation

## Current phase

Phase 5 — corrective target-results validation

## Overall status

Target-results visibility correction deployed; awaiting user validation before merge

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Validation required | Test target-based show/hide results control | Merge approval |
| Development | Complete | Preserve rollback path until validation | Merge approval |
| UX | Review required | Confirm target and raw-record controls behave consistently | Product validation |
| QA/Security | Complete | Regression and bilingual production contract checks passed | Merge approval |
| Architecture/Security | Not independently triggered | Join developer/QA review if a new orchestration guard or permission is proposed | Implementation |

## Latest change since previous review

The deployed UI now renders the shared show/hide-results control for root target references as well
as active artifact indications.

## Current blockers

- Merge is blocked on validation of the target-results visibility correction.

## Current risks

- Existing tools may not expose enough context for reliable field inference.
- Raw-record expansion may be slow or broad without an explicit budget.
- "Create new targets" remains ambiguous between preparing candidate context and persisting a target.

## Next expected artifact

User validation result, followed by merge approval or corrective refinement.

## Parent issue

Pending remote creation; local draft: `issues/parent-capability.md`.

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| Pending remote issue | Product | Approve capability semantics | Complete in artifacts | No |
| Pending remote issue | Development | Validate tool and orchestration approach | Complete in artifacts | No |
| Pending remote issue | UX | Review inferred-fields and clarification experience | Complete in artifacts | No |
| Pending remote issue | QA/Security | Review tests and protected-write boundary | Complete in artifacts | No |
| Pending remote issue | Planning | Produce execution plan after reviews | Complete in artifacts | No |

## Artifact links

- Capability brief: `capability-brief.md`
- Decisions: pending
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-006-target-results-toggle.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue drafts are identified.
