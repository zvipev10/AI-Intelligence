# Capability Status

## Capability

Complete draft investigation creation (`draft-investigation-completion`)

## Current phase

Phase 5 — accepted release

## Overall status

Accepted; checkpoint 002 ready for deployment

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product/UX | Accepted | Participant presentation removal explicitly requested | Complete |
| Development | Complete | Deploy checkpoint 002 | Release |
| QA | Complete | Full regression suite passed | Complete |
| Architecture/Security | Not required | Reassess only if real invitations enter scope | Release |

## Latest change since previous review

Removed the modal-only participant presentation while preserving regular participants after creation; 133 tests pass.

## Current blockers

None.

## Current risks

No new material risk; participant rendering after creation remains on the existing regular-investigation path.

## Next expected artifact

Deploy checkpoint 002 and merge to `main`.

## Parent issue

Local draft: `issues/parent-capability.md`.

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| Product/UX checkpoint | Product/UX | Approve modal behavior | Complete | No |
| Implementation | Development | Build draft conversion and save continuation | Complete | No |
| Final QA | QA | Validate regression and acceptance criteria | Complete | No |

## Artifact links

- Capability brief: `capability-brief.md`
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Decisions: `decisions.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-002.md`
- Handoff: pending

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue draft paths are current.
