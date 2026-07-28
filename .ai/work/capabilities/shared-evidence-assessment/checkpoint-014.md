# Checkpoint 014 — Timeframe-stage playback foundation

## Checkpoint status

Pending Product, Development/Architecture, and QA review.

## Handoff

Next role: Product owner.

Required action: approve or request changes to Slice 1.

Expected output: explicit approval before retrieval visibility implementation.

Do not proceed to: Slice 2 product code.

Until: the owner confirms the Slice 1 checkpoint and the proposed Slice 2
boundary.

## Slice goal

Implement the generic persistence and API foundation for historical scenario
playback using the approved simplified scenario artifact.

## What changed

- Added strict versioned scenario manifests with scenario-level scope and
  ordered timeframe stages.
- Defined stage boundaries as inclusive `from` and exclusive `to`.
- Enforced non-overlapping chronological stages and rejected unsupported
  fields, including embedded record IDs.
- Added persistent scenario runs linked to active workstreams.
- Start exposes the first stage; later stages advance one at a time.
- Visible time is cumulative from the first stage start through the current
  stage end.
- Added start/reopen, read, advance, complete, and reset APIs.
- Added optimistic revision conflicts and action-bound idempotency keys.
- Retained transition history across reset.
- Kept scenario state separate from Investigation Memory, source data,
  workstream artifacts, and the target bank.
- Added one historical fixture configured only by time windows.

## API surface

- `GET /api/scenarios`
- `GET /api/scenarios/{scenario_id}?version={version}`
- `POST /api/scenario-runs`
- `GET /api/scenario-runs/{run_id}`
- `POST /api/scenario-runs/{run_id}/advance`
- `POST /api/scenario-runs/{run_id}/complete`
- `POST /api/scenario-runs/{run_id}/reset`

Scenario discovery and run responses do not expose future stage windows.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/scenario_playback.py`
- `llm_investigation_orchestrator_serbia_poc/scenario_manifests/brnjak-engineering-assessment-v1.json`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/test_scenario_playback.py`
- capability plan, status, handoff, checkpoint, and decision records

## Decisions made

- The reusable manifest contains no record or target identifiers.
- Stage scope is expressed by time, with optional scenario-level layer filters.
- Gaps between stages are permitted; overlaps are rejected.
- Start and reset return to the first stage.
- Completion is explicit, including at the final stage.
- Reset preserves audit history and does not modify source or accepted artifact
  state.
- Atomicity is guaranteed within the current single UI-server process.

## Tests/checks run

- Full Python discovery: 93 tests passed.
- Python compilation: passed.
- Concurrent advance test: one success and one revision conflict.
- `git diff --check`: passed.

## Review findings

### Blocking issues

None within the approved Slice 1 boundary.

### Non-blocking comments

- Cross-process file locking is not implemented because the deployed demo uses
  one UI-server process. A multi-process deployment must add an external lock or
  transactional store.
- The fixture labels describe the historical case, but its reusable runtime
  contract contains no case-specific identifiers.

### Missing tests

None for the single-process foundation. Retrieval leakage tests belong to Slice
2 and UI/agent tests belong to later slices.

## Not completed yet

- Existing retrieval routes are not yet playback-filtered.
- Playback is not exposed in the UI.
- Stage advance does not yet trigger Moshe.
- The slice is not deployed.

## Risks

- Activating playback before Slice 2 would allow unreleased records through
  existing search routes. Therefore no UI activation is included.
- Timeframe scope alone assumes the configured dataset timestamps are the
  intended release authority.

## Recommendation

Approve Slice 1 and, only after a separate explicit confirmation, proceed to
Slice 2 retrieval visibility enforcement.

