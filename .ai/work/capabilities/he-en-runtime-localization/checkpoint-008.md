# Checkpoint 008 — MCP locale runtime implementation and degraded deployment

## Status
Implementation complete locally. Non-semantic production deployment completed, but final production acceptance is blocked because the first English hybrid semantic-index build exhausted the VM's resources and the host stopped completing SSH handshakes.

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

## Required recovery
1. Through the Oracle console, reboot the VM or terminate the orphaned `python3 -` semantic builder.
2. Confirm both gateway services and the UI service are active.
3. Upload the prebuilt English v2.1 cache to `/opt/serbia-poc/data/semantic_index/v2.1/en/` with ownership `ubuntu:ubuntu`.
4. Deploy the final fail-closed server revision from this checkpoint and restart both gateways.
5. Run the production English semantic query and verify manifest locale `en`, separate cache path, zero Hebrew, and `he → en → he` isolation.

## QA recommendation
Request changes / pause acceptance until VM recovery and semantic verification complete. The parent capability and Section 1 slice remain open.
