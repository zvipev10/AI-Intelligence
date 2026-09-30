# Handoff
Existing 300 IPDR source rows are now discoverable as a checksum-anchored evidence package. Records retain REC identity and exact source fields; missing IMEIs remain missing (two populated). Package metadata does not invent acquisition/case details or undocumented ip_out semantics.
Changed areas: shared ipdr_evidence module, source manifest, UI/MCP loaders and evidence resolver, evidence projection, catalog and viewer/Timeline, targeted tests, owning product/architecture/demo/decision docs. No additional storage or state migration.
Validation: 20 targeted Python tests; 12 foundation tests plus one skip; two JS test scripts and syntax/diff checks pass. Existing catalog-recovery harness failure reproduced on baseline. Browser visual review and deployment remain outstanding.
Publishing: local review branch prepared; remote publication attempted separately. No main update or production deployment.
