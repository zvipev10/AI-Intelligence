# Exact Satellite coordinates

User supplied first pair for record1/site1 and second pair for record2/site2. Site1:35.065212338738036,36.28815755309795. Site2:35.06503531383431,36.289563371508734. New immutable satellite-v2/profile11 changes only the two location objects (both locales), preserving all event/media bytes. Update offline cache because location signature changes. Controlled VM upgrade preserves saved state and old release.

Validation: 22 focused tests passed; offline Python semantic cache rebuilt for 424 records. Deployed commit55e3fc88 successfully with UI/gateway/role health checks. Public API confirms satellite-v2/profile11, 424 rows, maintenance false, and both exact latitude/longitude pairs. Backup: /opt/demo-runtime/backups/syria-satellite-coordinates-55e3fc88. Published in draft PR82; not merged. No additional architecture or product documentation changes needed.
