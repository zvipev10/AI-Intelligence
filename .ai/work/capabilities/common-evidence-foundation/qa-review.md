# QA Review — Common Evidence Foundation

## Local verification
- UI, pipeline, routing, and viewer tests: 36 passed.
- MCP test suite: 60 passed, 1 intentional skip.
- Python compilation, JavaScript syntax, and `git diff --check`: passed.

## Production verification
- `hermes-gateway.service`: active.
- `serbia-poc-ui.service`: active.
- Default and Moshe configs include `prepare_evidence`, `persist_fused_evidence`, and `search_evidence` (plus the remaining evidence tools).
- Deployed MCP version: `0.4.0`.
- Deployed UI asset: `app.js?v=181`.
- Public `/api/status`: HTTP 200 with dataset v2.1 and 14,800 rows.
- Public English page: HTTP 200 and references the v181 asset.

## Result
Approved for user testing. Evidence layers remain demand-driven and raw records remain provenance.
