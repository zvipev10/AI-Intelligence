# Capability Status

## Capability

Collaborative Scenario Playback

## Current phase

Role-review gate

## Overall status

Draft reviews prepared — pending human approval

## Accepted direction captured

- The product direction is a collaborative workspace where humans and agents jointly own tasks and artifacts.
- Every agent must provide a concrete functional advantage.
- A scenario may start from a supported object, investigation, question, or prepared context.
- The demo uses an explicitly labeled historical replay.
- Specific targets and records are reference fixtures, not capability semantics.

## Who needs to act now

| Role | Status | Required action |
|---|---|---|
| Product | Human approval needed | Confirm generic entry contexts, authority, scenario semantics, and MVP boundary in `product-review.md`. |
| Development/Architecture | Human approval needed | Review manifest, adapter, runtime, and trigger recommendations in `developer-review.md`. |
| UX | Human approval needed | Review the generic workstream shell, adapter views, and attention model in `ux-review.md`. |
| QA/Security | Human approval needed | Review contract independence, leakage, integrity, concurrency, and recovery gates in `qa-review.md`. |

## Current blockers

- Required role reviews are not yet human-approved.
- Supported starting contexts for the first slice must be selected.
- Manifest extensibility, adapter contract, persistence, and trigger model require architecture approval.
- Demo-global versus per-user runtime remains a deployment decision, not capability semantics.

## Current risks

- Future evidence may leak through retrieval paths not covered by replay filtering.
- A first demo deployment may still use global state and interfere with concurrent users.
- Automatic reevaluation may race with repeated stage changes.
- Over-generalization may produce an abstract framework without a compelling first experience.

## Next expected artifact

Human decisions recorded in the four role-review files. Only after approval should `execution-plan.md` be created.

## Parent and child issues

| Issue | Role | Status | Blocking? |
|---|---|---|---|
| #25 | Parent capability | Open | — |
| #26 | Product | Draft review ready; human approval pending | Yes |
| #27 | Development/Architecture | Draft review ready; human approval pending | Yes |
| #28 | UX | Draft review ready; human approval pending | Yes |
| #29 | QA/Security | Draft review ready; human approval pending | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Product review: `product-review.md`
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA/Security review: `qa-review.md`
- Execution plan: blocked by role approvals
- Checkpoint: not started
- Current handoff: `handoff-summary.md`
