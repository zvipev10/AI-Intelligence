# Capability Status

## Capability
Minimize and restore the chat panel

## Current phase
Final review and handoff

## Overall status
Complete

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Approved | Inspect deployed interaction | Complete |
| Development | Complete | Implementation complete | Complete |
| UX | Complete | Visual QA passed | Complete |
| QA | Complete | Regression and browser checks passed | Complete |
| Architecture/Security | Not required | No new data, service, or permission boundary | — |

## Latest change since previous review
Initial capability definition created from the supplied divider screenshot.

## Current blockers
None.

## Current risks
- Restore control visibility while the chat track is collapsed.
- Conflict between click and drag handling on the divider.
- Map sizing after the layout transition.

## Next expected artifact
None; handoff complete.

## Parent issue
`issues/parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/developer-review.md` | Development | Validate implementation approach | Draft | Yes |
| `issues/ux-review.md` | UX | Validate interaction and placement | Draft | Yes |
| `issues/qa-review.md` | QA | Validate test coverage | Draft | Yes |

## Artifact links
- Capability brief: `capability-brief.md`
- Decisions: Not required yet
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
- [x] Parent and child issue drafts are current.
