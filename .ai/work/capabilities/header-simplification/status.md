# Capability Status

## Capability

Compact upper-section controls

## Current phase

Final review and handoff

## Overall status

Complete

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Confirmed | Dataset semantics and language-control source confirmed | — |
| Development | Complete | None | — |
| UX | Complete | Deployed result validated in both locales | — |
| QA | Complete | Local and VM checks passed; baseline failures recorded | — |
| Architecture/Security | Not required | None; no architecture/security change expected | — |

## Latest change since previous review

Implementation commit `4af81c2` was deployed and verified on the VM.

## Current blockers

None.

## Current risks

- Existing HTTPS endpoint redirects to HTTP; unchanged by this capability.
- The full-package Windows deployment script still encounters a long historical-data path; focused static deployment succeeded.

## Next expected artifact

None; capability is deployed and handed off.

## Parent issue

Not created; local draft at `issues/parent-capability.md`.

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/ux-review.md` | UX/Product | Approve compact controls | Complete | No |
| `issues/developer-review.md` | Development | Validate implementation mapping | Complete | No |
| `issues/qa-review.md` | QA | Validate test coverage | Complete | No |

## Artifact links

- Capability brief: `capability-brief.md`
- Decisions: Not created
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-002.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue paths are current.
