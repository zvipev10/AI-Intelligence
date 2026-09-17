# Checkpoint 002 — production deployment

Deployed to the Serbia demo VM on 2026-09-17 from `codex/talia-enemy-assessments`.

Production verification:

- `hermes-gateway.service` and `serbia-poc-ui.service` are active.
- The main gateway multiplex allowlist contains `talia`, and the Talia MCP server is registered in both the profile and main gateway.
- Talia exposes 30 approved tools, including all six assessment tools and no target-bank or workstream tools.
- Real Evidence `EVD-REC-V2-006594` created and reopened `ASM-2F5C1B480ADD3046` with a Polygon assessment overlay.
- The target-bank SHA-256 was identical before and after assessment creation.
- A real `/api/investigate` request routed to `responding_agent=talia`, called `classify_question_intent`, `get_enemy_assessment`, and `present_requested_results`, and returned a standard `assessments` result layer.
- The UI service returned build `serbia-poc-v2.1`, dataset `v2.1`, 14,800 rows, and the deployed static app contains the assessment viewer/overlay implementation.

Two deployment defects were found and fixed during verification: the new multiplex profile required a profile-scoped API key, and its MCP server also had to be registered in the main gateway registry. Both fixes are encoded in the deployment scripts.
