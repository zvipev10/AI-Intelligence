# Checkpoint 008 — MCP locale runtime deployed and verified

## Status
Complete and approved for this execution slice. The VM was rebooted after the first on-host index build exhausted resources; the prebuilt cache and final server revision were then deployed and production verification passed.

## Runtime dependency inventory

| Asset | Classification | Runtime use |
|---|---|---|
| Event projection CSV | Tool-visible | Exact, aggregate, fusion, linkage, and semantic records |
| Location JSON | Tool-visible | Resolution, presentation, geographic filters |
| Entity JSON | Tool-visible | Entity resolution and presentations |
| UAV JSONL | Derived-only | Inputs projection generation; not read by production MCP tools |
| Full raw CSV/JSONL | Derived/evaluator-only | Not read by production MCP tools |
| Scenario visibility JSON | Runtime policy, language-neutral | Time/layer visibility only |
| Target SQLite | Separate locale-isolated mutable store | Already completed in checkpoint 006 |

## Implementation
- Added manifest-validated `DatasetRuntime` instances for Hebrew and English.
- Runtime state now owns events, locations, entities, aliases, presentations, fusion indexes, source manifests, and semantic index instances.
- MCP call dispatch selects the runtime from `locale`; omitted/invalid locale remains Hebrew.
- English asset absence/contamination fails closed without falling back to Hebrew; Hebrew remains available independently.
- Event and location identifier parity is validated between runtimes.
- Semantic caches are isolated under `<semantic-root>/<dataset-version>/<locale>` and include locale, version, and source checksums in their manifest.
- Added `get_runtime_health` for locale, paths, checksums, counts, backend, and cache namespace.
- English tool schemas and representative payloads are scanned for Hebrew; deterministic generated labels are localized, and unknown Hebrew fails closed at the result boundary.

## Local QA
- Deterministic generator regenerated v2 and v2.1 and validated six English files with zero Hebrew; generated assets were byte-equivalent to tracked files.
- v2.1 parity: 14,800 events, 170 locations, and 28 entities per locale.
- Full MCP suite: 60 tests passed, 1 optional test skipped.
- Actual hybrid semantic indexes built separately for Hebrew and English. Alternating `he → en → he` loads reported the correct manifest locale and separate cache directories.
- Python compilation passed.

## Production deployment
- Deployed MCP server and v2.1 English event/location/entity assets.
- Pre-deployment backup: `/opt/serbia-poc/backups/mcp-locale-runtime-20260808T185826Z`.
- Startup import validated 14,800/170/28 records for both locales.
- `hermes-gateway` and `hermes-moshe-gateway` were active after restart.
- Exact search, location, entity, aggregation, intent, and runtime-health checks reached the semantic step without English payload rejection.

## Blocking production incident
The first English v2.1 hybrid semantic cache build ran for more than ten minutes on the low-memory VM. After the SSH client timeout, the host continued accepting TCP port 22 but could no longer complete SSH banners. Subsequent SSH/Paramiko attempts timed out. The likely orphaned builder exhausted memory/swap. No Oracle CLI or configured instance-management connector is available locally.

The validated local English v2.1 cache is ready at the ignored build path:
`data/semantic_index/v2.1/en/semantic_event_index_hybrid_embedding.pkl`.

## Recovery and final production verification
- The user rebooted the VM; no orphaned builder remained afterward.
- Uploaded the prebuilt cache to `/opt/serbia-poc/data/semantic_index/v2.1/en/semantic_event_index_hybrid_embedding.pkl` with `ubuntu:ubuntu` ownership.
- Deployed the final fail-closed server revision and restarted both gateways.
- Final deployment backup: `/opt/serbia-poc/backups/mcp-locale-runtime-final-20260808T193411Z`.
- English cache loaded successfully without rebuild; first semantic request completed in 16.147 seconds.
- Semantic manifest locale is `en`, cache exists in the English namespace, and no runtime load errors were reported.
- English health, exact search, location, entity, aggregation, intent, and semantic payloads all contained zero Hebrew characters.
- Alternating English/Hebrew/English calls returned to default locale `he` with no context contamination.
- All three services are active. No semantic builder remains.
- Both target databases remain empty with SQLite integrity `ok`.
- Post-verification memory: 508 MiB available; swap: 1.5 GiB free.

## QA recommendation
Approve Section 1 MCP locale runtime. Continue to Section 4 workstream isolation; the parent bilingual capability remains open.
