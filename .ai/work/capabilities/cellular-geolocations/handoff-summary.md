# Initial delivery

Deployed 1436fe79: Syria cellular-v1/profile14, 430 records. Live catalog has four Cellular Geolocations; two Cellular Calls carry both endpoint IMEIs. Public data and app217 assets verified. System-Python MCP loaded the 430-record cache and SIM identifier search returned two expected geolocations. 34 Python checks, shared table/viewer harness and JS syntax passed. Existing 424 records and Kosovo dataset/profile preserved. Backup /opt/demo-runtime/backups/syria-cellular-1436fe79. Draft PR84, issue83; not merged. Next: refresh application and review samples.

All six new records are synthetic, with explicit summaries/provenance. IMEIs are string identifiers; SIM values are DEMO-SIM-SYR-001/002, distinct from synthetic call numbers. Location uses existing catalog IDs, with record IDs/timestamps retained for map/timeline/viewer. No audio or transcript was generated. Shared UI supports the new schema; Syria alone includes its catalog/data. No architecture or dependency changes. Updated scenario/operations guides are authoritative; no further documentation change proposed.

# Coastal route follow-up

Deployed 28feea1a: Syria cellular-v2/profile15, 444 records and 100 locations. 18 geolocations include the four earlier samples, 12 ordered coastal route observations and two remote endpoint observations. Both calls are at route stop05 (35.133,36.117), with Side B at new location (35.12,36.03). Calls occur at09:46/09:50 during the device1 stop09:45–10:00 on September20. Route starts at Satellite site1 and ends near Baniyas seafront at11:15. 35 tests passed; offline cache rebuilt. Live API verified route/order/endpoints/counts and maintenance disabled. Service health/identity passed. Backup /opt/demo-runtime/backups/syria-cellular-route-28feea1a. Published in draft PR84, unmerged. Refresh application to load latest data.

Existing observations remain historical samples on September1; the new route is September20. The waypoints describe synthetic travel and are not road-snapped navigation directions. All prior non-call records and location coordinates remain unchanged. Scenario/operations documentation updated.

# Supplied Call 1 media and viewer

Deployed 65867569 successfully: call-media-v1/profile18, 444 records, maintenance disabled. Backup: /opt/demo-runtime/backups/syria-call-media-65867569. Public API confirms both transcripts and preserved scenario IMEI; all four live media files match local bytes exactly. Original MP3 and both supplied text files match attachments byte-for-byte. Browser playback verified through PCM WAV derivative after an embedded-browser MP3 crash. 36 Python checks, JS syntax and shared-table harness passed. Translation toggle, missing-media state and responsive width checked.

Changed areas: app.js/styles.css and cache versions; Syria immutable data/profile/media; MCP public call fields and deploy bundle; regression tests; docs/demo-scenarios.md and design-qa.md. Draft PR84 updated, not merged. Issue83 remains open pending review. The existing scenario IMEIs are preserved; source speaker IMEI is shown separately pending user clarification. No speech timecodes were supplied, so no synchronized highlighting is claimed. Refresh the VM application and open REC-SYR-CALL-001. No further architecture or product documentation updates required.

# Timeline, polygon and current call inventory

PR85 delivers removal of Call 2, calls-first Timeline with compact selectable entries and an adjacent nonmodal call viewer, and a translucent bottom-right polygon drawing control. Only Call 1 remains in Syria; its supplied media is preserved. Polygons close by clicking the first vertex after at least three distinct points, remain page-local, and trigger no further action. Escape cancels the unfinished draft.

Product, architecture, scenario and operations guides now own the corresponding current facts and checks. Checkpoints 006–008 preserve deployment/validation evidence. User authorized push and merge; use PR85 for final publication status. No additional documentation work is proposed. Refresh the VM application after release.
