# Capability Status

## Capability

מכלול - investigation team management

## Current phase

Slice 1 implementation complete; review pending

## Overall status

Pending Product/UX/QA review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Complete | Product definition approved five predefined users, generated pictures, and compact placement near investigation-name combo. | Done |
| Development | Complete | Implemented and validated static local data/assets for Slice 1. | Done |
| UX | Review needed | Review compact strip below investigation combo. | Before Slice 2 |
| QA | Review needed | Validate Slice 1 behavior and regressions. | Before Slice 2 |
| Architecture/Security | Watch | Review only if MVP stores team state or introduces real identity/user semantics. | Execution planning |

## Latest change since previous review

Slice 1 implemented and validated a static read-only `מכלול` strip near the investigation combo with five generated local avatar assets.

## Current blockers

No current blockers. Product/UX/QA review is pending.

## Current risks

- Static predefined users must be modeled carefully so future real users and agents can be added without rework.
- Generated picture style is not yet specified; UX/development should choose a consistent approach or request Product preference if needed.

## Next expected artifact

Product/UX/QA review of `checkpoint-001.md`.

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
- Latest checkpoint: `checkpoint-001.md`
- Handoff: not created yet

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue links are current.
