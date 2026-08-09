# Handoff Summary

## Summary

The first deployment was rolled back after it was found to contain an older complete UI/MCP baseline.
Current production functionality is restored. The evidence-first change remains implemented only on
the feature branch and must be rebased onto the current production source before redeployment.

## Changed files

- `llm_investigation_orchestrator_serbia_poc/moshe_profile/SOUL.md`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
- `llm_investigation_orchestrator_serbia_poc/test_moshe_profile.py`
- `llm_investigation_orchestrator_serbia_poc/moshe_profile/workstream_evaluation_cases.json`
- capability artifacts under `.ai/work/capabilities/workstream-creation-simplification/`

## Tests and deployment

29 feature-branch tests passed, but they did not cover newer production functionality and were
therefore insufficient. Rollback verification confirmed exact restoration of managed files, active
services, and a healthy locale-aware v2.1 endpoint.

## Publishing status

Implementation commit `37bfa1e` remains pushed on `codex/workstream-creation-simplification` but must
not be deployed as-is. The rollback incident is recorded in `checkpoint-002-deployment-regression-rollback.md`.

## Assumptions

Raw-record flows may discover and prepare candidate target context but may not silently persist a new
target-bank record.

## Remaining risk

The feature branch is based on an old workstream version. Its broad deployment script can overwrite
newer UI, localization, classification, and result-presentation functionality.

## Next step

Rebase the three intended instruction changes onto the current production baseline, add regression
coverage for current capabilities, and use a narrow hash-guarded deployment path.

## Suggested durable documentation updates

After final acceptance, add the evidence-first creation policy and target-persistence boundary to
`docs/product-context.md` and `docs/decisions.md`.
