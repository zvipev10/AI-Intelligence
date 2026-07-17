# Capability Status

## Capability

מכלול - investigation team management

## Current phase

Capability initiation

## Overall status

Draft / Pending review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Pending | Confirm `מכלול` semantics, MVP scope, predefined users, and UI placement. | Developer review |
| Development | Pending | Review feasibility, data model, asset strategy, and integration point. | Execution planning |
| UX | Pending | Define compact presentation, avatar behavior, placement, and responsive states. | Execution planning |
| QA | Pending | Define edge cases and regression checks. | Execution planning |
| Architecture/Security | Watch | Review only if MVP stores team state or introduces real identity/user semantics. | Execution planning |

## Latest change since previous review

Initial capability workspace created from Product input: `מכלול` should represent a team that works with the analyst on investigations. MVP starts with predefined users, each with a picture and name. Future team members may be real users or agents.

## Current blockers

- Product has not yet provided the predefined users, pictures, count, roles, or exact UI placement.
- MVP behavior is not yet closed: read-only display versus selecting/assigning members to an investigation.

## Current risks

- The Hebrew term `מכלול` may imply more operational structure than a simple member list.
- Static predefined users must be modeled carefully so future real users and agents can be added without rework.

## Next expected artifact

Product review or Product-approved clarification for the open questions in `capability-brief.md`.

## Parent issue

Local draft: `issues/000-parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/010-product-review.md` | Product | Close semantics, MVP behavior, predefined users, and placement. | Draft | Yes |
| `issues/020-developer-review.md` | Development | Review implementation approach and risks. | Draft | Yes |
| `issues/030-ux-review.md` | UX | Review flow, layout, and avatar/name treatment. | Draft | Yes |
| `issues/040-qa-review.md` | QA | Review test plan and regression surface. | Draft | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Decisions: not created yet
- Developer review: not created yet
- UX review: not created yet
- QA review: not created yet
- Execution plan: not created yet
- Latest checkpoint: not created yet
- Handoff: not created yet

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue links are current.
