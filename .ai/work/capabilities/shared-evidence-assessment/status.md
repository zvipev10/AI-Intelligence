# Capability Status

## Capability

Collaborative Scenario Playback

## Current phase

Phase 1 complete; next-slice definition

## Overall status

Phase 1 persistence and chat-based workstream creation are merged to `main` through PRs #31 and #33

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
| Product | Decision needed | Confirm the boundary for the first shared workstream artifact. |
| Development/Architecture | Waiting | Review the artifact/revision model after Product definition. |
| UX | Waiting | Review the chat-based propose/accept/update flow after Product definition. |
| QA/Security | Waiting | Review persistence, concurrency, and contribution-history coverage after technical definition. |

## Current blockers

- No Phase 1 blocker remains.
- The next slice must define generic artifact and revision semantics before implementation.
- Broader manifest, adapter, and trigger decisions remain deferred beyond Phase 1.

## Current risks

- Future evidence may leak through retrieval paths not covered by replay filtering.
- A first demo deployment may still use global state and interfere with concurrent users.
- Automatic reevaluation may race with repeated stage changes.
- Over-generalization may produce an abstract framework without a compelling first experience.

## Next expected artifact

Capability brief extension for a generic shared workstream artifact and explicit human/agent contribution ledger.

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

## Artifact links

- Capability brief: `capability-brief.md`
- Product review: `product-review.md`
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA/Security review: `qa-review.md`
- Execution plan: `execution-plan.md` (Phase 1 approved)
- Latest checkpoint: `checkpoint-002.md`
- Current handoff: `handoff-summary.md`
