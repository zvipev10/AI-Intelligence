# Capability Status

## Capability

מכלול - investigation team management

## Current phase

Compact header correction implemented; VM deployment pending

## Overall status

In progress

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Complete | Product definition approved five predefined users, generated pictures, and compact placement near investigation-name combo. | Done |
| Development | Complete | Implemented Product-requested compact header correction. | Done |
| UX | Review needed | Review corrected compact header after VM deployment. | Before Slice 2 |
| QA | Review needed | Validate corrected compact header and regressions after VM deployment. | Before Slice 2 |
| Architecture/Security | Watch | Review only if MVP stores team state or introduces real identity/user semantics. | Execution planning |

## Latest change since previous review

Product requested compact upper-header corrections. Implemented `checkpoint-003.md`: renamed title to `סביבת מודיעין`, stacked statuses, narrowed the combo, moved `מכלול` inline, and added a three-dot expander for the remaining teammates.

## Current blockers

No current blockers. VM deployment of the correction is pending.

## Current risks

- Static predefined users must be modeled carefully so future real users and agents can be added without rework.
- Generated picture style is not yet specified; UX/development should choose a consistent approach or request Product preference if needed.

## Next expected artifact

VM deployment checkpoint for the compact header correction.

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
- Latest checkpoint: `checkpoint-003.md`
- Handoff: not created yet

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue links are current.
