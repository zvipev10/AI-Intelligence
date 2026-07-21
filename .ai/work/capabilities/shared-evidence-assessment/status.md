# Capability Status

## Capability

Shared Evidence Assessment

## Current phase

Capability definition and Product review

## Overall status

Draft - pending human Product review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Review needed | Confirm the capability direction, starting object, joint-ownership semantics, and review authority. | Role enrichment |
| Development/Architecture | Pending | Review persistence, revision history, atomic agent contributions, and reuse boundaries. | Execution planning |
| UX | Pending | Define the shared artifact, contribution comparison, disagreement, and attention experience. | Execution planning |
| QA | Pending | Define state-transition, provenance, corruption-recovery, and regression coverage. | Execution planning |
| Security | Pending | Review agent write authority and future human identity boundary. | Execution planning |

## Latest change since previous review

Created the initial proposal around two accepted directions: a persistent collaborative human-agent workspace, and explicit functional advantages for every agent collaborator.

## Current blockers

- Product has not selected whether the MVP assessment begins from a free question, target candidate, or both.
- Product has not defined the transition from proposed contribution to reviewed or accepted intelligence.

## Current risks

- Joint ownership could degrade into chat attribution without shared artifact state.
- The assessment may become too complex if contribution and review states are not tightly scoped.
- Current static member identity cannot support production authorization claims.

## Next expected artifact

Human Product review recorded in `product-review.md`, followed by developer/architecture review. No execution plan or product code should be created before these gates.

## Parent issue

Local draft: `issues/000-parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/010-product-review.md` | Product | Approve the product model and close MVP semantics. | Pending | Yes |
| `issues/020-developer-architecture-review.md` | Development/Architecture | Define feasible schemas, APIs, and revision/write boundaries. | Pending | Yes |
| `issues/030-ux-review.md` | UX | Define collaborative artifact flows and states. | Pending | Yes |
| `issues/040-qa-security-review.md` | QA/Security | Define integrity, permissions, recovery, and regression gates. | Pending | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Decisions: not created; no capability decision accepted yet
- Product review: pending
- Developer review: pending
- UX review: pending
- QA review: pending
- Execution plan: blocked by role reviews
- Latest checkpoint: not started
- Handoff: not started

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue links are current as local drafts.
