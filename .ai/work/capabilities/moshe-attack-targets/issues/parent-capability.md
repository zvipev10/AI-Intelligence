# [Capability] Moshe Attack Targets MVP

## Capability

Create a manually invoked Hermes agent, Moshe, that fuses end-state V2.1 evidence into explainable candidates stored in a global SQLite-backed `attack targets` layer for human approval or rejection.

## Current phase

Execution planning complete; Checkpoint B approval required before coding.

## Overall status

Pending review

## Operational status

See `.ai/work/capabilities/moshe-attack-targets/status.md`.

## MVP scope

- SQLite `targets` and `target_evidence` storage with candidate-only MVP lifecycle.
- Explicit `@משה` routing with consecutive-message Hermes session continuity.
- Shared General/Moshe backend, result normalization, layer, and frontend presentation modules.
- Candidate creation from at least two independent source groups.
- Compact evidence snapshots and fusion explanation.
- Moshe-owned clarification, investigation, candidate creation, and presentation.
- Final-state V2.1 processing with no movement or revision workflows.
- Existing location/entity references and layer presentation conventions.

## Acceptance criteria

- [ ] Chapter 1 schema passes developer and architecture/security review.
- [x] Chapter 2 shared agent/presentation refactor passes developer review.
- [ ] Fusion tools and Moshe mission contract are approved.
- [ ] All 300 positive V2.1 chains and 100 hard negatives are evaluated.
- [ ] Evaluator truth is inaccessible to runtime and Moshe.
- [ ] Human approval/rejection flow is accepted.
- [ ] Production deployment and rollback are verified.

## Child tasks

- [x] Product review: Chapter 1 schema decisions.
- [x] Developer review: SQLite schema baseline approved; implementation details remain gated.
- [x] Developer review: shared agent/backend presentation refactor.
- [x] UX review: explicit routing, Moshe attribution, candidate map/table layer, evidence, and states.
- [x] QA review: V2.1 fusion, hard-negative, isolation, routing, persistence, regression, and production plan.
- [x] Architecture/security review: SQLite access, permissions, truth isolation, backup, and reset.
- [ ] Execution plan approval; draft complete locally.
- [ ] Persistence implementation and review.
- [ ] Fusion tools implementation and review.
- [ ] Moshe agent implementation and review.
- [ ] Full evaluation.
- [ ] UI implementation and review.
- [ ] Final QA and handoff.

## Artifacts

- Capability brief: `.ai/work/capabilities/moshe-attack-targets/capability-brief.md`
- Status: `.ai/work/capabilities/moshe-attack-targets/status.md`
- Decisions: `.ai/work/capabilities/moshe-attack-targets/decisions.md`
- Chapter 1: `.ai/work/capabilities/moshe-attack-targets/chapter-001-target-bank-schema.md`

## Closure rule

Keep this parent issue open until all required child tasks are closed, acceptance criteria are satisfied, final QA is complete, and final handoff is published.
