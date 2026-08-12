# Capability Status

## Capability

Investigation welcome page (`welcome-page`)

## Current phase

Phase 1 — capability initiation

## Overall status

Pending review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Pending human input | Approve scope and answer navigation/action questions | Role enrichment |
| Development | Pending | Review initialization and view-switching feasibility | Execution planning |
| UX | Pending | Review ribbon structure, nested controls, and RTL flow | Execution planning |
| QA | Pending | Define regression and accessibility coverage | Execution planning |
| Architecture/Security | Not required | Reassess only if persistence or permissions enter scope | Implementation |

## Latest change since previous review

Initial capability brief created from the requested welcome-page behavior and the existing Serbia/North Kosovo frontend.

## Current blockers

- Required human checkpoint has not approved product/UX behavior.
- Return-to-welcome, workspace header, mock action, language control, and refresh behavior are not yet decided.

## Current risks

- Map rendering after revealing an initially hidden workspace.
- Conflicting semantics between clickable ribbons and nested action controls.
- Demo actions appearing persistent.

## Next expected artifact

Draft developer and UX reviews after product answers/accepts the open questions.

## Parent issue

Remote issue not created. Draft: `issues/parent-capability.md`.

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/product-review.md` | Product | Approve behavior and resolve open decisions | Draft | Yes |
| `issues/developer-review.md` | Development | Validate implementation approach | Draft | Yes |
| `issues/ux-review.md` | UX | Validate interaction and responsive design | Draft | Yes |
| `issues/qa-review.md` | QA | Define validation coverage | Draft | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Decisions: Not created
- Developer review: Not created
- UX review: Not created
- QA review: Not created
- Execution plan: Not created
- Latest checkpoint: Not created
- Handoff: Not created

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue draft paths are current.
