# Capability Status

## Capability

Collaborative Scenario Playback

## Current phase

Final MVP validation

## Overall status

Checkpoint 013 final validation passed on the deployed VM with REC-V2-007215

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
| Product | Ready | Accept the demonstrated REC-V2-007215 assessment flow. |
| Development/Architecture | Ready | Accept the server-owned persistence and scoping evidence. |
| UX | Follow-up | Consider clearer long-running Moshe progress and timeout handling. |
| QA/Security | Ready | Accept checkpoint 013 and the unchanged target-bank evidence. |

## Current blockers

- No Phase 1 blocker remains.
- No final-validation blocker remains for the demonstrated Phase 1 boundary.
- Broader manifest, adapter, and trigger decisions remain deferred beyond Phase 1.

## Latest change

- Final deployed validation passed with `REC-V2-007215`.
- Proposal remained unpersisted until a distinct explicit confirmation.
- One revision-1 assessment artifact survived restart and reopen.
- Target-bank SHA-256 remained unchanged throughout.
- The isolated validation workstream was archived after verification.
- Full functional coverage passes: 85 tests.
- The top team roster now has larger gaps and `34px` minimum click targets.
- Full test discovery passes: 85 tests.
- The opened workstream menu now matches chat text sizing; the compact header pill is restored to its original size.
- Full test discovery passes: 84 tests.
- Desktop sessions with an empty local workstream lookup now adopt the server's most recently active workstream investigation.
- Exact investigation matches remain authoritative.
- Full test discovery passes: 83 tests.
- Production smoke validation returned five workstreams, four active, for a new desktop investigation ID.

## Current risks

- Future evidence may leak through retrieval paths not covered by replay filtering.
- A first demo deployment may still use global state and interfere with concurrent users.
- Automatic reevaluation may race with repeated stage changes.
- Over-generalization may produce an abstract framework without a compelling first experience.

## Next expected artifact

Product acceptance or a follow-up issue for long-running Moshe progress UX.

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
| #41 | Artifact persistence/API | Accepted; closes with PR #45 | No |
| #42 | Moshe general-chat integration | Deployed and validated with REC-V2-007215 | No |
| #43 | Final MVP validation | Completed in checkpoint 013 | No |

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
- Latest checkpoint: `checkpoint-004.md`
- UX correction checkpoint: `checkpoint-005.md`
- Selected-teammate routing checkpoint: `checkpoint-006.md`
- Teammate selection-toggle checkpoint: `checkpoint-007.md`
- Workstream summary deduplication checkpoint: `checkpoint-008.md`
- Desktop workstream indicator checkpoint: `checkpoint-009.md`
- Workstream indicator typography checkpoint: `checkpoint-010.md`
- Workstream menu typography correction: `checkpoint-011.md`
- Team member icon spacing: `checkpoint-012.md`
- Final validation with REC-V2-007215: `checkpoint-013.md`
