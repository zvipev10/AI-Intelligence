# Capability Status

## Capability

Collaborative Scenario Playback

## Current phase

Phase 1 execution planning

## Overall status

Phase 1 authorized; planning PR must merge before implementation branch

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
| Product | Phase 1 approved | Review the Slice 1 checkpoint after persistence/API implementation. |
| Development/Architecture | Review after Slice 1 | Review the dedicated store, schema, API, and atomicity. |
| UX | Review before Slice 2 | Approve the minimal workstream UI shell. |
| QA/Security | Review after Slice 1 | Validate persistence, input boundaries, and memory regressions. |

## Current blockers

- Required role reviews are not yet human-approved.
- PR #24 must merge before the Phase 1 implementation branch is created.
- Broader manifest, adapter, and trigger decisions remain deferred beyond Phase 1.

## Current risks

- Future evidence may leak through retrieval paths not covered by replay filtering.
- A first demo deployment may still use global state and interfere with concurrent users.
- Automatic reevaluation may race with repeated stage changes.
- Over-generalization may produce an abstract framework without a compelling first experience.

## Next expected artifact

Merge planning PR #24, branch from updated `main`, then execute Slice 1 from `execution-plan.md` under issue #30.

## Parent and child issues

| Issue | Role | Status | Blocking? |
|---|---|---|---|
| #25 | Parent capability | Open | — |
| #26 | Product | Draft review ready; human approval pending | Yes |
| #27 | Development/Architecture | Draft review ready; human approval pending | Yes |
| #28 | UX | Draft review ready; human approval pending | Yes |
| #29 | QA/Security | Draft review ready; human approval pending | Yes |
| #30 | Phase 1 implementation | Approved scope; blocked on PR #24 merge | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Product review: `product-review.md`
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA/Security review: `qa-review.md`
- Execution plan: `execution-plan.md` (Phase 1 approved)
- Checkpoint: not started
- Current handoff: `handoff-summary.md`
