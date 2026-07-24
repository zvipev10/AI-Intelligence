# Capability Status

## Capability

Persistent Target Validation with Staged Scenario Replay

## Current phase

Role-review gate

## Overall status

Draft reviews prepared — pending human approval

## Accepted direction captured

- The product direction is a collaborative workspace where humans and agents jointly own tasks and artifacts.
- Every agent must provide a concrete functional advantage.
- The first experience starts from an existing candidate target, not an unprompted assessment form.
- The demo uses an explicitly labeled historical replay.
- `TGT-D4DC7A7EBE02` is the proposed anchor.

## Who needs to act now

| Role | Status | Required action |
|---|---|---|
| Product | Human approval needed | Confirm start-from-target, human decision authority, scenario scope, and MVP boundary in `product-review.md`. |
| Development/Architecture | Human approval needed | Review the AI-authored feasibility recommendation in `developer-review.md`. |
| UX | Human approval needed | Review the AI-authored flow and state model in `ux-review.md`. |
| QA/Security | Human approval needed | Review the leakage, integrity, concurrency, and recovery gates in `qa-review.md`. |

## Current blockers

- Required role reviews are not yet human-approved.
- Demo-global versus per-user scenario scope must be explicitly accepted; the draft recommends demo-global for the first slice.
- The exact workstream persistence schema and runtime trigger contract require architecture approval.

## Current risks

- Future evidence may leak through retrieval paths not covered by replay filtering.
- Global replay state may interfere with concurrent demo users.
- Automatic reevaluation may race with repeated stage changes.
- The experience may regress into chat if artifact-level changes are not primary.

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
- Handoff: not started
