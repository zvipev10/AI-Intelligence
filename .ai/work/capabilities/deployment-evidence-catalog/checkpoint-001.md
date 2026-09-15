# Checkpoint 001 — Catalog implementation complete

## Delivered
- Deterministic bilingual evidence catalog builder for all v2.1 records.
- Six-hour canonical fusion grouping with exact-only public object-class resolution.
- `evidence:all` catalog layer with map, table, and timeline capabilities.
- Manifest-only catalog counts and demand-loaded row artifacts.
- Deployment packaging and automatic local prebuild/upload.

## Dataset result
- Source records: 14,800.
- Raw records processed/projectable: 14,800.
- Cataloged observations and exact structured reports: 3,867.
- Validated fused evidence: 298.
- Rejected fusion groups: 9.
- Catalog total: 4,165 items (about 4.1 MB per locale).
- Ibar Bridge: 293 items, including 25 fused objects.

## UX/performance checkpoint
An initial all-projections build produced 15,098 rows and took 8.6 seconds to fetch in production. It was rejected because it duplicated raw public reports as symbols. The approved catalog still processes all raw records but presents only observations, exact structured extractions, and fused evidence.

## Regression status
- Existing target fusion semantics were preserved after a regression test caught an unsafe shared-helper change.
