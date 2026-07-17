# Capability Status

## Capability

מכלול - investigation team management

## Current phase

Three-dot outside-tap dismissal implemented; deployment and review pending

## Overall status

Pending deployment and Product/UX/QA review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Complete | Product definition approved five predefined users, generated pictures, and compact placement near investigation-name combo. | Done |
| Development | Complete | Added outside-tap dismissal for the three-dot teammate expander. | Done |
| UX | Review needed | Review corrected compact header on the VM. | Before Slice 2 |
| QA | Review needed | Validate corrected compact header and regressions on the VM. | Before Slice 2 |
| Architecture/Security | Watch | Review only if MVP stores team state or introduces real identity/user semantics. | Execution planning |

## Latest change since previous review

Added the requested dismissal behavior in `checkpoint-004.md`: when the three-dot teammate expander is open, any pointer tap outside the control closes it. Interactions inside the expanded list remain available.

## Current blockers

No current blockers. Product/UX/QA VM review is pending.

## Current risks

- Static predefined users must be modeled carefully so future real users and agents can be added without rework.
- Generated picture style is not yet specified; UX/development should choose a consistent approach or request Product preference if needed.

## Next expected artifact

Deploy and review the outside-tap dismissal described in `checkpoint-004.md`.

## Parent issue

Local draft: `issues/000-parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/010-product-review.md` | Product | Close semantics, MVP behavior, predefined users, and placement. | Complete | No |
| `issues/020-developer-review.md` | Development | Review implementation approach and risks. | Complete | No |
| `issues/030-ux-review.md` | UX | Review flow, layout, and avatar/name treatment. | Complete | No |
| `issues/040-qa-review.md` | QA | Review test plan and regression surface. | Complete | No |

## Artifact links

- Capability brief: `capability-brief.md`
- Product review: `product-review.md`
- Decisions: not created yet
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-004.md`
- Handoff: not created yet

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue links are current.
