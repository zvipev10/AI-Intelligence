# Checkpoint 002 — baseline and implementation slice

User authorized steps 1–6 and accepted brief shared-gateway restarts. Countrywide Syria map and Kosovo active at completion are stated assumptions. Implementation child: #70; parent #67; draft PR #69.

## Baseline
Latest main d475d2e fetched before work. Deployed server.py, app.js, agent_routing.py and MCP server/catalog logic match source after newline normalization. Hermes commit 00bbfc690060d1323ddb2f065297c7425cb71c26. VM has 954 MiB RAM, 217 MiB available and 1003 MiB swap used at baseline. Private source/config/state backup: /opt/demo-runtime/backups/20260922T195952Z. Root-only old backup files required sudo tar; completed successfully. Live SQLite root stores were backed up via SQLite backup; final migration will occur with writers stopped.

## Implemented locally
Validated checksummed profiles and empty Syria package, persistent state namespaces, API generation fencing, browser bootstrap/storage isolation, country-specific map bounds, stable 16-layer empty catalog, shared bounded agent slot including OpenAI, queue cancellation/priority with aging, append-only and per-run audit, operator activation and one-time state migration scripts. No new dependencies. Inactive datasets and private state are not statically served in scenario mode.

Gateway uses one service with named active demo profiles. Root WhatsApp configuration remains; demo MCP bindings move out of root into active demo roles so the root cannot retain inactive Kosovo tools. Syria receives shared configuration/credentials and role definitions, no sessions/memories/cron jobs. No scenario reset during activation.

## Checks
Eight new scenario tests passed: package checksums, bad selection, isolation, empty MCP semantic search, catalog/map, stale API calls, private/inactive static path protection, serialized execution/drain. JS syntax and Python compilation passed. Baseline full suite: 220 tests, 8 existing failures (stale asset/source/UI assertions). Focused suite exposed an intermittent playback reset assertion; isolated rerun passed. Full post-change regression is running; no claim that all checks are green.

## Remaining before deployment acceptance
Exercise activation failures/recovery, provision stopped-state migration with checksum reconciliation, validate both profile tool bindings, sequential VM round trip, media availability, agent behavior and resource headroom. No VM runtime changes yet except private backup directory/archive creation. Review focus: state isolation, no replay after interruption, one-runtime activation boundaries.
