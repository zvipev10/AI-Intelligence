# Capability Status

## Capability

Recorded workstream messages

## Current phase

Capability definition / review gate

## Overall status

Pending review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Pending | Approve read-only snapshot behavior and duplicate policy | Planning |
| Development | Pending | Review typed schema and shared renderer approach | Planning |
| UX | Pending | Approve modal labels, replay badge, and disabled actions | Planning |
| QA | Pending | Review mutation-safety and regression coverage | Planning |
| Architecture/Security | Not triggered | Reassess if raw HTML persistence is proposed | Implementation |

## Latest change since previous review

Product clarified that both workstream messages must expose the actual existing
recording save interaction, including persistence—not replay support alone.

## Current blockers

Product and UX choices in `capability-brief.md` remain open.

## Current risks

Historical replay must never expose live workstream mutation actions or trust
stored HTML.

## Next expected artifact

Developer, UX, and QA review artifacts after Product confirms the proposed MVP.

## Parent issue

Draft: `issues/parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/001-product-ux-review.md` | Product/UX | Confirm behavior and labels | Draft | Yes |
| `issues/002-developer-qa-review.md` | Development/QA | Confirm schema and tests | Draft | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Status: `status.md`
- Parent issue: `issues/parent-capability.md`
- Reviews: pending
- Execution plan: pending
- Checkpoint: none
- Handoff: pending

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Draft issue links are current.
