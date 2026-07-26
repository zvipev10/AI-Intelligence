# Checkpoint 003 — Indication Artifact Persistence/API

## Scope completed

- Added a focused `workstream_artifacts` service rather than expanding workstream normalization further.
- Added a generic artifact envelope and the first `target_assessment_lead` validator.
- Added server-owned artifact/indication IDs, timestamps, and append-only revision entries.
- Added human-participant and confirmation-turn attribution.
- Added optimistic `expected_revision` handling with `409 Conflict`.
- Added read-only resolution of `REC-...` indications from the explicitly attached event layer.
- Added read-only resolution of an optional `TGT-...` assessment subject.
- Added one-active-artifact enforcement.
- Added additive GET/create/revision APIs under the existing workstream routes.
- Preserved removed indications in history and prevented silent re-addition under a new ID.
- Prevented removal of the final active indication.
- Prevented artifact mutation after archive, rejection, or assessment handoff.

## API delivered

- `GET /api/workstreams/{workstream_id}/artifacts`
- `POST /api/workstreams/{workstream_id}/artifacts`
- `GET /api/workstreams/{workstream_id}/artifacts/{artifact_id}`
- `POST /api/workstreams/{workstream_id}/artifacts/{artifact_id}/revisions`

## Validation

- Full Python test discovery: 48 tests passed.
- Focused artifact, workstream, routing, result-pipeline, target-catalog, Moshe-profile, and UI-regression coverage passed.
- `python -m py_compile server.py workstream_artifacts.py` passed.
- `git diff --check` passed.

The test runtime initially lacked the existing `PyYAML` dependency required by `test_moshe_profile`; it was installed into the runtime and the complete suite then passed.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/workstream_artifacts.py`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/test_workstream_artifacts.py`
- capability status and handoff artifacts

## Deliberately incomplete

- No Moshe profile or MCP tools.
- No result-envelope changes.
- No chat rendering or behavior changes.
- No assessment execution.
- No target-bank writes.

## Review findings

### Blocking issues

None found in automated review.

### Non-blocking comments

- Actor attribution remains a single-user demo contract rather than authentication.
- Target resolution depends on the existing target-catalog configuration being available in the deployment.

### Missing tests

No missing Slice 1 test is considered blocking. Slice 2 must add cross-runtime proposal/action and natural-language evaluation coverage.

## Recommendation

Approve Slice 1 for merge, close issue #41, and begin Slice 2 only after Development/Architecture and QA/Security checkpoint acceptance.

## Approval

Approved by the human owner on 2026-07-26 with authorization to merge and begin Slice 2.
