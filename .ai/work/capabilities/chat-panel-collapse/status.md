# Capability Status

## Capability
Minimize and restore the chat panel

## Current phase
Capability initiation / review gate

## Overall status
Pending review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Ready | Confirm the brief reflects the requested behavior | Implementation planning |
| Development | Pending | Review the proposed grid-track approach | Implementation planning |
| UX | Pending | Confirm control placement and states | Implementation planning |
| QA | Pending | Confirm acceptance and regression coverage | Implementation planning |
| Architecture/Security | Not required | No new data, service, or permission boundary | — |

## Latest change since previous review
Initial capability definition created from the supplied divider screenshot.

## Current blockers
Repository workflow requires approval of the UX/development behavior before product code changes.

## Current risks
- Restore control visibility while the chat track is collapsed.
- Conflict between click and drag handling on the divider.
- Map sizing after the layout transition.

## Next expected artifact
Approved role reviews followed by `execution-plan.md`.

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
- Developer review: Pending
- UX review: Pending
- QA review: Pending
- Execution plan: Pending
- Latest checkpoint: Pending
- Handoff: Pending

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue drafts are current.
