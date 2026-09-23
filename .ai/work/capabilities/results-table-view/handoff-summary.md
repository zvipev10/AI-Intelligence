# Table results view â€” handoff

Implemented and deployed to http://151.145.93.180. Syria remains active, dataset network-v1 unchanged (208 records, including 200 geometry-free IPDR records). Runtime source commit: 89e772d88add95b765857e4af0831f64f0987049.

## Behavior and changed files
- app.js, index.html, styles.css, demo_bootstrap.js: Table beside Map/Timeline; same existing table DOM, filters, record viewer and layer state. Full-height table exposes record links without geometry. Overlay minimization is preserved when switching back. Empty state is localized. Asset versions JS 204 / CSS 153.
- server.py, mcp_server/server.py, agent_result_pipeline.py: Table supported in English/Hebrew instructions, intent defaults, presentation tools, evidence references, catalog actions, result audit parsing and saved-memory reconstruction. Map for spatial questions; Timeline for chronology; Table for raw records, identifiers and geometry-free results. Legacy evidence view remains compatible.
- activate_demo.py: refresh role audit paths when selecting a dataset. Live QA found a previously stale empty-v1 audit destination that prevented structured results reaching the UI; all roles now use network-v1.
- Tests: test_results_table.py, test_results_table_ui.cjs, updated MCP evidence-reference and asset-version contracts.

## Checks
- Application discovery: 238 tests, 230 passed; eight existing baseline failures unchanged (chat/evidence old asset assertions, mobile recovery, Moshe/Talia frontend assertions, old canonical source manifest, two welcome-page assertions). No new regression failures.
- MCP: 74 tests, 72 passed / 2 skipped.
- Focused scenario/pipeline/media tests pass; scenario operator suite rerun after audit-path fix: 13 passed.
- Node: Table switching and same component, geometry-free record links, legacy recommendation, minimized/empty states, catalog filtering/restoration/error path, media rendering, JS syntax all pass.
- Public HTTP assets and catalog verified; 200 IPDR records advertise map=false.
- Live Hermes run table-qa-1790171203: 21.22 sec, recommended_view=table, catalog action events:IPDR/view=table, no action errors, two audited steps. Proof: /opt/demo-runtime/control/table-view-qualification.json.
- Activation verifies all three agent roles and their current audit namespaces. Runtime healthy.

## Publishing, assumptions and remaining risks
PR #76 stacks on #74; parent #67, child #75. Branch codex/results-table-view published. Not merged into main; merge dependency chain #69 -> #72 -> #74 -> #76. No dataset changes or added dependencies. Assumption: shared Table behavior is appropriate in both scenarios, with only Syria active. Manual browser interaction was not performed; automated JS and live API checks cover behavior. Existing baseline tests remain a separate cleanup task.

Backups: /opt/demo-runtime/backups/table-fc1c0f9 and table-89e772d; manifests pinned under releases/<commit>. Prior datasets and audit files preserved.

Next action: refresh the application and review the Table tab/record viewer; merge the reviewed PR stack. Suggested durable docs updates: describe Map/Timeline/Table choice in product context and record that scenario activation updates audit destinations with dataset identity in architecture/decisions. These decisions are preserved here pending broader documentation consolidation.

## User correction — IPDR schema presentation
IPDR table now shows IP address and IMEI instead of actor/location; its viewer and filter list omit actor/location, and its table has no map action. All values come from the existing structured fields, preserving leading zeros. Other sources retain their existing layouts. JS cache version 205. Focused Node regression, media and syntax checks pass. Static VM deployment follows publishing; no dataset or agent configuration change. Product-context documentation should describe source-specific IPDR columns.
