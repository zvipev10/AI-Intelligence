# Checkpoint 007 — Target ID wording

## Summary

Target-backed workstreams now persist every resolved `TGT-*` identifier in both the title and
objective. The server enforces this invariant even if the model omits an identifier; Hebrew and
English agent instructions also request the wording explicitly.

## Changed files

- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
- `llm_investigation_orchestrator_serbia_poc/moshe_profile/SOUL.md`
- focused server and profile tests

## Validation

- Focused workstream tests: 21 passed.
- Full app/backend suite: 127 passed.
- MCP suite: 54 passed, 1 skipped.
- Python compilation passed.
- Production Hebrew smoke: `ws_20260809_143759_10c3ab16`; title and objective contain
  `TGT-F2CA47CB9859`.
- Production English smoke: `ws_20260809_143906_55390e77`; title and objective contain
  `TGT-F2CA47CB9859`.
- Both production services are active.

## Deployment

- Branch: `codex/workstream-target-results-toggle`
- Implementation commit: `dcb2ab9`
- Rollback backup: `/opt/serbia-poc-ui-backups/workstream-target-wording-20260809T143641Z`
- Merge remains blocked on product validation.

## Review recommendation

Continue with product testing. Do not merge until explicit approval.

