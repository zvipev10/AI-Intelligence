# Capability Status

## Capability

Evidence-first workstream creation

## Current phase

Phase 1 — capability initiation by Product

## Overall status

Draft — pending human product approval

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Review required | Approve the behavior and target-persistence boundary in `capability-brief.md` | Role reviews |
| Development | Waiting | Review tool coverage after product approval | Execution planning |
| UX | Waiting | Review inference summary and one-question fallback after product approval | Execution planning |
| QA/Security | Waiting | Review evaluation and protected-write coverage after product approval | Execution planning |
| Architecture/Security | Not independently triggered | Join developer/QA review if a new orchestration guard or permission is proposed | Implementation |

## Latest change since previous review

Initial capability brief created from the reported over-questioning example.

## Current blockers

- Human product approval is required because this changes workstream behavior and the handling of
  raw records near the target-bank persistence boundary.

## Current risks

- Existing tools may not expose enough context for reliable field inference.
- Raw-record expansion may be slow or broad without an explicit budget.
- "Create new targets" remains ambiguous between preparing candidate context and persisting a target.

## Next expected artifact

Human-approved capability brief, followed by `developer-review.md`.

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
- Developer review: pending
- UX review: pending
- QA review: pending
- Execution plan: pending
- Latest checkpoint: pending
- Handoff: pending

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue drafts are identified.
