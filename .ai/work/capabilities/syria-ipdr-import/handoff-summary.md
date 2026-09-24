# IPDR replacement handoff

Deployed runtime 2dc27ba0 as Syria ipdr-v1/profile9. Replaced200 prior IPDR rows with300 supplied records. Total424 rows; other124 records,86 locations and13 entities unchanged. Original CSV preserved; header SUBNETMASK trailing whitespace normalized, source values unchanged. Original record_id stored as source_record_id and shown as Record ID; internal REC-SYR-IPDR IDs remain navigation identities. Compatibility ip_address means ip_public; IP roles remain distinct. No actor/location inferred. Only2 records supply IMEI.

21 focused tests passed. JavaScript syntax and18-field viewer/string-ID/blank/zero harness passed. Live public data equals all18 source fields for all300 records. VM roles/gateway/UI readiness, Python-engine prebuilt index and original-ID retrieval passed. Browser verified300-row catalog, all18 table headers, original-ID record opening and all18 viewer fields without actor/location/map controls. No full-suite or live LLM investigation claimed.

Two source records (3001185062876120,3495155497992130) have end dates before start dates. Optional user clarification asked; no answer received at publication, so preserve exactly. These intervals must not be assumed valid overlap evidence. One IP has trailing whitespace, also preserved. Original backups/packages retained; private source/state backup /opt/demo-runtime/backups/syria-ipdr-2dc27ba0. Saved state copied with writers stopped.

Published to codex/syria-adint-import, included in draft PR82 with preceding ADINT/media changes. Not merged. Scenario and operations docs updated. Next: refresh IPDR; apply date correction only if user requests it. No remaining implementation blocker.
