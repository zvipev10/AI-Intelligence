# Capability Status

## Capability

מכלול - investigation team management

## Current phase

Defining member task mentions with `@` autocomplete

## Overall status

Clarifications complete / Ready for execution planning

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Complete | Clarified prompt-only behavior, multiple mentions, all prompt surfaces, client-only metadata, and Hermes ignore instruction. | Done |
| Development | Complete for planning | Use shared member data, reusable prompt-surface autocomplete, transient client metadata, and always-on Hermes ignore instruction. | Done |
| UX | Complete for planning | Approved caret/input-area popover, constrained scrolling, keyboard controls, and hidden no-match state. | Done |
| QA | Review needed | Confirm RTL mention typing, keyboard selection, filtering, and prompt-regression coverage. | Before implementation |
| Architecture/Security | Watch | Review only if MVP stores team state or introduces real identity/user semantics. | Execution planning |

## Latest change since previous review

Recorded Product clarifications for `@member` task mentions:

- mentions only address prompts and do not create visible task records;
- multiple members are supported in one prompt;
- autocomplete should work in every prompt-entry surface, including step-continuation prompts;
- structured mention metadata remains client-only for Slice 1;
- Hermes should be generally instructed to ignore `@member` names as investigation entities for now.
- UX/development implementation suggestions were approved: caret/input-area popover, constrained scrolling, Arrow Up/Down, Enter/Tab, Escape, hidden no-match state, and transient client metadata.

## Current blockers

No blocking Product, UX, or Development questions remain before execution planning.

QA review/test planning remains before implementation.

## Current risks

- Static predefined users must be modeled carefully so future real users and agents can be added without rework.
- Generated picture style is not yet specified; UX/development should choose a consistent approach or request Product preference if needed.

## Next expected artifact

Execution plan update for the `@member` autocomplete slice, then QA review before implementation.

## Parent issue

Local draft: `issues/000-parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/010-product-review.md` | Product | Close semantics, MVP behavior, predefined users, and placement. | Complete | No |
| `issues/020-developer-review.md` | Development | Review implementation approach and risks. | Complete | No |
| `issues/030-ux-review.md` | UX | Review flow, layout, and avatar/name treatment. | Complete | No |
| `issues/040-qa-review.md` | QA | Review test plan and regression surface. | Complete | No |
| `issues/050-member-task-mentions.md` | Product/UX/Development/QA | Define `@member` autocomplete for asking/requesting tasks from team members. | Ready for planning | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Product review: `product-review.md`
- Decisions: `decisions.md`
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
