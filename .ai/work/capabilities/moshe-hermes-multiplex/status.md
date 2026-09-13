# Moshe Hermes multiplex status

- Phase: deployed and verified
- Goal: serve Moshe through the default Hermes gateway while preserving profile identity, sessions, tools, authorization, and audit isolation.
- Production topology: General uses the unprefixed API on port 8642; Moshe uses `/p/moshe` on the same listener with a distinct profile API key. Port 8643 is no longer listening.
- Profile isolation: Moshe retains his own `SOUL.md`, config, MCP allowlist, audit file, memory/session scope, and provider scope.
- MCP compatibility: this Hermes build discovers MCP servers once from the default profile. The default config therefore registers a uniquely named `serbia-events-poc-moshe` server, but General's `platform_toolsets.api_server` excludes it. Moshe's profile selects only that server.
- Transport isolation: Moshe explicitly disables API-server and WhatsApp adapters; the default profile owns both shared transports.
- Application routing: `@משה` uses `/p/moshe` and Moshe's key; normal traffic remains unprefixed General traffic.
- Verification: 13 focused tests pass on the VM. Moshe end-to-end called `classify_question_intent` and `search_target_candidates`; General independently called `classify_question_intent`, `aggregate_events`, and `present_requested_results` and returned 14,367 records.
- Service state: `hermes-moshe-gateway.service` is stopped and disabled but retained as a rollback artifact. `hermes-gateway.service` and `serbia-poc-ui.service` are active.
- Known Hermes diagnostic issue: its generic `platform_toolsets` warning does not recognize a profile-only MCP server name and may claim the toolset is unknown. The server is registered in the default discovery registry and Moshe's end-to-end tool calls prove the warning is a false positive.
- Rollback backup: `/home/ubuntu/deployment-backups/moshe-multiplex-20260913T162204Z`.
- Deferred: WhatsApp group-to-profile routing requires the exact Moshe group JID; no speculative route was added.
