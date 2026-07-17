# Capability Status

## Capability

מכלול - investigation team management

## Current phase

Slice 2 UX clarification implemented locally; VM deployment in progress

## Overall status

Pending Product/UX/QA review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Complete | Clarified prompt-only behavior, multiple mentions, all prompt surfaces, client-only metadata, and Hermes ignore instruction. | Done |
| Development | In progress | Implemented Product/UX follow-up so selected recognized `@member` mentions render blue; publishing and VM deployment are in progress. | Current task |
| UX | Complete for planning | Approved caret/input-area popover, constrained scrolling, keyboard controls, and hidden no-match state. | Done |
| QA | Review needed | Validate RTL mention typing, keyboard selection, filtering, no-match behavior, prompt submission, selected-layer prompt context, step-continuation submission, and header regression. | Before acceptance |
| Architecture/Security | Watch | Review only if MVP stores team state or introduces real identity/user semantics. | Acceptance |

## Latest change since previous review

Implemented Product/UX follow-up in `checkpoint-007.md`: selected recognized `@member` mentions now render blue in prompt surfaces while keeping prompt submission and backend behavior unchanged. Review cache keys are now `styles.css?v=85` and `app.js?v=106`.

## Current blockers

No current blockers. Product/UX/QA review is pending.

## Current risks

- Static predefined users must be modeled carefully so future real users and agents can be added without rework.
- Generated picture style is not yet specified; UX/development should choose a consistent approach or request Product preference if needed.

## Next expected artifact

Publish and deploy the follow-up described in `checkpoint-007.md`, then Product/UX/QA review on the shared VM.

## Parent issue

Local draft: `issues/000-parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/010-product-review.md` | Product | Close semantics, MVP behavior, predefined users, and placement. | Complete | No |
| `issues/020-developer-review.md` | Development | Review implementation approach and risks. | Complete | No |
| `issues/030-ux-review.md` | UX | Review flow, layout, and avatar/name treatment. | Complete | No |
| `issues/040-qa-review.md` | QA | Review test plan and regression surface. | Complete | No |
| `issues/050-member-task-mentions.md` | Product/UX/Development/QA | Define, implement, and deploy `@member` autocomplete for asking/requesting tasks from team members. | UX follow-up deployment in progress | No |

## Artifact links

- Capability brief: `capability-brief.md`
- Product review: `product-review.md`
- Decisions: `decisions.md`
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Member task mentions: `member-task-mentions-brief.md`
- Latest checkpoint: `checkpoint-007.md`
- Handoff: not created yet

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue links are current.
