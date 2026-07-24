# Checkpoint Summary

## Checkpoint

001 — Phase 1 persistence and API foundation

## Capability

Collaborative Scenario Playback

## Related issue

#30; parent #25

## Checkpoint status

Complete — pending Development/Architecture and QA review

## Handoff

Next role:
Development/Architecture and QA

Required action:
Review the dedicated workstream schema, validation, atomic persistence, API boundary, and tests.

Expected output:
Approve Slice 1 or request changes.

Do not proceed to:
Minimal workstream UI shell.

Until:
The Slice 1 checkpoint is reviewed.

## Slice goal

Persist and reopen a minimal investigation-associated unit of shared human-agent work independently from chat, scenario playback, and Investigation Memory item selection.

## What changed

- Added a dataset-version-scoped `workstreams` directory.
- Added normalized workstream creation with server-owned ID and timestamps.
- Added investigation-scoped listing and item loading.
- Added constrained updates and idempotent archive.
- Made investigation association immutable.
- Prevented updates after archive.
- Added participant and assignment validation.
- Initialized empty `artifacts`, `activity`, and `attention_requests` containers.
- Added HTTP-level persistence/API tests.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/test_workstreams.py`
- `.ai/work/capabilities/shared-evidence-assessment/checkpoint-001.md`
- `.ai/work/capabilities/shared-evidence-assessment/status.md`
- `.ai/work/capabilities/shared-evidence-assessment/handoff-summary.md`

## Decisions made

- Workstreams use a dedicated state store; Investigation Memory documents remain unchanged.
- `investigation_id` is required and immutable.
- Direct transition to `archived` through update is rejected; archive uses a dedicated idempotent action.
- Archived workstreams are immutable in Phase 1.
- Empty future-facing containers are stored but have no contribution semantics yet.

## Tests/checks run

`python -m unittest test_workstreams.py test_target_catalog_api.py test_agent_routing.py test_agent_result_pipeline.py test_member_ui_regression.py`

- 30 tests passed.
- `git diff --check` passed.

Coverage includes create, list, load, update, archive, archive idempotency, investigation scoping, invalid IDs, participant/assignment integrity, immutable investigation association, and archived-state protection.

## Not completed yet

- Workstream UI.
- Investigation Memory item selection or promotion.
- Scenario definitions or playback.
- Artifact revision semantics.
- Agent triggers.
- Human attention and decision flows.
- Production authorization.

## Risks

- File-based storage has no cross-process locking; Phase 1 assumes one UI server writer.
- Current identity values are declared metadata, not authenticated principals.
- Empty future-facing arrays must not acquire semantics before their later design review.

## Continue / pause recommendation

Pause for Development/Architecture and QA review.

## Next planned slice

Slice 2 — minimal investigation-associated workstream UI shell.
