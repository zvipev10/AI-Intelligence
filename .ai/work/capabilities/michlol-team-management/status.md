# Capability Status

## Capability

מכלול - investigation team management

## Current phase

Defining member task mentions with `@` autocomplete

## Overall status

Product clarified / Pending UX and Development review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Complete | Clarified prompt-only behavior, multiple mentions, all prompt surfaces, client-only metadata, and Hermes ignore instruction. | Done |
| Development | Review needed | Review mention autocomplete data shape, prompt integration, client-only metadata, and Hermes instruction placement. | Before implementation |
| UX | Review needed | Define composer autocomplete placement, keyboard behavior, filtering, and empty state. | Before implementation |
| QA | Review needed | Confirm RTL mention typing, keyboard selection, filtering, and prompt-regression coverage. | Before implementation |
| Architecture/Security | Watch | Review only if MVP stores team state or introduces real identity/user semantics. | Execution planning |

## Latest change since previous review

Recorded Product clarifications for `@member` task mentions:

- mentions only address prompts and do not create visible task records;
- multiple members are supported in one prompt;
- autocomplete should work in every prompt-entry surface, including step-continuation prompts;
- structured mention metadata remains client-only for Slice 1;
- Hermes should be instructed to ignore `@member` names as investigation entities for now.

## Current blockers

No Product blockers remain for Slice 1 definition.

UX and Development still need to close implementation details:

- Exact autocomplete popover placement and collision behavior for each prompt surface.
- Temporary Hermes instruction wording and injection point in the current prompt flow.
- Whether client-side mention metadata remains transient or is attached to rendered local chat messages.

## Current risks

- Static predefined users must be modeled carefully so future real users and agents can be added without rework.
- Generated picture style is not yet specified; UX/development should choose a consistent approach or request Product preference if needed.

## Next expected artifact

UX and Development review of `member-task-mentions-brief.md`, followed by an execution plan update if approved.

## Parent issue

Local draft: `issues/000-parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/010-product-review.md` | Product | Close semantics, MVP behavior, predefined users, and placement. | Complete | No |
| `issues/020-developer-review.md` | Development | Review implementation approach and risks. | Complete | No |
| `issues/030-ux-review.md` | UX | Review flow, layout, and avatar/name treatment. | Complete | No |
| `issues/040-qa-review.md` | QA | Review test plan and regression surface. | Complete | No |
| `issues/050-member-task-mentions.md` | Product/UX/Development/QA | Define `@member` autocomplete for asking/requesting tasks from team members. | Product clarified | Yes |

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
