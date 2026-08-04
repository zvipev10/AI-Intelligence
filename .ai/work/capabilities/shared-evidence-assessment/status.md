# Capability Status

## Capability

Collaborative Scenario Playback

## Current phase

Investigation selection correction checkpoint

## Overall status

Checkpoint 017 exact investigation selection is implemented and pending Product/UX browser acceptance; checkpoint 016 playback acceptance also remains pending

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
| Product | Review required | Review checkpoint 016 and authorize deployment if accepted. |
| Development/Architecture | Complete | Minimal interaction and trigger are implemented. |
| UX | Review required | Confirm the one-button interaction and tooltip. |
| QA/Security | Complete | Duplicate-trigger and regression coverage pass. |

## Current blockers

- No Phase 1 blocker remains.
- Deployment is blocked on explicit Product confirmation.
- Broader manifest, adapter, and trigger decisions remain deferred beyond Phase 1.

## Latest change

- Separated investigation search from the active investigation name.
- Explicit investigation selection now loads exact scoped state and cannot adopt the latest unrelated investigation.
- Bootstrap-only fallback and stale-response protection preserve legacy continuity without overriding user selection.
- Focused JavaScript/API/playback validation passes: 45 tests.
- Added one next-stage button to the existing workstream update.
- Added a tooltip with the server-provided next-stage timeframe.
- Added one durable Moshe reevaluation claim per released revision.
- Full Python discovery passes: 95 tests.
- Enforced the active run's cumulative timeframe and optional layer scope across
  all evidence retrieval and presentation paths.
- Recomputed entity/location summaries from visible evidence and isolated
  stored target-bank objects during playback.
- Added one-active-run protection and fail-closed policy validation.
- Full Python discovery passes: 94 tests.
- Added a generic scenario artifact containing only scope and ordered timeframe stages.
- Added persistent start/reopen, advance, complete, and reset APIs.
- Future stage windows are absent from scenario discovery and run responses.
- Embedded record IDs and other unsupported manifest fields are rejected.
- Full Python discovery passes: 93 tests.
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

- A first demo deployment may still use global state and interfere with concurrent users.
- Automatic reevaluation may race with repeated stage changes.
- Over-generalization may produce an abstract framework without a compelling first experience.

## Next expected artifact

Product/UX browser acceptance of checkpoint 017, plus the outstanding Product approval of checkpoint 016, followed by explicit deployment authorization.

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
| #80 | Playback persistence/API foundation | Implemented; checkpoint review pending | Yes |
| #81 | Playback retrieval visibility | Implemented; checkpoint review pending | Yes |
| #82 | Minimal playback and Moshe trigger | Implemented; checkpoint review pending | Yes |

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
- Playback execution plan: `playback-execution-plan.md`
- Timeframe-stage foundation: `checkpoint-014.md`
- Playback retrieval visibility: `checkpoint-015.md`
- Minimal next-stage playback: `checkpoint-016.md`
- Investigation selection correction: `checkpoint-017.md`
- Investigation selection plan: `investigation-selection-execution-plan.md`
