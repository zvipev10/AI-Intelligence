# Separate cellular route start

User asks for a new location near site1, not exactly shared. Move only REC-SYR-CELL-ROUTE-001 to new LOC-SYR-CELL-START-001, 60m north of Satellite site1. Preserve Satellite location, all other records and call endpoints. Immutable cellular-v3/profile16: 444 records, 101 locations. Rebuild cache and deploy with backup.

Deployed 1f5bf201 as cellular-v3/profile16. Live coordinates verified: new start 35.065751931701584,36.28815755309795; Satellite site1 unchanged. Maintenance disabled. 35 checks passed. Backup /opt/demo-runtime/backups/syria-cellular-start-1f5bf201. Published in PR84, not merged.
