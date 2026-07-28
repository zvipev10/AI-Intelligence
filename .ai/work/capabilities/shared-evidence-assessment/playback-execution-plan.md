# Playback Execution Plan

## Approved design

The scenario artifact is deliberately small:

- scenario identity, version, title, and historical-playback label;
- scenario-level data scope;
- an ordered list of stages;
- one inclusive `from` and exclusive `to` timestamp per stage.

Record IDs, targets, assignments, agent state, revisions, and transition history
are not part of the reusable scenario artifact.

## Confirmation rule

The Product owner asked to approve every implementation step before product code
is changed. Each slice therefore stops after its checkpoint. The next slice may
not begin until the owner explicitly confirms it.

## Slice 1 — Scenario persistence and API foundation

Status: implemented and approved.

Scope:

- strict, versioned timeframe-stage manifest validation;
- read-only prepared scenario discovery;
- persistent scenario runs linked to an active workstream;
- start/reopen, read, advance, complete, and reset APIs;
- cumulative visible timeframe;
- optimistic revision conflicts;
- transition-bound idempotency;
- atomic single-process file persistence;
- focused and regression tests.

Explicitly excluded:

- filtering existing retrieval routes;
- UI controls;
- automatic agent reevaluation;
- deployment.

## Slice 2 — Retrieval visibility enforcement

Status: implemented; pending checkpoint approval.

Proposed scope:

- derive a playback visibility policy from the active run;
- enforce the cumulative timeframe and scenario scope across event retrieval,
  aggregation, semantic search, related-event expansion, and object loading;
- prevent unreleased records from appearing in result and evidence layers;
- preserve existing behavior when playback is inactive;
- add leakage and regression tests.

## Slice 3 — Playback controls and status

Status: not approved for implementation.

Proposed scope:

- prepared-scenario selection;
- unmistakable historical-simulation label;
- start/reopen, next-stage, complete, and reset controls;
- current stage and visible timeframe;
- loading, stale-revision, final-stage, completed, and recovery states;
- no agent automation yet.

## Slice 4 — Automatic Moshe reevaluation

Status: not approved for implementation.

Proposed scope:

- schedule exactly one reevaluation after an affected stage advance;
- pass only playback-filtered context;
- expose progress and failure;
- add or revise attributable workstream artifacts without overwriting human
  decisions;
- protect against duplicate, stale, and late agent results.

## Slice 5 — Deployed end-to-end validation

Status: not approved for implementation.

Proposed scope:

- deploy the accepted slices to the VM;
- execute the configured historical fixture;
- verify visibility, restart/reopen, reset, agent updates, artifact history, and
  target-bank immutability;
- publish release evidence and residual risks.
