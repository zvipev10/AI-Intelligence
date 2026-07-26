# Capability Status

## Capability

Collaborative Scenario Playback

## Current phase

Indication artifact role-review checkpoint

## Overall status

Phase 1 is merged; Product approved the first shared artifact; artifact-specific Development/Architecture, UX, and QA draft recommendations are ready for human acceptance

## Accepted direction captured

- The product direction is a collaborative workspace where humans and agents jointly own tasks and artifacts.
- Every agent must provide a concrete functional advantage.
- A scenario may start from a supported object, investigation, question, or prepared context.
- The demo uses an explicitly labeled historical replay.
- Specific targets and records are reference fixtures, not capability semantics.
- Phase 1 excludes individual Investigation Memory item selection.

## Who needs to act now

| Role | Status | Required action |
|---|---|---|
| Product | Approved | No action. |
| Development/Architecture | Approval needed | Accept or revise `artifact-001-developer-review.md`. |
| UX | Approval needed | Accept or revise the Moshe-interpreted general-chat flow in `artifact-001-ux-review.md`. |
| QA/Security | Approval needed | Accept or revise `artifact-001-qa-review.md`. |

## Current blockers

- No Phase 1 blocker remains.
- Execution planning is blocked until the artifact-specific role reviews are ready.
- Broader manifest, adapter, and trigger decisions remain deferred beyond Phase 1.

## Current risks

- Future evidence may leak through retrieval paths not covered by replay filtering.
- A first demo deployment may still use global state and interfere with concurrent users.
- Automatic reevaluation may race with repeated stage changes.
- Over-generalization may produce an abstract framework without a compelling first experience.

## Next expected artifact

Human acceptance or requested changes for the three artifact-specific role reviews.

## Parent and child issues

| Issue | Role | Status | Blocking? |
|---|---|---|---|
| #25 | Parent capability | Open | — |
| #26 | Product | Draft review ready; human approval pending | Yes |
| #27 | Development/Architecture | Phase 1 Slice 1 approved; broader review remains open | No |
| #28 | UX | Draft review ready; human approval pending | Yes |
| #29 | QA/Security | Phase 1 Slice 1 approved; broader review remains open | No |
| #30 | Phase 1 persistence | Closed; PR #31 merged | No |
| #32 | Phase 1 chat UX | Closed; PR #33 merged | No |
| #35 | Target Assessment Lead Product definition | Approved; closes with PR #36 | No |
| #37 | Artifact Development/Architecture review | Draft ready | Yes |
| #38 | Artifact UX review | Draft ready | Yes |
| #39 | Artifact QA/Security review | Draft ready | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Product review: `product-review.md`
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA/Security review: `qa-review.md`
- Execution plan: `execution-plan.md` (Phase 1 approved)
- Latest checkpoint: `checkpoint-002.md`
- Current handoff: `handoff-summary.md`
- First artifact definition: `artifact-001-target-assessment-lead.md`
- Artifact Development/Architecture review: `artifact-001-developer-review.md`
- Artifact UX review: `artifact-001-ux-review.md`
- Artifact QA/Security review: `artifact-001-qa-review.md`
