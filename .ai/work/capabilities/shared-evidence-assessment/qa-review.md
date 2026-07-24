# QA / Security Review

## Status

Phase 1 Slice 1 persistence/API validation approved by the human QA owner on 2026-07-24. Broader scenario-runtime and security recommendations remain pending.

## Highest-risk invariants

1. Unreleased scenario information cannot be retrieved, counted, inferred, or referenced through any user or agent path.
2. The core runtime behaves the same with multiple valid fixture definitions and contains no object-specific assumptions.
3. Agents cannot overwrite protected human decisions or apply results to a stale runtime revision.

## Contract tests

- Validate manifest versions, references, stages, transitions, assignments, contribution types, decisions, and reset policies.
- Reject unknown transition/contribution types unless provided by a registered adapter.
- Load at least two structurally different fixture scenarios through the same runtime.
- Verify no core API or UI shell requires fixture-specific identifiers or option wording.
- Verify a scenario can use no simulated clock and still play correctly.

## Visibility and leakage

Each adapter must pass a capability matrix covering direct lookup, batch retrieval, text/structured/semantic search, aggregation, correlation/fusion, counts, and agent tools. Tests derive forbidden references from the active manifest revision.

## State, concurrency, and recovery

- Start and advance are idempotent.
- Invalid/skipped transitions are rejected.
- Concurrent advance produces one revision and expected assignment runs.
- Unaffected assignments do not rerun.
- Old-revision results cannot modify current artifacts.
- Reset during active work cancels, rejects, or stales results according to policy.
- Restart/refresh preserves runtime and workstream integrity.

## Artifact and authority integrity

- Contributions retain participant, assignment, time, runtime revision, references, and state.
- Contribution payloads conform to declared types.
- Agents cannot exceed assignment authority.
- Human decisions cannot be overwritten.
- Stale/superseded history remains reviewable.
- Protected domain sources are not mutated by reset.

## UX, accessibility, and regression

- Playback/simulation labeling remains visible where applicable.
- Generic shell and two distinct adapters work in RTL/LTR and keyboard flows.
- Async changes are announced accessibly.
- Inactive playback preserves existing chat, domain views, memory, search, and agent behavior.

## Fixture-specific validation

The first historical target story may be tested for its expected releases and judgment point, but those tests live in fixture coverage. Passing that fixture alone is insufficient for platform acceptance.

## Release blockers

- Future-information leakage.
- Core coupling to a fixture object, identifier, agent name, or decision wording.
- Agent overwrite of human decisions.
- Duplicate transition/application.
- Reset mutation of protected source data.
- No recovery from agent failure.

## Approval

- [ ] Approved
- [ ] Approved with changes recorded below
- [ ] Changes requested

Human reviewer:

Date:

Notes:
