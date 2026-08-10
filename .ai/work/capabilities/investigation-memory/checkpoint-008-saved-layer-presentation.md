# Checkpoint 008 — Saved result-layer presentation

## Status

Implemented, deployed, and ready for Product validation.

## Scope

- Newly saved layers persist a typed reconstruction definition containing complete typed IDs, dataset version, and locale.
- `GET /api/investigation-memory/layers/<memory-layer-id>/presentation` resolves the saved definition into the standard `requested_result_layers` contract.
- Investigation reopening and explicit agent presentation actions use the same normal layer pipeline.
- The read-only `present_saved_memory_layers` MCP tool emits structured `present` or `clarify` actions.
- The server validates action IDs against the saved memory provided for the active investigation.
- Presentation reports `fully_restored`, `partially_restored`, or `unavailable`; ambiguous requests use a structured `clarify` action.

## Explicit Product exclusions

- Existing context-only saved layers are not migrated.
- No new tests were added or run.

## Changed files

- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/agent_result_pipeline.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
- `.ai/work/capabilities/investigation-memory/execution-plan.md`
- `.ai/work/capabilities/investigation-memory/status.md`

## Checks

- JavaScript syntax check passed.
- Python compilation passed for the UI server, result pipeline, and MCP server.
- Git diff whitespace check passed.
- Automated tests were intentionally not run per Product instruction.

## Risks

- A reconstruction is bounded to 5,000 typed IDs to keep memory payloads finite.
- Existing saved records without a reconstruction definition remain context-only.
- The repository source baseline is behind the bilingual production asset; deployment must forward-port this focused change onto the locale-aware production version rather than overwrite it wholesale.

## Deployment

- Deployed by semantically applying the focused implementation to the current bilingual production files.
- Public UI cache version: `app.js?v=149`.
- Updated UI files: `app.js`, `server.py`, and `agent_result_pipeline.py`.
- Updated MCP file: `/opt/serbia-poc/mcp_server/server.py`.
- Restarted services: `serbia-poc-ui`, `hermes-gateway`, and `hermes-moshe-gateway`.
- All three services are active with zero automatic restarts after startup.
- Hebrew and English status endpoints each report the correct v2.1 dataset with 14,800 rows.
- Public asset verification confirmed both locale-aware boot and saved-memory presentation code.
- Rollback backup: `/opt/serbia-poc-ui-backups/memory-layer-presentation-20260810T160253Z`.
- The existing KFOR memory layer reports `missing_reconstruction_definition`, as expected because migration was excluded. Product must save a new layer to validate reconstruction.

## Review request

Product should save a new result-derived layer, request that saved layer in a later prompt, and confirm it opens as a regular map/table/timeline layer.
