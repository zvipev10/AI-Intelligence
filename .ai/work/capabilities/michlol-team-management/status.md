# Capability Status

## Capability

מכלול - investigation team management

## Current phase

Product review complete; developer/UX/QA review pending

## Overall status

Pending role reviews

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Complete | Product definition approved five predefined users, generated pictures, and compact placement near investigation-name combo. | Done |
| Development | Pending | Review feasibility, data model, asset strategy, and integration point. | Execution planning |
| UX | Pending | Define compact presentation, avatar behavior, placement, and responsive states. | Execution planning |
| QA | Pending | Define edge cases and regression checks. | Execution planning |
| Architecture/Security | Watch | Review only if MVP stores team state or introduces real identity/user semantics. | Execution planning |

## Latest change since previous review

Product approved the MVP definition: five predefined users, generated picture for each, displayed compactly near the investigation-name combo. Future team members may be real users or agents, but that is not MVP behavior.

## Current blockers

No current blockers for developer, UX, and QA review.

## Current risks

- Static predefined users must be modeled carefully so future real users and agents can be added without rework.
- Generated picture style is not yet specified; UX/development should choose a consistent approach or request Product preference if needed.

## Next expected artifact

Developer review and UX review.

## Parent issue

Local draft: `issues/000-parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/010-product-review.md` | Product | Close semantics, MVP behavior, predefined users, and placement. | Complete | No |
| `issues/020-developer-review.md` | Development | Review implementation approach and risks. | Draft | Yes |
| `issues/030-ux-review.md` | UX | Review flow, layout, and avatar/name treatment. | Draft | Yes |
| `issues/040-qa-review.md` | QA | Review test plan and regression surface. | Draft | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Product review: `product-review.md`
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
