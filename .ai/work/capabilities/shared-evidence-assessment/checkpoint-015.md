# Checkpoint 015 — Playback retrieval visibility

## Checkpoint status

Implemented and pending Product, Development/Architecture, and QA review.

## Handoff

Next role: Product owner.

Required action: approve or request changes to Slice 2.

Do not proceed to: Slice 3 playback controls.

Until: the owner explicitly confirms the Slice 3 boundary.

## Slice goal

Make the active scenario stage a server-owned evidence boundary so unreleased
records cannot be recovered through alternate retrieval or presentation paths.

## What changed

- The app server atomically publishes the active run's dataset, optional layers,
  cumulative timeframe, run ID, and revision.
- The evidence server validates that policy on every relevant call.
- Search, semantic search, aggregation, tracing, related-event expansion,
  comparison, challenge, linkage, sequences, direct object loading, result and
  evidence layers, and fusion discovery use the same visible event set.
- Entity and location summaries are recalculated from visible events.
- Semantic matches are post-filtered even though the index contains all data.
- Prior aggregates are reusable only under the same run revision and timeframe.
- Stored target-bank objects are unavailable during playback because they may
  contain later evidence.
- Only one scenario run may be active. Completion deactivates the policy; reset
  safely reactivates it.
- Malformed or mismatched active policy data fails closed. Inactive playback
  preserves existing behavior.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/scenario_playback.py`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
- `llm_investigation_orchestrator_serbia_poc/test_scenario_playback.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/test_playback_visibility.py`
- capability plan, status, handoff, issue, checkpoint, and decision records

## Tests/checks run

- Full Python discovery: 94 tests passed.
- Focused playback visibility tests: 8 passed.
- Scenario playback API tests: 9 passed.
- Python compilation: passed.
- `git diff --check`: passed.

## Review findings

No blocking issue was found within the approved Slice 2 boundary.

The policy is intentionally global for the current single-demo deployment.
Multi-user playback requires session-scoped propagation or a transactional
store. Stored target browsing remains unavailable until targets gain
stage-aware provenance.

## Not completed yet

- Playback controls and status are not exposed in the UI.
- Stage advance does not trigger Moshe.
- The slice is not deployed.

## Recommendation

Approve Slice 2 and, only after a separate explicit confirmation, proceed to
Slice 3 playback controls and status.
