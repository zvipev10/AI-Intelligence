# Capability Status

## Capability

מכלול - investigation team management

## Current phase

Defining member task mentions with `@` autocomplete

## Overall status

Draft extension / Pending Product, UX, and Development review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Review needed | Confirm `@member` task mention MVP semantics and whether mentions create visible task records or only address prompts. | Before implementation |
| Development | Review needed | Review mention autocomplete data shape, prompt integration, and whether any API payload change is included. | Before implementation |
| UX | Review needed | Define composer autocomplete placement, keyboard behavior, filtering, and empty state. | Before implementation |
| QA | Review needed | Confirm RTL mention typing, keyboard selection, filtering, and prompt-regression coverage. | Before implementation |
| Architecture/Security | Watch | Review only if MVP stores team state or introduces real identity/user semantics. | Execution planning |

## Latest change since previous review

Added `member-task-mentions-brief.md` and `issues/050-member-task-mentions.md` to define the next `מכלול` extension: asking/requesting work from team members by typing `@member-name` with autocomplete.

## Current blockers

Product and UX must confirm the first-slice semantics before implementation:

- Does a mention create a visible task record now, or only address the prompt?
- Should multiple mentioned members be supported in one prompt?
- Should autocomplete apply only to the main prompt composer or also to step-continuation prompts?
- Should submitted prompts include structured `team_mentions` in an API payload now, or remain client/UI only until task routing is defined?

## Current risks

- Static predefined users must be modeled carefully so future real users and agents can be added without rework.
- Generated picture style is not yet specified; UX/development should choose a consistent approach or request Product preference if needed.

## Next expected artifact

Product/UX/Development review of `member-task-mentions-brief.md`, followed by an execution plan update if approved.

## Parent issue

Local draft: `issues/000-parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/010-product-review.md` | Product | Close semantics, MVP behavior, predefined users, and placement. | Complete | No |
| `issues/020-developer-review.md` | Development | Review implementation approach and risks. | Complete | No |
| `issues/030-ux-review.md` | UX | Review flow, layout, and avatar/name treatment. | Complete | No |
| `issues/040-qa-review.md` | QA | Review test plan and regression surface. | Complete | No |
| `issues/050-member-task-mentions.md` | Product/UX/Development/QA | Define `@member` autocomplete for asking/requesting tasks from team members. | Draft | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Product review: `product-review.md`
- Decisions: not created yet
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Member task mentions: `member-task-mentions-brief.md`
- Latest checkpoint: `checkpoint-004.md`
- Handoff: not created yet

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue links are current.
