# Capability Status

## Capability

Collaborative Scenario Playback

## Current phase

Indication artifact Slice 1 implementation

## Overall status

The execution plan is approved; Slice 1 artifact persistence/API implementation is authorized

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
| Product | Approved | No action during Slice 1. |
| Development/Architecture | Waiting for checkpoint | Review Slice 1 implementation after publication. |
| UX | Approved | No action during backend-only Slice 1. |
| QA/Security | Waiting for checkpoint | Review Slice 1 tests and persistence boundaries. |

## Current blockers

- No Phase 1 blocker remains.
- Slice 2 remains blocked until Slice 1 checkpoint acceptance.
- Broader manifest, adapter, and trigger decisions remain deferred beyond Phase 1.

## Current risks

- Future evidence may leak through retrieval paths not covered by replay filtering.
- A first demo deployment may still use global state and interfere with concurrent users.
- Automatic reevaluation may race with repeated stage changes.
- Over-generalization may produce an abstract framework without a compelling first experience.

## Next expected artifact

Slice 1 implementation and checkpoint for issue #41.

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
| #37 | Artifact Development/Architecture review | Approved; closes with PR #40 | No |
| #38 | Artifact UX review | Approved; closes with PR #40 | No |
| #39 | Artifact QA/Security review | Approved; closes with PR #40 | No |
| #41 | Artifact persistence/API | In progress | Yes |
| #42 | Moshe general-chat integration | Planned; blocked by Slice 1 acceptance | Yes |
| #43 | Final MVP validation | Planned; blocked by Slices 1–2 | Yes |

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
- Artifact execution plan: `artifact-001-execution-plan.md`
