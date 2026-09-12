# Hermes MCP toolset migration status

- Phase: deployed and verified
- Incident: after the VM boot at 2026-09-12 22:20 IDT, all Hermes gateways reloaded legacy `mcp-*` platform toolset aliases and General answered that no MCP tools were available.
- Root cause: application deployment and profile provisioning code used generated `mcp-serbia-events-poc` / `mcp-intelligence-events-poc` aliases instead of the configured `mcp_servers` keys. The aliases date to the initial application commit; the restart exposed the stale configuration during fresh Hermes tool resolution.
- Fix: API platform toolsets now reference exact MCP server keys. A validating, atomic migration updates existing configs and refuses unknown toolsets.
- Production: migrated General, persistent General, and Moshe configs; restarted all three gateways; installed the corrected deployment script and migration utility.
- Verification: all three systemd services active; all three capability endpoints reachable; migration tests and isolated profile assertions pass on the VM.
- End-to-end smoke: General and persistent General both called `classify_question_intent`, `aggregate_events`, and `present_requested_results` and returned 14,367 records. Moshe called `classify_question_intent` and `search_target_candidates` for `REC-V2-006948` and returned a grounded zero-result answer.
- Residual observation: Hermes startup also logged MCP `CancelledError` messages immediately after the VM boot. The post-fix end-to-end tool calls prove the servers are currently connected; the old alias warning has not recurred after the controlled restart.
