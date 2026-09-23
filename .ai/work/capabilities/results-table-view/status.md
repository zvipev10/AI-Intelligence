# Status

Phase: implemented, deployed and qualified; ready for review/merge.
Owner: reviewer / product acceptance. Blockers: none for deployment; main integration awaits PR stack review.
Parent: #67 remains open. Child: #75 implemented, closes with #76 merge.
PR: https://github.com/zvipev10/AI-Intelligence/pull/76, base codex/syria-adint-ipdr (#74).
Runtime: 89e772d88add95b765857e4af0831f64f0987049; Syria/network-v1 active.
Latest: live Hermes IPDR request returns Table action successfully after correcting stale dataset audit paths. All role activation health checks pass.
Next: user refresh / review, merge dependency chain. Details: handoff-summary.md; checkpoints 001/002. No manual browser QA claimed.

Latest correction deployed: native IP/IMEI fields, no actor/location in IPDR table/viewer/filters. Runtime eb93c67f249fbbab7893bfdfa11ee8ba68e913c7, JS 205. Focused tests and public asset verification pass. Next: refresh browser / review PR #76.

English basemap deployed: 13fbd504b4f184a5756df1368adafb333ecd5644, JS 206. CARTO Voyager vector labels prefer English at every zoom; native names are fallback only when English is unavailable. Scenario bounds and overlays retained. Syntax/mock initialization checks pass; Syria tile, glyph and sprite requests return HTTP 200 with CORS. Public VM assets verified, Syria healthy. No manual browser rendering check. Backup /opt/demo-runtime/backups/map-13fbd50. Next: refresh browser and review PR #76. Suggested product-context update: English basemap labels independent of interface language.

Street/Satellite switch deployed: d4b6d54d0354941344fac030e7f11df04abc4d02, JS 207 / CSS 154. Top-right map switch selects Esri World Imagery under English CARTO labels. Street remains default. Captured basemap layer visibility changes preserve investigation overlays and camera; white outlined labels on imagery, original styling restored on Street. Imagery-source error falls back to Street with a visible status. Source credits shown. Synthetic timestamped Satellite records unchanged. Node basemap/Table/media and syntax checks pass; live imagery sample HTTP 200/CORS; public app/CSS hashes verified and Syria remains active. No manual browser rendering check. Backup: /opt/demo-runtime/backups/satellite-d4b6d54. PR #76 updated; not merged. Next: refresh app and choose Satellite. Suggested product-context update: basemap imagery is separate from collected dated imagery.
