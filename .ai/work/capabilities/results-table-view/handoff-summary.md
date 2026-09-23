# Table results view — handoff

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

## User correction — IPDR fields
IPDR table uses IP address and IMEI instead of actor/location. The viewer and filters omit actor/location; table has no map action. Structured values preserve IMEI leading zeros. Other sources retain their layouts. Focused Node table/viewer/filter/media tests, Python presentation test and JS syntax pass. Deployed and public assets verified: eb93c67f249fbbab7893bfdfa11ee8ba68e913c7, JS 205. Syria remains active. No dataset or agent configuration change. Backup: /opt/demo-runtime/backups/ipdr-eb93c67. Suggested product-context update: source-specific IPDR columns.

English basemap deployed: 13fbd504b4f184a5756df1368adafb333ecd5644, JS 206. CARTO Voyager vector labels prefer English at every zoom; native names are fallback only when English is unavailable. Scenario bounds and overlays retained. Syntax/mock initialization checks pass; Syria tile, glyph and sprite requests return HTTP 200 with CORS. Public VM assets verified, Syria healthy. No manual browser rendering check. Backup /opt/demo-runtime/backups/map-13fbd50. Next: refresh browser and review PR #76. Suggested product-context update: English basemap labels independent of interface language.

Street/Satellite switch deployed: d4b6d54d0354941344fac030e7f11df04abc4d02, JS 207 / CSS 154. Top-right map switch selects Esri World Imagery under English CARTO labels. Street remains default. Captured basemap layer visibility changes preserve investigation overlays and camera; white outlined labels on imagery, original styling restored on Street. Imagery-source error falls back to Street with a visible status. Source credits shown. Synthetic timestamped Satellite records unchanged. Node basemap/Table/media and syntax checks pass; live imagery sample HTTP 200/CORS; public app/CSS hashes verified and Syria remains active. No manual browser rendering check. Backup: /opt/demo-runtime/backups/satellite-d4b6d54. PR #76 updated; not merged. Next: refresh app and choose Satellite. Suggested product-context update: basemap imagery is separate from collected dated imagery.
