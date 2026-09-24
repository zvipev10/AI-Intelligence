# Remove second call

Scope: remove REC-SYR-CALL-002 from both Syria locale datasets. Immutable call-media-v2/profile19 retains all other records, locations and media, with 443 records and one call. Rebuild the semantic cache and activate on VM with rollback backup. Verify removal in catalog, data API and search; preserve Call 1 exactly. Prior versions remain historical.

Completed: 17 targeted tests passed. Deployed c0cfe1f5 to VM with backup /opt/demo-runtime/backups/syria-one-call-c0cfe1f5. Live status reports 443 records and maintenance disabled. Both locale APIs contain only REC-SYR-CALL-001 with media; live Cellular Calls catalog count is 1. Published in draft PR85; not merged. Refresh the application to reload the active dataset. No further documentation changes required.
