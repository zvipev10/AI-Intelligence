# QA / Security Review

## Status

AI-authored draft — pending human QA/Security approval

## Highest-risk invariant

At replay revision N, no record assigned to a future stage may be returned, inferred, counted, fused, summarized, or referenced by any user or agent retrieval path.

## Required validation areas

### Visibility and leakage

- Direct future record-ID lookup returns not found/hidden.
- Batch retrieval omits future records without revealing their existence.
- Text, structured, and semantic search exclude future records.
- Fusion, similarity, source grouping, counts, and target expansion exclude future records.
- Moshe output and tool traces contain no future record IDs or facts.
- Reset returns all retrieval surfaces to the baseline stage.
- Replay inactive mode preserves existing full-corpus behavior.

Use a deny-list generated from the scenario manifest in integration tests, not model-output inspection alone.

### State and concurrency

- Start is idempotent.
- Advance requires the expected revision and cannot skip stages.
- Two concurrent advances create one new revision and one Moshe run.
- Refresh/restart preserves current stage and workstream state.
- A run completed against an old revision cannot modify the current artifact.
- Reset while a run is active cancels, rejects, or stales its result.
- Scenario state and workstream revisions cannot be partially committed.

### Artifact integrity

- Every contribution contains author, timestamp, scenario revision, raw references, and status.
- Human decisions cannot be overwritten by agent writes.
- Superseded/stale content remains in history.
- Full source rows are not duplicated into the artifact.
- Invalid or hidden raw references are rejected.
- The same stage/run cannot apply the same contribution twice.

### Agent behavior

- Baseline includes the same-place/different-entity challenge.
- Stage 1 produces a proposed evolution/movement update, not a target acceptance.
- Stage 2 presents alternatives and requests human judgment.
- Moshe does not claim proven source independence from source-group counts.
- No-evidence, timeout, malformed output, and gateway-unavailable paths are recoverable.

Behavioral checks should assert structured outputs and prohibited claims, while allowing wording variation.

### UX and accessibility

- Historical replay and simulated time remain visible.
- Asynchronous status and errors are announced accessibly.
- Keyboard and RTL flows cover stage advance, evidence inspection, and human decision.
- Proposed agent work and human decisions remain distinguishable without color.

### Regression

- Non-replay investigations use existing event visibility.
- Chat, layers, filters, memory, raw records, Moshe routing, and target catalog remain functional.
- Replay reset does not mutate source events or the target database.
- Performance remains acceptable when semantic results require over-fetching then filtering.

## Security boundary

The demo's current member identity is not authentication. Until real access control exists:

- describe replay controls as demo controls, not user permissions;
- restrict the environment operationally if concurrent or untrusted access is possible;
- never expose evaluator truth;
- validate scenario and target identifiers against the server-owned manifest;
- reject arbitrary file paths, record-release lists, and stage numbers from clients;
- log stage transitions and human decisions.

## Required failure evidence before implementation acceptance

- Automated leakage matrix covering every retrieval tool/path.
- Concurrency/idempotency tests for start, advance, and reset.
- Stale-run and partial-failure recovery tests.
- Artifact history/integrity tests.
- End-to-end deterministic replay of all stages.
- RTL/accessibility check.
- Regression suite results.

## Release blockers

- Any future-record leakage.
- Agent ability to overwrite a human decision.
- Non-idempotent stage advance or duplicate agent application.
- Reset mutating the underlying corpus/target.
- Missing historical-simulation labeling.
- No recovery path after agent failure.

## Approval

- [ ] Approved
- [ ] Approved with changes recorded below
- [ ] Changes requested

Human reviewer:

Date:

Notes:
