# Capability Status

## Capability

Compact upper-section controls

## Current phase

Capability initiation and role enrichment drafts

## Overall status

Pending human review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Pending | Confirm DB/dataset semantics and language-control source | Execution planning |
| Development | Draft prepared | Validate source mapping and implementation approach | Execution planning |
| UX | Draft prepared | Approve compact control and detail interaction | Execution planning |
| QA | Pending | Review state and accessibility coverage | Coding |
| Architecture/Security | Not required | None; no architecture/security change expected | — |

## Latest change since previous review

Initial capability, UX, and developer drafts created from the user request and current header source.

## Current blockers

- No language switch exists in the checked-out UI source.
- “DB connection” may refer to the current dataset-availability status, which is not explicitly a database connection.

## Current risks

- Hover-only details would not cover keyboard or touch users.
- Compact indicators could become ambiguous without accessible labels and non-color state cues.

## Next expected artifact

Human-approved UX/developer review, followed by QA review and `execution-plan.md`.

## Parent issue

Not created; local draft at `issues/parent-capability.md`.

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/ux-review.md` | UX/Product | Approve compact controls | Draft | Yes |
| `issues/developer-review.md` | Development | Validate implementation mapping | Draft | Yes |
| `issues/qa-review.md` | QA | Validate test coverage | Draft | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Decisions: Not created
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: Not created
- Execution plan: Not created
- Latest checkpoint: Not created
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue paths are current.
