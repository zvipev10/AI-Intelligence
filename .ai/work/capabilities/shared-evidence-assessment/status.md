# Capability Status

## Capability

Collaborative Scenario Playback

## Current phase

Phase 1 Slice 2 Product/UX definition

## Overall status

Slice 1 approved and ready to merge; Slice 2 chat-based workstream creation is under Product/UX definition

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
| Product | Input in progress | Confirm the chat-based `מעקב` creation semantics and confirmation boundary. |
| Development/Architecture | Slice 1 approved | No action until the approved Slice 2 flow is reviewed technically. |
| UX | Review needed | Define the plus-menu `מעקב` flow, explicit layer attachment, confirmation, reopen, and error states. |
| QA/Security | Slice 1 approved | No action until Slice 2 test planning. |

## Current blockers

- Slice 2 is gated on Product/UX approval of the chat-based creation flow.
- Broader manifest, adapter, and trigger decisions remain deferred beyond Phase 1.

## Current risks

- Future evidence may leak through retrieval paths not covered by replay filtering.
- A first demo deployment may still use global state and interfere with concurrent users.
- Automatic reevaluation may race with repeated stage changes.
- Over-generalization may produce an abstract framework without a compelling first experience.

## Next expected artifact

Focused Product/UX decision for the `מעקב` flow, followed by a Slice 2 execution issue and branch.

## Parent and child issues

| Issue | Role | Status | Blocking? |
|---|---|---|---|
| #25 | Parent capability | Open | — |
| #26 | Product | Draft review ready; human approval pending | Yes |
| #27 | Development/Architecture | Phase 1 Slice 1 approved; broader review remains open | No |
| #28 | UX | Draft review ready; human approval pending | Yes |
| #29 | QA/Security | Phase 1 Slice 1 approved; broader review remains open | No |
| #30 | Phase 1 implementation | Slice 1 approved; PR #31 ready to merge | No |

## Artifact links

- Capability brief: `capability-brief.md`
- Product review: `product-review.md`
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA/Security review: `qa-review.md`
- Execution plan: `execution-plan.md` (Phase 1 approved)
- Latest checkpoint: `checkpoint-001.md`
- Current handoff: `handoff-summary.md`
