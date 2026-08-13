# Capability Status

## Capability

Complete draft investigation creation (`draft-investigation-completion`)

## Current phase

Phase 2 — product/UX checkpoint

## Overall status

Pending human review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product/UX | Pending | Approve participant interaction and duplicate-name behavior | Execution planning |
| Development | Draft reviewed | Await product/UX checkpoint | Coding |
| QA | Draft reviewed | Await product/UX checkpoint | Coding |
| Architecture/Security | Not required | Reassess only if real invitations enter scope | Release |

## Latest change since previous review

Created the capability contract and draft technical/UX/QA reviews from current `main`.

## Current blockers

Human approval of the two product/UX choices in `capability-brief.md`.

## Current risks

Pending save continuation could double-submit if modal state is not single-use.

## Next expected artifact

Approved reviews, then `execution-plan.md`.

## Parent issue

Local draft: `issues/parent-capability.md`.

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| Product/UX checkpoint | Product/UX | Approve modal behavior | Pending | Yes |
| Implementation | Development | Build draft conversion and save continuation | Pending | Yes |
| Final QA | QA | Validate regression and acceptance criteria | Pending | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Execution plan: pending
- Handoff: pending

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue draft paths are current.
