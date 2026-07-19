# Checkpoint Summary

## Checkpoint

001 - Slice 1 shared agent invocation and result pipeline

## Capability

Moshe Attack Targets MVP

## Related issue

`issues/060-slice-1-shared-agent-pipeline.md`

## Checkpoint status

Rebuilt and redeployed on the member-enabled baseline; user validation passed, architecture/interface validation pending

## Handoff

Next role: Development/Architecture reviewer

Required action: Review the shared result envelope, normalization extraction, and agent-neutral UI entry point.

Expected output: Approve Slice 1 or request focused changes.

Do not proceed to: Slice 2 SQLite implementation.

Until: This checkpoint is approved.

## What changed since previous review

The user approved Slice 1 and explicitly authorized development.

## Slice goal

Create reusable General/Moshe result infrastructure without changing General-agent behavior or implementing Moshe routing, storage, fusion, or target presentation.

## What changed

- Extracted tool-result location/entity/group normalization from `HermesClient` into `agent_result_pipeline.py`.
- Added a backward-compatible shared result envelope with `responding_agent`, `session_id`, optional `mission_run_id`, and validated typed layers.
- Applied the envelope to live General-agent responses.
- Renamed the frontend result entry point from `applyHermesResult` to agent-neutral `applyAgentResult` and updated all callers.
- Added focused unit and integration regression tests.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/agent_result_pipeline.py`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/test_agent_result_pipeline.py`
- `.ai/work/capabilities/moshe-attack-targets/execution-plan.md`
- `.ai/work/capabilities/moshe-attack-targets/status.md`
- `.ai/work/capabilities/moshe-attack-targets/issues/055-execution-plan-review.md`
- `.ai/work/capabilities/moshe-attack-targets/issues/060-slice-1-shared-agent-pipeline.md`
- `.ai/work/capabilities/moshe-attack-targets/checkpoint-001.md`

## Decisions made

- Preserve the legacy General response fields while adding agent metadata, avoiding a coordinated breaking API migration.
- Keep typed layers generic and allowlisted; `attack_targets` remains deferred to Slice 5.
- Keep agent-specific routing and attribution behavior out of Slice 1.

## Tests/checks run

- Six Python unit/integration tests passed.
- `server.py` and `agent_result_pipeline.py` compiled successfully.
- `app.js` passed `node --check`.
- Local HTTP smoke test returned 200 for `/` and `/api/status`, reporting Hermes mode and 14,800 V2 rows.
- No stale `applyHermesResult` or nested extracted normalizer definitions remain.
- `git diff --check` passed before checkpoint creation and will be rerun after it.

## VM deployment

- Deployed the approved Slice 1 runtime files on 2026-07-19 using a scoped, rollback-capable deployment.
- Replaced only `server.py`, `app.js`, and `agent_result_pipeline.py`; dataset, MCP, Hermes configuration, and service unit were not replaced.
- VM service `serbia-poc-ui.service` is active.
- `/api/status` reports build `serbia-poc-v2.1`, dataset `v2.1`, and 14,800 rows.
- Remote backend module and frontend `applyAgentResult` entry point are present.
- Rollback backup: `/opt/serbia-poc-ui-backups/slice1-20260719T182108Z`.

## Deployment regression and recovery

- The first Slice 1 deployment replaced the member-enabled VM `app.js` with a stale branch version, removing member rendering and `@` autocomplete while leaving the dynamic member container empty.
- Root cause: the Moshe branch did not contain the member UI commits from `codex/integrate-michlol-dataset-v2`; the original regression suite validated only the stale branch baseline.
- Rebuilt Slice 1 by merging the current member-enabled baseline and retaining the shared `applyAgentResult` entry point.
- Added `test_member_ui_regression.py` to require the member container, renderer, Moshe roster entry, mention autocomplete, and shared agent entry point together.
- Local browser validation confirmed the member strip and all five `@` suggestions.
- Redeployed on 2026-07-19. VM verification confirms `renderMichlolTeam`, `activeMentionRange`, `applyAgentResult`, and `michlolTeam` are all present.
- V2.1 remains active with 14,800 rows and `serbia-poc-ui.service` is active.
- Current rollback backup: `/opt/serbia-poc-ui-backups/slice1-20260719T183742Z`.
- User functional UI validation passed on 2026-07-19: "Looks ok."

## Not completed yet

- SQLite target storage and tools.
- Fusion/source-independence tooling.
- Moshe profile, routing, sessions, and presentation.
- Full evaluation and deployment.

## Blockers

- Architecture/interface checkpoint approval.
- Draft PR creation remains blocked because GitHub CLI is unavailable in this workspace; the shared branch is published separately.

## Risks

- External consumers that strictly reject additional JSON fields could require confirmation, although the existing browser client is tolerant and passed smoke checks.
- Full live Hermes investigation was not invoked because it would exercise remote state and is unnecessary for this compatibility refactor.
- Future deployments must be based on the integrated member-enabled application, not only the V2.1 data branch.

## Open questions

None for Slice 1.

## Review requested from

Development/Architecture.

## Continue / pause recommendation

Pause for checkpoint review.

## Next planned slice

Slice 2 - SQLite target bank and constrained tools.
